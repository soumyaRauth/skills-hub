# Example — a beginner's first launch

Illustrative. The repository matches the `launch-no-monitoring` fixture; the
evidence lines show the shape real evidence takes, not output from a real run.

## Request

> We launch next week. How will we know if something breaks in production?

## What was read

- `fly.toml`: Fly.io app, `http_service` with no `checks`,
  `auto_start_machines = true`, `min_machines_running = 0`.
- `src/server.js`: `console.log(req.method, req.url, req.body)` on every
  request (request bodies in the logs), `console.log("error", err)` in each
  catch, no health route, no error handler.
- `package.json`: `express`, `pg`. No tracker SDK, no logger.
- `README.md`: managed Postgres, `DATABASE_URL` as a Fly secret.
- No `.observability/`, no `docs/runbook.md`, no `.release/`.

## Response

```
⚡ Observability Baseline — first production deploy, nothing would tell you it broke

OBSERVABILITY  bookshelf — first production deploy next week
LOGS           MISSING     console.log of raw request bodies; no request id. Next: structured lines + X-Request-Id, bodies out
HEALTH         MISSING     no route; fly.toml has no checks. Next: /livez and /readyz (SELECT 1)
ERRORS         MISSING     errors only printed. Next: a tracker (hosted or self-hosted), through Dependency Guard
UPTIME         MISSING     next: an external HTTP check on /readyz, not on the Fly machine itself
ALERT          MISSING     next: one alert to the channel you read at night; prove it on staging
BACKUPS        MISSING     managed Postgres: are backups on, and has one ever been restored? Unknown
RUNBOOK        MISSING     next: docs/runbook.md
NEXT           Logs and health are code in this repo; I can add them now and prove them locally.
```

Today, if the app goes down at night, a user tells you first. Two questions
before the rest: which channel do you actually read at night, and do you want
hosted or self-hosted for the tracker and the uptime check?

## What happens next, with a yes

1. Logs and health, as ordinary work (ProofBuild proves them):
   - A middleware sets `req.id` from `X-Request-Id` or `crypto.randomUUID()`,
     returns it in the response header, and every line is JSON with `request_id`.
     `req.body` is no longer logged.
   - `/livez` returns `{"status":"ok"}` without touching the database;
     `/readyz` runs `SELECT 1` and returns 503 on failure.
   - `fly.toml` gets an `http_service.checks` entry on `/readyz`. On Fly.io
     those checks affect routing only, which is readiness behavior.
   - Proof, locally: `/readyz` 503 with Postgres stopped and `/livez` still 200;
     a curl with `X-Request-Id: ob-proof-1` found as one JSON line.
2. `HANDOFF → dependency-guard: error tracker SDK for express`. After its
   decision, the SDK goes in, with the DSN from an environment variable and
   personal-data collection limited. A gated `/debug/error` route throws once on
   staging, the event is seen in the tracker, and the route is removed.
3. Uptime and alert: the human creates the external check (a hosted checker, or
   Uptime Kuma on a machine that is not the app's), and the alert is proven as
   in `alert-proven-on-staging.md`. Note for this app: with
   `auto_start_machines = true` and `min_machines_running = 0`, a stopped
   machine is started again by the probe itself.
4. Backups: the user checks the provider's backup setting and reports it
   (`SUPPLIED`). Then one restore into a new instance, and a row count compared.
5. `docs/runbook.md` and `.observability/baseline.md` from the templates.

## What it did not do

- Recommend a metrics stack, tracing or dashboards.
- Say whether the launch is safe. That is Production Guard's call, if asked.
- Mark anything `ADDED` before it fired.
