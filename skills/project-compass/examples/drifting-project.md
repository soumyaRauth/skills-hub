# Example — Five solutions to an unmeasured problem

The escalation pattern: each change is a larger mechanism aimed at the same
problem, and none of the changes is preceded by a measurement. It is the easiest
drift to see from the outside and the hardest to see from inside, because every
individual step is a thing a competent engineer would do.

---

## The trajectory

```
2026-08-12  perf   Raised the report endpoint timeout 30s → 120s   config/server.ts
2026-08-15  perf   Added retry on report generation failure        api/reports.ts:88
2026-08-21  perf   Moved report generation to a background job     workers/reports.ts
2026-08-29  perf   Cached the report payload for 15 minutes        lib/cache.ts
                   pattern: perf-escalation (4th)
```

**Request, 2026-09-03:**

> Let's add Redis. The in-process cache doesn't survive deploys and we've got two
> instances now.

---

## The search that decides the response

Before saying anything, look for the measurement. Absence is only evidence when
you looked, so the search is named:

```
grep -rn 'console.time\|performance.now\|duration\|elapsed\|histogram' src/ workers/
   → 0 hits outside test files
No APM, tracing, or metrics dependency in package.json
No timing in the request logger (lib/logger.ts logs status and path only)
No issue, comment, or commit naming a target, a threshold, or a number
git log -S'timeout' → the 30s value was itself never measured; it is a default
```

```
How slow is the report endpoint?          UNKNOWN
Which part of it is slow?                 UNKNOWN
What would be fast enough?                UNKNOWN
Did the background job help?              UNKNOWN
Did the cache help?                       UNKNOWN
Who is affected, and how often?           UNKNOWN
```

Five structural changes over three weeks, and not one number anywhere. The
`UNKNOWN` list *is* the finding — it is not that Redis is wrong. Redis may well
be right. Nothing in the repository could currently tell anyone either way.

---

## Level 3, and the shape of it

Recurrence: four instances, four locations, three weeks. Convergence: every one
of them is a response to "reports are slow". Consequence: Redis is a permanent
operational dependency — a service to run, monitor, secure and pay for — being
added as the fifth guess. Actionability: one timing log, one afternoon.

Not a refusal. The user may know exactly what is slow and simply never have
written it down.

---

## The response

> I can add Redis — the shared-cache argument across two instances is real and
> correct on its own terms.
>
> **Before I do, something worth thirty seconds.** Since August the report
> endpoint has had its timeout raised, a retry added, generation moved to a
> background job, and a cache put in front of it. That is four structural
> changes to one endpoint, and I cannot find a single measurement of it anywhere
> in the repo: no timing in the logger, no APM, no benchmark, no target in any
> issue or commit. So there is no way to tell whether the background job helped,
> whether the cache is hitting, or whether Redis is the fifth fix or the first
> one that addresses the actual cause.
>
> **What I would do first:** log generation time by stage — query, aggregate,
> render — on the existing endpoint. One afternoon, no new dependencies. It
> answers three things at once: what is actually slow, whether the last two
> changes did anything, and what "fast enough" needs to be.
>
> My guess, and it is only a guess, is that the time is in the query rather than
> the transport — the monthly report joins five tables with no index on
> `adjustments.created_at`. If that turns out to be right, Redis would have made
> the second request fast and left the first one exactly as slow as it is now.
>
> Say the word and I will add Redis anyway — you may have measured this
> somewhere I cannot see.

---

## Why this is a redirect rather than a nudge

A nudge would be *"worth measuring at some point"* — true, ignorable, and it
would still be true after Redis was in production forever. The escalation makes
the difference: each step raised the operational cost, and this step raises it
permanently. That is the moment when one afternoon of measurement is cheapest.

**The alternative is smaller than the work it replaces.** Timing logs versus
provisioning a cache service. That is what makes the recommendation a
recommendation rather than an objection.

**The hypothesis is labeled a hypothesis.** The missing index is `INFERRED
(Low)` — offered because it makes the suggestion concrete, flagged because
nothing measured it.

**The exit ramp is real.** If the user says they profiled it last month, Redis
gets built and the finding is closed as answered:

```markdown
# decisions.md
## Report latency was profiled off-repo; the query is the bottleneck
Stated by the user, 2026-09-03
Note      no measurement lives in the repository; timing logs still worth adding
Status    Closed — do not raise perf-escalation again for reports
```
