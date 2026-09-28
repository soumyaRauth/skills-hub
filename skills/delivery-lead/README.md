# Delivery Lead

An Agent Skill that lets one developer work like a team: it takes the next
ready ticket, drives it to done, then the next, until the milestone ships or a
human is needed.

> **What is the next ticket, and has it actually reached done?**

```bash
npx skills add soumyaRauth/skills-hub --skill delivery-lead
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill delivery-lead --agent claude-code --copy
```

---

## Why it exists

A plan and a set of tickets do not build anything. What a team adds is the
loop: someone picks the next ticket, makes sure it is really finished, moves
the board, and picks up the one after. Working alone, that loop is where
projects stall, and where "done" quietly comes to mean "the code was written".

## What it does

```
next ready ticket → in progress → branch t/<id>-<slug>
  → build (ProofBuild always; the other disciplines when the ticket earns them)
  → VERIFIED? → review → commit + PR → merge → done
  → milestone complete? → Production Guard → staging → production (if allowed)
  → next ticket, until the budget, the milestone, or a question
```

```
RUN 2026-09-28 · milestone M1 · 4 of 5 tickets
T-003  Class list page            done         VERIFIED · PR #12 merged
T-004  Book a class               done         VERIFIED · PR #13 merged
T-005  Cancel a booking           blocked      REVIEW REQUIRED — refund rule undecided (question below)
T-006  Staging deploy             done         release-engineer: staging smoke ok
Tracker  Trello · in sync
Next     T-007 (ready) · answer the T-005 question to unblock it
```

It needs a `.delivery/` directory, which `delivery-planner` creates. With no
spec yet it hands off to `project-kickoff`; with a spec and no tickets, to
`delivery-planner`.

Four worked examples:
[three tickets, one blocked on a product decision](examples/three-tickets-one-blocked.md) ·
[a milestone into staging, then production asks](examples/milestone-to-production.md) ·
[a new session resuming after a crash](examples/resumed-after-crash.md) ·
[a large request that is not a run](examples/not-a-run.md)

## When it activates

Only when you ask for the loop: *"work through the backlog"*, *"take the next
ticket"*, *"keep going until the milestone is done"*, *"build the whole
thing"*, or by name. A single request stays a single request, however large.
See [Activation](SKILL.md#activation).

## What you control

Everything outward-facing is set once in `.delivery/config.yml` (`autonomy`),
or said yes to in the session:

| Action | Setting | Missing means |
| --- | --- | --- |
| Open a PR | `autonomy.open_pr` | ask |
| Merge to the default branch | `autonomy.merge` | ask |
| Deploy staging | `autonomy.deploy_staging` | ask |
| Deploy production | `autonomy.deploy_production` | ask |
| Tickets per run | `run.max_tickets` | 5 |

## What it will not do

- **Call a ticket done without proof.** Done is ProofBuild `VERIFIED` (or you
  accepting `REVIEW REQUIRED`) and merged.
- **Decide for another discipline.** Verdicts are quoted from the skill that
  owns them. It sequences; it does not route or gate.
- **Touch the plan or the tracker.** Those belong to `delivery-planner`. It
  writes only its run ledger in `.delivery/runs/`.
- **Force-push, rewrite history, skip hooks, or mix two tickets on one branch.**
- **Merge or deploy production without authorization** recorded in `autonomy`
  or given in the session.

When it stops, it asks one compressed question with options, and a new session
can resume from the ledger.

References: [`loop.md`](references/loop.md) ·
[`run-ledger.md`](references/run-ledger.md) ·
[`git-and-pr.md`](references/git-and-pr.md) ·
[`claude-code.md`](references/claude-code.md)

## License

MIT — see [`LICENSE`](../../LICENSE).
