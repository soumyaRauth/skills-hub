# Example — "Should we split this service?"

A staff engineer asking an architecture question does not need a definition of a
microservice. They need the parts of the answer that live in *this* repository
and that they have not had time to go read.

The failure here is answering with the general case.

---

## The request

> We're thinking about splitting billing out of the monolith. Thoughts?

---

## What is actually asked

"Should we split X" is almost never about the split. Underneath is one of:

```
deployment coupling      billing releases are blocked by unrelated work
failure isolation        a billing bug takes down the product
scaling                  billing has a different load profile
team boundaries          two teams are colliding in one codebase
domain clarity           the boundary is unclear and a split would force it
```

Different answers, opposite in places. So the evidence gets read before the
opinion.

---

## Evidence

```
Deploy coupling
  git log --format='%h %s' --since='6 months' -- src/billing | wc -l   → 214
  Commits touching billing AND non-billing in one change              → 61 of 214
  Release cadence: weekly, whole monolith                             OBSERVED

Coupling at the boundary
  src/billing imports from src/{orders,users,notifications}           23 call sites
  Non-billing imports from src/billing                                41 call sites
  Shared tables written from both sides: subscriptions, invoices,
    usage_records, and orders.billing_status                          OBSERVED
  Transactions spanning billing and orders tables                     7 OBSERVED

Failure isolation
  Billing incidents in 6 months                                       2 (from the
    incident log in docs/) — neither took down non-billing traffic
  Provider timeouts already isolated behind a circuit breaker         OBSERVED

Load
  No metrics in-repo                                                  UNKNOWN

Ownership
  git shortlog on src/billing: 9 authors, no concentration            OBSERVED
```

---

## The answer

> The evidence in the repo points at a boundary problem rather than a deployment
> problem, and splitting now would make the boundary harder to fix rather than
> easier.
>
> **What the coupling actually looks like.** 41 inbound call sites from
> non-billing code into `src/billing`, 23 outbound. Four tables are written from
> both sides, and seven transactions span billing and orders — `applyCredit` and
> `cancelOrder` both update `orders.billing_status` and `invoices` in one
> transaction. Splitting makes each of those a distributed write, and the
> reconciliation for that is not in the current plan because nothing has forced
> anyone to name what "an order that is cancelled but whose credit failed to
> apply" is.
>
> **The pressure you are feeling is real, though.** 61 of the 214 billing
> commits in the last six months also touched something else, which is a
> genuinely coupled release train. That is the symptom. Splitting the deployment
> is one treatment; it just happens to be the one that pays the boundary cost up
> front, before the boundary is known.
>
> **What I have not got.** No load data in the repo, so if billing has a
> materially different scaling profile that changes the calculation and I cannot
> see it. Ownership does not point at a split either — nine authors across
> billing in six months, no concentration, so this is not two teams colliding.
>
> **What I would do instead, in this order.** Move the four shared tables behind
> a billing-owned module and route the 41 inbound call sites through an explicit
> interface, in place. It is mechanical, it is reversible, and it turns the
> question into an observable one: after that, the transactions that still span
> the boundary are exactly the split's cost, written down. Right now that number
> is seven and nobody has looked at it.
>
> If the release train is the urgent part, decoupling the deploy is a separate
> and much cheaper lever than decoupling the code.

---

## What is absent, deliberately

- No definition of a microservice, a bounded context, or a distributed
  transaction.
- No general discussion of monolith versus services.
- No recommendation of a saga, an outbox, or any pattern by name. The engineer
  knows them; naming them is filler.
- No hedging into uselessness. It takes a position — the boundary is the
  problem — and shows the count it rests on.
- No pretence about load. `UNKNOWN`, said once, with what it would change.

---

## The move worth stealing

The recommendation converts an irreversible decision into a reversible
experiment that produces the missing evidence. In-place modularization is most
of the work of a split, it is undoable in an afternoon, and it ends with the
number that actually decides the question.

That is generally the strongest thing this skill can offer a senior engineer:
not an opinion about the architecture, but a way to find out that costs less
than being wrong.

Note what the recommendation is not. It is not "the boundary is unclear" — that
is the observation, and it would have been useless on its own. It is *move the
four shared tables behind a billing-owned module and route the 41 inbound call
sites through an interface, in place, this week*. Startable today, smaller than
what it replaces, and it ends with the number that decides the original
question.

---

## If they disagree

> *"We've already decided to split — I'm asking about sequencing."*

Then the decision is made, and the useful contribution is the seven
cross-boundary transactions and the four shared tables, as a sequencing input.
Record it and move on:

```markdown
# decisions.md
## Billing will be extracted into its own service
Decided by the team, before 2026-09-05 (stated by the user)
Note      7 cross-boundary transactions and 4 dual-written tables are the known
          cost; sequencing should retire them first
Status    Active — do not re-argue the split
```

Re-litigating a decision the user has already made is how a skill gets turned
off, and the sequencing question was a good one.
