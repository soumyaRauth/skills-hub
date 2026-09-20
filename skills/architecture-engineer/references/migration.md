# Migration

Getting from the architecture that exists to the one that was decided, in states
that each work.

## The default is not a rewrite

A rewrite proposes to reproduce every behavior the current system has — the
documented ones, the accidental ones, and the ones customers depend on that
nobody has written down — while the original keeps changing underneath. It is
occasionally right. It needs an argument, and the argument is almost never
"the code is messy".

```
Rewrite is defensible when          Rewrite is not defensible because
the platform is end-of-life and     the code is ugly
unsupported
the data model cannot represent     the framework is unfashionable
what the business now requires
the system is small enough to       a rewrite would be more satisfying
rebuild in weeks, not quarters
```

Default to an evolutionary path where every state ships.

## Transition states

```
Current  →  Transition 1  →  Transition 2  →  Target
```

Each state is a system someone could run in production for a month without
distress. Not a checkpoint in a long branch — a shippable configuration.

Each step names:

```
Objective      the one thing this step changes
Touches        modules, tables, contracts
Risk           what could break, and how it would show
Validation     what is checked afterwards, concretely
Rollback       how to undo it, and whether that stays true after data moves
Production     does the system keep running during it
```

If a step cannot be described this way, it is too big. Split it.

## Patterns, and when each is the right one

| Pattern | Use when | Cost |
| --- | --- | --- |
| **Strangler routing** | A boundary can be put in front of the old path and traffic moved gradually | A routing layer, and a period where both exist |
| **Anti-corruption boundary** | The new model must not inherit the old one's shape | A translation layer that is genuinely thrown away later |
| **Dual write, read cutover** | Data must move without downtime | Two writers and a consistency window; needs reconciliation |
| **Expand / migrate / contract** | A schema change that cannot be atomic | Three deploys instead of one |
| **Compatibility shim** | Consumers cannot all move at once | A thing that must actually be deleted, with a date |
| **Branch by abstraction** | The seam is internal and traffic routing is overkill | An interface that exists during the migration |

Use one because the situation calls for it, not because it has a name. A shim
nobody removes is a permanent second implementation, which is what the migration
was supposed to end.

## Data migrations are the irreversible part

Code rolls back. Data usually does not.

```
Adding a column, nullable                 reversible
Backfilling a column                      reversible, if the old value survives
Making a column non-nullable              reversible only while old code tolerates it
Dropping a column                         not reversible — the data is gone
Splitting a table                         reversible only with the join preserved
Changing an identifier scheme             not reversible once anything external stores it
```

Rules that follow:

1. **Expand before contract.** Add the new shape, write both, read the new one,
   and only then remove the old — in separate deploys.
2. **Never drop in the same step that stops writing.** Leave a window long
   enough to notice.
3. **A backfill is a program**, not a statement: batched, restartable,
   idempotent, and observable from outside.
4. **Rollback plans expire.** Say when: *"revertible until the contract step,
   after which rolling back loses status changes made in the interim."*

## Sequencing

Order by what unblocks the rest and what reduces risk soonest:

```
1  Make the current behavior observable, if it is not — you cannot verify a
   migration whose starting behavior nobody measured
2  Establish the seam without moving anything (an interface, a routing layer)
3  Move the readers, which is reversible
4  Move the writers, which usually is not
5  Remove the old path
6  Delete the shim
```

Step 6 is the one that gets skipped, and skipping it means the migration did not
reduce complexity, it doubled it. Put a date on it.

## Before moving a boundary

The blast radius belongs to the skill that owns it:

```
HANDOFF → impact-map: moving order-status writes behind OrderService touches
          every current writer, including the reporting SQL [A-014]
```

And the behavior that must survive belongs to another:

```
HANDOFF → proof-driven-dev: the cancellation window must behave identically at
          the 15-minute boundary before and after extraction [D-006]
```

Architecture Engineer decides where the boundary goes. It does not own the list
of everything the move touches, or the proof that behavior held.

## Implementing

`MIGRATE` changes the project only when implementation was asked for, and then:

- one transition state at a time, never the whole plan in one pass
- the project's own checks run after each state, with real output
- the structural change verified, not asserted — see `fitness-checks.md`
- a state that fails its validation is reported as failed and not built upon

Report what moved and what did not:

```
Transition 1 of 3 complete.

Moved      order-status writes from 3 call sites into OrderService
Verified   no writer outside OrderService (grep + the import rule added in
           .eslintrc), suite 214/214, cancellation boundary test added
Not done   reporting still reads the column directly — transition 2
Rollback   revert the commit; no data changed
```

A migration step is complete when the structure changed **and** something
checked it. Code was edited is not the same claim.
