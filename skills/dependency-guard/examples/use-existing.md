# Example — a library for one function

Illustrative. The repository is invented; the decision shape is the point.

## Request

> Add lodash so we can debounce the customer search box.

## What the ladder found

- **Codebase:** `src/lib/timing.js` exports `throttle(fn, ms)`. It is 11 lines,
  used by `web/components/ScrollSpy.jsx`, with a test in
  `src/lib/timing.test.js`. There is no debounce.
- **Platform:** no standard debounce in the browser or in Node.
- **Installed dependencies:** `package.json` has `express`, `@prisma/client`,
  `jsonwebtoken`, `multer`. None of them provides one.
- **A few lines:** debounce is a well-understood 9-line function, and it belongs
  beside the throttle that already exists.

The ladder stopped at the fourth rung, so no package was evaluated.

## Response

```
DEPENDENCY  lodash — debounce for web/components/SearchBar.jsx
DECISION    USE EXISTING — add debounce() to src/lib/timing.js
WHY         One function is needed. timing.js already holds throttle() with its
            tests; debounce is its sibling, and no other lodash function is used
            anywhere in the repository.
```

Then the work: `debounce` added beside `throttle`, two tests in the style of the
existing ones (fires once after the quiet period; resets on each call),
`SearchBar.jsx` wired to it, and the suite run.

## What it did not say

- No lodash download count, maintainer list or size. None of it was needed to
  decide, and none of it was read.
- No lecture on dependency hygiene.
- Nothing about the other packages in the manifest. They were not the question.

If the user replies *"we'll want more of lodash later, add it"*, that settles
it. The next step is the name check and the dry run, and then the install.
