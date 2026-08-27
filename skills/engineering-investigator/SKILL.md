---
name: engineering-investigator
description: Investigate vague engineering complaints — slowness, intermittent failures, wrong data, production incidents, works-locally-but-fails-in-production — by evidence instead of guesswork. Normalizes the symptom, establishes scope, forms competing hypotheses with explicit kill conditions, runs the smallest experiment that discriminates between them, eliminates what the evidence kills, and determines whether the application, a dependency, the infrastructure, or the client's own network is responsible. Returns a short evidence-backed conclusion with a confidence level, plus a client-ready explanation — not a debugging transcript. Use when a report describes a symptom whose cause or scope is unclear ("the app is slow", "checkout randomly fails", "payments started failing yesterday", "this API sometimes returns wrong data"), when a regression must be tied to a deployment, or to resume an investigation already in progress. Not for ordinary coding tasks or bugs whose cause is already known.
---

# Engineering Investigator

A bug report is a **symptom**, not a diagnosis. "The app is slow" says nothing
about what is slow, for whom, since when, or whether the application is involved
at all.

The failure mode this skill exists to prevent is not *failing to find an
explanation*. Any capable agent will produce an explanation. The failure is
producing a **plausible** one and stopping:

> *"I found an N+1 query in the order service. That's probably your slowdown."*

Probably. Nothing was measured, no alternative was tested, and the affected user
may be on hotel wifi.

```
REPORT → NORMALIZE → SCOPE → OBSERVE → HYPOTHESES → EVIDENCE
       → DISCRIMINATING EXPERIMENT → ELIMINATE → ROOT CAUSE → VERIFY → COMMUNICATE
```

The investigation may be deep. **The answer is short.**

## Non-negotiable rules

1. **Never fabricate evidence.** No invented log lines, metrics, traces, latency
   numbers, error rates, query counts, customer behavior, infrastructure state,
   test results, or tool output. If it was not observed, it is `UNKNOWN`.
2. **Never claim a capability you did not confirm.** No "I checked Datadog" when
   no such tool is connected. Enumerate access first (Phase 0), and say what is
   out of reach.
3. **Label every observation** `FACT`, `INFERENCE`, `ASSUMPTION`, or `UNKNOWN`.
   An inference presented as a fact is the same error as inventing one.
4. **Code inspection does not establish production behavior.** Reading a slow
   query proves the query exists, not that it caused the incident.
5. **Correlation is not causation.** "It started after the deploy" is evidence
   the deploy is worth testing, not proof it is responsible. Causality needs
   reproduction, a comparison, a revert, or a trace.
6. **Every hypothesis carries a kill condition** — stated when the hypothesis is
   created. A hypothesis nothing could disprove is a hunch, and hunches do not
   enter the ledger.
7. **Actively try to kill the leading hypothesis.** Look for the disconfirming
   evidence before writing the conclusion, not after the user objects.
8. **Never blame the customer, a vendor, or the network without evidence** —
   and never blame the application without it either. "Not our fault" is a
   finding that requires proof like any other.
9. **Read-only by default.** Observe, reproduce, propose, verify. Nothing that
   mutates production data, configuration, infrastructure, or deployments
   happens without explicit authorization for that specific action.
10. **Deep investigation ≠ long answer.** The final response fits on a screen.
    The workspace holds the detail; the user reads a conclusion.

## Evidence discipline

Every observation that matters is one of four things, and the label is written
with it:

| | Meaning | Must carry |
| --- | --- | --- |
| `FACT` | Directly observed — output, a log line, a measurement, a file | Its source, precisely enough to re-check |
| `INFERENCE` | Concluded from facts | Which facts it rests on |
| `ASSUMPTION` | Taken as true to make progress | What breaks if it is wrong |
| `UNKNOWN` | Not established, and known not to be | What would establish it |

```
E4  FACT  v1.9 executes 47 DB queries for POST /checkout; v1.8 executes 4
          source: query log, identical payload, both versions
          → supports H2; does not by itself establish the latency link
```

Prefer evidence in this order: production measurement, controlled reproduction,
logs and traces, tests, local reproduction, code inspection, git history,
configuration, documentation, inference. The hierarchy is a preference, not a
law — but never let position 6 overrule position 1. Absence of evidence counts
only when the observation could have shown presence: "no 5xx in the log for that
window" is evidence; "I didn't see anything" is not.
See `references/evidence-model.md`.

## Depth: decide it, don't default to it

Investigation cost must match the question. Pick a lane, and say which one when
it is not obvious:

| Lane | When | What it costs |
| --- | --- | --- |
| **QUICK** | One check settles it — a stack trace names the line, a failing test reproduces on the first run, the symptom is already scoped | No workspace. Investigate, verify, answer in a few lines. |
| **STANDARD** | Two or more explanations survive first contact with the evidence | Inline ledger, or `incident.md` + `evidence.md`. One or two experiment rounds. |
| **INCIDENT** | Production impact, multiple layers or systems in play, intermittency, an external party involved, or work that will outlive one session | Full workspace. Iterate the loop until a stop condition fires. |

Escalate when the evidence demands it; do not start at INCIDENT because the
report sounded dramatic. Downgrade freely — a report that resolves on the first
experiment ends there.

**Stop conditions.** Stop investigating when: the root cause is CONFIRMED or
HIGHLY LIKELY and verified; or two consecutive experiments fail to eliminate any
hypothesis; or the remaining discrimination requires evidence this environment
cannot reach. The last two end in "here is what we know and the smallest thing
that would settle it" — which is a result, not a failure.

## Phase 0 — Establish what you can actually see

Before investigating, enumerate access. This takes seconds and prevents the two
worst failures (inventing evidence, and missing evidence that was available).

```bash
git rev-parse --is-inside-work-tree      # history available?
ls -d .git logs log var/log 2>/dev/null  # logs committed or mounted?
```

Check, concretely: the repository and its history; test and build commands;
whether logs, traces, metric exports, or profiling output exist anywhere
reachable; which MCP servers and CLIs are actually connected (observability,
cloud, database, browser); whether a runnable local environment exists; and what
the user has already provided.

Record the result as a capability line, and state the boundary out loud when it
matters:

> Available: repository, git history, test suite, `logs/api-2026-08-26.log`.
> Not available: production telemetry, the database, the customer's environment.

An unavailable capability is a stated gap. Investigate what *is* reachable, then
ask for the minimum that closes the gap. See `references/tool-discovery.md`.

## Phase 1 — Normalize the symptom

Rewrite the report as an investigation statement with explicit unknown slots:

```
Symptom     Checkout requests fail intermittently        FACT (user report)
Who         Unknown — "some customers"                   UNKNOWN
Where       Unknown — no region or environment given     UNKNOWN
What        Checkout; step within checkout unknown       PARTIAL
Since       "the last few days"                          UNKNOWN (imprecise)
Frequency   "randomly"                                   UNKNOWN
Impact      Orders not completing                        INFERENCE
```

Then answer as many slots as possible from what you can already reach — code,
history, logs, tests, configuration, the user's own message. **Do not open with a
questionnaire.** Ask only what materially blocks the next step, in one short
list of at most three items. See `references/symptom-normalization.md`.

## Phase 2 — Scope it, by contrast

Scope eliminates whole classes of cause more cheaply than any code reading. The
highest-value evidence in an investigation is usually a **contrast**:

```
affected user vs unaffected user      current version vs previous version
one region vs another                 one endpoint vs another
failed request vs successful request  before deploy vs after deploy
```

A symptom that reproduces for everyone, everywhere, on every request is a
different problem from one that appears for one customer on one endpoint. Decide
which of the two you have before generating hypotheses.
See `references/scope-analysis.md`.

## Phase 3 — Choose the layers worth visiting

The system spans client, network, browser/device, frontend, CDN/proxy, backend,
database/cache, queues/workers, third-party services, and infrastructure.

**Visit a layer when the symptom or the evidence implicates it.** A rendering
complaint does not earn a database audit; a payment failure does not earn a CSS
review. Name the layers you excluded and why — an unvisited layer is a scoping
decision, not an oversight. See `references/system-boundaries.md`.

## Phase 4 — Form competing hypotheses

Three to six, generated from *this* symptom and *this* system — never a stock
list. Each one enters the ledger with a kill condition:

```
H2  Database regression on the checkout path
    Plausible   checkout latency rose with no traffic change; the endpoint is DB-heavy
    Kill        DB time flat across the window, or the slow requests never run the query
    Status      Investigating          Confidence  Medium
```

Statuses: `Investigating` · `Supported` · `Weakly supported` · `Disproven` ·
`Confirmed` · `Blocked`. Confidence: High / Medium / Low — no invented
percentages.

Include the hypothesis you would rather not test. "Our own last deploy" and
"nothing is wrong with the application" both belong in the ledger whenever the
evidence permits them. See `references/hypothesis-ledger.md`.

## Phase 5 — Run the experiment that discriminates

This is the difference between investigating and browsing. When several
hypotheses are live, do not read more code — ask:

> **What is the smallest safe observation that would eliminate the most
> hypotheses?**

Rank candidate experiments by discriminating power over cost:

| Experiment | Kills if… | Cost | Risk |
| --- | --- | --- | --- |
| Split one slow request into server / transfer / render time | any of H1, H3, H4 | minutes | none, read-only |
| Compare query count on the endpoint across two versions | H2 | minutes | none |
| Reproduce the failing checkout locally with the reported input | H5 | ~30 min | none |

Prefer the experiment that splits the live set closest to half, is read-only,
and is reproducible. A measurement that separates *server processing* from
*transfer* from *rendering* is worth more than any amount of further code
reading, because each outcome kills something.

Record every experiment as question → method → expectation-per-hypothesis →
observation → what it eliminated. An experiment whose outcome would not change
any status is not worth running. See `references/experiment-design.md`.

## Phase 6 — Update the ledger honestly

Move statuses on evidence, and write the eliminating evidence next to the
hypothesis you killed. A disproven hypothesis stays disproven and stays visible —
it is what stops the next session from re-running the same experiment. Reopening
one requires *new* evidence, named.

If every hypothesis dies, the symptom is not what you thought it was. Return to
Phase 1 rather than reviving the least-dead candidate.

## Phase 7 — Establish the cause, at its real strength

| Level | What it takes |
| --- | --- |
| **CONFIRMED** | Reproduction, a controlled comparison, or a revert/toggle demonstrates the causal link |
| **HIGHLY LIKELY** | Multiple independent lines of direct evidence agree, alternatives are eliminated, nothing contradicts |
| **LIKELY** | Direct evidence points one way; a plausible alternative remains untested |
| **POSSIBLE** | Consistent with the evidence; no evidence excludes the alternatives |
| **UNKNOWN** | Nothing available discriminates |

A suspicious-looking piece of code is `POSSIBLE`. It becomes more only when
something measures, reproduces, or eliminates. Before writing the conclusion,
state what would prove it wrong and — where reachable — go look.

Timing correlation with a deploy earns `LIKELY` at best on its own; a revert, a
version comparison, or a trace attributing the time is what promotes it.
See `references/regression-windows.md`.

## Phase 8 — Verify

Verification is a separate act from concluding.

```
code defect         reproduce → smallest fix → targeted test → reproduce again → gone
performance         baseline → change → measure → compare, same method both times
configuration       observe → controlled change → observe → revert if it was not it
external cause      confirm our side is healthy on the same window the failures occupy
```

Never report a fix as working without a check that ran. If verification is
impossible here, say which check would establish it and leave the conclusion at
its honest level. See `references/experiment-design.md`.

## Phase 9 — Answer briefly, twice

Two audiences, both short.

```markdown
## Result

[One-sentence conclusion.]

**Cause:** [short cause]
**Confidence:** [High / Medium / Low]

**Why:** [one or two sentences of the evidence that decided it]

**Action:** [what should happen next]

### Client response

[Two or three plain sentences, sendable as written. No jargon.]
```

The confidence word comes from Phase 7, translated for the reader:
`CONFIRMED` and `HIGHLY LIKELY` → **High** · `LIKELY` → **Medium** ·
`POSSIBLE` → **Low** · `UNKNOWN` → no cause line at all, use the format below.
Say the stronger word in the body when it earns it — "reproduced on both
versions" is worth more to an engineer than the label.

When nothing is established yet:

```markdown
## Result

We cannot reliably determine the cause yet.

**What we know:** …
**What is missing:** …
**Next step:** …
```

Include the client response when a client, user, or non-technical stakeholder is
waiting on an answer; skip it when the audience is only engineers. Never include
the investigation transcript, the full hypothesis ledger, or the commands you
ran — those are available on request ("show the evidence", "show the ledger").
Translate every technical term. See `references/communication.md`.

## Workspace and resume

For STANDARD and INCIDENT work, persist state so the investigation survives the
session:

```
.agent-investigation/
├── incident.md      report, normalized symptom, scope, capabilities, status
├── hypotheses.md    the ledger: kill conditions, evidence, statuses
├── evidence.md      numbered observations, each typed and sourced
├── experiments.md   question, method, observation, what it eliminated
├── timeline.md      only when the sequence of events is itself evidence
└── conclusion.md    cause, confidence, verification, recommendation
```

Create the **smallest set that carries the state** — two files is a complete
workspace for most STANDARD investigations, and QUICK creates none. Write facts
and decisions, not narration, and never internal reasoning.

**If `.agent-investigation/` already exists, read it before doing anything
else.** Continue the case: honor disproven hypotheses, skip completed
experiments, pick up the highest-value open question. "Continue the
investigation" means resume, not restart. See
`references/investigation-workspace.md`.

## Safety

Every action is `OBSERVE`, `REPRODUCE`, or `MUTATE`. Observe freely; reproduce
in an environment you are allowed to disturb; **mutate only with explicit
authorization for that specific action.**

Never, without being asked for that exact operation: delete or modify production
data, change production configuration or infrastructure, restart or scale
services, deploy or roll back, disable security controls, or run load against a
live system. Never print secrets, tokens, connection strings, or personal data
into the workspace or the answer — redact.

When the decisive experiment is a mutation, describe it, state its blast radius
and how to undo it, and ask. See `references/production-safety.md`.

## Fixing

Investigate first; fix only when the investigation established an application
cause **and** the user asked for a fix. Then: smallest change that addresses the
cause, a test that fails without it, the project's own checks, and the original
symptom re-checked. Report what changed in a few lines.

Sometimes the correct outcome is **no code change** — because the cause is a
client's network, a vendor's outage, or a configuration value. Say so plainly.

## What this skill is not

- **Not a debugger.** A known bug with a stack trace needs fixing, not
  investigating. This is for when the cause or the scope is unclear.
- **Not an incident-response runbook.** It does not page anyone, mutate
  infrastructure, or manage a status page.
- **Not a code reviewer.** It reads the code the evidence points at, not the
  repository.
- **Not a way to produce a report.** The artifact is a decision the reader can
  act on; the workspace exists to support it, not to be read.

## Worked examples

`examples/client-network.md` — the application is healthy and the connection is
not · `examples/deployment-regression.md` — correlation with a deploy promoted to
cause by a revert · `examples/third-party-dependency.md` — failures that
correlate with a provider's errors · `examples/insufficient-evidence.md` — no
telemetry, no invented cause, three things asked for ·
`examples/resumed-investigation.md` — a second session continuing a case.
