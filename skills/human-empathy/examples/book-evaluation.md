# Example: a technical book for beginners

A full book evaluation of a short PDF book that promises "no web experience
needed". The code was executed in a scratch virtual environment; the PDF was
rendered and looked at. The evaluation is read-only.

## Contents

- The request
- Framing
- What was done
- The report
- What made this a good run

## The request

> Readers of my beginner book say they get lost in chapter 3. Can you review
> the book and tell me why?

Repository: `chapters/01-setup.md` … `04-accepting-data.md`, `theme/pdf.css`,
`build.sh`, `feedback/reader-notes.md` (three early-access notes).

## Framing

```
⚡ Human Empathy — beginner book review; readers report getting lost in ch. 3

MODE        Full book evaluation, focused on chapter 3 (no edits)
EMPATHY     A self-taught beginner who knows basic Python (functions, dictionaries,
STATEMENT   loops), has never built for the web, reading the PDF on a laptop in the
            evenings, wanting to build and deploy one small API.
PERSON      Stated by the book (ch. 1 opening; subtitle "No web experience needed")
PROMISE     "By the end you will have built a small to-do API and deployed it so
            anyone can use it."
EVIDENCE    Three reader notes (author-collected); no other research
```

## What was done

- Read all four chapters in order, keeping a concept log (term → where used →
  where explained).
- Ran chapter 1's setup and chapter 3's listing in a fresh virtual environment
  with the stated versions (Python 3.12+, FastAPI 0.115, Pydantic 2).
- Built the PDF from the source with a headless browser (pandoc and WeasyPrint
  were not installed), rendered pages with Ghostscript, viewed them, and
  compared rendered code with extracted text.

## The report

```
HUMAN EMPATHY — Full book evaluation · From Zero to API
────────────────────────────────────────────────────────
EXECUTIVE ASSESSMENT
Chapters 1 and 2 meet the reader where they are. Chapter 3 then asks them to
absorb about nine new concepts from one listing, before HTTP itself is
explained, and the listing does not run as printed. Two of the three reader
notes are these exact failures. The book's promise (deploy) is not delivered
in the chapters that exist. The PDF theme makes all of this harder: pale thin
body text, code split across columns, and ligatures that make `--reload` look
like a dash. Overall 2 · Significant weaknesses · confidence HIGH.

CONCEPT LOG, CHAPTER 3 (first listing)
  New in one listing: HTTP routes, decorators, async/await, type hints with
  generics, Pydantic models, BaseSettings, dependency injection (Depends),
  response models, HTTPException/status codes.
  Explained before use: none of them. HTTP is explained last (§3.6).
  Taught in ch. 2: functions, dictionaries, lists.

TECHNICAL ACCURACY (EXECUTED in a scratch venv, FastAPI 0.115.14, Pydantic 2.14)
  FAIL  §1.3 + §3.1  `pip install fastapi` does not install uvicorn;
                     `uvicorn main:app` → "command not found". Fix verified:
                     pip install "fastapi[standard]"
  FAIL  Listing 3.1  `from pydantic import BaseSettings` → PydanticImportError
                     (moved to pydantic-settings). Fix verified:
                     pip install pydantic-settings; from pydantic_settings import
                     BaseSettings. With both fixes the listing serves /tasks,
                     returns 404 for a missing id and 422 for a non-integer id.
  CHECKED  ch. 4     POST listing consistent with ch. 3's model; not run separately.
  NOT PRESENT        Deployment, which the promise names.

CRITICAL FINDINGS

F1  The first listing in chapter 3 does not run, and the reader blames themselves
  Affected reader   Every reader who types or copies it
  Evidence          VERIFIED by execution (above); reader note 2: "Spent an hour
                    thinking I'd installed something wrong." Reader note 3:
                    "uvicorn: command not found."
  Underlying need   To trust that following the book exactly will work
  Root cause        Examples never run in sequence against the stated versions;
                    setup in ch. 1 written before ch. 3's needs were known
  Severity          Critical · Confidence HIGH
  Recommendation    Ch. 1: pip install "fastapi[standard]". Ch. 3: remove Settings
                    from the first listing entirely (see F2); if kept later, add
                    pydantic-settings to the install step. Pin versions in a
                    requirements file the reader can download.

F2  Chapter 3 is a cliff: about nine new concepts arrive at once, none explained first
  Affected reader   The stated reader: knows functions and dictionaries, nothing web
  Evidence          VERIFIED: concept log; "production-grade async REST API with
                    dependency injection, typed models and settings management" in
                    the opening; reader note 1: "I didn't know what @app.get or
                    Depends were."
  Underlying need   One new idea at a time, each with something that works
  Root cause        The chapter shows the author's finished design rather than the
                    reader's next step (curse of knowledge); the outline never
                    mapped concept dependencies
  Severity          Critical · Confidence HIGH
  Recommendation    Rebuild ch. 3 around one tiny endpoint: what HTTP is (move §3.6
                    to the start) → a five-line app returning a list → just enough
                    about decorators to read @app.get → a path parameter. Move
                    async, Depends, BaseSettings and response models to later
                    chapters where a need appears. Needs your decision: it changes
                    the chapter plan (see examples/chapter-improvement.md)

F3  The promise is not delivered
  Evidence          VERIFIED: ch. 1 promises deployment; no chapter deploys
  Severity          High (the book is sold on it) · Confidence HIGH for the chapters
                    supplied; ask whether more chapters exist
  Recommendation    Add the deployment chapter, or change the promise and subtitle

F4  The page design works against reading
  Evidence          VERIFIED in theme/pdf.css and on rendered pages 1–3:
                    9 pt light-weight text in #9b9b9b on cream; two columns on A4
                    with 12 mm margins; justified without hyphenation (visible
                    gaps); script-font headings with h2 and h3 identical; code
                    7 pt grey on near-black, clipped (`Depends(get_se`,
                    `detail="Not fou`) and split across columns; coding ligatures
                    draw `->` as an arrow and `--reload` as a dash while the text
                    layer holds the correct characters
  Severity          High · affects every page; the ligature and clipping defects are
                    Critical for anyone retyping code
  Recommendation    See examples/pdf-visual-review.md for the full visual review

F5  Tone signals that confusion is the reader's fault
  Evidence          VERIFIED: "Obviously" (§3.1), "Simply decorate" (§3.2),
                    "trivially extended" (§3.2), "Now you know how to build APIs!"
                    after a chapter readers report failing
  Severity          Medium · Confidence HIGH (text); feelings are HYPOTHESIS,
                    consistent with reader note 2
  Recommendation    Remove the minimizers; replace the summary with a recap and a
                    check ("You can now…")

F6  One concept, four names
  Evidence          VERIFIED: endpoint, route, path operation, handler used
                    interchangeably in §3.2
  Severity          Medium · Recommendation: "endpoint" in prose; mention FastAPI's
                    "path operation" once, as the docs' name for the same thing

NOT A FINDING
The typo "recieve" (§2.2) is real and trivial: listed for proofreading, not
weighed here.

EMPATHY SCORES (rubric: references/empathy-scoring.md)
  Human Understanding         3   HIGH     Ch. 1–2 fit the reader; ch. 3 abandons them
  Emotional Experience        2   MEDIUM   Failure plus "obviously"; notes 2 and 3
  Cognitive Simplicity        1   HIGH     Nine concepts in one listing
  Clarity and Communication   2   HIGH     Use before explanation; four names
  Personal Relevance          3   MEDIUM   To-do example is fine; no reader-world tie
  Accessibility & Inclusion   2   MEDIUM   Contrast, columns, clipped code; tagging of
                                           the author's WeasyPrint build UNVERIFIED
  Respect for the User        3   MEDIUM   Minimizers, no manipulation
  Practical Value             1   HIGH     The core example fails; deployment absent
  Experience Consistency      3   MEDIUM   Ch. 1–2 vs ch. 3 shift in pace and tone
  Trustworthiness             2   HIGH     Stated versions contradict the code
  Overall                     2 · Significant weaknesses (median 2 of 10; cap
                              applies, Practical Value = 1) · HIGH

RECOMMENDED VALIDATION
- After revising ch. 3: three readers matching the stated profile work through
  ch. 1–3 from a fresh machine while thinking aloud; success = a running /tasks
  endpoint and explaining in their own words what @app.get does.
- Re-run every listing in order on macOS and Windows on each release.
```

## What made this a good run

- The reader notes were checked against the concept log: the stall points
  matched, and the report says so.
- Code was executed rather than eyeballed; both fixes were run too.
- Proofreading stayed at the bottom; the typo did not compete with the cliff.
- The chapter restructure was proposed, not performed: it changes the book's
  plan, which is the author's call.
