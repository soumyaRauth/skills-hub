# Personal brand SEO

When someone types a person's name, the results page is that person's first
impression. The goal is a first page that is accurate, consistent, and
mostly made of things the person controls or genuinely earned, with their
own site as the hub that ties it together.

## Contents

- Name-search analysis
- Classifying results
- Identity ambiguity
- Identity consistency
- The canonical bio
- Brand pages on the site
- Entity signals
- Reputation
- What it records
- Boundaries

## Name-search analysis

Build the query set from facts, not guesses:

- The full name as the owner uses it, and variants: with and without a
  middle name or initial, a shortened first name, transliterations, common
  misspellings the owner confirms.
- Name + profession (`jane doe data engineer`), name + key expertise, name +
  company or employer, name + website or brand, name + projects, products or
  publications, name + city or country when location matters.

For each query, take a snapshot (`references/research-methods.md`): date,
engine or tool, location and device if known, and the first page of results.
Run the same set the same way at each review so snapshots are comparable.

When no search tool is available, give the owner the query list and ask for
the first page of each from a private window, as text or a screenshot.

## Classifying results

Tag each result:

| Tag | Example | Note |
| --- | --- | --- |
| `OWNED-SITE` | The person's domain | The hub; should rank first for the name where winnable |
| `OWNED-PROFILE` | LinkedIn, GitHub, a speaker profile they edit | Controlled; consistency matters |
| `EARNED` | An interview, a conference page, a publication, a podcast episode | Genuine third-party signals |
| `ABOUT-NEUTRAL` | A directory, an aggregator, an old event listing | Accurate or not? Note it |
| `DIFFERENT-PERSON` | Someone else with the same name | Record only the kind of result |
| `IRRELEVANT` | Unrelated | |
| `HARMFUL` | Inaccurate, outdated or damaging content about the owner | Handle under Reputation |

Also note features on the page: a knowledge panel, images, "People also
ask", news, videos. Record what is there, not what you expect.

**Gaps** are where the first page lacks something the owner has: their site
missing for their own name, a strong project that never appears, a
publication only findable by its title, a profile that would surface but
does not link back.

## Identity ambiguity

When others share the name, decide which queries are realistic:

- A more prominent namesake can hold the bare-name query indefinitely. Set
  the realistic target as name + profession or name + expertise, and say so
  in the strategy, instead of promising the bare name.
- Consistent disambiguators help searchers and search engines tell people
  apart: the same role line everywhere, the same photo, a middle initial if
  the owner uses one, the same links between properties.
- Never claim, imply or borrow another person's work, profile or results.

## Identity consistency

Build the matrix in `brand.md` (one row per property):

| Property | Name as shown | Role or headline | Bio | Photo | Links to site | Location | Complete | Last checked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Check the website, author pages, GitHub, LinkedIn, relevant social
profiles, publications, portfolio platforms, professional directories,
public projects and communities. Recommend:

- One name form, used everywhere.
- One role line, adjusted only for platform length.
- The canonical bio (below), adapted per platform.
- A link to the canonical site from every profile that allows one, and links
  from the site's about page to the profiles that represent the person.
- Complete profiles: role, location if relevant, photo, links, featured work.
- Retiring or updating stale profiles the owner still controls.

Provide the text; the owner makes the changes. Never sign in to, create or
edit a third-party profile without explicit authorization for that profile.

## The canonical bio

Write it only from facts the owner confirmed or the site states:

- **One line** (role and focus): for headlines and meta descriptions.
- **Short** (about 50 words): for profiles and bylines.
- **Long** (about 150 words): for the about page and speaker pages.

Name, role, focus areas, notable work with verifiable references, location
if relevant, and what they want to be contacted for. No unverifiable
superlatives, no invented numbers ("helped 100+ companies") unless the owner
supplies and stands behind them.

## Brand pages on the site

Evaluate whether the site needs each; create only what has real content:

| Page | Worth it when | Essentials |
| --- | --- | --- |
| About | Always, for a personal site | Full name in title and `h1`, a clear role statement, photo with descriptive alt, the long bio, links to profiles, contact route |
| Projects or portfolio | The owner has work to show | One page per substantial project: what, why, their role, outcome, links |
| Writing or publications | They write | A list with dates and where each appeared, linking to originals |
| Talks or teaching | They speak or teach | Event, date, topic, slides or video links |
| Media or press | There is coverage or requests | Approved bios, photos, coverage links |
| Author pages | Several authors, or articles need a byline target | Bio, links, list of articles |

Do not create near-empty pages, or several pages that target the same name
query, to fill results. That is a doorway pattern, and it fails the reader.

Structured data for these pages: `references/structured-data.md` (Person,
often as the `mainEntity` of a `ProfilePage` on the about page; `author`
on articles; `WebSite` with the site name on the homepage).

## Entity signals

Search engines connect a name to a person through consistent, corroborated
facts across the web. Strengthen them legitimately:

- Original publications, and bylines on reputable sites in the field.
- Interviews and podcast appearances that fit the owner's expertise.
- Open-source projects with clear authorship and links back.
- Talks, workshops, teaching, community contributions.
- Collaborations that are real and can be named.

A knowledge panel cannot be requested or bought. If one appears, the person
can verify themselves through Google and suggest corrections. Treat it as an
outcome, never a task.

## Reputation

When the first page holds inaccurate, outdated or damaging results:

- First, publish and promote accurate, useful owned and earned content.
  Never fabricate content to push results down.
- For outdated information on a page the owner does not control, draft a
  correction request for the owner to send to that site.
- For personal contact details or doxxing, point the owner to Google's
  personal-information removal process and the site owner. Legal questions
  go to a lawyer.
- Never create fake reviews, fake profiles, fake news or attack content.

## What it records

`brand.md`: the query set, dated snapshots with classified results, gaps,
the consistency matrix, the canonical bio once approved, owned properties,
and brand tasks linked by ID to `backlog.md`.

## Boundaries

- Third-party accounts and profiles: the owner acts, or authorizes each one.
- Outreach for interviews, guest posts or podcasts: drafts only, sent by the
  owner or with explicit authorization (`references/authority-building.md`).
- Other people with the same name: never researched beyond what the name
  search shows, never recorded in detail, never acted against.
