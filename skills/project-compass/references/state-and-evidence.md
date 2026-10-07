# State and Evidence

## Contents

- Evidence model
- The project state
- Engineering state

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
