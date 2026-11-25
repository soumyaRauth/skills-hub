# Experiments

Most SEO changes are judged weeks later, against noisy data, with search
engines changing underneath. An experiment record makes that judgment honest:
what was expected, what the baseline was, when to look, and what was
actually seen.

## Contents

- When to run one
- The record
- Baselines
- Evaluation windows
- Judging the result
- Decisions
- Attribution rules

## When to run one

Start an experiment for a change whose effect is worth measuring and could
be measured: titles and descriptions on pages with impressions, a content
rewrite, a consolidation, internal links to a page, structured data on a set
of pages, a technical fix with a visible effect. Do not run one for hygiene
fixes nobody will evaluate.

Change one thing per page per experiment where possible. Two changes at once
cannot be told apart.

## The record

`experiments.md`, using `templates/experiments.md`:

```markdown
### EXP-002 · Name and role in the homepage title
- Task: SEO-004 · Pages: /
- Hypothesis: a title naming the owner and role will raise CTR for name
  queries, because the old title "Home" did not say whose site it is
- Baseline: Search Console, 2026-10-28 to 2026-11-24 (28 days): name queries,
  page / → 41 impressions, 9 clicks, average position 3.4 (VERIFIED, export)
- Change: <title>Home</title> → <title>Jane Doe · Data engineer</title>
- Implemented: 2026-11-25 · Deployed: 2026-11-26 (owner confirmed)
- Recrawled: UNKNOWN (check with URL Inspection)
- Expected: higher CTR for name queries; no change in position expected
- Evaluate: from 2026-12-24, comparing 28 days after recrawl with the baseline
- Result: —
- Interpretation: —
- Decision: —
```

Without Search Console, the baseline is whatever can be measured the same
way again (a dated snapshot method), and the record says how weak that is.

## Baselines

- Capture before changing anything. A baseline reconstructed afterwards is
  labelled as such.
- Record the source, the property, the exact date range and the numbers
  with their labels.
- Note context: recent algorithm updates, seasonality, other changes to the
  same pages.

## Evaluation windows

- The change counts from when the new version was live **and** recrawled,
  not from the commit.
- Compare equal-length windows, ending on the same weekday, excluding the
  days around the change.
- Twenty-eight days on each side is a sensible default for small sites. Use
  longer windows when impressions are few.
- Watch for a control: pages that were not changed. If they moved the same
  way, the change probably did not cause it.

## Judging the result

| Result | When |
| --- | --- |
| `IMPROVED` | The metric moved in the expected direction clearly beyond normal week-to-week variation on this page, and unchanged pages did not move the same way |
| `NO CHANGE` | Movement within normal variation |
| `WORSE` | A clear move in the wrong direction, with the same control check |
| `INCONCLUSIVE` | Too little data, a confounder (an update, a season, other changes), or no recrawl yet |

Estimate normal variation from the page's own history: how much the metric
moves between comparable windows when nothing changed. Low-volume pages are
usually `INCONCLUSIVE`, and saying so is the honest result.

## Decisions

- `KEEP` and close the task, recording the learning in `strategy.md` if it
  generalizes ("name-first titles worked on this site").
- `EXTEND` to similar pages, as new tasks.
- `REVERT` with approval when the change hurt.
- `RE-EVALUATE` on a stated later date when inconclusive.

## Attribution rules

- Never claim a change caused a ranking or traffic movement without a
  baseline, a window after recrawl, and a control check.
- Even then, say "consistent with", not "caused".
- Report failures as plainly as successes. A failed experiment is
  information; hiding it repeats it.
