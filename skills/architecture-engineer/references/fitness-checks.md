# Fitness checks

Verifying that the architecture which was decided is the architecture that
exists — and keeping it that way without building a cage nobody wants to live
in.

## Why assertion is not enough

The failure this prevents is small and common: a migration step edits the files
it intended to edit, the tests pass, and the report says the boundary now holds.
Nobody checked whether anything else still crosses it. Six weeks later a new
call site appears and the boundary was never real.

```
Asserted    "OrderService now owns order-status writes"
Checked     grep -rn "order_status" --include=*.php app/ | grep -v OrderService
            → 0 results, and an import rule that fails CI if one returns
```

## What is checkable

Structure is checkable. Behavior is not this skill's claim.

| Property | How | Cost |
| --- | --- | --- |
| Dependency direction | Import linter rule, dependency-cruiser, ArchUnit-style test | Low, and it holds forever |
| Module boundary | Forbid imports past a module's public entry point | Low |
| Cycles | Most dependency tools detect them | Low |
| Single writer for a table | A search that runs in CI, or a database grant | Low to medium |
| Deploy-unit independence | Build each unit in isolation in CI | Medium |
| Contract conformance | Validate handler output against the published schema | Medium |
| No external call in a transaction | Usually a review question, sometimes a lint rule | Varies |

What is not checkable this way: whether the architecture was a good idea,
whether the boundary is in the right place, and whether the feature still works.
The last of those belongs to `proof-driven-dev`.

## Add a check only where a violation matters

A check has to earn its permanence. Every one of them will eventually fail at an
inconvenient moment, and the question is whether that interruption was worth it.

```
Worth a check     the domain layer must not import infrastructure — the whole
                  point of the decision, and one import undoes it
Worth a check     nothing outside billing may import billing/internal
Not worth it      every file must be under 300 lines
Not worth it      every module must have a README
Not worth it      layering rules invented during the review that no decision
                  actually required
```

The test for a proposed check: **name the decision it protects.** A check that
protects no recorded decision is a preference, and preferences enforced in CI
are how teams learn to disable checks.

## Brittle checks are worse than none

A check that fails for reasons unrelated to what it protects trains everyone to
ignore or bypass it — and then the real violation passes too.

```
Brittle    asserting an exact list of files in a module
Durable    asserting no import crosses from domain to infrastructure

Brittle    a snapshot of the dependency graph
Durable    a rule that the graph is acyclic

Brittle    counting classes per package
Durable    forbidding a specific known-bad edge
```

Prefer rules stated as **forbidden edges** over rules stated as required shapes.
Forbidden edges stay true as the system grows; required shapes do not.

## Where the rules live

Use the ecosystem's own tooling rather than introducing a framework:

```
JS / TS     eslint-plugin-import (no-restricted-paths), dependency-cruiser,
            madge for cycles
PHP         deptrac, phparkitect
Python      import-linter
Java / C#   ArchUnit, NetArchTest
Go          the compiler already forbids import cycles; internal/ enforces
            package boundaries natively
Any         a grep-based check in CI — unglamorous, and it works
```

Adding a dependency to enforce architecture is itself an architecture decision,
and it goes through the normal ladder:

```
HANDOFF → dependency-guard: enforcing the domain boundary would add
          dependency-cruiser to the build
```

## Reporting a verification

State what was checked, what passed, and — most importantly — what was not
checked:

```markdown
**Verified against D-006 (OrderService owns order-status writes)**

✓ No write to order_status outside OrderService
  grep across app/, 0 results outside the service
✓ Import rule added, and it fails on a deliberate violation
  .eslintrc no-restricted-paths — confirmed by introducing one and reverting
✓ Suite 214/214, including the new 15-minute boundary test

✗ Not verified: the reporting module still reads the column directly. That is
  transition 2 and the rule deliberately allows reads today.
? Not checkable here: whether any external consumer writes the column. Nothing
  in this repository can establish that.
```

The last two lines are the ones that make the first three trustworthy. A
verification with no gaps stated is a verification nobody audited.

## Drift

Architecture does not stay where it was put. Between sessions, the useful check
is the difference between `target.md` and what is now true:

```
Decided     domain must not import infrastructure
Actual      src/domain/pricing.ts imports the Stripe client (added 2026-09-14)
Impact      pricing can no longer be tested without network stubs, and the
            provider is now a domain concept
Options     inject the port, or accept the coupling and record it
```

Drift is reported as a finding with evidence like any other, and it has the same
bar: name what it costs. A deviation nobody is paying for is recorded in
`risks.md`, not raised.

When a decision has genuinely been outgrown, the honest response is to supersede
it rather than to enforce it — the record exists to explain the system, not to
freeze it.
