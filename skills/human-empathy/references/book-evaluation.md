# Evaluating books and educational material

A book is a designed journey that takes a reader from where they are to where
they hoped to get. This file covers what applies to every kind of book or
document: reading it properly, the reader and the promise, the architecture,
and chapter-level review. The detail lives in the sibling files:
`learning-experience.md` (does it teach), `editorial-standards.md` (the
writing), `pdf-design-and-accessibility.md` (the page), `technical-accuracy.md`
(can it be trusted).

## Contents

- What counts as a book here
- Reading it properly
- The reader
- The promise
- Architecture
- Chapter-level review
- Front and back matter
- Writing the book-level findings
- Full evaluation order

## What counts as a book here

PDF books, e-books, technical and programming books, non-fiction, textbooks,
workbooks, learning guides, tutorials, documentation sets, training manuals,
instructional material, reports and research-based publications. The format
changes the checks (a documentation site has search and links, a print PDF
has page numbers and running heads); the reader-first method does not.

## Reading it properly

- **Get the source and the output.** Markdown, LaTeX, Word, a Google Doc or a
  docs folder is where changes happen. The PDF, EPUB or site is what the
  reader meets. Inspect both when both exist; when only one exists, say what
  that hides.
- **Read in reading order.** A chapter's problems often come from what the
  earlier chapters did or did not establish. To evaluate chapter 5 properly,
  read at least the table of contents, the introduction, and the chapters it
  depends on.
- **Large books:** read the table of contents, introduction, conclusion, and
  first and last pages of every chapter; then read fully the chapters in scope
  and every chapter a finding depends on. Say which chapters were read in full
  and which were sampled. Never generalize from a sample without saying so.
- **Keep a running log** while reading: each new term and where it is
  defined (or not), each forward reference, each prerequisite assumed, each
  place you as a newcomer would stall. That log becomes the progression and
  terminology findings.
- **Look at rendered pages** for anything visual. Extracted text hides
  layout, reading order, code formatting and figure placement.

## The reader

Answer before judging (`human-research.md` has the full method):

- Who is the reader, and why would they buy or open this?
- What problem are they trying to solve, and what outcome do they expect?
- What do they already know? What do they believe that is wrong?
- What are they afraid of or confused about? (Beginners often fear being too
  slow or "not a real programmer"; experts fear wasted time.)
- What complexity can they handle, and at what pace?
- What would make the book feel worth the money and the hours?

**Writing for the author's level** is the most common failure. Signs: terms
used before they are defined; steps skipped because they are obvious to the
author; examples drawn from the author's world rather than the reader's;
"simply", "just", "obviously", "trivially" before something that is none of
those for the reader.

**Evidence about readers** may already exist: reviews, reader emails, course
feedback, errata, questions in forums, beta-reader notes. Read them before
inferring, and quote them as what those readers said, not as what all readers
think.

## The promise

Every book makes a promise through its title, subtitle, cover or landing copy,
introduction and table of contents: *who it is for* and *what they will be
able to do*.

- State the promise in one sentence as a reader would understand it.
- Check that the content delivers it. A book called *Build and Deploy Your
  First API* that never deploys has broken its promise, however good the rest
  is.
- Check that the stated audience matches the actual difficulty. A "for
  complete beginners" book that assumes command-line fluency excludes the
  people it invited.
- Check that the content does not drift into a different book (an
  advanced-topics chapter that serves the author's interests, not the
  reader's outcome).

## Architecture

Evaluate the whole structure against the reader's journey:

| Element | Questions |
| --- | --- |
| Title and subtitle | Does a member of the intended audience recognize themselves and their problem? Is it honest about level and scope? |
| Introduction | Does it say who the book is for and not for, what they need beforehand, what they will be able to do, and how to use the book? |
| Learning outcomes | Are they stated, concrete and checkable ("deploy a Python API to a cloud host") rather than vague ("understand APIs")? |
| Table of contents | Can a reader see the path, and find their place? Do chapter titles say what the reader will do or learn? |
| Chapter sequence | Does each chapter need only what came before? Does difficulty rise steadily, with no cliffs? |
| Section hierarchy | Are heading levels consistent and meaningful? Is any section too long to hold in mind? |
| Chapter openings | Do they say why this matters, what the reader will get, and what it builds on? |
| Chapter conclusions | Do they consolidate, check understanding and bridge to what is next? |
| Examples and case studies | Are they realistic for this reader, and do they recur in a way that builds (a running project) rather than restarting each chapter? |
| Exercises | Do they practise the chapter's outcome at a reachable difficulty, with answers or ways to check? |
| Summaries and recaps | Present where load is high; absent where they would only repeat? |
| References, glossary, appendices | Do they support the reader (setup instructions, a glossary of the terms actually used, troubleshooting) or just pad? |
| Further learning | Does the reader know where to go next? |

Identify and name:

- **Missing explanations and prerequisites:** a concept used before it is
  taught, or never taught.
- **Wrong order:** a concept taught after the chapter that needed it.
- **Cliffs:** a chapter whose difficulty jumps beyond what the previous one
  prepared.
- **Unnecessary chapters:** content that does not serve the promise.
- **Repetition:** the same concept explained afresh in several places,
  sometimes inconsistently.
- **Poor transitions:** chapters that start cold, with no link to the last.
- **Incomplete journeys:** the reader is taught pieces but never assembles
  them into the outcome promised.

Do not assume the conventional structure is best. A troubleshooting guide is
better organized by symptom than by theory; a reference by lookup; a beginner
book by a running project. Choose the structure that makes the material
easiest to understand and use, and say why.

## Chapter-level review

For a single chapter, in context:

1. **Position:** what the reader knows on arriving (from earlier chapters and
   stated prerequisites) and what they must know on leaving (for later
   chapters and the promise).
2. **Opening:** why it matters, what the reader will be able to do, what it
   builds on.
3. **Concept inventory:** list every new concept, term and tool in order of
   first appearance, and where (if anywhere) each is explained. Count how many
   arrive at once. This is the most reliable way to find overload and
   forward references.
4. **Explanation quality:** each concept gets the why, the what, an example,
   and its boundaries (when not to use it, common mistakes).
5. **Practice:** something to do that uses the chapter's outcome.
6. **Close:** summary, check of understanding, bridge forward.
7. **Reader walk:** read it as the person in the empathy statement and mark
   where they stall. Supplied reader feedback about the chapter is evidence;
   check whether your stall points match it, and say so either way.

## Front and back matter

Often neglected, often where readers decide whether to continue:

- **Setup instructions:** the first place beginners fail. Every command must
  work on the platforms the book names, in the versions it names
  (`technical-accuracy.md`).
- **Conventions page:** how code, commands, notes and warnings look, and what
  the reader should type versus read.
- **Code downloads:** link works, code matches the book, versions pinned.
- **Index and glossary:** cover the terms readers actually look up.
- **Errata and support:** where to report a problem and get help.

## Writing the book-level findings

Use the finding format in `reporting.md`. For books, "affected reader" names
the reader and the moment ("a beginner arriving at section 3.2 without having
seen decorators"), and "evidence" cites the location precisely (chapter,
section, page or line). Keep pedagogical, editorial, structural, technical
and visual findings distinct; they have different owners and different fixes.

## Full evaluation order

For a whole book, in this order, because each step can invalidate the next:

1. Reader and promise (does it know who it is for and what it gives them?).
2. Architecture (does the path lead there?).
3. Technical accuracy of anything the reader will run or rely on.
4. Learning experience chapter by chapter.
5. Writing.
6. Visual design, navigation and accessibility of the rendered output.
7. Proofreading, last, and only as a summary of patterns unless asked for a
   line-by-line pass.

Proofreading is never a substitute for substantive editorial evaluation, and
beautiful page design is never a substitute for good teaching. A report that
spends its first page on typos while chapter 3 assumes knowledge the reader
was never given has its priorities wrong.
