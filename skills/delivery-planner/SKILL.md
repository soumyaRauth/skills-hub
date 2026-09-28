---
name: delivery-planner
description: Use when asked to plan the work, break a spec or large feature into milestones and tickets, set up or connect a tracker (Jira, Trello, Nextcloud Deck, GitHub, GitLab, Linear, or local files), create, update, move or close tickets, or asked what is left; and passively when work starts or finishes in a repository that keeps .delivery/. Writes vertical-slice tickets with numbered acceptance criteria and keeps the tracker in sync without duplicates or lost human edits. Not for a single small task in a project without .delivery/, or for creating a tracker or tickets nobody asked for.
---

# Delivery Planner

> **What is the work, in what order — and does the tracker say what is really true?**

A spec is not a plan, and a plan in someone's head is not a board. Two things go
wrong for a developer working alone. The work gets cut horizontally ("build the
database layer", "build the API"), so nothing can be shown working until
everything is done. And the tracker drifts: cards stay in *To Do* while the code
ships, a retried script creates the same ticket twice, an agent overwrites the
column a human just moved a card into.

This skill does two jobs. It **plans**: milestones in order, the first one a
walking skeleton deployed, and tickets that are vertical slices a single session
can build and prove, each with numbered acceptance criteria. And it **syncs**:
the local ticket files in `.delivery/` and whichever tracker the project uses
(Jira, Trello, Nextcloud Deck, GitHub, GitLab, Linear, or none) are kept in
agreement, at fixed moments, without being asked, and never by guessing.

```
PLAN     docs/spec.md → 3 milestones · 11 tickets · 1 open decision
M1       Walking skeleton deployed        T-001 T-002 T-003
M2       Customers book and cancel        T-004 … T-008
M3       Owner sees the week              T-009 T-010 T-011
BLOCKED  T-007 on D1: can a customer cancel inside 24 hours? (spec is silent)
TRACKER  trello · via rest · board "Salon" · 11 created · 0 already there
```

## Activation

**Engage when** someone asks to plan the work, break a spec or a large feature
into milestones or tickets, set up or connect a tracker, create, update, move
or close tickets, or asks *what's left?* / *where are we?*. Also engage
**passively** in a repository that keeps `.delivery/` whenever one of the fixed
sync moments happens (a ticket is picked up, a PR is opened for it, its proof
comes back, it is merged), whether or not anyone mentions the tracker.

**Stay quiet when** the request is a single small task in a project without
`.delivery/` (a bug fix, a feature that fits one session, a rename): do the work,
no plan, no ticket. Stay quiet for questions unrelated to planning or ticket
state. The words *ticket*, *board* or *issue* in a sentence are not a request to
plan. Never create a tracker, a board, a column or a ticket the human did not
ask for, and never set up `.delivery/` on your own initiative: offer it in one
line at most.

**Depth** `ACTIVE` when asked to plan, set up, or change tickets.
`PASSIVE` for sync moments: the move happens (within `autonomy`) and the reply
carries at most one line, `Tracker: T-004 → In Review (PR #31)`. `CONSULT` for
*what's left?*: a short answer from the files and the tracker, nothing built.
Never `GATING`: a ticket's readiness is ProofBuild's call, shipping is
Production Guard's.

**Composes with** `project-kickoff` (writes `docs/spec.md`, which this skill
plans from) · `delivery-lead` (runs the loop over the tickets this skill writes;
it asks this skill for every status move) · `proof-driven-dev` (a ticket's
acceptance criteria become its numbered requirements; `VERIFIED` is what moves a
ticket to done) · `project-compass` (an undecided business rule found while
planning is a direction question, and compass may already have recorded it) ·
`architecture-engineer` (a ticket that cannot be sliced until a boundary is
decided) · `release-engineer` (the walking skeleton's deploy) ·
`dependency-guard` (a community MCP server for a tracker is a dependency to
decide on, not to install by reflex).

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

1. **Never claim a tracker update that did not happen.** A write is reported
   only after the tracker's response was read and it succeeded. A failure,
   a timeout or an unreachable tracker is reported as exactly that, and the
   change waits in the local file (rule 7).
2. **Read before every write.** Fetch the tracker item before changing it. A
   change a human made there (status, title, labels, text) wins and is pulled
   into the local file. You never overwrite it.
3. **Never duplicate.** Every tracker item carries its local id as a title
   prefix, `[T-004] …`. Before any create, look for that marker; if it exists,
   link to it instead. A retried run creates nothing twice.
4. **Never delete.** Not a card, not an issue, not a column, not a local ticket
   file. Work that will not happen moves to `dropped` with a comment saying why.
5. **Every move carries a comment**: what changed and the evidence (ProofBuild's
   status line, the PR link, the deploy URL). A bare column change is a claim
   with nothing behind it.
6. **A credential lives in one place and is never shown.** The default home is
   `.delivery/.env`: git-ignored (proved with `git check-ignore`) and `chmod 600`
   *before* anything is written into it. `config.yml` holds only env var names
   and `auth_file`. Commands load the file inside the same command
   (`set -a; . .delivery/.env; set +a; curl …`). Never `cat`, `echo`, `grep` or
   `set -x` it; never put a token in a comment, a commit, a file other than
   `.delivery/.env`, or any output shown to the human. A token pasted into chat
   is written to the file, never repeated back, and gets one line suggesting
   rotation.
7. **The local file is the working copy; the tracker is where humans look.**
   When the tracker is unreachable, keep working on the local files, say
   `tracker: out of sync`, and reconcile on the next sync. Work never stops
   because a board is down.
8. **Autonomy is the human's, set once.** Tracker writes happen only as
   `autonomy` in `.delivery/config.yml` allows, or on an explicit yes in the
   session. `ask` means: state the change in one line and wait.
9. **Never guess a business rule.** A ticket that depends on a rule the spec
   does not decide is `blocked` with the question written down, not written
   around a guess.
10. **Say which access path is in use**: `via mcp`, `via cli (gh)`, `via rest`,
    or `local`, every time the tracker is touched.

## State: `.delivery/`

This skill owns `.delivery/` except `runs/`, which `delivery-lead` writes.
Everything in it except `.env` is meant to be committed; git history is the
backup of every ticket's earlier text. `.env` is git-ignored and never leaves
the machine.

```
.delivery/
├── config.yml            tracker + status mapping + autonomy (templates/config.yml)
├── .env                  credentials, git-ignored, mode 600 (only when the token-file path is used)
├── plan.md               milestones in order, each an outcome; open decisions
├── tickets/T-001.md      one file per ticket, canonical local copy (templates/ticket.md)
└── runs/                 delivery-lead's run ledgers; read, never written here
```

Ticket statuses are neutral: `backlog · ready · in_progress · in_review ·
blocked · done · dropped`. `status_map` in `config.yml` maps each to the
tracker's column, list, stack or workflow state. The ticket file's `synced`
block records what both sides last agreed on; it is how a human's edit is told
apart from a local one (`references/sync.md`).

## First run: setup

Setup happens only when someone asked for tickets or a tracker. You are the
guide: a conversation that **acts after each answer**, one step at a time, and
ends with ticket management that runs on its own. The human never edits
`config.yml` by hand and never pastes a token into chat. Nothing is created in
the tracker until step 6 reports `CONNECTED`.

`scripts/tracker.py` (Python 3 stdlib) does the deterministic parts: `secret`,
`whoami`, `boards`, `columns`, `create-board`, `create-column`. Each prints one
JSON object and never a secret. Run it from the repository root as
`python3 <skill dir>/scripts/tracker.py …`. Per-tracker facts (credential URL,
least scope, MCP command) are in `references/trackers.md`, *Connect*.

**Step 1 · Which tracker.** Detect first, never printing a value: tracker MCP
tools already in this session, `.mcp.json`, `gh auth status`, `glab auth
status`, `acli`, env vars (`[ -n "$JIRA_API_TOKEN" ] && echo set`), an existing
`.delivery/.env` (exists or not; never read aloud), and the git remote.

```
Where should tickets live? I found: gh logged in as dana · origin github.com/acme/salon
  1 jira  2 trello  3 deck (Nextcloud)  4 github  5 gitlab  6 linear  7 local (files only)
```

**Step 2 · Connect.** Offer only the chosen tracker's options, best first:

```
How should I connect to Jira?
  a) Atlassian's official MCP server — you sign in in the browser, no token stored  [recommended]
  b) An API token, which you type into a hidden prompt in your own terminal
  c) Already set up: JIRA_EMAIL/JIRA_API_TOKEN in your shell, or `acli` logged in
```

- **a) Official MCP** (only where an official server with its own sign-in
  exists; see *Connect*): on a yes, run the verified command yourself, e.g.
  `claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp`
  (outside Claude Code, print the equivalent for the human's client). Then ask
  for the one thing only they can do: `Run /mcp, pick "atlassian", and finish
  the sign-in in your browser. Reply "done".` Verify by calling one of the
  server's read tools. A community MCP server is never added without a
  `dependency-guard` decision.
- **b) Token via the helper** (default where no official MCP exists): give the
  exact command and wait. The script prints where to create the credential and
  the least scope, git-ignores `.delivery/.env` and proves it with `git
  check-ignore` *before* any prompt, reads each value with hidden input, writes
  the file with mode 600, and immediately runs `whoami`.

  ```
  Run this in your own terminal (not here), from the repository root:
    python3 <this skill's directory>/scripts/tracker.py secret jira
  It shows where to create the token and asks for it with hidden input.
  Reply "done" when it prints "ok": true.
  ```
  Write the real absolute path of the skill directory into the command. Then
  run `tracker.py whoami` yourself and read the JSON.
- **c) Existing env var or CLI login**: record the names; nothing is written.
- **A token pasted into chat anyway:** never repeat it. Git-ignore
  `.delivery/.env`, confirm with `git check-ignore -q .delivery/.env`, write the
  value there with mode 600 (a heredoc into the file; never an `echo` of the
  value), say once `That token passed through this conversation; rotate it when
  convenient.`, and continue. Never refuse to proceed over it.

**Step 3 · Which board.** Run `tracker.py boards` (or the MCP server's list
tool) and show the real ones:

```
Your Deck boards: 1 Salon (12) · 2 Personal (4) · 3 Website (9)
Pick one, or: n) create a new board "salon-booking"
```

Create only on an explicit yes to that name (`tracker.py create-board <name>`).
Where the API or the account's rights do not allow it (a Jira project needs a
Jira admin; a Linear key may lack team-creation rights), the script says so:
pass that on and ask for an existing one.

**Step 4 · Columns.** Run `tracker.py columns <board>`, match names to the
neutral statuses, and propose the map:

```
Proposed mapping for "Salon":
  ready → To do · in_progress → Doing · done → Done
  missing: in_review, blocked
Create lists "Review" and "Blocked" on the board? (yes / map them to existing ones)
```

On a yes, `tracker.py create-column <board> <name>` for each (Linear: add
`--type started`, or `completed`/`canceled`/`unstarted`/`backlog` to match).
Jira statuses belong to the workflow: the script refuses and says a Jira admin
adds them; map to an existing status or use a label.

**Step 5 · Autonomy.**

```
What may I do without asking?  [defaults]
  create tickets [auto] · move tickets [auto] · open PR [auto]
  merge [ask] · deploy staging [auto] · deploy production [ask]
Reply "defaults" or change any of them.
```

**Step 6 · Write the config and prove it.** Write `.delivery/config.yml` from
`templates/config.yml` (`type`, `via`, `project`, `url`, `auth_env` names,
`auth_file: .delivery/.env` when used, `status_map`, `autonomy`). Then run the
read-only proof, `whoami` and `columns` against the configured board, and
report:

```
CONNECTED  deck via rest as Dana Reyes · board Salon (12) · 5 of 7 statuses mapped
```

On failure, create nothing and say exactly what failed and what fixes it (the
script's `error` and `fix` fields): `401` the credential is wrong or expired
(create a new one, Connect step 1) · `403` a scope or project permission is
missing (Connect step 2) · `404` wrong board, project or URL · `unreachable`
network or host. Until `CONNECTED`, plan into local files and report
`tracker: not connected — <what failed>`. After it, the fixed moments run
within `autonomy` with no further setup.

Later tracker commands load the file inside the same command and never print
it: `set -a; . .delivery/.env; set +a; curl -sS -u "$JIRA_EMAIL:$JIRA_API_TOKEN" …`.

## Planning

Source, in order: `docs/spec.md`, the request, the issue or document the human
points to. Read the code that exists; a plan for a repository with a working
login does not re-plan login. Then:

1. **Milestones are outcomes, in order.** M1 is always a *walking skeleton
   deployed*: the thinnest end-to-end path (one screen, one route, one table,
   the deploy) running where users will reach it, even if it does almost
   nothing. Each later milestone is something a user can do that they could not
   before.
2. **Tickets are vertical slices.** Each one cuts through every layer it needs
   and ends in behavior someone can observe. Size: one session can build it and
   prove it. Split rules and the too-big signals are in `references/planning.md`.
3. **Numbered, observable acceptance criteria.** Three to seven per ticket,
   each a behavior a check can prove: an input, an action, an observable
   result. They become ProofBuild's requirements verbatim, so write them that
   way.
4. **Name the negative cases.** Wrong input, no permission, the empty state,
   the duplicate, the expired link. At least one criterion per ticket says what
   must *not* happen, unless the ticket genuinely has none, and then say so.
5. **Dependencies are explicit.** `depends_on` lists ids; no cycles; a ticket
   never depends on a later milestone.
6. **Undecided rules block, they are not guessed.** Record the question as a
   decision (`D1`) in `plan.md`, set the ticket `blocked`, label it
   `decision-needed`, and put the question in its notes. The rest of the plan
   proceeds.
7. **Ids are permanent.** `T-001`, `T-002`… in plan order, never reused, not
   even after a ticket is dropped.

Write `plan.md` and the ticket files, then sync (if `create_tickets` allows).
Show the plan in the shape above, not the ticket bodies; they are in the files.

## Sync

### The fixed moments (passive, within autonomy)

| Moment | Local status | Comment carries |
| --- | --- | --- |
| Ticket picked up (by a person or `delivery-lead`) | `in_progress` | branch name |
| PR opened for it | `in_review` | PR link (also attached as a link where the tracker supports it) |
| ProofBuild `VERIFIED` and the PR merged | `done` | the `VERIFIED` line and the merge commit or PR |
| ProofBuild `BLOCKED`, or `REVIEW REQUIRED` not yet accepted | `blocked` | the status line and the question for the human |
| The human accepts `REVIEW REQUIRED` and it is merged | `done` | "accepted by <human> in session", the PR |
| Work will not happen | `dropped` | why, and who decided |

`done` needs both halves: proof and merge. A merged PR without `VERIFIED` is
`in_review` with a comment saying proof is missing; a `VERIFIED` branch that is
not merged is still `in_review`.

When `autonomy.move_tickets` is `auto`, make the move and add one line to the
reply. When it is `ask`, write the move as one line and wait:
`Move T-004 to In Review with PR #31? (move_tickets: ask)`.

### The algorithm

Every write goes through the same steps (`references/sync.md` has the full
procedure and the conflict table):

```
load local ticket → find tracker item (tracker_ref, else search the [T-004] marker)
→ read it → compare with the synced block → pull human changes → write only what
is still different → read back → update synced block → report
```

### Asked to sync, or on the next run after an outage

Reconcile every ticket: pull, then push, then report.

```
TRACKER  deck · via rest · board "Salon" (id 12)
PUSHED   T-004 in_progress → in_review (PR #31)
PULLED   T-006 ready → in_progress (moved on the board by a human; local updated)
CREATED  none · already there: 11
PENDING  none
```

`PENDING` lists every local change the tracker has not received. It is never
empty when the tracker was unreachable.

## "What's left?"

Answer from the local files after a pull (or say the pull failed):

```
M1  Walking skeleton deployed   3/3 done
M2  Customers book and cancel   2/5 done · T-006 in review · T-007 blocked on D1
M3  Owner sees the week         0/3 · not started
NEXT      T-008 (ready, dependencies done)
DECISION  D1: can a customer cancel inside 24 hours?
```

Counts come from files actually read. No estimates in days unless the human
supplied them.

## Adding another tracker

A tracker is supported once `references/trackers.md` has its section (the seven
operations, each checked against the vendor's docs) and `scripts/tracker.py`
covers its setup calls. Until then, use `local` and say the tracker is
unsupported. *Adding another tracker* in `references/trackers.md` has the list.

## What this skill never does

- Creates a tracker, board, column, ticket or `.delivery/` nobody asked for.
- Deletes anything, locally or in the tracker.
- Overwrites a human's edit in the tracker.
- Moves a ticket to `done` without ProofBuild's `VERIFIED` (or the human's
  explicit acceptance of `REVIEW REQUIRED`) and a merge.
- States another skill's verdict. It records ProofBuild's status line; it does
  not decide it.
- Writes to `.delivery/runs/`. That is `delivery-lead`'s ledger.
- Prints, pastes back or commits a credential, or stores one anywhere but the
  git-ignored, mode-600 `.delivery/.env`.

## References

- `references/planning.md` — the ticket format, slicing heuristics, the walking skeleton, negative cases, decisions
- `references/sync.md` — read-before-write, idempotent create, conflicts, out-of-sync handling, reconciliation
- `references/trackers.md` — per tracker: access order, every operation's endpoint or command, auth, gotchas, MCP servers

Templates: `templates/config.yml` · `templates/ticket.md`. Setup helper:
`scripts/tracker.py`, with its self-check `scripts/test_tracker.py`.

## Worked examples

`examples/guided-setup-deck.md` — first run, end to end: Deck chosen, token
through the helper, board and stacks picked and created, `CONNECTED` ·
`examples/spec-to-jira.md` — a spec planned into milestones and synced to Jira
Cloud · `examples/deck-status-moves.md` — automatic moves on a Nextcloud Deck
board, and a card a human moved, which wins · `examples/tracker-unreachable.md`
— the tracker is down; local continues and reconciles · `examples/whats-left.md`
— a short answer to *what's left?*.
