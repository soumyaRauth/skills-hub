# Worked example — Hindi (hi-IN)

A B2B logistics dashboard, English source, no Hindi locale yet. The user asks:

> Localize the shipment tracking module to Hindi.

Illustrative only: conventions differ by audience, region and product register.

## The contrast with Bengali

The same reasoning method gives a different answer per language. For an everyday
physical object, Hindi commonly uses a native word in ordinary speech, so the
transliteration that reads naturally in one language's UI would read oddly here.
For software vocabulary that arrived with the technology, borrowed forms are
common in both.

```
Chair       Bengali example → borrowed form is the everyday word
            Hindi example   → an ordinary native word is the everyday word

Password    both → borrowed form is common in software
```

Never port a strategy across languages because the terms look analogous. Decide
per language, per term, against that ecosystem's actual usage
(`../references/translation-strategy.md`).

## Strategy table for this module

| Source | Strategy | Target | Note |
| --- | --- | --- | --- |
| Settings | transliterate | सेटिंग्स | dominant in software |
| Password | transliterate | पासवर्ड | ditto |
| Download | transliterate + native verb | डाउनलोड करें | borrowed noun, native verb |
| Save | translate | सहेजें | native verb, ordinary register |
| Delete | translate | हटाएँ | native verb |
| Continue | translate | जारी रखें | native |
| Get Started | adapt | शुरू करें | not word-for-word |
| Shipment ID | preserve + translate | शिपमेंट ID | identifier stays Latin |
| API, CSV | preserve | unchanged | identifiers |

Two decisions recorded in the locale profile before any string was written:

- **Address form:** the polite second person, consistently, for a B2B product.
- **Digits:** Latin digits, as the source dashboard mixes them with tracking
  codes; recorded so it does not drift.

## The finding that needed a human

Hindi past-tense participles and many adjectives agree with the grammatical
gender of the noun they describe. English UI strings carry no such information,
and it cannot always be recovered at runtime.

```
REVIEW REQUIRED
  Key      toast.itemDeleted
  Source   "{{item}} deleted"
  Problem  The participle must agree with the grammatical gender of the noun
           substituted into {{item}} — and {{item}} is a runtime value that may
           be a shipment, a file, a note or an address, which do not share one
           gender.
  Options  a) split the key per object type, so each string is written whole
           b) reword to a construction that avoids agreement, e.g. a nominal
              phrase — verified with a native reviewer for tone
           c) pass the gender with the value, if the data model can supply it
  Chosen   (b) as a provisional value, flagged; (a) recommended to the team
  Confidence LOW — the source hides information the target requires
```

Guessing one gender here produces text that is wrong for roughly half the
runtime values, silently, forever. Reporting it costs one line.
See `../references/context-analysis.md`.

## Other findings

**Concatenation.** `"Shipment " + status + " at " + time` cannot be localized —
Hindi word order and postpositions do not survive assembly from English parts.
Reported as a source-level fix (a single ICU message), not patched in the
catalog.

**One key, two meanings.** `common.order` renders both a purchase order and a
sort order in this dashboard. Two different Hindi words are needed; the key must
be split. Reported, not resolved by compromise wording.

**Plurals.** This locale uses a two-category system in CLDR, so `_one` and
`_other` are sufficient here — but the count placeholder must appear in both
forms, and one draft string dropped it. See `../references/pluralization.md`.

**Formatting.** Amounts are grouped Western-style; the locale commonly groups
the leading digits in pairs and uses लाख and करोड़ in prose. Currency symbol is
hardcoded in three strings. Both reported for a formatter fix, not edited.

**UI fit.** Devanagari sits taller than Latin at the same font size; two table
rows use a fixed height with `overflow: hidden`, so diacritics may clip —
`POTENTIAL UI FIT ISSUE`, verification in-browser recommended
(`../references/ui-fit.md`).

## Report excerpt

```
LOCALIZATION COMPLETE
────────────────────────────────
Target        Hindi (hi-IN)
Files changed locales/hi/shipments.json  (new)

Added 84   Updated 0   Unchanged 0

Placeholder validation    PASS
Plural validation         PASS
Structure validation      PASS
Terminology consistency   PASS — 19 glossary entries established

HUMAN REVIEW RECOMMENDED  6
  toast.itemDeleted     — gender agreement with a runtime value
  common.order          — one key, two concepts; needs splitting
  status.inTransit      — two conventions in use for this term in the industry
  hero.cta              — adapted, not translated; tone check wanted
  table.eta             — abbreviation kept in Latin; confirm with users
  errors.rateLimited    — register of the apology line
```
