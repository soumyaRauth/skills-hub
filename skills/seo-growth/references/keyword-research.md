# Keyword research

The goal is not a long list. It is a short, mapped set of queries the site
can genuinely satisfy, ranked by what they are worth to the owner and how
winnable they are.

## Contents

- Sources
- Categories
- Search intent
- The opportunity score
- Demand without a volume tool
- Mapping keywords to pages
- Cannibalization
- What it records

## Sources

Strongest first; label everything (`references/research-methods.md`).

1. **Search Console queries** for this site: what it already appears for, at
   what position. The best keyword source a site has.
2. **The site's own content and the owner's expertise**: what they can write
   about with authority.
3. **Search results**: autocomplete suggestions, related searches, "People
   also ask", and the titles of what ranks, as dated snapshots.
4. **Competitor pages**: the topics and subtopics they cover
   (`references/competitor-analysis.md`).
5. **Communities**: questions asked in forums, Q&A sites, issue trackers,
   discussion threads. The exact phrasing people use is evidence.
6. **Keyword tools the owner has**: Google Keyword Planner or Bing Webmaster
   Tools through the owner's account, or a paid tool they already use.
   Figures are `ESTIMATED`, ranges stay ranges, and the tool is named.
7. **Google Trends**: relative interest and seasonality, never volume.

## Categories

Tag each keyword with one primary category:

| Category | Example | Usually maps to |
| --- | --- | --- |
| Brand | the brand or product name | Homepage, product page |
| Personal identity | the owner's name and variants | Homepage, about page |
| Professional expertise | "airflow consultant" | Services or about page, pillar page |
| Educational | "how airflow retries work" | Article, tutorial |
| Informational | "what is a data lakehouse" | Article, glossary-style pillar |
| Commercial investigation | "airflow vs dagster" | Comparison article |
| Transactional | "hire data engineer remote" | Services page, contact |
| Navigational | "projectname docs" | The page itself |
| Product | "projectname install" | Product or docs page |
| Problem-solving | "airflow task stuck in queued" | Troubleshooting article |
| Local | "data engineer dhaka" | About or services page with location |

## Search intent

For every keyword that will be acted on, record:

- **Primary intent**: know, do, go, compare, buy.
- **Secondary intent**, if the results show a mix.
- **Expected content type**: what the current results are (tutorials, tool
  pages, lists, videos, profiles, documentation), from a snapshot. The
  results page is the best evidence of what searchers want.
- **Audience**: who types this, and what they already know.
- **Fit**: whether the site can satisfy that intent better than what ranks.

Intent comes from observed results and is labelled `INFERRED` with the
snapshot date. A keyword whose intent the site cannot serve is dropped,
however large its demand.

## The opportunity score

Score each candidate from 1 to 5 on four factors, with a one-line reason per
factor:

| Factor | 1 | 3 | 5 |
| --- | --- | --- | --- |
| **Fit**: relevance and intent match | Tangential, or intent the site cannot serve | Relevant, partial intent match | Core to the site, intent fully served by the planned page |
| **Value**: to the owner's objective | Traffic with no path to the goal | Builds topical authority | Directly drives the goal (clients, hiring, sign-ups) or protects the name |
| **Winnability**: given what ranks now | Page one is all major publishers or brands for broad intent | Mixed: some smaller or specialist sites rank | Pages like ours rank, or the site already appears in positions 8–30 |
| **Demand**: evidence people search it | No evidence | Direct evidence: autocomplete, "People also ask", recurring community questions | Measured: Search Console impressions, or an `ESTIMATED` volume high for this niche |

**Opportunity = 2 × Fit + 2 × Value + Winnability + Demand**, from 6 to 30.

- Fit and Value count double: a winnable, popular query that does not serve
  the owner's goal is not an opportunity.
- **Gate:** Fit of 1 or 2 drops the keyword, whatever the total.
- Personal identity and brand queries are always kept; they are scored for
  ordering only.
- Add a confidence (`HIGH`, `MEDIUM`, `LOW`) from the weakest evidence used.
- The score orders candidates. It is a judgment written as a number, not a
  measurement, and is never presented as one.

## Demand without a volume tool

Use the anchors in the Demand row, and say which evidence was used:

- 1: no autocomplete, no "People also ask", no community questions, no
  impressions.
- 2: indirect: related autocomplete, questions phrased differently.
- 3: the phrase appears in autocomplete or "People also ask", or recurs in
  community questions.
- 4: Search Console shows impressions for it, or a tool estimate exists.
- 5: among the highest measured or estimated demand in this site's set.

Never convert these into search volumes.

## Mapping keywords to pages

Group keywords that share intent into one target, and map each group to
exactly one page:

| Group | Primary keyword | Supporting variants | Intent | Target page | Status |
| --- | --- | --- | --- | --- | --- |
| Name | jane doe | jane doe engineer, j doe | go | / and /about/ (see note) | Exists |
| Airflow retries | airflow retries | airflow retry delay, retries vs retry_delay | know, do | /blog/airflow-retries/ | Exists, optimize |
| Airflow vs Dagster | airflow vs dagster | dagster or airflow | compare | — | New page |

Each mapping says whether the page exists, needs optimizing, or must be
created. A new page becomes a content task (`references/content-strategy.md`).

Name queries legitimately reach both the homepage and the about page. Decide
which one is the primary target and make the other support it with a clear
link, rather than two pages competing with identical titles.

## Cannibalization

Two pages target the same intent when a searcher would be equally satisfied
by either. Signs: Search Console shows both pages for the same query with
positions alternating; titles and headings are near-identical; the content
overlaps.

Resolve by differentiating the pages' intents, consolidating into one (a
redirect, which needs approval), or making one the clear primary with links
from the other. Do not create a new page for a group that already has one.

## What it records

`keywords.md`: candidate keywords with category, intent, the four factor
scores and reasons, the opportunity total, confidence, sources with dates,
and the map. Tasks generated from it link back by keyword group.
