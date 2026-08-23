# Terminology and translation memory

Consistency is the difference between a product that feels localized and one
that feels like several translators took turns. It is also the cheapest quality
win available: it needs no linguistic judgement, only discipline.

## The glossary

One entry per product concept, not per English word:

```yaml
- source: Delete
  target: মুছে ফেলুন
  strategy: translate
  context: destructive action on a record
  confidence: high
  notes: "Remove-from-list uses a different verb; see `Remove`."
```

Fields and why each exists:

| Field | Purpose |
| --- | --- |
| `source` | the concept as the source locale names it |
| `target` | the chosen target term |
| `strategy` | translate / transliterate / preserve / adapt |
| `context` | the UI role and domain that make this the right term |
| `confidence` | how strongly the evidence supports it (`confidence.md`) |
| `notes` | rejected alternatives, near-miss concepts, review notes |

Start from `../templates/glossary.yml`. If the project already ships a glossary
or style guide, it outranks anything you would infer.

## Harvesting what already exists

Before proposing terminology, extract it. Search the target catalog for the
recurring product nouns and verbs and count the forms in use:

```bash
grep -o '"[^"]*"' locales/bn/common.json | sort | uniq -c | sort -rn | head -40
```

Then, for each concept that matters, list every target term found and where.
Two target terms for one concept is a **TERMINOLOGY INCONSISTENCY** finding —
report it with both counts and pick one, rather than adding a third.

## Which term wins

1. **The project's own established term**, when it is not actually wrong.
   Twenty occurrences of an acceptable term beat one occurrence of a better one.
2. **The term the platform or ecosystem uses**, when the project has none.
3. **Your recommendation**, with confidence and reasoning, when neither exists.

Overriding an established term is a project-wide change: propose it once, list
every affected key, and only apply it if the user agrees. Never leave the app
half-migrated between two terms — that is strictly worse than either.

## Translation memory

Existing high-confidence translations are memory to reuse. Reuse when the
concept, the UI role and the grammatical role all match.

Do **not** reuse when:

- the grammatical role differs — a button label, a heading and a sentence
  fragment may need different forms of the same verb,
- the string is embedded in a sentence and needs agreement or a case ending,
- the earlier translation is itself flagged as unnatural or literal,
- the surrounding tone differs (error vs. marketing),
- the same English word covers two different concepts in this product.

Reuse is a decision too. Copying a string because it matched textually is how
"Save" ends up as "rescue" in the payment flow.

## One English word, several concepts

English UI copy collapses distinctions that many languages keep. When one source
word maps to more than one target term, split the glossary entry by context and
say so:

```yaml
- source: Remove
  target: সরান
  context: remove a member from a team (reversible)
- source: Remove
  target: মুছে ফেলুন
  context: permanently delete an uploaded file
```

If the catalog uses one key for both — `common.remove` reused everywhere — that
is a finding for the developers: the key needs splitting before the language can
be correct. Report it; do not fix it by changing keys unless asked.

## Terms that must not drift

Keep these stable across the whole app and call out any variation:

- product, feature and plan names,
- the core domain nouns (order, invoice, workspace, member, project),
- the verb set on primary actions (save, delete, cancel, submit, share),
- navigation labels and section titles,
- the transliteration spelling of a borrowed term — one spelling, everywhere.
