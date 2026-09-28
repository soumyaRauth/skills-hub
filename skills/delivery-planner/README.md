# Delivery Planner

An Agent Skill that turns a spec into milestones and tickets, and keeps
whichever tracker the project uses telling the truth:

> **What is the work, in what order — and does the tracker say what is really true?**

```bash
npx skills add soumyaRauth/skills-hub --skill delivery-planner
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill delivery-planner --agent claude-code --copy
```

---

## Why it exists

A developer working alone, or with an agent, loses the thread in two ways.
The work gets cut into layers (database first, API next, UI last), so nothing
can be shown working until everything is. And the board drifts: cards sit in
*To Do* while the code ships, a retried script creates the same ticket twice,
and an automation overwrites the column a person just moved a card into.

## What it does

```
spec → milestones (M1 = walking skeleton, deployed) → vertical-slice tickets
     → numbered acceptance criteria, negative cases, dependencies
     → undecided business rules become blocked tickets with the question, not guesses
     → .delivery/ files ⇄ your tracker, synced at fixed moments
```

```
PLAN     docs/spec.md → 3 milestones · 10 tickets · 2 open decisions
M1       Walking skeleton deployed        T-001 T-002
M2       Customers book and cancel        T-003 T-004 T-005 T-006
M3       Owner runs the week              T-007 T-008 T-009 T-010
BLOCKED  T-006 on D1: can a customer cancel on the day of the appointment?
TRACKER  jira · via rest · SAL · 10 created · 0 already there
```

**Trackers:** Jira (Cloud and Data Center), Trello, Nextcloud Deck, GitHub
Issues and Projects, GitLab Issues, Linear, or `local` (files only). Tickets are
not tied to any of them: the local files in `.delivery/tickets/` are the working
copy, and the tracker is where people look. It reaches each tracker through an
installed MCP server, then the official CLI, then the REST API, and says which.
[`references/trackers.md`](references/trackers.md) covers every operation, with
the official docs it was checked against, and how to add another tracker.

**Guided setup.** The first run is a conversation that acts after each answer:
which tracker, then the connection (an official MCP server with browser sign-in
where one exists; otherwise a token you type into a hidden prompt in your own
terminal, stored in a git-ignored, mode-600 `.delivery/.env`), then your real
boards to pick from or a new one to create, the columns to map or create, and
the autonomy choices. It ends in a read-only proof,
`CONNECTED deck via rest as Mira Okafor · board salon-booking · 7 of 7 statuses mapped`,
and nothing is created before it. You never edit config or paste a token into
chat. [`scripts/tracker.py`](scripts/tracker.py) (Python stdlib) does the
deterministic parts; `python3 scripts/test_tracker.py` checks it against a
local mock of every tracker.

**Automatic moves.** In a project with `.delivery/`, tickets move without being
asked: picked up → in progress, PR opened → in review, proven and merged → done,
blocked → blocked with the question. Every move carries a comment with its
evidence. How much happens without asking is set once, in
`.delivery/config.yml`.

Five worked examples: [guided first-run setup on Deck](examples/guided-setup-deck.md) · [spec to Jira](examples/spec-to-jira.md) ·
[automatic moves on a Nextcloud Deck board](examples/deck-status-moves.md) ·
[the tracker is down](examples/tracker-unreachable.md) ·
[what's left?](examples/whats-left.md)

## When it activates

When you ask it to plan the work, break a spec or feature into tickets, connect
a tracker, change tickets, or ask what's left, and passively whenever work
starts or finishes in a project that keeps `.delivery/`. It stays quiet for a
single small task in a project without `.delivery/`. See
[Activation](SKILL.md#activation).

## What it will not do

- **Create what you did not ask for.** No tracker, board, column, ticket or
  `.delivery/` on its own initiative.
- **Delete anything.** Work that will not happen is moved to dropped, with a
  comment saying why.
- **Overwrite a person.** A change someone made in the tracker wins and is
  pulled into the local file.
- **Duplicate.** Every item carries its `[T-004]` marker and is searched for
  before any create.
- **Claim an update that did not happen.** When the tracker is down, work
  continues locally, it says `tracker: out of sync`, and it reconciles next time.
- **Show a credential.** Tokens are typed into a hidden prompt, never into chat;
  they live in the git-ignored `.delivery/.env` (or your shell, a CLI login, or
  an MCP sign-in) and are never printed. A token pasted into chat anyway is
  stored, not repeated, and flagged for rotation.
- **Call a ticket done without proof.** Done needs ProofBuild's `VERIFIED` and a
  merge.

References: [`planning.md`](references/planning.md) ·
[`sync.md`](references/sync.md) · [`trackers.md`](references/trackers.md) ·
templates: [`config.yml`](templates/config.yml) · [`ticket.md`](templates/ticket.md)

## License

MIT — see [`LICENSE`](../../LICENSE).
