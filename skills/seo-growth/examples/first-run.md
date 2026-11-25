# Example: first run on a personal portfolio

The fixture `tests/fixtures/seo-growth/portfolio-site`: a plain-HTML portfolio
for a data engineer, deployed to GitHub Pages. No records exist. The crawl
output below is what `seo_audit.py` actually printed against that fixture,
served locally.

## Contents

- The request
- Context
- Diagnose
- Prioritize and execute
- The initial report
- What it did not do

## The request

```
/seo-growth https://noorhaldar.example
```

## Context

No `.seo-growth/` here or in `~/.seo-growth/`, so this is a first run.
`CNAME` says `noorhaldar.example` and the README says the folder is the site,
so records go in `.seo-growth/noorhaldar.example/` in this repository.

Stack: plain HTML, no build, GitHub Pages from `main` (README). Each page's
`<head>` is hand-written; `robots.txt` and `sitemap.xml` are static files.

Data access, probed: a web search tool, a page fetcher, `seo_audit.py`.
No Search Console, no analytics, no keyword tool. Recorded in `profile.md`.

## Diagnose

```
$ python3 -m http.server 8765 -d . &
$ python3 <skill dir>/scripts/seo_audit.py crawl https://noorhaldar.example/ \
      --map-origin https://noorhaldar.example=http://localhost:8765 --delay 0

## HIGH broken-internal (1): internal URLs that fail (status, then linking pages)
- https://noorhaldar.example/blog/airflow-sensors.html [404] ← https://noorhaldar.example/blog/
## HIGH noindex (1): pages marked noindex (confirm each is intended)
- https://noorhaldar.example/about.html
## HIGH sitemap-noindex (1): sitemap lists pages that are noindex
## HIGH jsonld-invalid (1): pages with JSON-LD that does not parse
- https://noorhaldar.example/projects/pipeline-lint.html
## MEDIUM canonical-other-origin (1): pages whose canonical points to another origin
- https://noorhaldar.example/blog/airflow-retries.html
## MEDIUM orphan (1): in the sitemap, but no crawled page links to it
- https://noorhaldar.example/talks.html
## MEDIUM duplicate-title (1): "Projects | Noor Haldar": /projects/, /projects/pipeline-lint.html
## LOW missing-from-sitemap (1): /blog/airflow-retries.html
## LOW description-missing (1): /
```

Read in full: the homepage (`<title>Home</title>`, `<h1>Portfollio</h1>`,
the name appears only as "Noor" and a footer "Noor H."), the about page (a
good bio, a `noindex` with the comment `staging: keep out of Google until
launch`, a portrait with `alt=""`), the retries article (strong, first-hand,
canonical pointing at `http://www.`).

Name snapshot, web search tool, location unknown, 2026-11-25: "noor haldar"
shows other people with the same name and a GitHub profile; the site is not
in the first ten. Recorded as a snapshot in `brand.md`, not as a ranking.

## Prioritize and execute

| Task | Score | Approval | This session |
| --- | --- | --- | --- |
| SEO-003 Remove `noindex` from /about.html | 5·5·5 ÷ 1 = 125 | needed: robots directive | Requested |
| SEO-002 Name and role in the homepage title, description and `h1` | 4·4·5 ÷ 1 = 80 | no | Done |
| SEO-005 Self-referencing canonical on the retries article | 4·5·4 ÷ 1 = 80 | needed: canonical | Requested |
| SEO-007 Make the pipeline-lint JSON-LD parse | 2·5·4 ÷ 1 = 40 | no | Done |
| SEO-004 Remove the link to the unpublished sensors article | 2·5·3 ÷ 1 = 30 | no | Done |

The broken link points at an article that does not exist yet. The fix is
removing the "coming soon" list item, not inventing a page.

After the edits, `seo_audit.py page` on `/`, `/blog/` and
`/projects/pipeline-lint.html` shows the new title and description, no
broken link, and a JSON-LD block typed `SoftwareApplication`, `Person`.

## The initial report

```
⚡ SEO Growth Engine — first run for noorhaldar.example

SEO · noorhaldar.example · first run · 2026-11-25
Records: .seo-growth/noorhaldar.example/ (plain Markdown; commit them to keep history,
         or keep them out of git if you'd rather not publish your strategy)

The site: a data engineer's portfolio and writing, plain HTML on GitHub Pages.
Goal (from your README): clients and remote teams finding you by name or for Airflow help.

Biggest problem
  Your about page tells search engines not to index it. It is the page most likely to
  answer a search for your name.

Done (validated before and after, not committed)
  SEO-002  Homepage title "Noor Haldar · Data engineer and Apache Airflow consultant",
           a description, and h1 "Noor Haldar" instead of "Portfollio"
  SEO-007  pipeline-lint structured data now parses (a trailing comma broke it)
  SEO-004  Removed the link to the sensors article that does not exist yet

Needs your approval
  SEO-003  Remove noindex from about.html                         recommended: yes
    What:    a line in about.html says "don't index this page", left from staging
    Why:     it holds your full bio; name searches cannot find it
    Change:  delete <meta name="robots" content="noindex">
    Expect:  Google can include the page once it recrawls it; no ranking is promised
    Measure: URL Inspection in Search Console; name-query impressions for /about.html
    Undo:    put the line back
  SEO-005  Canonical on the retries article points to http://www.noorhaldar.example
           Change it to the page's own https URL                  recommended: yes

Name search (snapshot, web search tool, 2026-11-25): other people with your name fill
the first results; your GitHub appears; your site does not.

Data I don't have: Search Console (indexing, real queries, clicks). It's free;
SEO-012 explains the two-minute verification.

Next: approve SEO-003 and SEO-005. Then SEO-009 (link the talks page) and
SEO-011 (Person structured data on the about page).
```

## What it did not do

- It did not remove the `noindex` or change the canonical: both need approval.
- It did not add the article to the sitemap: sitemap changes need approval,
  and the canonical comes first (SEO-010 depends on SEO-005).
- It did not write the sensors article. It is SEO-013 in the backlog; the
  incident details are the owner's to supply.
- It did not state search volumes, positions or indexing status.
- It did not commit.
