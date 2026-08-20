# Contributing

These are skills, not programs. Their quality is the quality of their reasoning
instructions, so contributions are judged on whether they make the agent's
analysis **more accurate and better evidenced** — not on whether they make it
produce more output.

## The two hard rules

### 1. Do not make the skills more speculative

A finding without evidence costs the reader more time than no finding at all,
and it teaches them to distrust the whole report. A single confident-sounding
guess does more damage than ten missed files, because a missed file gets caught
in review while a wrong claim gets acted on.

So: never add instructions that encourage the agent to list files "that might be
related", to guess at external consumers, to estimate counts, or to promote a
plausible hunch to MUST CHANGE or BLOCKER. If something cannot be evidenced, its
home is NEEDS VERIFICATION, UNVERIFIED, or OPEN QUESTIONS.

**Why false positives are worse than misses.** A missed finding gets caught in
review by a human who was going to look anyway. A false positive costs that human
the time to investigate, and each one lowers the odds they read the next report
carefully. A tool that cries wolf three times gets muted before the real fire.

### 2. No invented numbers

Never add instructions that produce a number the agent did not compute:

- No fabricated file counts ("184 files examined")
- No quality percentages, letter grades, or composite scores
- No claiming a check ran when it did not
- No `ACTUAL` value in a failure matrix for a scenario that was only reasoned about

`18/20 checks passed` is a fact. `91% production ready` is an invention that
sounds like a fact, which is what makes it worse than saying nothing. If a
summary score is ever added, it must come from a documented, reproducible scoring
system — and `scripts/validate.sh` fails the build on the anti-pattern to keep
it out of the docs.

## Ways to contribute

### Improve a methodology

Edits to `skills/<skill>/SKILL.md`. Highest-value and highest-risk, so:

- Keep it **concise**. SKILL.md holds the workflow and the behavioral rules;
  everything deeper belongs in `references/`. Length is a cost — a bloated skill
  file gets skimmed, and the rules that matter get diluted.
- Prefer sharpening an existing rule over adding a new one.
- Every rule should change what the agent *does*. Advice with no observable
  effect on the output is decoration.
- Test the change against at least two fixtures before opening a PR, and say in
  the PR what the output looked like before and after.

### Add framework guidance

Edits to `skills/impact-map/references/framework-detection.md`. Useful additions
name the places a framework hides its coupling — convention-based binding,
implicit registration, generated code, config-driven wiring — not just its
directory layout.

Include: manifest signals, where each layer lives, and at least one relationship
that produces **no textual reference** in the code.

### Add hidden-coupling patterns

Edits to `skills/impact-map/references/hidden-coupling.md`. The best
contributions come from real incidents: something that broke in production
because nothing referenced it symbolically. Include the mechanism, how to search
for it, and why it survives a type checker.

### Add a failure scenario

Edits to `skills/production-guard/references/failure-analysis.md`, or to a
change-type list in `change-type-checklists.md`. The best ones come from
postmortems. A good contribution states:

- **The mechanism** — what actually goes wrong, in one sentence
- **How to detect it statically** — what an agent reading the code would look for
- **Why it survives a green test suite** — if the existing tests would have caught
  it, it does not need to be in the skill
- **The severity it deserves**, and why it is not one level higher

Example shape: *"A worker dies after the external side effect but before marking
the job complete. Detect: an external call followed by a status write, with no
idempotency guard. Survives testing because tests never kill the worker mid-run.
BLOCKER on money paths, HIGH elsewhere."*

Resist the urge to add scenarios that cannot be checked. A scenario an agent
cannot detect from the repository produces an `UNVERIFIED` line in every report,
which is noise, not rigor.

### Add examples

New files under `skills/<skill>/examples/`.

An Impact Map example shows request, change statement, classified findings with
evidence and confidence, dependency paths, layer impact, risk with reasoning,
implementation order, and open questions.

A Production Guard example shows change summary, risk classification, baseline,
per-category counts, blockers in full, warnings, executed checks, unverified
items, recommended actions, and a verdict that follows mechanically from the
findings. Not every example should end in DO NOT SHIP — a gate that never passes
anything teaches the reader to ignore it.

Examples must be realistic and generic. No employer's code, no internal service
names, no proprietary domain models. Invent a plausible domain instead.

### Add or improve fixtures

New directories under `tests/fixtures/`, plus expected findings in
`tests/README.md`. Keep fixtures **small** — a fixture exists to trigger a
specific reasoning behavior, not to be a realistic application. A dozen short
files is plenty.

Every fixture needs documented expected findings in `tests/README.md`.

- **Impact Map fixtures** need at least one piece of coupling that shares no
  symbol with the change target — something a naive import-graph search misses.
- **Production Guard fixtures** need at least one genuine blocker. A fixture
  where everything passes tests nothing. Seed real bugs: a missing per-item
  authorization check, an external call inside a transaction, a non-nullable
  column with no default.

Do not explain the seeded problem inside the fixture — that hands the agent the
answer.

## Testing against fixtures

There is no assertion runner, because the output is prose and reasonable reports
vary in wording. Test by running the skill and comparing relationships found
against `tests/README.md`.

```bash
# 1. Install or point your agent at skills/<skill>
# 2. Open a fixture directory as the working repository
cd tests/fixtures/impact-map/mixed-architecture

# 3. Give the agent the request from tests/README.md, e.g.
#    "Rename the COMPLETED status to APPROVED. Deep analysis."
# 4. Compare the report against the expected findings
```

Judge on relationships, not wording:

- Were the expected findings found — especially the indirect ones?
- Did anything get classified above its evidence?
- Were any findings invented?
- Did the agent modify a source file? (Both skills are non-modifying during
  analysis.)
- For Production Guard: does the verdict follow mechanically from the findings,
  and did it correctly label everything as analyzed rather than executed? The
  fixtures are not runnable, so a claim that the suite ran is a failure.

Record misses in the PR. A contribution that fixes a documented miss is the most
valuable kind.

## Where things go

| Content | Location |
| --- | --- |
| Workflow phases, classification, behavioral rules | `skills/<skill>/SKILL.md` |
| Detailed per-topic guidance the agent consults on demand | `skills/<skill>/references/` |
| Worked reports | `skills/<skill>/examples/` |
| Fake repositories that exercise reasoning | `tests/fixtures/<skill>/` |
| Expected findings per fixture | `tests/README.md` |
| Usage, installation, limitations | `skills/<skill>/README.md` |
| Repository pitch and catalog page | top-level `README.md` |

Reference files are loaded on demand, so detail is cheap there and expensive in
`SKILL.md`. When in doubt, write it in a reference and link it.

## Validation

```bash
./scripts/validate.sh
```

Discovers every skill under `skills/` automatically and checks required files,
frontmatter validity, name/directory agreement, description presence, references
and examples, orphan references, internal links, secret patterns, hardcoded
paths, and invented quality scores. It runs `skills-ref` when that validator is
available and falls back to its own checks when it is not. CI runs the same
script.

Adding a new skill requires no change to the validator.

## Pull requests

- One concern per PR.
- Describe the behavior change, not just the text change: *what will the agent
  do differently?*
- Note which fixtures you ran it against and what you observed.
- Update `CHANGELOG.md` under `[Unreleased]`.
- Keep the public repository free of company-specific information; team
  conventions belong in a local `references/company-architecture.md` or
  `references/team-standards.md`, neither of which is committed here.

## Code of conduct

Be straightforward and civil. Review contributions on evidence, the same way the
skill reviews code.
