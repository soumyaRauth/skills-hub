# Project Compass

### Your agent knows how to build things. This helps it work out what to build next.

Project Compass is an [Agent Skill](https://code.claude.com/docs/en/skills) that
answers one question before every non-trivial request:

> **Given everything I know about this project, what should this developer do
> next, and why?**

Usually the answer is *the thing they just asked for*, and it builds it and says
nothing. Occasionally it is not — and on those occasions the answer is worth
more than the implementation would have been.

```bash
npx skills add soumyaRauth/skills-hub --skill project-compass
```

---

## The problem

Coding agents execute well. Ask for search, a refactor, another permission
check, a dashboard — you get all of them, competently, one after another.

That is the whole problem. Execution never asks whether the sequence adds up.

```
ACTIVITY   features added, code refactored, endpoints optimized
PROGRESS   the target problem solved, a real risk retired, a workflow completed
```

These come apart quietly. Nine permission exceptions, each reasonable, are an
authorization system nobody designed. Four fixes for four kinds of duplicate are
one missing idea about identity. Five performance changes with no measurement
anywhere are five guesses with deployments attached.

And the version that costs the most:

```
Add search.        Add export.          Add user groups.
Add filtering.     Add bulk delete.     Add permissions.
Add sorting.       Add saved filters.
```

Eight reasonable requests. Together they say *we are building an administration
system and nobody has defined the administration workflow* — which is a sentence
no single request could produce, and which the person making them cannot see,
because they see one request at a time.

## The change

```
Normal coding agent          Project Compass

request                      request
  ↓                            ↓
implementation               what is actually being asked?
                               ↓
                             what does this project look like now?
                               ↓
                             what has it been becoming?
                               ↓
                             what does this request assume, and what does it touch?
                               ↓
                             is there an unresolved gap underneath it?
                               ↓
                             does that gap matter now?  ── almost always no
                               ↓
                             what is the best next action?
                               ↓
                             implementation
```

Everything above the last two rows is cheap. Everything below them is unchanged.

## Three modes, and the first one is the default

Every request lands in one of three:

**Mode A — build it.** The overwhelming majority. The request fits, nothing is
unresolved, nothing is at risk. Build it, say nothing about direction. No
manufactured concerns, no *"this looks fine from a project perspective"*.

**Mode B — build it, flag one thing.** The implementation is right and the
project reveals something worth one paragraph, delivered *with* the work and
short enough to ignore.

**Mode C — pause and guide.** The request runs into an unresolved problem the
work would deepen. Rare, never a refusal, and it always ends with the offer to
build it as asked.

```
You:    Add another status to orders.

Agent:  I'd stop for a moment before adding this status.

        The problem isn't really the new status — there's no defined order
        lifecycle. pay.js treats paid as final, ship.js doesn't check
        cancellation, and refund.js will refund a cancelled order. A fifth flag
        lands in a set of four that already contradict each other.

        What I'd do first: write down the states and which transitions are
        legal. Ten lines, half an hour. Then the new status goes into that
        instead of becoming a fifth exception.

        Say the word and I'll just add the flag — you may know something the
        repository doesn't.
```

Nothing was refused. The alternative is smaller than the work it replaces, it is
startable today, and the evidence is three file names you can check in thirty
seconds.

## Every finding ends in an action

An observation is half a sentence. The deliverable is the other half.

| Not this | This |
| --- | --- |
| "There is no order lifecycle" | "Define the order lifecycle before adding a fifth status" |
| "There is technical debt" | "Extract the shared permission rule and route the three existing paths through it, before the fourth exception" |
| "The product direction is unclear" | "Decide what the dashboard is meant to help someone decide, before the next widget" |
| "Consider improving the architecture" | *[deleted — this is not a step]* |

When several things could be done, they are ranked by what most improves the
project's trajectory — blocking decisions, then broken core workflows, then
domain-model problems, then boundaries getting expensive, then security and data
integrity, and only then debt, performance and polish. **Technical issues do not
automatically outrank product and workflow ones.**

## The harder half: knowing when to shut up

An agent that comments on project direction four times a week gets uninstalled
in week two, and the one real observation it would have made in week nine never
arrives.

So Mode B and Mode C fire only when a gap clears **four gates**:

| Gate | Test |
| --- | --- |
| **Recurrence** | Three or more independent instances, each with a location you can name |
| **Convergence** | They share a *cause*, not a topic — could one decision have prevented all three? |
| **Consequence** | You can say what breaks next, in terms of work already asked for. *"This could get messy"* fails |
| **Actionability** | There is a step smaller than the work it prevents. *"Consider defining an authorization model"* is not a step |

Three out of four is a note in the project state, not a sentence to you. On top
of that: **one intervention per session, maximum**, and

> **a dismissed observation is closed permanently.**

Say *"that's intentional"* and it is recorded as a decision with your reason, and
never raised again — not next week, not in different wording. Say *"this is a
throwaway prototype"* or *"I'm experimenting"* and that becomes the frame every
later recommendation is measured against, because you know the goal and it does
not.

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill project-compass
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill project-compass --agent claude-code
```

No slash command needed — installed skills are matched by description, and
ordinary development supplies the evidence. It engages on its own when a request
touches something unresolved, and answers directly when you ask:

```
What should I work on next?          Should I add this?
What should I build now?             Does this make sense?
Where is this project going?         How should we handle X?
What do you think I'm missing?       Am I overengineering this?
```

## What it remembers

```
.project-compass/
├── project.md          what this is, who it serves — labeled, dated
├── direction.md        what it is becoming, the biggest gap, the next step
├── trajectory.md       dated entries: what changed, and which pattern it fed
├── decisions.md        settled questions, including "we discussed this, proceed"
├── open-questions.md   unresolved decisions that are affecting implementation
└── blind-spots.md      gaps that cleared the bar, and what closes them
```

`direction.md` is the one that earns its keep fastest — it is *"what should I do
next?"*, cached, so the answer next week costs one file read instead of a second
reconstruction of the project:

```markdown
**Appears to be**  Team task tracker
**Becoming**       A list/query management workflow          INFERRED (High)
**Biggest gap**    Nobody has said who the list screen is for; three features
                   already disagree about what a task is on it
**Next step**      One sentence naming the user and the job of that screen,
                   before the eighth control goes on it
**Not yet said**   nothing is blocked; raise at the next control request
```

This is the difference between the skill and asking an agent *"what am I
missing?"* — that question gets a fresh guess from nothing, every time. This
accumulates, and it is more useful in week eight than on day one.

The purpose of every file is **better guidance later**, not a record of what
happened. A first session usually writes `project.md` and nothing else; renames,
formatting and dependency bumps are never recorded, because a trajectory that
logs everything is a diary and nobody finds a pattern in a diary. The repository
always outranks the state: recorded claims are re-verified before anything is
built on them.

Creating that directory is the only write the skill makes outside the work you
asked for. It is announced once, in a line, and never mentioned again — and if
you would rather not have it, it degrades to single-session reasoning without
arguing about it.

## Everything is labeled

| | Means |
| --- | --- |
| `OBSERVED` | Read directly — with the location |
| `INFERRED` | Concluded, with High or Low confidence, and what would overturn it |
| `ASSUMED` | Believed to make progress, unverified — and what breaks if wrong |
| `UNKNOWN` | Established as not known, and what would settle it |

It will not invent your project's purpose, users, market, deadlines, metrics, or
history. When the objective is undocumented, *"there is no documented
objective"* is the finding — usually a useful one — and the recommendation says
which part of itself that limits.

## What it notices

| What accumulated | What it has become | What to do about it |
| --- | --- | --- |
| Search · filter · sort · saved views · bulk · export | A list-management workflow | One sentence naming who uses the screen and what they are finishing |
| Draft · submit · approve · reject · publish | A lifecycle | List the states, the legal transitions, and who may cause each |
| Invite · role · permission · org · access · audit | An authorization model | Subjects, resources, actions — and does ownership outrank role |
| Payments · refunds · subscriptions · invoices | A billing lifecycle | Write down how those four interact, before the fifth |
| Notification rules added per feature | An event system | Enumerate the real events, their consumers, their guarantees |
| Timeout · retry · queue · cache · Redis | Five guesses | One number: what is slow, measured how, acceptable at what |
| Fixes for four shapes of the same duplicate | A missing identity | Define what makes two requests the same operation |
| UI passes while the workflow underneath breaks | A sequencing problem | Finish the path end to end, then return to the interface |

Each detector requires specific evidence before it fires, and every one of them
is a hypothesis until it has been checked against the code.

## Answers it is willing to give

Most agents will build whatever you ask. This one is allowed to say:

```
Keep going — this is the thing. (The most common non-silent answer.)
Settle one decision; three features are waiting on it.
Finish the workflow underneath before adding more interface on top of it.
Ship it and watch. Four passes on a working screen is guessing.
Measure it first. There is no performance problem here yet, only a suspicion.
Delete it. Nothing uses it and it is charging rent.
Write down the rule. It currently lives in four conditionals that disagree.
```

And, rarely and with the evidence attached, *I can build this, but I don't think
it is what the project needs right now* — always ending with the offer to build
it anyway, because you have context the repository does not.

## Worked examples

- [**No intervention**](examples/no-intervention.md) — five ordinary requests in
  a project with a real open gap, and every temptation Mode A suppresses
- [**Becoming a system**](examples/becoming-a-system.md) — eight isolated
  features that turned out to be an administration console
- [**Feature accumulation**](examples/feature-accumulation.md) — six controls on
  one screen and the workflow nobody defined
- [**Sequencing**](examples/sequencing.md) — the fifth UI pass on a workflow that
  does not complete, and the fourth one that correctly got no comment
- [**Decision debt**](examples/decision-debt.md) — the same unanswered question
  surfacing in a third feature, asked so it takes one word to answer
- [**A drifting project**](examples/drifting-project.md) — five solutions to a
  problem nobody measured
- [**What should I do next**](examples/next-action.md) — answered from the
  repository, including what *not* to do
- [**Beginner**](examples/beginner.md) — Docker, Redis, Kafka and microservices
  for an app with eleven users
- [**Senior**](examples/senior.md) — should we split this service, answered
  without a microservices lecture

## References

The skill loads these on demand.

| | |
| --- | --- |
| [`next-action.md`](references/next-action.md) | The decision chain, the ranking, the concreteness tests, sequencing, and what a stated goal overrides |
| [`becoming.md`](references/becoming.md) | Crossings — when features have become a system, the evidence each needs, and how to say so without forcing architecture |
| [`direction-analysis.md`](references/direction-analysis.md) | Stated versus actual versus structural direction, and the `direction.md` file |
| [`project-model.md`](references/project-model.md) | The dimensions of a project, what evidence establishes each, and the reading order that gets there fastest |
| [`project-state.md`](references/project-state.md) | The state directory: formats, write triggers, size budgets, staleness, resuming |
| [`evidence-model.md`](references/evidence-model.md) | The four labels, strong versus weak inference, the source hierarchy, anti-fabrication |
| [`trajectory-analysis.md`](references/trajectory-analysis.md) | Turning requests into concepts, reading a sequence, getting from entries to structure |
| [`intervention-rules.md`](references/intervention-rules.md) | The four gates, mode selection, the budget, stated intent, dismissal, when never to speak |
| [`drift-detection.md`](references/drift-detection.md) | Telling drift from focused work — and the long list of things that are not drift |
| [`blind-spots.md`](references/blind-spots.md) | Eleven detectors, the evidence each one requires, and what closes it |
| [`decision-debt.md`](references/decision-debt.md) | Spotting unanswered questions, pricing them, and phrasing them to be answerable in a word |
| [`adaptive-expertise.md`](references/adaptive-expertise.md) | The same finding at four densities, without condescension in either direction |
| [`output-format.md`](references/output-format.md) | Shapes per mode, language, humor, and what never appears in output |

## What it is not

- **Not a project manager.** No velocity, no status reports, no asking how it is
  going.
- **Not a product owner.** It cannot know market demand, willingness to pay,
  politics, undisclosed strategy, or legal requirements. It reasons from the
  artifacts; a human decides.
- **Not a code reviewer.** [Impact Map](../impact-map/README.md) maps a change's
  blast radius; [Production Guard](../production-guard/README.md) decides whether
  it is safe to ship.
- **Not a reason to stop shipping.** Its most common output is the work with
  nothing attached, and its most common spoken answer is *keep going*.

## Limitations

- It sees the repository and the conversation. Everything else — your users,
  your market, what a stakeholder promised — is invisible, and it says so rather
  than guessing.
- Value compounds with use. A first session on an unfamiliar repository can
  reconstruct a project model, but a trajectory takes weeks to become one.
- Inherited history helps: on a repository that arrives with a pattern already
  in it, git history counts as evidence from the first session.
- Reading direction is judgment, not analysis. It will sometimes read focused
  work as a pattern; the four gates exist to make that rare, and being overruled
  costs one sentence.
- It cannot tell you whether your idea is good. It can tell you that nothing in
  the repository connects it to anything else.
- The state directory is only as good as what has been recorded through it. Work
  done outside the agent is invisible unless it left a commit.

## License

[MIT](../../LICENSE)
