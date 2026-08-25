# Contributing

These are skills, not programs. Their quality is the quality of their reasoning
instructions, so contributions are judged on whether they make the agent's
analysis **more accurate and better evidenced** — not on whether they make it
produce more output.

## The three hard rules

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

### 3. No unsupported linguistic claims

This one governs `practical-localizer`. Language is not a place for confident
generalization, and a skill that generalizes teaches the agent to do the same.

Never add:

- **Native-authority claims.** "Native speakers say X." Write "X is the more
  common convention in modern software for this locale", and name what that
  rests on.
- **Blanket language rules.** "Language X always prefers …", "Speakers of Y never
  …". Usage varies by region, age, profession, audience, product and register.
  Those are factors to weigh, never rules to encode.
- **Blanket strategy rules.** "Keep all technical terms in English", "always
  transliterate", "always translate". The right answer differs per language, per
  term, per product — which is the whole point of the skill.
- **Machine translation pasted without review**, in examples, references or
  fixtures. If you cannot say why a target string is the right choice, it does
  not belong in the documentation.
- **Hardcoded locale assumptions.** Plural categories, digit shapes, date order,
  formality defaults and currency placement belong in a locale profile the user
  can override, not baked into the workflow.

Contributions that add or correct target-language material should say what the
choice rests on — project evidence, platform convention, or your own experience
as a speaker, stated as such. Marking a judgement MEDIUM confidence is always
acceptable; presenting it as fact is not.

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

### Add a proof strategy or failure classification

Edits to `skills/proof-driven-dev/references/proof-strategies.md`,
`failure-analysis.md`, or `risk-model.md`.

A proof strategy earns its place by being *cheaper than the obvious one* or by
catching something the obvious one cannot. State:

- **The requirement shape** it applies to — what kind of claim it establishes
- **The mechanism**, concretely: the command, and what its output demonstrates
- **What it does not prove** — the boundary is the useful part
- **Why it beats a test**, if it does: a database constraint that makes a
  requirement unfalsifiable is better evidence than a test asserting the same
  thing, because it cannot rot

The rule that governs this whole skill: a strategy must produce evidence
somebody could re-run. "Inspect the code and confirm" is not a proof strategy,
and adding one that reads like one weakens every status the skill reports.

### Add a language example or localization reference

New files under `skills/practical-localizer/examples/`, or edits to
`skills/practical-localizer/references/`.

A good language example is not a word list. It shows *decisions*: a term where
the obvious dictionary answer is wrong for a UI and why, a string whose meaning
only the call site resolves, a technical defect (placeholder or plural) that no
amount of language knowledge would catch, and at least one item the method
correctly refuses to decide without a human.

Requirements:

- Distinguish **example convention** from **universal rule**, explicitly. Every
  language example in this repository ends with a section stating what it does
  not claim; keep that.
- Prefer evidence a reader can check — how the surrounding catalog already words
  things, what the platform's own UI does — over assertion.
- Cover something the existing examples do not. A sixth language that
  demonstrates the same three phenomena adds length, not value. Genuinely new
  ground: languages with case systems that break interpolated fragments, tonal
  or logographic input concerns, locales with contested script or digit
  conventions, languages where the software ecosystem is young.

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
- **Proof-Driven Development fixtures** must actually **run** — zero
  dependencies, `node --test`, and a suite that is **green** before the agent
  starts. The skill is being tested on whether it defines an outcome and proves
  it; a red suite hands it the answer. Seed the gap somewhere the existing tests
  do not look: an off-by-one that only appears at a non-multiple count, a shared
  helper with two callers, an authorization hole no positive case can reach.
- **Practical Localizer fixtures** need at least one defect that only the *call
  site* reveals — a key whose correct translation depends on the handler around
  it — plus one purely technical defect: a lost placeholder, a corrupted
  interpolation syntax, or a plural structure flattened into a single form. Seed
  the target strings deliberately, and document in `tests/README.md` why each
  one is wrong.

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
- Did the agent write outside its remit? Impact Map and Production Guard modify
  nothing; Practical Localizer writes only in LOCALIZE mode, and only to
  localization resources; Proof-Driven Development implements, so judge it on
  whether the diff stays inside the contract it wrote.
- For Proof-Driven Development: did a contract exist before the code, does every
  `PASS` name a command that really ran, and did an unverifiable requirement
  stay unverified?
- For Practical Localizer: were the placeholder and plural defects caught, was
  the established project terminology preferred over a new synonym, and did the
  report avoid claiming native authority?
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
| Worked reports and language examples | `skills/<skill>/examples/` |
| Copy-into-your-project starting points | `skills/<skill>/templates/` |
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

It also runs the fixtures that are *meant* to be executed — currently
`tests/fixtures/proof-driven-dev/` — and fails if any of them is red, since a
rotted fixture hands the agent under test the answer. That check skips cleanly
when Node is unavailable. If you add runnable fixtures for another skill, add
their directory to `RUNNABLE_ROOTS` in the script; do not widen it to every
`package.json` under `tests/fixtures/`, because the illustrative fixtures declare
test scripts they were never meant to satisfy.

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
