# Example — The application is not the problem

The hardest conclusion to reach honestly, because it is the one everybody
suspects the engineer of wanting.

---

**Report:**

> The application is unusably slow for one of our customers. They're threatening
> to churn. Can you look?

---

## Phase 0 — What can be seen

```
Available      repository, git history, the last 7 days of the API access log
               (logs/api-2026-08-*.log, includes duration and bytes per request),
               a HAR file the customer's IT team exported
Not available  APM traces, the customer's device, their network
```

Lane: **STANDARD**. Two files: `incident.md`, `evidence.md`.

## Phase 1 — Normalize

```
Symptom     Perceived slowness across the application    FACT (report)
Who         One customer account (Northwind)             FACT (report)
Where       Unknown network/region                       UNKNOWN
What        "everything"                                 UNKNOWN
Since       "the last week or so"                        UNKNOWN
Frequency   "always"                                     PARTIAL
```

"Everything is slow for one customer" is already a strong scoping signal: a code
path that is slow is slow for everyone who runs it.

## Phase 2 — Scope, by contrast

The access log has a tenant id, a duration, and a response size per request. The
contrast is free:

```
E1  FACT  Northwind requests, 2026-08-24 → 08-26: n=3,110
          server duration p50 96 ms · p95 210 ms
E2  FACT  All other tenants, same window: n=214,882
          server duration p50 91 ms · p95 228 ms
          source: logs/api-2026-08-2*.log, grouped by tenant_id
```

Server-side, Northwind is indistinguishable from everyone else. Whatever is slow
for them is not our processing time — a fact worth more than any code reading
that could have followed.

## Phase 3 — Layers

Server processing is excluded by E1/E2. That leaves transfer, client, device,
and the network path. Backend, database, and queue layers are **not visited**,
and the exclusion is recorded.

## Phase 4 — Hypotheses

```
H1  Payload size — Northwind's data makes responses much larger
    Kill: their response sizes are comparable to other tenants'
H2  Client network throughput
    Kill: transfer time is proportional to size at a normal rate
H3  Client device or browser
    Kill: time is spent in transfer, not in rendering or scripting
H4  Regional edge/CDN behavior
    Kill: connect and TLS times are normal; cache status matches other tenants
```

Note what is *not* here: no stock "N+1 query" hypothesis. Nothing in the evidence
implicates a query, and a hypothesis with no supporting pattern is a distraction.

## Phase 5 — One experiment, four predictions

```
Experiment 1 — where does Northwind's time go?

Method     Read the customer's HAR for the slowest interaction; compare the same
           endpoint's log entries for Northwind and for two other tenants.
Predicts   H1 → response bytes much larger for Northwind
           H2 → bytes normal, transfer time long, throughput low
           H3 → transfer normal, scripting/rendering long
           H4 → connect/TLS long, or an edge miss on every request

Observed   E3  FACT  HAR, GET /api/dashboard: DNS 24 ms · connect 61 ms ·
                     TTFB 173 ms · content download 6.42 s · 1.71 MB
                     → 2.1 Mbit/s effective on this transfer
           E4  FACT  Same endpoint, same window, two other tenants:
                     1.55 MB and 1.81 MB, total time 0.9 s and 1.1 s
                     source: logs/api-2026-08-26.log
           E5  FACT  HAR scripting + rendering for the interaction: 310 ms

Eliminates H1 (sizes comparable), H3 (client work is 310 ms of a 7 s
           interaction), H4 (connect and TLS normal, no edge anomaly).
           H2 supported.
```

## Phase 6 — Try to kill the survivor

The leading hypothesis is now "their network". Before writing that down, look
for what would disprove it:

- *Do all their requests transfer slowly, or only large ones?* — small API calls
  complete in ~200 ms total; the slow ones scale with size. Consistent with
  throughput, not with a per-request cost. (E6)
- *Is it constant?* — 2.0–2.4 Mbit/s across three days, all hours. Not
  congestion at a peak. (E7)
- *Could our payloads be the real story?* — 1.7 MB for a dashboard is fat, and
  on a normal connection it hides. That is a real finding, and it does not make
  the connection fast. Both go in the answer.

Nothing disproves H2. Nothing supports an application-side cause.

## Phase 7 — Cause

```
Cause       Low throughput on the affected customer's connection
Confidence  HIGHLY LIKELY

Chain       server time equal to every other tenant (E1, E2)
            → response sizes comparable (E3, E4)
            → transfer at ~2 Mbit/s where others complete in ~1 s (E3, E4)
            → client-side work is 310 ms of a 7 s interaction (E5)
            → constant across days and hours (E7)

Would prove it wrong: another tenant on a normal connection showing the same
transfer times; or Northwind's throughput being normal on a different endpoint.
```

Not `CONFIRMED`: nobody measured that connection directly. The customer running
one `curl` would upgrade it, and that is what the answer asks for.

## The answer

```markdown
## Result

The application is responding normally for this customer — the time is going
into transferring data over their connection, not into our processing.

**Cause:** Low network throughput on the affected connection (~2 Mbit/s, where
comparable customers complete the same requests in about a second)
**Confidence:** High

**Why:** Server processing for this account matches every other tenant (p95
210 ms vs 228 ms), response sizes are comparable, and the customer's own network
capture shows 6.4 s spent downloading a 1.7 MB response with only 310 ms of
browser work.

**Action:** Ask the customer to test the same page on a different network. In
parallel, our dashboard response is 1.7 MB — worth reducing, because it is what
makes a weak connection unusable rather than merely slow.

### Client response

"We've looked into the slowness and our systems are responding normally for your
account — as quickly as they do for everyone else. What we can see is that the
data is taking much longer than usual to travel to your computers: about six
seconds for something that normally arrives in one. That usually points to the
office internet connection or a network device between us. Could you try the
same page from a different connection, such as a phone hotspot, and tell us
whether it behaves differently? We're separately making that page lighter, which
will help on slower connections."
```

## What this example demonstrates

- The contrast (E1/E2) did more work than any code reading could have, and it
  cost one log query.
- Four hypotheses, one experiment, three eliminations.
- The survivor was attacked before it was reported.
- "Not our fault" was earned by three things: our side healthy in the same
  window, an unaffected comparison, and a measurement of the external factor.
- The 1.7 MB payload is reported honestly as our contribution — without letting
  it become a fake application root cause.
