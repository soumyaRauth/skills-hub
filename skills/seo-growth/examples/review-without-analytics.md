# Example: a monthly review with no Search Console

The portfolio, two months after the first run. Search Console is still not
connected. The owner asks how things are going.

## Contents

- The request
- What can and cannot be known
- The review
- When an export arrives

## The request

```
/seo-growth review
```

## What can and cannot be known

| Question | Source | Answer |
| --- | --- | --- |
| What changed on the site? | `history.md`, `git log`, crawl | `VERIFIED` |
| Is the site technically healthy? | `seo_audit.py crawl` | `VERIFIED` |
| Are the pages indexed? | Search Console only | `UNKNOWN` |
| Which queries bring impressions or clicks? | Search Console only | `UNKNOWN` |
| Does the name search look different? | Repeated snapshots, same tool and query set | Directional only |
| Did EXP-001 work? | Needs impressions and CTR | `INCONCLUSIVE` |

The review says this table's content in plain words before any detail, so
nothing that follows reads as more certain than it is.

## The review

Written to `reviews/2026-12-23.md`:

```
SEO review · noorhaldar.example · 2026-12-23 · monthly
Period: 2026-11-24 to 2026-12-23 · Previous review: none (first review)
Data: crawl 2026-12-23; name and topic snapshots 2026-10-20, 2026-11-25, 2026-12-23
      (web search tool, location unknown). Missing: Search Console, analytics.

Work completed
  SEO-003 about page indexable (approved 2026-11-27, deployed by you 2026-11-28)
  SEO-005 canonical fixed · SEO-009 talks linked · SEO-010 sitemap corrected
  SEO-011 Person structured data · SEO-013 sensors article published 2026-12-10

Search performance
  Impressions, clicks, CTR, positions: UNKNOWN (no Search Console)
  Snapshots for "noor haldar data engineer":
    2026-10-20 site absent · 2026-11-25 homepage at 6 · 2026-12-23 homepage 3, about page 7
  Read this as direction, not measurement: one tool, unknown location, three dates.

Experiments
  EXP-001 homepage title and h1: INCONCLUSIVE. The snapshots move the expected way, but
  no impressions or CTR data exist, and SEO-003 and SEO-005 changed the same queries'
  competition between pages. Re-evaluate with Search Console data.

Technical status: crawl clean; no broken links, no sitemap conflicts, no duplicate titles.

Interpretation (INFERRED): the site now presents one consistent identity, and owned
results for name + profession are rising in snapshots. Nothing here shows traffic.

Priority changes: SEO-012 (Search Console) moves to the top. Every remaining question
needs it, so it now outranks new content.

Next actions
  1. You: verify a Domain property in Search Console (SEO-012; steps in profile.md)
  2. Me: brief for "idempotent Airflow tasks" (roadmap item 2)
```

## When an export arrives

The owner later drops a Performance export into
`data/gsc-2026-12-01-2026-12-28/`. The next review runs:

```
python3 <skill dir>/scripts/gsc_report.py data/gsc-2026-12-01-2026-12-28/ \
    --brand "noor haldar,noorhaldar" --min-impressions 10
```

and reports totals from `Dates.csv`, brand against non-brand, and positions
8–20, each with the property and exact dates. The snapshot series stays in
the records but stops being the main KPI. EXP-001 gets a real baseline only
from this date on, and the record says so rather than back-filling one.
