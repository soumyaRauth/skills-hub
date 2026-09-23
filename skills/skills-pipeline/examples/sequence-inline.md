# Example: sequence given with the command, DO NOT SHIP sent back once

**Request:** `/skills-pipeline 6,7,10 cap refunds at the original charge amount`

The sequence comes first, so there is no menu.

```
⚡ Skills Pipeline — Impact → Build → Ship gate
```

**Impact.** The map finds the refund service, the admin refund endpoint, and a
nightly reconciliation job that sums refunds with raw SQL.

**Build.** ProofBuild adds the cap and proves it against the service and the
endpoint. Result: `VERIFIED`.

**Ship gate.** Production Guard returns `DO NOT SHIP`. Partial refunds issued
concurrently can each pass the cap check and together exceed it, because there
is no lock or constraint.

Build is in the sequence, so the failed check goes back to Build once.
ProofBuild adds a row lock and a test that races two partial refunds. Result:
`VERIFIED`. Production Guard runs again and returns `SHIP`.

```
#   Stage       Skill               Status   Result
6   Impact      impact-map          RAN      3 consumers, 1 raw-SQL job
7   Build       proof-driven-dev    RAN      VERIFIED — 5/5
10  Ship gate   production-guard    RAN      DO NOT SHIP — concurrent partial refunds exceed the cap
7   Build       proof-driven-dev    RAN      VERIFIED — 6/6, race covered
10  Ship gate   production-guard    RAN      SHIP
```

If the second verdict had also been `DO NOT SHIP`, the run would have stopped
there and reported. There is no third attempt.
