# Scope Analysis

Scope is the cheapest hypothesis killer available. Establishing that a symptom
affects one account and not the other 4,000 eliminates every explanation that
would affect everyone — before a single line of application code is read.

## The scope grid

Fill five dimensions. Each cell is `all`, a named subset, or `UNKNOWN`.

| Dimension | Values to distinguish |
| --- | --- |
| **Population** | all users · one tenant · one role · one account · one session |
| **Location** | all regions · one region · one network · one device class · one browser |
| **Surface** | all operations · one endpoint · one page · one job · one record type |
| **Time** | always · since a moment · during a window · at a period (peak, nightly) |
| **Persistence** | every attempt · a fraction of attempts · once |

The grid's value is that each filled cell excludes explanations. One browser
excludes the backend. One tenant excludes shared infrastructure. A fraction of
attempts excludes anything deterministic in the request path.

## Contrasts beat descriptions

Prefer evidence of the form *A differs from B* over evidence of the form *A is
bad*. A latency number alone is unreadable; the same number next to an
unaffected comparison is a conclusion.

| Contrast | What it eliminates |
| --- | --- |
| Affected user vs unaffected user, same operation | Anything global: the code path, the query, the deploy |
| Current version vs previous version | Everything that did not change |
| Region A vs region B | Application logic, if both hit the same code |
| One endpoint vs another on the same host | Host-level causes — CPU, memory, connection pool |
| Failed request vs successful request, same endpoint | Deterministic causes; points at input, state, or instance |
| Before deploy vs after deploy, same request shape | Traffic, data growth, external drift |
| Same request over two networks | Everything server-side |

Design the contrast so exactly one variable differs. A comparison of a
different user, on a different page, at a different time, from a different
country, proves nothing.

When no natural contrast exists, construct one: run the same request twice with
one variable changed, or replay a failing input against the previous version.

## Intermittency has a shape

"Random" is a statement about the observer, not the system. Find the pattern:

| Pattern | Typical mechanism |
| --- | --- |
| A stable fraction of requests | One bad instance in a pool, or one shard/replica |
| Bursts with quiet gaps | Rate limiting, retry storms, garbage collection, cron overlap |
| Only under load | Contention: pool exhaustion, lock waits, queue depth |
| Only for some records | Data-dependent: nulls, unicode, size, legacy rows, missing relations |
| First request after idle | Cold start, connection expiry, cache miss, token refresh |
| Only at a time of day | Scheduled jobs, backups, third-party maintenance, timezone boundaries |
| Increasing over time since restart | Leak: memory, file handles, connections |

Test the shape before theorizing about the mechanism. Twenty timestamped
failures are usually enough to distinguish "one instance in five" from "only
under load".

## Time correlation

When the symptom has a start, line up everything that also has a timestamp:
deploys, merges, migrations, configuration and flag changes, dependency
upgrades, infrastructure events, traffic changes, data volume milestones, and
external provider incidents.

```bash
git log --since="3 days ago" --pretty=format:'%h %ad %s' --date=iso
git log --since="3 days ago" --name-only --pretty=format:'--- %h %s'
```

Two rules keep this honest:

1. **Alignment is a lead, not a verdict.** Something always changed near the
   start of any incident.
2. **Establish the start independently of the suspect.** A start time inferred
   *from* the deploy time cannot then be evidence *for* the deploy.

If several candidates align, the tie is broken by an experiment — a revert, a
version comparison, a flag toggle — not by which one looks most suspicious.
See `regression-windows.md`.

## Scope changes the layer set

Scope hands you the layer triage directly:

```
one browser only          → frontend, client
one region only           → CDN/edge, regional infrastructure, network path
one tenant only           → tenant configuration, tenant data shape, per-tenant limits
one endpoint only         → that handler and its dependencies
everything, everywhere    → shared infrastructure, database, a global deploy
one user, everything slow → that user's connection or device
```

Write the exclusions down. "Frontend not investigated: symptom reproduces via
API client with no browser involved" is a finding — it tells the next reader
that layer was decided, not forgotten.
