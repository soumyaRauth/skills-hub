# Worked example — Arabic (ar)

A file-sharing web app, English source, Arabic locale being added. The user
asks:

> Analyze this app for Arabic localization.

ANALYZE mode: nothing is written. Illustrative only — Arabic usage varies
considerably by region and register, and the region should be settled in Phase 1.

## The two hard parts

Arabic exercises two mechanisms that most localization pipelines get wrong:
a six-category plural system, and right-to-left rendering that string
translation alone does not deliver.

## Plurals

This locale uses the full CLDR category set — `zero`, `one`, `two`, `few`,
`many`, `other` — and the categories are selected by rules, not by intuition
about the names. A catalog carrying only the English pair renders the wrong form
for most counts.

```
BLOCKING TECHNICAL ISSUE   files.count
  Mechanism   i18next suffixed keys
  Source      files_one, files_other
  Target      files_one, files_other        ← copied from the source shape
  Required    the categories this locale's CLDR rules select — the target file
              needs an entry for each, not two
  Effect      counts that select a missing category fall back and read wrongly
  Fix         author one form per required category, with the count placeholder
              present in every one
```

The same defect in ICU form is a `{count, plural, …}` block with only `one` and
`other` branches. Note also that the dual is a real grammatical number here, so
"two" is not a special case of "few". See `../references/pluralization.md`.

## Direction

Translating every string does not make the app RTL. From the code:

```
RTL READINESS
  dir attribute      hardcoded dir="ltr" in the root layout — the whole app
                     renders left-to-right regardless of locale
  Physical CSS       31 rules use margin-left / padding-right / text-align:left
                     on user-facing components; logical properties would work
                     in both directions
  Directional icons  ArrowBack, ChevronRight, Stepper and the send button use a
                     fixed rotation and will point the wrong way
  Non-mirroring      the clock and logo marks must NOT flip — flag before any
                     blanket transform is applied
  Direction wording  4 strings say "on the left" / "on the right"; these need
                     rewording, not mirroring
  Mixed content      filenames and URLs are interpolated into sentences with no
                     bidi isolation, so trailing punctuation will drift
  Fonts              the bundled family has no coverage for this script;
                     fallback rendering will be inconsistent

  POTENTIAL LAYOUT ISSUE — string localization will not resolve any of these.
  Recommend a direction pass before shipping the locale.
```

None of it was changed: layout and CSS are application source
(`../references/rtl.md`).

## A terminology trap worth naming

Some source concepts map to target terms that are themselves ambiguous or
contested across products and regions. In this app, upload and download appear
in the same screen, and the candidate terms overlap in common usage — one of
them is used by different products for both directions.

```
TERMINOLOGY — REVIEW REQUIRED
  Concepts   upload / download, rendered side by side in the transfer panel
  Risk       a term in wide use for one direction is used by some products for
             the other; choosing it for both, or choosing the pair
             inconsistently, makes the panel actively confusing
  Action     pick an unambiguous pair, apply it to all 11 related keys, and
             record it in the glossary with the rejected alternatives
  Confidence LOW without a native reviewer or a target-locale product to check
             against — surfaced rather than decided
```

Ambiguity that would confuse a user is worth a blocking review item even when
the string is grammatically fine.

## Other observations

**Definiteness and agreement.** Adjectives and the definite article interact,
so a fragment translated in isolation may not compose with the noun it is
inserted next to. Strings assembled from parts are reported as a source fix.

**Digits.** Arabic-script and Latin digits are both in use, with regional
variation. The choice is a product decision; record it in the locale profile and
apply it via a formatter, never per string.

**Calendars and dates.** Some audiences expect a non-Gregorian calendar, or both
side by side. Ask; do not assume from the language alone.

**UI fit.** Arabic strings here are often somewhat longer than the English, and
the script needs more vertical room at the same font size — two fixed-height
rows are at risk (`../references/ui-fit.md`).

## Report tail

```
RECOMMENDED STRATEGY
  1. Fix the plural category coverage — blocking, mechanical, no judgement
  2. Settle direction support before translating further: dir attribute,
     logical properties, icon policy
  3. Resolve the transfer-panel terminology pair with a native reviewer
  4. Establish digits and calendar conventions in the locale profile
  5. Then localize, namespace by namespace, starting with the auth flow

  Not verified: rendering. No browser check was run; every layout finding is
  read from source and should be confirmed visually.
```
