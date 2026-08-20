# Testing Impact Map

## Testing philosophy

Impact Map is instruction-driven. It has no engine to unit-test, and it does not
produce deterministic output — two good reports on the same request will differ
in wording, ordering, and level of detail.

So this is **not** a pass/fail assertion suite, and the skill makes no claim of
being "100% accurate". What these fixtures test is whether the instructions
produce the **desired reasoning behavior**:

- Did the agent find the relationships that matter?
- Did it find the *indirect* ones a naive import search would miss?
- Did it classify findings at the level its evidence supports?
- Did it avoid inventing findings, consumers, or counts?
- Did it stay read-only?

Exact wording may vary. Missing a documented hidden coupling is a real failure.
Inventing a finding is a worse one.

## Running a fixture test

```bash
# 1. Install the skill, or point your agent at skills/impact-map
# 2. Open the fixture as the working repository
cd tests/fixtures/mixed-architecture

# 3. Give the agent the request below for that fixture
# 4. Compare the report against the expected findings
```

The fixtures deliberately contain **no README explaining their coupling** —
that would hand the agent the answers. All expected findings live here.

Fixtures are illustrative skeletons, not runnable applications. They do not
install, build, or execute; some reference framework symbols that are not
present. That is intentional — they exist to be *read*, and keeping them
non-runnable keeps them small.

## Scoring a run

| Check | Failure means |
| --- | --- |
| All expected MUST CHANGE locations found | The core dependency trace is too shallow |
| All expected hidden coupling found | Phase 6 is not being executed properly |
| No finding classified above its evidence | Confidence discipline is eroding |
| No invented files, consumers, or counts | The most serious failure mode |
| No file was modified | Read-only rule broken — a bug, not a preference |
| Report includes relationship + evidence per finding | It degraded into a file list |

---

## Fixture: `simple-node`

Small Node/TypeScript service: model, service, controller, tests.

**Request:** *"Extend the order cancellation window from 15 to 30 minutes."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | `src/services/orderService.ts` | `CANCELLATION_WINDOW_MINUTES = 15`, read by `canCancel()` — the authoritative rule |
| 🟥 MUST CHANGE | `tests/orderService.test.ts` | Asserts the 15-minute boundary with a 16-minute case |
| ⚠️ HIDDEN COUPLING | `src/controllers/orderController.ts` | `orderSummary()` re-implements the window with an inline `15`, no call into the service |

The controller duplicate is the point of this fixture. It shares no symbol with
the constant, so symbol search alone will not find it.

Also acceptable: noting that `canCancel()` gates on `status` and that changing
the window does not change which statuses are cancellable.

**Should not appear:** claims about UI consumers, API versioning, or database
impact — none exist in this fixture.

---

## Fixture: `nextjs`

Next.js App Router structure: route handler, server component, client component,
shared type, test fixture, API doc.

**Request:** *"Rename the `state` field on the orders API response to `status`."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | `types/order.ts` | `OrderResponse.state` — the shared wire-contract type |
| 🟥 MUST CHANGE | `app/api/orders/route.ts` | Builds the response with `state: o.status` |
| 🟥 MUST CHANGE | `app/orders/OrderStatusBadge.tsx` | `switch (order.state)` and `LABELS[order.state]` |
| 🟧 LIKELY AFFECTED | `app/orders/page.tsx` | Fetches and passes the payload through; needs confirming it does not key off the field |
| ⚠️ HIDDEN COUPLING | `__tests__/fixtures/orders.json` | Mock payload uses `"state"` — tests keep passing against the old shape |
| ⚠️ HIDDEN COUPLING | `docs/api/orders.md` | Documents `state` as the response field |
| 🟨 NEEDS VERIFICATION | External consumers of `GET /api/orders` | Route is unversioned; no consumer inventory exists in-repo |

The fixture and the doc are the interesting finds — neither is type-checked.

**Should not appear:** an assertion that external consumers definitely exist, or
that they definitely do not.

---

## Fixture: `laravel`

Laravel-style structure: model, enum, service, controller, API resource, policy,
job, migration, factory, routes, feature test, raw-SQL report.

**Request:** *"Add an approval status to course completion so a manager can
approve or reject a completion, and expose it in the API."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | new migration | `create_course_completions_table` has no approval column |
| 🟥 MUST CHANGE | `app/Models/CourseCompletion.php` | `$fillable` and `$casts` define the persisted shape |
| 🟥 MUST CHANGE | `app/Services/CourseCompletionService.php` | `complete()` is the only writer of completion state |
| 🟥 MUST CHANGE | `app/Http/Resources/CourseCompletionResource.php` | Serializes every API response |
| 🟧 LIKELY AFFECTED | `app/Policies/CourseCompletionPolicy.php` | No `approve` ability exists; `update()` only allows the owner, so a manager cannot act today |
| 🟧 LIKELY AFFECTED | `app/Jobs/SendCompletionCertificate.php` | Dispatched on completion — certificate timing may need to move to approval |
| 🟧 LIKELY AFFECTED | `routes/api.php` | Approval needs an endpoint or an extension of the complete route |
| ⚠️ HIDDEN COUPLING | `app/Reports/CompletionReport.php` | Raw SQL `WHERE status = 'completed'`, bypassing the enum and the model |
| ⚠️ HIDDEN COUPLING | `database/factories/CourseCompletionFactory.php` | `completed()` state writes the literal `'completed'`; a non-nullable column without a default breaks every test using the factory |
| 🟨 NEEDS VERIFICATION | existing rows in `course_completions` | Historical completions need a defensible approval value; no backfill mechanism exists |

Expected in the report body: the authorization section should note that the
owner-only `update()` policy is incompatible with manager approval, and the test
section should flag that no test covers a `pending → approved` transition.

Expected open questions: pre-approved vs pending for historical rows;
certificate on completion or on approval; how a "manager" is identified.

---

## Fixture: `mixed-architecture`

The hidden-coupling fixture. One status value is referenced five ways: through
the enum, through the service, in raw SQL, in a job's string comparison, and in
frontend conditionals.

**Request:** *"Rename the `COMPLETED` enrollment status to `APPROVED`. Deep
analysis."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | `backend/models/enrollment.py` | `COMPLETED = "completed"` — both the member name and the stored string |
| 🟥 MUST CHANGE | `backend/services/enrollment_service.py` | Typed writer and guard in `complete_enrollment()` |
| 🟥 MUST CHANGE | data migration for `enrollments.status` | Existing rows hold the literal `'completed'` |
| 🟧 LIKELY AFFECTED | `backend/api/enrollments.py` | Serializes `status.value`; the wire format changes even though the code may not |
| ⚠️ HIDDEN COUPLING | `backend/reports/completion_report.py` | Raw SQL `WHERE status = 'completed'` — returns zero rows after the rename |
| ⚠️ HIDDEN COUPLING | `backend/jobs/nightly_sync.py` | `record["status"] == "completed"` plus a hardcoded `state="completed"` sent to the partner system, querying the table directly |
| ⚠️ HIDDEN COUPLING | `frontend/src/components/EnrollmentBadge.jsx` | `status === "completed"` string comparison |
| ⚠️ HIDDEN COUPLING | `frontend/src/components/EnrollmentList.jsx` | A second copy of the same comparison in the filter |
| 🟨 NEEDS VERIFICATION | downstream analytics / partner contract | Raw SQL reporting implies external consumers; the partner may expect the literal value |

A strong report additionally notes that **none** of the hidden-coupling sites
have test coverage, that nothing fails at build time, and that risk is High
because of the data migration plus untested string coupling across four
runtimes.

A weak report finds only the enum and the service — everything a type checker
would have caught anyway, and nothing that would have caused the incident.

**Should not appear:** a claim that a specific external dashboard exists. The
evidence supports "analytics consumers are plausible and must be checked", not
an inventory.

---

## Adding a fixture

1. Keep it small — a dozen short files. It exists to trigger one reasoning
   behavior, not to be a realistic application.
2. Seed at least one piece of coupling that shares **no symbol** with the change
   target.
3. Do not explain the coupling inside the fixture.
4. Document the request and expected findings in this file.
5. Note which findings a naive import-graph search would miss — that gap is what
   the fixture is measuring.
