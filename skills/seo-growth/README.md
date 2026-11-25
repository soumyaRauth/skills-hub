# SEO Growth Engine

**Sustainable search visibility for a website and the person behind it, measured honestly.**

SEO Growth Engine is an [Agent Skill](https://code.claude.com/docs/en/skills)
that runs a website's SEO as a long-term project. It discovers the site and
its owner, audits what actually stands between them and search results,
ranks the work, does the safe parts in the site's own code, validates them,
and writes everything down, so the next session starts where this one
stopped. It treats the owner's name as a first-class target: making a
person findable is often the most valuable search work a personal site has.

```bash
npx skills add soumyaRauth/skills-hub --skill seo-growth
```

Then, in Claude Code:

```
/seo-growth https://your-site.example
```

---

## The problem

```
"Do an SEO audit."        →  a 90-item checklist, nothing fixed
"Find me keywords."       →  invented search volumes in a confident table
"Make me rank for my name" → fake profiles and bought links, or a promise
```

SEO tools report; SEO advice generalizes; and both forget. A change made
today is judged a month from now, by someone who no longer remembers what
the baseline was. Meanwhile one leftover `noindex` on an about page outweighs
every keyword in the content plan.

## What it does

```
records → what changed → verify issues → rank the next action → do the safe work
   → ask for the rest → validate → write it down → one next step
```

- **Remembers.** Per-domain records in `.seo-growth/<domain>/`: profile,
  strategy, backlog, history, baselines, content inventory, keywords,
  competitors, personal brand, authority opportunities, experiments, reviews.
- **Decides.** A transparent priority score, overrides for critical issues,
  and a `Now` list of at most five tasks.
- **Does the work.** Titles, descriptions, headings, internal links,
  structured data and safe technical fixes, in the site's framework and
  conventions, validated with a build and a before-and-after audit.
- **Works on the name.** Name-search snapshots, namesakes, identity
  consistency across profiles, a canonical bio from verified facts, brand
  pages, Person structured data.
- **Measures honestly.** Search Console when available, with a bundled
  analyzer; dated snapshots and manual tracking when not; experiments with
  baselines and evaluation windows.

## Honest by construction

| It does | It never does |
| --- | --- |
| Labels every claim `VERIFIED`, `ESTIMATED`, `INFERRED`, `HYPOTHESIS`, `UNKNOWN` or `ASSUMED` | Invent search volume, rankings, traffic, backlinks or indexing status |
| Records search results as dated snapshots with the tool used | Present one snapshot as "Google ranks you at 4" |
| Says what it expects a change to influence and how it will be measured | Promise rankings |
| Evaluates experiments against a baseline, after recrawl, with a control | Claim a change caused a movement it cannot attribute |
| Drafts content from the owner's facts, with placeholders for the rest | Fabricate experience, credentials, statistics or quotes |
| Researches and drafts outreach | Send email, create accounts, publish, or pay for anything without approval |
| Follows Google Search Essentials and the spam policies | Buy links, cloak, stuff keywords, or build doorway pages, even when asked |

## Approval boundaries

| Without asking | Asks first | Never |
| --- | --- | --- |
| Research, audits, drafts; titles, descriptions, headings, alt text; internal links; structured data matching the page; performance fixes with no visible change | Publishing or deploying; deleting, merging or redirecting pages; URL changes; robots, `noindex`, canonical and sitemap changes; host or architecture changes; new dependencies; the owner's bio; outreach; anything paid; commits unless the owner's workflow says so | Link schemes, fake reviews or profiles, cloaking, hidden text, doorway pages, scaled unreviewed content, spam, acting against others |

The owner can widen the first column with a dated, written policy in
`profile.md`, and the skill does exactly that much more.

## Commands

| Command | Does |
| --- | --- |
| `/seo-growth <url>` | First run, or the next best action from the records |
| `audit` | A verified, prioritized audit; changes nothing |
| `improve` | Executes the highest-value safe tasks and validates them |
| `plan` | Creates or revises the strategy and backlog |
| `keywords` | Researches, scores and maps keywords |
| `competitors` | Profiles real search competitors and turns gaps into tasks |
| `personal-brand` | Name searches, identity consistency, brand pages |
| `technical` | Verifies and fixes technical issues; asks for risky ones |
| `content` | Clusters, roadmap, briefs, drafts, updates |
| `page <url or path>` | Optimizes one page |
| `backlinks` | Genuine authority opportunities and outreach drafts |
| `analytics` | Search Console and analytics analysis, or a plan to get the data |
| `review` | Compares periods, evaluates experiments, adjusts strategy |
| `status` | Reads the records: state, open tasks, due checks, next action |
| `experiment` | Creates, monitors or evaluates an experiment |

Plain words work too: *"my name doesn't show up on Google"*, *"what should
I write next?"*, *"how is search doing?"*.

## When it activates

| | |
| --- | --- |
| **Engages** | Search visibility questions: audits, technical SEO, keywords, competitors, optimizing a page for search, content to attract search traffic, internal links, backlinks, Search Console, making a name findable, `/seo-growth`, and resuming a site with `.seo-growth/` records |
| **Stays quiet** | A typo, copy or styling edit nobody framed as search work, even on a page with SEO problems; paid ads; social media growth; unrelated work in a repository that keeps records |
| **Depth** | `ACTIVE` when asked · `CONSULT` (two or three lines) when a change would move or remove URLs, noindex pages, change the domain, or switch to client-only rendering · never `GATING` |
| **Works with** | `human-empathy`, `practical-localizer`, `standards-compass`, `impact-map`, `proof-driven-dev`, `dependency-guard`, `release-engineer` |

## Example

```
You:   /seo-growth https://noorhaldar.example

Agent: ⚡ SEO Growth Engine — first run for noorhaldar.example

       Biggest problem: your about page tells search engines not to index it.

       Done (validated, not committed)
         SEO-002  Homepage title, description and h1 now name you and your role
         SEO-007  pipeline-lint structured data parses again
         SEO-004  Removed a link to an article that does not exist yet

       Needs your approval
         SEO-003  Remove noindex from about.html           recommended: yes
         SEO-005  Fix the retries article's canonical       recommended: yes

       Name search (snapshot, web search tool): other people with your name fill the
       first results; your site does not appear.
       Missing data: Search Console. Next: approve SEO-003 and SEO-005.
```

Worked examples: [first run](examples/first-run.md) ·
[continuing from records](examples/returning-session.md) ·
[a name that does not surface](examples/personal-brand.md) ·
[what to write next](examples/content-plan.md) ·
[technical fixes and an approval](examples/technical-fix.md) ·
[a review with no Search Console](examples/review-without-analytics.md) ·
[staying quiet](examples/stays-quiet.md).

## Inside the skill

| File | What it holds |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Activation, rules, approval boundaries, commands, the session loop |
| [`references/records.md`](references/records.md) | Where records live, every file, task format and statuses, multi-site rules |
| [`references/discovery.md`](references/discovery.md) | First-run discovery |
| [`references/research-methods.md`](references/research-methods.md) | Evidence labels, tools, snapshots, never-fabricate list |
| [`references/strategy.md`](references/strategy.md) | The master strategy and KPIs |
| [`references/personal-brand.md`](references/personal-brand.md) | Name searches, namesakes, identity consistency, brand pages |
| [`references/keyword-research.md`](references/keyword-research.md) | Sources, intent, the opportunity score, mapping, cannibalization |
| [`references/competitor-analysis.md`](references/competitor-analysis.md) | Competitor kinds, profiles, gaps to tasks |
| [`references/technical-seo.md`](references/technical-seo.md) | Crawling, indexing, URLs, rendering, performance, severity |
| [`references/on-page-seo.md`](references/on-page-seo.md) | Titles, descriptions, headings, content, images, internal links |
| [`references/content-strategy.md`](references/content-strategy.md) | Clusters, roadmap, briefs, drafting rules, publishing |
| [`references/structured-data.md`](references/structured-data.md) | Which schema, entity connections, validation |
| [`references/authority-building.md`](references/authority-building.md) | Genuine authority, the tracker, outreach rules |
| [`references/analytics.md`](references/analytics.md) | Search Console and analytics, working without them |
| [`references/prioritization.md`](references/prioritization.md) | The scoring model and choosing the next action |
| [`references/experimentation.md`](references/experimentation.md) | Hypotheses, baselines, windows, attribution |
| [`references/implementation.md`](references/implementation.md) | Changing website code safely, per framework |
| [`references/search-guidelines.md`](references/search-guidelines.md) | Google's guidance, spam policies, myths |
| [`references/reporting.md`](references/reporting.md) | Report formats and explaining changes to a beginner |
| [`templates/`](templates/) | One template per record file |
| [`scripts/seo_audit.py`](scripts/seo_audit.py) | `page`, `crawl`, `sitemap` and `robots` checks; can check a local build against production URLs |
| [`scripts/gsc_report.py`](scripts/gsc_report.py) | Search Console export analysis: brand split, positions 8–20, low CTR for position, period changes |
| [`scripts/test_seo_scripts.py`](scripts/test_seo_scripts.py) | Self-check for both scripts, against a local server; no network |

The scripts are standard-library Python 3 (3.9 or later), with nothing to
install.

## External data it can use

Whatever the environment already has: a web search tool, a page fetcher or
browser, a Google Search Console integration or exports, Google Analytics,
Bing Webmaster Tools, PageSpeed Insights or Lighthouse, and keyword or
backlink tools the owner already pays for. It never installs, signs up for or
buys anything without approval, and never suggests a subscription when a free
source answers the question.

## Limitations

- Without Search Console it cannot know indexing status, real queries,
  impressions or clicks. It says so, tracks what it can, and makes connecting
  Search Console an early task.
- Search results vary by person, place, device and time. Its observations
  are snapshots, and its web search tool may not be Google.
- No search volumes without a keyword tool. Demand is scored from evidence
  anchors instead.
- Pages that render their content with JavaScript can look empty to its
  fetcher. It checks with a browser tool or the source before reporting thin
  content.
- It cannot change third-party profiles, send outreach or publish. It
  prepares the text; the owner acts or authorizes.
- No SEO practice guarantees rankings, and this skill does not claim to.

## License

MIT
