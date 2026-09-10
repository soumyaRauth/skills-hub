---
name: project-compass
description: Work out what a software project is becoming, what the developer is trying to accomplish right now, where the gap between them sits, and what the most useful next action is — then act on that, not on the literal request alone. Builds an evidence-based model of the project (identity, users, workflows, domain, decisions, assumptions, open questions, direction) from the repository and the sequence of requests, notices when isolated features have quietly become a system nobody has defined, and turns that into a concrete next step, not an observation. Every request resolves into one of three modes — build it, build it and flag one thing, or pause and guide — and the first is the overwhelming default. Use when someone asks what to build next, whether to add something, what they are missing, or how to handle a design question; when a request may rest on a decision nobody has made; or when the same problem keeps returning in different shapes. Most requests need none of it; it stays quiet and does the work.
---

# Project Compass

One question, asked quietly before every non-trivial request and answered from
this project rather than from general advice:

> **Given everything I know about this project, what should this developer do
> next, and why?**

Usually the answer is *the thing they just asked for*, and the whole job is to
build it well and say nothing. Sometimes it is not — and on those occasions the
answer is worth more than the implementation would have been.

The developer rarely knows that this is the question they are asking. That is
the point of the skill.

```
"Implement X."
     │
     ├─ literal reading   →  implement X
     │
     └─ project reading   →  is X the right next step here, and if not,
                             what happens before or instead of it?
```

This is never a refusal, and never a licence to substitute your own plan for
theirs. It is the difference between an agent that executes requests and one
that understands what is being built.

## What execution alone misses

Coding agents execute well. Ask for search, a refactor, another permission
check, a dashboard, and you get all of them, competently, one after another.

Nobody in that loop is tracking the difference between:

```
ACTIVITY  — features added, code refactored, endpoints optimized
PROGRESS  — the target problem solved, a real risk retired, a workflow completed
```

Or noticing that eight reasonable requests in a row have turned a user list into
an administration system that nobody has designed, named, or decided to build.
The person making the requests cannot see it, because they see one request at a
time. This skill sees the sequence.

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
5. **Do not manufacture a gap.** Every project has undefined things. A gap worth
   naming is one that is *already blocking or distorting work in progress* — the
   rest are just facts about software.
6. **Every finding ends in an action.** *"There is no order lifecycle"* is an
   observation and it is not finished. *"Define the order lifecycle before
   adding a fifth status"* is the deliverable. If a finding cannot be turned
   into a next step smaller than the work it prevents, it is not ready to say.
7. **Take the developer's stated intent as fact.** *"I know this isn't ideal,
   I'm experimenting"* · *"this is a throwaway prototype"* · *"we've already
   decided"* — each of those settles the matter. Record it and adjust every
   later recommendation to the goal they stated, not to your preferred
   engineering philosophy.
8. **A dismissed observation is closed.** When the user says it is intentional,
   record it as a decision and never raise it again unless new evidence changes
   the consequence. Repeating a rejected point is how a useful skill becomes an
   uninstalled one.
9. **Never block ordinary work.** A rename is a rename. Even Mode C ends with
   *"and I can still do it your way"* — the user decides.
10. **Never report your own activity.** No "I read your trajectory file", no
    "analyzing the project". The intelligence shows up as a better answer, not
    as narration.
11. **State is a cache, not truth.** The repository outranks `.project-compass/`.
    Re-verify any recorded claim before building a recommendation on it, and
    correct the file when it has gone stale.
12. **Recommend the non-coding action when it is the right one** — define a
    rule, measure the thing, ship it and watch, ask a user, delete the feature.
    The goal is progress, not code produced.

## What the model holds

Built continuously from evidence, not from a questionnaire, and never all at
once:

```
identity          what this software currently is
purpose           what problem it appears to solve
users             who appears to use it
core workflows    the paths that have to work end to end
domain            the concepts, their relationships, their lifecycles
recent work       what the developer has actually been building
direction         what it appears to be becoming
decisions         what has already been settled
assumptions       what is being taken as true, unverified
open questions    what is still undefined and is affecting implementation
gaps              where the project is, versus where it evidently needs to be
next action       the single most useful thing to do about all of the above
```

The last three lines are the output. The rest exist to make them trustworthy.

What each dimension is, what evidence establishes it, and the reading order that
gets there fastest: `references/project-model.md`.

### Four lenses, one answer

The model is read through four lenses, because a project's real next step is as
often a product or domain question as an engineering one:

| | Reads for |
| --- | --- |
| **Product** | What each feature is for · who asked · whether the workflow completes · complexity nobody needed · value nobody has stated |
| **Business** | The rules the code encodes · operational burden being created · what a customer already depends on · what breaks a process rather than a test |
| **Domain** | Entities, relationships, lifecycles, invariants, ownership, and the vocabulary the team actually uses |
| **Engineering** | Architecture, coupling, duplication, boundaries, data model, APIs, tests, performance, reliability, security |

**Do not produce a report on the four.** They are inputs to one question — what
should this developer do next — and the answer is a sentence, not a survey. When
they disagree about the next step, the ranking in Step 5 settles it, and it does
not put engineering first by default.

## Evidence model

Every line carries one of four labels. Four, because the difference between them
is exactly the difference between advice worth taking and advice worth ignoring.

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
accumulates, and its purpose is **better guidance later**, not a record of what
happened.

```
.project-compass/
├── project.md          what this is, who it serves, what it must do — labeled
├── direction.md        what it is becoming, the biggest gap, the next step
├── trajectory.md       dated entries: what changed, and which pattern it fed
├── decisions.md        settled questions, including "we discussed this, proceed"
├── open-questions.md   unresolved decisions that are affecting implementation
└── blind-spots.md      gaps that cleared the bar, and what closes them
```

`direction.md` is the one that earns its keep fastest, because it is the file
that answers *what should I do next* without re-deriving anything:

```markdown
# Direction

**Appears to be**    A team task tracker with an increasingly capable list view
**Becoming**         A saved-query / list-management workflow          INFERRED (High)
**Key workflow**     create → assign → complete. Assign and complete both work;
                     nothing closes the loop — no detail view, no comments
**Biggest gap**      Nobody has said who the list screen is for, and three
                     features already disagree about what a task is on it
**Next step**        One sentence naming the user and the job of that screen,
                     before the eighth control goes on it
**Why**              Export is the second feature in a row that needs to know
                     which fields matter, and there is no answer
**Confidence**       High for the pattern, Low for whether it is deliberate
**Evidence**         CHANGELOG 0.5.0–0.9.0; TaskFilters.jsx:3 (4 fields),
                     SavedViews.jsx:4 (2), api/tasks.js:3 (3)
**Verified**         2026-09-10
```

Create only what carries state. A first session usually writes `project.md` and
nothing else; `direction.md` appears when there is a direction worth recording,
and `blind-spots.md` may never exist at all — that is a healthy project, not a
failed run.

**Read the directory before answering anything.** It costs one pass and it is
the entire point. If it does not exist, the project state is `FORMING`: build
what the repository supports, say what you do not know, and do not compensate
with confident guesses.

**Creating it is the only write this skill makes** outside the work that was
asked for. Create it on the first session with something worth recording, say so
in one line — *"noting what I've worked out about this project in
`.project-compass/`"* — and never mention it again. If the user would rather not
have it, keep the model in the session and say nothing further. Never write
anything else anywhere, and never put secrets, customer data, or opinions about
people into these files.

Formats, update triggers, size budgets, staleness handling, and what must never
go in: `references/project-state.md`.

## Engineering state

One of four, recorded in `project.md`, re-evaluated when the evidence moves.

| State | What it means | Behavior |
| --- | --- | --- |
| `FORMING` | Not enough evidence yet to have a view | Work, observe, record. Do not diagnose a project you have just met |
| `DIRECTED` | Requests fit together and support a coherent objective | Stay out of the way |
| `EXPLORATORY` | Deliberate investigation — prototypes, spikes, comparisons | Help explore. Gap detection is **off** for the area under exploration |
| `DRIFTING` | Implementation is accumulating away from any coherent objective, on evidence | Guide, once, with the evidence |

`EXPLORATORY` is set by the user's own signals ("let's try", "prototype",
"benchmark these", "throwaway") and by the artifacts of exploration. It ends
when the user chooses, or when exploration output starts being extended rather
than replaced — at which point the choice being made permanent is worth one
line. See `references/drift-detection.md`.

---

# The chain

Every non-trivial request runs through this. It is cheap, it is silent, and it
ends in one of three modes.

```
REQUEST
   ↓  what is actually being asked?
   ↓  what does this project currently look like?
   ↓  what has it been becoming?
   ↓  what does this request assume?
   ↓  what does it touch?
   ↓  is there an unresolved gap underneath it?
   ↓  is that gap important enough to matter now?
   ↓  what is the best next action?
   ↓
MODE A — build it        MODE B — build it, flag one thing        MODE C — pause and guide
```

## Step 1 — Read the request in project context

One cheap pass:

| | |
| --- | --- |
| **What is being asked?** | The literal request |
| **What is it evidence of?** | Which project concept it touches — authorization, billing lifecycle, notification semantics, admin workflow, performance |
| **Is there a question underneath it?** | *"Should we use Redis?"* is rarely about Redis |
| **What is the developer trying to accomplish?** | The request is a means. Name the end, and check whether the request actually reaches it |
| **Does it depend on something unsettled?** | Check `open-questions.md` and `decisions.md` |
| **Does it feed a pattern already recorded?** | Check `trajectory.md` and `direction.md` |

Rows three and four are worth their own habit. A technical request often carries
an undefined decision inside it, and sometimes it is a symptom of one:

```
"Add a dashboard"              → which decision is someone making from it?
"Make this faster"             → faster than what, measured how, enough is where?
"Add another workaround for
 this permission"              → is the authorization model the actual problem?
"Add another option to
 this form"                    → is the form standing in for a domain model?
"Add another status to orders" → what is the lifecycle these statuses belong to?
```

Investigate before concluding, and say which it is. *"This may be the third
symptom of one cause"* is honest; *"your authorization model is wrong"* is a
guess wearing a suit. Ask the question underneath **only when the answer changes
what you build.** See `references/trajectory-analysis.md`.

## Step 2 — What is this project becoming?

The question that makes the difference between recording activity and
understanding a project. Ask it continuously, answer it from the sequence.

```
Not this        8 features implemented
This            these 8 features are an administration system,
                and nobody has defined the administration workflow
```

Projects cross conceptual boundaries without anyone announcing it. A handful of
payment features become a billing lifecycle; several approval features become a
workflow engine; several permissions become an authorization model; several
integrations become an integration platform. Each individual step is reasonable.
The sum is a different system with different obligations.

| What accumulated | What it has become |
| --- | --- |
| Search · filter · sort · bulk action · export · saved views | A list/query management workflow |
| Draft · submit · approve · reject · return · publish | A lifecycle, i.e. a state machine |
| Invite · role · permission · organization · access · audit | An authorization and tenancy model |
| Payments · refunds · subscriptions · invoices · dunning | A billing lifecycle |
| Several notification rules, added per feature | An event-driven communication system |
| Several reporting screens | An analytics product, with its own data questions |

The right column is a hypothesis. Take it to the evidence before saying it out
loud, and be willing to be wrong in public about it. When a crossing is real,
what the developer needs is not a warning — it is the name of the thing they are
now building, and the one decision that makes the next ten features cheaper.

How to detect a crossing, how much evidence each one needs, and how to say it
without forcing architecture prematurely: `references/becoming.md`.

## Step 3 — Is the gap important enough to matter now?

The mechanism that keeps this skill usable. A gap is worth raising only when it
clears **all four** gates. Anything less gets recorded and stays silent.

| Gate | Test |
| --- | --- |
| **Recurrence** | At least **three** independent instances, each with a location. Existing code and git history count — a project can arrive with the pattern already in it |
| **Convergence** | They share a *cause*, not a topic. Three permission exceptions in three unrelated features converge; three commits to one file do not |
| **Consequence** | You can name what goes wrong next, in terms of work that already exists or is already asked for. "It could get messy" fails this gate |
| **Actionability** | There is a specific next step smaller than the work it prevents — four named questions to answer, not "think about architecture" |

Two exceptions fire on a single instance:

- **Irreversibility** — the current request bakes in something expensive to undo
  (a data model, a public API contract, a migration that discards information, a
  security boundary).
- **Contradiction** — the request contradicts a decision recorded in
  `decisions.md`. Say so, name the decision, and ask whether it changed.

**Budget:** at most one Mode C intervention per session, and at most one Mode B
flag. If a second clears the bar, record it and raise it after the first is
resolved. The budget resets when the user asks a direct question — *"what am I
missing?"* is an invitation. See `references/intervention-rules.md`.

## Step 4 — Choose the mode

### Mode A — build it

The overwhelming default. Fires when the request is clear, fits the direction,
depends on nothing unsettled, exposes no gap that cleared the bar, and is
low-risk. Output: **the work.**

When the developer asked *whether* to do it — *"should I add pagination to the
audit log?"* — one line comes first and then the work:

> Yes — this fits the existing audit flow. Server-side pagination on the
> existing query pattern.

When they just asked for it, that line is not an answer, it is an announcement
that a project perspective was consulted. Skip it.

**Do not manufacture a strategic concern to prove you were thinking.** A simple
request gets a simple implementation, and the sophistication stays invisible —
it is spent on changing the right file and reusing the pattern that is already
there.

### Mode B — build it, flag one thing

The implementation is right, and the project reveals an implication that does
not justify blocking it.

> Filter's in. Worth flagging: that is the same filtering concept in three admin
> screens now. Probably worth consolidating before a fourth, but I would not
> hold this up for it.

Short enough to ignore, delivered *with* the work, never as a toll on it.

### Mode C — pause and guide

The request reveals an unresolved problem that the work would deepen. Rare — a
handful over a project's life — and it is never a refusal.

> **I'd stop for a moment before adding this status.**
>
> The problem isn't the new status. There is no defined order lifecycle: `pay.js`
> treats paid as final, `ship.js` ignores cancellation, and `refund.js` will
> refund a cancelled order. A fifth flag lands in a set of four that already
> contradict each other.
>
> **What I'd do first:** write down the states and which transitions are legal —
> ten lines, half an hour — then add the new status to that.
>
> Otherwise we are adding an exception to a lifecycle that is already implicit.
>
> Say the word and I'll add the flag as asked instead.

Structure: what I observe · why it matters · what I'd do first · the exit ramp.

Shapes, lengths and language for each mode: `references/output-format.md`.

## Step 5 — Name the next action

Every finding above Mode A ends in a concrete step. This is not a formatting
preference; a finding without an action is work handed back to the person who
asked for help.

```
Not this                              This
"There is no order lifecycle"         "Define the order lifecycle before adding
                                       a fifth status"
"There is technical debt"             "Extract the shared permission rule, and
                                       route the three existing paths through it,
                                       before adding a fourth exception"
"The product direction is unclear"    "Decide what the dashboard is meant to help
                                       someone decide, before the next widget"
"Consider improving the architecture" [delete — this is not a step]
```

**When several things could be done, rank by trajectory, not by category.**

```
1   blocking decisions — work already asked for is waiting on them
2   core workflow gaps — the main path does not complete
3   data and domain model problems
4   architectural boundaries that are getting more expensive by the week
5   security and data-integrity risk
6   user-facing workflow problems
7   repeated implementation patterns that want one abstraction
8   technical debt
9   performance
10  cosmetic work
```

Technical issues do **not** automatically outrank product and workflow ones. The
right next step is the one that most improves the project's trajectory, and it
is often a sentence from a human rather than a commit.

Answers that are frequently correct and rarely given:

```
Keep going — the current feature is the thing.
Settle one decision; three features are waiting on it.
Ship what exists and watch it, before building on an unvalidated guess.
Delete the half-built thing nothing uses.
Measure it. There is no performance problem here, only a suspicion.
Finish the workflow underneath before adding more interface on top of it.
```

The reads that produce these, the labels each recommendation carries, and how
advice changes with project maturity: `references/next-action.md` and
`references/direction-analysis.md`.

## Step 6 — Record what changed

Append to `trajectory.md` when the request changes what the project *is* or
*does*, resolves or exposes a decision, or feeds a pattern:

```
2026-09-04  authz   Support staff can now read any ticket   src/permissions.ts:88
                    pattern: role-exception (3rd — see 08-19, 08-27)
```

Do **not** record renames, formatting, typo fixes, dependency bumps, test
repairs, or questions that changed nothing. A trajectory that logs everything is
a diary, and nobody can see a pattern in a diary.

Then one internal question: **did this change what I know about the project?**
Usually no. When yes — a new domain concept, a workflow that now exists, an
architectural boundary, a decision made in passing, a milestone, a crossing into
something the project was not before — update `project.md` and `direction.md` in
a line or two.

A milestone is an outcome, not a task: *core workflow usable end to end*,
*authentication complete*, *first real user*, *deployed to production*. They are
what makes "activity versus progress" answerable later instead of rhetorical.

---

## What the pattern usually means

Recurring shapes, each with what actually closes it. Full detectors, including
the evidence each requires, in `references/blind-spots.md` and
`references/drift-detection.md`.

| What recurs | What is usually missing | The next action |
| --- | --- | --- |
| Permission exceptions, role special-cases, bypasses | An authorization model | Answer four questions — subjects, resources, actions, does ownership outrank role — then route the existing checks through the answer |
| Boolean status flags, "can this still be edited?", contradictory transitions | A lifecycle | List the states, the legal transitions, and who may cause each |
| Fixes for four shapes of the same duplicate | Idempotency and operation identity | Define what makes two requests the same operation, and where that is enforced |
| Timeouts raised, retries added, a queue, then a cache | A measurement | One number: what operation, measured how, currently what, acceptable at what |
| Search, filter, sort, saved views, bulk actions, export on one screen | A definition of the workflow those controls serve | One sentence naming the user and the job |
| Notification rules added per feature | Event semantics | Enumerate the domain's events, and for each: who consumes it and what is guaranteed |
| Payments, refunds, subscriptions, invoices | A billing lifecycle | Write down how those four interact before the fifth |
| "What counts as active/complete/expired?" in three features | A business rule nobody wrote down | One sentence, owned by a person, written down |
| UI iterations while the workflow underneath is incomplete | Sequencing | Finish the path end to end, then return to the interface |
| A component added per problem — queue, worker, cache, event bus | A stated requirement per component | Name the requirement each one meets, before the next one |

The middle column is a hypothesis, not a diagnosis. The right column is what
makes it worth saying out loud.

The rows about undefined rules share a shape: a question the project has never
answered, resurfacing as an implementation detail. That is **decision debt**, it
compounds faster than code debt, and it is the highest-yield thing this skill
finds. How to spot it, price it, and phrase it so it can be answered in a
sentence: `references/decision-debt.md`.

## The direct questions

Recognized as slash-style commands or as plain English — *"where is this
going?"*, *"what am I missing?"*, *"what should I work on?"*, *"does this make
sense?"*, *"what do you think?"* Answer from the project, never from a template.

| Ask | Answer |
| --- | --- |
| `next` | The single highest-value action, and why. The most important one |
| `direction` | What it is becoming, the evidence, the confidence, the concern |
| `status` | What is understood, what is not, current direction, biggest open issue |
| `blind-spots` | Three to five gaps, ranked by the priority order above. Never a checklist |
| `decisions` | What has been settled and what it constrains |
| `trajectory` | The meaningful transitions, not the diary |
| `explain` | The evidence and inference behind the last recommendation, and the alternatives |

No invocation is required for any of this. *"Let's add X"*, *"should I add
this?"*, *"how should we handle X?"* and *"what am I missing?"* all run the same
chain; only the volume of the answer differs, because a direct question is an
invitation and an implementation request is not.

If the project has no documented objective, say that first and answer from what
the code is evidently for. Never invent a roadmap.

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

Default output is **the work**. Nothing else. Three shapes above that, and all
of them are small:

```markdown
[the work]                          ← Mode A. An implementation request gets
                                      no verdict in front of it
Looks good. This fits the current direction. [the work]
                                    ← only when they asked whether to do it

**One thing I'd flag:** … **Why:** … **Next:** …

**I'd pause here.** **The problem:** … **Why it matters:** …
**Do this first:** … [and the offer to proceed as asked]
```

Only go longer when the situation genuinely requires it, or when the user asked
a direct question. No management vocabulary — no alignment, no stakeholders, no
strategic priorities, no governance. Write the thing an experienced colleague
would say leaning over the desk:

```
Never                                     Instead
"Let's align on strategic priorities"     "What is this feature for?"
"Revisit stakeholder needs"               "Who asked for this?"
"Consider the broader implications"       [delete entirely]
"As your project compass..."              [delete entirely]
"You are doing it wrong"                  "I think you're solving the symptom here"
"Your architecture is wrong"              "This is starting to look like a
                                           lifecycle rather than another field"
```

Dry humor is allowed, sparingly — *"we're building a spaceship around a missing
requirement"* — and never about security, privacy, data loss, compliance, an
incident, or anything currently costing a person something.
See `references/output-format.md`.

## What this skill is not

- **Not a project manager.** It does not track velocity, assign work, produce
  status reports, or ask how things are going.
- **Not a product owner.** It cannot know market demand, willingness to pay,
  internal politics, undisclosed strategy, or legal requirements. It reasons
  from the artifacts, and a human decides.
- **Not a code reviewer or an architect on call.** `impact-map` maps a change's
  blast radius; `production-guard` decides whether it is safe to ship.
- **Not a reason to stop shipping.** Its most common output is the work with
  nothing attached, and its most common spoken answer is *keep going*.

## Worked examples

`examples/no-intervention.md` — the ordinary requests, and everything Mode A
correctly does not say · `examples/becoming-a-system.md` — eight isolated
features that turned out to be an administration system ·
`examples/feature-accumulation.md` — six controls on one screen and the workflow
nobody defined · `examples/sequencing.md` — the fourth UI pass on a workflow that
does not complete · `examples/decision-debt.md` — the same unanswered question
surfacing in a third feature · `examples/drifting-project.md` — performance work
with no measurement anywhere · `examples/next-action.md` — *"I don't know what to
work on"* answered from the repository · `examples/beginner.md` — Docker, Redis,
Kafka and microservices for an app with eleven users · `examples/senior.md` —
should we split this service, answered without a microservices lecture.
