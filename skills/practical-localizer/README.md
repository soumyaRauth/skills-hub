# Practical Localizer

**Make your application speak like a local product — not like a translated
document.**

Practical Localizer is an [Agent Skill](https://code.claude.com/docs/en/skills)
that turns application translation into a localization decision per string:
what the source actually means *here*, how the target language normally
expresses it in software, what the project already says, and what a real user
would expect to read.

```bash
npx skills add soumyaRauth/skills-hub --skill practical-localizer
```

---

## The problem

```
strings → send to a translator (human or machine) → paste back → ship
```

The output is usually *correct*. It is often not what the product should say.

```
English:   Chair
Literal:   a dictionary-valid, formal/literary word
Practical: the borrowed word people actually use for the object
```

Both are "the translation". Only one of them sounds like a modern app — and
which one that is differs by language, by product and by audience, which is
exactly why a dictionary cannot decide it.

The failure modes are consistent across projects:

- **Register drift.** Every word correct, all of them one register too formal,
  so the app reads like a government form.
- **Context loss.** `t("remove")` is translated as *erase permanently* when the
  handler is `removeMember(member)` — different verbs in most languages.
- **Terminology drift.** Three target words for one product concept, because
  each batch of strings was translated separately.
- **Silent technical breakage.** `"Hello, {{name}}"` comes back without the
  placeholder. Nothing fails. The name simply never renders.
- **Half-localized mechanics.** Text translated, dates, currency, plurals and
  direction untouched.
- **Wrong plural shape.** The English two-form split copied into a locale that
  needs one form, or six.

## The solution

```
source application → localization architecture → language usage profile
   → existing terminology → context extraction → translation strategy
   → natural localization → technical validation → consistency review
   → localized application
```

Every meaningful term gets one of four strategies, chosen from evidence:

| | Meaning |
| --- | --- |
| **TRANSLATE** | The language has a current, ordinary equivalent |
| **TRANSLITERATE** | The borrowed source word *is* the word users say |
| **PRESERVE** | Identifiers, protocols and brands, where translating destroys meaning |
| **ADAPT** | Reword for the same intent, because word-for-word would be unidiomatic |

And every non-trivial decision carries a confidence level, so the things a human
should look at are visible instead of buried.

---

## Three modes

| Mode | You ask | It does | Writes files |
| --- | --- | --- | --- |
| **ANALYZE** | *"Analyze this app for Bengali localization."* | Inventory, terminology map, technical issues, language observations, a recommended plan | No |
| **LOCALIZE** | *"Localize the checkout flow to Bengali."* | Context-aware localization of the locale resources, then validation | Locale resources only |
| **REVIEW** | *"Review the Bengali localization for naturalness."* | Findings with source, current, recommended, reason and confidence | No |

Review and analyze never modify anything. Localize modifies localization
resources and nothing else — never application logic, never variable or route
names, never CSS, never your git history.

## Example

```
You:  Review the Bengali localization for naturalness and consistency.

Agent: LOCALIZATION REVIEW
       ────────────────────────────────
       Target        Bengali (bn-BD)
       Reviewed      742 strings
       High-confidence issues    18
       Medium-confidence issues  27
       Technical issues          3

       #1
         Key          greeting.hello
         Source       "Hello, {{name}}"
         Current      "হ্যালো"
         Category     Placeholder — BLOCKING TECHNICAL ISSUE
         Effect       the interpolation was dropped; the name never renders
         Confidence   HIGH

       #2
         Key          team.remove
         Source       Remove
         Current      মুছে ফেলুন
         Recommended  সরিয়ে দিন
         Category     Context / terminology
         Reason       Rendered in <TeamMemberRow>, handler removeMember() —
                      the member is taken off the team, not deleted. Bengali
                      uses different verbs; English does not.
         Confidence   HIGH

       #3
         Concept      sign in
         Found        লগইন (18 occurrences) · প্রবেশ করুন (2 occurrences)
         Category     Terminology inconsistency
         Recommended  লগইন everywhere — the project's established term
         Confidence   HIGH
```

Five worked language examples: [Bengali](examples/bengali.md) ·
[Hindi](examples/hindi.md) · [Japanese](examples/japanese.md) ·
[Arabic](examples/arabic.md) ·
[European languages](examples/european-language.md)

---

## Translation vs localization

| | Translation | Localization |
| --- | --- | --- |
| Unit of work | the string | the decision behind the string |
| Input | a word list | the application |
| "Save" | one target word | one per context, resolved from the call site |
| Technical terms | a rule ("keep them English") | a per-term judgement per language |
| Plurals | source shape copied | the target locale's own categories |
| Numbers, dates, money | out of scope | in scope, reported for a formatter fix |
| Direction | out of scope | reported, with the layout work it implies |
| Uncertainty | invisible | an output, with confidence attached |
| Success | every string filled | the product sounds like it was written locally |

## What it will not do

- **Claim native authority.** Never "native speakers say this" — instead "this
  is the more common software convention", with what the claim rests on.
- **Guess hidden grammar.** When the target needs gender, formality or a counter
  the source does not carry, it says so and offers the options.
- **Invent numbers.** No fabricated string counts, no claimed validation that
  did not run, no cited source it did not read.
- **Encode stereotypes.** Language use varies by region, age, profession,
  audience and product. Those are factors, never rules.
- **Touch your source code.** Hardcoded strings, concatenated sentences and
  formatter bugs are reported as findings, not silently refactored.

---

## Technical validation

Language quality is a judgement call. These are not, and they run on everything
produced or reviewed:

| Check | Failure is |
| --- | --- |
| Placeholders match the source exactly — `{name}`, `{{name}}`, `%s`, `%1$s`, `:name`, `<0>…</0>` | **BLOCKING** |
| Plural categories match what the target locale requires | **BLOCKING** |
| Keys, nesting and file syntax unchanged | **BLOCKING** |
| HTML, Markdown and rich-text tags intact | **BLOCKING** |
| No pluralization faked by string concatenation | High |
| Terminology consistent with the project glossary | High |

Placeholder order is deliberately *not* checked: verb-final languages move the
interpolation, and that is correct.

## Glossary and locale profile

Two artifacts keep a localization consistent across sessions, contributors and
agents:

- **[`templates/glossary.yml`](templates/glossary.yml)** — one entry per product
  concept: source, target, strategy, context, confidence, notes. Reused as
  translation memory; conflicts against it are findings.
- **[`templates/locale-profile.yml`](templates/locale-profile.yml)** — the
  decisions that would otherwise be re-made differently every run: register and
  address form, digits, plural mechanics, date/number/currency conventions.

Copy them into your project. If you already have a glossary or style guide, it
outranks anything the skill would infer.

A **[review report template](templates/review-report.md)** is included for
REVIEW mode output.

## Confidence

| Level | Basis |
| --- | --- |
| **HIGH** | Established project terminology, platform convention, fully resolved context, or a mechanical fix |
| **MEDIUM** | Natural, but several conventions are in genuine use, or context was inferred rather than observed |
| **LOW** | Ambiguous source, missing grammatical information, or culturally variable wording |

LOW-confidence decisions are always surfaced. A LOW-confidence translation may
still be written — flagged — but it is never presented as settled.

---

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill practical-localizer
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill practical-localizer --agent claude-code
```

Then ask for what it does — skills are selected by description, so there is no
command to memorize:

```
Analyze this app for Bengali localization.
Localize the onboarding namespace to Japanese and keep the existing terminology.
Review the French locale for naturalness — I think it reads like a translation.
Why does the Arabic build show the wrong plural form for 3 items?
```

## Supported localization systems

Detected by inspection, not assumption: i18next and react-i18next, react-intl /
FormatJS, next-intl, next-i18next, vue-i18n, Laravel `lang/`, gettext `.po`,
Rails I18n, Flutter `.arb`, Android `strings.xml`, Apple `.strings` and
`.stringsdict`, Java properties, and custom systems — plus JSON, YAML, XML, PHP
and TS/JS catalogs generally.

If your project does localization some other way, the skill reads how it works
before touching it. See
[`references/localization-workflow.md`](references/localization-workflow.md).

## Documentation

| Reference | Covers |
| --- | --- |
| [localization-workflow.md](references/localization-workflow.md) | Framework and format detection, scoping, git safety |
| [translation-strategy.md](references/translation-strategy.md) | Translate / transliterate / preserve / adapt, and tone |
| [terminology.md](references/terminology.md) | Glossary, translation memory, consistency |
| [context-analysis.md](references/context-analysis.md) | Reading meaning out of the codebase |
| [pluralization.md](references/pluralization.md) | Plural categories per system and locale |
| [locale-formatting.md](references/locale-formatting.md) | Dates, numbers, currency, units, sorting |
| [rtl.md](references/rtl.md) | Right-to-left readiness |
| [ui-fit.md](references/ui-fit.md) | Expansion, contraction, layout risk |
| [confidence.md](references/confidence.md) | What evidence supports which claim |
| [review-methodology.md](references/review-methodology.md) | Reviewing an existing localization |

Test fixtures and their expected findings: [`tests/README.md`](../../tests/README.md).

## Limitations

Practical Localizer is instruction-driven, not a translation engine, and it does
not claim perfect or native-quality output.

- **It is not a replacement for a native reviewer.** For a product where the
  language is the product, it is a first pass that makes the human review
  cheaper and better targeted — not a substitute for it.
- Quality varies by language, by how much context the repository carries, and by
  the agent running it.
- Low-resource languages and highly specialized domain vocabulary are where it
  is weakest, and where its confidence levels matter most.
- It reads the repository. Runtime data, screenshots and rendering are outside
  what it can observe, so UI fit and layout findings are flagged as potential
  rather than confirmed.
- Without web access it relies on application context, existing translations and
  the glossary you supply — and says so.
- An absent finding is not proof that the localization is correct.

## License

[MIT](../../LICENSE)
