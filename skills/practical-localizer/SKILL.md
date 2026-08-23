---
name: practical-localizer
description: Localize software applications into natural, context-aware target-language experiences rather than literal translations. Use when translating, reviewing, or analyzing application UI strings, locale files, terminology, pluralization, formatting, or language-specific product conventions.
---

# Practical Localizer

A technically correct translation is not necessarily a natural one. For every
string, answer the product question rather than the dictionary question:

> Not "what is the translated word?" but
> **"what would a real user of this language expect this product to say here?"**

The deliverable is a **localization decision** per meaningful string — strategy,
evidence, confidence — not a bilingual word list.

## Non-negotiable rules

1. **Context before translation.** Never translate an isolated string when the
   application can be inspected. A key, its call sites, its component, its
   neighbouring copy and its UI role all change the answer. See
   `references/context-analysis.md`.
2. **Never break the localization infrastructure.** Keys, nesting, placeholders,
   ICU expressions, HTML/Markdown, escapes and formatting tokens survive
   unchanged. A translation that loses `{{name}}` is a defect, not a style
   choice.
3. **Existing project terminology wins.** If the app already says `লগইন` in
   twenty places, a new, better-sounding synonym is an *inconsistency*, not an
   improvement. Change established terminology only deliberately, everywhere at
   once, and say so.
4. **Evidence and humility.** Never claim "native speakers say this". Say "this
   is the more common software convention" or "this is likely more natural in
   contemporary product usage", and name what the claim rests on. See
   `references/confidence.md`.
5. **Surface uncertainty instead of guessing.** Missing gender, unclear plural
   context, ambiguous source term, culturally loaded copy → mark
   `REVIEW REQUIRED` and keep going. Silence is the failure mode.
6. **Scope discipline.** Modify localization resources only, and only in
   LOCALIZE mode. Never rename variables, functions, routes, CSS classes,
   database columns or test identifiers. Never edit layout or CSS for RTL unless
   explicitly asked — report the need instead.
7. **No fabricated numbers.** Report counts you actually produced. "Several
   strings" beats an invented total.
8. **Quality over volume.** Forty strings that sound like the product beats four
   hundred that sound like a dictionary.

## Modes

Pick the mode from the request; state which one you are running before starting.

| Mode | Trigger | Writes files |
| --- | --- | --- |
| **ANALYZE** | "analyze this app for X localization", "are we ready to ship in X?" | No |
| **LOCALIZE** | "localize this app to X", "translate the missing strings" | Locale resources only |
| **REVIEW** | "review the X localization", "does this sound natural?" | No — recommendations only |

If the request is ambiguous, run ANALYZE and offer the other two. Never write
files in ANALYZE or REVIEW mode, even when the fix looks obvious; propose the
change and let the user ask.

## Workflow

Phases 1–6 run in every mode. Phase 7 is LOCALIZE-only. Phases 8–10 run whenever
there are translations to check — produced or pre-existing. Skip a phase
explicitly rather than inventing content for it.

### Phase 1 — Understand the request

Establish: source locale, target locale(s), region if it matters (`pt-BR` vs
`pt-PT`, `zh-Hans` vs `zh-Hant`), scope (whole app, one namespace, one file, the
diff), mode, and who the product's users are. Compress it into one
**LOCALIZATION STATEMENT**:

> Localize the checkout flow of a consumer e-commerce app from `en` to `bn-BD`,
> matching the existing informal-polite tone.

If something is ambiguous, choose the most reasonable reading, state it under
`INTERPRETATION`, and continue.

### Phase 2 — Localization reconnaissance

Learn how *this* application does localization before touching it. Read the
manifests, then find the actual mechanism: JSON/YAML catalogs, TS/JS message
objects, i18next, react-intl/FormatJS, next-intl, next-i18next, Laravel `lang/`,
gettext `.po`, Rails I18n, Flutter `.arb`, Android `strings.xml`, iOS
`Localizable.strings`, or something custom.

Never assume a framework or a directory. Look. When the repository contradicts
convention, the repository wins. See `references/localization-workflow.md`.

Record: message format, placeholder syntax, plural mechanism, namespace layout,
locale list, fallback locale, and how the app formats dates, numbers and money.

### Phase 3 — Build the language usage profile

Before substantial work, build a working profile of the target locale: script,
direction, formality and pronoun conventions, plural categories, how software
vocabulary is normally handled (translated / transliterated / kept in English),
date-time-number-currency conventions, punctuation and quotation marks, and the
terms that are known to be contested.

Treat it as a set of *factors*, not laws. Regional, generational and product
variation is real — never encode "language X always ...". Start from
`templates/locale-profile.yml`; a profile the user supplies overrides your
assumptions.

### Phase 4 — Harvest existing terminology

Existing high-confidence translations are translation memory. Extract the target
terms already used for recurring product concepts, count where they appear, and
note conflicts — two target terms for one concept is a finding.

Build a working glossary (`templates/glossary.yml`): source term, target term,
strategy, context, confidence, notes. Reuse it for the same concept in the same
grammatical role; do **not** reuse it blindly when the role or sentence
structure differs. See `references/terminology.md`.

### Phase 5 — Extract context per string

For each string that carries meaning, gather what the repository knows: the key
path and namespace, the component and function names around the call site,
nearby copy, whether it is a button / label / heading / status / error /
placeholder / tooltip / aria-label, the action it triggers, and any comments.

`t("remove")` inside `removeMember(member)` is "remove this member from the
team", not "delete permanently" — and many languages need that distinction where
English does not. Watch the classic ambiguous terms: Save, Remove, Delete,
Cancel, Submit, Apply, Back, Continue, Close, Open, Share, Account, User,
Profile, Project, Workspace. If context cannot resolve it, mark
`REVIEW REQUIRED`. See `references/context-analysis.md`.

### Phase 6 — Choose a strategy per term

Every meaningful term gets exactly one strategy, with a reason:

| Strategy | Use when | Illustration |
| --- | --- | --- |
| **TRANSLATE** | The language has a natural, current equivalent | Delete → a native verb form |
| **TRANSLITERATE** | The borrowed source word *is* the word users say | Chair → চেয়ার |
| **PRESERVE** | Translating would obscure meaning: identifiers, protocols, brands | API, JSON, HTTP, product names |
| **ADAPT** | Word-for-word would be unidiomatic — reword for the same intent | "Get Started" → the local call-to-action |

Choose from target language, UI context, existing project terminology,
audience and product tone — never from a blanket rule such as "keep all
technical terms in English" or "translate everything". The correct answer
differs *between* languages for the same word. See
`references/translation-strategy.md`.

### Phase 7 — Produce the localization (LOCALIZE only)

Before writing: run `git status`, note pre-existing modifications, confirm the
exact files in scope, and never touch anything else. Then, per string:
copy the key and structure verbatim, translate the human-readable text only,
preserve every placeholder and ICU construct character-for-character, and match
the product's tone (`references/translation-strategy.md` covers tone matching).

Prefer adding missing strings and fixing defects over rewriting acceptable
existing translations. Never commit, push, checkout, reset, or discard user
changes.

### Phase 8 — Technical validation

Mechanical, blocking, and run on every translation you produced or reviewed:

- **Placeholders:** the multiset of placeholders in source and target must
  match exactly — `{name}`, `{{name}}`, `${name}`, `%s`, `%1$s`, `:name`,
  `%{name}`, `<0>…</0>`. A mismatch is a **BLOCKING TECHNICAL ISSUE**. Do not
  silently "fix" one unless the correct form is unambiguous.
- **Plural forms:** every category the target locale requires is present, and no
  invented ones. Never fake pluralization with string concatenation when the
  framework provides a mechanism. See `references/pluralization.md`.
- **Structure:** keys, nesting and file syntax unchanged; valid JSON/YAML/XML/PHP;
  no lost escapes; no smart-quote substitution inside code or HTML.
- **Markup:** HTML tags, Markdown and rich-text components intact and balanced.

Report each as PASS or list the failures. Do not report PASS for a check you did
not perform.

### Phase 9 — Naturalness and consistency pass

Re-read the target text as a user of the product, not as a translator. For each
non-trivial string judge: literalness (does it mirror English word order for no
reason?), naturalness, product convention (does it sound like modern software?),
consistency with the glossary, contextual accuracy, audience fit and tone.
Anything below HIGH naturalness or HIGH context confidence goes on the review
list. See `references/review-methodology.md`.

### Phase 10 — Locale mechanics

Text is not the whole of localization. Check and report — do not silently
change:

- Date, time, number, decimal/thousands separators, currency placement and
  symbol, units, percentages. Prefer the platform's locale-aware mechanism
  (`Intl`, framework formatters) over hardcoded patterns.
  See `references/locale-formatting.md`.
- Direction for RTL targets: layout assumptions, directional icons,
  left/right wording, mixed LTR content, punctuation.
  See `references/rtl.md`.
- UI fit: expansion and contraction in buttons, nav, tabs, tables, badges and
  modal titles. Flag as `POTENTIAL UI FIT ISSUE` — never invent pixel
  measurements you cannot observe. See `references/ui-fit.md`.

## Report formats

Show a count only when you actually produced it. Omit sections that have no
content instead of padding them.

### ANALYZE

```
PRACTICAL LOCALIZER
────────────────────────────────
SOURCE       English (en)
TARGET       Bengali (bn-BD)
APPLICATION  <detected framework and localization mechanism>

LOCALIZATION INVENTORY
  Source strings          <n>
  Existing translations   <n>
  Missing                 <n>
  Naturalness concerns    <n>
  Terminology conflicts   <n>
  Technical issues        <n>

LANGUAGE OBSERVATIONS
  <profile factors that will drive decisions: script, formality, plural
   categories, how this product's domain vocabulary is normally handled>

TERMINOLOGY
  <established terms found in the project, plus the conflicts>

REVIEW REQUIRED
  <ambiguous source terms, missing gender/context, culturally loaded copy>

RECOMMENDED STRATEGY
  <what to do, in what order, and what needs a human>
```

### REVIEW

One numbered entry per finding, highest confidence first:

```
LOCALIZATION REVIEW
────────────────────────────────
Target        Bengali (bn-BD)
Reviewed      <n> strings
High-confidence issues    <n>
Medium-confidence issues  <n>
Technical issues          <n>

#1
  Key          furniture.chair
  Source       Chair
  Current      কেদারা
  Recommended  চেয়ার
  Category     Naturalness / terminology
  Reason       Dictionary-valid but reads as formal/literary for a modern app;
               the transliterated form is the more common product usage and
               matches সোফা / টেবিল already used in this file.
  Confidence   HIGH
```

Categories: naturalness · terminology consistency · tone · grammar ·
placeholder · pluralization · locale format · technical term · transliteration
consistency · should-stay-source · cultural fit · UI fit.

### LOCALIZE

```
LOCALIZATION COMPLETE
────────────────────────────────
Target        Bengali (bn-BD)
Files changed <list>
Added <n>   Updated <n>   Unchanged <n>

Placeholder validation    PASS / <failures>
Plural validation         PASS / <failures>
Structure validation      PASS / <failures>
Terminology consistency   PASS / <conflicts>

HUMAN REVIEW RECOMMENDED  <n>
  <key> — <why, and what the alternatives are>
```

Follow with the glossary entries you established, so the next run stays
consistent.

## Evidence and research

When web access is available you may check uncertain terminology against
reputable evidence: how major products localize the same UI concept, official
platform localization glossaries, language authorities, quality dictionaries,
and native-language technical writing. Prefer several converging sources over
one, and never treat a machine-translation site as authority.

When it is unavailable, rely on application context, existing translations,
the supplied glossary and the user's guidance — and say which. Never fabricate a
source, a corpus, or a usage statistic.

## References

- `references/localization-workflow.md` — end-to-end workflow, framework and file-format detection
- `references/translation-strategy.md` — translate / transliterate / preserve / adapt, and tone
- `references/terminology.md` — glossary building, translation memory, consistency
- `references/context-analysis.md` — extracting meaning from the codebase
- `references/pluralization.md` — plural categories per system and locale
- `references/locale-formatting.md` — dates, times, numbers, currency, units
- `references/rtl.md` — right-to-left considerations
- `references/ui-fit.md` — expansion, contraction and layout risk
- `references/confidence.md` — what evidence supports which claim
- `references/review-methodology.md` — reviewing an existing localization

Templates: `templates/glossary.yml` · `templates/locale-profile.yml` ·
`templates/review-report.md`

Worked language examples: `examples/bengali.md` · `examples/hindi.md` ·
`examples/japanese.md` · `examples/arabic.md` · `examples/european-language.md`
