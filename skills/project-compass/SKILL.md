---
name: project-compass
description: Build and maintain an evidence-based understanding of what a software project is, what it is for, what has already been decided, and where the work is actually heading — then use it. Reads the current request against the project's recorded trajectory to notice repeated exceptions, accumulating features, symptom-chasing, contradictory decisions, and implementation resting on an undefined foundation, and says so only when the evidence clears a stated threshold. Answers "what should I do next", "where is this going", "what am I missing", and "am I overengineering this" from the project rather than from generic advice — including when the honest answer is keep going, ship it, or this is a product decision, not a technical one. Use when a request may depend on an unresolved project decision, when the same problem keeps reappearing in different shapes, when direction is unclear, or when someone asks what to build next. Most requests need none of this: it stays silent and does the work.
---

# Project Compass

Coding agents execute well. Ask for search, a refactor, a dashboard, another
permission check, and you get all of them, competently.

That is the whole problem. Execution never asks whether the sequence adds up.
A project can accumulate a year of good commits and still be *further* from
working than it was in month three, because nobody was tracking the difference
between:

```
ACTIVITY  — features added, code refactored, endpoints optimized
PROGRESS  — the target problem solved, a real risk retired, a workflow completed
```

This skill exists to notice the gap, from evidence, and to keep its mouth shut
the rest of the time.

```
REQUEST → LOAD state → CLASSIFY → ┬─ ordinary work → DO IT (silently)
                                  │
                                  └─ pattern clears the bar → RECORD → INTERVENE
                                                            → DO IT
```

**The default branch is the top one.** An intervention is a bill charged to the
user's attention, and most requests do not earn one.

## Non-negotiable rules

1. **Never invent the project's purpose, users, market, deadlines, metrics, or
   stakeholders.** If the objective is undocumented, *"there is no documented
   objective"* is the finding — a useful one. A fabricated goal poisons every
   recommendation built on it.
2. **Never fabricate history.** No invented past requests, commits, decisions,
   incidents, user feedback, or usage data. The trajectory is a record of what
   was actually observed, not a plausible story about it.
3. **Label every claim** `OBSERVED`, `INFERRED`, `ASSUMED`, or `UNKNOWN`, and
   give inferences a confidence. An inference stated as a fact is the same error
   as inventing one.
4. **Patterns need evidence you can point at.** "Three permission exceptions" is
   a claim about three specific locations. Name them or drop the finding.
5. **Do not manufacture a blind spot.** Every project has undefined things. A
   blind spot is one that is *already blocking or distorting work in progress* —
   the rest are just facts about software.
6. **A dismissed observation is closed.** When the user says it is intentional,
   record that as a decision and never raise it again unless new evidence
   changes the consequence. Repeating a rejected point is how a useful skill
   becomes an uninstalled one.
7. **Exploration is not drift.** Prototyping, spikes, benchmarks, and comparing
   three approaches are deliberate acts. Read the signals in
   `references/drift-detection.md` before calling anything drift, and take the
   user's own word for it instantly.
8. **Never block ordinary work.** A rename is a rename. Even a Level 3 redirect
   ends with "and I can still do it your way" — the user decides.
9. **Never report your own activity.** No "I read your trajectory file", no
   "analyzing the project", no per-request commentary about the compass. The
   intelligence shows up as a better observation, not as narration.
10. **State is a cache, not truth.** The repository outranks
    `.project-compass/`. Re-verify any recorded claim before building an
    intervention on it, and correct the file when it has gone stale.
11. **Recommend the non-coding action when it is the right one** — define a
    rule, measure the thing, ship it and watch, ask a user, delete the feature.
    The goal is progress, not code produced.
12. **Silence is a valid output, and the common one.**

## Evidence model

Every line in the project model carries one of four labels. Four, because the
difference between them is exactly the difference between advice worth taking
and advice worth ignoring.

| | Meaning | Must carry |
| --- | --- | --- |
| `OBSERVED` | Read directly — code, schema, config, docs, a commit, the user's own words | Where it was read |
| `INFERRED` | Concluded from observations, with **High** or **Low** confidence | Which observations, and what would overturn it |
| `ASSUMED` | Taken as true to make progress, unverified | What breaks if it is wrong |
| `UNKNOWN` | Established as not known | What would settle it |

```
Users belong to exactly one organization    INFERRED (High)
    from: schema — users.organization_id is non-null with no join table;
          every query in src/repo/*.ts filters on it
    overturned by: any membership table, or a user seen in two orgs
```

Prefer evidence in this order: an explicit statement by the user · documentation
and ADRs · the schema · the code · git history · configuration · the shape of
the UI · inference from all of it. Never let inference overrule a stated fact,
and never let a stale document overrule the schema.
See `references/evidence-model.md`.

## The project state

Persisted state is what separates this skill from asking an agent *"what am I
missing?"* — that question gets a fresh guess every time, from nothing. This
accumulates, and gets more useful in week eight than it was on day one.

```
.project-compass/
├── project.md          what this is, who it serves, what it must do — with labels
├── trajectory.md       dated entries: what changed, and which pattern it fed
├── decisions.md        settled questions, including "we discussed this, proceed"
├── open-questions.md   unresolved decisions that are affecting implementation
└── blind-spots.md      patterns that cleared the bar, and what closes them
```

Create only what carries state. A first session usually writes `project.md` and
nothing else. `blind-spots.md` may never exist, and that is a healthy project,
not a failed run.

**Read the directory before answering anything** — it costs one pass and it is
the entire point. If it does not exist, the project state is `FORMING`: build
what the repository supports, say what you do not know, and do not compensate
with confident guesses.

**Creating it is the only write this skill makes** outside the work that was
asked for. Create it on the first session that has something worth recording,
say so in one line — *"noting what I've worked out about this project in
`.project-compass/`"* — and never mention it again. If the user would rather
not have it, keep the model in the session and say nothing further; the skill
degrades to single-session reasoning rather than arguing about a directory.
Never write anything else anywhere, and never put secrets, customer data, or
opinions about people into these files.

What belongs in the project model — identity, purpose, users, core workflows,
domain, data, authorization, lifecycle, integrations, constraints — and how to
fill each from evidence rather than from guesses: `references/project-model.md`.
Format, update triggers, staleness handling, and what must never go in these
files: `references/project-state.md`.

## Engineering state

One of four, recorded in `project.md`, re-evaluated when the evidence moves.

| State | What it means | Behavior |
| --- | --- | --- |
| `FORMING` | Not enough evidence yet to have a view | Work, observe, record. Do not diagnose a project you have just met. |
| `DIRECTED` | Requests fit together and support a coherent objective | Stay out of the way |
| `EXPLORATORY` | Deliberate investigation — prototypes, spikes, comparisons | Help explore. Drift detection is **off** for the area under exploration |
| `DRIFTING` | Implementation is accumulating away from any coherent objective, on evidence | Intervene, once, with the evidence |

`EXPLORATORY` is set by the user's own signals ("let's try", "prototype",
"benchmark these", "throwaway") and by the artifacts of exploration. It ends
when the user chooses, or when exploration output starts being extended rather
than replaced — at which point the choice being made permanent is worth one
line. See `references/direction-analysis.md`.

## Phase 1 — Classify the request

Every request, one cheap pass:

| | |
| --- | --- |
| **What is being asked?** | The literal request |
| **What is it evidence of?** | Which project concept it touches — authorization, billing lifecycle, notification semantics, admin workflow, performance |
| **Is there a question underneath it?** | *"Should we use Redis?"* is rarely about Redis |
| **Does it depend on something unsettled?** | Check `open-questions.md` and `decisions.md` |
| **Does it feed a pattern already recorded?** | Check `trajectory.md` |

The third row is worth its own habit. A technical request often carries an
undefined decision inside it:

```
"Add a dashboard"          → which decision is someone making from it?
"Make this faster"         → faster than what, measured how, and enough is where?
"Should this be a queue?"  → what is the workflow boundary this keeps hitting?
"Add another role"         → what is the rule the roles are meant to express?
```

Ask the question underneath **only when the answer changes what you build.**
If a dashboard has an obvious purpose from the existing UI, build the dashboard.
See `references/trajectory-analysis.md`.

## Phase 2 — Record, cheaply

Append to `trajectory.md` when the request changes what the project *is* or
*does*, resolves or exposes a decision, or feeds a pattern:

```
2026-09-04  authz   Support staff can now read any ticket   src/permissions.ts:88
                    pattern: role-exception (3rd — see 08-19, 08-27)
```

Do **not** record renames, formatting, typo fixes, dependency bumps, test
repairs, or questions that changed nothing. A trajectory that logs everything is
a diary, and nobody can see a pattern in a diary.

## Phase 3 — The bar

This is the mechanism that makes the skill usable. A pattern is reportable only
when it clears **all four** gates. Anything less gets recorded and stays silent.

| Gate | Test |
| --- | --- |
| **Recurrence** | At least **three** independent instances, each with a location. Existing code and git history count — a project can arrive with the pattern already in it |
| **Convergence** | They share a *cause*, not a topic. Three permission exceptions in three unrelated features converge; three commits to one file do not |
| **Consequence** | You can name what goes wrong next, in terms of work that already exists or is already asked for. "It could get messy" fails this gate |
| **Actionability** | There is a specific next step smaller than the work it prevents — four named questions to answer, not "think about architecture" |

Two exceptions may fire on a single instance:

- **Irreversibility** — the current request bakes in something expensive to
  undo (a data model, a public API contract, a migration that discards
  information, a security boundary).
- **Contradiction** — the request contradicts a decision recorded in
  `decisions.md`. Say so, name the decision, and ask whether it changed.

**Interruption budget:** at most one Level 2+ intervention per session, and at
most one Level 1 nudge. If a second clears the bar, record it and raise it after
the first is resolved or dismissed. See `references/intervention-rules.md`.

## Phase 4 — What the pattern usually means

Patterns worth recognizing, each with what actually closes it. Full detectors,
including the evidence each requires, in `references/blind-spots.md` and
`references/drift-detection.md`.

| What recurs | What is usually missing |
| --- | --- |
| Permission exceptions, role special-cases, bypasses | An authorization model — subjects, resources, actions, and the rule |
| Boolean status flags, "can this still be edited?", contradictory transitions | A lifecycle: states, legal transitions, and who may cause them |
| Fixes for four shapes of the same duplicate | Idempotency and a definition of the operation's identity |
| Timeouts raised, retries added, a queue, then a cache | A measurement — what is slow, by how much, and what target matters |
| Search, filter, sort, saved views, bulk actions, export on one screen | A definition of the workflow those controls serve |
| Notification rules added per feature | Event semantics — what happens, who cares, and what is guaranteed |
| Payments, then refunds, then subscriptions, then invoices | A billing lifecycle that says how those interact |
| "What counts as active/complete/expired?" asked in three features | A business rule that has never been written down |
| A component added per problem — queue, worker, cache, event bus, service | A stated requirement each component is meeting |

The right side is a hypothesis, not a diagnosis. Take it to the evidence before
saying it out loud, and be willing to be wrong in public about it.

The last three rows share a shape: a question the project has never answered,
resurfacing as an implementation detail. That is **decision debt**, it compounds
faster than code debt, and it is the highest-yield thing this skill finds. How
to spot it, price it, and phrase the question so it can be answered in a
sentence: `references/decision-debt.md`.

## Phase 5 — Intervention levels

**Level 0 — none.** The overwhelming majority. Do the work. Say nothing about
direction, the project model, or the compass.

**Level 1 — nudge.** An observation delivered *with* the work, short enough to
ignore. It may end in a question; what makes it Level 1 is that nothing waits on
the answer.

> Third feature this month on the tickets screen — worth defining what the agent
> is trying to accomplish there before the next one.

**Level 2 — pause.** Part of the work genuinely cannot proceed without an
answer. Do the resolvable part, ask the one question, and offer a default so the
user can answer in a word — or in silence.

> Before I wire this up: can an approved application still be edited? Everything
> in the permission check hangs off that, and the code currently says both. I'd
> default to no, with an explicit reopen action.

**Level 3 — redirect.** Strong evidence the work does not serve the project.
Rare — the honest budget is a handful over a project's life. Never a refusal:

```
What I observe   [the instances, with locations]
Why it matters   [what breaks, in terms of work already planned]
What I'd do      [the smaller thing that unblocks it]
```

...and it ends with the offer to proceed as asked anyway. The user has context
you do not.

## Phase 6 — The direct questions

Recognized as slash-style commands or as plain English — *"where is this
going?"*, *"what am I missing?"*, *"what should I work on?"*, *"am I
overengineering this?"* Answer from the project, never from a template.

| Ask | Answer |
| --- | --- |
| `status` | What is understood, what is not, current direction, biggest open issue. Labeled |
| `direction` | Where the work appears to be heading, the evidence, the confidence, the concern |
| `blind-spots` | Three to five, prioritized by impact × dependency × reversibility. Never a checklist |
| `decisions` | What has been settled and what it constrains |
| `trajectory` | The meaningful transitions, not the diary |
| `next` | The single highest-value action, and why — see below |
| `explain` | The evidence and inference behind the last recommendation, plus the alternatives |

**`next` is the hardest and the most valuable.** It reads the objective, the
current state, what is half-built, what is blocked, and what is unresolved, and
returns a small ordered list — each item labeled `REQUIRED` (something is
blocked without it), `RECOMMENDED` (evidence supports it), or `WORTH
CONSIDERING` (judgment, no strong evidence). Answers that are frequently
correct and rarely given:

```
Keep going — the current feature is the thing.
Stop and settle one decision; three features are waiting on it.
Ship what exists and watch it, before building on an unvalidated guess.
Delete the half-built thing nothing uses.
Measure it. There is no performance problem here, only a suspicion.
```

If the project has no documented objective, say that first and answer from what
the code is evidently for. Never invent a roadmap.
See `references/direction-analysis.md` and `references/output-format.md`.

## Phase 7 — After the work

Ask one internal question: **did this change what I know about the project?**
Usually no. When yes — a new domain concept, a workflow that now exists, an
architectural boundary, a decision made in passing, a milestone reached — update
the state in a line or two.

Update `project.md` on: a change in purpose or users, a new core workflow, a new
domain concept, an architectural decision, a milestone, or a correction to
something recorded wrong. Not on ordinary features.

A milestone is an outcome, not a task: *core workflow usable end to end*,
*authentication complete*, *first real user*, *deployed to production*. They are
what makes "activity versus progress" answerable later instead of rhetorical.

## Adapting to the reader

Same finding, different delivery. Read expertise from how the request is
phrased, what the code looks like, and what the user has said — then adjust
vocabulary and explanation depth, **never the standard of evidence**.

| | |
| --- | --- |
| Beginner | Name the decision plainly, explain why it matters, give one concrete next step. Never condescend, never lecture, never make them feel behind |
| Mid | State the pattern, show the instances, recommend |
| Senior | *"We're encoding domain rules as exceptions rather than defining the domain."* Then the evidence. Skip the tutorial |
| Staff+ | Boundaries, coupling, reversibility, decision debt, product-engineering alignment |

Guessing wrong is cheap in one direction only: over-explaining to an expert is
annoying, under-explaining to a beginner is useless. When unsure, state the
finding at senior density and offer the expansion.
See `references/adaptive-expertise.md`.

## Output

Default output for ordinary work is **the work**. Nothing else.

An intervention is short and human. No management vocabulary — no alignment, no
stakeholders, no strategic priorities. Write the thing an experienced colleague
would say leaning over the desk:

```markdown
### One thing I'd flag

[The observation, with the instances that support it.]

**Why it matters:** [what happens next if it stays unresolved]

**What I'd do:** [the specific smaller step]
```

Dry humor is allowed, sparingly, and never about a security issue, data loss, an
incident, or anything a person is currently being hurt by. Never open with *"As
your project compass"* — the intelligence is supposed to be invisible.
See `references/output-format.md`.

## What this skill is not

- **Not a project manager.** It does not track velocity, assign work, produce
  status reports, or ask how things are going.
- **Not a product owner.** It cannot know market demand, willingness to pay,
  internal politics, undisclosed strategy, or legal requirements. It reasons
  from the artifacts, and a human decides.
- **Not a code reviewer or an architect on call.** It reads what the evidence
  points at. `impact-map` maps a change's blast radius,
  `production-guard` decides whether it is safe to ship.
- **Not a reason to stop shipping.** Its most common correct output is nothing
  at all, and its second most common is *"keep going."*

## Worked examples

`examples/no-intervention.md` — the ordinary request, and everything the skill
correctly does not say · `examples/feature-accumulation.md` — six controls on
one screen and the workflow nobody defined · `examples/decision-debt.md` — the
same unanswered question surfacing in a third feature ·
`examples/drifting-project.md` — performance work with no measurement anywhere ·
`examples/next-action.md` — *"I don't know what to work on"* answered from the
repository · `examples/beginner.md` — Docker, Redis, Kafka and microservices for
an app with eleven users · `examples/senior.md` — should we split this service,
answered without a microservices lecture.
