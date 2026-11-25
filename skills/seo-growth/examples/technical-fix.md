# Example: technical fixes and an approval

A different site from the portfolio: a small Astro blog. Records exist from
an earlier audit. The owner asks for the technical work.

## Contents

- The request
- Verify before fixing
- What it fixes without asking
- What it asks about
- Validation
- After the approval

## The request

```
/seo-growth technical
```

## Verify before fixing

The backlog holds four technical findings from the audit three weeks ago.
Each is re-checked against the current code and a local build before
anything changes. Records can go stale.

```
$ npm run build            # passes before any change (recorded)
$ npx astro preview --port 4321 &
$ python3 <skill dir>/scripts/seo_audit.py crawl https://blog.example/ \
      --map-origin https://blog.example=http://localhost:4321 --delay 0
```

| Finding | Still true? | Evidence |
| --- | --- | --- |
| Tag pages duplicate titles ("Tag | Blog") | Yes | crawl: 14 tag pages share one title |
| Images without `width` and `height` on posts | Yes | `src/components/PostImage.astro` renders `<img>` without dimensions |
| `/feed` returns 404, linked from the footer | No | the owner fixed it last week (commit `4e1c2a0`); task closed as Completed with that note |
| Sitemap includes `/drafts/*` pages | Yes | `@astrojs/sitemap` has no filter; `astro.config.mjs` |

## What it fixes without asking

- **Tag page titles.** `src/pages/tags/[tag].astro` builds the title from a
  constant. It now uses the tag name: `Posts tagged "airflow" | Blog`. One
  template change, fourteen pages fixed.
- **Image dimensions.** `PostImage.astro` already receives the image
  metadata from Astro's image pipeline. It now passes `width` and `height`,
  so the browser reserves space and the layout stops shifting. No visual
  change.

Both are inside the approval table's "do without asking" column: metadata on
existing pages, and a performance fix that does not change what visitors see.

## What it asks about

```
Needs your approval
  SEO-021  Keep draft pages out of the sitemap                    recommended: yes
    What:    the sitemap lists 3 unfinished drafts under /drafts/
    Why:     it invites search engines to index pages you haven't published
    Change:  add a filter to the sitemap integration in astro.config.mjs:
             sitemap({ filter: (page) => !page.includes('/drafts/') })
    Risk:    low; only those 3 URLs leave the sitemap
    Undo:    remove the filter
  Also worth deciding: should /drafts/ pages be public at all? Removing them or adding
  noindex is a bigger change, and only yours to make.
```

Sitemap behavior is in the approval column, however small the diff.

## Validation

```
$ npm run build            # passes
$ npm test                 # 12 passed (the project's own tests)
$ python3 <skill dir>/scripts/seo_audit.py crawl ... --map-origin ...
```

- `duplicate-title` is gone. Each tag page's title names its tag.
- Every post image has `width` and `height` in the built HTML.
- No new findings. Page count and links are unchanged.
- Layout shift is expected to drop, but it was not measured: no field data
  exists for this site, and no Lighthouse run was made. The report says so.

## After the approval

The owner replies "approve SEO-021". The filter goes in, the build passes,
`seo_audit.py sitemap` lists 41 URLs instead of 44 with no `/drafts/`
entries, and `history.md` records the approval with the owner's words and the
date. The question about whether drafts should be public stays open in the
backlog as SEO-022, `Awaiting Approval`, until the owner decides.
