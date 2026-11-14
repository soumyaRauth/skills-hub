# Editorial standards

How to evaluate and edit non-fiction writing for its readers, and how to
write new material, without imposing a style or losing the author.

## Contents

- What to evaluate
- Clarity and precision
- Readability without condescension
- Structure: sentences, paragraphs, flow
- Terminology and consistency
- Tone
- Editing someone else's work
- Writing new material
- Proofreading
- Edit notation

## What to evaluate

Clarity · precision · readability · natural language · tone consistency ·
sentence structure · paragraph structure · logical flow · terminology
consistency · depth of explanation · repetition · unnecessary jargon ·
ambiguity · unnecessary complexity.

The test for every one of them is the reader's experience, not a style
manual: does this make it easier or harder for *this* reader to understand
and use what is being said?

## Clarity and precision

- **One idea per sentence** where the idea is new or hard. Long sentences are
  fine for familiar material and for connecting ideas.
- **Concrete over abstract:** "the request fails with a 422 error" over "an
  issue may arise".
- **Precise verbs and subjects:** who does what. Watch for hidden actors ("it
  is configured" — by whom, where?) where the reader needs to act.
- **Ambiguity:** pronouns with unclear referents ("it", "this", "that"
  starting a sentence), "should" meaning either "must" or "probably will",
  "simple" meaning either "easy" or "basic".
- **Hedging:** enough to be honest, not so much that the reader cannot tell
  what the author believes.

## Readability without condescension

Respect the reader's intelligence without assuming their knowledge.

- **Oversimplification** removes what makes the idea true: analogies that
  break at the first real use, rules stated without the exceptions the reader
  will meet next week.
- **Overcomplication** makes a plain idea hard: nominalizations ("perform the
  configuration of"), stacked qualifiers, passive chains, jargon where a
  plain word exists.
- **Condescension:** "simply", "just", "obviously", "of course", "it is easy
  to see"; explaining what the reader clearly knows; cute tone around
  difficult material.
- Readability formulas measure sentence and word length, not understanding.
  Use them, if at all, as a prompt to look, never as a verdict.

## Structure: sentences, paragraphs, flow

- **Paragraphs** have one job. The first sentence tells the reader what it is.
- **Order inside a section:** why → what → how → example → caveats is a good
  default for teaching; reference material may lead with the answer.
- **Transitions** say why the next thing follows: "That works for one user.
  With two, the counter breaks, because…".
- **Lists and tables** for parallel items and comparisons; prose for
  reasoning and causation. A bulleted list of reasoning steps loses the
  "because".
- **Headings** say what the reader will find or do ("Handle a missing
  file"), not a topic label ("Errors").

## Terminology and consistency

- Build a **terminology list** while reading: each term, its first use, its
  definition (if any), and its variants. Variants for one concept ("endpoint",
  "route", "path operation", "handler" used interchangeably) are a finding:
  readers assume different words mean different things.
- **Jargon** is fine when it is the reader's real vocabulary or is taught.
  It is a finding when it is undefined for this reader or replaceable by a
  plain word with no loss.
- Keep **names, capitalization, code formatting and spelling** consistent
  across chapters (product names, `inline code`, British or American
  spelling as the book chooses).

## Tone

- Consistent across the book unless the change is deliberate.
- Warm without being sentimental; confident without being dismissive;
  honest about difficulty.
- Matched to the moment: patient around hard ideas, brisk around easy ones,
  serious around safety, data loss, money and security.
- Inclusive: examples and names from more than one culture; no assumptions
  about gender, age, ability or background that the content does not need.

## Editing someone else's work

1. **Understand it first.** Read the whole scope before changing a word.
   Identify the author's voice, intended meaning, and recurring choices.
2. **Preserve meaning, honesty and accuracy.** Never change a factual or
   technical claim without verifying the new one. When the original is wrong,
   say so in a note; do not quietly fix and move on.
3. **Change for the reader, not for taste.** Every significant change must
   make the text clearer, more accurate, better ordered, or more welcoming
   for the reader. "I would have written it differently" is not a reason.
4. **Keep the author's voice.** Match their sentence rhythm, their humour,
   their level of formality. An edit that sounds like a different person is
   a defect even if each sentence improved.
5. **Prefer the smallest effective change.** Fix the sentence before
   rewriting the paragraph; fix the paragraph before restructuring the
   section.
6. **Explain significant changes** in a sentence each: what changed, why it
   helps the reader.
7. **Use reviewable edits** when the work belongs to someone else and the
   medium supports it: suggestion mode, tracked changes, a diff, a pull
   request. The author decides.

## Writing new material

- Start from the reader, the outcome and the place in the book
  (`book-creation.md`).
- Prioritize usefulness, clarity, depth and comprehension over word count.
  Long is not thorough; short is not clear.
- Write the example first, then the explanation around it, for technical
  material.
- Match the surrounding book: voice, terminology, heading depth, callout
  conventions, code style.
- Every factual and technical claim is checked or marked for checking.
  Never invent a citation, a quotation, a statistic or a study.
- Write in the language and register of the book. When the book is in a
  language other than English, the same standards apply to that language's
  conventions; do not import English punctuation, idiom or register.

## Proofreading

Last, after structure and substance:

- Spelling, grammar, punctuation, typos in code and commands (a typo in a
  command is a technical defect, not a proofreading one).
- Consistency of terms, capitalization, numbers, units, cross-references,
  figure and table numbering.
- Broken references ("see section 4.3" where 4.3 moved).

In an evaluation, summarize proofreading as patterns with a few examples
unless a full pass was requested. Never let a proofreading list stand in for
an editorial evaluation.

## Edit notation

When presenting proposed edits outside a tool with suggestion mode:

```
LOCATION   Chapter 3, §3.2, paragraph 2
CURRENT    Simply decorate the function and FastAPI does the rest.
PROPOSED   Put @app.get("/") on the line above the function. This line is a
           decorator: it tells FastAPI to call the function whenever a browser
           asks for "/". Section 3.1 showed what decorators are.
WHY        "Simply" signals ease where readers reported confusion; the
           sentence used a term (decorate) the book had not introduced.
TYPE       Pedagogical · tone
```
