# Tools: vendor-neutral options

The baseline is defined by what it proves, not by which product produces it.
The tools below are **examples**, not recommendations, and every fact about
them was read from the linked official page on the date given. Pricing, free
tiers and limits change: read the current page before telling a user what
something costs, and never quote a price from this file.

Anything that adds a package, SDK, agent or container to the project is a
`dependency-guard` decision. This file only narrows the options.

## How to choose, for one developer

| Question | Leans hosted | Leans self-hosted |
| --- | --- | --- |
| Does anyone want to run and update another service? | No | Yes, and has a machine for it |
| Must the monitor survive the app's server dying? | Always yes for uptime: run the check somewhere else | Only if the checker runs on a different machine and network |
| Is data residency or keeping error data in-house a requirement? | — | Yes |

Default for a beginner's first launch: a hosted uptime check and alert, and
either a hosted tracker or a small self-hosted one. The uptime checker must not
share a machine with the app.

## Error tracking

| Tool | Facts checked | Source |
| --- | --- | --- |
| Sentry (hosted) | The Express guide initialises the SDK in an `instrument.js` file loaded with `node --import ./instrument.js app.js`, and verifies setup with a route that throws `new Error("My first Sentry error!")`. The page states the SDK sends user identity data (IP address, id) by default and documents a `dataCollection` option to control it. | https://docs.sentry.io/platforms/javascript/guides/express/ — checked 2026-09-28 |
| Sentry (self-hosted) | Self-hostable. Stated minimums: 4 CPU cores, 16 GB RAM plus 16 GB swap, 20 GB free disk; 32 GB RAM recommended. Comes with no guarantees or dedicated support. Usually too heavy to run beside a small app. | https://develop.sentry.dev/self-hosted/ — checked 2026-09-28 |
| GlitchTip | Open source, self-hostable, and also offered hosted. Its SDK docs point to "any Sentry-compatible SDK", so the same client code works against either. | https://glitchtip.com/documentation and https://glitchtip.com/sdkdocs — checked 2026-09-28 |

Because GlitchTip accepts Sentry-compatible SDKs, the SDK choice and the
backend choice are separate: the DSN in the environment variable decides where
events go.

Not verified here: current free-tier quotas for either hosted service. Read the
pricing page at the time.

## Uptime check and alert

| Tool | Facts checked | Source |
| --- | --- | --- |
| Uptime Kuma | Self-hosted, MIT licensed. Monitors HTTP(s), TCP, keyword, JSON query, ping, DNS, push and more; notifications through Telegram, Discord, Slack, Pushover, email (SMTP) and 90+ other services. | https://github.com/louislam/uptime-kuma — checked 2026-09-28 |
| Better Stack Uptime | Hosted. HTTP monitors, heartbeat (cron) monitors, alerting by email, SMS, phone call and Slack, on-call scheduling, status pages. | https://betterstack.com/docs/uptime/ — checked 2026-09-28 |

Uptime Kuma's push monitor and Better Stack's heartbeat monitor both cover the
"backup job did not run" case later, without a second tool.

Not verified here: whether Better Stack currently has a free plan (the docs
page does not say). Read the pricing page at the time.

## Logs

Start with what the host already collects from stdout (the platform's log view
or CLI). A log shipping or search product is a later step.

## Later, not in the baseline

| Tool | Facts checked | Source |
| --- | --- | --- |
| OpenTelemetry | A vendor- and tool-agnostic framework for generating, exporting and collecting traces, metrics and logs. Not an observability backend: storage and visualisation are left to other tools. | https://opentelemetry.io/docs/what-is-opentelemetry/ — checked 2026-09-28 |
| Grafana | Open source; queries, visualises, alerts on and explores metrics, logs and traces wherever they are stored. | https://grafana.com/docs/grafana/latest/introduction/ — checked 2026-09-28 |

Both are reasonable when the app has more than one service, or someone asks
for metrics and dashboards. Neither is needed to answer *who finds out first*.

## Health checks

The liveness/readiness distinction and the warning against checking
dependencies in liveness come from
https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
(checked 2026-09-28). Platforms that are not Kubernetes have their own
health-check setting; read the platform's docs for which path it calls and what
it does on failure, and record that in the runbook.
