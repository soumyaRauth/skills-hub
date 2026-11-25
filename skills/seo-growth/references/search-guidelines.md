# Search guidelines and safety

Sustainable SEO is what still works after the next update. It follows the
search engines' own published guidance, which in Google's case is Google
Search Essentials: technical requirements, spam policies, and key best
practices.

## Contents

- Check the current guidance
- Official sources
- What the guidance rewards
- Spam policies to never break
- Myths and distractions
- When the owner asks for a risky tactic

## Check the current guidance

Search guidance changes. Before a significant strategy or a claim about how
Google behaves, check the current official page, with a fetch or a search,
and cite it with the date. When the official page and this file disagree,
the official page wins; note the difference in `history.md`.

## Official sources

Prefer these over blogs and social posts:

- Google Search Central documentation (developers.google.com/search): Search
  Essentials, the SEO starter guide, crawling and indexing, structured data
  and the Search Gallery, page experience and Core Web Vitals, international
  sites, JavaScript SEO.
- Google's spam policies for web search.
- Google's guidance on creating helpful, reliable, people-first content, and
  on AI-generated content.
- Search Console Help.
- The Google Search Status Dashboard and the Search Central blog, for updates.
- Bing Webmaster Guidelines, for Bing.
- schema.org, for vocabulary; web.dev, for performance.

## What the guidance rewards

- Content made primarily for people: helpful, reliable, original, written
  with real expertise or first-hand experience, accurate, and satisfying.
  Google's self-assessment asks **who** created the content (is it clear?),
  **how** it was created (including any automation, disclosed where readers
  would expect it), and **why** (to help people, rather than to attract
  search visits).
- Pages search engines can crawl, render and index, on a site that serves a
  consistent canonical version.
- Clear titles, headings, descriptive links and image text that help both
  people and machines.
- Links that people choose to give because the content is worth it.

E-E-A-T (experience, expertise, authoritativeness, trust) is a framework
from Google's quality rater guidelines. It describes what good results look
like; it is not a score or a single ranking factor to optimize.

## Spam policies to never break

| Policy | In practice, never |
| --- | --- |
| Cloaking | Show search engines different content from visitors |
| Doorway abuse | Create many similar pages to funnel searchers, such as one per city or per keyword variant |
| Expired domain abuse | Buy an old domain to borrow its reputation for unrelated content |
| Hidden text and links | Text or links visible to search engines but not to people |
| Keyword stuffing | Pad pages, titles, alt text or markup with repeated keywords |
| Link spam | Buy, sell or trade links that pass ranking credit; link schemes; spammy guest posts, comments or directories |
| Machine-generated traffic | Automate queries or traffic to search engines |
| Misleading functionality | Pages that pretend to offer something they do not |
| Scaled content abuse | Generate many pages mainly to rank, by any method, including AI, with little value for people |
| Scraping | Republish others' content without adding substantial value |
| Sneaky redirects | Send people somewhere other than what search engines see |
| Site reputation abuse | Host third-party content to exploit the site's ranking signals |
| Thin affiliation | Affiliate pages with no original value |
| User-generated spam | Leave spam in comment sections or forums the site runs |

Also never: fake reviews or ratings, structured data that does not match the
page, fabricated credentials or affiliations, impersonation, or attacks on
another site.

## Myths and distractions

Do not spend the owner's time on these, and correct them gently when the
owner raises them:

- The `keywords` meta tag (unused by Google).
- Keyword density targets and "LSI keywords".
- Minimum word counts.
- Third-party "authority" scores as goals: vendor metrics, not Google's.
- Sitemap `priority` and `changefreq` values (Google ignores them; accurate
  `lastmod` can help).
- Submitting the site to hundreds of search engines or directories.
- Changing publication dates without changing content.
- Meta descriptions as a ranking lever (they affect clicks, not rank).
- Social shares as a direct ranking signal.
- "Google penalizes multiple `<h1>` elements" (it does not; one clear `h1`
  is still good practice for readers).

## When the owner asks for a risky tactic

1. Decline in one line, naming the policy it breaks and the realistic risk
   (ignored links, demoted pages, a manual action).
2. Name the genuine alternative that serves the same goal.
3. Record the request and the decision in `history.md`, so it is not
   re-litigated every session.

Never present a risky tactic as an option with a warning attached. The
approval table's "Never" column does not move.
