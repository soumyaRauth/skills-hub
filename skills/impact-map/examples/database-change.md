# Example 3 — Database / schema change

A Laravel application gaining a new column that participates in a workflow.
Shows how a schema change pulls in authorization, jobs, serialization, and
existing-row semantics.

## Request

> Course completions need an approval step. Add an approval status so a manager
> can approve or reject a completion, and show it in the API and UI.

**CHANGE STATEMENT:** Introduce `approval_status` on course completions, with
manager-driven transitions, exposed through the existing API and UI.

**INTERPRETATION:** `approval_status` is modeled as a new column alongside the
existing `status`, not as a replacement for it — the request describes an extra
step, not a renamed one. Confirm before implementing.

## Change surface

Migration and model, the service that owns completion transitions, the API
resource and controller, the policy governing manager actions, one job that
fires on completion, plus fixtures and a report query that filter on status.

## 🟥 MUST CHANGE

```
database/migrations/  (new migration)

  Relationship:   `course_completions` has no approval column today.
  Evidence:       2024_01_01_000000_create_course_completions_table.php defines
                  id, user_id, course_id, status, completed_at — no approval
                  field.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Add `approval_status` with an explicit default for existing
                  rows, plus an index if the reports filter on it.
```

```
app/Models/CourseCompletion.php

  Symbol:         $fillable, $casts
  Relationship:   Model defines the persisted shape and status casting.
  Evidence:       `protected $casts = ['status' => CompletionStatus::class]`.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Add the column to $fillable and cast it to a new
                  ApprovalStatus enum.
```

```
app/Services/CourseCompletionService.php

  Symbol:         complete()
  Relationship:   The only writer of completion state found in the repository.
  Evidence:       Sets `$completion->status = CompletionStatus::COMPLETED` and
                  dispatches SendCompletionCertificate.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Initialize approval_status on completion and add the
                  approve/reject transitions, including the guard for which
                  states may transition.
```

```
app/Http/Resources/CourseCompletionResource.php

  Relationship:   Serializes the model for every API response.
  Evidence:       Returns id, status, completed_at.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Expose approval_status (additive, backward compatible).
```

## 🟧 LIKELY AFFECTED

```
app/Policies/CourseCompletionPolicy.php

  Symbol:         update()
  Relationship:   Governs who may modify a completion; approval is a new
                  privileged action with no existing rule.
  Evidence:       Policy has view/update/delete; no approve ability.
  Classification: 🟧 LIKELY AFFECTED
  Confidence:     High
  Action:         Add an `approve` ability and register it. Confirm whether
                  managers are identified by role, team, or course ownership.
```

```
app/Jobs/SendCompletionCertificate.php

  Relationship:   Dispatched when a completion is marked complete; a certificate
                  probably should not be issued before approval.
  Evidence:       Dispatched from CourseCompletionService::complete().
  Classification: 🟧 LIKELY AFFECTED
  Confidence:     Medium
  Action:         Decide whether the trigger moves from completion to approval.
                  This is a product decision — see Open Questions.
```

## 🟨 NEEDS VERIFICATION

```
Existing rows in course_completions

  Relationship:   Every existing completion needs a defensible approval value.
  Evidence:       Table is populated in production per the seeder and factory;
                  no backfill mechanism exists in the repository.
  Classification: 🟨 NEEDS VERIFICATION
  Confidence:     Medium
  Action:         Decide: treat historical completions as pre-approved, or as
                  pending. The choice changes the migration default and whether
                  a data migration is required.
```

## ⚠️ HIDDEN COUPLING

```
app/Reports/CompletionReport.php

  Coupling type:  Raw SQL
  Relationship:   Counts completions with a raw query filtering on status.
  Evidence:       `WHERE status = 'completed'` — string literal, not the enum.
  Classification: ⚠️ HIDDEN COUPLING
  Confidence:     High
  Action:         Decide whether the report should now count only approved
                  completions. If yes, the query needs the new predicate.
```

```
database/factories/CourseCompletionFactory.php

  Coupling type:  Fixture
  Relationship:   Builds completions for every feature test.
  Evidence:       Sets status only; a non-nullable approval column without a
                  default will break every test that uses the factory.
  Classification: ⚠️ HIDDEN COUPLING
  Confidence:     High
  Action:         Add the new attribute with a sensible default and a state
                  helper for the approved case.
```

## Dependency paths

```
course_completions.approval_status          ← the change
  ↓ mapped by
app/Models/CourseCompletion.php
  ↓ written by
CourseCompletionService::complete() / approve()
  ↓ authorized by
CourseCompletionPolicy::approve()
  ↓ serialized by
CourseCompletionResource
  ↓ returned by
routes/api.php  →  GET|POST /api/course-completions
  ↓ and read (bypassing the model) by
CompletionReport  →  raw SQL on course_completions.status
```

## Database impact

- **Migration:** additive column. Non-nullable with a default is safest; a
  nullable column pushes the "unknown state" problem into application code.
- **Existing records:** must receive a value — decide pre-approved vs pending.
- **Index:** add one if reports or list endpoints filter on the column.
- **Ordering:** the migration must land before any code path reads the column.
- **Backward compatibility:** old code ignoring a new column is safe, so the
  migration can deploy ahead of the application.

## API impact

- Adding a response field is backward compatible.
- The approve/reject action needs a new endpoint or an extension of the existing
  update route — the latter requires request validation for the new field.
- Authorization for the new action must be explicit; it does not inherit from
  the existing update ability.

## Authorization impact

Approval is a privileged transition. Required: a policy ability, a controller
authorization call, request validation restricting allowed target states, and a
UI check so the button is not shown to users who cannot use it. Server-side
enforcement is the one that matters; the UI check is cosmetic.

## Test impact

- `tests/Feature/CourseCompletionTest.php` protects the completion flow and will
  exercise the new column through the factory.
- No test covers the `pending → approved` transition or its authorization — that
  gap is a risk, since authorization regressions fail silently in the
  permissive direction.

## Risk

**Medium** — the schema change is additive and safe, but the surface spans
persistence, authorization, async work, and a raw-SQL report, and the historical
data decision has no reversible default.

## Recommended implementation order

1. Resolve the open questions (existing rows, certificate timing, manager
   definition).
2. Migration with explicit default; index if needed.
3. Enum + model casts and fillable.
4. Service transition logic and guards.
5. Policy ability and controller authorization.
6. Request validation and API resource.
7. UI display and gated action.
8. Job trigger adjustment if the certificate moves to approval.
9. Factory, feature tests including the authorization negative case.
10. Revisit the raw-SQL report predicate.

## Open questions

- Do historical completions count as approved?
- Should the certificate be issued on completion or on approval?
- Who is a "manager" here — a role, the course owner, or a team relationship?
- Should the completion report now count approved completions only?
