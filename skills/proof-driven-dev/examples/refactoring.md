# Example — Refactoring

A refactor is the one contract whose objective is that **nothing observable
changes**. That inverts the usual proof: the evidence is not new tests passing,
it is old tests passing *unchanged*.

---

**Developer:**

> Refactor the notification service. It's a mess.

---

## 1. Investigate

```
File          src/notifications/service.ts  — 612 lines, one class, 9 methods
Callers       11 files (git grep NotificationService)
Public API    send(), sendBulk(), schedule(), cancel()  — used across the app
Tests         tests/notifications/service.test.ts — 24 tests
Coverage      the four public methods: covered
              retry/backoff path, template resolution: NOT covered
```

That last line decides the shape of the whole contract. Refactoring covered code
is cheap; refactoring uncovered code without characterizing it first is an
untracked behavior change.

## 2. Contract

Risk: **medium** — no new behavior, but eleven callers and a partly uncovered
surface.

```yaml
objective: "Restructure NotificationService with no observable behavior change"
risk: medium
assumptions:
  - "Public API stays identical — 11 callers, none of which are being edited"
requirements:
  - { id: REFAC-001, priority: critical, description: "Every existing test in tests/notifications/ passes UNCHANGED", proof: { type: regression } }
  - { id: REFAC-002, priority: critical, description: "The public API is byte-identical: send, sendBulk, schedule, cancel — same signatures, same exports", proof: { type: typecheck } }
  - { id: REFAC-003, priority: critical, description: "Uncovered behavior (retry/backoff, template resolution) is characterized by tests BEFORE the refactor, and those tests pass after", proof: { type: unit } }
  - { id: REFAC-004, priority: high,     description: "All 11 call sites typecheck without modification", proof: { type: typecheck } }
  - { id: REFAC-005, priority: high,     description: "The full suite passes", proof: { type: regression } }
  - { id: REFAC-006, priority: normal,   description: "Whether the new structure is actually clearer", proof: { type: manual } }
```

REFAC-006 is Level D from the start. "It's a mess" is a judgment, and so is
whether it stopped being one — the skill can prove the behavior survived, not
that the result is better.

## 3. Characterize first

Before touching anything, capture what the uncovered code actually does — not
what it should do:

```
npm test -- tests/notifications/         24 passed        ← baseline
+ 7 characterization tests for retry/backoff and template resolution
npm test -- tests/notifications/         31 passed        ← new baseline
```

One of the seven records something surprising:

```
test("retries a 500 four times, not three")
  documented: 3 retries
  observed:   4 attempts total (initial + 3) — the log message says "retry 3/3"
              on the fourth call
```

That is not fixed here. A refactor preserves behavior, including behavior that
looks like a bug; the characterization test records it and the report mentions
it once. Changing it would be a different contract.

## 4. Refactor, then verify

```
Stage 1  npm run typecheck            pass — REFAC-002, REFAC-004
         npm run lint                 pass
Stage 2  npm test -- tests/notifications/   31 passed — REFAC-001, REFAC-003
         git diff --stat tests/            0 files changed  ← the key evidence
Stage 3  npm test                     412 passed — REFAC-005
```

`git diff --stat tests/` showing zero changes to the pre-existing tests is what
makes REFAC-001 Level A. A test suite edited during a refactor proves nothing
about whether behavior survived.

```
Public API diff (typecheck-verified):
  send(input: SendInput): Promise<SendResult>          unchanged
  sendBulk(inputs: SendInput[]): Promise<BulkResult>   unchanged
  schedule(input: SendInput, at: Date): Promise<void>  unchanged
  cancel(id: string): Promise<boolean>                 unchanged
```

## 5. What the developer sees

```
⚠ REVIEW REQUIRED

Notification service refactor — behavior preserved

Requirements   5/6 verified
Tests          412/412 (7 characterization tests added first; the 24 existing
               tests pass with zero edits)
API            unchanged — 11 call sites typecheck untouched
Changed        service.ts → 4 files, 612 → 380 lines

For your review:
  Whether the new structure is clearer is your call, not something I can verify.

One thing surfaced, not changed:
  Retry sends 4 attempts, not the documented 3. Pre-existing; now covered by a
  characterization test. Fixing it is a behavior change — separate task?
```

---

## What this example demonstrates

- The objective was *no observable change*, which makes "existing tests pass
  unchanged" the strongest available evidence — and `git diff --stat tests/` the
  proof that they were unchanged.
- Uncovered code was characterized **before** the refactor. Without that step,
  the retry behavior could have changed silently and nothing would have caught it.
- A pre-existing oddity was recorded, reported once, and not fixed. Scope
  discipline in both directions: the refactor did not absorb a bug fix, and the
  bug did not get buried.
- REFAC-006 was Level D from the beginning rather than discovered at the end —
  and its honesty costs nothing, because the other five are Level A.
