# Contributing

Impact Map is a skill, not a program. Its quality is the quality of its
reasoning instructions, so contributions are judged on whether they make the
agent's analysis **more accurate and better evidenced** — not on whether they
make it produce more output.

## The one hard rule

**Do not make the skill more speculative.**

A finding without evidence costs the reader more time than no finding at all,
and it teaches them to distrust the whole report. A single confident-sounding
guess does more damage than ten missed files, because a missed file gets caught
in review while a wrong claim gets acted on.

So: never add instructions that encourage the agent to list files "that might be
related", to guess at external consumers, to estimate counts, or to promote a
plausible hunch to MUST CHANGE. If a relationship cannot be evidenced, its home
is NEEDS VERIFICATION or OPEN QUESTIONS.

## Ways to contribute

### Improve the analysis methodology

Edits to `skills/impact-map/SKILL.md`. Highest-value and highest-risk, so:

- Keep it **concise**. SKILL.md holds the workflow and the behavioral rules;
  everything deeper belongs in `references/`. Length is a cost — a bloated skill
  file gets skimmed, and the rules that matter get diluted.
- Prefer sharpening an existing rule over adding a new one.
- Every rule should change what the agent *does*. Advice with no observable
  effect on the output is decoration.
- Test the change against at least two fixtures before opening a PR, and say in
  the PR what the output looked like before and after.

### Add framework guidance

Edits to `references/framework-detection.md`. Useful additions name the places a
framework hides its coupling — convention-based binding, implicit registration,
generated code, config-driven wiring — not just its directory layout.

Include: manifest signals, where each layer lives, and at least one relationship
that produces **no textual reference** in the code.

### Add hidden-coupling patterns

Edits to `references/hidden-coupling.md`. The best contributions come from real
incidents: something that broke in production because nothing referenced it
symbolically. Include the mechanism, how to search for it, and why it survives
a type checker.

### Add examples

New files under `skills/impact-map/examples/`. An example must show request,
change statement, classified findings with evidence and confidence, dependency
paths, layer impact, risk with reasoning, implementation order, and open
questions.

Examples must be realistic and generic. No employer's code, no internal service
names, no proprietary domain models. Invent a plausible domain instead.

### Add or improve fixtures

New directories under `tests/fixtures/`, plus expected findings in
`tests/README.md`. Keep fixtures **small** — a fixture exists to trigger a
specific reasoning behavior, not to be a realistic application. A dozen short
files is plenty.

Every fixture needs documented expected findings, including at least one piece
of hidden coupling that a naive import-graph search would miss.

## Testing against fixtures

There is no assertion runner, because the output is prose and reasonable reports
vary in wording. Test by running the skill and comparing relationships found
against `tests/README.md`.

```bash
# 1. Install or point your agent at skills/impact-map
# 2. Open a fixture directory as the working repository
cd tests/fixtures/mixed-architecture

# 3. Give the agent the request from tests/README.md, e.g.
#    "Rename the COMPLETED status to APPROVED. Deep analysis."
# 4. Compare the report against the expected findings
```

Judge on relationships, not wording:

- Were the expected MUST CHANGE locations found?
- Was every documented hidden coupling found?
- Did anything get classified above its evidence?
- Were any findings invented?
- Did the agent modify a file? (That is a bug — the skill is read-only.)

Record misses in the PR. A contribution that fixes a documented miss is the most
valuable kind.

## Where things go

| Content | Location |
| --- | --- |
| Workflow phases, classification, behavioral rules | `SKILL.md` |
| Detailed per-topic guidance the agent consults on demand | `references/` |
| Worked reports | `examples/` |
| Fake repositories that exercise reasoning | `tests/fixtures/` |
| Expected findings per fixture | `tests/README.md` |
| Usage, installation, limitations | `skills/impact-map/README.md` |
| Repository pitch and catalog page | top-level `README.md` |

Reference files are loaded on demand, so detail is cheap there and expensive in
`SKILL.md`. When in doubt, write it in a reference and link it.

## Validation

```bash
./scripts/validate.sh
```

Checks required files, frontmatter validity, the skill name, description
presence, references and examples, internal links, and obvious secret patterns.
It runs `skills-ref` when that validator is available and falls back to its own
checks when it is not. CI runs the same script.

## Pull requests

- One concern per PR.
- Describe the behavior change, not just the text change: *what will the agent
  do differently?*
- Note which fixtures you ran it against and what you observed.
- Update `CHANGELOG.md` under `[Unreleased]`.
- Keep the public repository free of company-specific information; team
  conventions belong in a local `references/company-architecture.md`, which is
  deliberately not committed here.

## Code of conduct

Be straightforward and civil. Review contributions on evidence, the same way the
skill reviews code.
