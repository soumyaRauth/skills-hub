# Example: continuing from records

The fixture `tests/fixtures/seo-growth/returning-site`: two sites in one
repository (`portfolio/` and `pipeline-lint-docs/`), each with records in
`.seo-growth/`. The last session for the portfolio was 2026-10-20, followed by
an owner update on 2026-10-21. Today is 2026-11-25.

## Contents

- The request
- Context, from the records
- What it does, in order
- The report
- What it must not do

## The request

```
Pick up where we left off on my site's search traffic.
```

## Context, from the records

- Two sites have records. Neither folder is the current directory, so it
  continues `noorhaldar.example`, the one with the most recent history entry,
  and says so in the first line.
- `backlog.md`, `Now`: SEO-003 and SEO-005 await approval; SEO-009 and
  SEO-011 are ready; SEO-012 is blocked on the owner.
- `history.md`, 2026-10-21: the owner pushed the first session's changes and
  wrote, about SEO-003, "let me check why I added it first".
- `profile.md`, standing authorization dated 2026-10-21: titles,
  descriptions, alt text and links in `portfolio/` may be edited without
  asking; no commits.
- `experiments.md`: EXP-001 became due on 2026-11-24.
- Completed: SEO-001, SEO-004, SEO-007, SEO-008. SEO-002 is Monitoring.
  None of these is redone.

## What it does, in order

1. **Check what changed since 2026-10-21.** `git log` shows no commits to
   `portfolio/` since then. A crawl of `portfolio/` served locally confirms
   the completed fixes are still in place and nothing new broke. The
   `noindex` and the canonical are unchanged.
2. **Evaluate EXP-001.** The baseline is a web-search-tool snapshot, so the
   evaluation repeats the same query set with the same tool:
   "noor haldar" now shows the homepage at position 6
   (`data/serp-2026-11-25.md`). Result: `INCONCLUSIVE`. It is one snapshot
   from a tool whose engine and location are unknown, with no recrawl date
   and no control. The record says the observation is consistent with the
   hypothesis and that Search Console is what would settle it.
   Decision: `RE-EVALUATE` on 2026-12-23, or as soon as SEO-012 is unblocked.
3. **Re-raise the approvals**, now 36 days old, with the context the owner
   asked for: the comment in `about.html` says the `noindex` was for
   staging, and the history records the site going live with the owner's
   push on 2026-10-21.
4. **Do the next ready work** under the standing authorization:
   - SEO-009: links to `/talks.html` from the about page ("Talks I've
     given") and the homepage's "Work with me" paragraph. The crawl now shows
     two inlinks and no orphan.
   - SEO-011: Person structured data on the about page, every property taken
     from the visible bio, with `sameAs` for the two profiles the page links
     to. It parses, and its name, role and location match the page.
     Structured data is not in the owner's standing authorization, but the
     approval table allows it, and it adds no claim the page does not make.
5. **Persist.** Backlog statuses and logs, a new `history.md` entry, the
   experiment result, a `content.md` update for `/about.html` and
   `/talks.html`, and the snapshot in `data/`. Nothing is written to
   `.seo-growth/pipeline-lint.example/`.

## The report

```
⚡ SEO Growth Engine — continuing noorhaldar.example from 2026-10-21

SEO · noorhaldar.example · 2026-11-25 · continuing
(pipeline-lint.example also has records, last worked 2026-09-30. Say the word to switch.)

Since last time: you pushed the first fixes on 2026-10-21; nothing else changed in portfolio/.

Done (validated, not committed)
  SEO-009  /talks.html is linked from the about page and the homepage (crawl: 2 inlinks)
  SEO-011  Person structured data on the about page, matching the visible bio

Experiment EXP-001 (homepage title and h1): INCONCLUSIVE
  Today's snapshot (same tool, same queries) shows your homepage at 6 for "noor haldar";
  on 2026-10-20 it was not in the first 10. That is encouraging, but one snapshot from
  one tool is not a trend. Re-evaluating on 2026-12-23, or sooner with Search Console.

Still waiting on you
  SEO-003  Remove noindex from about.html. You asked why it was added: the comment above
           it reads "staging: keep out of Google until launch". The site is live.
  SEO-005  Fix the retries article's canonical (http://www. → https://)
  SEO-012  Verify Search Console. It is the only way to see what Google actually shows.

Next: approve SEO-003 and SEO-005. Then SEO-010, the sitemap, which depends on both.
```

## What it must not do

- Redo the first run, re-audit the whole site, or re-propose completed work.
- Treat one snapshot as a ranking improvement, or EXP-001 as a success.
- Remove the `noindex` because the approval is "obviously" coming.
- Mix the two sites' records, or pick the docs site without saying so.
- Commit: the standing authorization says the owner pushes.
