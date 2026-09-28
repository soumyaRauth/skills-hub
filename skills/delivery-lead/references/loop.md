# The loop, step by step

`SKILL.md` gives the shape. This file is the table to follow when a step is
unclear. Every status move in the table is made by `delivery-planner`; the lead
asks for it and records the result.

## Steps

| # | Step | Who does it | Authorized by | On failure |
| --- | --- | --- | --- | --- |
| 1 | Pick the next ready ticket | lead | — | nothing ready → stop |
| 2 | Status `in_progress` | delivery-planner | `autonomy.move_tickets` | tracker unreachable → keep going on local files, ledger says `tracker: out of sync` |
| 3 | Write the checkpoint `started` line | lead | — | cannot write `.delivery/runs/` → stop; a run without a trail cannot resume |
| 4 | Update the default branch (`git fetch`, then fast-forward only) and cut `t/<id>-<slug>` | lead | — | fast-forward impossible → stop and ask; never reset or force |
| 5 | Build: the ticket is the request; `proof-driven-dev` always | the disciplines | — | see the proof table in `SKILL.md` |
| 6 | Review with the agent's review command, fix, prove again | lead + proof-driven-dev | — | still a correctness problem after one round → `blocked` |
| 7 | Commit, push the branch, open the PR | lead | `autonomy.open_pr` | `ask` → the question; the branch stays local |
| 8 | Status `in_review`, with the PR link | delivery-planner | `autonomy.move_tickets` | as step 2 |
| 9 | Merge when required checks pass | lead | `autonomy.merge` | checks fail → back to step 5 once; `ask` → queued for the question |
| 10 | Status `done`, with the ProofBuild line and the merge | delivery-planner | `autonomy.move_tickets` | as step 2 |
| 11 | Rewrite the checkpoint line | lead | — | — |
| 12 | Milestone complete? → gate and release | production-guard, release-engineer, observability-baseline | `autonomy.deploy_staging`, `autonomy.deploy_production` | `DO NOT SHIP` → stop |
| 13 | Check the stop conditions, then back to 1 | lead | — | — |

`move_tickets: ask` is unusual but allowed. Then every status move joins the
stop question, and the local run continues on files only.

## Picking, precisely

1. Candidates: status `ready`, every `depends_on` id `done`.
2. An `in_progress` ticket from an unfinished run comes first (see
   `run-ledger.md`).
3. Milestone order from `plan.md`: the current milestone's tickets before any
   later one. A later milestone's ticket is picked only when the user said
   *"build the whole thing"* or named that milestone.
4. Within a milestone: the order `plan.md` lists them in, else the lowest id.
5. Never pick `backlog`, `blocked`, `dropped`, or a ticket whose dependency is
   only `in_review`. Merged is what makes a dependency met.

## Slug

Lowercase the title, replace every run of non-alphanumeric characters with one
hyphen, trim hyphens, cut to 40 characters at a hyphen. `T-004 Book a class` →
`t/T-004-book-a-class`. Keep the id exactly as the ticket file writes it.

## A ticket that turns out bigger than itself

When the build finds the ticket needs work another ticket owns, or an
acceptance criterion contradicts the spec, do not widen the branch. The ticket
goes `blocked` with the question, and `HANDOFF → delivery-planner` to split or
amend it. Scope changes are the planner's; the lead only reports them.

## Two tickets' changes

If proving a ticket needs a fix that belongs to another ticket, stop that
ticket (`blocked: depends on <id>`), and let the planner add the dependency.
Never carry the other fix on this branch.

## Budget

`run.max_tickets` in `.delivery/config.yml` (default 5) counts tickets
**attempted** in this run: done and blocked both count; a ticket that only
moved from `in_review` to `done` on resume does not. Deploy steps at a
milestone's end do not count. The human can raise it in the session
(*"do 8 this time"*) for this run only.

## When the human is present

The run is autonomous, not unattended by design. If the human answers a stop
question mid-session, apply the answer (through the planner for anything that
changes a ticket), record it in the ledger's Decisions section, and continue
the same run while budget remains.
