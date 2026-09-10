# The next action

The output of this skill is not an observation. It is a specific thing to do
next, chosen because it improves the project's trajectory more than the
alternatives, and stated concretely enough that someone could start it in the
next five minutes.

Everything else — the model, the trajectory, the evidence labels — exists to
make this one sentence trustworthy.

## The chain

For every non-trivial request:

```
USER REQUEST
      ↓
WHAT IS BEING ASKED?                     the literal request
      ↓
WHAT DOES THE PROJECT LOOK LIKE?         identity, workflows, domain, decisions
      ↓
WHAT HAS IT BEEN BECOMING?               the sequence, not the last request
      ↓
WHAT DOES THIS REQUEST ASSUME?           and is the assumption recorded anywhere?
      ↓
WHAT DOES THIS CHANGE AFFECT?            workflows, data, rules, boundaries
      ↓
IS THERE AN UNRESOLVED GAP?              between what exists and what this needs
      ↓
IS THE GAP IMPORTANT ENOUGH NOW?         the four gates, in intervention-rules.md
      ↓
WHAT IS THE BEST NEXT ACTION?
      ↓
MODE A build it  ·  MODE B build + flag  ·  MODE C pause and guide
```

Most requests fall out at the sixth row with *no*, and the whole pass costs one
read of `.project-compass/` plus whatever the work needed anyway.

## The reads that produce an answer

When asked directly — *"what should I do next?"*, *"what should I build?"*,
*"what am I missing?"* — read these six, in this order, before answering:

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
three when there is one. Say what *not* to do as well — half a good answer to
"what next" is the deprioritization, and it is the half usually missing.

## Ranking, when several things could be done

Rank by what most improves the trajectory. Not by category, and specifically
**not by putting technical concerns above product and workflow ones**.

```
1   Blocking decisions          work already asked for is waiting on a sentence
2   Core workflow gaps          the main path does not complete end to end
3   Data and domain model       the wrong shape here costs migrations later
4   Architectural boundaries    getting more expensive by the week
5   Security and data integrity risk
6   User-facing workflow problems
7   Repeated implementation patterns wanting one abstraction
8   Technical debt
9   Performance
10  Cosmetic work
```

Two adjustments to the order, both common:

**Irreversibility promotes.** Anything about to be baked into a public API, a
populated data model, an external identifier scheme or a security boundary moves
up, because the cost of being wrong is asymmetric.

**Live harm promotes to the top, always.** A security hole a user can reach, a
path that loses data, a bug costing someone money — those outrank every
structural concern on the list and are never traded against elegance.

The rest is judgment. A rule of thumb that survives contact: a decision that
three planned features are waiting on, that is expensive to reverse, and that has
already resurfaced three times, outranks everything else in the project.

## Concreteness

A finding that does not name an action is not finished.

```
Not this                             This
"There is no order lifecycle"        "Define the order lifecycle — states and
                                      legal transitions — before adding a fifth
                                      status"
"There is technical debt"            "Extract the shared permission rule and route
                                      the three existing paths through it before
                                      adding a fourth exception"
"Product direction is unclear"       "Decide what the dashboard is meant to help
                                      someone decide, before the next widget"
"Consider improving the             [delete — this is not a step]
 architecture"
"You should think about scaling"    [delete — this is not a step]
```

Three tests a next action has to pass:

1. **Smaller than what it prevents.** Four questions beat a refactor. A page of
   states beats a rewrite. If the recommendation is bigger than the request, it
   is an objection, not a recommendation.
2. **Startable today.** Name the artifact — the questions to answer, the file to
   write, the number to measure, the thing to delete.
3. **It says what happens with the answer.** *"If it is no, I'll add an explicit
   reopen action that gets audited"* converts an abstract decision into a
   concrete consequence, which is what makes people answer it.

## Answers that are frequently right and rarely given

**Keep going.** The current work is the thing; the project is `DIRECTED`. Say it
in one line and get out of the way. Manufacturing a concern here is the worst
failure this skill has, because it is invisible — it just quietly wastes weeks.

**Settle one decision.** Three features are waiting on a question a human can
answer in a sentence. This outranks all coding.

**Finish the workflow underneath.** Interface work is running ahead of a path
that does not complete. See below.

**Ship it and watch.** The feature is functional, the polish is speculative, and
nothing on the list is evidence-driven.

**Measure it.** There is a suspicion of a performance problem and no number
anywhere. The next optimization is a guess with a deployment attached.

**Validate the assumption.** Something substantial is about to be built on a
belief about users that nothing has tested.

**Delete it.** Something half-built that nothing uses is charging maintenance
rent. Deleting is progress, and it is the recommendation nobody makes.

**Write it down.** A rule lives in four conditionals that disagree. One
paragraph fixes it more thoroughly than a refactor would.

## Sequencing: when the interface is ahead of the workflow

A specific and common failure that the priority list above exists to catch.

**The shape:** repeated requests to change, polish, or extend the interface,
while the workflow the interface is for does not complete. Screens get refined
around functionality that is not there.

**The evidence, all of which must be present:**

```
The core path has a break in it        a button wired to nothing, a worker
                                       attached to no scheduler, a step that
                                       has no backend
The recent work is all presentation    three or more UI-tagged entries running
                                       while that break stays open
Nothing indicates the break is next    no request for it, no TODO with a date,
                                       no branch
```

**The response** is a sequencing recommendation, not a criticism of the UI work:

> The last three changes have all been on the invoice screen, and the invoice
> workflow still stops at "Download PDF", which is wired to an empty handler
> (`InvoiceView.jsx:41`). I would finish the path first — right now the polish
> is being applied to a screen that a user cannot get to the end of, so we are
> guessing about which parts of it matter.

**Not this** when the user has said the interface is the current job, when the
break is deliberate (a stub for a feature explicitly deferred), when the polish
is fixing something reported, or when the missing backend belongs to someone
else. Ask before diagnosing whenever the answer would change the advice.

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

A shape, not a checklist, and skipping steps is often correct. Its use is as a
sanity check: a project doing step five in week one is optimizing something
nobody has used, and a project on step one in month nine has never finished
anything.

## When the developer has stated a goal

Their stated goal replaces the inferred one. Completely, and without argument.

```
"This is a throwaway prototype"          → optimize for learning speed; no
                                           lifecycle modeling, no abstractions,
                                           no tests beyond what unblocks them
"I know it's not ideal, I'm
 experimenting"                          → help experiment. Say nothing about
                                           the architecture. Once.
"We've already decided to split it —
 I'm asking about sequencing"            → answer the sequencing question. Do
                                           not re-argue the decision.
"I just want it working by Friday"       → recommend the shortest path that
                                           works, and name only what will hurt
                                           before Friday
"This is a learning project"             → the recommendation is whatever
                                           teaches most, not what ships fastest
```

Record it in `decisions.md` so the next session inherits it. Overriding a stated
goal with your own engineering preference is the fastest route to being ignored,
and it is also just wrong: they know the goal and you do not.

## What this can never know

Say so plainly when it applies. Nothing in a repository reveals:

market demand · willingness to pay · what a competitor is shipping · internal
politics · undisclosed strategy · legal or regulatory requirements · what a
stakeholder promised · how long the runway is · who is about to quit

When a recommendation depends on one of those, name the dependency and let the
human decide:

> If the reporting feature is what customers are asking for, ignore this and
> build it. I only see that nothing in the repository connects it to anything
> else.
