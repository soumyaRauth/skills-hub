# Learning experience and pedagogy

How to judge whether material actually helps a person learn: progression,
explanation, practice, cognitive load and the reader's confidence. Grounded
in established instructional research, applied with judgement rather than as
a checklist.

## Contents

- The research worth knowing, briefly
- Learning progression
- Explanation quality
- Practical learning
- Cognitive load
- Learning confidence
- Adults, beginners and experts
- Diagnosing "readers get lost here"
- Fixing progression problems

## The research worth knowing, briefly

Use these as reasons, named in a few words when they support a finding. Do
not decorate reports with them.

| Idea | What it says | Typical finding it supports |
| --- | --- | --- |
| Cognitive load theory (Sweller) | Working memory is small. Intrinsic load comes from the material; extraneous load from how it is presented; only the first is necessary | Five new concepts in one code example; explanations split across pages |
| Worked-example effect | Novices learn more from studying worked solutions than from solving unaided | A beginner chapter that jumps to exercises with no worked example |
| Expertise reversal | Support that helps novices can slow experts | A book for experienced developers that over-explains basics |
| Mayer's multimedia principles | Coherence (cut the extraneous), signalling (highlight structure), spatial contiguity (words near the picture), segmenting (learner-paced chunks), pre-training (names and characteristics of key concepts first) | Decorative images; a diagram on a different page from its explanation |
| Merrill's first principles | Learning is promoted when it is problem-centred and moves through activation of prior knowledge, demonstration, application and integration | A chapter that demonstrates but never lets the reader apply |
| Retrieval and spaced practice | Recalling something strengthens it more than re-reading; spacing beats cramming | No questions or exercises; nothing revisited later |
| Prior knowledge and misconceptions | New knowledge is built on old; a wrong existing belief must be addressed, not ignored | "A variable is a box" never corrected when references matter |
| Curse of knowledge | Experts find it hard to imagine not knowing what they know | Skipped steps, undefined terms, "simply" |
| Revised Bloom's taxonomy | Remember, understand, apply, analyse, evaluate, create | Outcomes stated as "understand X" with exercises that only test recall |

## Learning progression

- **Starting level:** does the first chapter start where the stated reader
  actually is? Are prerequisites stated, and checkable by the reader?
- **Sequence:** is each concept introduced after what it depends on? Draw the
  dependency graph of the concepts in scope if it is not obvious; a
  forward reference (a concept used before it is taught) is a defect unless
  it is announced and harmless ("we will explain `async` in chapter 6; for
  now, type it as shown").
- **Building:** does each chapter use and extend the previous one, ideally
  through a running project or recurring example?
- **Prerequisites:** explained, or pointed to, at the moment they are needed.
- **Decomposition:** difficult ideas broken into steps that can each be
  understood and checked.
- **Transitions:** each section answers "why are we doing this now?"
- **Pace:** no cliffs (sudden jumps) and no plateaus (pages that add nothing
  new).

## Explanation quality

For each significant concept, look for:

1. **Why it matters,** in the reader's terms, before the details. A reader
   who does not know what problem a thing solves cannot organize what they
   learn about it.
2. **What it is,** in plain words, with technical terms introduced
   deliberately: the term, a plain definition, then consistent use.
3. **A concrete example** before or right after the abstraction. Abstract
   definitions alone rarely land for newcomers.
4. **The boundaries:** when not to use it, common mistakes, what it looks like
   when it goes wrong (error messages the reader will actually see).
5. **Anticipated confusion:** the question the reader is about to ask,
   answered at the moment they would ask it.

Completeness without complication: an explanation is complete when the reader
can use the concept correctly at the level the book promises, not when every
edge case has been covered.

## Practical learning

- **Examples** are realistic for the reader's world and work as printed.
- **Code examples** are complete enough to run (or clearly marked as
  fragments), use the versions the book states, and produce the output the
  book shows (`technical-accuracy.md`).
- **Instructions** are actionable: one action per step, the expected result
  stated, what to do if the result differs.
- **Exercises** practise the chapter's outcome, rise in difficulty, and come
  with a way to check (answers, tests, expected output, hints).
- **Application:** the reader ends able to do something they could not do
  before, ideally something they care about.

## Cognitive load

Signs of overload:

- Many new concepts in one section, or in one code example. List them; if a
  newcomer must hold several unfamiliar things at once to follow a single
  step, it is overloaded.
- Long paragraphs that mix the explanation of several ideas.
- Explanations split from what they explain (a figure three pages away, code
  explained only after a long listing).
- The reader asked to remember disconnected details for later use.
- Detours and asides in the middle of a difficult explanation.

Remedies, in order of preference: reorder so prerequisites come first;
split one section into several, each with its own example; move side
information to a later section, a callout or an appendix; add a worked
example; add a short recap at the point of highest load; replace a dense
paragraph with a numbered sequence or a small table.

Never reduce load by removing what the reader needs. That moves the
difficulty to later, usually to a worse moment.

## Learning confidence

- Does the reader feel able to continue? Look for early wins, visible
  progress, and difficulty introduced with support.
- Are difficult concepts handled with patience: acknowledged as difficult,
  approached from more than one angle?
- Does the material encourage curiosity (why, what if) rather than only
  compliance (type this)?
- Does anything make the reader feel inadequate? "Simply", "just",
  "obviously", "as everyone knows", "this is trivial", jokes at beginners'
  expense, and error messages presented as the reader's fault all do. So does
  a sudden jump in difficulty with no acknowledgement.
- Are errors normalized? Showing the error a reader will hit, and how to read
  it, is one of the most confidence-building things a technical book can do.

## Adults, beginners and experts

Adult learners usually want to know why something matters before investing,
bring experience that can help or interfere, and are oriented toward
problems they have now. Respect their time and their existing knowledge.

- **Beginners** need foundations before abstractions, worked examples,
  explicit steps, reassurance that confusion is normal, and fewer choices.
- **Intermediate readers** need the mental model behind what they already do,
  trade-offs, and realistic problems.
- **Experts** need density, precision, references and no hand-holding; the
  same scaffolding that rescues a beginner wastes their time.

A book for mixed audiences should say how each can use it (which chapters to
skip, which callouts are optional), not compromise every page.

## Diagnosing "readers get lost here"

When readers report confusion at a point:

1. **Read what precedes the point,** not just the point. The cause is often
   earlier: a missing prerequisite, a term never defined, a mental model
   never built.
2. **List the concepts in play** at the point and where each was introduced.
3. **Check the example:** does it work as printed? A broken or unexplained
   example produces exactly the "I got lost" report.
4. **Check the load:** how many new things arrive at once?
5. **Check the transition:** does the reader know why this section exists?
6. **Compare with the evidence:** do the readers' own words match the cause
   you found? If two notes say "I didn't understand what `@app.get` does",
   decorators were never taught; that is a stronger finding than "too
   dense".

## Fixing progression problems

- **Missing prerequisite:** add a short section or sidebar at the point of
  need, or move the chapter that teaches it earlier. Moving chapters is a
  direction change; propose it.
- **Overloaded section:** split it; introduce one concept per step, each with
  its own working example; show the full combination only after the parts.
- **Abstraction before example:** lead with the concrete case, then
  generalize.
- **Forward reference:** teach it now, defer the usage, or announce it
  honestly ("type this for now; chapter 6 explains it").
- **No practice:** add one exercise that uses exactly the chapter's outcome,
  with a way to check.
- **Missing why:** open with the problem the concept solves, in the reader's
  situation.

Re-read the revised section in context afterwards, as the reader, to check
the fix did not move the problem.
