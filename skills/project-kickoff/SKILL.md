---
name: project-kickoff
description: "Use when someone wants to start a new app, project or product from an idea, or when the repository is empty or holds only a README or notes and the request is to build something whole: \"I want to build an app where...\", \"start a new project for...\", \"where do I start?\". Asks only the product questions that change what gets built, writes docs/spec.md with every claim labelled, picks a boring stack the developer already knows, scaffolds a proven runnable skeleton, and hands the spec to planning. Not for features in an existing codebase, declared throwaway spikes, or talk about an idea with no intent to build."
---

# Project Kickoff

> **What exactly are we building first, on what, and is the empty repo ready to build in?**

A new project fails early in two quiet ways. The first is building the wrong
thing: the idea was never pinned down, so the first week goes into login pages
and settings screens while the one workflow anybody cares about is still vague.
The second is building on sand: no test runs, nothing says how to start it, a
real API key sits in a committed file, and the first deploy is a research
project.

Coding agents make both worse. Handed *"an app where members book classes"*,
they invent the gym's pricing, pick a stack from a blog post, and generate forty
files nobody asked for. A beginner cannot tell which parts were decided and
which were made up.

The deliverable is a proven starting point, in five stages:

```
idea ─▶ 1 product frame (≤5 questions, one block)
     ─▶ 2 docs/spec.md (every claim: [you said] or [assumed])
     ─▶ 3 stack (boring default + one-line reason)
     ─▶ 4 scaffold (runs, one passing test, lint, CI — commands actually executed)
     ─▶ 5 HANDOFF → delivery-planner (milestone 1 = walking skeleton deployed)
```

## Activation

**Engage when** someone wants to start something new and whole: *I want to
build an app where…*, *start a new project for…*, *I have an idea for a
product, where do I start?*, *set up a new repo for…*. Also when the repository
is empty or near-empty (see *Repository state*) and the request is to build an
application rather than a single script. A request that names the stack and
the features up front still engages: stage 1 is then skipped, not the skill.

**Stay quiet when** the repository already holds application code or a
dependency manifest: a feature there belongs to `proof-driven-dev`, a
structural question to `architecture-engineer`, a direction question to
`project-compass`. Stay quiet for a declared throwaway spike (*quick script to
try X*, *just a prototype I'll delete*), for a one-file tool, for questions
about an idea with no intent to build it (*is this a good business idea?*), and
for a new module or service inside an existing project. The word *new* in a
request is not a new project.

**Depth** `ACTIVE`: it shapes the whole first session. It never gates; it
stops only to ask the stage-1 questions, or before overwriting a file.

**Composes with** `delivery-planner` (turns the spec into milestones and
tickets) · `dependency-guard` (every package the scaffold installs) ·
`proof-driven-dev` (the evidence standard for the scaffold, and every ticket
after it) · `standards-compass` (the spec involves accounts, payments, personal
data, uploads or AI) · `architecture-engineer` (only when a stated requirement
forces a non-default stack) · `release-engineer` (deployment pipelines beyond
the first CI check) · `project-compass` (reads `docs/spec.md` once the project
exists) · `deployment-compatibility` (a named hosting target whose fit is
unknown).

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

1. **Never invent the user's world.** Market, users, prices, schedules, team
   size, deadlines, legal obligations, business rules: they come from the user
   or they are written as `[assumed]` with the assumption stated. A plausible
   invented fact is worse than a gap, because the plan gets built on it.
2. **Never scaffold on top of existing code.** Read the repository first. Any
   application code or dependency manifest means this skill stops (see
   *Repository state*).
3. **Ask before overwriting any file.** An existing README, `.gitignore`,
   LICENSE or notes file is kept and extended, or left alone. Replacing one
   needs an explicit yes in this session.
4. **Boring by default.** The stack is what the developer already knows,
   matched to where it must run. A beginner never gets an exotic language,
   a microservice split, a message queue, Kubernetes, or a framework released
   in the last year. A non-default choice needs a stated requirement that forces
   it, and then it goes to `architecture-engineer`.
5. **Questions only when the answer changes what gets built.** At most five, in
   one block, in plain words a non-engineer can answer. Anything technical gets
   a safe default instead of a question.
6. **Proven, not generated.** The scaffold is done when its install, test, lint
   and run commands were actually executed here and their output read. A
   command that could not run is reported as not run, never as passing.
7. **No secrets, anywhere.** `.env.example` holds names and placeholder values
   only. `.env` is in `.gitignore` before any `.env` exists. Real keys are never
   written to a file, a commit, or the chat.
8. **Nothing outward-facing without a yes.** Creating a remote repository,
   pushing, enabling a hosted service, or deploying needs the user's explicit
   yes in this session (or the autonomy settings in `.delivery/config.yml`).
   Local `git init` and local commits of the scaffold are fine when the user
   asked for the project to be set up.

## Repository state

Read the tree before anything else. Ignore `.git/`.

| State | What is there | What this skill does |
| --- | --- | --- |
| **EMPTY** | Nothing, or only `LICENSE` / `.gitignore` | Proceed |
| **IDEA-ONLY** | A README, notes, sketches, `docs/` with prose, no code | Proceed. Read every note first: it is the user's own statement of the idea, and it answers questions you would otherwise ask |
| **STARTED** | A generator's output, one manifest, a hello-world, and no features | Ask once: *extend what is here, or start clean in a new directory?* Never delete it |
| **EXISTING** | Application code, a manifest with real dependencies, tests, migrations | Stop. This is not a kickoff. Say so in one line and let the request go to the skill that fits |

`docs/spec.md` already present means kickoff happened before. Read it, update
the parts the user changes, and never rewrite their `[you said]` lines.

## Stage 1 — Product frame

Read the request and any notes. For each question below, decide: *answered*,
*safe to assume*, or *must ask*. Ask only the *must ask* ones, and never more
than five.

| Question | Ask when | Otherwise |
| --- | --- | --- |
| **Who uses it?** Kinds of people, and who is in charge | The request does not name them | — |
| **The one core workflow, end to end** | You cannot write it as five to eight concrete steps from a real person's point of view | — |
| **What v1 leaves out** | The idea invites scope (payments, messaging, mobile apps, multi-location, admin reporting) | Assume the smallest v1 and list the rest as non-goals |
| **Money** — does v1 take payments? | Payment is plausible and unstated | Assume no payments in v1 |
| **Personal data** beyond name and email (health, children, ID documents, location) | The domain suggests it | Assume name and email only |
| **Deadline or fixed date** | The user mentioned one vaguely | Assume none; never invent one |
| **Where it must run** — phone, browser, a specific company server, offline | The request implies a place (an app store, a kiosk, an intranet) | Assume a web app that works in a phone's browser |

Everything else is a default, not a question: language, framework, database,
hosting, auth mechanism, styling, testing tools. `references/product-questions.md`
has the wording that works for beginners and the defaults to state.

Output, as the one interruption:

```
Before I write anything, five questions. Short answers are fine; "you decide"
is an answer too, and I will write it down as an assumption.

1. Who will use it? (for example: members, instructors, the front desk)
2. Walk me through one booking from start to finish, as a member would do it.
3. Should members pay for classes in the app in the first version, or not yet?
4. What do you already know how to program in, if anything?
5. Is there a date this needs to be working by?

Meanwhile I am assuming: a web app that works on phones, no payments in v1,
one gym location. Say so if any of that is wrong.
```

**Skip stage 1 entirely** when the request already answers every *must ask*
row. An experienced developer who names users, workflow, scope and stack gets
no questions; go straight to stage 2.

**The user answers "you decide"** to a product question: pick the smallest
option and write it as `[assumed]`. Never pick on their behalf for price,
deadline, or who is allowed to do what without marking it.

## Stage 2 — `docs/spec.md`

Write the spec in the shape of `references/spec-format.md`. Sections: problem,
users, core workflow (numbered steps), v1 scope, non-goals, constraints, open
decisions. Every claim carries a label:

- `[you said]` — the user stated it, in the request, the notes or an answer.
- `[assumed]` — you chose it; the line says what would change it.

Open decisions are the questions that do not block v1 but will block a later
milestone (*cancellation window?*, *waitlist?*). They are listed, not answered.

**Standards trigger.** When the spec involves accounts, payments, personal
data beyond a name, file uploads, or AI features, engage `standards-compass`
in the same turn and add what it names to the spec's constraints section:

```
HANDOFF → standards-compass: v1 has member accounts and stores phone numbers [spec §Users, §Constraints]
```

Its requirements go into the spec as constraints. Never state its verdict.

## Stage 3 — Stack

Pick from `references/stack-defaults.md`, in this order: what the developer
already knows → where it must run → the boring default for that pair. Output:

```
STACK   Python 3.12+ · Django · SQLite locally, PostgreSQL when deployed
WHY     You know some Python; Django ships accounts, an admin screen for the
        front desk and database migrations, so v1 needs few extra packages.
```

Rules for this stage:

- **One stack, one line of reason.** No comparison table for a beginner unless
  asked.
- **Every package the scaffold installs** goes through `dependency-guard` first,
  including the framework: `HANDOFF → dependency-guard: django, pytest-django for the scaffold`.
- **Hand off to `architecture-engineer`** only when a stated requirement forces
  a non-default choice: it must work offline, must be a native store app, must
  run on hardware or inside a customer's network, real-time collaboration, a
  regulated data-residency rule. Quote the requirement in the HANDOFF line.
  *"It should scale"* is not such a requirement.
- **A named host** (*it has to run on our office server*) with unknown fit →
  `HANDOFF → deployment-compatibility`. Otherwise hosting is decided later, by
  `release-engineer`.

## Stage 4 — Scaffold

Create the smallest skeleton that proves the stack works end to end. Nothing
for later: no feature code, no empty folders "for services", no auth before the
spec's workflow needs it.

| Must exist | Why |
| --- | --- |
| A runnable app that serves one page or endpoint | Proves the stack starts |
| One passing test that exercises that page or endpoint | Proves the test runner works; the first ticket adds to it |
| Lint and format config, using the ecosystem's standard tool | Mistakes caught before review |
| `.env.example` — variable names, placeholder values, a comment each | Configuration is visible without secrets |
| `.gitignore` covering `.env`, dependencies, build output, the local database | Secrets and junk never committed |
| `README.md` with the exact install, run and test commands, copied from what you ran | A newcomer, or the user next month, can start it |
| A first CI check: install, lint, test on every push and pull request | The walking skeleton stays green |

An existing README from the idea stage is extended with a *Run it* section; the
idea text is kept (rule 3). Deployment pipelines are not part of the scaffold:
`HANDOFF → release-engineer: deploy pipeline for milestone 1`.

**Prove it.** Run each command and read the output, in the manner of
`proof-driven-dev`:

```
SCAFFOLD PROOF
install   pip install -r requirements.txt                  exit 0
lint      ruff check . && ruff format --check .            exit 0
test      python manage.py test                            1 passed
run       python manage.py runserver → GET / returned 200  checked, then stopped
CI        .github/workflows/ci.yml written                 not run here (runs on first push)
```

A step that could not run (no network, a missing runtime) is `not run: <why>`,
and the result is `SCAFFOLD UNPROVEN`, never ready.

## Stage 5 — Handoff to planning

```
HANDOFF → delivery-planner: docs/spec.md is ready; milestone 1 = walking skeleton deployed
```

Milestone 1 is always *walking skeleton deployed*: the scaffold reachable at a
real URL through the pipeline, before any feature. The core workflow becomes the
next milestone. Open decisions become tickets that ask a question, not tickets
that guess the answer. This skill writes no tickets and no `.delivery/` files.

## Output

The reply leads with where the kickoff stands:

| Status | When |
| --- | --- |
| `WAITING FOR ANSWERS` | Stage 1 asked its questions. Nothing else was written |
| `READY TO BUILD` | Spec written, scaffold proven, handoff made |
| `SCAFFOLD UNPROVEN` | Spec written and scaffold created, but a proof step did not run or failed |
| `NOT A KICKOFF` | The repository holds existing code; one line, then the request goes where it belongs |

```
READY TO BUILD

Spec      docs/spec.md · 9 [you said] · 4 [assumed] · 3 open decisions
Stack     Python · Django · SQLite (PostgreSQL when deployed)
Scaffold  install ✓ · lint ✓ · 1/1 tests ✓ · runs ✓ · CI written
Next      HANDOFF → delivery-planner: milestone 1 = walking skeleton deployed

Check the [assumed] lines in docs/spec.md — each one is a guess I made.
```

**For a beginner**, add one plain sentence per command under the proof block
saying what it does and when they will use it. Explain; do not lower the bar.
The proof is the same for everyone.

## What this skill is not

- **Not an architect.** It picks a boring default. Real structural choices go
  to `architecture-engineer`.
- **Not a planner.** It writes the spec; `delivery-planner` owns milestones,
  tickets and the tracker.
- **Not a feature builder.** The scaffold proves the stack. The first feature is
  the first ticket, built under `proof-driven-dev`.
- **Not a deployer.** A CI check, yes. Hosting and pipelines belong to
  `release-engineer`.
- **Not a business advisor.** It does not judge whether the idea is good, size
  a market, or suggest pricing.

## References

- `references/product-questions.md` — the question bank, beginner wording, and the default stated for each unasked question
- `references/spec-format.md` — the `docs/spec.md` shape, with labels and open decisions
- `references/stack-defaults.md` — boring defaults by what the developer knows and where it runs, scaffold commands, CI, with sources

## Worked examples

`examples/beginner-climbing-gym.md` — a first-time builder's idea, five
questions, then the spec ·
`examples/experienced-full-brief.md` — everything given up front: no questions,
straight to spec and a proven scaffold ·
`examples/existing-repo-quiet.md` — "start a new booking module" in a
running codebase, where it stays out.
