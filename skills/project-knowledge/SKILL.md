---
name: project-knowledge
description: "Use when asked to learn the codebase, update or capture project knowledge, make a repository AI-ready, prep it for handover or onboarding, or when the knowledge Stop hook reports the knowledge is behind HEAD. Builds and incrementally maintains a committed knowledge base in .agents/knowledge/ (architecture, dated decisions, gotchas) so the next developer or agent who clones the repository is productive without re-deriving it; each run reads only what changed since the last one. Also use it to answer how this codebase works when .agents/knowledge/ exists, reading the recorded knowledge first. Never records secret values. Not for one-off code questions in a repository without .agents/knowledge/, for summarizing a single file, or for writing user-facing documentation."
---

# Project Knowledge

Every new developer, and every new agent session, pays the same cost: rebuild
how this codebase fits together from the code. Most of what they rediscover was
known to someone already — why the queue is idempotent, which env var silently
changes the auth mode, why the obvious refactor was tried and reverted.

This skill keeps that knowledge in the repository, where it travels with the
code, and keeps it **true over time**: each run reads what changed since the
last run and updates only that.

```
1. LOAD STATE  → .agents/knowledge/.learn-state.json: learned as of which commit?
2. DIFF        → what changed since then (cheapest view first)
3. LEARN       → what in that change a newcomer would otherwise rediscover
4. WRITE       → update the knowledge docs; never a secret value
5. RECORD      → move the cursor to HEAD
```

## Activation

**Engage when** asked to learn the codebase, update or capture the project
knowledge, make the repository AI-ready, or prep it for handover or onboarding;
when the knowledge Stop hook asks for a run; or after a significant feature or
refactor when the repository keeps `.agents/knowledge/`.

**Stay quiet when** the request is ordinary work in a repository without
`.agents/knowledge/`, a one-off question about one file, or a request for user
documentation (a README, API docs, a guide). Never start a first-run scan
nobody asked for: it is the one expensive run.

**Depth** `ACTIVE` when asked or prompted by the hook. `PASSIVE` otherwise:
where `.agents/knowledge/` exists, read the section a request needs before
reading code, and say nothing about it.

**Composes with** `architecture-engineer` (it owns `.architecture/` and its
ADRs; link to them from `decisions.md` rather than copying them) ·
`project-compass` (it owns `.project-compass/`; direction is its question, not
this one's) · `engineering-investigator` (a confirmed root cause that would
surprise the next developer becomes a gotcha) · `release-engineer` (deploy
steps belong in its runbook; record only where that runbook lives).

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

1. **Never write a secret value.** Record that a variable or key exists, its
   name, and what it controls. Never its value, never a token, never a
   connection string with credentials, never a private hostname that is not
   already in a committed file.
2. **Record only what was observed.** Every entry comes from the code, the
   commit history, configuration, or the user. A guess about why something was
   built a certain way is written as a question in `gotchas.md` ("Unclear:
   …"), not as a decision.
3. **Incremental by default.** A run after the first reads the change since the
   cursor, not the repository. Cost should scale with the diff, not the
   codebase.
4. **The log is append-only.** `decisions.md` entries are never edited or
   deleted. A reversed decision gets a new entry that names the old one.
5. **The repository outranks the knowledge.** When a doc and the code disagree,
   the code is right: fix the doc in this run, and say so in the report.
6. **Keep the always-loaded file small.** `CLAUDE.md` / `AGENTS.md` get one
   pointer line to `.agents/knowledge/`, not the knowledge. Whatever goes there
   costs tokens in every session.

## Where knowledge lives

```
.agents/knowledge/
  architecture.md     what each part is for, how data flows, how to run it   (updated in place)
  decisions.md        dated log: what was decided, why, what was rejected     (append-only)
  gotchas.md          non-obvious behavior, footguns, "don't change X without Y" (append, prune when fixed)
  .learn-state.json   { "last_learned_commit": "<sha>", "updated_at": "<ISO date>" }   (committed)
```

All of it is committed, the cursor included, so every clone and every machine
shares one view and nobody re-learns what someone else already recorded. Only
the Stop hook's marker, `.agents/knowledge/.learn-nagged`, is gitignored.
Formats, entry templates and what earns a place in each file:
`references/knowledge-format.md`.

## Step 1 — Load state

Read `.agents/knowledge/.learn-state.json`. Missing, or its commit is not in
this history (a rebase, a shallow clone): this is a first run. Otherwise note
`last_learned_commit`.

Read the existing docs' headings before writing anything, so an update lands in
the right section instead of a duplicate one.

## Step 2 — Diff since the last run

First run: walk the repository's structure and entry points, not every file.
Skip `node_modules`, `.git`, build output, vendored code, and lockfile contents
(note that the lockfile exists).

Later runs, cheapest view first. Stop reading once you know enough:

1. `git log --format='%h %s%n%b' <last>..HEAD` — commit messages usually name
   the decision and the why.
2. `git diff --stat <last>..HEAD` — which areas moved.
3. `git diff <last>..HEAD -- <path>` only for paths that change structure or
   contracts: new top-level directories, scripts, env and config, migrations,
   routes, schemas, transports.

Never read the whole patch, lockfiles, tests, fixtures or generated output.
What each step is for, and the first-run walk: `references/incremental-learning.md`.

## Step 3 — Decide what is worth recording

Bias toward what a newcomer would otherwise rediscover the hard way:

- **Structure** — what each top-level part is for, one line each; how a request
  or a job moves through it.
- **Commands** — install, run, test, build, migrate, deploy, taken from
  scripts, a Makefile, CI or the README. Never guessed.
- **Conventions actually used** — naming, file layout, error handling, testing
  style, as the code does them, not as a style guide hopes.
- **Decisions** — a library swap, a pattern change, an approach tried and
  reverted, a constraint someone chose. Why, and what was rejected.
- **Gotchas** — ordering requirements, workarounds for a vendor quirk, coupling
  the types do not show, "this looks unused but a cron job reads it".
- **Config surface** — environment variables and config keys by name, and what
  each one controls. Prefer `.env.example` as the source.
- **Open threads** — known debt worth flagging, so a successor need not grep.

Skip what the code already says plainly: a function's signature, a file list
any `ls` gives, a restatement of the README.

## Step 4 — Write

- `architecture.md`: replace the sections for the areas that changed; leave the
  rest untouched.
- `decisions.md`: append dated entries.
- `gotchas.md`: append; when a gotcha is fixed in code, remove it and note the
  fix in `decisions.md`.
- On a first run, add the one pointer line to `CLAUDE.md` and/or `AGENTS.md`,
  whichever exist (`CLAUDE.md` if neither does).

Plain, specific language. "Payments retry three times with the same idempotency
key; the provider dedupes on it" is knowledge. "Follows best practices" is not.

## Step 5 — Record

Write `HEAD` and the current date to `.agents/knowledge/.learn-state.json`. Do
not commit: say which files changed, and let the developer commit them with the
work.

## Reading mode

Where `.agents/knowledge/` exists and a request needs to know how something
works, read the relevant section first (the MCP tools `knowledge_search` and
`knowledge_onboard` do this cheaply), then confirm the parts that matter
against the code. Mention staleness only when the knowledge is behind HEAD in
the area the request touches.

## Keeping it current without being asked

`npx -y github:soumyaRauth/skills-hub knowledge init` sets a repository up for
the whole team, as committed files: this skill, a Stop hook that asks for a run
once enough commits pile up past the cursor (no tokens until it fires), and an
MCP server that serves the knowledge to any MCP client. What each piece does
and how a new developer uses it: `references/setup.md`.

## Final report

A few lines: first run or incremental, the commit range, which files changed,
and any new decision or gotcha by title. Never a reprint of the docs.

## Handover mode

When asked to prep the repository for a handover, after the normal run: read
`architecture.md` as if you had never seen the repository, and confirm it alone
gets a newcomer to the entry point, a running app, the tests, and the two
things most likely to trip them. Then confirm no secret value appears in any
knowledge file. Examples of all three run types: `examples/first-run.md`,
`examples/incremental-run.md`, `examples/onboarding.md`.
