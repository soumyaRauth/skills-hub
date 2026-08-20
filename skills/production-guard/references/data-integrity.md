# Data Integrity

The question behind every check here:

> Can this operation leave the database in an invalid or surprising state?

Code that computes the right answer and persists it wrongly is worse than code
that fails loudly, because the damage accumulates silently.

## Transactions and atomicity

- Does the operation span multiple writes? If so, are they in one transaction?
- Does the transaction boundary include the writes that must succeed or fail
  together — and exclude the external calls that must not be retried by a
  rollback?
- Is an external side effect (charge, email, webhook) performed **inside** a
  transaction that might roll back afterwards? The rollback undoes the row, not
  the email.
- Are errors caught in a way that silently commits partial work?

The frequent anti-pattern:

```
for record in records:
    delete(record)        # each commits independently
```

Failure at item 47 leaves 46 deleted, 1 failed, 53 untouched, and no record of
which is which.

## Constraints

Are the invariants enforced by the database or only by application code?
Uniqueness enforced in application code alone is a race condition with a
friendly name. Check foreign keys, unique constraints, check constraints,
nullability, and defaults — and whether the change adds a state the existing
constraints do not cover.

## Concurrent writes

- Two requests updating the same row: last-write-wins, or lost update?
- Is there optimistic locking (version column) or pessimistic locking (select
  for update) where it matters — balances, counters, quotas, statuses?
- Read-modify-write cycles are the usual offender. `count = count + 1` in the
  database is safe; reading, incrementing in the application, and writing back
  is not.

## Orphans and cascades

- Does deleting a parent leave children pointing at nothing?
- Does a cascade delete more than intended — audit trails, billing records,
  historical data that must survive for compliance?
- Is a soft delete respected everywhere, or do some queries ignore the flag and
  resurrect "deleted" rows?

For destructive operations, establish explicitly: soft or hard delete, what
happens to references, whether audit records survive, and whether recovery is
possible at all.

## Migrations

- **Existing rows**: does a new non-nullable column have a safe default, or will
  the migration fail on a populated table?
- **Ordering**: can the migration run before the code that needs it, and can the
  old code survive the new schema during a rolling deploy?
- **Reversibility**: is there a down path, and does it lose data?
- **Large tables**: will this lock a table long enough to matter? Adding an
  index, rewriting a table, or backfilling in one statement are the usual
  culprits.
- **Backfill**: if existing rows need values, is that a separate, resumable,
  batched operation — or one `UPDATE` across millions of rows?

## State machines

- Which states are legal?
- Which **transitions** are legal? A status column with no transition guard
  permits every transition, including the nonsensical ones.
- Can the system skip a state — `pending → completed` without `approved`?
- Can the same transition run twice, and does the second run repeat the side
  effects of the first?

Look for the guard. `if status == PENDING` before the write is a guard;
unconditional assignment is not.

## Reporting

Name the failure mode concretely, in terms of the state left behind:

```
🔴 BLOCKER — Partial failure leaves the operation half-applied with no record.

Evidence:  BulkDeleteService::execute() deletes each user in its own implicit
           transaction inside a loop; the exception handler logs and re-raises
           (app/Services/BulkDeleteService.php:28-41).
Risk:      A failure mid-run leaves an arbitrary subset deleted. Neither the API
           response nor any persisted record identifies which succeeded, so the
           operation cannot be safely retried or reconciled.
Confidence: High — verified by reading the loop and the caller.
Recommendation: Wrap in one transaction, or return a per-item result set and
           make the operation idempotent so retry is safe.
```
