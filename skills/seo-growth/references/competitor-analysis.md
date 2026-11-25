# Competitor analysis

Competitor research earns its place only when it produces tasks. The question
is always: where can this site be more useful, more original or more focused
than what currently wins these searches?

## Contents

- Kinds of competitor
- Finding them
- What to look at
- Profiles
- From gaps to tasks
- Limits

## Kinds of competitor

| Kind | Who | Why it matters |
| --- | --- | --- |
| Direct | Offers the same thing to the same people | Positioning and differentiation |
| Search | Ranks for the site's target queries, whatever they offer | The real SEO competition; often a publisher or a forum, not a rival |
| Content | Covers the same topics for the same audience | Topic gaps and formats |
| Personal brand | Other people in the field with strong name visibility | What a well-built personal presence looks like here |
| Topic authority | The sites search engines treat as authorities on a topic | What the bar for depth and evidence is |
| Per keyword | Whoever holds page one for one specific query | Intent and format for that page |

A namesake who outranks the owner for their name is not a competitor. They
are an ambiguity to work around (`references/personal-brand.md`).

## Finding them

- Take snapshots for the site's top keyword groups and the owner's
  profession and topics. Note which domains recur.
- Ask the owner whom they consider peers or rivals; check whether those
  actually appear in search.
- Search Console does not name competitors. A third-party tool the owner
  has may estimate overlap; label it `ESTIMATED`.

Keep the set small: three to six profiles. More is research for its own sake.

## What to look at

For each competitor, on public pages only:

- Positioning: who they serve and how they describe themselves.
- Topic coverage and architecture: their sections, pillars and how deep each
  goes.
- The pages that rank for shared targets: title, headings, format, depth,
  freshness, evidence, examples, media.
- Intent alignment: why that page satisfies the query.
- Internal linking around those pages.
- Unique assets: tools, datasets, original research, templates, courses,
  open-source projects.
- Where they earn mentions and links, as far as public evidence shows
  (`references/authority-building.md`).
- Visible technical problems, only as context, never to exploit.
- Gaps: questions their pages leave unanswered, outdated content, missing
  examples, no first-hand experience.

## Profiles

Use `templates/competitors.md`. Each profile is short:

```markdown
## example-rival.com · search competitor (Airflow topics)
- Snapshot dates: 2026-11-25 (web search tool, location unknown)
- Positioning: tutorials for Airflow beginners, ad-supported
- Ranks for (in snapshots): "airflow retries", "airflow sensors"
- Strengths: step-by-step tutorials, code samples, updated 2026
- Gaps: no production troubleshooting; no real failure cases; nothing on
  retries with idempotent tasks
- Opportunity: SEO-012 a troubleshooting guide built from the owner's
  production incidents (first-hand experience they lack)
- Metrics: none sourced (no tool); do not estimate
```

## From gaps to tasks

Every profile ends in zero or more tasks in `backlog.md`, each saying what
this site will do better and why it is credible for the owner to do it.
Prefer opportunities that use what the owner uniquely has: real projects,
incidents, data, code, opinions grounded in experience.

Never: copy structure or text, rewrite a competitor's article, or produce a
"better" version that adds length without adding knowledge.

## Limits

- Traffic, authority and link figures for competitors are `UNKNOWN` unless a
  named tool supplied them.
- A competitor's success with a tactic is not evidence the tactic is
  compliant or that it caused their ranking.
- Revisit competitors at reviews only when rankings or strategy changed, not
  every session.
