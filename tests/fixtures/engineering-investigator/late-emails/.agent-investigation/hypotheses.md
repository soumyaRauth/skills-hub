# Hypotheses

## H3 — Queue backlog: jobs wait for a free worker
Plausible     Delay is ~30 min and uniform, which fits waiting rather than sending.
Kill          Queue wait is short for delayed jobs, or the time is inside the job.
Evidence for  —
Evidence vs   —
Status        Investigating          Confidence  Medium
Next          Compare enqueued→started and started→finished for delayed vs on-time jobs.

## H4 — Slow job runtime (template render or attachment)
Plausible     Some templates are heavier; a slow render would delay the send.
Kill          Runtime is comparable for delayed and on-time jobs.
Evidence for  —
Evidence vs   —
Status        Investigating          Confidence  Low
Next          Same measurement as H3 — one experiment settles both.

## H5 — Scheduler or cron misconfiguration
Plausible     A batched or scheduled send would explain a fixed ~30 min offset.
Kill          Sends are triggered per order, not on a schedule.
Status        Blocked — no access to the production scheduler configuration.

## H1 — The email provider is slow to deliver  ·  DISPROVEN
Killed by     E3 — the provider accepts with 202 and the delay is already present
              in our own send timestamp. Delivery is not where the time goes.

## H2 — Orders enqueue their email late  ·  DISPROVEN
Killed by     E4 — enqueue timestamps track order creation within a second, for
              delayed and on-time orders alike.
