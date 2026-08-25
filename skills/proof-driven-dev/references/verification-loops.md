# Verification Loops

Implementation is one step of a loop, not the end of the work.

```
        ┌────────────────────────────────────────────┐
        │                                            │
   CONTRACT → IMPLEMENT → VERIFY → failed? ──yes──> CLASSIFY → REPAIR
                              │                        │
                              no                   budget spent?
                              │                        │
                              ▼                       yes
                          STATUS ◄──────────────── ✗ BLOCKED
```

The loop's job is to reach a *defensible* status, not a green one.

## Running verification

Per requirement, in the order the proof plan set:

1. Run the planned check. Capture the exact command and its real output.
2. Compare against the requirement's expectation — the one written before the
   implementation, not one adjusted to match what happened.
3. Record `PASS`, `FAIL`, `BLOCKED`, or `HUMAN` with a proof level.
4. Move on. Do not repair mid-sweep — a full picture of what failed is worth
   more than an early fix, because failures cluster and one cause often explains
   several.

Then run the regression checks the contract named, and only then start repair.

## Contradiction detection

The highest-value check in the loop: compare what you believe against what
actually happened.

> Reasoning: "the token is invalidated after first use — `used_at` is set in
> `consumeToken()`."
> Observed: the same token reset the password twice, both returning 200.

```
✗ CONTRADICTION — AUTH-005
  Expected  second use rejected
  Observed  second use returned 200 and changed the password
  Cause     consumeToken() writes used_at after the response is sent; the
            guard reads a value that is not there yet
```

Evidence wins. Always. The failure mode this prevents is the most damaging one
an AI agent has: a confident, articulate, wrong claim of success.

Look for contradictions in three places specifically: a test that passes for a
different reason than the one you assumed; a check that never ran but was
reported as passing; and a requirement whose evidence actually demonstrates a
neighboring behavior rather than the requirement itself.

## When a check cannot run

Missing service, absent credential, no network, unavailable fixture, a suite too
expensive to run here. That requirement is `BLOCKED`, at Level C or D — never
silently passed, and never counted in a passing total.

```
CHECKOUT-007  BLOCKED · environment
  Needed    Stripe test-mode key (STRIPE_TEST_KEY unset)
  Ran       nothing — the integration test skipped at setup
  Effect    webhook replay behavior is unverified in this environment
```

An unverifiable requirement makes the run `⚠ REVIEW REQUIRED` at best. It never
makes it `✓ VERIFIED`.

## The repair budget

Default **3 attempts per requirement**; 2 at high risk; 1 at critical. The budget
is per requirement, not per run — three attempts at one stubborn test does not
consume the allowance for an unrelated one.

An attempt is spent when a fix is applied and re-verified. Re-running an
unchanged check is not an attempt; neither is fixing something the classification
identified as an environment problem.

Stop early, before the budget is gone, when:

- The same failure recurs after a fix that should have changed it — the model of
  the problem is wrong, and more attempts will produce more wrong fixes.
- Each repair breaks a different requirement. That is a contract or design
  problem, not a bug.
- The fix under consideration would weaken a test or narrow a requirement.
- The change is critical-risk and the first attempt did not settle it.

When the budget is spent, the answer is `✗ BLOCKED` with the diagnosis, the
attempts, and what a human should decide. Not another attempt.

## Repair by classification

| Classification | Repair |
| --- | --- |
| `IMPLEMENTATION_ERROR` | Fix the code. Re-verify the requirement *and* everything that passed before. |
| `TEST_ERROR` | Fix the test; state what was wrong with it. Never delete the assertion. |
| `CONTRACT_ERROR` | Amend the contract explicitly, in the report. Never silently. |
| `ENVIRONMENT_ERROR` | Do not touch the code. Report `BLOCKED` with the missing piece. |
| `EXISTING_REGRESSION` | Report as pre-existing, with the evidence that it predates the change. |
| `UNRELATED_FAILURE` | Report; keep it out of scope. |
| `UNKNOWN` | Investigate until it is one of the above. Do not repair a failure you cannot name. |

## Re-verification

After any repair, re-run the failing check **and** the checks that already
passed in the same area. A repair that fixes AUTH-005 by moving the write
earlier may break AUTH-002. Partial re-verification is how a loop converges on a
report that is green and wrong.

At the end of the last iteration, every requirement's status must come from a
check run against the **final** state of the code. A pass recorded two repairs
ago is stale evidence.

## Convergence

A loop that has run its budget without converging has produced something
valuable: a precise description of what does not work and what was tried. That
is a better outcome than a fourth attempt, and far better than lowering the bar
until the run turns green.
