# Behavioral Validation

The behavioral model is the contract you validate against. Without it, "it
works" means "it did something and nothing crashed".

## The contract

For the feature under change, write down:

**Primary behavior** — the sequence a successful operation follows, in product
terms, not implementation terms.

```
FEATURE: Bulk user deletion

Primary behavior:
  1. Admin selects users.
  2. System validates authorization for each target.
  3. System deletes eligible users.
  4. UI reflects the resulting state, including partial results.
```

**Alternate paths** — valid but non-default routes: empty selection, single
item, already-deleted target, mixed eligible/ineligible sets.

**Invalid input** — missing, malformed, out-of-range, wrong type, hostile.

**Authorization** — who may do this, and what happens to everyone else.

**State transitions** — which states are legal, which transitions are legal, and
whether a transition can run twice.

**Side effects** — writes, emails, webhooks, events, queue jobs, cache
invalidation, external calls.

**Invariants** — what must hold no matter which path executes:

```
Important invariants:
  - Billing records remain intact.
  - Audit records remain intact and attributable.
  - Unauthorized users cannot perform deletion.
  - Already-deleted users do not produce inconsistent state.
```

Invariants are where the valuable findings come from. A feature usually works on
its happy path; what breaks is something the author never framed as a promise.

## Deriving it

Read the change, then the surrounding code, then the tests. Existing tests are
the best source of "existing behavior to preserve" — a test asserts a promise
someone made deliberately.

Where the intended behavior is genuinely ambiguous, do not guess it into the
contract. Put it in `OPEN QUESTIONS` and validate everything else.

## The regression matrix

The regression surface is the set of behaviors that existed before the change
and must still hold after it. Build it from: existing tests, existing API
consumers, shared components, permissions, jobs, reports, exports, and
integrations touching the same entities.

```
BEHAVIOR                          STATUS      EVIDENCE
──────────────────────────────────────────────────────────────────────
Individual deletion still works   PASS        tests/users/delete_test.py (executed)
Admin authorization enforced      PASS        tests/users/authz_test.py (executed)
Audit record written per deletion FAIL        no audit call in bulk path (analyzed)
Billing records preserved         PASS        no cascade on billing_accounts (analyzed)
Retry produces no duplicates      WARNING     no idempotency key (analyzed)
```

Rules:

- A row is `PASS` only with evidence. "It probably still works" is not a row.
- Mark whether the evidence is executed or analyzed. Both are legitimate; only
  conflating them is not.
- A behavior you could not evaluate is `UNVERIFIED`, never quietly omitted.

## Validating without a test suite

Plenty of real repositories have thin coverage. When you cannot execute:

1. Trace the code path by reading it, and say so.
2. Compare against the contract point by point.
3. Report each conclusion as `ANALYZED`.
4. Recommend the specific test that would convert the most important
   `UNVERIFIED` row into an executed one.

A report that says "these four behaviors are unverified because the project has
no tests covering them, and here is the smallest test that would cover the
riskiest one" is far more useful than a confident-sounding claim with nothing
behind it.
