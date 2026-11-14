# Creating and improving books: the lifecycle

When asked to create a book, or to take an existing one through improvement
to publication, follow this lifecycle. Each stage has a deliverable the
author can approve before the next stage spends effort on it.

## Contents

- The twelve stages
- Stage 1: reader research
- Stage 2: positioning and the promise
- Stage 3: content architecture
- Stage 4: chapter planning
- Stage 5: writing
- Stages 6–11: verification and review
- Stage 12: publication readiness
- Improving an existing book
- Working with the author

## The twelve stages

| # | Stage | Deliverable | Approval needed before next stage |
| --- | --- | --- | --- |
| 1 | Reader research | Reader profile, with evidence levels and unknowns | Yes: the reader defines everything else |
| 2 | Positioning and promise | One-sentence promise, title options, who it is not for | Yes |
| 3 | Content architecture | Learning outcomes, concept dependency map, chapter sequence | Yes |
| 4 | Chapter planning | Per-chapter plan: outcome, prerequisites, concepts, example, practice | Yes for the whole plan; small changes later are fine |
| 5 | Writing | Chapters, in order | Per chapter or per batch, as the author prefers |
| 6 | Technical and factual verification | Accuracy report (`technical-accuracy.md`) | Failures fixed |
| 7 | Editorial review | Findings and edits (`editorial-standards.md`) | Author accepts or rejects |
| 8 | Pedagogical review | Progression and load findings (`learning-experience.md`) | Author accepts or rejects |
| 9 | Visual design review | Typography, layout, figures (`pdf-design-and-accessibility.md`) | Design decisions approved |
| 10 | PDF quality assessment | Rendered-page, navigation and accessibility checks | Failures fixed |
| 11 | Final proofreading | Corrections | — |
| 12 | Publication readiness | Verdict with conditions | The author decides to publish |

Scale it: a ten-page tutorial may compress stages 1–4 into one short plan.
Never skip stage 1 entirely; a book without a reader is written for the
author.

## Stage 1: reader research

Use `human-research.md`. Ask the author what they know about their readers:
who has asked them for this, where readers will come from, what those readers
struggle with. Look for evidence the author can supply: audience questions,
course feedback, forum threads, competitor reviews (what readers of similar
books complain about is strong evidence of unmet needs; quote and cite real
reviews only).

Deliverable:

```
READER (evidence: author's course feedback, 40 forum questions supplied; no interviews)
  Who          Self-taught developers who know basic Python, have never built a web service
  Wants        To build and deploy one small API they can show an employer
  Knows        Variables, functions, loops, pip; not HTTP, not decorators, not async
  Fears        That web development needs a computer science degree
  Context      Evenings, laptop, often Windows
  Not for      Experienced backend developers; people who have never written Python
  Unknown      How many use Windows (affects every setup instruction) — ask or survey
```

## Stage 2: positioning and the promise

- The promise in one sentence: "*After this book, you will be able to …*",
  concrete and checkable.
- Title and subtitle that let the intended reader recognize themselves and
  the level; honest about scope.
- What the book is not, stated in the introduction, so the wrong readers
  self-select out before they waste money.
- How it differs from what already exists, from the reader's point of view
  (not "more comprehensive", but "the only one that assumes no web
  background and deploys on a free tier").

## Stage 3: content architecture

1. **Learning outcomes:** what the reader will be able to do, written with
   action verbs, each checkable by an exercise or project.
2. **Concept inventory:** every concept the outcomes require.
3. **Dependency map:** for each concept, what must be understood first. A
   topological order of this map is the backbone of the chapter sequence.
4. **Through-line:** a running project or recurring example that grows across
   chapters, if the subject allows. It gives every chapter a reason to exist
   and the reader a sense of progress.
5. **Structure choice:** tutorial path, problem-by-problem, reference, or a
   hybrid with parts for different readers. Choose for the reader's use, not
   by convention, and say why.
6. **Cut list:** topics the author wants to include that the outcomes do not
   need. Propose where they go (appendix, a later book, nowhere).

## Stage 4: chapter planning

For each chapter:

```
CHAPTER 3 — Your first endpoint
  Outcome        Write and run an endpoint that returns JSON, and call it from a browser
  Builds on      Ch. 2 (functions, return values, dictionaries)
  New concepts   HTTP request/response · route · decorator (just enough) · JSON
  Not yet        async, dependency injection, Pydantic models (ch. 5, 6)
  Example        The /tasks endpoint of the running to-do API
  Practice       Add a /tasks/{id} endpoint; check with the browser and with curl
  Likely stalls  What a decorator is; why the server must keep running
  Close          Recap; what ch. 4 adds (accepting data)
```

Limit new concepts per chapter to what the reader can absorb with practice;
when the list is long, split the chapter.

## Stage 5: writing

Follow `editorial-standards.md` (writing new material) and
`learning-experience.md`. Chapter template, adapted to the book:

1. Opening: the problem this chapter solves for the reader, and what they
   will be able to do at the end.
2. Prerequisite check, in a sentence or two.
3. Concepts, one at a time: why → what → example → boundaries.
4. Worked example, building the running project.
5. Common mistakes and the errors the reader will see.
6. Practice with a way to check.
7. Summary and bridge to the next chapter.

Write the code first and run it; then write the prose around working code.

## Stages 6–11: verification and review

Run them in the listed order. Technical verification comes before editing,
because fixing code can change the prose. Pedagogical review comes before
visual design, because restructuring changes pages. Proofreading comes last,
because every earlier stage introduces new text.

## Stage 12: publication readiness

Give a verdict, with conditions, never a guarantee:

- **READY TO PUBLISH:** the promise is delivered; the reader journey works
  end to end; technical content verified (or the unverified items are listed
  and accepted by the author); no high-severity editorial, pedagogical,
  visual or accessibility findings open.
- **READY WITH CONDITIONS:** listed findings to fix or explicitly accept.
- **NOT READY:** the promise is not delivered, a core chapter fails its
  reader, examples the reader depends on do not run, or the document cannot
  be navigated or read by part of its audience.

Include what was not checked (for example: no beta readers yet; no
screen-reader test; deployment chapter not executed) and the validation that
would close each gap, with beta readers and a comprehension check of the
hardest chapter at the top of the list when no reader has seen the book.

## Improving an existing book

1. **Understand the existing work first.** Read it (or the scope) completely
   before proposing anything. Identify what is valuable and must be kept.
2. **Evaluate** in the full-evaluation order (`book-evaluation.md`).
3. **Recommend** changes ranked by reader benefit, with effort and risk.
4. **Ask** before direction changes: audience, promise, chapter order,
   removing chapters, changing the technical stack or versions.
5. **Implement** authorized improvements (`implementation-guidelines.md`).
6. **Maintain consistency** across chapters: terminology list, code style,
   version, running-project state, cross-references.
7. **Review the complete document after revisions**, including the rendered
   output, not only the changed passages.

## Working with the author

- The author owns the book. Recommendations are offered with reasons, and the
  author decides.
- Be honest about substantial problems early. Discovering at stage 12 that
  the book's audience was wrong wastes months.
- Match the author's process: chapter-by-chapter approval, or batches.
- When the manuscript lives in a shared document, prefer suggestion mode or
  tracked changes so every edit is reviewable.
