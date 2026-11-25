# Technical SEO

Technical SEO decides whether search engines can find, fetch, understand and
index the pages at all. On a small site, a single wrong directive can
outweigh everything else. On a healthy site, technical work has diminishing
returns, and the time goes to content and authority instead.

## Contents

- Rules for technical findings
- Severity
- Crawlability
- Indexability
- URLs and hosts
- Architecture and internal links
- Rendering and JavaScript
- Performance and Core Web Vitals
- Mobile, semantics and accessibility
- Status codes, redirects and broken links
- Security
- International
- Finding format

## Rules for technical findings

- **Verify before reporting.** Fetch the URL, read the header, read the
  source. A checklist item is not a finding until it is observed on this
  site.
- **Name the affected URLs**, or the pattern and a count from the crawl.
- **Give evidence**: the response header, the tag, the crawl row, the file
  and line.
- **Explain the impact** in one plain sentence.
- **Give a fix that fits the framework** (`references/implementation.md`).
- **Separate the critical from the cosmetic.** Ten low findings do not
  outrank one critical one.
- **Ask first** for changes in the approval column of `SKILL.md`: robots,
  noindex, canonicals that move indexing, sitemaps, redirects, URL changes,
  host or protocol policy, rendering or architecture.

## Severity

| Severity | Means | Example |
| --- | --- | --- |
| Critical | Important pages cannot be indexed, or the site risks dropping out | `noindex` on the homepage or about page; `Disallow: /` in production; the whole site canonicalized to another host |
| High | Important pages are substantially harder to discover or understand | Canonical to a wrong URL; key pages only reachable through JavaScript actions; broken links from navigation; sitemap full of redirects |
| Medium | Weakens many pages or one important one | Duplicate titles across a section; orphaned pages; redirect chains; large layout shifts |
| Low | Minor or hygiene | Missing alt on decorative images; a few long titles; one internal link to a redirect |

## Crawlability

| Check | Verify with | Typical fix |
| --- | --- | --- |
| `robots.txt` exists, returns 200, and blocks nothing important | `seo_audit.py robots <url> --path /important/` | Narrow the rule (approval) |
| `robots.txt` does not block CSS or JS needed to render | Same, on asset paths | Allow the assets (approval) |
| Sitemap is reachable and named in `robots.txt` | `seo_audit.py sitemap <url>` | Add the `Sitemap:` line (approval) |
| Important pages are linked with real `<a href>` links | Crawl: discovered by links, not only via the sitemap | Add links in navigation or content |
| No orphans: every indexable page has an internal link | Crawl: in sitemap, zero inlinks | Link from a relevant page or hub |
| Important pages are shallow | Crawl depth; three clicks from home is a sensible ceiling for key pages | Hubs, navigation, contextual links |

Remember: `robots.txt` controls crawling, not indexing. A blocked URL can
still be indexed from links, without its content, and a `noindex` on a
blocked page is never seen.

## Indexability

| Check | Verify with | Typical fix |
| --- | --- | --- |
| No unintended `noindex` (meta robots, `googlebot` meta, `X-Robots-Tag`) | `seo_audit.py page` shows both the tag and the header | Remove (approval) |
| Canonical is present, absolute, self-referencing on unique pages, and points to a 200, indexable URL on the canonical host | `seo_audit.py page`; the crawl flags canonicals to other URLs | Correct the template (approval when it moves indexing) |
| Duplicate content variants resolve to one URL | Fetch variants: parameters, trailing slash, case, `index.html` | Canonical or redirect (approval) |
| Pagination pages are crawlable and self-canonical, not canonicalized to page one | Fetch page 2 | Fix the template |
| Soft 404s: pages that say "not found" or are empty but return 200 | Crawl: tiny word counts; fetch the missing-page URL | Return 404 or 410 |
| Unneeded pages are not indexable: tag archives with one post, internal search results, staging copies | Crawl and sitemap | `noindex` or remove from sitemap (approval) |
| Indexing status | Search Console page indexing report or URL Inspection, through the owner | `UNKNOWN` without it; a `site:` search is only a sample |

## URLs and hosts

- One canonical origin: HTTPS, one host (`www` or apex). Every other variant
  answers with one permanent redirect to it. Verify all four variants.
- Trailing slash: either style is fine; be consistent, and make the other
  form redirect or canonicalize.
- Readable, stable URLs with words, not IDs, for content pages. Never change
  existing URLs for cosmetic reasons; a change needs a redirect and approval.
- Query parameters that do not change content (tracking, sorting) should not
  create indexable duplicates.

## Architecture and internal links

- A clear hierarchy: home → sections or hubs → pages, with breadcrumbs where
  the depth warrants them.
- Pillar pages link to their supporting pages and back
  (`references/content-strategy.md`).
- Navigation exposes what matters for the owner's goal.
- Internal linking rules: `references/on-page-seo.md`.

## Rendering and JavaScript

- Compare the raw HTML (`seo_audit.py page`) with what a browser renders. If
  the title, main content, links or structured data exist only after
  JavaScript runs, search engines may see them late or not at all.
- Links must be `<a href="...">` with real URLs, not click handlers or
  fragment routes.
- Each route must return its own title, description and canonical in the
  initial HTML on a server-rendered or static site.
- A client-only single-page app is a structural risk. Moving to static
  generation or server rendering is an architecture change: propose it with
  its cost, and hand implementation to `proof-driven-dev`.

## Performance and Core Web Vitals

Measure; do not guess.

- Field data (the Chrome UX Report, shown in PageSpeed Insights and Search
  Console) reflects real users and is what the Core Web Vitals assessment
  uses. Small sites often have none. Then lab data (Lighthouse) is a
  diagnostic, not a verdict.
- Google's "good" thresholds, at the 75th percentile of page loads: LCP at
  most 2.5 s, INP at most 200 ms, CLS at most 0.1. Check current values in
  Google's documentation before quoting them in a report.
- Usual fixes: sized images (`width` and `height`), modern formats and
  responsive sizes, no lazy-loading on the main above-the-fold image, fewer
  render-blocking scripts and styles, `font-display` for web fonts, less
  JavaScript on content pages.
- Performance is one signal among many. Do not rebuild a site for a few
  milliseconds when its content and links are the real gap.

## Mobile, semantics and accessibility

- A `viewport` meta tag; content and links usable on a phone. Google indexes
  the mobile version of pages.
- `<html lang>` set correctly.
- One clear `<h1>` describing the page; headings in a logical order.
- Descriptive link text; `alt` text on meaningful images, empty `alt=""` on
  decorative ones.
- Semantic elements (`<main>`, `<nav>`, `<article>`) help every machine
  reader. Accessibility conformance verdicts belong to `standards-compass`.

## Status codes, redirects and broken links

- Important pages return 200 directly, not through redirects.
- Removed pages return 404 or 410, or redirect to a true equivalent; never
  redirect everything to the homepage.
- Redirects are permanent (301 or 308) when the move is permanent, and one
  hop long. Update internal links to point at the final URL.
- Internal links never point to 4xx or 5xx pages. The crawl lists them with
  their source pages.
- Avoid meta-refresh and JavaScript redirects for moved pages.

## Security

- HTTPS everywhere, with no mixed content on pages.
- No unexpected pages, links or content (a symptom of a hacked site): check
  the crawl and the sitemap for pages the owner does not recognize.
- Report a suspected compromise to the owner at once, in one line, before
  any SEO work continues.

## International

Only when the site serves several languages or regions:

- One URL per language version; never switch language by cookie or IP alone.
- `hreflang` annotations: valid language (and optional region) codes,
  every version listing every other and itself, and `x-default` where a
  fallback exists. In HTML, HTTP headers or the sitemap, consistently.
- Localized titles, descriptions and content, not machine output left
  unreviewed; hand translation quality to `practical-localizer`.

## Finding format

```
T-3  High · /blog/airflow-retries/ canonical points to another host
     Evidence: <link rel="canonical" href="http://www.example.com/blog/airflow-retries/">
               (VERIFIED, seo_audit.py page, 2026-11-25); the site serves https://example.com
     Impact:   search engines may index the wrong URL or ignore the canonical
     Fix:      layouts/post.html line 12 builds the URL from the old config value;
               use the site URL setting (approval: changes indexing)
     Task:     SEO-006
```
