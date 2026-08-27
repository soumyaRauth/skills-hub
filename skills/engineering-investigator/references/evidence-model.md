# Evidence Model

Everything the investigation knows is one of four things. Mislabelling is how a
guess becomes a conclusion.

| Type | Definition | Test |
| --- | --- | --- |
| `FACT` | Directly observed — a command's output, a log line, a measurement, a file's contents, something the user stated as fact | Could someone else reproduce the observation? |
| `INFERENCE` | A conclusion drawn from facts | Which facts? Would the conclusion survive if one were removed? |
| `ASSUMPTION` | Taken as true without evidence, because progress requires it | What breaks if it is false? |
| `UNKNOWN` | Not established, and known not to be established | What would establish it? |

```
E3  FACT       Checkout p95 rose from 310 ms to 2.1 s on 2026-08-25
               source: logs/api-2026-08-25.log, aggregated by hand (n=1,412)
E4  FACT       v1.9 executes 47 DB queries for POST /checkout; v1.8 executes 4
               source: query log, same request payload, both versions
E5  INFERENCE  The added queries account for most of the added latency
               from: E3, E4 — DB time per query ~40 ms in this log
E6  ASSUMPTION The two versions were measured under comparable load
               risk: if v1.8 was measured off-peak, the comparison inflates
E7  UNKNOWN    Whether other endpoints regressed in the same deploy
```

An `INFERENCE` names the facts it rests on. An `ASSUMPTION` names what its being
wrong would cost. An `UNKNOWN` names what would resolve it. An entry that cannot
supply its own line is not ready to be written down.

## Provenance

Every meaningful piece of evidence records where it came from, in enough detail
that another engineer could go and look:

```
file path + line          src/checkout/cart.ts:142
command + when            `git log --since=... --stat`, run this session
log + timestamp range     logs/api-2026-08-25.log, 14:02–14:31 UTC
trace / request id        trace 9f2c…, POST /checkout
metric + window + source  p95 latency, 24 h, provided by the user as a screenshot
test + result             `npm test -- checkout` → 38 passed, 0 failed
tool result               named tool, named query
user-provided             "the user said checkout fails for about 1 in 20 attempts"
```

Two rules:

- **User-provided information is evidence with a source, not a fact about the
  system.** "Support says it started Tuesday" is a `FACT` about what support
  said; the start time itself may still be `UNKNOWN`.
- **Copy real values.** A latency, a count, or an error code is quoted from
  output, never remembered approximately and never rounded into invention.

`evidence.md` holds only what changed a status or supports the conclusion. It is
not a shell transcript; a file that records every `ls` is a file nobody reads.

## Evidence hierarchy

When two sources disagree, the higher one wins — and the disagreement itself
gets recorded, because it is usually informative.

1. **Direct production measurement** — a trace, a metric, a log from the
   affected system in the affected window
2. **Controlled reproduction** — the failure produced on demand with a known
   input
3. **Logs, traces, metrics** from adjacent windows or systems
4. **Automated tests** that exercise the behavior
5. **Controlled local reproduction** in an environment resembling production
6. **Code inspection**
7. **Git and deployment history**
8. **Configuration inspection**
9. **Documentation**
10. **Reasoned inference**

The hierarchy is a preference, not a law: a decisive local reproduction beats an
ambiguous production graph. What it forbids is the inversion — using position 6
to overrule position 1. If the code says the cache is used and the trace shows a
database hit per request, the trace is right and the interesting question is
why.

## Correlation and causation

Correlation earns a hypothesis and an experiment. It does not earn a conclusion.

```
Correlated                      What promotes it to causal
deploy time ≈ symptom start     revert or version comparison restores behavior
traffic peak ≈ errors           the failure reproduces on demand under load
one query looks expensive       that query's time is attributed inside the slow requests
provider errors ≈ our failures  our failures carry the provider's error code and ids
```

Three traps to check for by name:

- **Reversed direction.** Slow requests can *cause* a queue backlog rather than
  result from it.
- **Common cause.** Two systems degrading together may share an upstream — a
  host, a network path, a dependency.
- **Selection.** Failures are logged and successes are not, so the log looks
  like a system that only fails. Compare rates, not counts, and get the
  denominator.

## Fabrication: the prohibitions

Never write, imply, or infer into existence:

- log lines, trace ids, request ids, or error messages you did not read
- latency, throughput, error rate, query count, or resource numbers you did not
  measure or copy
- the state of production, a database, a queue, or an external service
- what other users are experiencing
- a tool, dashboard, MCP server, or console you did not confirm and use
- a test or command result you did not run
- a customer's network conditions, device, or behavior

When something is needed and unavailable, the entry is `UNKNOWN` with the
reason. "No production telemetry is reachable from this environment" is a
finding, and stating it is what makes the rest of the report trustworthy.

## Negative evidence

Absence is evidence only when the observation could have shown presence:

- "No errors in the log for that window" counts **if** the log covers that
  window at that level for that service. Otherwise it is `UNKNOWN`.
- "The test suite passes" counts against a hypothesis only if some test covers
  the behavior in question. Green usually means untested, not correct.
- "Nobody else reported it" is the weakest form and is often just reporting
  latency.

Record what the absence covers: `FACT: no 5xx for /checkout in api.log 14:00–15:00
(log level INFO, all instances)`. That sentence can eliminate a hypothesis; "no
errors found" cannot.
