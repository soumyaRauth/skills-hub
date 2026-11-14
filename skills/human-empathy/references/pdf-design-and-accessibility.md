# PDF design, readability and accessibility

How to evaluate a book's visual and navigational experience, at the level of
the whole document and of individual pages, and how to actually look at a PDF
with the tools available.

## Contents

- Look at the pages, not just the text
- Tools: a ladder from best to fallback
- What to sample in a long document
- Typography
- Layout
- Visual communication
- Code in books
- Navigation
- Accessibility of the PDF itself
- Screen versus print
- Consistency across the document
- Writing visual findings

## Look at the pages, not just the text

Extracted text tells you what the words are. It cannot tell you how small
they are, how pale, how long the lines are, whether a table split across
pages, whether code wrapped mid-token, or whether a figure sits three pages
from its explanation. Any finding about layout, typography, figures, code
presentation or reading order needs a rendered page behind it.

A visually attractive PDF is not necessarily readable or accessible. Elegant
thin type on a tinted background, decorative headings, full-bleed images and
justified text across a wide page can all look premium and read badly.

## Tools: a ladder from best to fallback

Check what exists (`command -v …`, `python3 -c "import …"`) and use the first
that works. Say which you used.

| Need | Preferred | Fallbacks |
| --- | --- | --- |
| Metadata, page count, page size | `pdfinfo book.pdf` (poppler) | PyMuPDF `fitz.open(p).metadata`; pypdf `PdfReader(p).metadata`; Ghostscript `gs -q -dNODISPLAY -dNOSAFER -c "(book.pdf) (r) file runpdfbegin pdfpagecount = quit"` |
| Fonts and embedding | `pdffonts book.pdf` | PyMuPDF `page.get_fonts()` |
| Text and reading order | `pdftotext -layout` and plain `pdftotext` (compare the two) | PyMuPDF `page.get_text()`; pypdf `page.extract_text()`; Ghostscript `gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=out.txt book.pdf` |
| Render pages to images | `pdftoppm -r 80 -png -f 1 -l 20 book.pdf out/p` | PyMuPDF `page.get_pixmap(dpi=80).save(...)`; Ghostscript `gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r80 -dFirstPage=1 -dLastPage=20 -sOutputFile=out/p-%03d.png book.pdf`; ImageMagick `magick -density 80 book.pdf[0-19] out/p-%03d.png` (needs Ghostscript) |
| Contact sheet of many pages | `magick montage out/p-*.png -tile 6x -geometry 300x+8+8 sheet.png` | Look at pages individually |
| Bookmarks (outline), links | PyMuPDF `doc.get_toc()`, `page.get_links()`; pypdf `reader.outline` | `strings book.pdf \| grep -c /Outlines` (presence only, unreliable with compressed object streams) |
| Tagging, language | pypdf: `"/StructTreeRoot" in reader.trailer["/Root"]`, `/MarkInfo`, `/Lang` | Search raw bytes; treat a negative as `UNVERIFIED` |
| Only the source exists (HTML/CSS, Markdown with a stylesheet) | Run the project's own build | Print the HTML with a headless browser (`chrome --headless --print-to-pdf=out.pdf file:///…/book.html`), then render that; say the output approximates the real build |

Then **view the rendered images** (open them with the file-reading tool, which
displays images) and judge them as a reader would. A contact sheet shows
consistency across many pages at once; individual pages at a readable
resolution show typography.

If nothing can render pages: say so, limit visual findings to what the source
(CSS, LaTeX, Word styles, build configuration) proves, mark the rest
`UNVERIFIED`, and ask the person for screenshots of representative pages.

Never install software on the person's machine without asking. A virtual
environment in a scratch directory for a Python library is a reasonable
proposal; say what it is for.

## What to sample in a long document

Render a contact sheet of every page if the document is under a few hundred
pages, to spot inconsistency. Then inspect at reading resolution:

- the cover, title page, copyright page and table of contents;
- the first page of every chapter (openings set the reader's expectations);
- the densest text page you can find;
- every kind of special element at least once: code block, long code listing,
  table (especially one crossing a page break), figure, screenshot, callout,
  warning, footnote, equation;
- the index and glossary;
- any page a reader or the author has complained about.

## Typography

| Aspect | Look for | Conventional range (judge against the reading device) |
| --- | --- | --- |
| Body font | A text face designed for reading at length; serif or sans both fine | Decorative, condensed, very light or script faces for body text are findings |
| Size | Comfortable at the intended size: print page, tablet, laptop at 100% zoom | Roughly 10–12 pt for print-sized pages; on-screen PDFs often need the upper end or more |
| Weight and colour | Enough contrast between text and background | Light grey or thin weights on tinted backgrounds are the classic attractive-but-unreadable failure; WCAG's 4.5:1 for body text is a sound target (conformance is `standards-compass`'s call) |
| Line length | Easy return to the next line | Around 45–75 characters per line is the long-standing typographic convention; very long lines on wide single columns tire readers |
| Line height | Lines separated enough to track | Roughly 1.2–1.5 times the font size for body text |
| Letter spacing | Normal for body text | Tracking added to lowercase body text hurts reading |
| Alignment | Even word spacing | Justified text without hyphenation produces rivers and gaps, worst in narrow columns |
| Paragraph spacing | Paragraphs distinguishable | Either indent or space, consistently |
| Headings | Clear hierarchy by size, weight and space; distinguishable levels | Levels that look alike; decorative heading fonts that slow scanning |
| Code font | Monospaced, distinguishable `0/O`, `1/l/I`, sized to match body text | Proportional fonts for code; tiny code; ligatures that change how operators look to beginners |

Treat the numeric ranges as conventions, not laws. A large-print book, a
children's book or a slide-like workbook legitimately differs.

## Layout

- **Margins:** enough to hold the page comfortably and for binding in print;
  generous enough on screen that text is not crammed against the edge.
- **Text density and white space:** pages that feel like a wall of text, or
  so sparse the reader keeps turning pages.
- **Columns:** two columns are hard on screen (scroll up and down) and break
  code; single column is usually better for technical PDFs read on screens.
- **Alignment and grid:** elements share edges; captions align with figures.
- **Page balance:** widows and orphans (single lines stranded at the top or
  bottom), headings at the foot of a page with their text on the next,
  half-empty pages before every figure.
- **Visual hierarchy:** the eye goes first to what matters most on the page.
- **Consistency:** the same element looks the same everywhere.

## Visual communication

For every diagram, illustration, chart, table, screenshot and callout:

- Does it make the idea easier to understand than words alone? If not, it is
  decoration (coherence principle) and adds load.
- Is it next to the text that explains it, and referred to from that text?
- Is it legible at the reading size? Screenshots shrunk until their text is
  unreadable are common.
- Are labels on the diagram itself rather than in a distant legend?
- Do colours carry meaning that colour-blind readers or greyscale printing
  would lose?
- Tables: a header row, units, alignment of numbers, repeated headers across
  page breaks, not so wide they shrink to illegibility.
- Callouts (notes, tips, warnings): few kinds, consistently styled, with the
  warning style reserved for real risk. When every page has three callouts,
  readers stop reading them.

## Code in books

- Code blocks are visually distinct, high-contrast, and in a monospaced font.
- Long lines wrap visibly (with a continuation marker) or are reformatted;
  silent wrapping that breaks a command when copied is a defect.
- Copying from the PDF gives working code: no curly quotes, no line numbers
  mixed into the text, no hyphenation inside identifiers. Test by extracting
  the text of a code block and checking it.
- **What the page shows can differ from what the text layer holds.** Coding
  ligatures draw `->` as an arrow and `--` as a dash, so the extracted text is
  correct while a beginner retyping from the page types the wrong
  characters. Compare the rendered code with the extracted code; a
  difference is a finding that text extraction alone can never reveal.
- Nothing is clipped: `overflow: hidden` or a fixed box width can cut the
  ends off long lines, in the picture and in the text layer alike.
- Code listings are not split across columns or pages mid-statement; a
  two-column layout almost guarantees it.
- What the reader types is distinguishable from output and from prompts
  (`$`, `>>>`).
- Syntax highlighting, if used, survives the background and greyscale print.

## Navigation

- **Table of contents** with page numbers, and in a PDF, clickable.
- **Bookmarks (outline)** matching the chapter and section structure; their
  absence makes a long PDF hard to navigate in every viewer.
- **Page numbers** present, and the printed page numbers matching the PDF's
  page labels where possible, so "page 47" means one thing.
- **Running headers or footers** telling the reader where they are.
- **Internal links and cross-references** that work and land on the right
  place; "see page 112" in a reflowed e-book is a finding.
- **External links** meaningful as text ("the FastAPI tutorial", not "click
  here") and not dead.

## Accessibility of the PDF itself

- **Real text:** selectable and searchable, not images of text (scanned pages
  need OCR).
- **Tagged PDF** with a structure tree, so assistive technology knows headings,
  lists, tables and reading order. Check for `/StructTreeRoot` and
  `/MarkInfo`.
- **Reading order:** compare `pdftotext` (or equivalent) output against the
  visual order. Sidebars, callouts and multi-column layouts often come out
  interleaved.
- **Heading structure:** tags or at least bookmarks reflecting the real
  hierarchy.
- **Document language** set (`/Lang`), and a meaningful document title in the
  metadata.
- **Alternative text** for informative images; decorative images marked as
  artifacts.
- **Tables** with header cells.
- **Fonts embedded** so the text renders and extracts correctly everywhere.

Report what the inspection found and what it could not establish. Whether the
PDF meets PDF/UA or WCAG is a conformance question; hand it to
`standards-compass` with the evidence, or say plainly that conformance was not
assessed. Testing with an actual screen reader is the only way to know what a
screen-reader user experiences; recommend it rather than claiming it.

## Screen versus print

Ask, or infer from the distribution channel, how the book is read:

- **Screen PDFs** (most technical e-books): single column, larger type,
  bookmarks and links matter most, no wasted blank verso pages, colour fine.
- **Print:** binding margins, colour that survives greyscale, no reliance on
  links, facing-page layout.
- **Reflowable e-books** (EPUB): fixed page layouts, page references and
  wide tables break; reading order and semantic structure matter most.

A layout optimized for the wrong medium is a finding even when it is
beautiful for the right one.

## Consistency across the document

On the contact sheet and the sampled pages, look for: heading styles that
drift between chapters, different code styles in different chapters (often a
sign chapters were written separately), inconsistent callout styles, figure
numbering gaps, varying margins, mixed fonts from pasted content, chapters
that start on different page sides without reason.

## Writing visual findings

Each visual finding names the page(s), what was seen, the reader it affects,
and the effect on reading or learning, not just the aesthetics:

```
Finding        Body text is light grey (#9a9a9a) on white at about 9 pt
Pages          All body pages; rendered p. 5, 12, 31 inspected
Evidence       VERIFIED in theme/pdf.css (body color, font-size); seen on renders
Reader         Anyone reading at length, especially on a laptop at 100% zoom or
               with low vision
Impact         Slower reading and fatigue; likely to make long chapters feel
               harder than they are (SUPPORTED: contrast and size conventions)
Severity       High: affects every page of the book
Fix            Body text near-black (#1a1a1a or similar), 11 pt, line-height 1.45
```
