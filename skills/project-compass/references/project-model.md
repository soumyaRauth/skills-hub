# The project model

What to understand about a project, what evidence establishes each part, and —
more important — what to write when the evidence is not there.

Do not fill this in as a questionnaire on first contact. Build it from what a
session already needed to read, and leave the rest `UNKNOWN`. A model with four
solid lines beats one with eighteen guesses.

## Reading order

Twenty minutes of reading, in the order that establishes the most per minute:

```
1  README, and any docs/ or adr/ directory      what it says it is
2  package manifest / dependency file           what it is built out of
3  The schema, or the model/entity definitions  what it actually holds
4  Route table, CLI entrypoints, or page list   what it lets people do
5  The single most-changed file (git log)       where the work actually lives
6  The last 30 commit subjects                  what has been happening lately
7  Test names                                   what the team believed mattered
```

Step 3 is the highest-yield read in most codebases. Entities and their
relationships tell you the domain, the multi-tenancy story, the lifecycle, and
usually the authorization model, in one file.

Step 5 is the highest-yield read that people skip:

```bash
git log --format= --name-only --since='3 months ago' \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -20
```

Where the churn is concentrated is where the project's unresolved problem lives.

## The dimensions

Each line below: what to read, what it establishes, and the conclusion it does
**not** support.

**Identity** — what this is.
Read the README, the manifest name, the entrypoints. If the README describes
something the code has outgrown, record both. *Does not establish:* who it is
for.

**Purpose** — the problem it solves.
Read docs, the first commits, issue templates, the vocabulary in the UI. Often
`UNKNOWN`, and honestly so. *Does not establish:* business value, priority, or
whether anyone wants it.

**Users** — who uses it.
Read the roles in the schema, the auth flows, the language in the interface, the
seed data. A single-role system with an admin flag is a different product from
one with an org hierarchy. *Does not establish:* how many, or how they feel.

**Core workflows** — the primary journeys.
Read routes, navigation, and the sequences the tests exercise. A workflow is a
path, not a screen: *intake → adjustment → approval → reconciliation*. When
features cluster on a screen with no path through it, that is the finding in
`blind-spots.md`, not a workflow.

**Domain model** — the concepts and their relationships.
Read the schema, the type definitions, the language of the code. Note the
concepts that exist in the *vocabulary* but not in the *model* — a codebase that
says "subscription" in twelve places with no subscription entity is telling you
something.

**Data model** — what information exists and how it moves.
Read migrations in order; they are the project's real history. What was added,
what was backfilled, what was nullable-then-required, what got soft-deleted
instead of deleted.

**Authorization model** — who can do what.
Read for a *rule*, not for checks. If authorization exists only as inline
conditions at call sites, record: `no authorization model; N inline checks at
[locations]`. That absence is the single most common high-value finding this
skill makes.

**State / lifecycle model** — what things become.
Read status columns, enums, boolean flags, and transition code. Four booleans
that cannot legally be true together are a state machine nobody has written
down. Record the illegal combinations you can find — they are the evidence.

**Integration model** — what outside systems matter.
Read config, env examples, HTTP clients, webhook handlers. Note what happens
when each one is down; usually nothing is written, which is a real finding on a
project that takes money.

**Operational burden** — what this software commits someone to doing.
Read for things that need a human when they go wrong: manual steps in a
workflow, a support path implied by a feature, data that has to be corrected by
hand, anything that generates a customer conversation. New burden is a real cost
of a feature and it is almost never in the ticket. *Does not establish:* who
carries it — ask.

**Constraints** — what cannot easily change.
Read for public API contracts, published schemas, data that cannot be
re-derived, compliance-shaped code, and anything a customer already depends on.
Constraints are what turn a Mode B flag into a Mode C pause.

**Decisions** — what has been settled.
ADRs if they exist; otherwise commit messages, code comments explaining *why*,
and anything the user has said in this or a previous session.

**Assumptions** — believed but unverified.
Every one of these is a candidate question. Track them because assumptions are
what interventions turn out to have been built on when they are wrong.

**Open questions** — unresolved and affecting implementation.
The filter is the second half. Undefined things that nothing is waiting on are
not open questions, they are just software.

**Direction** — what the work has been doing lately, and what that adds up to.
Read the last thirty commits, the newest tables, and the trajectory together.
This is the dimension the recommendation actually comes from, and it is the one
most likely to disagree with the README. *Does not establish:* whether the
direction is deliberate — only the user can say that. See
`direction-analysis.md` and `becoming.md`.

**Current gap** — where the project is, versus where the evidence says it needs
to be next. Not a list of everything undefined: the one or two things that work
already in progress is waiting on, guessing at, or working around.

## Knowledge debt

Some code exists for a reason nobody remembers. It looks removable and is not.

```bash
git log -S'the odd condition' --format='%h %ad %s' --date=short -- path/to/file
```

A strange rule introduced in a commit named *"hotfix: duplicate charges on
retry"* is not cruft — it is an incident, encoded. Record it under Decisions
with its origin, and never recommend removing behavior whose reason is
`UNKNOWN`. Say instead: *this looks unnecessary; before removing it, find out
what it was for.*

## Writing it down

`project.md` stays under a page. It is read at the start of every session — a
long one gets skimmed, and a skimmed model is a wrong model.

```markdown
# Project

**Is**        Multi-tenant inventory app for warehouse teams        OBSERVED
**For**       Warehouse managers; a separate admin role exists      OBSERVED
**Objective** UNKNOWN — not stated in README, docs, or commits
**Workflows** intake → adjustment → approval → reconciliation       OBSERVED
              reporting exists but connects to nothing              OBSERVED
**Domain**    Organization · Warehouse · Product · Adjustment       OBSERVED
**Authz**     No model. 6 inline role checks, 2 with exceptions     OBSERVED
              src/api/{adjustments,reports,users}.ts
**Lifecycle** Adjustments: draft/submitted/approved via 3 booleans  OBSERVED
              Illegal combinations are reachable                    INFERRED (High)
**Assumes**   Refund window is 30 days — one hardcoded constant,    ASSUMED
              no policy anywhere. Breaks: any refund logic built on it
**State**     DIRECTED — reconciliation work is coherent
**Verified**  2026-09-06
```

That fits on a screen, every line points at something re-checkable, and the two
weakest lines are labeled as the weakest lines.

What the project is *becoming*, and the next step that follows from it, live in
`direction.md` rather than here — they change on a different clock, and mixing
the two produces a model nobody trusts because half of it is always out of date.
