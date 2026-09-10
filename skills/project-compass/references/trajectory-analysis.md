# Trajectory analysis

A request is a signal. A sequence of requests is a trajectory, and a trajectory
carries information that no single request does — including information the
person making the requests does not have, because they see them one at a time.

## Extract the concept, not the words

Store what a request was *about*, not what it said. Raw prompts do not cluster;
concepts do.

```
"Let managers approve their own warehouse's adjustments"   → authz
"Add a bypass so support can read any ticket"              → authz
"Make the admin check configurable per org"                → authz

"Why is checkout slow?"                                    → performance
"Add caching to the product list"                          → performance
"Move the report to a background job"                      → performance
```

Use the project's own vocabulary when it has one — `billing`, `intake`,
`reconciliation` beat generic tags. Add a second tag when a request genuinely
touches two concepts; do not add a third.

## What is worth recording

| Record | Skip |
| --- | --- |
| A capability the project did not have | Renames, formatting, lint fixes |
| A rule, permission, or state that changed | Dependency bumps |
| A decision made, or exposed as missing | Test repairs that changed no behavior |
| A component, service, or dependency added | Questions that changed nothing |
| A reversal or an undo | Repeated attempts at the same task |
| A statement of intent by the user | Anything already recorded this session |

The skip column is longer in practice than the record column. Aim for a few
entries a week on an active project, not a few a day.

## Reading a sequence

Four things to look for, in ascending order of value.

**Concentration.** Several entries on one concept in a short window. Concentration
alone is not a problem — it is what focused work looks like. It becomes a
question when the concept is a *mechanism* (permissions, notifications, caching)
rather than a *feature*, because mechanisms are supposed to be defined once.

**Shape.** How the entries relate to each other matters more than how many
there are:

```
Additive     each adds a case to the same construct       → a rule is missing
Corrective   each fixes a variant of one failure          → a cause is missing
Escalating   each is a bigger mechanism for one problem   → a measurement is missing
Oscillating  changes reversed and reinstated              → a decision is missing
Radial       features fanning out from one screen         → a workflow is missing
```

The right column is the finding. The left column is the evidence for it.

**Reversals.** Anything undone, re-done, made configurable, or given a flag
after being decided. Reversal is the strongest single signal in a trajectory,
because it is the project saying out loud that a decision did not hold.
Two reversals on one concept usually beat five additions on it.

**Silence.** What has *not* been touched. A project six months into building a
payments flow with no entry ever tagged `reconciliation` or `failure` is not
missing a feature — it is missing a question. Absence is only evidence when you
looked for it, so name what you searched.

## From entries to structure

Counting is not the point. Four entries tagged `admin` is a number; *"these four
are an administration workflow that has never been defined"* is a finding. The
step between them is the one that matters, and it is the step a request-by-request
reading never takes.

```
Record        2026-08-04 admin  Search on the members table
              2026-08-11 admin  Filters: role, status, joined
              2026-08-19 admin  Sortable columns
              2026-08-26 admin  Saved filter presets
              2026-09-01 admin  Bulk deactivate / change role

Do not stop   "five admin features since August"
at
Reach         these five are a list-management workflow over one entity, and
              three of them already disagree about which fields a member has
```

Ask the structural question every time a concept reaches four entries: **what
system do these add up to, and has anyone defined it?** The answer is a
hypothesis until it is checked against the code, and the check is usually cheap —
find the place where two of the features disagree, or fail to find it and drop
the claim. `becoming.md` has the crossings worth recognizing and the evidence
each one needs.

## Activity versus progress

The question that makes a trajectory worth keeping:

> Since the last milestone, what changed for someone using this system?

Milestones are outcomes — *core workflow usable end to end*, *first real user*,
*deployed*, *billing live*. Twenty entries and no milestone is not automatically
bad: infrastructure phases look exactly like that, and so do rewrites. It earns
a mention only when the entries are also *radial* or *corrective*, i.e. the work
is fanning outward or chasing itself.

The sharpest version of the question is about sequencing: **is the work
happening on top of something that does not finish?** Three entries of interface
refinement while the path underneath still has a button wired to nothing is not
a productivity observation, it is a recommendation about order — see the
sequencing section of `next-action.md`.

Never present this as a scolding, and never present it as a metric. There is no
number here. The observation is:

> Most of the last month has gone into the tickets screen, and none of it into
> the part that closes a ticket. If that is deliberate, ignore me.

## Beware the pattern that is just a job

The commonest false positive: reading focused, competent work as a pattern.

- A backlog being worked through produces varied, unrelated entries. That is a
  backlog, not drift.
- A feature being built produces many entries on one concept. That is a feature,
  not accumulation.
- A migration produces long corrective runs. That is a migration.
- Someone learning a codebase asks many "how does X work" questions. That is
  onboarding.

Before calling anything a pattern, ask: *what is the ordinary explanation, and
have I ruled it out?* If the ordinary explanation is live, the pattern has not
cleared the Convergence gate. Say nothing, and record it.

## Sessions

Patterns that span sessions are worth more than patterns inside one. A single
session with four permission edits is one task; four permission edits across
three weeks is a shape. Weight accordingly, and note the dates in the finding —
*"three times since August"* is a sentence the user can check against their own
memory, which is what makes them believe the rest of it.

## Inherited history

On a codebase that arrives with the pattern already in it, git history is the
trajectory. It counts, with the same evidence rules:

```bash
git log --oneline --since='6 months ago' -- src/permissions.ts
git log --format='%s' -n 100 | grep -icE 'fix|hotfix|revert'
git log -S'isApproved' --format='%h %ad %s' --date=short
```

Commit messages describe intent as remembered at commit time; treat them as
`OBSERVED` for *what changed* and `INFERRED` for *why*. A repository with six
"fix duplicate X" commits has handed you a corrective run for free, and the
first session can legitimately raise it — the recurrence gate does not care who
generated the instances.
