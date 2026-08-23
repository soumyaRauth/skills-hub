# Worked example — Bengali (bn-BD)

A consumer marketplace app, English source, existing partial Bengali locale of
uneven quality. The user asks:

> Review the Bengali localization for naturalness and consistency.

The examples below are **illustrations of the method**, drawn from this
fictional project. Terminology varies by region, audience and product; verify
against the real project before adopting anything here as a rule.

## Why Bengali is a good demonstration

Bengali software vocabulary mixes two registers. A large part of everyday
technology vocabulary is borrowed and written in Bengali script, while ordinary
verbs and nouns stay native. A dictionary translates both sides into the native
register, which is exactly what makes a Bengali UI feel wrong: correct words, in
a register nobody uses for this kind of product.

```
English:   Chair
Literal:   কেদারা      ← dictionary-valid, reads as formal/literary
Practical: চেয়ার        ← the borrowed form most people use in speech
```

Neither is "the translation". The question is which register this product's
users expect for this concept — and the answer is per-term, not per-language.
Note that the same reasoning gives a different answer in Hindi, where an
ordinary native word for the same object is in everyday use
(see `hindi.md`).

## Findings, abbreviated

### #1 — Naturalness / terminology

```
Key          catalog.category.chair
Source       Chair
Current      কেদারা
Recommended  চেয়ার
Category     Naturalness / terminology
Reason       Dictionary-valid but belongs to a literary register; the borrowed
             form is what this catalog's other entries already use — সোফা and
             টেবিল appear in sibling keys, so the current value is also
             internally inconsistent.
Confidence   HIGH   (project-internal evidence, not a claim about all speakers)
```

The confidence is HIGH because of the sibling keys, not because of a general
statement about Bengali.

### #2 — BLOCKING TECHNICAL

```
Key       greeting.hello
Source    "Hello, {{name}}"
Current   "হ্যালো"
Effect    the interpolation is gone; the user's name never renders
Fix       "হ্যালো, {{name}}" — placeholder restored verbatim
Category  Placeholder
Confidence HIGH (mechanical)
```

Placeholder loss is not a style question. It ships as a visible defect and no
test catches it. See `../references/pluralization.md` for the same class of
failure in plural wrappers.

### #3 — Terminology inconsistency

```
Concept    sign in
Found      লগইন     — 18 occurrences (auth flow, nav, onboarding)
           প্রবেশ করুন — 2 occurrences (one settings screen, one error)
Recommend  লগইন everywhere; it is this project's established term and the two
           outliers were added later
Confidence HIGH
```

The rule from `../references/terminology.md` applies: the established term wins
unless it is actually wrong. Adding a third, better-sounding synonym would be
the worst outcome.

### #4 — Context, not vocabulary

```
Key       team.remove
Source    Remove
Context   <TeamMemberRow> action, handler removeMember(member) — takes a person
          off a team; the member is not deleted and can be re-invited
Current   মুছে ফেলুন     ← "erase / delete"
Recommended  সরিয়ে দিন   ← "take away / remove"
Reason    The current wording describes permanent deletion. Bengali uses
          different verbs for removing something from a list and destroying it;
          English does not, so the string alone cannot be translated correctly.
Confidence HIGH — the handler name and the surrounding UI resolve the meaning
```

This is the finding a spreadsheet-based translation workflow structurally cannot
produce. See `../references/context-analysis.md`.

### #5 — Register on destructive actions

```
Key       account.delete.confirm
Source    Delete account
Current   অ্যাকাউন্ট ডিলিট
Recommended  অ্যাকাউন্ট মুছে ফেলুন
Reason    The rest of this product uses polite imperative verb forms (…করুন)
          for actions. The current value is a bare borrowed noun phrase, which
          reads as abrupt for an irreversible action and breaks the pattern used
          by every other primary button in the catalog.
Confidence MEDIUM — register judgement, supported by in-project consistency
```

### #6 — Strategy per term, not per category

Technical vocabulary does not get one blanket rule:

| Source | Strategy | Target | Why |
| --- | --- | --- | --- |
| Password | transliterate | পাসওয়ার্ড | borrowed form dominates in software |
| Settings | transliterate | সেটিংস | ditto; already used across this project |
| Download | transliterate + native verb | ডাউনলোড করুন | borrowed noun, native verb ending |
| Delete | translate | মুছে ফেলুন | ordinary native verb, in everyday use |
| Cancel (dismiss) | translate | বাতিল | ditto |
| API, JSON, URL | preserve | unchanged | identifiers; translating obscures them |
| Get Started | adapt | শুরু করুন | word-for-word would be unidiomatic |

The mix is the point. "Transliterate all technical terms" and "translate
everything" both produce a worse UI than deciding term by term.

## Locale mechanics reported, not changed

```
Plural categories   this locale uses a two-category system; the i18next catalog
                    has _one and _other for every counted string — OK
Numerals            catalog mixes Bengali and Latin digits across screens;
                    pick one convention with the product owner and apply it
                    through Intl rather than in strings
Grouping            large amounts are grouped Western-style in three places;
                    the locale commonly groups in the Indian style with লাখ and
                    কোটি — verify the intended convention
Currency            ৳ hardcoded inside two catalog strings; should come from a
                    formatter so amounts and symbols stay consistent
Dates               one string contains the literal pattern MM/DD/YYYY
UI fit              nav.notifications target is materially longer than the
                    source in a fixed-width tab — POTENTIAL UI FIT ISSUE
```

None of these were edited. Formatting lives in application code; changing it is
a source change, not a localization change
(`../references/locale-formatting.md`).

## What this example does not claim

- That চেয়ার is correct for every Bengali product, or for every audience.
- That borrowed forms are always more natural — they are not; the pattern varies
  strongly by term.
- That bn-BD and bn-IN conventions are interchangeable. They are not always, and
  the region should be established in Phase 1.
