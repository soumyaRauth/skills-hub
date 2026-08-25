# Proof Strategies

A proof plan answers one question per requirement: **what evidence would make
this true, and what is the cheapest mechanism that produces it?**

Tests are the most common mechanism. They are not the only one, and reaching for
a test when a type or a constraint would settle it is wasted work.

## Mechanisms

| Mechanism | Proves | Cost | Good for |
| --- | --- | --- | --- |
| Typecheck | Shapes, signatures, exhaustiveness | very low | Refactors, renames, API shape |
| Lint | Conventions, some correctness rules | very low | Everything, as a gate |
| Build | It compiles and bundles | low | Everything, as a gate |
| Unit test | One function's behavior | low | Pure logic, validators, calculations |
| Integration test | Components together, real database or a close double | medium | Most feature requirements |
| API test | The contract as a client sees it | medium | Status codes, payload shape, auth |
| Database inspection | What was actually written | low | Migrations, side effects, "and nothing else" |
| Runtime probe | Real behavior at a real endpoint | medium | Wiring, config, boot-time failures |
| E2E / browser | The user's path, in a browser | high | Critical flows, UI state |
| Screenshot | Visible rendering | medium | Layout and visual regression — *evidence*, not a verdict |
| Benchmark | A measured difference against a recorded baseline | medium | Performance requirements |
| Existing suite | Nothing else broke | varies | Regression |

## Choosing per requirement

Ask, in order:

1. Could a type or a database constraint make this unfalsifiable? Prefer that —
   it is cheaper than a test and it cannot rot.
2. Does a test that already exists cover it? Run it. Do not write a second one.
3. What is the smallest new check that would fail if the requirement were false?
   That is the proof. A test that passes whether or not the code works is not
   evidence — it is decoration.
4. Can no mechanism here settle it? Say so now, and mark it Level D.

## Use the project's own infrastructure

Find and use what exists: the test framework, the runner command, fixtures,
factories, helpers, the database setup, the CI configuration. New tests match
the conventions of the files beside them.

Introducing a second test framework because the first is unfamiliar is a defect,
not a proof. If a project has no test infrastructure at all, say so, and pick
the lightest mechanism that still produces evidence — a runnable script, a
runtime probe, a database check — rather than installing a stack the developer
did not ask for.

## Staged verification

```
Stage 1   typecheck · lint · build
Stage 2   targeted tests for this contract
Stage 3   integration · API · database
Stage 4   E2E · browser · full regression suite
```

Run Stage 1 first because it is seconds and it catches the common case. Escalate
when risk requires it, when the change is broad, or when a cheaper stage
surfaced something. On a `low` risk change, Stage 4 is usually waste; on a
`critical` one, skipping it needs a stated reason.

## Performance requirements

Never state a performance improvement you did not measure.

```
1. Establish a baseline before the change, with the command and the number.
2. Change the code.
3. Measure again — same command, same conditions, same data.
4. Report both, and the delta.
```

```
PERF-001  Dashboard first paint
  Command   npm run bench:dashboard
  Before    p50 4.21s  (10 runs, seeded fixture, local)
  After     p50 1.87s  (10 runs, same fixture)
  Status    PASS · Level A
  Note      local measurement; production hardware and data volume differ
```

When a reliable measurement is not available here, the requirement is Level C.
Say what was done and what could not be shown:

> The N+1 was removed — query count for the dashboard load dropped from 143 to
> 4, verified by the query log. End-to-end latency was not measured: this
> environment has neither production data volume nor comparable hardware.

Query counts, allocation counts, and payload sizes are often measurable when
wall-clock time is not — and they are better evidence than a noisy timing.

## Security requirements

Positive cases prove the feature exists. Negative cases prove it is a boundary.
A security requirement without a negative case is untested.

For every permitted action, write the requirement for the same action performed
by: an unauthenticated caller, an authenticated caller without the permission, a
caller from another tenant or organization, and the resource's own edge cases —
expired credentials, replayed tokens, tampered identifiers, direct object
references.

Report as *the tested properties held* — never as *secure*. See
`risk-model.md` for the checklist by change type.

## Refactoring requirements

The objective of a refactor is that **nothing observable changes**. That makes
the contract unusual and the proof strong:

- Existing tests pass **unchanged**. A test edited to accommodate a refactor is
  a behavior change until proven otherwise — call it out.
- Public API surface is identical: signatures, exports, routes, payload shape.
- Typecheck and build pass.
- Where behavior is not covered by tests, characterize it *before* the change
  (record real output), then compare after.

The dangerous refactor is the one over untested code. There, the honest contract
includes a requirement that says so, and the first work is characterization —
capture current behavior as tests, then refactor against them.

## Evidence that is not proof

- Reading the code and concluding it looks right.
- A test asserting the function was called, when the requirement is what it did.
- A passing test whose assertion cannot fail (`expect(true).toBe(true)`,
  a mock returning the value under test).
- A snapshot updated in the same run that changed the behavior.
- A screenshot, offered as proof that a design is good — it is evidence of what
  rendered; the judgment stays human.
