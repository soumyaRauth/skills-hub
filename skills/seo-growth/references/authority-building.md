# Authority building

Links and mentions from relevant, respected places are among the strongest
signals a site can earn, and the hardest to fake without risk. The only
durable method is to be worth citing, then make sure the right people know.

## Contents

- What counts
- Opportunity types
- Finding opportunities
- Prioritizing
- The tracker
- Outreach
- Never

## What counts

A genuine opportunity has: a relevant audience, editorial judgment on the
other side (someone chooses to link or feature), a real contribution from the
owner, and value to that audience even if the link carried no SEO weight. If
the only reason to do it is the link, it is probably a link scheme.

## Opportunity types

| Type | What the owner contributes | Fits when |
| --- | --- | --- |
| Original publications | An article, research, a dataset, a benchmark others can cite | The owner has knowledge or data others lack |
| Expert contributions | A guest article or answer on a respected site in the field, written for its readers | The site publishes practitioners and the topic fits |
| Interviews and podcasts | An informed conversation | The owner has a story or expertise the show's audience wants |
| Talks and workshops | A session at a meetup or conference | The owner can teach something; event pages link to speakers |
| Open-source projects | Useful code with clear authorship | The owner builds tools; READMEs, package registries and dependents link back |
| Useful tools and resources | A calculator, template, checklist, reference | A recurring need in the field is unmet |
| Educational content | Courses, tutorials, documentation contributions | The owner teaches well |
| Communities | Helpful participation where the audience gathers | Profiles and contributions there are legitimate; links only where they help |
| Collaborations | Joint projects, co-authored work | Real partnerships |
| Professional profiles and directories | A complete, accurate listing | Respected in the field (a professional body, a speakers' directory); not bulk directories |
| Resource pages | A genuinely useful page that belongs on a curated list | The list is maintained and the page earns its place |
| Unlinked mentions and broken links | A polite note | Someone mentions the owner or their project without linking; or links to a dead page the owner's page replaces |
| Digital PR | A newsworthy finding or story | There is real news |

## Finding opportunities

- Search for where peers and competitors are featured: interviews, podcast
  guests, conference speakers, contributor pages
  (`references/competitor-analysis.md`).
- Search for mentions of the owner's name, projects and products that do not
  link.
- Check communities the audience uses, and publications in the field that
  accept contributions.
- Check the owner's existing assets: projects that could be listed, talks
  never linked, publications without a canonical page on the site.
- Search Console's Links report, when available, shows who already links.

Record evidence for each: the page, why it fits, and the date found.

## Prioritizing

Score opportunities with the task model in `references/prioritization.md`,
reading the factors as: Impact (relevance and editorial quality of the
place, and its audience's value to the owner), Confidence (how likely a real
yes is), Relevance, Effort. Add Risk: anything resembling a paid placement,
a reciprocal arrangement or a mass campaign is high risk and usually
rejected.

## The tracker

`authority.md`, one entry per opportunity:

```markdown
### AUTH-004 · Guest on a data engineering podcast
- Website: example-podcast.example · Contact page: https://example-podcast.example/guests
- Type: Interview · Relevance: high (audience is data engineers)
- Evidence: episodes with practitioners on orchestration topics (VERIFIED, 2026-11-25)
- Proposed contribution: the retry-storm incident and what changed afterwards
- Status: Drafted · awaiting the owner's approval to send
- Dates: found 2026-11-25 · sent — · follow-up —
- Result: —
```

Statuses: `Idea`, `Researching`, `Drafted`, `Awaiting Approval`, `Sent`,
`Follow-up due`, `Accepted`, `Declined`, `Published`, `Dropped`. Record the
resulting link or mention when one appears, verified by fetching it.

## Outreach

- **Draft only.** The skill researches and drafts. The owner sends, or
  authorizes sending, per message or under a written policy in
  `profile.md`.
- One person, one message, written for them: why them, what the owner
  offers their audience, what is being asked, in a few sentences.
- No templates blasted to lists, no flattery that is not specific, no
  misrepresentation of who is writing or why.
- At most one polite follow-up, and only if the owner agrees.
- Never commit the owner to work, dates or payment.

## Never

- Buy or sell links that pass ranking credit, or exchange links at scale.
- Private blog networks, link farms, expired-domain schemes.
- Guest posting campaigns built to place keyword-rich anchor links.
- Comment, forum or directory spam; profile creation for links.
- Fake testimonials, reviews, credentials, editorial mentions or affiliations.
- Widgets, templates or tools with hidden or keyword-rich links.
- Automated link building of any kind.

When the owner asks for one of these, decline in one line, name the risk
(Google's link spam policies can lead to ignored links or a manual action),
and offer the closest genuine alternative.
