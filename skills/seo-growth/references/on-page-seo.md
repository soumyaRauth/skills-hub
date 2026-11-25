# On-page SEO

One page, one job: satisfy the search intent it targets better than the
alternatives, and make that obvious to both the reader and the search engine.
Every change on a page starts from its intent, not from a checklist score.

## Contents

- The page workflow
- Intent first
- Titles
- Meta descriptions
- Headings
- Content
- Images
- URLs
- Freshness
- Social metadata
- Internal linking
- Ignore these

## The page workflow

For `page <url or path>`:

1. Find the page in `content.md` and `keywords.md`: its role, its keyword
   group, its intent. If it has none, decide it now or record that the page
   does not target search.
2. Take a snapshot of the primary query: what format and depth win, and
   what they leave out.
3. Run `seo_audit.py page` on it. Read the whole page as a visitor would.
4. List the gaps against intent, competitors, the site's other pages, and
   the checks below. Each gap gets evidence.
5. Make the safe changes (titles, descriptions, headings, alt text, internal
   links, structured data that matches the content). Draft content additions;
   anything that needs the owner's experience or facts gets a question or a
   placeholder, never an invention.
6. Validate: re-run the audit, build, compare before and after.
7. Record: `content.md` row, the task, an experiment if the page has data to
   measure against (`references/experimentation.md`).

## Intent first

- Does the page answer what people searching its query want, in the format
  the results suggest (a tutorial, a comparison, a profile, a tool)?
- Is the answer near the top, or buried under preamble?
- Does it serve one intent? A page trying to be a tutorial, a sales page and
  a news post serves none well.

## Titles

Search engines usually build the result's title link from the `<title>`, and
may rewrite it when it is vague, stuffed or mismatched.

- Unique per page, describing that page specifically.
- The primary topic early and natural; the brand or name at the end when it
  helps (`Airflow retries, explained with real failures | Jane Doe`).
- For the homepage and about page of a personal site: the person's full name
  and role.
- No repetition of keywords, no lists of variants, no clickbait the page
  does not deliver.
- Length: concise enough to read at a glance; long titles get truncated in
  display. Do not pad or trim to hit a character count.

## Meta descriptions

Search engines may show the description as the snippet, or pick text from the
page. It influences whether people click, not where the page ranks.

- Unique per page, an accurate summary of what the visitor gets.
- Written for the searcher: what is here, for whom, why it is worth it.
- No keyword lists, no promises the page does not keep.

## Headings

- One `<h1>` that states what the page is; it usually echoes the title.
- `h2`–`h4` in logical order, outlining the content so a skimmer can find
  their part.
- Keywords appear where they are natural. Never force one into every heading.

## Content

Judge content by usefulness, not length:

- Answers the actual question completely, with the specifics a practitioner
  would include: steps, code, numbers with sources, trade-offs, failure cases.
- Shows first-hand experience where the owner has it: their project, their
  incident, their data. That is what competing pages usually lack.
- Accurate, current, with external references to primary sources where
  claims need support.
- Clear structure, short paragraphs, examples, and no filler introduction.
- Covers the subtopics the intent requires (from the snapshot and
  community questions), and stops there.

Never: keyword density targets, invented statistics or citations, fabricated
experience, padding to a word count, or copying competitors' structure. See
`references/content-strategy.md` for drafting rules.

## Images

- Descriptive `alt` text on meaningful images (what the image shows, in
  context); `alt=""` on decorative ones. Never keyword lists.
- Descriptive file names for new images.
- `width` and `height` set; compressed, responsive, modern formats.
- Images near the text they illustrate.

## URLs

- Short, readable, lowercase words separated by hyphens for new pages.
- Never change an existing URL for SEO cosmetics. A change needs a permanent
  redirect, updated internal links, and approval.

## Freshness

- Update content when the facts change, and show the updated date when the
  update is substantial.
- Never change a date without changing the content. That misleads readers
  and search engines alike.

## Social metadata

Open Graph and similar tags control how links look when shared. They are not
ranking signals, but they shape the personal brand wherever the site is
shared. Set `og:title`, `og:description`, `og:image` and `og:url` on key
pages when the framework supports it cheaply.

## Internal linking

Internal links tell readers and search engines which pages matter and how
they relate.

- **Find opportunities:** pages that mention a topic another page covers in
  depth; pillar pages and their supporting pages; orphans and pages with very
  few inlinks (from the crawl); important pages buried deep.
- **Anchor text:** natural, descriptive phrases that tell the reader where
  the link goes. Vary them naturally; do not repeat one exact-match phrase
  sitewide.
- **Placement:** contextual links in the body carry the most meaning;
  navigation and footer links are for what matters on every page, not a
  place to list keywords.
- **Relevance:** link because the reader would want to go there next. No
  irrelevant cross-links, no link blocks added only for search engines.
- **Fix:** links to redirects (point to the final URL) and broken links.

Record each change: source page, target page, anchor text, date.

## Ignore these

- The `keywords` meta tag: Google does not use it.
- Plugin "SEO scores" and green lights: useful as reminders, not as goals.
- Exact character counts, keyword density, "LSI keywords": not how search
  engines evaluate pages.
