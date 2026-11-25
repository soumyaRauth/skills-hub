# Example: a name that does not surface

The owner of the portfolio fixture, after the first run. No Search Console
yet; a web search tool is available.

## Contents

- The request
- Query set and snapshots
- Classification and gaps
- Identity consistency
- Tasks
- A tactic it declines
- The report

## The request

```
/seo-growth personal-brand
When people google my name they find musicians, not me.
```

## Query set and snapshots

From facts on the site and in `profile.md`, not guesses:

`noor haldar` · `noor haldar data engineer` · `noor haldar airflow` ·
`noor haldar pipeline-lint` · `noor haldar dhaka` · `noor h data engineer`
(the old footer form)

Each query is run once with the web search tool and stored in
`data/serp-2026-11-25.md` with the tool, the date, and "location and device
unknown". The owner is also given the list to run in a private window on
their phone, because what they see is what a client in their city sees.

## Classification and gaps

| Query | What the snapshot shows (first 10) |
| --- | --- |
| noor haldar | `DIFFERENT-PERSON` ×3 (musicians, a teacher) at 1–3, GitHub profile (`OWNED-PROFILE`) at 4, the site absent |
| noor haldar data engineer | GitHub at 1, LinkedIn at 2, the site absent |
| noor haldar airflow | the pipeline-lint repository at 1, the docs site at 2 |
| noor haldar pipeline-lint | the repository at 1, the docs site at 2, the site's project page absent |

Findings, labelled:

- The bare name is shared with more established people. Holding position 1
  for it may not be realistic soon (`INFERRED`). The realistic target is
  name + profession and name + Airflow, where owned results already lead.
  `strategy.md` is revised to say so, with the reason.
- The site is absent everywhere. The about page carries `noindex`
  (`VERIFIED`), and the homepage only recently started naming the owner
  (SEO-002).
- The talk, the article and the project page never appear for name
  queries: nothing links them to the name except a byline.

## Identity consistency

The owner pastes their GitHub and LinkedIn headlines, because the skill does
not sign in to third-party sites:

| Property | Name as shown | Role | Links to site |
| --- | --- | --- | --- |
| Website | Noor Haldar | data engineer | — |
| GitHub | noorhaldar-example, no display name | none | no |
| LinkedIn | Noor H. | "Engineer at a stealth startup" | no |
| pipeline-lint docs | Noor Haldar | maintainer | yes |

Recommendations, each with the exact text to paste:

- GitHub: display name "Noor Haldar", bio from the approved one-line bio,
  website field `https://noorhaldar.example`.
- LinkedIn: full name, a headline matching the site ("Data engineer · Apache
  Airflow reliability"), and the website link.
- A canonical bio in three lengths, drafted from the about page only, marked
  "draft" in `brand.md` until the owner approves it.

## Tasks

| Task | Score | Note |
| --- | --- | --- |
| SEO-003 Remove `noindex` from the about page | 125 | Still awaiting approval; the whole name strategy depends on it |
| SEO-014 GitHub and LinkedIn: name, headline, link to the site | 5·4·5 ÷ 1 = 100 | The owner makes the changes |
| SEO-011 Person structured data with `sameAs` to both profiles | 45 | `sameAs` only after the profiles show the same name |
| SEO-015 Talks page: slides and the meetup's own event link | 3·3·4 ÷ 2 = 18 | Earned signal, if the meetup lists speakers |
| AUTH-001 Ask the meetup organizers to link the talk to the site | 18 | Draft only; the owner sends it |

## A tactic it declines

The owner asks: *"Could we make a few extra profiles on directory sites and
buy some links to push the musicians down?"*

```
I won't do that one. Bought links and profiles made only for links break Google's
link spam policies: at best they are ignored, at worst the site is demoted. It would
also put pages about you that you don't really maintain on the first page.

What works for the same goal: SEO-014 (your GitHub and LinkedIn pointing to your
site under one name), the talk listed by the meetup itself, and a byline on a
respected data engineering publication (I can find three that accept practitioners).
```

The request and the decision go in `history.md`, so the next session does not
re-open it.

## The report

```
⚡ SEO Growth Engine — personal brand: name searches for Noor Haldar

The honest picture: other people share your name and hold the top results for it
alone. You already own the results for "noor haldar airflow" and
"noor haldar data engineer". Your site appears for none of them yet.

Why: your about page is hidden from search (SEO-003, waiting on you), and your GitHub
and LinkedIn don't use your full name or link to your site, so nothing ties
"Noor Haldar" to noorhaldar.example.

Your part (10 minutes, text ready in brand.md): GitHub display name, bio and website;
LinkedIn name, headline and website.

Measure: I'll repeat the same searches with the same tool monthly. Search Console
(SEO-012) would show what Google actually does with your name.
```
