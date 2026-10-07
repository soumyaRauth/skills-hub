# The baseline, item by item

## Contents

- Logs
- Health
- Errors
- Uptime
- Alert
- Backups
- Runbook

Each item: what good looks like for one developer, how to add it, and the exact
proof. The proof is the part that is never skipped. An item without a performed
proof is `MISSING (never proven)`.

Commands are examples. Use the project's own stack, host CLI and scripts.

## Logs

**Good looks like:** one line per event, machine-readable (JSON lines or
`key=value`), written to stdout so the host collects it. Every line inside a
request carries a `request_id`. Errors carry the error type and message, and the
stack goes to the error tracker. A level field (`info`, `warn`, `error`).

**Never in a log line:** passwords, tokens, API keys, cookies, session ids,
`Authorization` headers, full request bodies of sign-in or payment forms, card
numbers, and personal data (email, name, address, phone, IP where the project
treats it as personal). An opaque internal user id is fine. When unsure what the
project counts as personal data, `standards-compass` decides.

**Add:**

- Prefer the framework's or an already-installed logger. A new logging package
  is a `dependency-guard` decision.
- Take `request_id` from an incoming `X-Request-Id` header if the host or proxy
  sets one, otherwise generate one (`crypto.randomUUID()` in Node,
  `uuid.uuid4()` in Python). Return it in the response header so a user report
  can quote it.
- Replace `console.log` of objects that might hold request bodies with explicit
  fields.

**Prove:**

1. Send one request with a known id: `curl -H 'X-Request-Id: ob-proof-1' <url>/livez`.
2. Find it in the host's log output (`fly logs --no-tail` on Fly.io,
   https://docs.fly.io/flyctl/logs/, checked 2026-09-28; `docker logs`,
   `journalctl -u <unit>`, or the platform's log view): the line parses as structured and carries
   `ob-proof-1`.
3. Grep the recent output for obvious secret shapes (`password`, `token`,
   `authorization`, `@` in an email-shaped field). Report what was checked.

## Health

Two endpoints with different jobs. The distinction comes from Kubernetes, and it
applies to any host that restarts a process or routes traffic based on a check.

| Endpoint | Checks | On failure the host should |
| --- | --- | --- |
| `liveness` (e.g. `/livez`) | Only that the process can answer: no database, no downstream calls | Restart the process |
| `readiness` (e.g. `/readyz`) | That the app can serve: database reachable with a trivial query, required config present | Stop sending it traffic until it passes again |

Kubernetes documentation warns against checking back-end dependencies in the
liveness probe: a database blip would restart every instance and cause a
cascade. Liveness checks the app's own health; readiness additionally checks
the back-end services it needs.
(https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/,
checked 2026-09-28)

Platforms differ. Fly.io's `http_service.checks` affect routing only: a failing
check takes the Machine out of load balancing and does not restart it, so it
behaves like readiness (https://docs.fly.io/reference/configuration/, checked
2026-09-28). Read the target platform's own docs for what its check does.

A single-process app on a platform with one health-check setting points that
setting at readiness only if a failing database should take the app out of
rotation; otherwise at liveness, with readiness used by the uptime check.
Say which, and why, in the runbook.

Neither endpoint returns versions, hostnames, connection strings or stack
traces. `{"status":"ok"}` or a short failure reason is enough.

**Prove:**

1. Both return 200 with everything up.
2. Stop the database (locally or on staging, never production): liveness still
   200, readiness non-200 (503).
3. Start it again: readiness back to 200.

## Errors

**Good looks like:** unhandled exceptions and explicitly reported errors land in
an error tracker with stack trace, release/commit, environment, and the
`request_id` as a tag. Personal data collection is off or limited unless the
project decided otherwise. The tracker's key (DSN) comes from an environment
variable.

**Choose:** hosted or self-hosted, see `tools.md`. The SDK is a
`dependency-guard` decision. When nothing can be added, the fallback is a
top-level error handler that logs one structured `error` line with the
`request_id`, plus an alert on error lines if the log host supports one. Say it
is the fallback.

**Prove:**

1. Add a temporary route or command that throws a known error (the Sentry
   Express guide uses a `/debug-sentry` route that throws
   `new Error("My first Sentry error!")`,
   https://docs.sentry.io/platforms/javascript/guides/express/, checked
   2026-09-28). Protect it or remove it after: an unauthenticated route that
   throws on demand is a small denial-of-service surface.
2. Call it on staging.
3. See the event in the tracker, with stack trace and `request_id`. Record the
   event link (not the DSN) in `.observability/baseline.md`.
4. Remove or gate the route.

## Uptime

**Good looks like:** a check from outside the app's own network against the
real public URL (readiness, or liveness when readiness is too strict for
public exposure), at an interval the service offers, on HTTPS. Keyword or
status-code match, not only "TCP port open". A self-hosted checker on the same
machine as the app is not external: when the machine dies, so does the check.

**Prove:** the check shows at least one successful probe of the production (or
staging) URL, read from its own history, with the date.

## Alert

**One alert.** It fires when the uptime check fails, and reaches one human on a
channel they read at night: phone push, SMS, a chat app with notifications on.
Not a shared email inbox. Add the recovery notification too, so the human knows
it is over.

**Threshold that does not page for noise:** require more than one consecutive
failed check before alerting (most services call this retries, confirmation
period or "down after N failures"), so a single slow response or a deploy
restart does not page. Pick the number from the service's own setting and the
deploy's restart time observed on staging; do not invent one. Record the chosen
value and why in the runbook.

**Later, not now:** an alert on error-tracker volume, or on a failed backup job
(a heartbeat/cron monitor). Name them once as next steps.

**Prove** (needs a yes, rule 7):

1. On staging, stop the app (`fly machine stop <id>`, `docker stop`,
   `systemctl stop`), or point a second check at a URL that returns 503.
   Never production. Watch for hosts that start a stopped app on the next
   request: on Fly.io, `auto_start_machines` starts Machines "when a new request
   is made", so the uptime probe itself can wake the app and the alert never
   fires. Test against the failing URL instead, or disable auto-start on
   staging for the test (https://docs.fly.io/reference/configuration/ and
   https://docs.fly.io/flyctl/machine-stop/, checked 2026-09-28).
2. Wait for the alert on the named channel. The human confirms receipt; record
   it `SUPPLIED`, with the time they report.
3. Start the app again; confirm the recovery message.
4. If it did not arrive, the alert is `MISSING`, whatever the configuration
   says. The usual causes: notifications muted, wrong channel, retries set so
   high it never fired during the test.

## Backups

**Good looks like:** automatic backups on a schedule, stored somewhere other
than the app's own disk, kept for a period the project decided (retention of
personal data is a `standards-compass` question), and **restored once**.

A backup that has never been restored is not a backup yet. It is a file.

**Prove:**

1. Take or pick a recent backup.
2. Restore it into a scratch database, never over a live one. For PostgreSQL:
   plain dumps restore with `psql -X --set ON_ERROR_STOP=on <scratch_db> < dumpfile`
   into a database created with `createdb -T template0 <scratch_db>`; custom or
   directory format dumps restore with `pg_restore -d <scratch_db> <file>`
   (https://www.postgresql.org/docs/current/backup-dump.html, checked 2026-09-28).
   Managed databases: the provider's restore-to-new-instance or point-in-time
   restore, into a new instance.
3. Read back one known row (a count of a table, the newest record's timestamp)
   and compare with the source.
4. Drop the scratch database. Record the date, the backup it came from, and what
   was compared.

A backup job that fails silently is its own gap: name a heartbeat check on the
job as a next step.

## Runbook

`docs/runbook.md`, from `../templates/runbook.md`. Written for someone tired and
alone. Every command in it was run once while writing it; a command that could
not be run is marked `(not run: <why>)`. It covers: how to check health, where
the logs are and how to find a request id, where errors show up, how to roll
back (link to the release procedure; `release-engineer` owns it), how to restore
a backup, and who gets alerted on what channel.
