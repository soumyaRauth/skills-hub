# `docs/spec.md` format

The spec is project content, not hidden state: it is committed, humans read it,
`project-compass` reads it later to know what the project is meant to be, and
`delivery-planner` turns it into milestones. Keep it to one or two screens.

## Labels

Every factual line ends with one label:

- `[you said]` — stated by the user: the request, their notes, an answer.
  Quote or closely paraphrase; never improve their words into a claim they did
  not make.
- `[assumed]` — chosen by the agent. Follow it with *what would change it*.

Lines without a label are headings and plain structure only. When the user
confirms an assumption, change its label to `[you said]`; do not delete it.

## Shape

```markdown
# <Project name> — spec

Status: draft · written <YYYY-MM-DD> · labels: [you said] = the user's words, [assumed] = a default to check

## Problem
<One or two sentences: what is painful today, for whom.> [you said]

## Users
- <Kind of user> — <what they need to do>. [you said]
- <Kind of user> — <what they need to do>. [assumed: changes if ...]

## Core workflow (v1)
The one path that must work end to end.
1. <A real person does a concrete thing.> [you said]
2. ...
(five to eight steps)

## v1 scope
- <Capability the workflow needs, and nothing else.> [you said | assumed]

## Non-goals (not in v1)
- <Thing the idea invites but v1 does not do.> [you said | assumed]

## Constraints
- Where it runs: <...> [you said | assumed]
- Money: <none in v1 | ...> [...]
- Personal data: <what is stored> [...]
- Deadline: <date, or "none stated"> [you said]
- Standards: <what standards-compass named, if it engaged>

## Open decisions
Questions that do not block v1 but will block a later milestone.
- <Question?> — blocks: <which later step>

## Stack
<Stack line and one-line reason, from stage 3.> [assumed | you said]
```

## What does not go in

- Invented numbers: member counts, prices, expected traffic, revenue.
- Screens, colours, database tables. The workflow says *what*; the tickets
  and the code say *how*.
- A roadmap. Milestones belong to `delivery-planner` in `.delivery/plan.md`.
- Secrets, hostnames with credentials, or real personal data from the user's
  business.

A deadline appears only when the user gave one. `Deadline: none stated` is a
correct line; `Deadline: end of quarter [assumed]` is not allowed.
