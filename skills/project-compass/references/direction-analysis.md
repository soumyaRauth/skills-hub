# Direction

Two questions live here: *what is this project actually doing?* and *what is it
turning into?* The answers are the input to every recommendation the skill
makes, which is why they get their own file and their own evidence standard.

The crossing itself — a task list becoming a task management system, screens
becoming an administration system — is in `becoming.md`. Choosing what to do
about it is in `next-action.md`. This file is about establishing the direction
honestly in the first place.

## Three directions, and what their disagreement means

Direction is not what the README says the project is for. It is what the work
has actually been doing, which is often different and occasionally more honest.

```
Stated direction      README, docs, roadmap, what the user has said
Actual direction      trajectory entries, recent commits, where churn concentrates
Structural direction  what the schema and the interface are becoming
```

When those three agree, direction is `OBSERVED` and there is nothing to say.
When they disagree, the disagreement is the finding — and it is usually the most
interesting thing in the project.

| Disagreement | What it usually means |
| --- | --- |
| Stated says A, actual does B | Either the goal changed and nobody wrote it down, or the work has quietly gone somewhere else. **Ask, do not diagnose** |
| Actual says A, structure says B | The schema is ahead of the feature work — often the truest signal of what is being built |
| Stated and actual agree, structure lags | Normal. The model catches up when it has to |
| All three disagree | `FORMING`, a rewrite in progress, or a project that has changed hands |

The first row is worth one question and never a verdict: *"we started on X and
the last eight changes are mostly Y — did the goal change, or did we end up
here?"* Both answers are fine, and either one belongs in `decisions.md`.

## Writing it down

```markdown
### Direction

**Appears to be:** formalizing inventory adjustments — approval, audit,
reconciliation reporting.

**Evidence:** eleven of the last fourteen trajectory entries; the three newest
tables are all adjustment-related; the README still describes a stock-count tool.

**Confidence:** High for the direction, Low for whether it is deliberate.

**Biggest gap:** the adjustment flow now has approval, audit and reporting and
no defined lifecycle. Each of those three features invented its own idea of what
"approved" means.

**Next step:** list the states and the legal transitions before the fourth
feature reads `approved_at`.
```

Always separate *where it is going* from *whether that is intended*. The first
is evidence. The second is only ever the user's to state.

## `direction.md`

The persisted form of the above, and the file that makes *"what should I do
next?"* answerable without re-deriving a project every time. It is **rewritten,
not appended to** — it is a view of the present, and an out-of-date direction is
worse than none.

```markdown
# Direction

**Appears to be**    [what the software currently is]
**Becoming**         [the crossing, with a label and confidence]
**Key workflow**     [the path that has to work, and where it currently breaks]
**Biggest gap**      [the decision, model or measurement that work depends on]
**Next step**        [the concrete action]
**Why**              [the consequence it prevents, in terms of real work]
**Confidence**       High / Medium / Low, and for which part
**Evidence**         [locations and dates]
**Verified**         [date]
```

Update it when the direction moves, when the gap closes, when a milestone lands,
or when the recorded next step has been done. Not per request — a `direction.md`
that changes daily is a diary with a better name.

Two lines are worth adding when they apply:

```
**Not yet said**   nothing is blocked; raise at the next control request
**Stated goal**    user said 2026-09-04 this is a throwaway prototype
```

The first makes silence deliberate rather than forgetful. The second makes sure
the next session inherits the frame rather than re-deriving advice the user has
already declined.

## Direction on a project with no stated objective

Common, and not a failure. Record it plainly:

```
Objective   UNKNOWN — not stated in README, docs, or any commit message.
            The code is evidently for [what it does]; why it exists has
            not been recorded anywhere.
```

Then answer direction questions from what the code is evidently for, and say
that is what you are doing. On a project with no written objective, that
sentence is frequently the most useful output of the session — and it is the
reason a recommendation can be honestly labeled *"this comes from what is
closest to working, not from what matters most to you."*

Never fill the gap with a plausible-sounding goal. A fabricated objective reads
exactly like a discovered one, and every recommendation built on it inherits the
fabrication invisibly.

## Recommendations follow direction, not the other way round

The order matters. Establish what the project is becoming, then decide what to
do about it. Reversing those two produces the characteristic failure of
architecture advice: a recommendation in search of evidence.

```
Right   the schema, the trajectory and the interface all point at a lifecycle
        → therefore the next step is to define one
Wrong   defining a lifecycle is good practice
        → therefore let us find some evidence that this project needs one
```

Where the recommendation goes from there — the six reads, the ranking, the
concreteness tests, the answers that are frequently right and rarely given —
lives in `next-action.md`.

## What direction can never tell you

Nothing in a repository reveals market demand, willingness to pay, what a
competitor is shipping, internal politics, undisclosed strategy, legal
requirements, what a stakeholder promised, or how long the runway is.

When a reading of direction depends on one of those, name the dependency and
hand it back:

> If the reporting feature is the thing customers are asking for, ignore this
> and build it. I only see that nothing in the repository connects it to
> anything else.
