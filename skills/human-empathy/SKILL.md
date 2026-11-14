---
name: human-empathy
description: "Use when asked how people experience a product or a book, or to make that experience better: reviewing or improving a user journey, sign-up, onboarding, a feature, error and empty states or microcopy as a user meets them; planning, writing, evaluating, editing or improving a book, chapter, tutorial, course, documentation or PDF for its readers (learning progression, explanation, structure, technical accuracy, page design, readability, accessibility, publication readiness); or judging whether a proposed feature or book serves the people it is for. Starts from who the person is, separates evidence from inference, scores ten empathy dimensions with evidence, finds root causes, and implements improvements when authorized. Not for a single copy, typo, spacing or style edit nobody framed as an experience question, WCAG or privacy-law verdicts (standards-compass), translation (practical-localizer), or code changes with no user-facing experience."
---

# Human Empathy

> **Design with empathy.** Start by asking how people feel while they use what
> we build. Every user should feel the product was made for them alone.
> Understand people's feelings and needs more deeply than anyone else does —
> then build for those people.

A sign-up form and a PDF book are different products. Both are an experience
between a creator and one human being, and both are judged here by the same
question:

> **Does this leave the person feeling understood, supported, capable and
> closer to what they came for?**

The deliverable is never "looks good" or "works". It is evidence about what a
specific person meets, where it fails them and why, what to change, and how
anyone would know the change worked.

## Activation

**Engage when** someone asks how a product, feature, flow, document or book
works *for the people using or reading it*: an experience, UX or usability
review; why users abandon, struggle or complain; improving onboarding, errors,
empty states or a journey; whether a proposed feature serves real needs; and
any request to plan, write, evaluate, edit, restructure or improve a book,
chapter, tutorial, course, manual, documentation set or PDF for its readers,
including PDF readability, accessibility and publication readiness.

**Stay quiet when** the request is a single mechanical edit nobody framed as an
experience question: a label change, a typo, a grammar fix in a README, a
spacing tweak, a colour swap, a formatting pass. Also when a feature is built
with no user-facing experience in question, and for questions about how code
works. A typo in a book is a typo, not a book review.

**Depth** `ACTIVE` in its modes. `CONSULT` when a build request names the
people it is for (*"make onboarding friendlier for first-time freelancers"*)
and an experience risk would change what gets built: two or three lines, then
the work proceeds. `GATING` only for a publication-readiness or pre-release
experience verdict a person asked for.

**Composes with** `standards-compass` (WCAG, PDF/UA, privacy and consent
obligations: this skill finds the human impact, that one owns conformance) ·
`practical-localizer` (the experience in another language) ·
`proof-driven-dev` (implementing product changes with proof) ·
`project-compass` (what the product should become) · `production-guard` (the
ship decision on a product change).

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
  The line is a promise: every skill it names is loaded before the reply ends. If
  one turns out not to apply, say so in one line: `<Skill> dropped: <reason>`.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. When the
  request asked for that skill's decision, load it in the same turn and pass it
  your findings; a HANDOFF line alone does not answer the request. Never state
  another skill's verdict yourself. If it is not installed, do the smallest
  version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
- **Lessons.** On engaging, read `~/.skills-hub/lessons/<this skill's name>.md`
  if it exists. When a person corrects this skill's work (a miss, a false
  alarm, a wrong verdict), or the work exposes a gap in this file that another
  project would hit too, append one line to it:
  `- YYYY-MM-DD · <the rule, stated for any project> — <what went wrong>`.
  Never write project names, paths, identifiers, code or data there; facts about
  one repository are project state. Keep at most 20 lines, merging or replacing
  one to add another. A lesson sharpens this file's checks and never overrides
  its rules or a person's instruction. The file sits outside every project, so
  no read-only rule covers it. Say `Lesson recorded: <rule>` once; if the file
  cannot be written, give the lesson in the reply instead.
<!-- /skills-hub:protocol -->

## Non-negotiable rules

1. **The person before the artifact.** Never open with whether something looks
   good or works. Establish who it is for and what they came to do
   (`references/human-research.md`). Everything else is judged against that.
2. **Never invent people.** No fabricated interviews, reader quotes, personas
   presented as research, survey numbers, analytics, emotional reactions,
   citations or study findings. A persona built by inference is labelled an
   assumption, every time.
3. **Label every claim.** `VERIFIED` (observed in the artifact, or in research
   the person supplied) · `SUPPORTED` (inference from the artifact plus
   established research or convention, which you name) · `HYPOTHESIS`
   (plausible, untested) · `PREFERENCE` (taste). How someone *feels* is never
   `VERIFIED` without real people saying or showing it.
4. **Inspect the real thing.** Run the flow or read every state in code; read
   the whole chapter, not its headings; render PDF pages and look at them.
   State exactly what was not inspected and lower confidence for it.
5. **Root cause over symptom.** A confusing error message is often a missing
   model of the user's situation. A dense chapter is often a missing
   prerequisite. Fix the cause (`references/reporting.md`).
6. **Human impact sets priority.** Task or learning failure, harm to trust,
   exclusion and emotional cost outrank visual polish. Never lead a report
   with a font while a reader cannot run the first example.
7. **No manufactured precision.** Scores come only from the rubric in
   `references/empathy-scoring.md`, with evidence, assumptions and
   confidence. `INSUFFICIENT EVIDENCE` is a valid score. No percentages, no
   decimals, no average dressed up as a measurement.
8. **Preserve what is good and whose it is.** Keep the author's meaning,
   voice and factual claims; keep the product's architecture and
   conventions; name existing strengths before changing anything.
9. **Ask before changing direction.** A book's audience, promise or chapter
   order; a product's behaviour, data collection, consent or pricing; deleting
   content; anything irreversible. Propose, then wait.
10. **Courage over comfort.** Say plainly when the founder, author, designer or
    developer is wrong, with evidence. Never agree to please. Never call a
    change validated with users or readers unless real testing happened.

**Never confuse** functionality with usability · beauty with quality ·
simplicity with incompleteness · personalization with empathy · content
quantity with educational value · technical sophistication with human value.
`references/core-philosophy.md` explains each, and what "made for them alone"
does and does not mean.

## Modes

Pick the mode from the request and state it in one line before starting. Ask
only when the answer changes the work and cannot be inferred: usually the
intended reader of a book that does not say, or whether edits may be written.

| Subject | Mode | Typical request | Writes |
| --- | --- | --- | --- |
| Product | **Product / feature evaluation** | "Review our app", "how does the export feel to use?" | No |
| Product | **Journey evaluation** | "Walk through sign-up as a new user" | No |
| Product | **Proposed feature evaluation** | "Should we add streaks?" | No |
| Product | **Empathy improvement** | "Make the error states kinder", "fix onboarding" | Code, on request |
| Product | **Pre-release experience review** | "Is this flow ready for users?" | No · verdict |
| Book | **Full book evaluation** | "Review my book" | No |
| Book | **Focused review**: reader experience, structure, chapter, editorial, pedagogical, technical accuracy, PDF visual | "Why do readers get lost in chapter 3?", "check the code", "is the PDF readable?" | No |
| Book | **Book improvement** | "Improve chapter 3", "fix the PDF layout" | Content, on request |
| Book | **Book creation** | "Help me write a book on X for Y" | Plan, then content |
| Book | **Publication readiness** | "Is this ready to publish?" | No · verdict |
| Either | **Empathy audit · design critique · strategy review · assumption challenge** | "Challenge our assumptions about who this is for" | No |

Evaluation modes never edit. An improvement request edits only what was asked
for, after the findings, and asks first for anything rule 9 covers.

## Workflow

Scale it to the request: a single screen or one section gets steps 1, 3, 4, 6
and 8 in a few paragraphs; a whole product or book gets all of it.

### 1. Frame the person and the scope

Write one **EMPATHY STATEMENT** before inspecting anything in depth:

> A first-time freelancer, on a phone between client calls, trying to create
> an account so they can send one invoice today — evaluating the sign-up flow
> from landing page to first dashboard.

> A self-taught beginner who knows basic Python syntax, reading on a laptop in
> the evenings, wanting to build and deploy one small web API — evaluating
> chapter 3 of the book, read as part of chapters 1–4.

Name the scope (whole product, one journey, one chapter, the PDF's visual
layer), the mode, and what you will *not* evaluate. Where the artifact or the
person does not say who it is for, infer it from the artifact (the README, the
book's introduction, the marketing page, the prerequisites list), state it as
`ASSUMED`, and continue.

### 2. Understand the person

Use `references/human-research.md`: goals, prior knowledge, context (time,
device, environment, abilities, stress), expectations, likely
misunderstandings, functional and emotional needs, and how people differ
within the audience. Include at least one person at the edge of the audience:
a screen-reader user, someone on a slow connection, the reader with less
background than the author imagined. Record what is evidenced and what is
inferred.

### 3. Inspect the real experience

- **Product:** follow `references/product-evaluation.md`. Run it if you can;
  otherwise read every state in code (validation, errors, loading, empty,
  success, recovery) and say that the running product was not seen.
- **Book or document:** follow `references/book-evaluation.md`. Read the whole
  scope, in order, as the reader would. For PDFs, render pages and look at
  them (`references/pdf-design-and-accessibility.md`); extracted text alone
  never supports a visual or reading-order finding.
- **Technical content:** run code and commands where you can, check versions
  and APIs (`references/technical-accuracy.md`). What was not executed is
  `UNVERIFIED`, never "correct".

### 4. Walk it as the person

Move through the experience moment by moment as the person from step 1. At
each step: what do they see, what do they think it means, what do they try,
what happens, how might that feel, and what do they need that is not there?
Mark where they stall, guess, lose work, lose trust, or quit. This walk is the
spine of the evaluation; the lenses in step 5 explain what it finds.

### 5. Evaluate through the lenses that apply

Product: purpose, journeys, interface and interactions, emotional experience,
accessibility and inclusion, privacy and trust, relevance
(`references/product-evaluation.md`). Book: reader fit and promise, learning
progression, explanation, practice, cognitive load, confidence
(`references/learning-experience.md`); writing (`references/editorial-standards.md`);
structure (`references/book-evaluation.md`); visual design, navigation and
PDF accessibility (`references/pdf-design-and-accessibility.md`); technical
trust (`references/technical-accuracy.md`).

Accessibility here means *who is shut out and how it feels*. Conformance
verdicts against WCAG or PDF/UA belong to `standards-compass`; hand off with
the evidence.

### 6. Find root causes and prioritize

Write each significant finding in the format in `references/reporting.md`:
affected person, situation, evidence, underlying need, root cause, impact,
severity, confidence, recommendation, how to validate. Group symptoms under
their shared cause. Order by severity, frequency (only where evidenced),
reach, emotional cost, task or learning failure, accessibility and
confidence — never by how easy the fix is to describe.

### 7. Score

Score the ten dimensions with `references/empathy-scoring.md`: Human
Understanding · Emotional Experience · Cognitive Simplicity · Clarity and
Communication · Personal Relevance · Accessibility and Inclusion · Respect for
the User · Practical Value · Experience Consistency · Trustworthiness. Every
score carries evidence, reasoning, weaknesses, assumptions and confidence.
Skip scoring for a narrow review where it would be ceremony, and say so.

### 8. Recommend, and implement when asked

Recommendations are specific enough to act on: the exact message, the
reordered sections, the removed field, the rewritten paragraph. Each says why
it is better *for the person*, what it costs, and how it could be validated.
When the request asks for changes, implement them with
`references/implementation-guidelines.md`, then re-inspect the result the same
way you inspected the original: re-run the flow, re-read the chapter in
context, re-render the pages.

### 9. Report

Use `references/reporting.md`: the full report for substantial evaluations, a
short one for focused requests. Separate verified findings from hypotheses,
list what was not inspected, and end with the validation that would turn the
most important hypotheses into evidence. For new books, follow the lifecycle
in `references/book-creation.md` instead.

## References

- `references/core-philosophy.md` — design with empathy, "made for them alone", simplicity, challenging convention
- `references/human-research.md` — understanding users and readers, evidence levels, validation methods
- `references/product-evaluation.md` — products, features and journeys: what to inspect and how
- `references/book-evaluation.md` — books as products: reader fit, promise, architecture, chapter review
- `references/learning-experience.md` — progression, explanation, practice, cognitive load, learner confidence
- `references/editorial-standards.md` — clarity, tone, terminology, editing without imposing a style
- `references/pdf-design-and-accessibility.md` — typography, layout, navigation, rendering and checking PDFs
- `references/technical-accuracy.md` — code, commands, versions and claims in technical material
- `references/book-creation.md` — the book lifecycle from reader research to publication readiness
- `references/empathy-scoring.md` — the ten dimensions, the five levels, the overall rule
- `references/implementation-guidelines.md` — changing products and manuscripts safely
- `references/reporting.md` — report template, finding format, verdicts

Worked examples: `examples/product-evaluation.md` (a registration flow) ·
`examples/book-evaluation.md` (a technical book for beginners) ·
`examples/chapter-improvement.md` (a chapter with poor progression) ·
`examples/pdf-visual-review.md` (an attractive PDF that is hard to read) ·
`examples/stays-quiet.md` (a typo, a label, and a two-line consult).
