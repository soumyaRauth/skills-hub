# Example — Correlation with a deploy, promoted to cause

Everything started after the deploy. That sentence is where this investigation
begins, not where it ends.

---

**Report:**

> Checkout became very slow since yesterday's release.

---

## Phase 0 — Access

```
Available      repository, git history, deploy log (deploys/2026-08.log),
              API access log with per-request duration, local dev environment,
              test suite
Not available  APM traces, production database
```

Lane: **INCIDENT** — production impact on a money path, more than one plausible
layer. Workspace: `incident.md`, `hypotheses.md`, `evidence.md`, `experiments.md`.

## Phase 1 — Normalize

```
Symptom     Elevated latency on POST /checkout       FACT
Who         Unknown — "customers"                    UNKNOWN → resolved in Phase 2
What        Checkout submit                          FACT (report)
Since       "yesterday's release"                    ASSUMPTION — must be checked
                                                     independently of the deploy
```

The last line matters. If the window is taken from the deploy time, the deploy
cannot then be evidence for itself.

## Phase 2 — Establish the window independently

```
E1  FACT  POST /checkout, hourly p95 from the access log:
          08-25 12:00 → 298 ms · 13:00 → 310 ms · 14:00 → 1.42 s ·
          15:00 → 2.09 s · 08-26 09:00 → 2.14 s
          source: logs/api-2026-08-2*.log
E2  FACT  Other endpoints, same hours: p95 within 8% of their prior values
E3  FACT  Request volume 08-25 13:00 vs 15:00: 1,204 vs 1,187 (flat)
E4  FACT  Failure rate unchanged (0.3%) — slow, not failing
```

Window: `[08-25 13:00, 08-25 14:00]`. Scope: one endpoint, all tenants, every
request, persistent. Derived from latency data, not from the release notes.

## Phase 3 — What changed inside the window

```
E5  FACT  deploys/2026-08.log: release v1.9.0 completed 08-25 13:52
E6  FACT  git log v1.8.4..v1.9.0 — 7 commits; one touches the checkout path:
          a4f1c92 "Add gift-wrap options to cart serializer"
E7  FACT  No migrations, no lockfile change, no config change in the window
```

## Phase 4 — Hypotheses

```
H1  a4f1c92 added per-item work to the checkout response
    Kill: v1.8.4 is equally slow on the same input, or the added code does
          not execute on the slow requests
H2  Deploy-restart effects (cold cache, cold pools)
    Kill: latency persists 20 h after the deploy — restart effects decay
H3  Data growth crossed a threshold at the same time
    Kill: latency is flat across cart sizes, or the pre-deploy version is slow
          on the same data
H4  A dependency or infrastructure change shares the window
    Kill: nothing else changed (E7) and per-instance latency is uniform
H5  Traffic change
    Kill: volume flat (E3)
```

H5 is disproven on arrival by E3, and H2 by E1 (still slow the next morning).
Both are recorded as `Disproven` rather than left out — that is what stops the
next session from re-checking them.

Two live: H1 and H3, plus H4 weakly.

## Phase 5 — The discriminating experiment

Query count, not latency: deterministic, cheap, immune to load noise.

```
Experiment 1 — does v1.9.0 do more database work per checkout?

Method     Local environment, identical seeded cart (6 items), query log on.
           Run POST /checkout on v1.9.0, then on v1.8.4.
Predicts   H1 → query count materially higher on v1.9.0
           H3 → both versions equal on the same data
           H4 → both versions equal locally

Observed   E8  FACT  v1.9.0 → 47 queries, 1.31 s
           E9  FACT  v1.8.4 → 4 queries, 0.28 s
           E10 FACT  Query log: 43 of the 47 are
                     SELECT * FROM gift_wrap_options WHERE product_id = ?
                     — one per cart item, inside the serializer loop
Eliminates H3 disproven (same data, different result).
           H4 disproven (reproduces with no infrastructure involved).
           H1 supported, with a mechanism.
```

## Phase 6 — Attack the survivor

- *Does cart size predict latency in production?* Carts of 1–2 items: p95
  620 ms. Carts of 5+: p95 3.1 s. Consistent with per-item work. (E11)
- *Could the slowness be elsewhere and the queries incidental?* Local total for
  v1.9.0 is 1.31 s against 0.28 s, with 43 extra queries accounting for most of
  the gap. Nothing else in the diff touches the path. (E8, E9, E10)
- *Would reverting fix it?* The strongest test — and it is a production
  mutation, so it is proposed rather than performed.

## Phase 7 — Cause

```
Cause       a4f1c92 added a per-item query to the cart serializer, turning
            checkout into 4 + N queries
Confidence  CONFIRMED (reproduced: same input, both versions, 47 vs 4 queries,
            1.31 s vs 0.28 s)
```

`CONFIRMED` is earned by the controlled comparison, not by the timing
alignment — which on its own would have been `LIKELY`, and which is exactly what
H3 would also have predicted.

## Phase 8 — Fix and verify

The user asked for a fix, so the smallest change that addresses the cause: one
batched lookup keyed by product id, replacing the per-item query.

```
Verification         predicted        observed
query count          back to ~5       5
local p95, 6 items   ~300 ms          312 ms
existing checkout tests               41 passed, 0 failed
new regression test  fails without the fix, passes with it — confirmed both ways
gift-wrap options still returned      asserted in the new test
```

The regression test asserts the query count, not the elapsed time — a timing
assertion in CI is a flake waiting to happen, and query count is what actually
regressed.

## The answer

```markdown
## Result

Checkout slowed down because yesterday's release added one database query per
cart item to the checkout response.

**Cause:** Per-item query in the cart serializer introduced by a4f1c92 (gift-wrap
options) — 47 queries per checkout, previously 4
**Confidence:** High (reproduced on both versions with identical input)

**Why:** Latency stepped up within the deploy window with flat traffic, only the
checkout endpoint regressed, and running the same cart against both versions
gives 47 queries / 1.31 s versus 4 queries / 0.28 s.

**Action:** Fix merged — the options are now fetched in one batched query.
Checkout is back to 5 queries and ~310 ms locally, with a regression test
asserting the query count. Worth confirming production p95 returns to ~300 ms
after release.

### Client response

"We found the cause of the slow checkout: an update we released yesterday made
the system do far more database work than it needed to for each item in the
cart. We've corrected it and added a check that prevents this specific problem
from coming back. Checkout should be back to its normal speed once the fix is
released."
```

## What this example demonstrates

- The window was established from latency data, independently of the deploy.
- Traffic and restart effects were killed early and recorded as disproven.
- Query count — deterministic and cheap — discriminated better than any latency
  measurement could have.
- `CONFIRMED` came from a controlled comparison, not from the timing.
- The production revert was proposed, not performed.
- The fix was verified against the metric that regressed, both with and without
  the change.
- The client paragraph was included because customers were the ones experiencing
  the slowdown. An internal-only regression ends at `Action` — the section is
  contextual, not part of the format.
