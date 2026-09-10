# Example — Eight isolated features that turned out to be a system

The pattern this skill exists to catch, and the one no single request reveals.
Each ask was legitimate. Nobody in the loop ever asked what they added up to,
because each one arrived alone and was cheap.

---

## Ten weeks of requests

```
2026-06-30  lookup   Customer lookup by email
2026-07-07  lookup   Customer detail page
2026-07-14  console  Search on the customer list
2026-07-21  console  Filters: plan, status, region, signup date, last seen
2026-07-28  console  Sortable columns
2026-08-04  console  CSV export
2026-08-11  console  Bulk deactivate and bulk delete
2026-08-18  console  Saved segments — a filter set, named and reused
2026-08-25  access   Staff groups; a group can be given manage rights
2026-09-02  access   support_lead can reassign accounts
```

**Request, 2026-09-09:**

> Add an audit log of admin actions.

---

## The question that gets asked at four entries

Not *"how many features is that?"* — the answer is ten entries, eight of them
capabilities added since mid-July, and a count is not a finding. The structural
question: **what do these add up to, and has anyone defined it?**

The README says: *"Internal page for support staff to look up a customer."*

What is in the repository is a list-management console with bulk mutation, saved
views, export, and a staff access model. That is not a lookup page. It is an
administration system, and nobody named the moment it became one.

That claim needs more than a count, so it gets checked against the code.

---

## Checking it — three places that already disagree

**Two parallel permission mechanisms.** `api/permissions.js:can()` decides by
`staff.role`. `api/export.js` ignores it and asks `groups.isManager()` instead,
so export is governed by group membership while bulk delete is governed by role.
`api/groups.js:addToGroup` accepts either. There is no third place that agrees
with both, because there is no rule.

```
OBSERVED  api/permissions.js:4      role-based, five actions, admin short-circuits
OBSERVED  api/export.js:6           group-based, ignores can() entirely
OBSERVED  api/groups.js:15          either mechanism grants group membership
```

**Two ideas of deletion.** The schema carries `customers.deleted_at`, and
`customers.list` filters on it. `bulkDelete` issues a hard `DELETE`. So the
console has soft delete everywhere except in the one operation that runs on
fifty rows at a time.

```
OBSERVED  db/schema.sql:10          deleted_at column
OBSERVED  api/customers.js:7        list filters deleted_at IS NULL
OBSERVED  api/customers.js:28       bulkDelete does a hard DELETE
```

**Three ideas of what a filter is.** `CustomerFilters.jsx:1` offers five fields.
`saved_segments` has columns for two, and `SavedSegments.jsx:2` silently drops
the rest. `export.js` exports every column in the table regardless of the filter
that was on screen.

And one thing that simply does not work: `customers.reassign` writes
`owner_staff_id`, which is not in `db/schema.sql`. The most recent release cannot
have run.

---

## Why this is Mode C rather than a flag

An audit log is a record of **who did what to whom, and under what authority.**
Every one of those four fields is currently ambiguous in this codebase:

```
who        staff.role, or staff group membership, or both — export and bulk
           delete already answer this differently
what       "deleted" means two different things depending on which path ran
to whom    fine
authority  there is no rule to record. Only call sites
```

Building the audit log now means picking answers at the logging layer and
freezing them. Audit records are the worst possible place to guess: they get
exported, they get quoted in incidents, and they are the one table nobody is
willing to backfill or rewrite later. That is the irreversibility exception, on
top of a pattern that cleared all four gates.

---

## The response

> **I'd stop for a moment before building this.**
>
> Not because an audit log is wrong — because we cannot currently say what it
> would record. An audit entry is *who did what to whom under what authority*,
> and three of those four are ambiguous right now:
>
> - **Who is allowed** is decided two different ways. `permissions.js:can()` goes
>   by `staff.role`; `export.js` ignores it and asks `groups.isManager()`
>   instead. So export is governed by group membership and bulk delete by role,
>   and nothing reconciles them.
> - **What happened** has two meanings. Everything treats `deleted_at` as the
>   delete, except `bulkDelete`, which issues a hard `DELETE` — the one operation
>   that runs on fifty rows at once is the one that leaves nothing behind to
>   audit.
> - **Under what authority** has no answer to record. There is no rule, only
>   call sites.
>
> Worth naming what has happened here: this stopped being a lookup page a while
> ago. Search, filters, sorting, saved segments, export, bulk mutation and staff
> groups over one entity — that is an administration console, and the audit log
> request is what usually arrives right after a project crosses that line.
>
> **What I'd do first**, and it is about an hour: write down the administration
> model. Three questions settle it —
>
> 1. Does authority come from a role, from group membership, or from both? (If
>    both, which wins?)
> 2. What can be done to a customer, and which of those are reversible?
> 3. Who may change staff access itself — right now a group with `can_manage`
>    can add members to any group, including its own.
>
> Then the audit log records the answers instead of inventing them, and
> `export.js` stops being a second permission system.
>
> One thing separate from all of this: `customers.reassign` writes
> `owner_staff_id`, and that column is not in the schema. Last week's release
> cannot have worked — worth checking before anything else.
>
> If you would rather I just add the audit log against the current call sites, say
> so and I'll do that — it is your call, and I would log the acting staff id, the
> action string and the target id, which is at least recoverable later.

---

## Why it reads that way

**It names the thing.** *"This is an administration console now"* is the most
useful sentence in the response, because it turns a vague sense that things are
getting complicated into a category with known answers.

**It does not complain about the eight features.** They were fine. The point is
about the ninth, and about the decision that makes the next ten cheaper.

**Three questions, one hour, a named artifact.** Not "define your authorization
model", which is a project. Three questions someone can answer over coffee.

**The consequence is specific to audit logs**, not generic. Audit tables are
quoted in incidents and are the ones nobody backfills. That is why this is a
pause and the export request three weeks ago was not.

**The broken release is separated out.** `owner_staff_id` has nothing to do with
the pattern; it is just broken, and burying a real bug inside a structural
observation is how both get ignored.

**The exit ramp is real, and it is specific.** Not "I can do it anyway" but
*here is exactly what I would log if we skip this*, so declining costs one word
and produces something recoverable.

---

## Afterwards

If the user answers, `direction.md` is rewritten and the pattern closes:

```markdown
# Direction
**Appears to be**  Staff administration console for customer accounts
**Becoming**       — crossed already; recorded 2026-09-09        OBSERVED
**Biggest gap**    closed — administration model written down, see decisions.md
**Next step**      route export.js and bulkDelete through the single rule,
                   then the audit log
**Verified**       2026-09-09
```

If the user says *"just add the audit log, we'll sort permissions out later"*:

```markdown
# decisions.md
## Administration model stays undefined for now
Decided by the user, 2026-09-09
Reason     audit log is needed for a customer conversation this week
Status     Accepted — do not raise again unless the two permission paths
           disagree in a way that lets someone act without authority
```

Also closed. The escape hatch is observable rather than "unless it gets worse",
and the audit log gets built the same session, because that was always the deal.
