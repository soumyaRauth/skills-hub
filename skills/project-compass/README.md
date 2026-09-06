# Project Compass

### Your agent knows how to build things. This helps it understand where the project is going.

Project Compass is an [Agent Skill](https://code.claude.com/docs/en/skills) that
builds an evidence-based understanding of a project — what it is, what has been
decided, what keeps recurring, where the work is heading — and uses it to notice
the thing the person making one request at a time cannot see.

Then, almost always, it says nothing and does the work.

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

These come apart quietly. A project can accumulate a year of good commits and be
further from working than it was in month three — not because anyone did bad
work, but because nobody was reading the requests as a sequence. Nine
permission exceptions, each reasonable, are an authorization system nobody
designed. Four fixes for four kinds of duplicate are one missing idea about
identity. Five performance changes with no measurement anywhere are five
guesses with deployments attached.

The person making the requests cannot see this. They see one request.

## The change

```
Normal coding agent          Project Compass

request                      request
  ↓                            ↓
implementation               project state — what is known, decided, recorded
                               ↓
                             does this fit the trajectory?
                               ↓
                             does it depend on something unresolved?
                               ↓
                             has this pattern happened three times?
                               ↓
                             is it worth interrupting for?   ── almost always no
                               ↓
                             implementation
```

The last two steps are the skill. Everything above them is cheap, and everything
below them is unchanged.

## The moment it is built for

```
You:    Add CSV export to the members table.

Agent:  Export added — all visible columns, respecting the current filter and
        sort, streamed so large orgs don't time out.

        One thing I'd flag. That's six controls on this table since August:
        search, filters, sorting, saved views, bulk actions, now export. Each
        made sense on its own, but they're pointing at a workflow nobody has
        written down — and it's already showing: saved views track role, status
        and joined date, bulk actions work on role and active, and export just
        took everything.

        Before the seventh, one sentence would settle it: who opens this screen,
        and what are they trying to finish? If it's "support checks whether
        someone still has access", the table needs three columns and a search
        box and half of what's there is in the way. If it's "an admin does
        quarterly access reviews", export is the main event and should probably
        be scheduled rather than clicked.
```

Nothing was refused. The export was built and tested. The observation is
checkable in thirty seconds — six controls, five dates, three inconsistent
column sets — and the missing thing is one sentence from a human, not a
refactor.

## The harder half: knowing when to shut up

An agent that comments on project direction four times a week gets uninstalled
in week two, and the one real observation it would have made in week nine never
arrives.

So a pattern is reportable only when it clears **four gates**:

| Gate | Test |
| --- | --- |
| **Recurrence** | Three or more independent instances, each with a location you can name |
| **Convergence** | They share a *cause*, not a topic — could one decision have prevented all three? |
| **Consequence** | You can say what breaks next, in terms of work already asked for. *"This could get messy"* fails |
| **Actionability** | There is a step smaller than the work it prevents. *"Consider defining an authorization model"* is not a step |

Three out of four is a note in the project state, not a sentence to you. On top
of that: **one interruption per session, maximum**, and

> **a dismissed observation is closed permanently.**

Say *"that's intentional"* and it is recorded as a decision with your reason,
and never raised again — not next week, not in different wording. That one rule
is what makes the skill survivable past month two.

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill project-compass
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill project-compass --agent claude-code
```

No slash command needed — installed skills are matched by description. It
engages on its own when a request touches something unresolved, and answers
directly when you ask:

```
What should I work on next?
Where is this project going?
What do you think I'm missing?
Am I overengineering this?
Why do I keep running into this?
What have we not thought about?
```

## What it remembers

```
.project-compass/
├── project.md          what this is, who it serves, what it must do — labeled, dated
├── trajectory.md       dated entries: what changed, and which pattern it fed
├── decisions.md        settled questions, including "we discussed this, proceed"
├── open-questions.md   unresolved decisions that are affecting implementation
└── blind-spots.md      patterns that cleared the bar, and what closes them
```

This is the difference between the skill and asking an agent *"what am I
missing?"* — that question gets a fresh guess from nothing, every time. This
accumulates, and it is more useful in week eight than on day one.

Only what carries state gets written. A first session usually writes
`project.md` and nothing else, `blind-spots.md` may never exist, and renames,
formatting and dependency bumps are never recorded. A trajectory that logs
everything is a diary, and nobody finds a pattern in a diary.

The repository always outranks the state: recorded claims are re-verified before
anything is built on them, and a claim that has gone stale gets corrected rather
than quoted.

Creating that directory is the only write the skill makes outside the work you
asked for. It is announced once, in a line, and never mentioned again — and if
you would rather not have it, it degrades to single-session reasoning without
arguing about it. It generally belongs in version control, since a decision the
whole team can see is worth more than one only an agent remembers.

## Everything is labeled

| | Means |
| --- | --- |
| `OBSERVED` | Read directly — with the location |
| `INFERRED` | Concluded, with High or Low confidence, and what would overturn it |
| `ASSUMED` | Believed to make progress, unverified — and what breaks if wrong |
| `UNKNOWN` | Established as not known, and what would settle it |

It will not invent your project's purpose, users, market, deadlines, metrics, or
history. When the objective is undocumented, *"there is no documented
objective"* is the finding — usually a useful one — and recommendations say
which parts of them that limits.

## What it notices

| What recurs | What is usually missing |
| --- | --- |
| Permission exceptions, role special-cases, bypasses | An authorization model |
| Boolean status flags, "can this still be edited?" | A lifecycle: states, transitions, who may cause them |
| Fixes for four shapes of the same duplicate | Idempotency, and what makes an operation *the same* one |
| Timeout raised, retry, queue, cache, Redis | A measurement — what is slow, and what target matters |
| Search, filter, sort, saved views, bulk actions, export | The workflow those controls serve |
| Notification rules added per feature | Event semantics |
| Payments, refunds, subscriptions, invoices | A billing lifecycle |
| "What counts as active?" asked in three features | A business rule nobody wrote down |

Each detector requires specific evidence before it fires, and every one of them
is a hypothesis until it has been checked against the code.

## Answers it is willing to give

Most agents will build whatever you ask. This one is allowed to say:

```
Keep going — this is the thing. (The most common non-silent answer.)
Ship it and watch. Four passes on a working screen is guessing.
Measure it first. There is no performance problem here yet, only a suspicion.
This is a product decision, not a technical one — one sentence unblocks three features.
Delete it. Nothing uses it and it is charging rent.
Write down the rule. It currently lives in four conditionals that disagree.
```

And, rarely and with the evidence attached, *I can build this, but I don't think
it is what the project needs right now* — always ending with the offer to build
it anyway, because you have context the repository does not.

## Worked examples

- [**No intervention**](examples/no-intervention.md) — four ordinary requests in
  a project with a real open blind spot, and every temptation the skill suppresses
- [**Feature accumulation**](examples/feature-accumulation.md) — six controls on
  one screen and the workflow nobody defined
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
| [`project-model.md`](references/project-model.md) | The dimensions of a project, what evidence establishes each, and the reading order that gets there fastest |
| [`project-state.md`](references/project-state.md) | The state directory: formats, write triggers, size budgets, staleness, resuming |
| [`evidence-model.md`](references/evidence-model.md) | The four labels, strong versus weak inference, the source hierarchy, anti-fabrication |
| [`trajectory-analysis.md`](references/trajectory-analysis.md) | Turning requests into concepts, reading a sequence, activity versus progress |
| [`intervention-rules.md`](references/intervention-rules.md) | The four gates, the budget, dismissal, level selection, timing, when never to speak |
| [`drift-detection.md`](references/drift-detection.md) | Telling drift from focused work — and the long list of things that are not drift |
| [`blind-spots.md`](references/blind-spots.md) | Ten detectors, the evidence each one requires, and what closes it |
| [`decision-debt.md`](references/decision-debt.md) | Spotting unanswered questions, pricing them, and phrasing them to be answerable in a word |
| [`direction-analysis.md`](references/direction-analysis.md) | Reconstructing direction; answering "what next"; what a repository can never know |
| [`adaptive-expertise.md`](references/adaptive-expertise.md) | The same finding at four densities, without condescension in either direction |
| [`output-format.md`](references/output-format.md) | Shapes per level, language, humor, and what never appears in output |

## What it is not

- **Not a project manager.** No velocity, no status reports, no asking how it is
  going.
- **Not a product owner.** It cannot know market demand, willingness to pay,
  politics, undisclosed strategy, or legal requirements. It reasons from the
  artifacts; a human decides.
- **Not a code reviewer.** [Impact Map](../impact-map/README.md) maps a change's
  blast radius; [Production Guard](../production-guard/README.md) decides whether
  it is safe to ship.
- **Not a reason to stop shipping.** Its most common correct output is nothing,
  and its second most common is *keep going*.

## Limitations

- It sees the repository and the conversation. Everything else — your users,
  your market, what a stakeholder promised — is invisible, and it says so rather
  than guessing.
- Value compounds with use. A first session on an unfamiliar repository can
  reconstruct a project model, but a trajectory takes weeks to become one.
- Inherited history helps: on a repository that arrives with a pattern already
  in it, git history counts as evidence from the first session.
- Pattern detection is judgment, not analysis. It will sometimes read focused
  work as a pattern; the four gates exist to make that rare, and being overruled
  costs one sentence.
- It cannot tell you whether your idea is good. It can tell you that nothing in
  the repository connects it to anything else.
- The state directory is only as good as what has been recorded through it. Work
  done outside the agent is invisible unless it left a commit.

## License

[MIT](../../LICENSE)
