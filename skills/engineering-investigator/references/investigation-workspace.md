# The Investigation Workspace

State exists so that a second session — or a second engineer — can pick the case
up without re-deriving it, and so that no experiment is run twice. It is not a
report, and it is not a diary.

```
.agent-investigation/
├── incident.md      report, normalized symptom, scope, capabilities, status
├── hypotheses.md    the ledger
├── evidence.md      numbered observations, typed and sourced
├── experiments.md   question, method, prediction, observation, elimination
├── timeline.md      only when the order of events is itself evidence
└── conclusion.md    cause, confidence, verification, recommendation
```

## Create the smallest set that carries the state

| Lane | Files |
| --- | --- |
| QUICK | none |
| STANDARD | `incident.md` + `evidence.md`; add `hypotheses.md` once three or more are live |
| INCIDENT | all of the above; `experiments.md` once an experiment is designed; `timeline.md` only if sequence matters |

Create a file when it has content that belongs in it. An empty `timeline.md` is
noise in someone's diff, and `conclusion.md` written before there is a
conclusion is worse than noise.

Tell the user the workspace exists, in one line, once. Add
`.agent-investigation/` to `.gitignore` if the project's convention is to ignore
scratch directories, and ask before committing it.

## What goes in, what stays out

**In:** the report verbatim, the normalized symptom, capabilities and access
boundaries, scope findings, hypotheses with kill conditions and statuses,
evidence that changed a status, experiments with their predictions and outcomes,
open questions, the next action, and the conclusion when reached.

**Out:** internal reasoning and deliberation, narration of what you did in what
order, every command you ran, raw log dumps (keep the deciding lines, cite the
file for the rest), speculation not framed as a hypothesis, and anything
secret — tokens, credentials, connection strings, customer names, personal data.
Redact by shape: `postgres://user:***@host/db`.

Prose costs the next reader time. Every line should be something they could act
on or check.

## File formats

**`incident.md`**

```markdown
# Investigation — checkout slowness

## Report
"Checkout has become very slow since yesterday." — reported by support, 2026-08-26

## Normalized symptom
Symptom     Elevated latency on POST /checkout
Who         All tenants (E2)
Where       Production, all regions checked (E2)
What        Checkout submit; other endpoints normal (E5)
Since       2026-08-25 ~14:00 UTC (E3)
Frequency   Every request (E3)
Impact      Checkout p95 310 ms → 2.1 s

## Capabilities
Available     repository, git history, deploy log, api access log, test suite
Not available production DB, APM traces, customer environment

## Scope
Population all · Surface one endpoint · Time since deploy · Persistence every request

## Status
Leading: H2 (deploy regression). Confidence Medium.
Next: compare query count for POST /checkout across v1.8 and v1.9.
```

**`hypotheses.md`** — one entry per hypothesis in the ledger format
(`hypothesis-ledger.md`), ordered with live ones first, disproven ones kept at
the bottom with the evidence that killed them.

**`evidence.md`** — numbered, typed, sourced, and stating what it did:

```markdown
## E4
FACT — v1.9 executes 47 DB queries for POST /checkout; v1.8 executes 4.
Source: query log, identical request payload, both versions, local.
Impact: supports H2; does not by itself establish the latency link.
```

**`experiments.md`** — question, method, per-hypothesis prediction, observation,
elimination. An experiment that eliminated nothing is still recorded, so nobody
repeats it.

**`conclusion.md`** — cause, confidence with the level's justification, the
evidence chain, how it was verified, what would prove it wrong, recommended
action, and residual uncertainty.

## Resuming

When `.agent-investigation/` exists, **read it before touching anything else**,
then:

1. Reconstruct: symptom, scope, capabilities, live and dead hypotheses,
   experiments already run.
2. Check freshness — has the system changed since? A deploy, a fix attempt, or a
   configuration change since the last session can invalidate earlier evidence.
   Say so rather than silently trusting it.
3. Re-verify only evidence that is both load-bearing and cheap to re-check.
4. Honor eliminations. Do not re-run a completed experiment; do not revive a
   disproven hypothesis without new evidence.
5. Take the `Next` line from `incident.md`, or choose the highest-value open
   question if it is stale.
6. Update state as you go, and leave a fresh `Next` line at the end of the
   session.

Answer the user with what changed *this* session, not with a recap of the whole
case. The recap is available in the workspace and on request.

## Closing a case

When the investigation concludes: write `conclusion.md`, set the status line in
`incident.md` to the outcome, and leave the ledger as it stands — the disproven
hypotheses are the record of what the answer had to survive.

If the investigation ends without a cause, that is also a conclusion: write what
is established, what is eliminated, what is missing, and the smallest evidence
that would move it. A case that can be resumed later is worth more than one that
was closed with a guess.
