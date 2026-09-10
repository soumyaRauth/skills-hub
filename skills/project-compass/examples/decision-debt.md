# Example — The same question, for the third time

Decision debt is invisible in any single file. It shows up as three
implementations quietly disagreeing about something nobody ever decided.

---

## The request

> Add bulk approve to the adjustments queue — managers should be able to select
> several and approve them at once.

---

## What the state already held

```markdown
# open-questions.md
## Can an approved adjustment be edited?
Impact      High — permissions, audit trail, reporting totals
Blocks      the approval UI (worked around 2026-08-27)
Surfaced    2× — src/api/adjustments.ts:140, ui/EditPanel.tsx:22
Default     none recorded
```

Two instances. Below the bar, so nothing had been said. This request makes it
three, and it is the first one where the question is not avoidable.

---

## Verifying before speaking

State is a cache. Both recorded locations get re-read, and the code has moved
since — which is the point of re-checking:

```
src/api/adjustments.ts:140     OBSERVED  PATCH rejects when approved_at is set
ui/EditPanel.tsx:22            OBSERVED  edit controls stay enabled after approval;
                                         the save fails with a 400 the UI swallows
src/reports/monthly.ts:57      OBSERVED  totals recompute from the current row,
                                         so a post-approval edit silently changes
                                         a month that was already reported
```

The third location is new and was not in the file. It also changes the price of
the question: this is no longer a UI inconsistency, it is a reporting integrity
question. Update `open-questions.md` first, then decide what to say.

---

## Mode C, and why

Bulk approve *cannot* be built without answering this. Approving fifty
adjustments at once means deciding what happens to the ones that get edited
afterwards, and the three existing answers do not agree.

Irreversibility applies too: whichever behavior ships becomes what customers
depend on, and the reporting path means the wrong choice corrupts numbers people
have already seen.

Do the part that does not depend on the answer. Ask the one question. Offer the
default.

---

## The response

> Bulk approve is wired up — selection, the manager check, and a partial-failure
> result so one bad row does not silently drop the other forty-nine.
> `api/adjustments/bulk-approve.ts`, tests for the mixed-outcome case.
>
> **I need one answer before I finish the audit trail.** Can an approved
> adjustment still be edited? Right now the API says no, the UI leaves the edit
> controls enabled and swallows the failure, and monthly reports recompute from
> the current row — so an edit after approval would change a month that has
> already been reported, with nothing recording that it happened.
>
> That is the third place this question has come up. It is a policy call, not a
> technical one, so I do not want to guess it a fourth time.
>
> **My default, if you would rather not decide now:** approved is final; editing
> requires an explicit *reopen* that is audited and that flags the affected
> reporting period. I will build that unless you say otherwise, and it is
> reversible in either direction as long as we pick it deliberately.

---

## What makes this work

**One question.** Not "the lifecycle is underspecified" — a yes/no a human can
answer between meetings.

**The contradiction is shown.** Three behaviors, three locations. That is what
makes it obviously theirs to answer rather than something the agent should have
figured out.

**The consequence is specific and material.** Reported numbers changing after
the fact. Not "inconsistency".

**A default is offered**, so the cost of not deciding is five seconds, and the
work is not held hostage. Roughly always, the default is accepted.

**It says what happens with the answer.** The abstract policy question becomes a
concrete piece of code.

---

## Recording it

Answered:

```markdown
# decisions.md
## Approved adjustments are final; reopening is explicit and audited
Decided by the user, 2026-09-05
Reason     reported totals must not change silently
Constrains the edit UI, bulk approve, the audit record, monthly reports
Follow-up  ui/EditPanel.tsx:22 still enables edit controls after approval — a
           real bug this uncovered, now fixed
```

Unanswered:

```markdown
# open-questions.md
## Can an approved adjustment be edited?
Surfaced    3× — api:140, ui:22, reports/monthly.ts:57
Default     No; reopen is explicit and audited. Proceeding on this.
Reversible  yes, until the reopen action ships to customers
```

Either way it stops being asked, which is the entire value. The next feature
that touches approval reads one line instead of guessing for the fourth time.
