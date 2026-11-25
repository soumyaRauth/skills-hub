# SEO records

SEO is slow. A change made today is judged weeks from now, by a session that
remembers nothing. The records are that memory. They are plain Markdown so
the owner can read them, edit them, and keep them in git.

## Contents

- Where records live
- The site key
- Files
- Tasks
- History
- Baselines
- Persistence rules
- Several sites
- Privacy and git
- The status view

## Where records live

Resolve the folder in this order, and say which one was used in the first
report:

1. **The owner named a location.** Use it.
2. **Records already exist.** `.seo-growth/` in the current directory or the
   repository root, or `~/.seo-growth/<site key>/`. Check both before creating
   anything.
3. **This repository is the site's source.** Evidence: a `CNAME` file, a site
   URL in the framework config (`site`, `baseURL`, `url`, `siteUrl`,
   `metadataBase`, `homepage`), the domain in deployment config, or the owner
   saying so. Use `<repository root>/.seo-growth/`.
4. **The site's source is elsewhere on this machine.** A repository whose
   `CNAME`, framework config or deployment config names the domain. Use that
   repository's `.seo-growth/`, do the code work there, and say so.
5. **Otherwise** (a URL with no source on this machine, or an unrelated
   repository), use `~/.seo-growth/`. Never create records inside a
   repository that is not the site's source.

## The site key

One folder per site: `.seo-growth/<site key>/`.

- The key is the canonical host the site actually serves after redirects,
  lowercased, without scheme, port or a leading `www.`: `example.com`.
- Subdomains are separate sites (`blog.example.com`) unless the owner says
  they are one property.
- A site under a path joins host and path with `-`:
  `username.github.io-project`.
- A person with no website yet: a short slug of the name, `person-jane-doe`,
  renamed to the domain once one exists (record the rename in `history.md`).
- `profile.md` records the exact canonical origin (`https://www.example.com`)
  and every variant seen (http, www, apex) with how each one responds.

## Files

Create a file from `templates/` the first time it is needed, not before.
`profile.md`, `strategy.md`, `backlog.md`, `history.md` and the first baseline
are created on the first run; the rest appear when their work starts.

| File | Holds | Template |
| --- | --- | --- |
| `profile.md` | Site identity, owner, audiences, markets, languages, positioning, objectives, source repository and framework, data access, standing authorizations | `templates/profile.md` |
| `strategy.md` | The master strategy and its dated revision log | `templates/strategy.md` |
| `backlog.md` | The `Now` list and every task | `templates/backlog.md` |
| `history.md` | Activity history and changelog, newest first | `templates/history.md` |
| `baselines/YYYY-MM-DD.md` | A full snapshot of the site's SEO state on that date | `templates/baseline.md` |
| `content.md` | The content inventory, one row per relevant page | `templates/content.md` |
| `keywords.md` | Researched keywords, scores and the keyword-to-page map | `templates/keywords.md` |
| `roadmap.md` | Topic clusters and the content roadmap | `templates/roadmap.md` |
| `competitors.md` | Competitor profiles and the gaps they reveal | `templates/competitors.md` |
| `brand.md` | Name-search snapshots, owned properties, the identity consistency matrix | `templates/brand.md` |
| `authority.md` | Authority and link opportunities, outreach drafts and their status | `templates/authority.md` |
| `experiments.md` | Every measured change: hypothesis, baseline, evaluation, decision | `templates/experiments.md` |
| `reviews/YYYY-MM-DD.md` | Periodic and monthly reviews | `templates/review.md` |
| `drafts/` | Content drafts awaiting approval, when the site has no drafts convention of its own | — |
| `data/` | Raw evidence: exports, audit output, search snapshots, each with a date in its filename | — |

## Tasks

IDs are per site and never reused: `SEO-001`, `SEO-002`, … Experiments are
`EXP-001`, … Authority opportunities are `AUTH-001`, … Baseline findings
are referenced as `B-<date>-<n>` so a task can say where it came from.

Every task in `backlog.md` is a block with these fields, in this order:

```markdown
### SEO-007 · Add Person structured data to the about page
- Status: Ready
- Category: Brand · Structured data
- Target: /about/
- Keyword or intent: "jane doe" · navigational, brand
- Why: About page names the owner but carries no Person markup (VERIFIED,
  seo_audit.py page /about/, 2026-11-25). Supports entity understanding for
  name searches (SUPPORTED: Google structured data docs).
- Score: Impact 3 · Confidence 3 · Relevance 5 · Effort 1 → 45
- Risk: Low · Approval: not needed
- Depends on: SEO-003
- Measure: markup parses and matches visible text; Search Console
  enhancement report shows no errors; impressions for brand queries on /about/
- Created: 2026-11-25 · Completed: —
- Log: 2026-11-25 created from B-2026-11-25-4
```

**Statuses**

| Status | Means |
| --- | --- |
| `Backlog` | Worth doing, not yet ready or not yet ranked high enough |
| `Researching` | Needs evidence before it can be scored with confidence |
| `Ready` | Scored, unblocked, can be done now |
| `In Progress` | Started this session; never left here at the end of a session without a log line saying what remains |
| `Awaiting Approval` | Needs the owner's yes; the request is in `history.md` and the session report |
| `Completed` | Done and validated, with the date and where the change lives (commit, file, URL) |
| `Monitoring` | Done, and an experiment is measuring it; links `EXP-…` |
| `Blocked` | Cannot proceed; says on what (access, a decision, another task) |
| `Rejected` | The owner declined, or evidence showed it was not worth doing; the reason stays |

A rejected task is not proposed again unless circumstances change, and then
the new proposal says what changed.

**The `Now` list** at the top of `backlog.md` holds at most five task IDs in
the order they should be done, each with one line. Re-rank it every session.

## History

`history.md` is append-only, newest entry first. One entry per session:

```markdown
## 2026-11-25 · improve
- Done: SEO-002 titles on 4 pages, SEO-004 broken link on /blog/ (uncommitted, working tree)
- Validated: seo_audit.py page on the 4 pages before and after; site builds
- Proposed: SEO-003 remove noindex from /about/ → Awaiting Approval
- Approvals: SEO-001 approved by the owner ("yes, go ahead")
- Found: /talks/ is in the sitemap but nothing links to it (VERIFIED, crawl)
- Data: crawl 2026-11-25 (data/crawl-2026-11-25.json); no Search Console access
- Next: SEO-003 once approved, otherwise SEO-005
```

Record approvals and rejections with the owner's words, briefly quoted, and
the date. Record what was proposed but not done. Never write an entry for
work that did not happen.

## Baselines

A baseline is a snapshot, not a living document. Never edit an old one
except to fix a factual error, marked as such.

Write a new baseline on the first run, when the owner asks, after a major
site change (redesign, migration, domain change), or when a review needs a
fresh reference point and the last baseline no longer describes the site.
Each new one says what changed since the previous.

## Persistence rules

- Read before writing: load the existing records at the start of every
  session, and build on them.
- Update after meaningful work, in the same session. A session that changed
  the site and did not update the records left the next session blind.
- One file per purpose. Before creating a file, check that the content does
  not already have a home in the table above.
- Dates are absolute (`2026-11-25`), never "last week".
- Every number keeps its label and source (`references/research-methods.md`).
- When a record turns out to be wrong, correct it and say so in `history.md`.
- Never delete history. Superseded strategy goes into the revision log.

## Several sites

- One folder per site key, each self-contained. Never copy a metric, keyword
  score or finding from one site's records into another's.
- When records for several sites exist and the request does not say which:
  the site whose source is the current directory; failing that, the site
  with the most recent `history.md` entry. Name it in the report's first
  line and offer to switch. Ask only when the request could mean either and
  the choice changes the work.
- A person's other properties (a portfolio and a project site) may be listed
  in `brand.md` as owned properties. Their data stays in their own folders.

## Privacy and git

- Never store credentials, API keys, OAuth tokens or cookies in records. Note
  only that access exists and how it is obtained.
- Name searches show other people. Record them as "a different person (a
  musician)" with the result position, never their personal details.
- `.seo-growth/` holds strategy, competitor notes and, in `data/`, Search
  Console exports. On the first run in a repository, say once that committing
  the records keeps history across machines, and that in a public repository
  they would be public too. The owner decides; never edit `.gitignore` or
  commit without their say.

## The status view

`status` reads the records and runs nothing new. It shows:

```
SEO status · example.com · records: .seo-growth/example.com/

Last session   2026-11-25 · improve · 2 tasks completed
Now            1. SEO-003 Remove noindex from /about/      Awaiting Approval
               2. SEO-005 Add internal links to /talks/    Ready
               3. SEO-008 Write the Airflow retries guide  Ready
Due            EXP-001 homepage title: evaluate on or after 2026-12-23
Data access    Search Console: not connected · Analytics: none · Web search: yes
Open           12 tasks: 4 Ready · 1 Awaiting Approval · 2 Monitoring · 5 Backlog
Next action    Approve SEO-003, or say no and I will continue with SEO-005
```
