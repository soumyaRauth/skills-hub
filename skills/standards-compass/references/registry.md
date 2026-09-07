# The registry, and keeping it current

The registry is the part of this skill that ages. Everything else is method;
this is facts about the world, and the world revises its standards without
telling anyone.

## Layout

```
registry/
├── registry.yaml     what the registry is: categories, types, statuses,
│                     authority domains, required fields
├── controls.yaml     the normalized control model
└── <category>/*.yaml one file per standard
```

`registry.yaml` deliberately does **not** list the entries. Entries are
discovered by scanning the category directories, because an index that has to be
kept in sync eventually is not, and a stale index is worse than none.

## Adding a standard

One file. Nothing else changes — not the skill, not a mapping table, not a
build step.

```yaml
id: some-standard             # kebab-case, unique across the registry
name: Full descriptive name
identifier: "Official designation as cited"
version: "2.2"
authority: W3C                # must exist in registry.yaml authorities
type: technical-standard      # from registry.yaml types
category: accessibility       # must match the directory
status: current               # from registry.yaml statuses
official_url: https://...     # must be on one of the authority's domains
publication_date: "2023-10-05"
free_to_read: true
last_verified: "2026-09-07"
verification:
  method: authoritative-source   # or bundled-knowledge
  source: https://...            # required for authoritative-source
summary: >
  Two to four sentences, written from scratch. What it is, what it covers,
  what makes it different from its neighbours.
applies_when:
  - profile_fact
  - another_profile_fact
applicability_notes: >
  When this genuinely applies, and the traps — especially anything that looks
  applicable and is not.
assessment:
  repository_evidence: partial   # full | partial | limited | none
  automatable: [...]
  manual_only: [...]
  external_only: [...]
controls:
  - authorization               # ids from controls.yaml
claim_boundary: >
  What may and may not be said about a project on the basis of repository
  evidence. This field is not optional politeness — it is what keeps reports
  defensible.
```

Optional: `supersedes`, `superseded_by`, `related`, `notes`,
`not_indicated_when`.

`scripts/validate-registry.sh` checks all of it: unique ids, required fields,
enum membership, category matching its directory, ISO-8601 dates, official URLs
on the authority's own domains, control references that resolve, and
`verification.source` present whenever the method claims an authoritative source.

## Copyright

Many standards are copyrighted and sold. **Do not copy standard text into this
repository.** Not clauses, not requirement text, not control descriptions, not
tables.

What belongs here: the name, the identifier, the version, the official source,
what it is for, when it applies, how much of it a repository can speak to, and
concise summaries written from scratch. Requirement identifiers may be cited
where they are public and citing them is normal practice — an ASVS chapter, an
API Top 10 entry, a NIST CSF outcome. Link to the authority for the text itself.

## Status and version discipline

Every entry's `status` says whether the named version is `current`,
`superseded`, `withdrawn`, `draft`, `historical`, or `unknown`. Never assess
against a superseded edition silently.

When a user names a version:

> ISO/IEC/IEEE 12207:2017 is the edition this registry records as current, and
> ISO lists a further edition whose publication status I have not confirmed. I
> can assess against either — the 2017 edition by default, or the newer one if
> your organization is contractually aligned to it. Which do you want?

Never substitute a version without saying so.

## Reassessing against a new edition

When a standard the project was assessed against publishes a new version, the
question is not "redo the audit" — it is what actually changed for this project.

```markdown
Reassessment — OWASP ASVS

Previously assessed  4.0.3 (2026-03-11)
Now assessing        5.0.0

Newly relevant here
  - <the requirement areas the new edition adds that this project touches>

No longer applicable
  - <requirements the new edition drops or reframes>

Findings whose status changes
  STD-009  PARTIAL → PASS   the new edition's phrasing is satisfied by the
                            fix made in April
  STD-017  PASS → PARTIAL   the new edition expects something the old one did
                            not; this is a change in the standard, not a
                            regression in the code

Unchanged  11 findings
```

The `STD-017` row carries the distinction that matters: a status that moved
because the standard moved is **not** a regression, and labelling it as one
implies the team broke something they did not touch. Say which kind of change it
is, every time.

## Currentness

Two fields carry the honesty:

- `last_verified` — the date the entry was last checked.
- `verification.method` — `authoritative-source` (checked against the
  authority's own site, with the URL) or `bundled-knowledge` (carried from
  training data, unverified).

Any report leaning on the registry says which. A `bundled-knowledge` entry is
usable; it is just weaker evidence, and a reader deserves to know that before
quoting a version number in a customer questionnaire.

## When to go to the web

Not for every request. Use authoritative sources when:

- the current version affects the conclusion,
- the entry is `bundled-knowledge` and the answer matters,
- `last_verified` is old relative to how fast that standard moves,
- regulatory status or a deadline is in question,
- the user explicitly asks what is current.

Authoritative means the body that publishes it: iso.org, w3.org, etsi.org,
nist.gov and csrc.nist.gov, owasp.org, pcisecuritystandards.org,
eur-lex.europa.eu and other official EU sources, official government and
regulator domains. `registry.yaml` maps each authority to its domains, and the
validator enforces it for `official_url`.

**Search for the standard, never for the project.** A web query is a request to
a third party. The version of WCAG, the status of an ISO edition, an effective
date — those are public facts, and looking them up is fine. The repository's code,
architecture, data model, customer names, dependency list or findings are not
public facts, and none of them belongs in a query, a prompt to an external
service, or an uploaded file. If a lookup cannot be phrased without describing
the project, do it from the bundled registry instead and say the version is
unverified.

Secondary sources — vendor guides, consultancy blogs, summaries — may help
explain a concept. They are never evidence of what a requirement says. A
requirement quoted from a blog is a rumour with a citation.

## Offline

The skill works with no network. When it does, say so once:

> Assessed against the bundled registry, last reviewed 2026-09-07. Version
> currentness has not been checked online; confirm before relying on this for
> anything contractual.

Never present the bundled registry as permanently current.

## Keeping it alive

Reviewing the registry is ordinary maintenance, not a special event. For each
entry: is the version still current, is the official URL still live, has the
status changed, does the summary still describe it accurately. Update
`last_verified` when you check, and only when you actually check — a refreshed
date on an unchecked entry is worse than an old one, because it converts an
honest doubt into a false assurance.
