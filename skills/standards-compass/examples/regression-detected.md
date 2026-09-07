# Regression — a control that used to hold

**Context:** a security focus ran in September. Authorization passed after three
findings were fixed and negative tests were added. It is now late October and
the team asks for a re-check before a release.

The value here is entirely in the recorded baseline. Nobody finds this by
reading a diff, because the change that caused it looks correct in isolation.

---

## What state held

```yaml
# .project-standards/findings.md (extract)
STD-003  authorization  FIXED 2026-09-19  VERIFIED 2026-09-19
         all 14 admin routes route through requireRole()
         evidence: tests/authz/admin-routes.test.ts — 14 negative tests
```

## Response

```markdown
## Re-check against the 2026-09-19 baseline

Improved     2 findings resolved since September (session expiry, log redaction)
New          3 — all in the new billing module
Regressed    1 — below
Unchanged    6 unable-to-verify items; still no infrastructure evidence in-repo

---

### REGRESSION — authorization

Previously   PASS (2026-09-19) — 14 of 14 admin routes behind requireRole(),
             with a negative test per route
Currently    FAIL — 2 of 17 admin routes authenticate only
Severity     HIGH · Confidence HIGH · Gap type: implementation

Evidence
  src/api/admin/reports.ts:12      requireAuth() only
  src/api/admin/reconcile.ts:9     requireAuth() only
  tests/authz/admin-routes.test.ts still asserts 14 routes; the two new ones
                                   were never added to the list

Cause
  Both routes were added on 2026-10-02 as part of the billing module. They
  follow the pattern of the file they were copied from — src/api/billing/
  summary.ts, which is a member-accessible route — rather than the admin
  pattern.

Why it matters more than a new finding
  This is the third time authorization has been the finding. The fix in
  September worked; what didn't hold is the mechanism that keeps it fixed.
  The test file enumerates routes by hand, so a new route is invisible to it
  by default.

Fix
  Route both handlers through requireRole('admin'), and change the test to
  enumerate the admin route directory rather than a hand-written list, so the
  next new route is covered without anyone remembering.

Verify
  The rewritten test should fail before the two handlers are fixed. If it
  passes immediately, the enumeration isn't finding them.
```

---

## What makes this a regression rather than a finding

| | |
| --- | --- |
| A recorded state exists | `PASS` on 2026-09-19, with the evidence that established it |
| The same control is now not passing | Same control id, same evidence file, different result |
| The cause is identifiable | A commit, a date, and a pattern that was copied |
| The remediation addresses the mechanism | Not just the two routes — the check that would have caught them |

The last row is the one that matters. Fixing the two routes returns the project
to September. Fixing the test returns it to September *and* stops the fourth
occurrence.

## What was not done

- No re-audit of the whole repository. Two areas changed; those were assessed.
- No re-derivation of the profile or the applicability set — both were read from
  state and spot-checked against the code.
- No new finding id. `STD-003` reopened, so the history shows this has now
  happened twice, which is a more useful fact than two unrelated entries.
