# Planning: milestones, tickets, decisions

## Contents

- The ticket file
- Acceptance criteria
- Slicing
- Milestones
- Decisions
- Re-planning

How a spec becomes `plan.md` and `tickets/T-nnn.md`. Everything here serves one
test: can a single session pick up this ticket, build it, and prove it, without
asking what it means?

## The ticket file

Copy `templates/ticket.md`. The frontmatter is the shared model other skills
read (`delivery-lead`, `proof-driven-dev`); do not add or rename keys other than
the planner-owned `synced` block.

| Field | Rule |
| --- | --- |
| `id` | `T-001`, `T-002`… in plan order. Permanent; never reused, even after `dropped` |
| `title` | The outcome as a user sees it: *Customer can reset password by email*. Not the task (*Add reset endpoint*) |
| `milestone` | `M1`, `M2`… from `plan.md` |
| `status` | `backlog · ready · in_progress · in_review · blocked · done · dropped` |
| `depends_on` | Ids that must be `done` before this can start. `[]` when none |
| `tracker_ref` | The tracker's id or URL once synced (`PROJ-17`, a card id, `#42`). Empty for `local` and before the first sync |
| `labels` | Free labels; `decision-needed` is reserved for rule 9 |
| `synced` | Planner-owned. What local and tracker last agreed on: `at`, `status`, `title`. Empty until the first sync |

Body sections, in this order: `## Why` (one to three sentences, the user's
reason, not the implementation), `## Acceptance criteria` (numbered),
`## Notes / decisions` (links, the open question, what was decided and by whom).

### `ready` versus `backlog`

- `ready`: fully specified, no open decision. It may still wait on
  `depends_on`; whoever picks tickets checks that.
- `backlog`: known work not yet specified enough to build (usually a later
  milestone, or a follow-up noticed during another ticket).

## Acceptance criteria

Each criterion is one observable behavior: a starting state or input, an
action, and a result a check can see. They are handed to ProofBuild as its
numbered requirements without rewording, so write them the way a test would
assert them.

| Weak | Observable |
| --- | --- |
| Password reset works | Requesting a reset for a registered email sends one email containing a single-use link |
| Handle errors | Requesting a reset for an unknown email shows the same confirmation message and sends nothing |
| Secure tokens | A reset link used once, or older than the expiry the spec states, shows "link expired" and changes nothing |
| Fast search | *(no number in the spec)* → a decision: what response time counts as acceptable? |

Three to seven criteria. More than seven is a split signal. Fewer than three
often means the negative cases are missing.

### Negative cases to name

Go through these for every ticket and write down each one that applies:

- invalid or missing input
- the actor without permission (another tenant, a logged-out user, a non-admin)
- the empty state (no items yet)
- the duplicate (submitted twice, retried, double-clicked)
- the expired or already-used thing (link, invite, slot)
- the limit (maximum length, maximum count, a full calendar)
- the external dependency failing (email not sent, payment declined)

If none applies, write `No negative case: <why>` in the notes, so the absence is
a decision and not an omission.

## Slicing

A vertical slice goes through every layer it needs (UI, route, logic, storage)
and ends in behavior someone can observe. A horizontal slice ("create all the
tables") ends in nothing observable, so nothing can be proven.

Split a ticket when any of these is true:

| Signal | Split by |
| --- | --- |
| The title has *and* in it | One ticket per outcome |
| More than seven acceptance criteria | The happy path first; the variations next |
| Several user roles | One role per ticket, the most common first |
| Several input sources or formats | One source first, the rest after |
| A new subsystem *and* a feature on it | The smallest version of the subsystem inside the first feature that needs it |
| It cannot be proven without another unfinished ticket | Make the dependency explicit, or merge the two |

Do not split below observability: *"add the column"* on its own is not a
ticket, it is a step inside one.

## Milestones

`plan.md` lists milestones in order. Each has an outcome, a *done when* line,
and its tickets.

- **M1 is a walking skeleton, deployed.** The thinnest path through the whole
  system, running where users will reach it (staging at least): a real page,
  served by the real stack, reading from the real database, shipped by the real
  pipeline. It proves the architecture and the deploy before any feature depends
  on them. If `release-engineer` is installed, the deploy ticket is its work.
- Each later milestone is a capability a user gains. Order by what unblocks the
  most, then by what the spec says matters first.
- A milestone is complete when every ticket in it is `done` or `dropped`.

```markdown
# Delivery plan

Source: docs/spec.md (read 2026-09-28)

## M1 — Walking skeleton deployed
Outcome: the home page is served from staging by the real stack and database.
Done when: T-001..T-003 are done and the staging URL answers.
Tickets: T-001, T-002, T-003

## M2 — Customers book and cancel
...

## Open decisions
- D1 — Can a customer cancel inside 24 hours? Spec is silent. Blocks T-007.
```

## Decisions

A business rule the spec does not decide (a limit, a refund policy, who may see
what, what happens on conflict) becomes a decision:

1. Add `Dn — <the question>` under *Open decisions* in `plan.md`, with the
   tickets it blocks.
2. Set each affected ticket `status: blocked`, add the label `decision-needed`,
   and write the question in its notes.
3. Ask the human the questions together, once, after the plan is shown.
4. When answered: write the answer and who gave it under the decision, move it
   to *Decided*, update the criteria, set the tickets `ready`, and sync.

If `project-compass` has already recorded the rule in `.project-compass/`, use
its wording and link to it instead of asking again.

## Re-planning

When the spec changes, re-plan against the existing files: keep every id,
update tickets whose meaning changed (the change goes through sync like any
other edit), add new ids for new work, and move work that no longer applies to
`dropped` with the reason. Never renumber.
