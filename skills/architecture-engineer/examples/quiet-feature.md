# Example — the requests that sound architectural and are not

Half of this skill's value is not engaging. A skill that turns every feature
request into a design session gets uninstalled, and the one genuinely
architectural moment in month three never gets the attention it deserved.

Three vignettes, illustrative.

---

## 1 — Sounds architectural, is not

> Where should I put the function that formats invoice totals for display?

Phase 1 answers it: a different decision here changes one module and is trivial
to undo. There is no architecture work.

**Response:** beside the other invoice formatting, in the module that already
owns it, matching the existing convention. Then the code.

No `.architecture/` write, no `⚡` line, no options table, no question about
scale. The word *where* is not an invitation.

---

## 2 — Genuinely architectural, handled in four lines

> Add organization-level permissions so customers can manage their own teams.

This one is real. It moves a tenancy boundary, changes who may read what, adds
a subject to every authorization decision, and touches every query that returns
customer data. It is also expensive to reverse once populated — a data model
plus a security boundary, both in rule 7's right-hand column.

But it does not earn a design session, because only one decision is genuinely
open. `CONSULT`, not `ACTIVE`:

> One decision worth settling before I build this, because it is hard to change
> once there is data in it: **does a user belong to exactly one organization, or
> can they belong to several?**
>
> Your schema currently assumes one — `users.organization_id` is non-null and
> every query filters on it. Several means a membership table and a "current
> organization" concept in the session, which is a bigger change now and a much
> bigger one later.
>
> If one is right, I'll build it on the existing column. Say the word if
> multi-org is coming.

Four lines, one question, and the work proceeds either way. What it did not do:
open a discovery session, produce an options table, ask about scale, or write a
target architecture for a permissions feature.

---

## 3 — Messy project, ordinary request

> Bump the date library to v4 and fix what breaks.

The repository is genuinely tangled: business rules in controllers, two writers
for one table, authorization at call sites. All of it visible. None of it this
request's business.

**Response:** the upgrade, the call sites fixed, the tests run.

The architecture findings are not mentioned. They will still be true tomorrow,
and noticing them unprompted is `project-compass`'s job — it has the
interruption budget and the four gates that decide whether the observation has
earned a sentence. This skill does not volunteer an architecture review because
the code looks bad.

---

## The line

```
Engage              Stay quiet
"design this"       "where does this function go?"
"how should this    "add a field to this form"
 be structured?"
"review our         "this codebase is messy" — that is Project Compass's
 architecture"       call, not an invitation
"monolith or        "refactor this class"
 services?"
a handoff from      a large repository
another skill
```

The test is not whether architecture *exists* in the vicinity. It always does.
The test is whether a different answer would change more than one module, or
something expensive to undo — and whether anyone asked.
