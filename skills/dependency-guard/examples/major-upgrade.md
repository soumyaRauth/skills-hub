# Example — a major upgrade, measured against the call sites

Illustrative. The repository is invented. The Express 5 changes listed are ones
its migration guide describes; a real run reads the guide rather than relying
on a list like this one.

## Request

> Upgrade Express to version 5.

## Evaluation

Identity is not in question here: `express` is already installed and the
upgrade stays on the same package. The questions are what version 5 removes,
and which of those removals this codebase uses.

**Runtime floor.** Express 5 requires Node.js 18 or newer. `package.json` has
no `engines` field. `.nvmrc` says `16`. The CI workflow runs on `node-version:
16`.

**Breaking changes that this repository hits**, found by grepping for each
removed or changed API from the migration guide:

| Change in 5 | Where it is used here |
| --- | --- |
| `app.del()` removed (use `app.delete()`) | `src/api/admin/users.js:22` |
| `req.param(name)` removed | `src/api/search.js:5`, `src/api/admin/billing.js:6` |
| Route path syntax: wildcards must be named, optional parameters use braces | `src/server.js:12` (`/files/*`), `src/api/upload.js:14` (`/:id?`) |
| Rejected promises from handlers reach the error handler | `src/server.js:15` error handler assumes synchronous errors. Now it sees async ones too, and it returns stack traces (a separate existing problem) |

**Not hit:** `res.sendfile` (never used), `res.json(obj, status)` (never used).

**Transitive change:** measured from `npm install express@5 --dry-run
--ignore-scripts` in a scratch copy, 11 packages changed, 4 removed. No
lifecycle scripts added.

## Response

```
DEPENDENCY  express ^4.18.2 → ^5 — framework upgrade
DECISION    ADD WITH CONDITIONS
WHY         Six call sites use APIs version 5 removes or changes, and the project
            runs Node 16, below version 5's floor of 18.
CONDITIONS  Node 18+ in .nvmrc and CI first · fix the 6 call sites in the same
            change · the error handler reviewed for async errors
UNVERIFIED  Behavior under the new path matcher for URLs already in clients'
            bookmarks — needs a request-level test, not a grep
```

```
HANDOFF → impact-map: express 5 breaks 6 call sites across 5 files; route syntax
          changes affect public URLs
HANDOFF → proof-driven-dev: route-matching tests for /files/* and /:id? before
          and after the upgrade
```

## What it did not do

- Did not start the upgrade before the Node floor was raised: the work would
  have been blocked by CI anyway.
- Did not list every change in the migration guide, only the ones this code
  hits.
- Did not guess at transitive counts: the number is from the dry run, with the
  command named.
