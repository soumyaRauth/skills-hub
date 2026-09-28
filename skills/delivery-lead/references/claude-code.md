# Claude Code specifics

Everything in `SKILL.md` outside its *In Claude Code* section works in any agent
that supports Agent Skills. This file covers what Claude Code adds. Facts below
were checked against the official documentation on 2026-09-28.

## Loading skills

Claude invokes skills through the Skill tool, with the skill's name as the
parameter. Skills installed from a plugin are namespaced `plugin-name:skill-name`,
so from this repository's plugin they appear as `skills-hub:proof-driven-dev`.
Source: https://code.claude.com/docs/en/skills (checked 2026-09-28).

`impact-map` and `production-guard` declare `context: fork`, so each runs as
its own subagent and sees only the task passed to it. Pass the ticket (title,
why, acceptance criteria) or, at a milestone's end, the list of merged PRs and
their ProofBuild results.

## Review

Claude Code bundles a `/code-review` skill that reviews the branch's commits
ahead of its upstream plus uncommitted changes, and reports correctness bugs
and cleanups; `--fix` applies findings. It runs as a forked subagent. Sources:
https://code.claude.com/docs/en/skills and
https://code.claude.com/docs/en/code-review (checked 2026-09-28).

Use it at step 6 of the loop, on the ticket branch. Its cloud `ultra` mode runs
only when the user invokes it; never start it from the loop.

## Parallel tickets

Subagents are started with the Agent tool (renamed from Task in version
2.1.63), can run in parallel, and a subagent definition may set
`isolation: worktree` to work in a temporary git worktree that is removed if it
makes no changes. Source: https://code.claude.com/docs/en/sub-agents (checked
2026-09-28).

Use this only when all of these hold:

- both tickets are `ready` and neither depends on the other;
- the files each is expected to touch do not overlap (from the ticket's notes,
  or an impact map when one ran). Shared files such as a router, a schema or a
  lockfile count as overlap;
- the run budget covers both.

Each subagent builds one ticket on its own `t/<id>-<slug>` branch and returns
ProofBuild's status block and the branch name. The lead, in the main session,
does every status move, the PR, the merge and the ledger. If the two branches
later conflict, merge one, then the other ticket goes back through proof on the
updated default branch.

When in doubt, run tickets one after another. Parallelism saves time; a
conflict costs a ticket.

## Not verified

The subagent worktree's base branch is documented as the default branch "by
default"; how to change it was not checked for this file. Cut the ticket branch
explicitly inside the worktree rather than relying on it.
