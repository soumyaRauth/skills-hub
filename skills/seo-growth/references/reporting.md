# Reporting

Reports are short, honest, and end in an action. The owner may be new to SEO:
the report should leave them knowing what happened, what it means, and what
they need to decide, without having to learn the vocabulary first.

## Contents

- Rules for every report
- Explaining a change
- The session report
- The initial report
- The periodic review
- The monthly report
- Approval requests

## Rules for every report

- Lead with what matters most, in plain words.
- Every number has its label and source; every period has exact dates.
- Separate what was done from what was proposed.
- Say what was not checked and what data was missing.
- Show at most five priorities. The rest are in `backlog.md`.
- End with one next action, and anything awaiting the owner.
- Never fill a missing metric. Write `UNKNOWN (no Search Console access)`.

## Explaining a change

For each significant change or recommendation, five short lines:

```
What:     The about page tells search engines not to index it.
Why:      It is the page most likely to answer a search for your name.
Change:   Remove the noindex line from about.html.
Expect:   Google can include the page in results once it recrawls it.
Measure:  URL Inspection in Search Console; name-query impressions for /about/.
```

Explain a term once, the first time it appears, in a clause: "a canonical
tag (the line that tells search engines which URL is the main version)". Do
not explain it again in later reports.

## The session report

```
SEO · example.com · improve · 2026-11-25

Done
  SEO-002  Titles and descriptions on 4 pages             validated before/after
  SEO-004  Fixed the broken link on /blog/                validated by crawl

Needs your approval
  SEO-003  Remove noindex from /about/   [What/Why/Change/Expect/Measure]

Found
  /talks/ is listed in the sitemap but no page links to it (VERIFIED, crawl)

Not checked
  Indexing and real queries: no Search Console access

Changes are in the working tree, not committed.
Next: approve SEO-003; then SEO-005, internal links to /talks/.
```

## The initial report

After the first run:

1. **Website overview**: what the site is, whose, for whom, built how.
2. **SEO health**: the few findings that matter, by severity, verified.
3. **Brand visibility**: the name-search snapshot, labelled with how it was
   taken.
4. **Technical issues**: critical and high only; the rest counted.
5. **Keyword opportunities**: the first groups and why.
6. **Content opportunities**: updates first, then new pages.
7. **Competitor observations**: who actually ranks, and the gap to exploit.
8. **Authority opportunities**: two or three genuine ones.
9. **Top priorities**: the `Now` list.
10. **Done this session**, **needs approval**, **data limitations**, and
    **where the records are**.

## The periodic review

`reviews/YYYY-MM-DD.md` from `templates/review.md`, for `review` or a weekly
cadence:

- Period covered and the previous review's date.
- Work completed since, by task ID.
- Technical and content improvements, with validation.
- Search performance, if data exists, against the previous period.
- Experiments evaluated, with results and decisions.
- New opportunities and discoveries.
- Pending tasks and approvals.
- Priority changes and why.
- Next actions.

## The monthly report

Adds, for the calendar month or the stated 28-day window, each with source:

- Organic impressions, clicks, CTR and average position, against the
  previous period.
- Brand and non-brand performance.
- Pages with impressions; indexed pages, where available.
- Organic sessions and key events, where available.
- Content published and updated, and early performance.
- Technical status.
- Authority opportunities pursued and earned.
- Interpretation: what the numbers likely mean, labelled, with confounders.
- Risks.
- Next month's strategy, as changes to `strategy.md` if any.

Without data, the monthly report says which sections are unavailable and
reports the manual tracking instead (`references/analytics.md`).

## Approval requests

One block per session, each item:

```
SEO-003  Remove noindex from /about/                         recommended: yes
  Why:   the page most likely to answer a search for your name is excluded
  Risk:  low; the page is meant to be public
  Undo:  put the line back
  Reply "approve SEO-003", or "no" with a reason and I will record it.
```
