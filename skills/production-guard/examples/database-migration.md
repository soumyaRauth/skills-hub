# Example — Database migration

**Risk: High.** Demonstrates existing-data handling, constraints, large-table
behavior, rollback, and deploy ordering.

```
╔══════════════════════════════════════════╗
║       PRODUCTION GUARD REPORT            ║
╚══════════════════════════════════════════╝

CHANGE
Add a non-nullable `region` column to `orders`, backfilled from the shipping
address, with an index for the new regional reporting query.

RISK CLASSIFICATION
High — schema change on a large, actively written table with a data backfill.

VERDICT
🔴 DO NOT SHIP

BLOCKERS  1      HIGH  2      MEDIUM  1      LOW  0

──────────────────────────────────────────

BASELINE
Scope:  targeted — tests/orders/ and migration tests
Result: 61 passed, 0 failed
Note:   The local database has 214 orders. Production row count is unknown from
        this repository; the risks below are sized on the assumption it is
        substantially larger, which the pagination defaults and archival job
        both imply.

──────────────────────────────────────────

FUNCTIONAL VALIDATION     4/4  passed
REGRESSION VALIDATION     6/6  passed
DATA INTEGRITY            3/6  passed
FAILURE SCENARIOS         2/5  validated
PERFORMANCE               1/3  validated

──────────────────────────────────────────

🔴 BLOCKERS

#1 The migration adds a NOT NULL column with no default and backfills in the
   same statement.

   Category:       Data integrity
   Evidence:       2026_08_01_add_region_to_orders.php adds the column with
                   nullable(false) and no default, then issues a single
                   UPDATE orders SET region = ... across the whole table.
                   EXECUTED locally against 214 rows → PASS. That result does
                   not transfer to a large table.
   Risk:           On a populated table the column addition fails outright on
                   engines that require a default, and the single-statement
                   backfill locks the table for the duration of the update.
                   Rolling deploy makes it worse: old application code inserting
                   an order without a region violates the constraint.
   Confidence:     High for the mechanism; the production impact scales with row
                   count, which is unverified.
   Recommendation: Split into three deploys — (1) add the column nullable, (2)
                   backfill in batches and ship the code that always writes it,
                   (3) add the NOT NULL constraint. Standard expand-and-contract.

──────────────────────────────────────────

⚠️ WARNINGS

🟠 HIGH — The index is created without a concurrent strategy.

   Evidence:       $table->index('region') in the same migration.
   Risk:           On PostgreSQL a plain CREATE INDEX takes a write lock for the
                   build duration. On a large orders table that is a write
                   outage, not a slow migration.
   Recommendation: Create the index concurrently in its own migration, outside a
                   transaction.

🟠 HIGH — The down migration drops the column, losing the backfilled data.

   Evidence:       down() calls dropColumn('region').
   Risk:           A rollback after the backfill discards derived data that took
                   a maintenance window to produce. Re-rolling forward means
                   backfilling again.
   Recommendation: Acceptable only if the backfill is genuinely re-derivable —
                   it is here, from the address — but say so in the migration and
                   confirm the address data has not itself changed.

🟡 MEDIUM — Orders with no shipping address get an empty string, not a real
   region.

   Evidence:       The backfill uses COALESCE(address.region, '') (migration
                   line 24). 11 of 214 local orders have no address.
   Risk:           The reporting query groups by region, so those orders form a
                   silent empty-string bucket rather than surfacing as unknown.
   Recommendation: Use an explicit 'unknown' sentinel, or keep the column
                   nullable and handle it in the query.

──────────────────────────────────────────

TESTS EXECUTED

  php artisan migrate --pretend             →  statements printed and reviewed
  php artisan migrate (local, 214 rows)     →  PASS (0.4s)
  php artisan migrate:rollback              →  PASS
  vendor/bin/phpunit tests/Feature/Orders   →  61 passed

──────────────────────────────────────────

UNVERIFIED

- Migration duration and lock behavior at production row counts
- Behavior during a rolling deploy with old and new code running together
- Index build time on the production table
- Whether any replica lag threshold would be exceeded by the backfill

──────────────────────────────────────────

RECOMMENDED ACTIONS

1. Split into expand-and-contract migrations (blocker #1).
2. Build the index concurrently in a separate migration.
3. Batch the backfill and make it resumable.
4. Replace the empty-string fallback with an explicit sentinel.
5. Confirm the production row count before scheduling.

FINAL VERDICT
🔴 DO NOT SHIP — the migration is safe on a development dataset and unsafe on a
production one. The local PASS is evidence about 214 rows, not about the table
this will actually run against.
```
