# Prioritization

The skill acts as the decision-maker: out of everything that could be done,
what should be done next, and what should never be done at all? The answer is
a short ranked list, not an exhaustive one.

## Contents

- The task score
- Factor anchors
- Overrides
- Categories
- Picking the next action
- What not to do

## The task score

Score every task from 1 to 5 on four factors, each with a one-line reason:

**Priority = (Impact × Confidence × Relevance) ÷ Effort**

The range is 0.2 to 125; round to a whole number. Bands:

| Score | Band | Meaning |
| --- | --- | --- |
| 40 and above | Now | Candidates for the `Now` list |
| 15 to 39 | Next | Strong, after the current work |
| 5 to 14 | Later | Worth keeping, not soon |
| Below 5 | Icebox | Record it once; do not revisit without new evidence |

The score orders judgments; it does not measure anything, and the report
never presents it as a measurement. Two tasks within a few points of each
other are a tie; break ties with dependencies, risk and the owner's goal.

## Factor anchors

| Factor | 1 | 3 | 5 |
| --- | --- | --- | --- |
| **Impact**: effect on search visibility for the site's goals | Cosmetic, or a page nobody searches for | Improves an important page, or many minor ones | Unblocks indexing of important pages, or the main brand or money query |
| **Confidence**: how sure the evidence makes us that the impact is real | Speculation | Supported by documentation or a clear pattern in the data | Verified defect, or measured opportunity in Search Console |
| **Relevance**: to the owner's objective | Tangential | Supports authority in a core topic | Directly serves the goal or the name |
| **Effort**: time and complexity, including the owner's time | Minutes | A focused session | Weeks, or needs others' involvement |

Risk and dependencies are not in the formula. They decide whether a task can
run: high-risk tasks need approval, and blocked tasks cannot be `Now`,
whatever their score.

## Overrides

Ahead of any score, in this order:

1. A suspected hacked site, malware, or anything harming visitors.
2. Critical technical issues: important pages not indexable, site-wide
   blocks, wrong canonical hosts.
3. Work the owner explicitly asked for in this request.
4. Approvals already granted, so approved work does not stall.
5. Experiments whose evaluation date has arrived.

## Categories

Tag each task with one category. Reports group by them, so the owner sees
balance at a glance:

- Critical technical
- Quick win: high score, effort 1 or 2
- Strategic: long-term, high impact, high effort
- Content
- Brand
- Authority
- Maintenance
- Low value: kept for the record, rarely done

A healthy backlog has work across technical, content, brand and authority.
If every task is technical, ask whether the technical work is still the
constraint.

## Picking the next action

1. Apply the overrides.
2. Among `Ready` tasks the approval table allows, take the highest score.
3. Prefer finishing `In Progress` work over starting new work.
4. Fit the session: a quick win and one strategic step beat five half-done
   tasks.
5. Re-rank the `Now` list (at most five), and name the single next action in
   the report.

## What not to do

- Spend sessions on tasks scoring below 5.
- Re-audit what has not changed.
- Chase a third-party tool's score or a plugin's checklist.
- Produce content to raise page count.
- Ask the owner to rank tasks. Recommend, and let them override.
