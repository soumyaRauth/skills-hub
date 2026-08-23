# Reviewing an existing localization

REVIEW mode inspects translations that already exist and reports what is wrong
with them. It changes nothing unless the user asks for the fixes to be applied.

## Order of passes

Run the cheap, mechanical passes first — they find defects that no amount of
linguistic judgement would catch, and they are unarguable.

**1. Coverage.** Which keys exist in the source and not in the target; which
exist in the target and not the source (stale); which are present but identical
to the source string (often untranslated rather than deliberately preserved).

**2. Technical integrity.** Placeholder sets, ICU syntax, plural categories,
HTML and Markdown balance, escapes, file validity. Every mismatch is a
**BLOCKING TECHNICAL ISSUE** — the app renders wrongly regardless of language
quality. See `pluralization.md`.

**3. Terminology consistency.** For each recurring product concept, list every
target term in use with its occurrence count. More than one is a finding.
See `terminology.md`.

**4. Register and tone.** Does the formality of address stay constant across a
flow? Do errors and destructive confirmations sit at the right level? Does
marketing copy read like marketing?

**5. Naturalness.** The judgement pass, string by string, for the strings that
matter most: primary actions, navigation, empty states, errors, onboarding.

**6. Locale mechanics.** Dates, numbers, currency, direction, UI fit —
see `locale-formatting.md`, `rtl.md`, `ui-fit.md`.

## Naturalness signals

Suspect a literal translation when:

- the target sentence follows English word order where the language prefers
  another,
- an English noun stack has been rendered as a chain of nouns,
- a preposition maps one-to-one from English,
- a dictionary-formal or literary word appears in a UI context where the
  everyday or borrowed form is what products use,
- a technical term has been translated into a coinage no one says out loud,
- the polite verb ending appears on a two-word button in a product that
  otherwise uses bare forms,
- articles, auxiliaries or a subject pronoun were carried over from English
  where the target language would omit them,
- the string is grammatically fine but says nothing a user would expect there.

Also suspect *over*-localization: brand names translated, identifiers
translated, or an English term replaced by a native coinage that the product's
audience would not recognise.

## Writing a finding

One finding per issue, highest confidence first, each with a recommendation
someone can act on without asking a follow-up question:

```
#4
  Key          settings.security.password
  Source       Password
  Current      <current target string>
  Recommended  <recommended target string>
  Category     Terminology consistency
  Reason       The recommended form appears in 14 other keys in this catalog,
               including the login flow; the current form appears only here.
  Confidence   HIGH
  Fix          single key; no placeholder or plural impact
```

Include, at the top: what was reviewed (which files, how many strings, which
passes ran), what was not reviewed, and the counts per severity — actual counts,
not estimates.

## Severity

| Level | Meaning |
| --- | --- |
| **BLOCKING TECHNICAL** | Placeholder, ICU, plural or structure defect. The app misrenders. |
| **HIGH** | Wrong meaning, wrong term for the context, inconsistency in a core term, tone that misleads about a destructive action. |
| **MEDIUM** | Understandable but literal or stiff; secondary inconsistency; formatting that looks foreign. |
| **LOW** | Preference-level polish, where the current wording is defensible. |

Do not inflate. A reviewer who marks stylistic preferences as HIGH trains the
team to ignore the report, and the placeholder defect goes out with it.

## What review must not do

- Do not edit files. Recommend, and offer to apply.
- Do not rewrite acceptable translations to match personal preference — a
  finding needs a reason beyond "I would have said it differently".
- Do not introduce a third term for a concept that already has two.
- Do not claim the review was exhaustive if it sampled. Say what was sampled and
  how it was chosen.
