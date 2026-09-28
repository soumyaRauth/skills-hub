# Example — an alert proven by stopping the app on staging

Illustrative. Names and times are invented to show the shape of the record.

## Situation

`.observability/baseline.md` shows UPTIME `ADDED` (external check on
`https://staging.example.app/readyz`, last probe successful) and ALERT
configured to the developer's phone through the checker's push notification,
threshold 3 consecutive failures. The alert has never fired.

## Request

> Set up alerting so I know when the site is down.

## Response

```
⚡ Observability Baseline — alert configured but never fired

ALERT          MISSING (never proven)   configured: push to phone after 3 failed checks
NEXT           Stop staging and watch the alert arrive. OK to stop staging now?
```

Stopping staging is an outward action, so it waits for a yes
(`.delivery/config.yml` has no autonomy entry for it).

## After the yes

1. Staging's `fly.toml` has `auto_start_machines = true`, so a probe would
   start a stopped Machine again. The test uses a second check pointed at
   `/readyz` with `DATABASE_URL` pointed at a stopped scratch database instead,
   which returns 503 without depending on auto-start. (Alternatively: disable
   auto-start on staging for the test and `fly machine stop <id>`.)
2. The checker's history shows the failures. The developer reports: *"got it,
   push arrived"*. Recorded `SUPPLIED`, with the time they gave.
3. The scratch database is started again; the checker records recovery; the
   developer reports the recovery push arrived.
4. First attempt, before the one above, nothing arrived: phone notifications
   for the checker app were off. That is the failure this proof exists to catch.
   Fixed on the phone, and re-run.

```
OBSERVABILITY  bookshelf-staging — alert proof
ALERT          ADDED       503 on /readyz → push after 3 failed checks; received (SUPPLIED by developer, 2026-09-28); recovery received
NEXT           Point the same alert at the production check once it exists.
```

`.observability/baseline.md` records the channel, the threshold and why (a
deploy restart on staging stayed under it), and the date. `docs/runbook.md`'s
*Who gets alerted* table is filled in.

## What it did not do

- Stop production to test.
- Report the alert as working because the configuration looked right.
- Add a second or third alert.
