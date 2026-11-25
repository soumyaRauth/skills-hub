# The master strategy

`strategy.md` is the answer to "why are we doing this task and not another?"
It is short enough to reread every session, and it changes only for a
reason that gets written down.

## Contents

- What it contains
- Writing it the first time
- KPIs that mean something
- Revising it
- Strategy smells

## What it contains

Use `templates/strategy.md`. Every section is a few lines, not an essay.

| Section | Answers |
| --- | --- |
| Long-term objectives | What search visibility is for: clients, a job, readers, sign-ups, reputation |
| Target search categories | Brand and name, expertise topics, projects and products, problem-solving queries, local if relevant |
| Brand search strategy | Which owned pages and profiles should appear for the name, and in what role |
| Keyword strategy | Which clusters first, and why those (`references/keyword-research.md`) |
| Content strategy | Pillars, cadence the owner can sustain, what makes the content original (`references/content-strategy.md`) |
| Technical priorities | What must be true for the rest to work (`references/technical-seo.md`) |
| Authority strategy | Which genuine contributions build reputation in this field (`references/authority-building.md`) |
| Competitive positioning | Where the site can be better, more original or more focused than what ranks |
| Geography and language | Markets, languages, whether international SEO applies |
| Audiences | Who searches, what they already know, what they need |
| KPIs | What will be measured, from which source, at what cadence |
| Assumptions | What the strategy rests on that has not been verified |
| Revision log | Dated changes and their reasons |

## Writing it the first time

Write it after discovery, from evidence:

1. Start from the owner's objective. A portfolio whose goal is consulting
   clients and a portfolio whose goal is a job have different keyword
   strategies.
2. Brand and name come first for a personal site. They are the most
   winnable queries and the ones a prospective client or employer will type.
3. Choose two or three topic areas to build authority in, where the owner has
   real experience or work to show. Fewer, deeper clusters beat many thin
   ones.
4. Name the technical preconditions (indexable, crawlable, canonical) before
   any content plan, because content on a page that cannot be indexed is
   invisible.
5. Pick an authority approach that fits the owner's actual work: open
   source, writing, talks, teaching, research, collaboration.
6. Write the assumptions down. They become research tasks or questions.

## KPIs that mean something

Define each as metric · source · cadence · what "better" means.

| KPI | Source | Notes |
| --- | --- | --- |
| Brand and name query impressions and clicks | Search Console, query filter | The core personal-brand KPI |
| Non-brand impressions and clicks | Search Console | Growth in topics; slower |
| Pages with impressions | Search Console, pages report | A proxy for how much of the site is visible |
| Indexed pages versus pages meant to be indexed | Search Console page indexing report | Technical health |
| Queries in positions 1–10 and 11–20 | Search Console | Watch the movement, not one day |
| Organic landing sessions and conversions | Analytics | Only if conversions are defined |
| Owned results on the first page for the name | Dated snapshots, taken the same way each time | Directional only |
| Genuine mentions and links earned | Search Console Links report, `authority.md` | Count real ones, not totals from a vendor |

Without Search Console, KPIs fall back to snapshots and the site's own
state, and the strategy says so. Never adopt a vanity metric (a vendor
authority score, total page count, word count) as a KPI.

## Revising it

Revise when evidence says so: an experiment's result, a new data source, a
change in the owner's goals, a competitor shift, a major site change, or a
failing assumption. Each revision adds a line:

```
2026-12-20  Moved "Airflow" ahead of "dbt" as the first cluster: Search Console
            shows 14 Airflow queries with impressions and none for dbt (VERIFIED,
            export 2026-11-21 to 2026-12-18). Was: equal priority (ASSUMED).
```

Never rewrite history. The superseded text stays in the revision log.

## Strategy smells

- Every topic in the field is a target. Pick.
- The plan depends on ranking for a head term held by major publishers.
- Content volume is the plan. Usefulness and originality are the plan.
- No technical precondition is mentioned on a site with indexing problems.
- The name strategy relies on pages the owner does not control.
- KPIs cannot be measured with the data the owner has.
