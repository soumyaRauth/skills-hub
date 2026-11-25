# Content strategy and topical authority

Topical authority comes from covering a subject so usefully and so
completely that the site becomes a natural destination for it. For one
person, that means a few subjects they genuinely know, covered with the
evidence only they have.

## Contents

- Choosing topics
- Topic clusters
- The roadmap
- Existing content: update, consolidate, remove
- The brief
- Drafting rules
- The production workflow
- The quality bar
- Publishing

## Choosing topics

Core topics sit where three things meet: the owner's real expertise and
work, what the owner's audience searches for, and what serves the owner's
objective. Two or three to start. A topic the owner cannot write about from
experience is a topic they will lose on.

## Topic clusters

For each core topic, plan:

| Piece | Role |
| --- | --- |
| Pillar page | The broad, definitive overview of the topic, linking to every supporting piece |
| Supporting articles | One specific intent each: a how-to, a troubleshooting guide, a comparison, a concept |
| Project pages and case studies | First-hand proof: what the owner built, the decisions and the outcome |
| Tutorials and practical guides | Step-by-step, with working code or concrete steps |
| FAQs | Only where real questions recur and a short answer serves them |

Links: the pillar links to each supporting page; each supporting page links
back to the pillar and to its close siblings; project pages link to the
articles they illustrate and back.

## The roadmap

`roadmap.md` lists clusters and their pieces, each with: target keyword
group, intent, format, the owner's unique angle, priority score
(`references/prioritization.md`), status (idea, brief, draft, review,
published, updating) and the task ID.

Order by: technical preconditions satisfied, strategic importance,
opportunity score, existing authority (start where the site already has
impressions), feasibility for the owner, and effort. Plan at a cadence the
owner can keep; a monthly article they can sustain beats a weekly plan they
abandon.

## Existing content: update, consolidate, remove

Before writing anything new, check what exists:

- **Update** pages with impressions but weak engagement or outdated facts.
  Usually the highest-value content work on an established site.
- **Consolidate** pages that split one intent between them
  (`references/keyword-research.md`, cannibalization): merge into the
  stronger URL and redirect the other. Needs approval.
- **Remove or `noindex`** only when a page is useless to readers, cannot be
  improved, and has no links or traffic worth keeping, with evidence. Needs
  approval. Never prune for its own sake.

## The brief

Write one before drafting. `templates/roadmap.md` has the format.

- Audience and what they already know.
- Primary keyword group and intent, from a dated snapshot.
- What currently ranks, its format and depth, and its gaps.
- The unique value: what this page will have that the others do not
  (first-hand experience, a real dataset, working code, a decision
  framework, a clearer explanation).
- Outline with headings.
- Facts that need verifying, and facts only the owner can supply.
- Internal links in and out; external references to primary sources.
- Title, description and structured data plan.

## Drafting rules

- Write in the owner's voice, from the owner's knowledge. Read their
  existing articles first.
- Never invent experience, results, clients, numbers, quotes or citations.
  Mark gaps with a visible placeholder the owner fills:
  `[[OWNER: what happened when the retry storm hit production?]]`.
- Verify technical claims: run the code, check the current documentation
  and versions, and note what could not be verified.
- Cite primary sources for claims a reader would want to check.
- Cut filler: no throat-clearing introductions, no padded conclusions.
- AI assistance is acceptable when the result is accurate, original and
  reviewed by the owner. Producing many pages mainly to attract search
  traffic is scaled content abuse, whoever or whatever writes them.

## The production workflow

1. Audience · 2. Intent · 3. Search landscape snapshot · 4. Competing pages ·
5. Gaps · 6. Unique value · 7. Outline · 8. Fact list · 9. Draft ·
10. Accuracy review · 11. Intent alignment review · 12. Originality review ·
13. Quality review · 14. Title, description, slug · 15. Internal links ·
16. External references · 17. Structured data · 18. Final read of the page
as a visitor · 19. **Publish only with approval** · 20. Track: a `content.md`
row, an experiment or a review date.

Steps 1 to 8 are the brief. Steps 10 to 13 can lean on `human-empathy` for
whether the piece serves its reader.

## The quality bar

A draft is ready for the owner when it:

- Answers the target intent fully and early.
- Contains something a reader cannot get from the current top results.
- Has no unverified factual claim presented as fact.
- Has no placeholder left unmarked, and no invented experience.
- Reads clearly, with no filler.
- Has a descriptive title and description, sensible headings, internal
  links, and correct structured data.

## Publishing

Publishing is the owner's decision unless `profile.md` holds a written
publication policy. Save drafts where the site keeps drafts (a `draft: true`
front matter flag, a drafts folder), or in `.seo-growth/<site>/drafts/` if it
has no convention. Never commit a draft as published, never deploy, and never
post anything externally without authorization.
