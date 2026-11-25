# SEO backlog · noorhaldar.example

Scoring: Priority = (Impact × Confidence × Relevance) ÷ Effort, each 1–5 (references/prioritization.md).
Statuses: Backlog · Researching · Ready · In Progress · Awaiting Approval · Completed · Monitoring · Blocked · Rejected

## Now

1. SEO-003 Remove noindex from /about.html — Awaiting Approval — the page most likely to answer a name search is excluded
2. SEO-005 Fix the canonical on the retries article — Awaiting Approval — points to http://www.
3. SEO-009 Link to /talks.html — Ready — orphan in the sitemap
4. SEO-011 Person structured data on the about page — Ready
5. SEO-012 Connect Search Console — Blocked on the owner

## Tasks

### SEO-001 · First-run discovery, baseline and records
- Status: Completed
- Category: Maintenance
- Target: site
- Keyword or intent: —
- Why: no records existed
- Score: —
- Risk: Low · Approval: not needed
- Depends on: none
- Measure: records exist
- Created: 2026-10-20 · Completed: 2026-10-20
- Log: 2026-10-20 baselines/2026-10-20.md written

### SEO-002 · Name and role in the homepage title, description and h1
- Status: Monitoring
- Category: Brand · Quick win
- Target: /
- Keyword or intent: "noor haldar" · navigational, brand
- Why: title was "Home" and h1 "Portfollio"; nothing on the homepage named the owner in a heading (VERIFIED, seo_audit.py page, 2026-10-20)
- Score: Impact 4 · Confidence 4 · Relevance 5 · Effort 1 → 80
- Risk: Low · Approval: not needed
- Depends on: none
- Measure: EXP-001
- Created: 2026-10-20 · Completed: 2026-10-20
- Log: 2026-10-20 done in portfolio/index.html, validated; 2026-10-21 owner pushed to main

### SEO-003 · Remove noindex from /about.html
- Status: Awaiting Approval
- Category: Critical technical · Brand
- Target: /about.html
- Keyword or intent: "noor haldar" · navigational
- Why: meta robots noindex with a "staging" comment (VERIFIED, 2026-10-20); the page holds the full bio
- Score: Impact 5 · Confidence 5 · Relevance 5 · Effort 1 → 125
- Risk: Low · Approval: needed (robots directive)
- Depends on: none
- Measure: page indexable in seo_audit.py; URL Inspection once Search Console exists
- Created: 2026-10-20 · Completed: —
- Log: 2026-10-20 approval requested; 2026-10-21 owner: "let me check why I added it first"

### SEO-004 · Remove the link to the unpublished sensors article
- Status: Completed
- Category: Maintenance
- Target: /blog/
- Keyword or intent: —
- Why: /blog/airflow-sensors.html returns 404, linked from /blog/ (VERIFIED, crawl 2026-10-20)
- Score: Impact 2 · Confidence 5 · Relevance 3 · Effort 1 → 30
- Risk: Low · Approval: not needed
- Depends on: none
- Measure: crawl shows no broken internal links
- Created: 2026-10-20 · Completed: 2026-10-20
- Log: 2026-10-20 removed the list item; crawl clean

### SEO-005 · Fix the canonical on the retries article
- Status: Awaiting Approval
- Category: Critical technical
- Target: /blog/airflow-retries.html
- Keyword or intent: airflow retries · know, do
- Why: canonical is http://www.noorhaldar.example/... while the site serves https://noorhaldar.example (VERIFIED, 2026-10-20)
- Score: Impact 4 · Confidence 5 · Relevance 4 · Effort 1 → 80
- Risk: Low · Approval: needed (canonical change)
- Depends on: none
- Measure: seo_audit.py shows a self-referencing canonical
- Created: 2026-10-20 · Completed: —
- Log: 2026-10-20 approval requested

### SEO-007 · Make the pipeline-lint JSON-LD parse
- Status: Completed
- Category: Quick win
- Target: /projects/pipeline-lint.html
- Keyword or intent: pipeline-lint · navigational
- Why: trailing comma made the block invalid JSON (VERIFIED, 2026-10-20)
- Score: Impact 2 · Confidence 5 · Relevance 4 · Effort 1 → 40
- Risk: Low · Approval: not needed
- Depends on: none
- Measure: block parses
- Created: 2026-10-20 · Completed: 2026-10-20
- Log: 2026-10-20 fixed and validated

### SEO-008 · Unique title, description and alt text on the pipeline-lint page
- Status: Completed
- Category: Quick win
- Target: /projects/pipeline-lint.html
- Keyword or intent: pipeline-lint, airflow dag linter · navigational, know
- Why: title and description duplicated /projects/ (VERIFIED, crawl 2026-10-20)
- Score: Impact 3 · Confidence 4 · Relevance 4 · Effort 1 → 48
- Risk: Low · Approval: not needed
- Depends on: none
- Measure: crawl shows no duplicate titles
- Created: 2026-10-20 · Completed: 2026-10-20
- Log: 2026-10-20 done and validated

### SEO-009 · Link to /talks.html from the about page and homepage
- Status: Ready
- Category: Quick win · Brand
- Target: /talks.html
- Keyword or intent: noor haldar talks · navigational
- Why: in the sitemap, no internal links (VERIFIED, crawl 2026-10-20)
- Score: Impact 2 · Confidence 4 · Relevance 4 · Effort 1 → 32
- Risk: Low · Approval: not needed
- Depends on: none
- Measure: crawl shows inlinks
- Created: 2026-10-20 · Completed: —
- Log: 2026-10-20 created

### SEO-010 · Sitemap lists the article, and stops listing noindex pages
- Status: Backlog
- Category: Critical technical
- Target: /sitemap.xml
- Keyword or intent: —
- Why: sitemap omits /blog/airflow-retries.html and lists noindex /about.html (VERIFIED, crawl 2026-10-20)
- Score: Impact 3 · Confidence 5 · Relevance 4 · Effort 1 → 60
- Risk: Low · Approval: needed (sitemap)
- Depends on: SEO-003, SEO-005
- Measure: crawl shows no sitemap conflicts
- Created: 2026-10-20 · Completed: —
- Log: 2026-10-20 created

### SEO-011 · Person structured data on the about page
- Status: Ready
- Category: Brand · Structured data
- Target: /about.html
- Keyword or intent: noor haldar · navigational
- Why: no structured data names the owner anywhere on the site (VERIFIED, 2026-10-20)
- Score: Impact 3 · Confidence 3 · Relevance 5 · Effort 1 → 45
- Risk: Low · Approval: not needed
- Depends on: none (useful only once SEO-003 lands, but harmless before)
- Measure: parses; matches visible bio
- Created: 2026-10-20 · Completed: —
- Log: 2026-10-20 created

### SEO-012 · Connect Google Search Console
- Status: Blocked
- Category: Maintenance
- Target: site
- Keyword or intent: —
- Why: no first-party search data; KPIs cannot be measured (VERIFIED, 2026-10-20)
- Score: Impact 4 · Confidence 5 · Relevance 5 · Effort 2 → 50
- Risk: Low · Approval: owner action (DNS record or verification file token)
- Depends on: owner
- Measure: exports arrive in data/
- Created: 2026-10-20 · Completed: —
- Log: 2026-10-20 owner asked to verify a Domain property

### SEO-013 · Write "Airflow sensors that don't starve your workers"
- Status: Backlog
- Category: Content
- Target: new /blog/airflow-sensors.html
- Keyword or intent: airflow sensor reschedule mode · know, do
- Why: owner planned it; the retries article references the incident (VERIFIED); demand evidence 3 (autocomplete, 2026-10-20 snapshot)
- Score: Impact 3 · Confidence 3 · Relevance 4 · Effort 3 → 12
- Risk: Low · Approval: needed to publish
- Depends on: a brief; facts only the owner can supply
- Measure: content.md row; impressions once Search Console exists
- Created: 2026-10-20 · Completed: —
- Log: 2026-10-20 created
