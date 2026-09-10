# Example — Six controls and no workflow

The one this skill exists for. Each request is reasonable. The sequence is the
finding, and the person making the requests cannot see it, because they are
making them one at a time.

---

## The trajectory, over five weeks

```
2026-08-04  admin   Search added to the members table        ui/Members.tsx
2026-08-11  admin   Filters: role, status, joined date       ui/MembersFilter.tsx
2026-08-19  admin   Sortable columns                         ui/Members.tsx
2026-08-26  admin   Saved filter presets, per user           ui/SavedViews.tsx + table
2026-09-01  admin   Bulk actions: deactivate, change role    api/members/bulk.ts
                    pattern: control-accumulation (5th)
```

**Request, 2026-09-05:**

> Add CSV export to the members table.

---

## Against the four gates

| Gate | |
| --- | --- |
| Recurrence | Five instances, five weeks, five locations. Export is the sixth |
| Convergence | Every one adds a *control* to one table. One decision — what is this screen for — would have shaped all of them |
| Consequence | Export is the second feature in a row that needs to know which columns matter, and there is no answer. Bulk actions already guessed, and guessed differently from saved views |
| Actionability | One sentence naming who uses this screen and what they are trying to finish. Ten minutes |

Clears the bar. And a detail that raises it from a passing note to something
worth a question: **saved views store `role`, `status`, `joined`; bulk actions
operate on `role` and `active`; the export request does not say which columns.**
Three features, three different ideas about what a member *is* here.

Not Mode C. Nothing is contradicted, nothing is irreversible, export is
independently useful, and the missing definition does not change what export
should do today. **Mode B** — build it, flag one thing.

---

## The response

> Export added — all visible columns, respecting the current filter and sort,
> streamed so large orgs do not time out. `api/members/export.ts`, one test
> covering the filtered case.
>
> **One thing I'd flag.** That is six controls on this table since August:
> search, filters, sorting, saved views, bulk actions, now export. Each made
> sense on its own, but they are pointing at a workflow nobody has written down
> — and it is already showing: saved views track role, status and joined date,
> bulk actions work on role and active, and export just took everything.
>
> Before the seventh, one sentence would settle it: who opens this screen, and
> what are they trying to finish? If it is "support checks whether someone still
> has access", the table needs three columns and a search box, and half of what
> is there is in the way. If it is "an admin does quarterly access reviews", then
> export is the main event and it should probably be scheduled rather than
> clicked.

---

## Why it reads that way

**The work came first.** The user asked for export and got export, tested. The
observation is not a toll.

**The instances are named.** Six controls, five dates, three inconsistent column
sets. Every one checkable in thirty seconds — that is what makes the last
paragraph credible rather than a lecture.

**The consequence is concrete.** Not "this may become hard to maintain" but
*these three features already disagree about what a member is*.

**The question is answerable in a sentence**, and both plausible answers are
supplied — because they lead to genuinely different products, which is the
actual point.

**No solution was proposed.** Not "you need an information architecture", not a
redesign. The missing thing is one sentence from a human, and the code follows.

**It still ends in an action.** *"Before the seventh, one sentence would settle
it"* is a next step with a trigger attached — not "worth thinking about", which
is what the same observation becomes when the action is left off.

---

## Afterwards

If the user answers:

```markdown
# decisions.md
## The members table is for support access checks
Stated by the user, 2026-09-05
Constrains column set, saved views, export, anything added to this screen
Note      quarterly access review is a separate need — not this screen
```

Pattern closed. It never comes up again, and the next request for a control on
that screen gets measured against a written purpose instead of against a hunch.

If the user says *"not now, just keep building"*:

```markdown
# decisions.md
## Members screen purpose stays undefined for now
Decided by the user, 2026-09-05
Status     Accepted — do not raise again unless two controls contradict each
           other in a way a user can see
```

Also closed. The counter keeps running silently; the escape hatch is specific
and observable, not "unless it gets worse".
