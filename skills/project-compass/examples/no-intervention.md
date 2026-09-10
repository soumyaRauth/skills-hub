# Example — Mode A, five times

Every other example in this directory shows the skill saying something. This one
shows it not saying anything, which is what it does almost all of the time and
the only reason the other examples are worth reading.

If this behavior is not solid, nothing else matters: an agent that comments on
project direction four times a week gets uninstalled before it ever makes the
observation that would have been worth a month.

Mode A is not the absence of the skill. The project model was read, the
trajectory was updated, the pattern counters moved, and the guidance that
follows from all of it was *build exactly this*. The sophistication is spent on
getting the work right, not on proving it happened.

---

## Setup

This is not a clean project. `.project-compass/blind-spots.md` has a real,
unresolved entry in it:

```markdown
## Adjustment lifecycle is undefined
Observed  approval, audit and reporting each define "approved" differently
          (src/api/adjustments.ts:88, src/audit/record.ts:31, src/reports/sum.ts:57)
Costs     the bulk-approve request will need a fourth definition
Closes    list the states, the legal transitions, and who may cause each
Raised    2026-09-02 — user acknowledged, deferred until after the release
```

It was raised. It was deferred. It is real, and it is closed.

---

## Five requests, five silences

**Request:** *"Rename `adj` to `adjustment` in the reconciliation module."*

```
Concept    none — no behavior changes
Trajectory not recorded (renames are on the skip list)
Pattern    none
Output     the rename
```

Not: "while we are in here, the lifecycle…". Not: "this is a good moment to…".
The user is doing housekeeping and asked for exactly one thing.

---

**Request:** *"The date on the adjustment row should be the approval date, not
the created date."*

This one *touches* the deferred blind spot — approval semantics are exactly what
is undefined. It still gets nothing, for three reasons: the observation has
already been raised and deferred, the fix is local and correct either way, and
the interruption budget was spent on 2026-09-02 and never refunded.

```
Trajectory recorded — a display rule changed, tagged `adjustment`
           pattern: approval-semantics (4th)
Output     the change
```

The pattern counter goes up. Nobody hears about it. That is the mechanism
working: the count survives, so if the deferral is ever revisited the evidence
is *stronger*, not re-derived.

---

**Request:** *"Add a loading spinner to the export button."*

```
Concept    UI feedback
Trajectory not recorded — no capability, rule or state changed
Output     the spinner
```

The export button belongs to a screen that has accumulated six controls. The
accumulation pattern is real and recorded. A spinner is still a spinner.

---

**Request:** *"Bump the postgres client to 8.13 and fix whatever breaks."*

```
Trajectory not recorded — dependency bump
Output     the bump, and the fixes
```

Even if it breaks four call sites and reveals that connection handling is
duplicated in three places. That is a finding for `trajectory.md`, at most, and
only if it is the third one.

---

**Request:** *"I want to try rebuilding the variance calculation three
different ways to see which reads better. Throwaway — don't worry about it
fitting the rest of the code."*

The user has just declared the frame. That settles it.

```
State      EXPLORATORY for the variance calculation, recorded with the date
Output     help with all three. Make the comparison sharper if asked —
           same input, same measure — and say nothing about structure
```

Not: "these three approaches duplicate the reconciliation logic". Not: "worth
deciding which one before going further". They said throwaway; the entire point
of the exercise is to write code that will be deleted. Gap detection is off in
that area until they say otherwise.

The one thing that would still be said, later and once: if the third attempt
starts acquiring features rather than being replaced, the spike has quietly
become the implementation, and it was built to be discarded.

---

## What was suppressed, and by which rule

| Temptation | Rule |
| --- | --- |
| Mention the lifecycle gap on the date fix | Dismissal is permanent — raised and deferred on 09-02 |
| Mention the six controls on the spinner request | Recurrence without consequence; nothing is blocked |
| Note the duplicated connection handling | Two instances. The bar is three |
| Ask what the export is for | Already asked, already answered |
| Summarize the project state at session start | Nobody asked |
| Comment on the three parallel variance implementations | The user declared it exploratory. Their word settles it |
| Say "no concerns with this change" | That is still commentary. Silence is silence |
| Open with "this fits the current direction" | Nobody asked. Mode A is the work, not a verdict on the work |

The last two rows are the subtle ones. *"This looks fine from a project
perspective"* is not neutral — it is an announcement that a project perspective
was consulted, and four of those a day is the same annoyance in a friendlier
costume. Mode A means the work arrives and the model stays invisible.

---

## Underneath

The state was still read. The trajectory was still updated twice. The pattern
counters still moved. The project model is one session more accurate than it was
this morning.

The user saw a rename, a date fix, a spinner, a dependency bump, and help with
three throwaway experiments.

That is the deal: the work is quiet, and the credit is spent later, once, on
something worth their attention.
