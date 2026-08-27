# Engineering Investigator

### Don't find an explanation. Find out whether the explanation is true.

Engineering Investigator is an [Agent Skill](https://code.claude.com/docs/en/skills)
for the vague complaint: *the app is slow*, *checkout randomly fails*, *payments
started failing this morning*, *it works locally but not in production*. It
treats the report as a **symptom**, forms competing explanations, runs the
smallest experiment that can eliminate some of them, and answers in one screen —
including, when the evidence says so, that the application is not at fault.

```bash
npx skills add soumyaRauth/skills-hub --skill engineering-investigator
```

---

## The problem

Ask a capable coding agent why the app is slow and you will get an explanation.
That is the problem. It will read the code, find something genuinely suspicious,
and tell you about it:

> *"I found an N+1 query in the order service — that's likely your slowdown."*

Likely. Nothing was measured. No alternative was tested. The query may have been
there for two years, and the affected customer may be on hotel wifi. You now
have a plausible story, a code change to review, and no more knowledge about the
incident than before.

The gap is not effort or capability. It is method: **finding an explanation and
establishing a cause are different activities**, and one is being delivered as
the other.

## The change

```
Before                            After

complaint                         complaint
  ↓                                 ↓
read the code                     normalize the symptom
  ↓                                 ↓
find something suspicious         scope it — who, where, what, since, how often
  ↓                                 ↓
plausible story                   competing hypotheses, each with a kill condition
                                    ↓
                                  the experiment that eliminates the most
                                    ↓
                                  what survived, at its real confidence
                                    ↓
                                  verify
                                    ↓
                                  four lines + a client-ready paragraph
```

---

## What you actually get

```markdown
## Result

The application is responding normally for this customer — the time is going into
transferring data over their connection, not into our processing.

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
account… "
```

Behind those lines: seven symptom slots, a scope contrast across 218,000
requests, four hypotheses, one experiment that killed three of them, and a
deliberate attempt to kill the survivor. None of it in your way.

When nothing is established, it says so, and asks for three specific things
instead of inventing a cause.

---

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill engineering-investigator
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill engineering-investigator --agent claude-code
```

Skills are selected by their description, so there is nothing to memorize —
describe the symptom and it applies. To invoke it explicitly:

```
Investigate why checkout is slow for some customers.
Users say the app is slow — investigate before changing anything.
Continue the investigation.
```

Afterwards, the detail is one question away:

```
show the evidence        show the hypotheses      what did you rule out?
how do you know?         what did you not check?  what would change this?
```

---

## How it works

```
REPORT → NORMALIZE → SCOPE → OBSERVE → HYPOTHESES → EVIDENCE
       → DISCRIMINATING EXPERIMENT → ELIMINATE → ROOT CAUSE → VERIFY → COMMUNICATE
```

Not every investigation runs the whole loop. The skill picks a lane first —
**QUICK** when one check settles it, **STANDARD** when explanations compete,
**INCIDENT** when production is involved — and stops when the cause is
established, when two experiments in a row eliminate nothing, or when the
remaining question needs access this environment does not have.

### Five things that make it an investigation

**Every hypothesis carries a kill condition**, written when the hypothesis is
created — before any evidence arrives. A claim nothing could disprove is a
hunch, and hunches do not enter the ledger.

**Experiments are chosen for discriminating power.** When four explanations are
live, the next action is not "read more code"; it is the cheapest safe
observation that kills the most of them. Splitting one request into server time,
transfer time, and render time settles more than an hour of reading, because
each outcome eliminates something.

**Evidence is typed and sourced.** `FACT`, `INFERENCE`, `ASSUMPTION`, `UNKNOWN` —
and code inspection never establishes production behavior. Timing correlation
with a deploy is a lead; a revert, a version comparison, or a trace is a cause.

**The leading hypothesis gets attacked.** Before the conclusion is written, the
skill asks what would prove it wrong and — where reachable — goes and looks.

**The application can be exonerated, but only on evidence.** Three things are
required: our side healthy in the same window, an unaffected comparison, and a
measurement of the external factor. With one of the three, the honest sentence
is *"we have found no evidence of an application-side problem yet"* — and that is
what gets written.

### Confidence means something

| | Requires |
| --- | --- |
| **CONFIRMED** | Reproduction, controlled comparison, or a revert demonstrates causality |
| **HIGHLY LIKELY** | Independent lines of direct evidence agree, alternatives eliminated |
| **LIKELY** | Direct evidence points one way; a plausible alternative is untested |
| **POSSIBLE** | Consistent with the evidence; nothing excludes the alternatives |
| **UNKNOWN** | Nothing available discriminates |

A suspicious piece of code is `POSSIBLE`. It becomes more when something
measures, reproduces, or eliminates — never because it looks guilty.

---

## Investigation state

For anything beyond a quick check, the case is persisted:

```
.agent-investigation/
├── incident.md      report, normalized symptom, scope, capabilities, status
├── hypotheses.md    the ledger — kill conditions, evidence, statuses
├── evidence.md      numbered observations, typed and sourced
├── experiments.md   question, method, prediction, observation, elimination
├── timeline.md      only when sequence is itself evidence
└── conclusion.md    cause, confidence, verification, recommendation
```

Only the files that carry state get created — a quick investigation creates
none. Say **"continue the investigation"** in a later session and the skill reads
the case first: disproven hypotheses stay disproven, completed experiments are
not re-run, and it picks up the open question. See
[`references/investigation-workspace.md`](references/investigation-workspace.md).

---

## Safety

Read-only by default. Every action is `OBSERVE`, `REPRODUCE`, or `MUTATE`, and
mutations to production data, configuration, infrastructure, or deployments
require explicit authorization for that specific action — presented with its
blast radius, how to undo it, and what each outcome would prove. Secrets and
personal data never enter the workspace or the answer. See
[`references/production-safety.md`](references/production-safety.md).

---

## Worked examples

| Example | What it shows |
| --- | --- |
| [client-network.md](examples/client-network.md) | The application is healthy and the customer's connection is not — earned, not assumed |
| [deployment-regression.md](examples/deployment-regression.md) | Timing correlation with a deploy promoted to `CONFIRMED` by a controlled comparison |
| [third-party-dependency.md](examples/third-party-dependency.md) | Failures attributed to a vendor by their own error codes — plus our own contribution, reported honestly |
| [insufficient-evidence.md](examples/insufficient-evidence.md) | No telemetry: six hypotheses stay `Blocked`, nothing is invented, three things are asked for |
| [resumed-investigation.md](examples/resumed-investigation.md) | A second session continuing a case instead of restarting it |

## References

The methodology in depth, loaded on demand:
[symptom normalization](references/symptom-normalization.md) ·
[scope analysis](references/scope-analysis.md) ·
[system boundaries](references/system-boundaries.md) ·
[the hypothesis ledger](references/hypothesis-ledger.md) ·
[evidence model](references/evidence-model.md) ·
[experiment design](references/experiment-design.md) ·
[regression windows](references/regression-windows.md) ·
[investigation workspace](references/investigation-workspace.md) ·
[production safety](references/production-safety.md) ·
[communication](references/communication.md) ·
[tool discovery](references/tool-discovery.md)

---

## What it is not

- **Not a debugger.** A known bug with a stack trace needs fixing, not
  investigating.
- **Not incident response.** It does not page anyone, mutate infrastructure, or
  run a status page.
- **Not a code reviewer.** It reads the code the evidence points at — use
  [impact-map](../impact-map/README.md) to map a change's blast radius, and
  [production-guard](../production-guard/README.md) to gate a release.
- **Not a report generator.** The artifact is a decision you can act on. The
  workspace exists to support it, not to be read.

## Limitations

- It cannot see what it cannot reach. With no logs, metrics, or traces, it
  establishes candidate mechanisms and the evidence that would discriminate
  between them — not a cause. That boundary is stated in the answer, every time.
- Confidence above `LIKELY` usually requires reproduction or a controlled
  comparison. In a repository-only environment, most conclusions honestly stop
  at `POSSIBLE` or `LIKELY`.
- It investigates one symptom at a time. Two unrelated incidents in one report
  should be split, and the skill will say so.
- It does not monitor. It answers about a window that has already happened.

## License

MIT — see [LICENSE](../../LICENSE).
