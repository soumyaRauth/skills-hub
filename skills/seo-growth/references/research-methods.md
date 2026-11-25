# Research methods and evidence

Every recommendation rests on evidence, and the evidence has to be honest
about what it is. A guessed search volume in a confident table is worse than
no number: it gets acted on.

## Contents

- Evidence labels
- Never fabricate
- Discovering tools
- Sources, strongest first
- Search-result observations
- Fetching and crawling politely
- Recording research

## Evidence labels

| Label | Means | Example |
| --- | --- | --- |
| `VERIFIED` | Observed this session, or in data the owner supplied, with the source and date | "`/about/` returns `noindex` (VERIFIED, fetched 2026-11-25)" |
| `ESTIMATED` | A third-party tool's figure, with the tool's name and date | "~300 searches a month (ESTIMATED, the owner's keyword tool, 2026-11-25)" |
| `INFERRED` | Reasoned from evidence you name | "Page one is all tutorials, so a tutorial matches the intent (INFERRED from the 2026-11-25 snapshot)" |
| `HYPOTHESIS` | Plausible, untested; usually becomes an experiment | "A clearer title may raise CTR on brand queries" |
| `UNKNOWN` | Not available; say what would make it known | "Indexing status: UNKNOWN without Search Console" |
| `ASSUMED` | A stated working assumption about the owner or site, to be confirmed | "Target market: Bangladesh and remote global roles (ASSUMED)" |

Search Console data the owner exported is `VERIFIED` for that property and
period, with Google's own caveats (rounded, privacy-filtered queries
omitted).

## Never fabricate

Search volume · keyword difficulty · rankings or positions · backlinks or
referring domains · impressions, clicks or CTR · traffic · competitor
metrics · what a search result page shows · search intent stated as fact ·
whether Google has indexed a page · a page's crawl date · Core Web Vitals.

Without a source, write `UNKNOWN` and, when it matters, how to get it. A
`site:` search is a rough sample, never an index count. Third-party
"authority" scores are a vendor's model, not a Google metric, and are
labelled with the vendor's name.

## Discovering tools

At the start of research, list what this environment can actually do, and
use the best available:

| Need | Check for | Fallback |
| --- | --- | --- |
| Search results | A web search tool, a browser tool | Ask the owner to run named queries in a private window and paste or screenshot the first page |
| Page content | A page fetcher, `scripts/seo_audit.py`, `curl` | The owner's source code |
| Google's own data | A Search Console MCP server or API access; an export from the owner | Public observations, labelled |
| Demand | Search Console queries; a keyword tool the owner has; Google Keyword Planner or Bing Webmaster Tools through the owner's account; Google Trends for relative interest | Qualitative demand evidence (`references/keyword-research.md`) |
| Links | Search Console Links report; a backlink tool the owner has | Mentions found by search, labelled as a sample |
| Performance | PageSpeed Insights (field data from CrUX when available, lab data otherwise), Lighthouse locally | Source inspection for obvious causes |

Never install a tool, create an account or start a paid service without the
owner's approval. Never suggest a subscription when a free source answers
the question.

## Sources, strongest first

1. The owner's Search Console and analytics data for this site.
2. The site itself: live responses, source code, sitemap, robots.txt.
3. Official documentation: Google Search Central, Search Console Help,
   schema.org, framework docs (`references/search-guidelines.md`).
4. Observed search results, as dated snapshots.
5. Third-party tool estimates, labelled `ESTIMATED`.
6. Communities and competitor pages, for language, questions and gaps.
7. SEO blogs and social posts: leads to verify, never authorities.

## Search-result observations

A results page differs by location, language, device, signed-in state,
history and time. A web search tool may not even be Google. So:

- Record each observation as a snapshot: query, date, the engine or tool,
  location and device if known, and the top results as URL and kind
  (owner's site, profile, news, a different person, directory).
- Say "in this snapshot", never "Google ranks".
- Compare snapshots taken the same way. A change between a web-search-tool
  snapshot and an owner's phone screenshot is not a ranking change.
- Do not query Google in bulk by automation. Use the available search tool,
  a few manual checks, or the owner's own searches. Search Console is the
  right source for how the site appears in Google over time.
- Store snapshots in `data/serp-<date>.md` and summarize them in the record
  that uses them (`brand.md`, `keywords.md`, `competitors.md`).

## Fetching and crawling politely

- Identify honestly; never spoof a search engine's user agent.
- Respect `robots.txt` for crawling, keep a delay between requests, and cap
  the page count. `seo_audit.py crawl` does all three by default.
- Crawl only the owner's site. For competitors, fetch the specific pages
  being compared.
- A page that renders its content with JavaScript may look empty to a plain
  fetch. Before reporting "no content", check with a browser tool or the
  source, and say which was used.

## Recording research

- Raw outputs go in `data/` with a date in the filename.
- Conclusions go in the record that uses them, with labels and a pointer to
  the raw file.
- Research that changed nothing still gets one line in `history.md`, so the
  next session does not repeat it.
