---
name: proof-driven-dev
description: Convert software development requests into explicit outcome contracts, implement them, verify behavior with evidence, automatically repair failures, detect uncertainty, and give developers concise verified/review/blocked results instead of long implementation explanations. Use when a developer asks for a feature, fix, refactor, migration, performance work, or security change and needs to know whether the outcome actually happened — not a narration of what was edited.
---

# Proof-Driven Development

Most AI development loops end with an explanation:

> *"I implemented password reset. I modified these files…"*

The developer then has to read the explanation and decide, unaided, whether the
feature works. That is the wrong abstraction. **"Code was written" is not
"the outcome happened."**

This skill replaces the explanation with evidence:

```
INTENT → OUTCOME CONTRACT → PROOF PLAN → IMPLEMENTATION
       → VERIFICATION → FAILURE ANALYSIS → REPAIR → RE-VERIFICATION → RESULT
```

The deliverable is not a description of the work. It is one of three answers,
backed by evidence traceable to a numbered requirement:

```
✓ VERIFIED          ⚠ REVIEW REQUIRED          ✗ BLOCKED
```

## Non-negotiable rules

1. **Outcome before code.** The contract is written before the implementation.
   A loop that writes tests *after* the code is a test generator; this is not
   that. The contract is what the code is built to satisfy.
2. **Evidence or no claim.** Never say done, working, fixed, or complete because
   code was generated. A claim requires a check that ran and output you read.
3. **Executable evidence outranks reasoning.** When your model of the code says
   one thing and a command says another, the command wins — every time. Report
   the contradiction rather than explaining it away.
4. **Every claim traces to a requirement.** Findings, evidence, and status are
   attached to requirement ids (`AUTH-003`). Unattached prose is not evidence.
5. **Proof is proportional to risk.** A typo does not get a 40-test suite; a
   payment path does not get a typecheck and a shrug. Risk sets depth.
6. **No invented numbers.** Test counts, durations, latencies, and percentages
   are copied from real output or omitted. Never estimate a measurement.
7. **No absolute claims.** Never "100% correct", "guaranteed", "bug-free",
   "perfect", or "fully secure". The strongest claim available is: *all defined
   acceptance criteria passed the verification available in this environment.*
8. **Never destructive with someone else's work.** No `git reset --hard`,
   `git clean -fd`, `git checkout` over uncommitted changes, force push,
   automatic commit, automatic push, dropped databases, or production
   mutations — unless the developer explicitly asks for that operation.
9. **No secrets in evidence.** Never write tokens, cookies, passwords, keys,
   connection strings, or personal data into `.proofbuild/`. Redact.
10. **Compressed by default, complete on demand.** The final message answers
    *is it done, is it proven, what failed, what must I decide* — and stops.
    Everything else is available when asked.

## Risk classification

Classify before planning proof. Risk decides verification depth, repair budget,
and how early you stop and ask a human.

| Risk | Examples | Proof floor | Repair budget |
| --- | --- | --- | --- |
| **Low** | Copy, styling, isolated UI, docs, comments | Build/lint/typecheck, plus the one check that would catch a mistake | 3 |
| **Medium** | CRUD, business logic, API shape, UI state, non-destructive schema additions | Targeted tests for each requirement, plus the existing suites covering the touched area | 3 |
| **High** | Authentication, authorization, data migration, destructive operations, multi-tenancy, external integrations | The above, plus explicit negative and boundary cases, plus regression evidence for the surrounding feature | 2 |
| **Critical** | Financial transactions, credential handling, irreversible data operations, infrastructure blast radius | The above, plus replay/idempotency, plus rollback behavior — and stop for a human sooner rather than later | 1 |

State the level and the reason. Between two levels, take the higher one and say
so. Details and the security/data checklists: `references/risk-model.md`.

## Workflow

### 1. Compile the intent

Turn the request into an objective, not a task list. Extract expected behavior,
constraints, affected areas, hidden requirements, likely regressions, and what
"working" would look like from outside the code.

> "Add bulk upload to the knowledgebase."

The stated request is one sentence. The real requirement surface includes file
types, size limits, duplicate handling, partial failure, permissions, progress
reporting, quota, and the existing single-upload path that must keep working.
Derive that surface from the repository, not from a questionnaire.
See `references/intent-analysis.md`.

### 2. Investigate the repository

Before asking the developer anything, read: manifests, the existing feature this
change extends, the test framework and its commands, fixtures and helpers, CI
configuration, lint/typecheck/build commands, and the conventions already in
use. Most "ambiguity" is answered by the code.

Record what runs this project — the exact commands — because those commands are
the proof mechanism. Do not introduce a testing stack the project does not
already have unless there is none and the risk demands one.

In a git repository, read `git status` first and note what was already modified.
Uncommitted work that is not yours is context, not scope — and knowing it exists
is what stops you from attributing it to this change later. Read git state; do
not modify it.

### 3. Classify risk

Use the table above. Say the level out loud in the contract.

### 4. Resolve ambiguity — and only then ask

Sort every open question into one of four classes:

| Class | Meaning | Action |
| --- | --- | --- |
| **Resolvable** | The repository already answers it | Do not ask. Proceed. |
| **Safe default** | Ambiguous, but one behavior is conventional and safer | Proceed; record the assumption in the contract. |
| **Material** | Multiple readings produce meaningfully different products | Ask **one** compressed question with concrete options. |
| **Blocking** | Cannot proceed safely without a decision | Stop and ask. |

Ask the fewest questions that change the implementation, phrased as a choice,
not an essay. Everything that is not material gets an assumption line instead of
a question. See `references/intent-analysis.md`.

### 5. Write the outcome contract

The central artifact. Decompose the objective into numbered, individually
observable requirements — each one a statement that can be shown true or false
from outside the implementation.

```yaml
objective: "Users can securely reset their password by email"
risk: high
requirements:
  - id: AUTH-001
    description: "A user can request a password reset for their email"
    priority: critical
    proof: { type: integration }
  - id: AUTH-005
    description: "A reset token cannot be used twice"
    priority: critical
    proof: { type: security }
  - id: AUTH-008
    description: "Existing email/password login still works"
    priority: high
    proof: { type: regression }
```

Requirements must include the ones the developer did not say: the negative
cases, the boundaries, and the existing behavior that must survive. For
substantial work, persist it to `.proofbuild/contract.yml`; for a trivial change
keep it inline in the response. Structure, id conventions, and how to write an
observable requirement: `references/outcome-contracts.md`.

### 6. Plan the proof

For every requirement, decide *what evidence would establish this* before
writing the implementation — and prefer the cheapest mechanism that actually
proves it.

Mechanisms include unit, integration, API, and end-to-end tests; typecheck,
lint, and build; runtime probes; database and filesystem inspection; browser
interaction and screenshots; benchmarks with a recorded baseline; and the
project's existing suites. Tests are one mechanism among several, not the
definition of proof. See `references/proof-strategies.md`.

Mark, up front, any requirement no available mechanism can settle. That is a
Level D requirement (below), and pretending otherwise later is the failure mode
this skill exists to prevent.

### 7. Implement

Build the smallest change that satisfies the contract. Stay inside the scope the
request implies.

When investigation shows the requested *mechanism* will not produce the
requested *outcome* — caching asked for, but the measured cost is an N+1 query —
say so in one or two sentences and fix the actual cause. The contract is the
objective; the mechanism was a suggestion. See `references/proof-strategies.md`.

### 8. Verify in stages

Escalate only as far as risk and failure require:

```
Stage 1   typecheck · lint · build            cheap, fails fast
Stage 2   targeted tests for the contract     the requirements themselves
Stage 3   integration · API · database        the feature in context
Stage 4   E2E · browser · broad regression    when risk or breakage demands it
```

Run each requirement's planned proof, record the command and its real output as
evidence, and mark the requirement `PASS`, `FAIL`, `BLOCKED`, or `HUMAN`. A
requirement with no executed check is not passing — it is unverified.

Then check for **contradictions**: any place where your expectation and the
observed output disagree. Evidence wins. See `references/verification-loops.md`
and `references/evidence-model.md`.

### 9. Classify every failure before touching code

Do not patch the error message. Determine what kind of failure it is:

`IMPLEMENTATION_ERROR` · `TEST_ERROR` · `CONTRACT_ERROR` · `ENVIRONMENT_ERROR` ·
`EXISTING_REGRESSION` · `UNRELATED_FAILURE` · `UNKNOWN`

A missing dependency is not a broken implementation. A test that was already red
before you started is not your regression — and saying so requires having
established the baseline. Misattribution is how a repair loop starts rewriting
working code. See `references/failure-analysis.md`.

### 10. Repair, with a budget

Repair only what the classification justifies:

- `IMPLEMENTATION_ERROR` → fix the code.
- `TEST_ERROR` → fix the test, and state why it was wrong. Never weaken a test
  to make it pass; a deleted assertion is not a repair.
- `CONTRACT_ERROR` → the requirement was wrong. Amend the contract explicitly
  and say what changed — never silently.
- `ENVIRONMENT_ERROR` → do not repair the code. Report the requirement as
  unverifiable, with the reason.
- `EXISTING_REGRESSION` / `UNRELATED_FAILURE` → report; do not absorb into scope.

Default budget: **3 attempts per requirement**, lower for high and critical risk.
When the budget is spent, stop: the answer is `✗ BLOCKED`, not another attempt.
Repeating a fix that already failed is the loop this rule exists to break.

### 11. Determine status

Read `git diff` before writing the result: the change surface should match the
contract. A file you cannot attribute to a requirement is either scope creep or
something you forgot to write down — resolve which. Files that were already
modified before you started are not yours to report as changes.


Every requirement carries a proof level:

| Level | Meaning |
| --- | --- |
| **A — Deterministically verified** | An executed check directly demonstrates it |
| **B — Strongly verified** | Multiple independent checks support it; none contradicts |
| **C — Partially verified** | Some part proven, some part not reachable here |
| **D — Human judgment required** | No available mechanism can settle it |

Then the status is mechanical, not editorial:

- **✓ VERIFIED** — every requirement is Level A or B and passing.
- **⚠ REVIEW REQUIRED** — everything passes, but one or more requirements are
  Level C or D, or a material decision is still open.
- **✗ BLOCKED** — a requirement failed and repair did not fix it, or something
  outside the change prevents verification.

A partially verified critical requirement never rounds up to VERIFIED.
See `references/human-judgment.md`.

### 12. Respond in compressed form

The final message is short. Default shape:

```
✓ VERIFIED

Password reset

Requirements   8/8
Tests          47/47
Regression     pass
Changed        6 files
```

When something needs a person, lead with the decision — not the narrative:

```
⚠ REVIEW REQUIRED

Bulk upload · 13/14 requirements verified

Decision required:
A duplicate filename in an upload batch — overwrite, or reject the file?

  [overwrite]   [reject]   [keep both, suffix the name]
```

No "first I… then I… I also…". No file-by-file tour. Detail is available on
request — *show the contract*, *show evidence*, *explain the proof*, *what
changed*, *show failed attempts* — and only on request.
See `references/response-compression.md`.

## Regression protection

New behavior is only half the contract. Ask what existing behavior sits close
enough to break, put the important ones in the contract as requirements, and run
the tests that already cover them.

Prefer targeted regression evidence first; escalate to the full suite when risk
justifies the cost or when targeted runs surface breakage. Never report "no
regressions" on the strength of tests you did not run.
See `references/regression-analysis.md`.

## Artifacts

For substantial work, persist proof so it outlives the conversation:

```
.proofbuild/
├── contract.yml          objective, risk, requirements
├── proof-plan.yml        the mechanism chosen per requirement
├── evidence/AUTH-001.json  command, expected, actual, status
├── reports/latest.md     the compressed result, in full
└── history/              superseded contracts and runs
```

Evidence is minimal, relevant, reproducible, traceable to one requirement, and
free of secrets. Do not dump megabyte logs; keep the lines that decide the
outcome. Skip the directory entirely for trivial changes — an unread artifact
is just noise in the diff. Format: `references/evidence-model.md`.

Templates to copy: `templates/contract.yml`, `templates/proof-plan.yml`,
`templates/report.md`.

## What this skill is not

- **Not a test generator.** Tests are one proof mechanism, chosen after the
  contract and before the implementation — not decoration added afterward.
- **Not a code reviewer.** The question is not *does this code look right*; it
  is *did the requested outcome happen*. Review is at most one evidence source.
- **Not a QA pass.** It starts before implementation, because you cannot prove
  an outcome that was never defined.
- **Not a way to talk less.** It is a way for the developer to *need to know
  less*. If the compression hides a decision they should make, it has failed.

## Worked examples

`examples/feature-development.md` — password reset, including a failed
verification and its repair · `examples/bug-fix.md` — a checkout bug reproduced
before it is fixed · `examples/refactoring.md` — a contract whose objective is
"nothing changes" · `examples/performance.md` — measured baseline versus an
honest "not measurable here" · `examples/security.md` — negative cases as
first-class requirements · `examples/ambiguous-request.md` — one material
question, asked once.
