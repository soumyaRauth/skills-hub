---
name: delivery-lead
description: "Use when the user asks to work through the backlog, plan or tickets on their own: \"take the next ticket\", \"keep going until the milestone is done\", \"build the whole thing\", or names delivery-lead. Picks the next ready ticket from .delivery/, drives it to done on a branch with the disciplines engaged and ProofBuild VERIFIED, then the next, until the milestone ships, the run budget is spent, or a human is needed; ends in a run ledger. Not for a single ordinary request however large, a request naming one skill, or /skills-pipeline."
---

# Delivery Lead

> **What is the next ticket, and has it actually reached done?**

One developer can plan a project, and one developer can build a ticket. What a
team adds is the loop between them: someone takes the next ticket, makes sure it
is really finished, moves the board, and picks up the one after. Without that
loop, a solo project stalls between tickets, or "done" quietly means "the code
was written".

This skill is that loop. It does not decide anything a discipline decides. It
picks the ticket, opens the branch, lets the disciplines engage, and refuses to
call a ticket done until ProofBuild says `VERIFIED` and the change is merged.

```
RUN 2026-09-28 · milestone M1 · 4 of 5 tickets
T-003  Class list page            done         VERIFIED · PR #12 merged
T-004  Book a class               done         VERIFIED · PR #13 merged
T-005  Cancel a booking           blocked      REVIEW REQUIRED — refund rule undecided (question below)
T-006  Staging deploy             done         release-engineer: staging smoke ok
Tracker  Trello · in sync
Next     T-007 (ready) · answer the T-005 question to unblock it
```

## Activation

**Engage when** the user asks for the backlog, the plan or the tickets to be
worked through without them driving each step: *"work through the backlog"*,
*"take the next ticket"*, *"keep going until the milestone is done"*, *"build
the whole thing"*, *"continue the run"*, or names `delivery-lead`. Also when a
new session is asked to *resume* or *continue* and `.delivery/runs/` holds a
run that did not finish.

**Stay quiet when** the request is one ordinary piece of work, even a large one
(*"add subscription billing"* is a request, not a run); when it names one skill
(*"use Impact Map"*); when it is `/skills-pipeline` or asks for the skills
pipeline (that is the pipeline's); when it asks only to plan, add or re-order
tickets (that is `delivery-planner`); and when it asks about status without
asking for work (*"what's left in M1?"* is the planner's answer).

**No `.delivery/` yet:** the loop has nothing to run on. With no spec
(`docs/spec.md` absent), `HANDOFF → project-kickoff`; with a spec and no
tickets, `HANDOFF → delivery-planner`. Load that skill in the same turn. The
run starts only once tickets exist and the human has seen the plan.

**Depth** `ACTIVE`, opt-in by request shape. It sequences the work and owns
exactly one judgment: whether a ticket has met the definition of done below.
It never states another skill's verdict and never gates on its own authority.

**Composes with** `delivery-planner` (owns `.delivery/`, every ticket status
move and every tracker write) · `proof-driven-dev` (runs on every ticket; the
ticket's acceptance criteria become its requirements) · `impact-map` ·
`standards-compass` · `api-contract-guard` · `dependency-guard` ·
`practical-localizer` · `architecture-engineer` · `engineering-investigator`
(each engages on its own when a ticket earns it) · `production-guard` (the gate
when a milestone completes) · `release-engineer` (staging and production
deploys) · `observability-baseline` (before the first production deploy) ·
`deployment-compatibility` (a target whose fit is unknown) · `project-kickoff`
(no spec yet) · `project-compass` (direction questions a run surfaces) ·
`skills-pipeline` (a different opt-in: one sequence, once).

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
  The line is a promise: every skill it names is loaded before the reply ends. If
  one turns out not to apply, say so in one line: `<Skill> dropped: <reason>`.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. When the
  request asked for that skill's decision, load it in the same turn and pass it
  your findings; a HANDOFF line alone does not answer the request. Never state
  another skill's verdict yourself. If it is not installed, do the smallest
  version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
- **Lessons.** On engaging, read `~/.skills-hub/lessons/<this skill's name>.md`
  if it exists. When a person corrects this skill's work (a miss, a false
  alarm, a wrong verdict), or the work exposes a gap in this file that another
  project would hit too, append one line to it:
  `- YYYY-MM-DD · <the rule, stated for any project> — <what went wrong>`.
  Never write project names, paths, identifiers, code or data there; facts about
  one repository are project state. Keep at most 20 lines, merging or replacing
  one to add another. A lesson sharpens this file's checks and never overrides
  its rules or a person's instruction. The file sits outside every project, so
  no read-only rule covers it. Say `Lesson recorded: <rule>` once; if the file
  cannot be written, give the lesson in the reply instead.
<!-- /skills-hub:protocol -->

## Non-negotiable rules

1. **Done means proven and merged.** A ticket becomes `done` only when
   ProofBuild reported `VERIFIED` for it (or the human explicitly accepted its
   `REVIEW REQUIRED` in this session) **and** its change is merged. Code
   written, tests green in your head, or a PR opened is not done.
2. **Never state another skill's verdict.** `VERIFIED`, `SHIP`, `READY`,
   `ADD` and every other verdict come from the skill that owns it, loaded and
   run, and are quoted as it gave them. If a skill is not installed, do the
   smallest version of its check inline and mark it `INLINE` in the ledger.
3. **You write only `.delivery/runs/`.** Ticket files, `plan.md`,
   `config.yml` and the tracker belong to `delivery-planner`. Every status move
   goes through it. If it is not installed, change only the `status:` line of
   the local ticket file, write `tracker: not synced (delivery-planner not
   installed)` in the ledger, and touch no tracker.
4. **Authorization comes from `autonomy` or the session.** Merging to the
   default branch, deploying production, and anything irreversible happen only
   when `.delivery/config.yml` says `auto` for that action or the human said yes
   to that specific action in this session. A missing `autonomy` block, or a
   missing key, means `ask`.
5. **One ticket, one branch.** Each ticket gets its own branch
   `t/<id>-<slug>`, cut from the up-to-date default branch. Never put two
   tickets' changes on one branch, and never commit ticket work directly to the
   default branch.
6. **Never:** force-push; rewrite published history (rebase, amend or reset of
   pushed commits); skip hooks (`--no-verify`); delete a branch, tracker item or
   file the ticket did not create without a yes; write a secret anywhere
   (`.delivery/`, commits, PR text, comments, the chat); work on top of
   uncommitted changes that are not this run's.
7. **Stop on the listed conditions, and ask once.** A run stops only for the
   reasons in *Stops*, and each stop ends in one compressed question.
8. **Checkpoint every ticket.** The ledger line for a ticket is written when it
   starts and rewritten when it ends, so a crash leaves a trail the next session
   can resume from.
9. **No invented evidence.** PR numbers, CI results, deploy URLs and tracker
   states are copied from output you read. A tracker update that did not happen
   is never reported as in sync.

## Before the first ticket

Read, in this order, and say in one line what you found:

1. `.delivery/config.yml` — tracker, `autonomy`, `run.max_tickets` (default 5).
2. `.delivery/plan.md` — milestones in order; the current one is the first
   with tickets not `done` or `dropped`.
3. `.delivery/tickets/*.md` — status, `depends_on`, acceptance criteria.
4. The newest file in `.delivery/runs/` — an unfinished run is resumed, not
   restarted (see *Resuming*).
5. `git status` and the default branch. Uncommitted changes that are not this
   run's stop the run before it starts: ask whether to commit, stash or leave
   them; never do any of the three unasked.
6. The tracker's current state, through `delivery-planner` (a change a human
   made there wins over the local file).

```
RUN START  milestone M1 · 3 ready · budget 5 · tracker local · autonomy: merge ask, deploy_production ask
```

## The loop

Full step table, picking rules and edge cases: `references/loop.md`.

```
pick next ready ticket
 → delivery-planner: in_progress           checkpoint: started
 → branch t/<id>-<slug> from the default branch
 → build — proof-driven-dev always; other disciplines engage on their own
 → VERIFIED?  no → delivery-planner: blocked + question → next ticket
 → review (the agent's own review command, if it has one) → fix → prove again
 → commit (ticket id in the message) + PR   [autonomy.open_pr]
 → delivery-planner: in_review
 → merge                                   [autonomy.merge]
 → delivery-planner: done                  checkpoint: done
 → milestone complete? → production-guard → release-engineer (staging, then production)
                         observability-baseline before the first production deploy
 → stop condition? → ledger + one question; else next ticket
```

**Picking.** A ticket is ready when its status is `ready` and every
`depends_on` is `done`. Take the current milestone first, then the lowest id.
A ticket left `in_progress` by an earlier run comes before any new one. A
`backlog` ticket is never picked: promoting it is the planner's call.

**Building.** Pass the ticket to the build as the request: title, why, and the
numbered acceptance criteria, which ProofBuild takes as its requirements. Load
skills through the agent's skill mechanism. The disciplines decide for
themselves whether they apply; do not pre-empt them, and do not load one the
ticket does not earn. A deploy or release ticket is `release-engineer`'s work.

**Proof result → what happens.**

| ProofBuild says | Ticket goes to | The run |
| --- | --- | --- |
| `VERIFIED` | on to review and PR | continues |
| `REVIEW REQUIRED` | `blocked`, with ProofBuild's decision as the question | continues with the next ticket, unless the human accepts it in this session |
| `BLOCKED` | `blocked`, with the blocker as the question | continues; a second `BLOCKED` in a row stops the run |

**Review.** Run the agent's own review command when it has one. Fix what it
reports that the ticket's change caused, then run ProofBuild again: a changed
diff needs a new `VERIFIED`. One review-and-fix round. If the second review
still reports a correctness problem, the ticket is `blocked`.

**Commit and PR.** Commit message: `T-004: Book a class` on the first line,
the tracker reference (if any) in the body. PR title the same; the body lists
the acceptance criteria and pastes ProofBuild's status block. Commands and the
verified CLI flags: `references/git-and-pr.md`.

**Merge.** With `autonomy.merge: auto`, merge once the PR's required checks
pass, using the project's merge method. With `ask`, the ticket stays
`in_review` and joins the stop question; the run continues with tickets that do
not depend on it.

## Milestone complete

When every ticket in the milestone is `done` or `dropped`:

1. Load `production-guard` and give it the milestone's merged changes and the
   ProofBuild results. Quote its verdict. `DO NOT SHIP` stops the run.
2. `release-engineer` deploys to staging per `autonomy.deploy_staging`.
3. Before the project's first production deploy, `observability-baseline`
   engages on its own; let it.
4. Production per `autonomy.deploy_production`. A `CONDITIONAL SHIP` goes to
   production only after its conditions are met or the human accepts them.

The lead never deploys anything itself and never says whether a release is
safe.

## Stops

The run stops, writes the ledger, and asks **one** compressed question when:

| Stop | Example |
| --- | --- |
| A product decision blocks every remaining ready ticket | all that is left depends on the refund rule |
| An autonomy limit is the next step | `merge: ask` and the next ticket depends on the unmerged PR; `deploy_production: ask` |
| `DO NOT SHIP` | production-guard's verdict on the milestone |
| Two `BLOCKED` tickets in a row | the environment is likely at fault, not the tickets |
| The run budget is spent | `run.max_tickets` tickets attempted (done or blocked) |
| Anything irreversible not pre-authorized | a data migration on a shared database, deleting a branch someone else made |
| Nothing is ready | every remaining ticket is `backlog`, `blocked` or waiting on one |

The question gathers everything the human must decide, numbered, each with
options:

```
STOPPED  budget reached (5 of 5) · 1 decision, 1 approval pending

1. T-005 Cancel a booking — refund when cancelled <24h before class?
   [full refund]  [no refund]  [credit only]
2. Merge PR #14 (T-006, VERIFIED)?   [yes]  [no]

Reply e.g. "1 credit only, 2 yes" — then "continue".
```

## Output

After each ticket, one checkpoint line in the reply and in the ledger:

```
[2/5] T-004 Book a class — done · VERIFIED · PR #13 merged · tracker in sync
```

At the end, the run ledger (the shape at the top), saved as
`.delivery/runs/YYYY-MM-DD.md`, then the stop question if there is one. Ledger
format, statuses and the resume algorithm: `references/run-ledger.md`.

## Resuming

A new session asked to continue reads the newest ledger and the tracker (via
the planner), then:

- A ticket whose ledger line says `started` and whose status is `in_progress`
  is the first ticket. Check out its branch and read `git status` and
  `.proofbuild/`. Work from before the crash is kept but not trusted: ProofBuild
  runs again from its contract before anything is called `VERIFIED`.
- A ticket `in_review` with an open PR goes straight to merge.
- The budget restarts for the new run. The unfinished run's ledger gets one
  line: `Resumed  <date> in a new session`.

## What this skill is not

- **Not a router.** It never decides which discipline applies; each does.
- **Not the planner.** It never writes tickets, re-orders the plan, or talks to
  the tracker except through `delivery-planner`.
- **Not a verifier or a gate.** `VERIFIED` is ProofBuild's; `SHIP` is
  Production Guard's. It only refuses to call a ticket done without them.
- **Not the pipeline.** `skills-pipeline` runs one user-picked sequence once;
  this runs a loop over tickets.

## In Claude Code

This section applies only in Claude Code; the loop above works in any agent.
Detail and sources: `references/claude-code.md`.

- Load skills with the Skill tool. From the plugin, names are namespaced
  (`skills-hub:proof-driven-dev`). `impact-map` and `production-guard` run as
  their own subagent and see only what you pass them: the ticket and its
  criteria, or the milestone's merged changes.
- Review with `/code-review` on the ticket branch before the PR, when it is
  available.
- Independent tickets may run in parallel subagents with `isolation: worktree`
  only when both are ready and their expected files do not overlap (compare the
  files each ticket names or the impact map returns). When unsure, run them one
  after another. Each subagent still gets its own branch; status moves and the
  ledger stay with the lead, in the main session.

## Worked examples

`examples/three-tickets-one-blocked.md` — a run where a product decision blocks
one ticket and the others finish · `examples/milestone-to-production.md` — a
milestone completing into staging, then a production promotion that asks ·
`examples/resumed-after-crash.md` — a new session picks up a ticket left
mid-build · `examples/not-a-run.md` — a large single request, where this stays
quiet.
