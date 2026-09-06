# Direction and what to do next

Two questions this file answers: *where does this project appear to be going?*
and *what should I do next?* They are the same question at different distances,
and both are answered from the project or not at all.

## Reconstructing direction

Direction is not what the README says the project is for. It is what the work
has actually been doing, which is often different and occasionally more honest.

```
Stated direction    README, docs, roadmap, what the user has said
Actual direction    trajectory entries, recent commits, where churn concentrates
Structural direction what the schema and the interface are becoming
```

When those three agree, direction is `OBSERVED` and there is nothing to say.
When they disagree, the disagreement is the finding — and it is usually the most
interesting thing in the project.

```markdown
### Direction

**Appears to be:** formalizing inventory adjustments — approval, audit,
reconciliation reporting.

**Evidence:** eleven of the last fourteen trajectory entries; the three newest
tables are all adjustment-related; the README still describes a stock-count tool.

**Confidence:** High for the direction, Low for whether it is deliberate.

**Worth noting:** the adjustment flow now has approval, audit and reporting, but
no defined lifecycle. Each of those three features invented its own idea of what
"approved" means.
```

Always separate *where it is going* from *whether that is intended*. The first
is evidence. The second is only ever the user's to state.

## Answering "what should I do next?"

This is the highest-value question the skill takes, and the easiest to answer
badly — a generic backlog is worse than no answer, because it looks like work.

Read six things before answering, in this order:

```
1  The objective                     what is this trying to achieve?
2  Blocked work                      what is waiting on an unmade decision?
3  Half-built things                 what is started and not usable?
4  The nearest outcome               what is closest to being real for a user?
5  Unretired risk                    what would hurt most, discovered late?
6  What was just being worked on     momentum is worth something
```

Then return **three items at most**, ordered, each labeled:

| Label | Means |
| --- | --- |
| `REQUIRED` | Something already asked for is blocked without it |
| `RECOMMENDED` | Evidence supports it; a reasonable person could sequence differently |
| `WORTH CONSIDERING` | Judgment. No strong evidence. Say so |

Never invent a fourth category, never present it as a roadmap, and never pad to
three when there is one.

## Answers that are frequently right and rarely given

**Keep going.** The current work is the thing; the project is `DIRECTED`. Say it
in one line and get out of the way. Manufacturing a concern here is the worst
failure this skill has, because it is invisible — it just quietly wastes weeks.

**Settle one decision.** Three features are waiting on a question a human can
answer in a sentence. This outranks all coding.

**Ship it and watch.** The feature is functional, the polish is speculative, and
nothing on the list is evidence-driven. See below.

**Measure it.** There is a suspicion of a performance problem and no number
anywhere. The next optimization is a guess with a deployment attached.

**Validate the assumption.** Something substantial is about to be built on a
belief about users that nothing has tested.

**Delete it.** Something half-built that nothing uses is charging maintenance
rent. Deleting is progress, and it is the recommendation nobody makes.

**Write it down.** A rule lives in four conditionals that disagree. One
paragraph fixes it more thoroughly than a refactor would.

## Ship it

Recommend shipping when the core workflow is functional end to end, the recent
work is refinement, and no known problem is driving the refinement.

The evidence is specific: several iterations on the same surface, no bug report,
no usage data, no user request behind them.

> This screen has been through four passes and the workflow already works. Unless
> you know of a usability problem I cannot see, I would ship it and let real use
> tell you what to fix next — right now we are guessing about what is worth
> polishing.

Do not say this when there is a known defect, an accessibility gap, a security
issue, or anything that costs a user something real. "Ship it" is about
diminishing returns, never about lowered standards.

## Recommendations change with maturity

The same project deserves different advice at different points, and a skill that
gives the same answer in week ten as in week one has learned nothing:

```
Early     make one path work end to end; do not generalize anything yet
Then      validate that the path is the right one, with a real user or real data
Then      define the rules the path assumed — lifecycle, permissions, failures
Then      stabilize: failure modes, idempotency, the parts that lose data
Then      measure, and optimize what the measurement names
Throughout delete what nothing uses
```

This is a shape, not a checklist, and skipping steps is often correct. Its use
is as a sanity check: a project doing step five in week one is optimizing
something nobody has used, and a project on step one in month nine has never
finished anything.

## What this can never know

Say so plainly when it applies. Nothing in a repository reveals:

market demand · willingness to pay · what a competitor is shipping · internal
politics · undisclosed strategy · legal or regulatory requirements · what a
stakeholder promised · how long the runway is · who is about to quit

When a recommendation depends on one of those, name the dependency and let the
human decide:

> If the reporting feature is the thing customers are asking for, ignore this
> and build it. I only see that nothing in the repository connects it to
> anything else.
