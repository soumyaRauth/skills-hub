# Failure Analysis

A failing check is information, not an instruction to edit code. Classify first;
the classification decides whether code should change at all — and which code.

## Classifications

### `IMPLEMENTATION_ERROR`

The code does not do what the requirement says. The ordinary case, and the only
one where the answer is "fix the implementation."

### `TEST_ERROR`

The check is wrong: bad fixture, wrong assertion, wrong setup, a mock that does
not match the real interface, a test asserting yesterday's behavior.

Fix the test and say what was wrong with it. The trap here is enormous — a test
that fails because the implementation is broken looks exactly like a test that
is wrong, and "fixing" it converts a caught defect into a shipped one. Before
classifying `TEST_ERROR`, state what evidence shows the *behavior* is correct.

### `CONTRACT_ERROR`

The requirement was wrong — it described behavior the product should not have,
or it contradicts another requirement, or investigation proved its premise
false. Amend the contract explicitly and visibly.

### `ENVIRONMENT_ERROR`

The failure is about this machine, not this change: missing dependency,
unavailable service, absent credential, no network, wrong runtime version, a
sandbox restriction.

```
FAIL  npm test -- upload.integration.test.ts
      Error: connect ECONNREFUSED 127.0.0.1:5432

Classification: ENVIRONMENT_ERROR
  No database is running. Nothing in this change touches connection setup.
  UPLOAD-003 and UPLOAD-004 cannot be verified here.
```

Do not repair the code. Do not start a database in someone's environment
uninvited. Report the requirement as blocked with the reason.

### `EXISTING_REGRESSION`

The check was already failing before this change. Proving that requires having
established a baseline — which is why the baseline is worth the minute it costs.

If no baseline was captured, `git stash` is *not* the way to find out; that
touches the developer's working tree. Read history instead — recent CI results,
the test's last modification, whether the failure references code the change
never touched — and if it stays unclear, say `UNDETERMINED` rather than guessing
in whichever direction is convenient.

### `UNRELATED_FAILURE`

A failure in an area with no relationship to the change, appearing in the same
run. Flaky tests, timing, a snapshot in another module, a network-dependent
test. Report it in one line; do not absorb it into scope; do not silently
re-run until it passes.

### `UNKNOWN`

Not yet classified. A legitimate temporary state and never a final one — repair
never begins from `UNKNOWN`, because every fix applied to a failure you cannot
name is a guess with side effects.

## The diagnostic sequence

1. **Read the actual output.** Full error, stack trace, the assertion's expected
   and received. Not the summary line.
2. **Reproduce narrowly.** Run the single failing test, not the suite.
3. **Locate the boundary.** Does the failure come from code this change touched?
   `git diff` answers this in seconds.
4. **Check the baseline.** Was this failing before?
5. **Form one hypothesis**, stated in a sentence: *what* is wrong and *why* it
   produces *this* output. A hypothesis that does not explain the specific
   output is not a hypothesis.
6. **Verify the hypothesis before fixing it** — a log line, a probe, a smaller
   test. Fixing an unverified hypothesis is how repair loops spiral.

## Cascades

One cause, many red checks. Fix the cause once and re-run everything before
concluding anything about the others; repairing each downstream failure
separately produces a large diff, a slow loop, and new bugs.

Signals of a cascade: many failures appearing together after one edit; failures
across unrelated modules; the same error text in every failure; a failing import,
config load, or migration at setup.

## Reporting failure

The developer needs the diagnosis, not the transcript:

```
✗ BLOCKED

Checkout · 11/12 requirements verified

CHECKOUT-009  Session expires after 30 minutes
  Observed   expires after 30 minutes of wall-clock time, not idle time —
             an active user is signed out mid-checkout
  Cause      expiry is computed from session.createdAt; no activity timestamp
             exists on the session record
  Attempts   3 — refreshing on request, sliding expiry, a lastSeenAt column
  Blocker    adding lastSeenAt changes the session schema, which is shared with
             the mobile client's token contract

Decision required: extend the session record, or scope expiry to web only?
```

What that gives: the failing requirement, what actually happens, why, what was
tried, and the specific decision that is wanted. What it leaves out: every file
touched along the way.
