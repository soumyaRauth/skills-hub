# Example — Bulk operation

**Risk: High.** Destructive and multi-record. Demonstrates partial failure,
concurrency, progress reporting, retry safety, and user feedback.

```
╔══════════════════════════════════════════╗
║       PRODUCTION GUARD REPORT            ║
╚══════════════════════════════════════════╝

CHANGE
Add bulk deletion to user management: an admin selects multiple users and
deletes them in one request.

RISK CLASSIFICATION
High — destructive, multi-record, and irreversible.

VERDICT
🔴 DO NOT SHIP

BLOCKERS  2      HIGH  2      MEDIUM  1      LOW  1

──────────────────────────────────────────

BASELINE
Scope:  targeted — tests/users/ (full suite runs in CI only)
Result: 38 passed, 1 failed
Pre-existing failures: UserExportTest::test_csv_headers — fails on main before
                       this change; unrelated to bulk deletion.

──────────────────────────────────────────

FUNCTIONAL VALIDATION     7/7   passed
REGRESSION VALIDATION     11/13 passed
SECURITY                  3/4   passed
DATA INTEGRITY            2/5   passed
FAILURE SCENARIOS         4/8   validated
PERFORMANCE               1/3   validated
OBSERVABILITY             0/2   validated

REGRESSION MATRIX

  BEHAVIOR                          STATUS   EVIDENCE
  ────────────────────────────────────────────────────────────────
  Individual deletion works         PASS     tests/users/ (executed)
  Admin authorization enforced      PASS     tests/users/ (executed)
  Audit record per deletion         FAIL     absent in bulk path (analyzed)
  Billing records preserved         PASS     no cascade (analyzed)
  Soft-delete flag respected        PASS     tests/users/ (executed)
  Retry produces no duplicates      WARNING  no operation key (analyzed)

──────────────────────────────────────────

🔴 BLOCKERS

#1 Authorization is checked once for the actor, never per target.

   Category:       Security
   Evidence:       BulkDeleteController::destroy() calls
                   authorize('bulkDelete', User::class) once, then deletes every
                   id in the request body without a per-record policy check
                   (BulkDeleteController.php:34). The single-delete path does
                   check per record (UserController.php:71).
   Risk:           A team admin can delete users outside their own team by
                   supplying their ids. The UI never offers them, but the ids
                   come straight from the request body.
                   EXECUTED — a test posting a foreign user id deleted it.
   Confidence:     High — observed.
   Recommendation: Authorize each target, or scope the delete query to the
                   actor's team before executing it.

#2 Partial failure leaves the operation half-applied with no record of what
   succeeded.

   Category:       Data integrity
   Evidence:       BulkDeleteService::execute() deletes each user in its own
                   implicit transaction inside a loop; the handler logs and
                   re-raises on the first exception (BulkDeleteService.php:28-41).
   Risk:           A failure at item 47 of 100 leaves 46 deleted, 1 failed, and
                   53 untouched. The API returns 500, so the client cannot tell
                   which. Retrying deletes an arbitrary further subset. There is
                   no persisted operation record to reconcile against.
   Confidence:     High — verified by reading the loop and the caller.
   Recommendation: Decide the semantics explicitly. Either wrap in one
                   transaction (atomic), or return a per-item result set and make
                   the operation safely retryable.

──────────────────────────────────────────

⚠️ WARNINGS

🟠 HIGH — No audit record is written for bulk deletions.

   Evidence:       Individual deletion calls AuditLog::record()
                   (UserService.php:88); the bulk path deletes via the query
                   builder and does not (BulkDeleteService.php:31).
   Risk:           The highest-volume deletion path is unattributable. The audit
                   trail appears complete while missing exactly the operations
                   most worth auditing.
   Recommendation: Emit one audit record per deleted user, with the acting admin
                   and an operation id shared across the batch.

🟠 HIGH — N+1 query across the deletion loop.

   Evidence:       Each iteration loads the user, then its subscription, inside
                   the loop (BulkDeleteService.php:28-36). ANALYZED — 3 queries
                   per item.
   Risk:           The UI permits selecting 500 users → ~1,500 queries in one
                   request, against a 30-second gateway timeout. A timeout here
                   produces exactly the partial state described in blocker #2.
   Recommendation: Batch the loads, or move the operation to a background job
                   with progress.

🟡 MEDIUM — Partial results are not communicated to the user.

   Evidence:       The endpoint returns 204 on success and 500 on any failure;
                   the UI shows "Something went wrong" (BulkActions.tsx:62).
   Risk:           After a partial failure the admin does not know which users
                   were deleted, and the natural response — retry — makes it
                   worse.
   Recommendation: Return per-item outcomes and render "37 of 50 deleted, 13
                   failed" with a retry for the failures.

🔵 LOW — No confirmation step for an irreversible bulk action.

   Recommendation: Require typed confirmation above a threshold count.

──────────────────────────────────────────

TESTS EXECUTED

  pytest tests/users/ -q                        →  38 passed, 1 failed (pre-existing)
  pytest tests/users/bulk_delete_test.py -q     →  7 passed
  pytest tests/users/bulk_authz_test.py -q      →  FAIL (foreign id deleted)
  mypy app/users                                →  PASS

──────────────────────────────────────────

UNVERIFIED

- Behavior at 500 selected users — not executed; reasoned from query count
- Two admins bulk-deleting overlapping selections concurrently
- Recovery path after partial deletion — no restore mechanism found to test
- Gateway timeout behavior — infrastructure not available locally

──────────────────────────────────────────

RECOMMENDED ACTIONS

1. Authorize every target record (blocker #1).
2. Define and implement partial-failure semantics (blocker #2).
3. Write audit records in the bulk path.
4. Eliminate the N+1, or move to a background job with progress.
5. Return and display per-item outcomes.
6. Add a concurrency test for overlapping bulk deletions.

FINAL VERDICT
🔴 DO NOT SHIP — 2 blocking issues. One permits deleting records outside the
actor's scope; the other leaves irreversible partial state that cannot be
reconciled.
```
