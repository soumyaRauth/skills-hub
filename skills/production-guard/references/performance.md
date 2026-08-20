# Performance

Contextual, not reflexive. Do not report every loop. Report the things that
change behavior as data grows, and say what volume makes them matter.

## Establish the scale first

Before judging anything, find what the real numbers plausibly are:

- What does this operate on — rows, files, requests?
- What is the current volume, if the repository shows it (seeders, fixtures,
  pagination defaults, existing limits, migration data)?
- What is the growth shape — bounded per user, or unbounded per tenant?

If the repository gives no signal, say so and reason in relative terms: "linear
in the number of selected items, with one query per item". Do not invent
benchmarks or cite numbers you did not measure.

## The reliable findings

**N+1 queries.** One query to fetch a collection, then one more per item. Look
for loops containing repository calls, lazy relation access, or serializers that
touch relations. This is the single most common real performance defect and it
is visible statically.

**Unbounded result sets.** A query with no limit, a full-table export, an
in-memory `all()` before filtering. Fine at 100 rows, fatal at 10 million.

**Everything in memory.** Loading a collection to count it, building an entire
export in memory before writing, accumulating results in a list that grows with
input size.

**Missing pagination.** An endpoint returning a collection with no page
parameter, or a UI that requests everything and filters client-side.

**Synchronous expensive work.** Report generation, external API calls in a
loop, image processing, or large emails inside a request. Ask what the request
timeout is and whether the work can exceed it.

**Missing indexes.** A new query filtering or joining on an unindexed column,
especially one added by this change. Check the migration for the index, not just
the column.

**Resource exhaustion under concurrency.** Unbounded parallelism, a connection
per item, no rate limiting on an expensive endpoint.

## Reasoning about scale

Where you can, reason across bands rather than a single point:

```
100 records      — 101 queries, ~acceptable
10,000 records   — 10,001 queries, request timeout likely
1,000,000 records— not viable; needs batching and a background job
```

Only use concrete numbers the repository or the domain supports. If you ran
something, label it EXECUTED and give the measurement. If you reasoned, label it
ANALYZED — a query count derived from reading a loop is legitimate analysis, but
it is not a measurement.

## Severity calibration

- **Blocker**: the operation cannot complete at the volumes the feature is
  explicitly designed for.
- **High**: works today, degrades badly within plausible near-term growth, or
  risks exhausting a shared resource under concurrency.
- **Medium**: measurable inefficiency with a clear fix and no near-term cliff.
- **Low**: micro-optimization. Usually not worth reporting at all.

A slow endpoint nobody calls is not a blocker. A 30-second bulk operation behind
a 30-second gateway timeout is.
