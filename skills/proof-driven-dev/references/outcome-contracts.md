# Outcome Contracts

The contract is the artifact that makes everything else possible. Without it
there is no definition of success, so "verified" would mean whatever the
implementation happens to do.

## What a contract is

Three parts:

- **Objective** — one sentence describing the outcome from outside the code.
- **Requirements** — numbered, individually observable statements that together
  mean the objective happened.
- **Proof** — for each requirement, the mechanism that will establish it.

The contract is written **before** the implementation, and it is the thing the
implementation is built to satisfy. Writing it afterward turns it into a
description of the code, which proves nothing.

## Writing an observable requirement

A requirement is observable when someone outside the codebase could tell whether
it holds. That is the whole test.

| Not observable | Observable |
| --- | --- |
| "Token handling is secure" | "A reset token rejected after its first successful use" |
| "The service is refactored cleanly" | "Every existing test in `tests/billing/` still passes unchanged" |
| "Upload is fast" | "A 50 MB upload completes without the request timing out at 30s" |
| "Errors are handled" | "An upload of an unsupported type returns 415 and stores nothing" |

Rules:

- One behavior per requirement. "Token expires and cannot be reused" is two.
- Stated as the observable outcome, never as the implementation. "Uses a UUID
  token" is a design choice; "a token from another user's request is rejected"
  is a requirement.
- Include the negatives. Most real defects live in what should *not* happen.
- Include the survivors — existing behavior that must still work.
- Priority is `critical`, `high`, or `normal`, and it decides what a failure
  means: a failed `critical` requirement is `✗ BLOCKED`, never a footnote.

## Requirement ids

`AREA-NNN` — a short uppercase area prefix and a sequence: `AUTH-001`,
`UPLOAD-004`, `CHECKOUT-002`, `PERF-001`. Ids are stable for the life of the
task: evidence files, repair attempts, and the final report all key off them.
Never renumber a requirement mid-run; if one is dropped, mark it `withdrawn`
with a reason and leave the id retired.

## Deriving the requirements the developer did not state

The request names the happy path. The contract has to name the rest. For each
stated requirement, ask:

- What is the negative case? (wrong user, wrong state, expired, malformed)
- What is the boundary? (empty, one, many, maximum, over the maximum)
- What already works here that this could break?
- What is the failure path, and what does the user see when it happens?
- What must be true afterward in storage — rows written, rows *not* written?

For "add password reset", none of AUTH-003 through AUTH-008 below were in the
request, and every one of them is where the bugs are:

```yaml
objective: "Users can securely reset their password by email"
risk: high
assumptions:
  - "Reset links expire in 1 hour — matches the existing invite-token TTL in
     src/auth/invites.ts:22"
requirements:
  - id: AUTH-001
    description: "A user can request a password reset for their email address"
    priority: critical
    proof: { type: integration, note: "POST /auth/reset returns 202" }

  - id: AUTH-002
    description: "A valid request produces a single-use token bound to that user"
    priority: critical
    proof: { type: integration }

  - id: AUTH-003
    description: "An unknown email returns the same response as a known one"
    priority: critical
    proof: { type: security, note: "no account enumeration via status or timing" }

  - id: AUTH-004
    description: "A token past its expiry is rejected"
    priority: critical
    proof: { type: security }

  - id: AUTH-005
    description: "A token already used once is rejected on reuse"
    priority: critical
    proof: { type: security }

  - id: AUTH-006
    description: "After reset, the new password authenticates"
    priority: critical
    proof: { type: integration }

  - id: AUTH-007
    description: "After reset, the old password no longer authenticates"
    priority: critical
    proof: { type: integration }

  - id: AUTH-008
    description: "Existing email/password login is unchanged"
    priority: high
    proof: { type: regression, note: "existing tests/auth/login.test.ts" }
```

## Assumptions

Every ambiguity resolved by a safe default becomes an `assumptions` entry with
the evidence that made it safe — usually a file and line showing the convention
already in use. Assumptions are cheap to read and let the developer correct one
in a sentence. Silent defaults do not.

## When to persist, when to keep it inline

| Situation | Contract |
| --- | --- |
| Typo, copy change, one-line fix | Inline, one or two requirements, no files written |
| Ordinary feature or bug fix | Inline for the response; persist if the work spans sessions |
| Multi-file feature, migration, anything high or critical risk | `.proofbuild/contract.yml` |
| Work that will be handed to another session or another agent | `.proofbuild/`, always |

Persisting a contract for a typo is bureaucracy. Skipping one for a payments
change is how "it's implemented" gets mistaken for "it works".

## Amending a contract

Contracts change when investigation proves a requirement wrong or incomplete.
That is legitimate — with two conditions: the amendment is explicit, and it is
visible in the result. Move the superseded version to `.proofbuild/history/` and
state the change in one line:

```
CONTRACT AMENDED
AUTH-004  expiry 24h → 1h  (matches existing invite TTL; 24h was assumed, not sourced)
```

What is never legitimate is quietly relaxing a requirement so the run can be
called verified. That is the one failure mode that makes every other output of
this skill worthless.
