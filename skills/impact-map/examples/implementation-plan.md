# Example 5 — Implementation plan handoff

The plan produced *after* [example 4](cross-module-change.md), on an explicit
"turn this into an implementation plan". Same finding ids (F1–F10), no code, and
written so a session that never saw the analysis can execute it.

## Request

> Yes — turn that into an implementation plan.

---

```
IMPLEMENTATION PLAN
────────────────────────────────────────

FROM   Rename the enrollment status value COMPLETED to APPROVED across the
       domain, persistence, API, frontend, async jobs, and reporting.
SCOPE  backend (models, services, api, jobs, reports), frontend, fixtures and
       seed data, one data migration.
RISK   15 / 18 → High. Set by string-coupled untested paths and by consumers
       outside this repository.
```

## Prerequisites

Resolve these before step 1. Two of them can change the plan.

```
P1 · Do any dashboards or warehouse models filter on 'completed'?          (F5)
     Ask the data team. If yes, the backfill needs a coordinated window and
     step 4 grows a communication step.

P2 · Does the partner system in the nightly sync expect the literal value?  (F7)
     Ask whoever owns that integration. If yes, the sync must translate at
     the boundary and keep emitting 'completed' — step 1 changes shape.

P3 · Read backend/jobs/reminder_scheduler.py.                              (F10)
     History says it moves with the enum in 8 of 11 commits; the code does
     not say why. If it consumes the status, it gains its own step. If it
     does not, record that and drop F10.
```

## Steps

```
STEP 1 — Accept both values on every string-coupled path

  Files:      backend/reports/completion_report.py
              backend/jobs/nightly_sync.py
              frontend/src/components/EnrollmentBadge.jsx (badge + list filter)
  Resolves:   F6, F7, F8
  Depends on: P2
  Change:     Widen each comparison to match both 'completed' and 'approved'
              before anything is renamed, so deploy order stops mattering.
              In the frontend, put the accepted values in one shared constant
              rather than two inlined comparisons.
  Evidence:   F6 — WHERE status = 'completed' in raw SQL, never touches the
              enum. F7 — if row["status"] == "completed", querying the table
              directly. F8 — status === 'completed' in the badge and a second
              copy in the list filter.
  Verify:     A report query returns rows for enrollments in either state, and
              the sync selects them. Neither path has a test today — add one
              per path in this step; they are the coverage gap that makes this
              change High risk.
  Rollback:   Revert. Widened comparisons are inert until the rename lands.
  Stop if:    P2 came back "the partner expects 'completed'" — the sync then
              needs a boundary translation, not a widened comparison.

STEP 2 — Rename the enum member and its stored value

  Files:      backend/models/enrollment.py
              backend/services/enrollment_service.py
  Resolves:   F1, F2
  Depends on: Step 1 deployed.
  Change:     Rename EnrollmentStatus.COMPLETED to APPROVED and its value from
              "completed" to "approved". Update the typed writer in the same
              step — the rename breaks it, so they are one commit, not two.
  Evidence:   F1 — COMPLETED = "completed"; member name and stored string both
              carry the old name. F2 — the sole typed writer,
              enrollment.status = EnrollmentStatus.COMPLETED.
  Verify:     The existing service test for the completion transition passes
              against the new member; the type checker reports no remaining
              references to the old name.
  Rollback:   Revert. Existing rows still hold 'completed' and step 1 left
              every reader tolerant of both.

STEP 3 — Update fixtures and seed data

  Files:      test fixtures and the local seed script writing the literal
  Resolves:   F9
  Depends on: Step 2.
  Change:     Write the new value. Keep one fixture holding the legacy value
              until step 6, so the compatibility paths stay exercised.
  Evidence:   F9 — fixtures and the seed script both write "completed".
  Verify:     Suite passes; the legacy-value fixture still exercises the
              widened comparisons from step 1.
  Rollback:   Revert.

STEP 4 — Backfill existing rows

  Files:      a new migration against enrollments.status
  Resolves:   F3
  Depends on: Steps 1–2 deployed, and P1 answered.
  Change:     Update rows holding 'completed' to 'approved'. Check for indexes
              on the column before running it against production volume.
  Evidence:   F3 — the enum persists its value and the reporting SQL matches on
              'completed', confirming what is stored.
  Verify:     No rows remain with the legacy value; the report and the sync
              return the same counts before and after.
  Rollback:   The reverse update, which is only safe while step 6 has not run.
              After step 6 this step is one-way.
  Stop if:    P1 identified a warehouse consumer that has not been coordinated.

STEP 5 — Settle the API wire format

  Files:      backend/api/enrollments.py
  Resolves:   F4
  Depends on: Step 4, and the deprecation decision in OPEN QUESTIONS.
  Change:     Either emit the new value directly, or translate at the boundary
              for one release. This is a decision, not a discovery — it needs
              an answer before the step runs.
  Evidence:   F4 — returns enrollment.status.value, so the wire format follows
              the enum.
  Verify:     A response-shape assertion covering whichever option is chosen.
              None exists today.
  Rollback:   Revert; the boundary translation is the safer default because it
              is reversible without touching consumers.

STEP 6 — Remove the compatibility shim

  Files:      the three files from step 1, plus the legacy fixture
  Resolves:   —  (cleanup; introduces no new finding)
  Depends on: Step 4 complete, and no 'completed' rows remaining.
  Change:     Narrow the comparisons back to the single value and drop the
              legacy fixture.
  Verify:     The suite passes with no fixture holding the legacy value.
  Rollback:   Revert — but after this step, step 4 is no longer reversible.
```

## Coverage

```
F1 → step 2      F2 → step 2      F3 → step 4      F4 → step 5
F5 → P1          F6 → step 1      F7 → step 1      F8 → step 1
F9 → step 3      F10 → P3

Deferred:  none
Unmapped:  none
```

## Handoff

Execute on a branch off the current main with this plan and the map from
example 4. Two prerequisites (P1, P2) are answered by people, not by the
repository, and P3 can add a step — do not start step 1 before all three come
back.

If implementation contradicts the map — a finding that does not exist, a
consumer nobody knew about — stop and say which finding changed rather than
re-planning silently.

After implementation, what deserves validation is exactly what set the risk
band: the three formerly string-coupled paths (F6, F7, F8), the backfill's row
counts, and the API wire format decision. That is the input for a
[Production Guard](../../production-guard/README.md) pass if the team runs one.
