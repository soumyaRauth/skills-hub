# Remediation

A finding that nobody acts on was not worth writing. The measure of this phase
is whether an engineer can start work from the report without a meeting.

## Prioritized roadmap

Not a dump of findings ordered by severity — a plan with time horizons.

```markdown
## Fix immediately          (critical and high, exploitable now)
1. STD-003  Authorization bypass on 3 admin endpoints        ~2h + tests
2. STD-007  Customer emails written to application logs      ~1h

## Fix before production    (important, not currently exploited)
3. STD-011  Upload path trusts client-supplied filename      ~3h
4. STD-014  No rate limiting on password reset               ~2h

## Improve next             (medium)
5. STD-018  Session lifetime never expires server-side
6. STD-021  No negative authorization tests anywhere

## Track                    (low and informational)
7. STD-025  Dependency 3 majors behind; no known advisory

## Verify externally        (not answerable from the repository)
-  Backups exist and restore has been tested
-  Whether EU users are in scope
-  Screen reader behaviour on the checkout flow
```

The last block is not a to-do list for engineering. Keeping it separate is what
stops it being ignored along with everything else.

## Writing a recommendation

| Bad | Good |
| --- | --- |
| "Improve security" | "Route the three admin handlers through `requireRole('admin')` and add a negative test per endpoint" |
| "Implement proper logging" | "Log authentication failures and admin actions with actor, target and outcome; the logger at `src/lib/log.ts` already supports structured fields" |
| "Ensure GDPR compliance" | "Deleting a user leaves their email on `orders`; decide whether orders are anonymized or retained under a stated legal basis, then implement it in `deleteUser()`" |
| "Add tests" | "Add an integration test asserting a `member` session receives 403 from each admin route" |

Every recommendation: the specific change, where, and how it will be verified.

## Smallest safe change

Prefer the minimal correct fix. Rewrites do not happen, and recommending one
usually means nothing happens at all.

- Use the infrastructure that exists before adding any. If a middleware, a
  policy layer, or a logger is already there, the fix is routing through it.
- Do not introduce a dependency for something the platform or the existing stack
  already does. If a new tool genuinely is the answer, say what it buys and what
  it costs to operate.
- Only recommend architectural change when the current architecture makes the
  requirement unachievable — and say that explicitly, because it is a much
  larger claim.

## `fix` mode

When asked to fix findings, do not start editing.

1. **Summarize the intended changes** — which findings, which files, what
   changes, what could break.
2. **Separate safe from disruptive.** Adding a role check to an endpoint is
   safe. Changing session lifetime, tightening a CSP, or altering deletion
   semantics changes behaviour for real users and needs a decision.
3. **Implement the safe changes**, smallest first.
4. **Add or extend tests** that would fail if the fix regressed. A security fix
   without a test is a fix with a countdown attached.
5. **Run what can be run** and report what it printed.
6. **Reassess the affected controls** against the new code.
7. **Report what changed and what did not**, including anything deliberately
   left for a human decision.

## Verification after a fix

```markdown
STD-003  Administrative endpoints bypass the shared authorization policy

Before   FAIL        3 of 14 admin routes had no role check
After    PASS        all 14 route through requireRole(); src/api/admin/*.ts
Evidence tests/authz/admin-routes.test.ts — 14 negative tests, executed, 14 passed
Residual The tenant scoping fix in exports.ts covers the query path; confirm no
         cached export artifacts from before the fix remain in S3
```

Before, after, evidence, residual. The residual line is the one people skip and
the one that matters six months later.

## What not to fix in code

Process and legal gaps have no code fix, and inventing one is worse than leaving
the gap open because it removes the signal that anything is missing.

```
Finding    No documented incident response procedure
Wrong      Create SECURITY.md and mark the finding resolved
Right      Process gap. A repository cannot establish this. If you want a
           starting point I can draft a procedure for a human to own and
           approve — but the finding closes when the organization adopts one,
           not when a file exists
```

Same for "does GDPR apply", "is the organization ISO 27001 certified", "what is
our PCI scope". Answer the engineering half; route the rest to the person who
can answer it.

## Regression prevention

Every fix to a security or privacy control should leave behind a check that
fails if it comes back — a negative test, a CI rule, a lint rule, a schema
constraint. Findings that keep returning are findings whose fix was never
verified automatically, and the second occurrence is always more expensive than
the test would have been.
