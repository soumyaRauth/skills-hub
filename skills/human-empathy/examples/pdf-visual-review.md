# Example: an attractive PDF that is hard to read

A PDF visual review of a book whose theme looks premium in a thumbnail and
reads badly at length. It shows the rendering ladder when the preferred tools
are missing, and a finding only rendered pages could produce.

## Contents

- The request
- Getting at the pages
- What the pages show
- The report
- What made this a good run

## The request

> I paid for a nice editorial theme for my book. Can you check the PDF is
> easy to read?

## Getting at the pages

```
⚡ Human Empathy — PDF readability review of the book theme

MODE        PDF visual review (no edits)
READER      Beginners reading on a laptop at 100% zoom, often for an hour at a time
            (from the book's README and introduction; ASSUMED device)
TOOLS       poppler: not installed · PyMuPDF, pypdf: not installed ·
            Ghostscript: available · ImageMagick: available
            Built PDF not in the repository and pandoc/WeasyPrint not installed:
            built the HTML from the chapters with the theme CSS and printed it with
            a headless browser. Rendering approximates the author's build; fonts
            fall back where the theme's fonts are not installed.
RENDERED    All 3 pages at 80 dpi (contact sheet), page 2 at 110 dpi
TEXT LAYER  Ghostscript txtwrite, page 2
```

Commands used:

```
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r80 -sOutputFile=out/p-%03d.png book.pdf
magick montage out/p-*.png -tile 6x -geometry 300x+8+8 sheet.png
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -dFirstPage=2 -dLastPage=2 -sOutputFile=p2.txt book.pdf
```

## What the pages show

At thumbnail size the pages look elegant: cream paper, gold script headings,
dark code panels. At reading size, page 2:

- Body text is thin, pale grey and small, on cream.
- Two columns on A4; justified text opens wide gaps ("Depends(get_settings)
  ··· tells ··· FastAPI ··· to ··· call").
- The chapter 3 listing is split across both columns, and its long lines are
  cut off at the panel edge: `Depends(get_se`, `detail="Not fou`.
- In the code, `def get_settings() -> Settings:` is drawn with an arrow, and
  `uvicorn main:app --reload` with a single long dash.
- "3.5 Response models" sits alone at the foot of the page; its text is on the
  next.

The text layer for the same page contains `->` and `--reload` correctly. A
reader who copies gets the right characters; a reader who retypes from the
page, which is what beginners are told to do, types an arrow and a dash and
gets a syntax error or an unrecognized option. Text extraction alone would
have passed this page.

## The report

```
HUMAN EMPATHY — PDF visual review · From Zero to API
────────────────────────────────────────────────────────
EXECUTIVE ASSESSMENT
The theme optimizes for how a page looks at a glance, not for an hour of
reading or for retyping code. Two defects break code for beginners (clipping
and ligatures); the rest slow every page. All of them are in one stylesheet,
so the fix is one file. No scores: the scope is the visual layer only.

F1  Code is cut off and split across columns          Critical · HIGH
    Evidence   VERIFIED on render p. 2 and in the text layer (truncated in both);
               theme/pdf.css: pre { white-space: pre; overflow: hidden },
               body { column-count: 2 }
    Reader     Anyone copying or retyping listings
    Fix        Single column; pre { white-space: pre-wrap; overflow-wrap: anywhere }
               with a visible continuation, or shorter lines in the source;
               break-inside: avoid for short listings

F2  The page shows different characters from the code   Critical · HIGH
    Evidence   VERIFIED: `->` and `--` rendered as arrow and dash (p. 2), correct in
               the text layer; font-variant-ligatures: common-ligatures on code
    Reader     Beginners retyping from the page
    Fix        font-variant-ligatures: none on pre and code

F3  Body text is too faint and small for long reading     High · HIGH
    Evidence   VERIFIED in CSS: 9 pt, weight 300, #9b9b9b on #fdf8f0; visible on render
    Impact     Slower reading and fatigue across the whole book (SUPPORTED: contrast
               and size conventions). Computed contrast 2.6:1 against the 4.5:1
               target for body text; conformance verdict
               HANDOFF → standards-compass
    Fix        Near-black text (#1f1f1f), regular weight, 11 pt, line-height 1.45

F4  Two justified columns on screen                         High · HIGH
    Evidence   VERIFIED: column-count: 2, text-align: justify, hyphens: none; gaps
               visible on p. 2
    Reader     Screen readers of a screen PDF scroll down, up, down per page
    Fix        One column, about 65–75 characters per line (wider margins), left
               aligned, or justified with hyphenation

F5  Heading levels look the same, in a script face          Medium · HIGH
    Evidence   VERIFIED: h2 and h3 both 20 pt "Great Vibes"/script; render p. 2
    Fix        A readable heading face; distinct sizes or weights per level

F6  Code contrast                                           Medium · HIGH
    Evidence   VERIFIED: #5c6370 on #2b2b2b at 7 pt, computed contrast 2.3:1
    Fix        Light text on the dark panel, 9–10 pt

F7  Navigation                                              Medium · LOW
    Evidence   No outline in the browser build; the author's WeasyPrint build was
               not available. UNVERIFIED for the real book
    Fix        Ensure bookmarks for chapters and sections; check in the real build

KEEP
The cream page and gold accent can stay as accents: on headings, rules and
callouts, not on body text.

VALIDATION
Re-render after the CSS change; compare retyped listings with the text layer;
ask two readers to read chapter 3 on a laptop for 20 minutes and report where
they slowed down. A screen-reader pass on the real build.
```

## What made this a good run

- The tool ladder was followed and the fallback said so, including that the
  rendering approximates the author's build.
- The most serious finding came from comparing the picture with the text
  layer.
- Every fix is a stylesheet change, so it stays consistent across the book.
- No overall score for a single-layer review, and the contrast conformance
  question went to `standards-compass`.
