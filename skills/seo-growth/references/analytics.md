# Search Console and analytics

Search Console is the only first-party view of how a site appears in Google:
which queries showed it, how often, at what position, and how often people
clicked. When it is available it outranks every other source. When it is not,
the work continues, and the first task is usually to connect it.

## Contents

- Getting access
- What the data is, and is not
- Analysis recipes
- Using gsc_report.py
- Analytics
- Working without Search Console
- Reporting periods

## Getting access

In order of preference, and only what the owner sets up:

1. **A Search Console integration in this environment** (an MCP server or
   tool). Use it read-only.
2. **Exports**: in Search Console, Performance → set the date range → Export
   → CSV (a zip with `Queries.csv`, `Pages.csv`, `Countries.csv`,
   `Devices.csv`, `Dates.csv` and more). The owner drops it in
   `.seo-growth/<site>/data/gsc-<start>-<end>/`.
3. **The API** with credentials the owner creates and stores outside the
   records. Never write credentials into `.seo-growth/`.

If the site is not verified yet: a Domain property (verified by a DNS
record) covers every protocol and subdomain variant; a URL-prefix property
can be verified with an HTML file or meta tag. Adding the owner's
verification tag or file to the site is a safe code change once the owner
provides the token. DNS changes are the owner's.

Bing Webmaster Tools can import a verified Search Console site, and adds a
second engine's view at no cost.

Never claim to have read Search Console or Analytics when no access exists.

## What the data is, and is not

- Clicks, impressions, CTR and average position, by query, page, country,
  device, search appearance and date, for about the last 16 months.
- Queries the privacy filter hides are omitted from query tables, so query
  totals fall short of the chart totals. Use `Dates.csv` or the chart for
  totals.
- The most recent days are preliminary and can change.
- Average position is an average over impressions, and noisy when
  impressions are few. Trends over weeks matter, single days do not.
- The interface exports a capped number of rows per table; the API returns
  more.
- It shows Google only. It does not show competitors, search volume, or
  queries the site never appeared for.

## Analysis recipes

| Question | How | Leads to |
| --- | --- | --- |
| Which pages get seen but not clicked? | High impressions, CTR low compared with this site's own pages at similar positions | Title and description work, intent check |
| What is almost on page one? | Queries and pages averaging roughly positions 8–20 with steady impressions | On-page improvements, internal links, content depth |
| What is growing or declining? | The same-length periods compared, by page and query | Investigate declines: indexing, content age, competitors, results-page changes |
| How does the name perform? | Filter brand and name queries; compare periods | Personal brand KPI |
| What unexpected queries appear? | Queries the keyword map does not cover | New content, or a page whose intent is unclear |
| Which pages never appear? | Pages in `content.md` with no impressions | Indexing check, intent check, internal links |
| Country and device | Splits for the main pages | Geographic strategy, mobile issues |

Always state the property, the date range, and the comparison period. A
change in a metric is an observation; its cause is a hypothesis until
`references/experimentation.md` says otherwise. Check Google's Search Status
Dashboard for ranking updates in the period, and seasonality in last year's
data, before attributing anything.

## Using gsc_report.py

```bash
python3 <skill dir>/scripts/gsc_report.py data/gsc-2026-10-28-2026-11-24/ \
    --brand "jane doe,janedoe" --min-impressions 20
python3 <skill dir>/scripts/gsc_report.py data/gsc-2026-10-28-2026-11-24/ \
    --compare data/gsc-2026-09-30-2026-10-27/ --brand "jane doe"
```

It reports totals (with the omitted-query caveat), the brand and non-brand
split, positions 8–20, low CTR for position measured against the site's own
CTR at similar positions (not an industry curve), and with `--compare` the
largest gains and losses and new and lost queries. Save its output in
`data/` and cite it.

## Analytics

With Google Analytics or another analytics tool:

- Organic search sessions (in GA4, the Organic Search default channel
  group), by landing page.
- Engagement on organic landing pages: do visitors stay, read, go further?
- Key events or conversions from organic visits, if the owner has defined
  them. If none exist, propose what to measure (a contact form submission, a
  sign-up), and hand consent and privacy obligations for any new tracking to
  `standards-compass`.
- Compare organic trends with Search Console clicks; they will not match
  exactly, and that is expected.

## Working without Search Console

The skill stays useful:

1. Say plainly what cannot be known: indexing status, real queries,
   impressions, clicks, positions over time.
2. Add a task to connect Search Console and, where the code is here, prepare
   the verification change.
3. Track manually in the meantime, each entry dated and recorded the same way
   every time:
   - name and top keyword snapshots (`references/research-methods.md`)
   - crawl health from `seo_audit.py crawl`
   - the content inventory and what was published when
   - authority opportunities and earned mentions, verified by fetching them
4. Treat these as directional. A snapshot moving from position 7 to 4 for
   one query on one day is not a trend.

## Reporting periods

- Compare equal-length periods ending on the same weekday, or the same
  period a year earlier when seasonality matters.
- Monthly reports use the previous full calendar month or the last 28 days,
  stated explicitly.
- Keep the raw exports for each reported period in `data/`.
