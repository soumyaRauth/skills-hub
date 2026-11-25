# Example: what should I write?

The portfolio owner, with records in place and the technical issues resolved.
Still no Search Console; a web search tool is available.

## Contents

- The request
- Sources used
- Scoring
- The roadmap
- The first brief
- What it does not do

## The request

```
Which articles should I write next to get more people to my site?
```

## Sources used

- The owner's expertise and existing writing: the retries article, the
  pipeline-lint rules, the meetup talk.
- Snapshots of autocomplete, "People also ask" and the first ten results for
  candidate queries, taken 2026-11-25 with the web search tool.
- Questions in public Airflow community channels and the pipeline-lint issue
  tracker, quoted in `keywords.md` as evidence of phrasing.
- No search volumes: no keyword tool, no Search Console. Demand is scored
  from evidence anchors, never converted to numbers.

## Scoring

Opportunity = 2 × Fit + 2 × Value + Winnability + Demand.

| Keyword group | Fit | Value | Win | Demand (evidence) | Total | Note |
| --- | --- | --- | --- | --- | --- | --- |
| airflow sensor reschedule vs poke | 5 | 4 | 4 | 3 (autocomplete; recurring community question) | 29 | Owner has the incident; the results are docs and forum threads |
| airflow task stuck in queued | 4 | 4 | 3 | 3 (People also ask; many threads) | 25 | Troubleshooting intent; the owner has fixed it twice |
| airflow idempotent tasks | 5 | 4 | 4 | 2 (phrased differently in threads) | 28 | Builds on retries; a natural pillar section |
| airflow vs dagster | 3 | 2 | 1 | 3 (autocomplete) | 16 | Results are vendor pages and large publications. Low value for consulting |
| what is apache airflow | 2 | — | — | — | dropped | Fit gate: the intent is beginners, not the owner's clients |

## The roadmap

Cluster **Airflow reliability**, at the owner's stated pace of one article a
month:

1. *Sensors that don't starve your workers* (reschedule vs poke): SEO-013,
   brief ready.
2. *Idempotent Airflow tasks: making retries safe*: links to and from the
   retries article.
3. *Why Airflow tasks get stuck in queued, and how I fixed it twice*.
4. Pillar, once three supporting pieces exist: *Airflow reliability: a field
   guide*, linking all of them and pipeline-lint.

Each is a `roadmap.md` row with its keyword group, intent, format, unique
angle, score and task ID.

## The first brief

```
Audience     Engineers running Airflow in production; know DAGs and operators
Intent       know + do: why sensors exhaust worker slots and what to change (INFERRED,
             2026-11-25 snapshot: docs page and three forum threads)
What ranks   The official docs (accurate, no failure story); forum answers (partial)
Unique value The owner's incident: a sensor holding slots for hours (mentioned in the
             retries article), the reschedule-mode fix, and the pipeline-lint rule PL002
Outline      The symptom · poke vs reschedule · timeouts and retries multiplying ·
             deferrable operators · what I check now
Owner facts  [[OWNER: how many slots, for how long, and what alerted you?]]
             [[OWNER: Airflow version at the time]]
Verify       Current docs for reschedule mode and deferrable operators, against the
             Airflow version the article targets
Links        From: the retries article §3, the pipeline-lint page. To: both, and PL002
```

## What it does not do

- Write the article around invented incident details. The placeholders stay
  until the owner fills them.
- Promise traffic or rankings for any keyword.
- Plan more than the owner said they can sustain.
- Publish. A finished draft goes to the owner, and `history.md` records it
  as awaiting approval.
