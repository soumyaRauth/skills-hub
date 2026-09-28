# Example — three tickets, one blocked on a product decision

Illustrative. The project is the fixture `tests/fixtures/delivery-lead/planned-backlog`,
a class-booking app with `tracker: local`, `merge: auto`, and the default
budget of 5.

## Request

> Work through the backlog.

## Before the first ticket

```
⚡ Delivery Lead — working the M1 backlog
RUN START  milestone M1 · 1 ready, 2 waiting on dependencies · budget 5 · tracker local · autonomy: merge auto, deploy_production ask
```

`git status` is clean. No earlier run ledger.

## T-002 Class list page

The planner moves it to `in_progress`. Branch `t/T-002-class-list-page`.
The ticket's three acceptance criteria go to ProofBuild as its requirements.
Nothing else engages: no shared concept changes, no new dependency, no
personal data.

```
✓ VERIFIED
Class list page · Requirements 3/3 · Regression pass
```

`/code-review` reports nothing on the branch. Commit `T-002: Class list page`,
PR opened, planner → `in_review`, checks pass, squash-merged (the history is
squash commits), planner → `done`.

```
[1/5] T-002 Class list page — done · VERIFIED · PR #12 merged · tracker local
```

## T-003 Book a class

Now ready: T-002 is done. Standards Compass engages on its own (a booking
stores the member's email) and adds one requirement; API Contract Guard stays
quiet (the only consumer ships in the same deploy). ProofBuild: `VERIFIED`,
4/4. Review, PR, merge.

```
[2/5] T-003 Book a class — done · VERIFIED · PR #13 merged · tracker local
```

## T-004 Cancel a booking

Ready now that T-003 is done. ProofBuild turns the four acceptance criteria
into requirements and finds the one nobody wrote down: what happens to the
payment when a member cancels late. `docs/spec.md` says bookings are paid and
says nothing about refunds. Its status:

```
⚠ REVIEW REQUIRED
Cancel a booking · 4/5 requirements verified
Decision required: a member cancels less than 24 hours before class — refund?
```

Not `VERIFIED`, so not done. The planner moves T-004 to `blocked` with
ProofBuild's question. The branch stays, unmerged. One blocked ticket does not
stop a run, but no ready ticket is left in M1, so this one stops.

```
[3/5] T-004 Cancel a booking — blocked · REVIEW REQUIRED · refund rule undecided
```

## Ledger and question

```
RUN 2026-09-28 10:14 · milestone M1 · 3 of 5 tickets · status stopped
T-002  Class list page            done         VERIFIED · PR #12 merged
T-003  Book a class               done         VERIFIED · PR #13 merged
T-004  Cancel a booking           blocked      REVIEW REQUIRED — refund rule undecided (question below)
Tracker  local
Next     nothing ready in M1 · answer the T-004 question to unblock it

STOPPED  nothing ready · 1 decision

1. T-004 Cancel a booking — when a member cancels less than 24 hours before
   class, do they get: [a full refund]  [no refund]  [a class credit]
```

## What it did not do

- Did not decide the refund rule, or build cancellation with a guessed one.
- Did not mark T-004 done on 4/5: only `VERIFIED`, or the human accepting
  `REVIEW REQUIRED` in so many words, would. The answer goes to
  `delivery-planner`, which records it in the ticket's decisions.
- Did not say the booking feature was safe to ship; the milestone is not
  complete, so Production Guard was not asked.
