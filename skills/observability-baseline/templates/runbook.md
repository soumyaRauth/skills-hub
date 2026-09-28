# Runbook — <app>

Written for whoever is on call, tired, alone. Every command below was run once
while this was written; a command that was not is marked `(not run: <why>)`.
Secrets are never in this file: only the names of the environment variables
that hold them.

Last reviewed: <YYYY-MM-DD>

## Who gets alerted

| Alert | Fires when | Goes to | Channel |
| --- | --- | --- | --- |
| <app> down | <N> consecutive failed checks of <url>/readyz (<service>) | <person> | <phone push / SMS / chat> |

Threshold chosen because: <deploy restart observed at … on staging; one slow
request must not page>.

## Is it healthy?

```
curl -fsS <url>/livez     # process answers; restart if this fails
curl -fsS <url>/readyz    # can serve (database reachable); 503 = look at the database first
```

Uptime history: <link to the check, no tokens in the URL>

## Logs

Where: <`fly logs --no-tail` / `docker logs <container>` / platform log view>

Find one request: every response carries `X-Request-Id`; search the logs for
that value.

## Errors

Where: <error tracker project link>. Filter by the `request_id` tag.
Tracker key: environment variable `<SENTRY_DSN or equivalent>`.

## Roll back

See <link to the release procedure, e.g. .release/ or docs/release.md>.
If there is none yet: <the platform's rollback command, from its docs, dated>.

## Restore a backup

Backups: <where, how often, kept how long>.
Last restore test: <YYYY-MM-DD>, into <scratch database>, compared <what>.

```
<exact restore commands, into a NEW database; never over the live one>
```

## After an incident

Write down: what happened, who noticed first (us or a user), and the one signal
that would have caught it sooner. Add it to `.observability/baseline.md`.
