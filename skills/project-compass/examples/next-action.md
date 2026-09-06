# Example — "I don't know what to work on"

The answer must come from the project. A generic backlog — *add tests, improve
error handling, write documentation* — is worse than saying nothing, because it
looks like an answer and costs a week.

---

## The request

> Honestly I don't know what to do next. Everything's half done.

---

## What gets read, in order

**The objective.** `project.md` records it as `UNKNOWN` — the README describes a
"simple tool to track warehouse stock counts", and the schema now has
organizations, roles, approvals and an audit table. Re-checked: still true.

**Blocked work.** `open-questions.md` has one entry with `Blocks` filled in:
whether an approved adjustment can be edited. Three features named against it.

**Half-built things.** Four:

```
Reconciliation report   ui/Reconcile.tsx renders; the export button does nothing
Mobile intake           routes exist, no auth; unreachable from any nav
Notifications           email sends on approval; nothing on rejection or timeout
Bulk adjustments        API done, UI never started, blocked on the edit question
```

**The nearest outcome.** Intake → adjustment → approval → reconciliation is the
workflow the schema is built around. The first three work end to end. The fourth
renders and then stops at a dead button. One workflow is one button from being
real.

**Unretired risk.** No defined behavior when the approval email fails to send —
`workers/notify.ts` catches and logs. An approval that nobody hears about is
indistinguishable from one that never happened.

**Momentum.** The last four sessions were all on reconciliation.

---

## The answer

> Three things, and the first one is smaller than it sounds.
>
> **1. Finish the reconciliation export.** `REQUIRED`
> The intake → adjustment → approval → reconciliation path works end to end
> except for the export button on `ui/Reconcile.tsx:88`, which is wired to
> nothing. That is the only gap between "four features exist" and "one workflow
> a warehouse manager can actually complete". It is also where you already are —
> the last four sessions were all in that module.
>
> **2. Answer one question: can an approved adjustment be edited?** `REQUIRED`
> Bulk adjustments has a finished API and no UI because of this. The approval
> screen worked around it. Monthly reports recompute from the current row, so
> today an edit after approval would silently change a month that was already
> reported. It is a policy call, not a technical one — one sentence unblocks two
> features and closes a real reporting hole.
>
> **3. Decide what mobile intake is.** `RECOMMENDED`
> It has routes, no auth, and no way to reach it from the app. Either it is next
> and it needs a session story, or it is not and it should be deleted — leaving
> unauthenticated routes in the tree is the kind of thing that ends up shipped.
> Deleting it is progress; I would not leave it as it is.
>
> **What I would leave alone:** notifications. Rejection and timeout emails are
> missing, but nothing is blocked on them and there is no evidence anyone is
> waiting. It will look more urgent once the workflow is finished, and you will
> know more about what it should say.
>
> **One thing I cannot answer.** There is no objective recorded anywhere — the
> README still describes a stock-count tool, and what is in the repository is a
> multi-tenant approval system. That is not necessarily a problem, but it means
> the ordering above comes from what is closest to working, not from what
> matters most to you. If the priority is actually something like "the pilot
> customer starts in three weeks", tell me and the order probably changes.

---

## Why this shape

**Three items, ordered, labeled.** Two `REQUIRED` because named work is actually
blocked on them; one `RECOMMENDED`, and the reasoning is given rather than
asserted.

**Every item names a location.** `ui/Reconcile.tsx:88` is checkable in ten
seconds, and checkable claims are what make the rest believable.

**The first item is where the momentum already is.** Correct sequencing is not
just importance ranking — a person who is stuck benefits from finishing
something.

**Deleting is offered as progress**, which is the recommendation that almost
never gets made and is frequently right.

**Something is explicitly deprioritized, with a reason.** *What not to do* is
half the answer, and the half that is usually missing.

**The limit is stated at the end, not hedged throughout.** No invented objective,
no fabricated customer, no invented deadline — and a specific description of the
input that would change the answer.

---

## What this answer must never be

```
1. Add tests to improve coverage
2. Set up CI/CD
3. Improve error handling
4. Add monitoring and observability
5. Write documentation
6. Refactor for maintainability
```

All defensible. None derived from this project. Every one of them would be
equally true of any repository, which is exactly what makes them worthless here
— and a person who is already stuck will pick one, do it, and be no closer to a
working workflow than they were this morning.
