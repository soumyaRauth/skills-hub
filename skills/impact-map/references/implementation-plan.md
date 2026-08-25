# Implementation Plan

The plan is the handoff artifact. It is produced **only when the user asks for
it**, after the map, and it still contains no code — it tells an engineer (or a
fresh agent session with no memory of the analysis) exactly what to do, in what
order, and how to know each step worked.

A plan that cannot be executed without re-reading the analysis has not handed
anything off.

## Structure

```
IMPLEMENTATION PLAN
────────────────────────────────────────

FROM          <the change statement from the map>
SCOPE         <packages and layers the plan touches>
RISK          <score → band, carried over from the map>

PREREQUISITES

- <the OPEN QUESTIONS and 🟨 checks that must resolve before step 1>
- <each one names who or what answers it>

STEP 1 — <goal, in one line>

  Files:      <repository-relative paths>
  Resolves:   F3, F9
  Depends on: —
  Change:     <what to do, in prose — no code>
  Evidence:   <one line per finding: what the map observed there>
  Verify:     <the command, test, or observation that shows this step worked>
  Rollback:   <how to undo it, or the flag that gates it>
  Stop if:    <the condition that means the plan was wrong — optional>

STEP 2 — …

COVERAGE

  F1 → step 3     F2 → step 3     F3 → step 1     F4 → step 4
  F5 → prerequisite               F6 → step 5     …
  Deferred:  F9 — <why, and what happens instead>
  Unmapped:  none

HANDOFF

<what a fresh session needs: the branch, this plan, the unresolved questions,
 and what to validate after implementation>
```

## Coverage rules

The coverage table is what makes this a handoff rather than a to-do list.

| Finding | Requirement |
| --- | --- |
| 🟥 MUST CHANGE | Resolved by **exactly one** step. A 🟥 with no step is an invalid plan — fix the plan, do not quietly drop the finding. |
| 🟧 LIKELY AFFECTED | Mapped to a step, or listed under `Deferred` with a reason and a consequence. |
| 🟨 NEEDS VERIFICATION | Becomes a **prerequisite**, resolved before the first step that depends on it — never a check buried inside an implementation step. |
| ⚠️ HIDDEN COUPLING | Each one gets a step or an explicit decision recorded in `Deferred`. These are the findings that get lost, so they are the ones the table exists for. |
| ⬜ OUT OF SCOPE | Not in the table. |

`Unmapped: none` is a claim. Check it against the map's finding ids before
writing it.

## Ordering rules

Order by dependency and by reversibility, not by layer aesthetics:

1. **Resolve prerequisites first.** A plan that starts implementing before the
   unverified findings resolve is a plan that will be rewritten mid-flight.
2. **Compatibility before change.** When a contract or stored value moves, make
   both sides tolerant first — dual-read, dual-emit, accept both values — so
   deploy order stops mattering.
3. **Then the change itself**, innermost outward: data structure, domain,
   service, serialization, authorization, UI, async work.
4. **Then data.** Backfills run after the code that can read both shapes is
   deployed.
5. **Then coverage.** Tests for the hidden-coupling paths go in with the change
   that touches them, not in a trailing "add tests" step.
6. **Cleanup last**, as its own step: remove the compatibility shim once nothing
   reads the old shape.

**Every step must leave the system working.** If the plan is stopped after any
step, what is deployed is coherent. A step that only makes sense together with
the next one is one step, not two.

Size a step to one commit. A step touching eleven files across four layers is
usually two or three steps that were not separated.

## Verification rules

`Verify` is an observation someone can actually make:

- an existing test path that now covers the behavior;
- a new test described by what it asserts ("a report query returns rows for the
  approved status"), not by an invented file name;
- a command whose output shows the change took effect;
- a manual check, when that is honestly what is available.

Never write "verify it works", and never claim a test exists that the analysis
did not observe. If a step cannot be verified, say so in the step — an
unverifiable step is a risk the reader needs to see.

## Handoff rules

The plan travels. Write it so the executing agent or engineer needs nothing else:

- **Self-contained steps.** Repository-relative paths, symbol names, and the
  one-line evidence from the map. Do not write "as established above".
- **Decisions stay open, visibly.** An unresolved OPEN QUESTION appears as a
  prerequisite or a `Stop if:`, never as an assumption baked silently into a
  step.
- **No code.** The plan says what to do; the implementation session writes it.
  Producing the plan is not permission to start editing.
- **Drift is reported, not absorbed.** If implementation shows the map was wrong
  — a finding does not exist, a new consumer appears — stop and say which
  finding changed. Re-planning quietly is how a map stops being trustworthy.
- **Point at the next gate.** The plan's last line names what should be
  validated after implementation: the hidden-coupling findings and the risk
  factors that set the band. That is exactly what
  [Production Guard](../../production-guard/README.md) consumes if the team uses
  it.

## What the plan is not

- Not a schedule. No estimates, no story points, no dates.
- Not a design document. If the plan needs to argue an approach, that argument
  belongs in the map's OPEN QUESTIONS, resolved by a human.
- Not a place to widen scope. A step that is not resolving a finding from the
  map does not belong in the plan; if the analysis missed something, add the
  finding to the map first.
