# Example — API change

**Risk: Medium.** Demonstrates backward compatibility, authorization,
response-contract validation, and existing clients. Ends in CONDITIONAL SHIP —
no blockers, but a real risk being knowingly accepted.

```
╔══════════════════════════════════════════╗
║       PRODUCTION GUARD REPORT            ║
╚══════════════════════════════════════════╝

CHANGE
Add filtering and pagination to GET /api/orders, and include the customer's
email in each order object.

RISK CLASSIFICATION
Medium — changes a response contract consumed by existing clients, and widens
the data returned.

VERDICT
🟠 CONDITIONAL SHIP

BLOCKERS  0      HIGH  1      MEDIUM  2      LOW  1

──────────────────────────────────────────

BASELINE
Scope:  full suite
Result: 312 passed, 2 failed
Pre-existing failures: both in tests/billing/, failing on main before this
                       change. Unrelated.

Current: 317 passed, 2 failed
Interpretation: 5 new tests added and passing; no increase in failures.

──────────────────────────────────────────

FUNCTIONAL VALIDATION     5/5  passed
REGRESSION VALIDATION     8/8  passed
SECURITY                  5/6  passed
DATA INTEGRITY            n/a
FAILURE SCENARIOS         3/4  validated
PERFORMANCE               3/3  passed

──────────────────────────────────────────

⚠️ WARNINGS

🟠 HIGH — Default pagination changes the response shape for existing clients.

   Category:       Regression
   Evidence:       The endpoint previously returned a bare array; it now returns
                   { data: [...], meta: {...} } unconditionally
                   (app/api/orders/route.ts:28). Two in-repo consumers were
                   updated; the mobile client is not in this repository.
   Risk:           Any consumer outside this repository that iterates the
                   response directly breaks immediately on deploy.
   Confidence:     High for the shape change; Low for the existence of external
                   consumers — no client inventory exists here.
   Recommendation: Return the paginated shape only when a page parameter is
                   present, or version the endpoint. If the team accepts the
                   break, record who accepted it and coordinate the mobile
                   release.

🟡 MEDIUM — Customer email is now returned to every caller of the endpoint.

   Category:       Security / data exposure
   Evidence:       The serializer includes customer.email for all roles
                   (OrderResource.ts:19). The endpoint is available to the
                   support role, which previously could not see customer email
                   anywhere in the API.
   Risk:           Widens personal-data access beyond the role that had it. Not
                   rated a blocker: support staff are authenticated internal
                   users, and the data is already visible to them in the admin UI.
   Recommendation: Gate the field on the permission that governs email
                   elsewhere, rather than on endpoint access.

🟡 MEDIUM — The status filter is not validated against the allowed set.

   Evidence:       ?status= is passed through to the query builder without
                   validation (route.ts:34). Parameterized, so not injectable —
                   but an unknown value silently returns an empty list.
   Risk:           A client typo produces "no orders" rather than an error,
                   which reads as data loss to the user.
   Recommendation: Validate against the status enum and return 422 on mismatch.

🔵 LOW — No maximum page size.

   Evidence:       ?per_page= is unbounded (route.ts:31).
   Recommendation: Cap it at a sane maximum.

──────────────────────────────────────────

TESTS EXECUTED

  npm test                                   →  317 passed, 2 failed (pre-existing)
  npm test -- orders                         →  22 passed
  npx tsc --noEmit                           →  PASS
  npm run lint                               →  PASS
  npm run build                              →  PASS

  Query count check (EXECUTED):
  50 orders with customer eager-loaded       →  2 queries (no N+1)

──────────────────────────────────────────

UNVERIFIED

- Mobile client compatibility — client not in this repository
- Behavior against a production-sized orders table — local dataset is ~200 rows

──────────────────────────────────────────

RECOMMENDED ACTIONS

1. Decide the compatibility strategy for the response shape and record the
   decision (HIGH).
2. Gate the email field on the email permission.
3. Validate the status parameter.
4. Cap page size.

FINAL VERDICT
🟠 CONDITIONAL SHIP — no blocking issues, and the change is well covered by
tests. Shipping is acceptable only once the response-shape break is either
mitigated or explicitly accepted and coordinated with the mobile release.
```
