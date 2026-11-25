# First-run discovery

Understand the site before changing anything. A first run that starts by
writing blog posts has skipped the only part that tells it which posts to
write.

## Contents

- Scope of a first run
- 1. Resolve the site
- 2. The site's identity
- 3. Search positioning
- 4. Inventory the site
- 5. The source code, if it is here
- 6. Data access
- 7. What to ask the owner
- 8. Outputs

## Scope of a first run

One session. Enough discovery to set direction and do the first valuable
thing, not every analysis this skill can perform. Deeper keyword, competitor
and content work becomes tasks in the backlog. The report says what was
deferred.

## 1. Resolve the site

- Fetch the URL the owner gave. Record the status, the redirect chain and the
  final URL (`scripts/seo_audit.py page <url>`).
- Request the variants: `http://` and `https://`, with and without `www.`.
  Each should end at one canonical origin with a single permanent redirect.
  Record what each one does.
- Fetch `/robots.txt` and the sitemap it names, or `/sitemap.xml`
  (`seo_audit.py robots` and `seo_audit.py sitemap`).
- Resolve the records folder and site key (`references/records.md`) and read
  any records that already exist. If they do, this is not a first run.

## 2. The site's identity

Answer from the site itself and say where each answer came from:

| Question | Where to look |
| --- | --- |
| What is this site, and what type (portfolio, business, product, SaaS, docs, blog, agency, community, educational)? | Homepage, navigation, about page, footer |
| Who owns it, and what is their professional identity? | About page, author bylines, footer, linked profiles |
| What does it offer? | Services, products, projects, pricing, calls to action |
| Who is it for? | Copy, examples, the problems pages address |
| Which countries and languages? | `lang` attributes, hreflang, currency, addresses, phone formats, content |
| What sets it apart, and what are its strongest assets? | Original projects, research, tools, publications, credentials stated on the site |
| What are the objectives? | Calls to action (hire me, sign up, buy, subscribe, read) |

Do not invent what the site does not say. An unanswered question becomes an
`ASSUMED` answer stated in `profile.md`, or one of the few questions for the
owner.

## 3. Search positioning

From the identity, write down:

- **What the site should be known for:** two to five areas of expertise or
  offering, in the words searchers use, not internal jargon.
- **Searches that should reach it:** the owner's name and its variants, the
  brand, products and projects by name, and the topics from the line above.
- **Realistic now versus later:** branded and name queries, project names and
  narrow long-tail topics are usually realistic for a new or small site;
  broad head terms dominated by large publishers are later or never. Judge
  this from what currently ranks (`references/keyword-research.md`), and label
  it `INFERRED`.
- **Out of scope:** queries that are irrelevant, or whose searchers want
  something the site will never offer.

## 4. Inventory the site

- Crawl politely: `seo_audit.py crawl <url> --max-pages 200`. For larger sites
  crawl a sample and say so.
- Compare the crawl with the sitemap: pages in one and not the other,
  non-indexable pages in the sitemap, orphans.
- Read the important pages in full: homepage, about, the main offering or
  project pages, the best articles, contact.
- Record each relevant page in `content.md`: URL, title, type, topic,
  apparent intent, status and quality notes. Leave performance blank until
  data exists.
- Note existing structured data, metadata patterns, internal linking and
  navigation depth.

## 5. The source code, if it is here

Follow `references/implementation.md` to identify the framework, build,
deployment, and where titles, descriptions, canonicals, robots directives,
sitemaps and structured data come from. Record it in `profile.md`. Run the
build once to confirm the site builds before anything is changed, and record
the result.

If the site is live but its code is not here, changes become instructions or
patches for the owner, and the report says so.

## 6. Data access

Probe; never assume. Record each in `profile.md` as available, not available,
or unknown, and how it is reached:

- Web search tool, page fetcher, browser automation
- Google Search Console (an MCP server, an API credential the owner set up,
  or exports the owner can download)
- Google Analytics or another analytics tool
- Bing Webmaster Tools
- Keyword or backlink tools the owner already has (record the tool name; do
  not suggest buying one)
- PageSpeed Insights or Lighthouse, for performance

When Search Console is not available, follow "Working without Search
Console" in `references/analytics.md` and add a task to connect it.

## 7. What to ask the owner

Ask in one short message, only what changes the work and cannot be found:

- The name they want to be found by, and its common variants or
  misspellings, if the site does not make it clear.
- Their main goal for the site (clients, a job, readers, product sign-ups,
  speaking), if the site does not make it clear.
- Their target countries or languages, if the content does not decide it.

Everything else: infer, label `ASSUMED`, and continue. Never block a first
run waiting for answers; do the work that does not depend on them.

## 8. Outputs

- `profile.md`, complete, with assumptions labelled
- `baselines/<date>.md`, from `templates/baseline.md`
- `content.md` with the important pages
- `brand.md` with the first name-search snapshot, when a person or brand is
  central to the site (`references/personal-brand.md`)
- `strategy.md` (`references/strategy.md`) and a scored `backlog.md` with a
  `Now` list
- `history.md` with the first entry
- The first safe task done and validated, if the source is here
- The initial report (`references/reporting.md`)
