# Example — Performance

Performance requests are where invented numbers are most tempting and most
damaging. The rule is simple: **measure, change, measure again** — or say what
could not be measured.

---

**Developer:**

> The dashboard is slow. Add caching.

---

## 1. Measure before believing the mechanism

The request names a mechanism (caching) and an objective (fast dashboard). The
objective is the contract; the mechanism is a proposal that has to survive
measurement.

```
Repository   Django + PostgreSQL, django-debug-toolbar available in dev
Fixture      seed script exists: python manage.py seed_demo (2k orders)

Baseline — GET /dashboard/ with the seeded dataset
  Wall clock    3.9s – 4.4s over 10 runs (p50 4.21s)
  SQL queries   143
  Slowest       0.04s  →  no single slow query
```

143 queries, none slow: that is an N+1, not a computation cost. Caching would
store the result of a fundamentally expensive assembly and add a staleness
problem to the existing latency problem — while leaving the first request, every
invalidation, and every new user exactly as slow.

Stated in two sentences, then the root cause is fixed:

> The measured cost is 143 queries per load from an unbatched relation fetch,
> not repeat computation — a cache would hide it on the second request and leave
> the first one unchanged. Fixing the query pattern; if you still want a cache
> on top afterward, that's a separate contract.

## 2. Contract

Risk: **medium** — read path, no data mutation, but it touches a query shared by
two views.

```yaml
objective: "The dashboard loads substantially faster, measured"
risk: medium
requirements:
  - { id: PERF-001, priority: critical, description: "Dashboard query count drops from 143 to fewer than 10", proof: { type: benchmark } }
  - { id: PERF-002, priority: critical, description: "Dashboard p50 wall-clock time improves measurably against the recorded baseline", proof: { type: benchmark } }
  - { id: PERF-003, priority: critical, description: "The rendered dashboard is identical — same orders, same totals, same ordering", proof: { type: integration } }
  - { id: PERF-004, priority: high,     description: "The orders list view, which shares the same queryset, is unchanged", proof: { type: regression } }
  - { id: PERF-005, priority: normal,   description: "Production-scale behavior", proof: { type: manual } }
```

PERF-003 is the requirement that makes the rest safe. Optimizations that quietly
change the result set are the classic failure of this kind of work.

## 3. Verify

```
Fix   select_related("customer") + prefetch_related("items__product") on the
      dashboard queryset (orders/views.py:38)

Measurement — identical command, fixture, and machine as the baseline
  Command       python manage.py bench_dashboard --runs 10
  Queries       143  →  4          PERF-001  PASS · Level A
  Wall clock    p50 4.21s → 1.87s  PERF-002  PASS · Level A
                (local dev, 2k-order seeded fixture, 10 runs)

PERF-003  PASS · Level A
  Rendered HTML compared before/after: identical order ids, totals, ordering.

PERF-004  PASS · Level A
  python manage.py test orders   →  38 passed
```

## 4. What could not be measured

```
PERF-005  HUMAN · Level D
  Measured on local hardware against a 2,000-order fixture. Production data
  volume, hardware, connection latency, and cache state differ. The query-count
  reduction (143 → 4) transfers; the wall-clock number does not.
```

That distinction is the honest part. A structural improvement of 143 queries to
4 is real everywhere. `4.21s → 1.87s` is a fact about one laptop.

## 5. What the developer sees

```
⚠ REVIEW REQUIRED

Dashboard — 143 queries per load reduced to 4

The measured cost was an N+1, not repeat computation, so I fixed the query
pattern rather than adding a cache.

Queries        143 → 4          (measured)
p50            4.21s → 1.87s    (local, 2k-order fixture, 10 runs)
Requirements   4/5 verified
Rendered output identical; orders list view unchanged (38/38 tests)

Not verified:
  Production-scale timing. The query reduction transfers; the wall-clock
  number is local. Want a cache on top of this? Separate contract.
```

---

## What this example demonstrates

- The requested mechanism was overridden by **evidence**, not preference, and
  the override was stated in two sentences before any code changed.
- Baseline first, same command after. Both numbers appear; neither is estimated.
- The "unchanged output" requirement is what separates an optimization from a
  behavior change.
- Two kinds of measurement are distinguished: a structural one that transfers to
  production and a wall-clock one that does not. Reporting the second as if it
  were the first is the ordinary way performance claims become false.
- The status is `⚠ REVIEW REQUIRED`, not `✓ VERIFIED`, because one requirement
  is Level D. Four Level-A wins do not upgrade the fifth.
