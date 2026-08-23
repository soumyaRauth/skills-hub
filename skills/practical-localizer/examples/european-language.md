# Worked example — a European language pair (de-DE, fr-FR, es-ES)

A SaaS billing console, English source, three European locales at different
stages. The user asks:

> Review the German, French and Spanish localizations before the EU launch.

Illustrative only. Every convention below varies by product, register and
region — several of them vary *within* the same language.

European languages are the easy case in the popular imagination and are not:
they add grammatical gender, formal and informal address, agreement, and
punctuation systems that differ from English in ways a spell-checker will not
catch.

## German — compounds, address form, and expansion

**Address form.** The formal and informal second person are different words with
different verb forms, and the choice runs through the entire product. Evidence
from the source copy — contractions, humour, imperative style — plus the
audience decides it. This is a B2B billing console, so the formal form was
recorded in the locale profile. The finding:

```
#1  Register inconsistency
  Keys       onboarding.step1, onboarding.step3, billing.updateCard
  Problem    two keys address the user informally, the rest formally
  Effect     the flow switches register mid-way — highly noticeable
  Fix        align to the formal form recorded in the locale profile
  Confidence HIGH — mechanical once the profile decision exists
```

**Expansion and compounds.** German strings are frequently longer than English,
and compound nouns form a single unbreakable word with no wrap opportunity:

```
POTENTIAL UI FIT ISSUE
  Key       nav.accountSettings
  Evidence  rendered in a sidebar with a fixed width and `truncate`
            (components/SideNav.tsx); the target is a single compound noun
  Options   a shorter established alternative · allow two lines · verify visually
  Confidence Medium — length measured, rendering not observed
```

**Nouns are capitalized**, which makes a lowercase noun in the middle of a
target string a reliable signal of a hasty edit.

## French — agreement, spacing, and the singular zero

**Zero is singular.** French takes the singular form with zero, where English
takes the plural. In CLDR terms the locale's `one` category covers it, so a
catalog authored by mirroring the English `one`/`other` split is wrong at
exactly the count an empty state displays:

```
#2  Pluralization
  Key       invoices.count
  Source    {count, plural, one {# invoice} other {# invoices}}
  Current   the target's branches were filled by translating the English
            branches one-to-one, so zero renders the plural form
  Fix       author each branch from the locale's own rules, and verify the
            empty state at count = 0
  Confidence HIGH
```

**Gender agreement.** Adjectives and past participles agree with the noun. A
generic string like "Selected" or "None" that renders next to several different
nouns cannot agree with all of them:

```
REVIEW REQUIRED
  Key      filters.none
  Problem  the target adjective must agree with the noun it qualifies; this key
           renders next to three nouns of differing gender
  Options  split the key per filter type · reword to a form that avoids
           agreement
  Confidence LOW — the source hides information the target requires
```

**Typographic spacing.** French typography places a narrow no-break space before
certain punctuation marks, and conventions differ between France and other
French-speaking regions. A catalog mixing plain spaces, no spaces and non-breaking
spaces before the same mark is inconsistent whichever convention is chosen:

```
#3  Typography
  Scope     23 strings containing : ; ! ?
  Problem   three different spacing treatments in use across the catalog
  Fix       settle the convention for the target region, then apply uniformly
  Note      use the non-breaking form, so the mark cannot wrap to the next line
  Confidence MEDIUM — convention depends on the region, consistency does not
```

Quotation marks follow the locale's own convention rather than the English
pair; check that quotes inside strings were converted rather than copied.

## Spanish — regional variation and inverted marks

**Which Spanish.** The region matters for real product vocabulary: common
settings and computing terms differ between Spain and Latin American markets,
and picking one without saying so leaves the catalog mixed. This project targets
Spain, so the profile records that — and one finding follows directly:

```
#4  Terminology consistency
  Concept    settings
  Found      two different target terms across the catalog, split roughly by
             when the keys were added
  Fix        adopt the term used by the recorded target region; migrate all
             occurrences in one change
  Confidence HIGH — internal inconsistency is observable regardless of which
             term is preferred
```

**Inverted punctuation.** Questions and exclamations open with an inverted mark.
A target string that opens without one was translated, not localized:

```
#5  Typography
  Keys      6 interrogative strings missing the opening mark
  Confidence HIGH — mechanical
```

**Address form and gender.** As in German, the formal and informal second person
must be chosen once and held. Gendered adjectives raise the same agreement
problem as French; where the referent is the user and the app does not know the
user's gender, prefer constructions that avoid agreement rather than inventing a
default, and record the decision.

## Cross-locale mechanics

```
Numbers      decimal and grouping separators differ from the source convention
             in all three locales; two catalogs contain hardcoded amounts
Currency     symbol placement differs by locale and is hardcoded before the
             amount in 5 strings — move to a formatter
Dates        one shared component formats with a literal English pattern
Sorting      the customer list sorts by code point; locale-aware collation is
             needed for these alphabets
Address form recorded per locale in the locale profile, so it stops being
             re-decided per string
```

See `../references/locale-formatting.md`. None of these were edited — they live
in application code.

## What this example does not claim

- That the formal address form is right for every product in these languages.
  Consumer products frequently choose the informal one.
- That one regional convention is "standard" and another is not.
- That agreement problems always have a graceful workaround. Sometimes the
  honest answer is that the key must be split, and that is a code change.
