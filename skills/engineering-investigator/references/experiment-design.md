# Experiment Design

An investigation makes progress when a hypothesis dies. Reading more code is not
progress; it is inventory. The question at every decision point is:

> **What is the smallest safe observation that would eliminate the most live
> hypotheses?**

## Selecting the next experiment

Score candidates on four axes and take the best ratio, not the most thorough
option:

| Axis | Prefer |
| --- | --- |
| **Discriminating power** | Splits the live hypothesis set — ideally in half. An experiment whose every outcome leaves all statuses unchanged is not worth running. |
| **Cost** | Minutes over hours. A log query beats building a load test. |
| **Risk** | Read-only over reproduce over mutate. Never mutate production to satisfy curiosity. |
| **Reproducibility** | An observation someone can repeat outranks a one-off glimpse. |

Write the expected outcome **per hypothesis before running it**. That is what
makes the result an elimination rather than an interpretation:

```
Experiment 2 — where is the checkout time spent?

Method     Time one affected request end to end: server processing (TTFB),
           transfer, render. Same request, unaffected user, as comparison.
Predicts   H1 backend      → TTFB high, transfer normal
           H2 database     → TTFB high, and DB time dominates the trace
           H3 payload/net  → TTFB normal, transfer high
           H4 rendering    → TTFB and transfer normal, paint late
Observed   TTFB 148 ms · transfer 4.8 s · payload 1.9 MB · paint +180 ms
Eliminates H1, H2, H4 disproven. H3 supported.
```

Four hypotheses, one observation, three eliminations. That is the shape to aim
for.

## Experiments by question

**Where is the time going?**
Split total into DNS/connect, server processing, transfer, and render
(`system-boundaries.md`). One measurement forks the whole investigation.

**Did this version cause it?**
Run the same input against both versions and compare a specific metric — query
count, response time, response body. Query count is especially good: it is
deterministic, cheap, and immune to load noise.

```bash
git stash && git checkout <previous-tag>   # only in a working copy you own
# measure, then return
```

**Is it data-dependent?**
Run the failing input and a working input through the same path. If one record
fails and another succeeds on identical code, the cause is in the data or the
state it implies.

**Is it load-dependent?**
Compare the same operation at a quiet time and a busy one, or with one
concurrent request versus several — in a non-production environment. Never
generate load against production without explicit authorization.

**Is it one instance?**
Attribute failures to instance, host, pod, or availability zone. A stable
fraction that maps to one instance is one instance.

**Is it us or them?**
Attribute the time or the error inside the boundary: does the failure carry the
provider's error code and request id? Does our own latency return to normal when
the vendor call is excluded from the measurement?

**Does it reproduce at all?**
The most valuable single result in any investigation. A reproduction turns every
later claim into something testable, and it is the only route to `CONFIRMED`.

## The revert test

For a suspected regression, reverting the change and observing the symptom
disappear is the strongest available evidence short of a full root-cause
reproduction.

Its costs are real: it is a mutation, it may be impossible on production, and it
can be confounded by a restart that clears an unrelated state. Prefer, in order:

1. Reproduce with the previous version locally or in staging.
2. Compare a deterministic metric across versions (query count, response shape).
3. Toggle a feature flag if the change is behind one.
4. Revert in production — with authorization, and with a stated expectation of
   what should change and by how much.

A revert that fixes the symptom shows *that* change is responsible. It does not
show *why*; finish the investigation into the mechanism before writing the
conclusion, or the fix will re-introduce it.

## Bisecting

When the window contains many candidate changes and reproduction is available,
bisect it:

```bash
git bisect start <bad> <good>
git bisect run ./repro.sh      # exit 0 = good, non-zero = bad
```

Requires a deterministic reproduction; without one, bisect amplifies noise into
a confident wrong answer. If the repro is flaky, run it enough times per step to
make a false "good" unlikely, and say in the evidence that the bisect rests on a
probabilistic check.

## Verification experiments

Verification is an experiment whose hypothesis is *the conclusion*. Design it
the same way, and state the prediction first.

```
Claim       The added serializer queries caused the checkout regression.
Predicts    Removing them returns query count to ~4 and p95 to ~300 ms.
Method      Apply the fix; re-run the same measurement, same input, same load.
Observed    5 queries; p95 340 ms over 200 requests.
Verdict     Verified. Residual 40 ms is within the pre-change range.
```

Rules that keep verification honest:

- **Same method both sides.** A baseline measured one way and a result measured
  another is not a comparison.
- **Baseline before change.** A baseline reconstructed afterward is a guess.
- **Re-check the original symptom**, not only the proxy metric. Query count
  falling is not the same as checkout being fast for the affected user.
- **Never report a fix as working without a check that ran.** "Should resolve
  it" is a prediction; say so in those words.

## Experiments not to run

- Anything that mutates production data, configuration, or infrastructure
  without explicit authorization for that action (`production-safety.md`).
- Load generation against a live system.
- Broad instrumentation added to production code as a first step — a log line
  that ships is a deploy, with a deploy's risk.
- A second experiment that would eliminate exactly what the first one did.
- More code reading, when a measurement is available and would decide it.
