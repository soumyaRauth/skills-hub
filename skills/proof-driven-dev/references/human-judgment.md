# Human Judgment

Some requirements cannot be settled by any check available here. Naming them
honestly is what keeps every other "verified" worth reading.

## Proof levels

| Level | Meaning | Example |
| --- | --- | --- |
| **A — Deterministically verified** | An executed check directly demonstrates the requirement | A test asserts the reused token is rejected; it passes |
| **B — Strongly verified** | Several independent checks support it, none contradicts, but no single check demonstrates it end to end | Typecheck, unit tests, and an API probe together show the payload shape changed everywhere |
| **C — Partially verified** | Part is proven; part is unreachable in this environment | The query count dropped from 143 to 4 (measured), but production-scale latency was not measured |
| **D — Human judgment required** | No available mechanism can settle it | "The interface should feel premium" |

Level is a property of the *evidence*, not of confidence. Believing strongly
that something works does not make it Level B.

## Level D is a real answer

"Make the dashboard feel premium", "improve the UX", "make the copy friendlier",
"is this architecture right" — these are legitimate requirements and no test
resolves them.

Decompose them. Most of a subjective request has an objective skeleton:

```
"Make the settings page feel premium"

  ✓ Level A   Every control is reachable by keyboard
  ✓ Level A   Contrast meets WCAG AA on all text  (axe: 0 violations)
  ✓ Level A   Layout holds at 320px, 768px, 1440px  (screenshots attached)
  ✓ Level A   No layout shift on load  (CLS 0.00)
  ✓ Level B   Interaction states exist for every control: hover, focus,
              active, disabled, loading
  ⚠ Level D   Whether the result reads as "premium"
```

Six of seven become evidence. The seventh stays with the person who asked, and
saying so costs nothing — while claiming it costs the credibility of the other
six.

## Surfacing a judgment call

Small, specific, and never buried in prose:

```
⚠ REVIEW REQUIRED

Settings redesign · 12/12 functional requirements verified

One requirement needs your eye:
  "The page should feel premium" — accessibility, responsive behavior, and
  interaction states are verified; visual quality is not something I can
  establish.

  Screenshots: .proofbuild/evidence/UI-007/{320,768,1440}.png
```

Attach the artifacts that make the judgment cheap — screenshots, before/after
pairs, the rendered output. Do not attach an argument for why it looks good.

## Decisions versus judgments

Two different asks, and they should not be confused:

- A **judgment** is *does this meet the bar?* — you did the work, they assess it.
- A **decision** is *which behavior do you want?* — no work is right until they
  choose.

A decision blocks; a judgment does not. Present a decision as options:

```
Decision required:
A duplicate filename inside one upload batch —

  [overwrite]   [reject the duplicate]   [keep both, suffix the name]
```

Present a judgment as a finished thing to look at.

## Batch them

If a run produces three judgment calls and a decision, ask once:

```
⚠ REVIEW REQUIRED

Bulk upload · 14/16 requirements verified

Decision required:
  Duplicate filename in a batch —  [overwrite]  [reject]  [suffix]

For your review (not blocking):
  UI-003  Progress indicator styling — screenshot in .proofbuild/evidence/
  PERF-002  Batch of 500 files takes 41s locally; production timing unknown
```

Four interruptions for one task is a worse experience than a slightly longer
message. One message, decisions first, judgments after.

## Never fake Level A

The temptation is a test that technically passes and does not demonstrate the
requirement — asserting a function was called, snapshotting whatever rendered,
checking a 200 when the requirement is about the payload.

That is worse than reporting Level D, because it converts an honest gap into a
false claim, and the developer stops checking. When no mechanism exists, the
answer is:

```
AUTH-009  Level D — human judgment required
  No mechanism available here demonstrates this. What was verified instead:
  <the adjacent objective facts>. What remains for you: <the specific judgment>.
```
