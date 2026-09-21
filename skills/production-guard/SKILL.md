---
name: production-guard
description: Decide whether a change is safe to ship. Checks behavior, regressions, failure modes, retries and idempotency, security and tenancy, data integrity and migrations, performance at volume, observability and recovery, running the project's own checks where possible, and ends in SHIP, CONDITIONAL SHIP or DO NOT SHIP derived from explicit rules. Use when someone asks whether a change is ready to merge, release or deploy, and when meaningful work on money, authentication, authorization, migrations, bulk or destructive operations, multi-tenancy or external integrations is being wrapped up. Not for work still in progress, low-risk changes, or prototypes not headed to production.
context: fork
background: false
---

# Production Guard

A normal code review asks: *does this code look correct?*

Production Guard asks: **what happens to the product when this change reaches
real users?**

The deliverable is a production-readiness report ending in one verdict —
🟢 SHIP, 🟠 CONDITIONAL SHIP, or 🔴 DO NOT SHIP — derived from explicit checks,
not from an impression of quality.

## Activation

**Engage when** someone asks about shipping (*is this safe to merge*, *ready to
release*, *can I deploy*), or when a meaningful change has just been completed
on a high-risk surface: money, authentication, authorization, migrations, bulk
or destructive operations, multi-tenancy, external integrations, deploy
configuration.

**Stay quiet when** the work is still in progress, the change is low-risk, or
the user said it is not going to production.

**Depth** `GATING` when a person asked for the ship decision: the full report
and a verdict. Otherwise `CONSULT`. After high-risk work nobody asked to gate,
name the two or three failure scenarios that most need a check, and offer the
full readiness pass. It never blocks work nobody asked it to gate.

**Composes with** `proof-driven-dev` (starts from what was proven; hands failed
checks back) · `impact-map` (the hidden-coupling findings are the regression
surface) · `standards-compass` (applicable controls feed the security category)
· `dependency-guard` (a manifest change in the diff). Observability is one of
this skill's own categories, not another skill's.

**In Claude Code** it runs as its own subagent (`context: fork`), so what it
reads and runs stays out of the conversation. It sees this file and the task it
is handed, which arrives as `ARGUMENTS:` at the end, and not the conversation.
With no task, assess the current branch's diff against its base. With nothing to
assess, return one line naming what to pass. It returns the report, and fixes
happen back in the conversation.

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. If it is
  not installed, do the smallest version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
- **Lessons.** On engaging, read `~/.skills-hub/lessons/<this skill's name>.md`
  if it exists. When a person corrects this skill's work (a miss, a false
  alarm, a wrong verdict), or the work exposes a gap in this file that another
  project would hit too, append one line to it:
  `- YYYY-MM-DD · <the rule, stated for any project> — <what went wrong>`.
  Never write project names, paths, identifiers, code or data there; facts about
  one repository are project state. Keep at most 20 lines, merging or replacing
  one to add another. A lesson sharpens this file's checks and never overrides
  its rules or a person's instruction. The file sits outside every project, so
  no read-only rule covers it. Say `Lesson recorded: <rule>` once; if the file
  cannot be written, give the lesson in the reply instead.
<!-- /skills-hub:protocol -->

## Non-negotiable rules

1. **No invented scores.** Never emit "code quality: 94%", "security: 87%", or
   any percentage not computed from checks you actually performed. Report counts
   — `Regression checks 18/20 passed` — and derive the verdict from the rules
   below.
2. **Executed ≠ analyzed.** Every check is labeled `EXECUTED` (a command ran,
   with its output) or `ANALYZED` (reasoned from source, `STATUS: UNVERIFIED`).
   Never describe reasoning as if it were a test run, and never report a
   scenario's "actual" behavior unless it was actually observed.
3. **Baseline before blame.** Establish which failures already existed before
   this change. A pre-existing failure is reported as pre-existing. When you
   cannot tell, say `STATUS: UNDETERMINED` and explain why.
4. **Evidence on every finding.** Name the file, the test output, the query, or
   the configuration. Reasoning-only findings state
   `EVIDENCE: static analysis / inferred behavior`.
5. **Never destructive.** Do not drop databases, reset environments, delete
   data, destroy containers, rewrite git history, force push, deploy, or modify
   any production-like system. Do not modify git state at all — no commits, no
   resets, no stashing. This is a validation tool.
6. **Do not inflate severity.** A blocker is something that should stop a
   release. Calling a style issue a blocker destroys the signal that makes the
   verdict worth reading.
7. **State what you could not check.** Unavailable dependencies, untestable
   production scale, and absent external systems belong in `UNVERIFIED`, not in
   silence.

## Risk classification

Classify the change first — it decides which phases run. Running every check on
a copy change wastes the reader's attention; skipping security on a payments
change is negligence.

| Risk | Examples | Required categories |
| --- | --- | --- |
| **Low** | Copy, styling, isolated UI, docs | Functional, regression, basic UX |
| **Medium** | Business logic, API changes, schema changes, shared components | Functional, regression, failure, security, data integrity, relevant performance |
| **High** | Payments, auth, authorization, destructive operations, migrations, multi-tenancy, financial logic, external integrations | All categories: the above plus concurrency, idempotency, observability, recovery, integration behavior |

State the classification and the reason in the report. When in doubt between two
levels, take the higher one and say so.

## Workflow

### 1. Understand the change

What changed and why; expected user-visible behavior; existing behavior that
must be preserved; entities, APIs, and data touched; permissions involved;
external systems involved. Then answer four questions explicitly, because they
drive most of the later analysis:

- Is the operation **synchronous or asynchronous**?
- Is it **reversible**?
- Is it **idempotent**?
- Can it **run concurrently** with itself?

Produce a `CHANGE SUMMARY`, an `EXPECTED BEHAVIOR` statement, and an
`EXISTING BEHAVIOR TO PRESERVE` list. Do not invent requirements — unclear ones
go to `OPEN QUESTIONS`.

If the repository is a git repository, use `git status` and `git diff` to scope
the change. Read git state; never modify it.

### 2. Establish baseline

Find how this project builds and tests itself: package manifests, `Makefile`,
CI configuration, contributor docs. Then determine the pre-change health —
ideally by running the suite, or a targeted subset.

Report what you actually ran:

```
BASELINE
Scope:    targeted — tests/payments/ only (full suite ~14 min)
Result:   42 passed, 2 failed
Existing failures: PaymentRetryTest::test_backoff (pre-existing, unrelated)
```

Never present a targeted run as if it were the full suite.

### 3. Build the behavioral model

A contract for the change: happy path, alternate paths, invalid input,
authorization, state transitions, side effects, persistence, external effects —
plus the **invariants** that must hold regardless of path. See
`references/behavioral-validation.md`.

### 4. Identify the regression surface

What existing behavior could this break? Existing API behavior, UI workflows,
shared components, permissions, reports, notifications, exports, integrations,
background jobs, scheduled processes. Produce a regression matrix, and mark a
row PASS only with evidence.

### 5. Failure-first analysis

The signature phase. Ask *how does this fail in production?* across input
failures, dependency failures, concurrency, retries, partial failure, and
recovery. Build the failure matrix defined in `references/failure-analysis.md`,
where each row is either executed (`ACTUAL` observed) or analyzed
(`STATUS: UNVERIFIED`).

For anything touching money, provisioning, messaging, queues, webhooks, or
external mutations, answer explicitly: **what happens if this runs twice?**

### 6–10. Security, data integrity, performance, observability, UX

Run the categories the risk level requires:

- **Security** — authentication, authorization, object-level access, input
  manipulation, data exposure, tenancy isolation. Frontend filtering is not
  security; verify backend enforcement. → `references/security-validation.md`
- **Data integrity** — transactions, atomicity, constraints, concurrent writes,
  partial updates, orphans, cascades, destructive-operation semantics, legal
  state transitions. → `references/data-integrity.md`
- **Performance** — expected volume, behavior at 10× and 100×, N+1 queries,
  unbounded memory, missing pagination, synchronous expensive work, missing
  indexes. Contextual, not reflexive. → `references/performance.md`
- **Observability** — if this fails at 3 AM, how would anyone know? Logging,
  metrics, audit trail, error reporting, job status. Risk sets the bar. →
  `references/observability.md`
- **User experience** — loading, error, and empty states; validation feedback;
  partial-failure feedback; destructive-action confirmation; accessibility where
  relevant. "Something went wrong" after a half-completed bulk operation is a
  product defect, not a cosmetic one.

### 11. Execute available validation

Read the project's own scripts before running anything. Prefer targeted
validation first, then broaden if it is practical.

Typical order: targeted tests → type check → lint → related integration tests →
build → wider suite. Record the exact command and its result for each.

Never run destructive commands. Never install packages or change configuration
to make a check pass. If the environment cannot run something, that is an
`UNVERIFIED` entry, not a failure.

### 12. Inspect results

For every failure, determine whether it is caused by this change or
pre-existing, and compare against the baseline:

```
Baseline: 312 passed, 2 failed
Current:  317 passed, 2 failed
Interpretation: no increase in failures; the 2 failures match the baseline set.
```

Do not claim causality the evidence does not support.

### 13. Classify findings

Every finding carries severity, category, evidence, confidence, and
recommendation:

| Severity | Meaning |
| --- | --- |
| 🔴 **BLOCKER** | Should prevent shipping: security vulnerability, data corruption, broken critical workflow, severe authorization failure, destructive operation without safeguards, unrecoverable partial failure. |
| 🟠 **HIGH** | Strong production risk; may block depending on context. |
| 🟡 **MEDIUM** | Meaningful concern, not necessarily release-blocking. |
| 🔵 **LOW** | Minor quality improvement. |

### 14. Verdict

Apply these rules mechanically, then explain the reasoning:

| Verdict | Rule |
| --- | --- |
| 🔴 **DO NOT SHIP** | At least one BLOCKER. |
| 🟠 **CONDITIONAL SHIP** | No blockers, but at least one HIGH finding, or a category required by the risk level left UNVERIFIED. |
| 🟢 **SHIP** | No blockers, no unresolved HIGH findings, and every category required by the risk level was validated. |

The verdict follows from the findings. If the verdict feels wrong, the findings
are wrong — fix the classification, do not override the rule.

## Report format

Emit the structure in `references/report-schema.md`: change summary, verdict,
severity counts, per-category check counts, blockers in full, warnings,
executed checks, unverified items, recommended actions, and the final verdict
restated with its reason. Formatting may adapt to context; the semantic
structure may not.

## After the verdict

Stop at the report. Offer to fix the blockers; implement only when asked. If the
user asks for fixes, address blockers first, then re-run the checks that failed
and report the new counts rather than asserting the problem is resolved.

## References

- `references/behavioral-validation.md` — behavioral contracts and regression matrices
- `references/failure-analysis.md` — failure taxonomy, idempotency, partial failure, recovery
- `references/security-validation.md` — authorization, tenancy, exposure, input manipulation
- `references/data-integrity.md` — transactions, constraints, destructive operations, state machines
- `references/performance.md` — scale reasoning, N+1, memory, indexes
- `references/observability.md` — logging, metrics, audit trails, alerting
- `references/report-schema.md` — full report structure and finding fields
- `references/change-type-checklists.md` — per-change-type checks (payments, auth, migrations, uploads, bulk, API)

If `references/team-standards.md` exists in this skill directory, read it during
phase 2 — it carries team-specific release criteria that override the defaults
here.
