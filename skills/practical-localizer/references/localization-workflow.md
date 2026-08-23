# Localization workflow

The detail behind Phases 1–2 of `SKILL.md`: how to find out what the application
actually does before changing any of it.

## The shape of the work

```
source application
      ↓  what mechanism does this app use?
localization architecture
      ↓  what does the target language do with software vocabulary?
language usage profile
      ↓  what does this project already say?
existing terminology
      ↓  what does each string actually mean here?
context extraction
      ↓  translate / transliterate / preserve / adapt
translation strategy
      ↓
natural localization
      ↓  placeholders, plurals, structure
technical validation
      ↓  glossary, tone, naturalness
consistency review
      ↓
localized application
```

Every arrow is a decision that can be wrong. Word-for-word translation collapses
all of them into one.

## Detecting the mechanism

Read the manifests first (`package.json`, `composer.json`, `pyproject.toml`,
`Gemfile`, `pubspec.yaml`, `build.gradle`), then confirm against the tree. The
dependency tells you the message format; the tree tells you the layout.

| Signal | Mechanism | Placeholder style | Plural mechanism |
| --- | --- | --- | --- |
| `i18next`, `react-i18next` | i18next JSON | `{{name}}` | suffixed keys (`_one`, `_other`, `_zero`, …) or ICU via plugin |
| `react-intl`, `@formatjs/*` | ICU MessageFormat | `{name}` | `{count, plural, ...}` |
| `next-intl` | ICU MessageFormat | `{name}` | `{count, plural, ...}` |
| `next-i18next` | i18next on Next.js | `{{name}}` | i18next rules |
| `vue-i18n` | its own / ICU | `{name}` | `\|` separated forms |
| `lang/*.php`, `lang/*.json` | Laravel | `:name` | `trans_choice` ranges |
| `.po` / `.pot`, `gettext` | gettext | `%s`, `%1$s`, `%(name)s` | `Plural-Forms` header |
| `config/locales/*.yml` | Rails I18n | `%{name}` | `:one` / `:other` keys |
| `.arb` files | Flutter `intl` | `{name}` | ICU `plural` |
| `res/values*/strings.xml` | Android | `%1$s`, `%d` | `<plurals>` |
| `*.lproj/Localizable.strings` | Apple | `%@`, `%1$@` | `.stringsdict` |
| `messages.properties` | Java / Spring | `{0}` | `ChoiceFormat` / ICU |
| none of the above | custom | inspect and document it | inspect |

Also record, because they change the work:

- **Fallback locale** — does a missing key silently render English?
- **Namespaces / file split** — one catalog or many, and what the split means.
- **Key style** — nested objects, dotted flat keys, or English-as-key (Laravel
  JSON, Apple `.strings`). English-as-key means the source *is* the key: never
  edit the key side.
- **Interpolation with components** — `<Trans>` and its numbered tags carry
  markup through the string; those tags are structure, not text.
- **Where non-text locale behavior lives** — `Intl` calls, `date-fns` locales,
  `dayjs` plugins, currency formatting helpers.

## What counts as a localization file

Only resources whose purpose is user-facing text. Not every file containing
strings is one, and modifying the wrong file is the way this skill causes damage.

Localize: locale catalogs, translation namespaces, `.arb`/`.strings`/`.po`
files, framework `lang/` directories, and — only when explicitly in scope —
inline literals a developer asks to extract.

Do not touch: enum values, database seed data, API contract strings, config
keys, log messages, test fixtures, analytics event names, feature-flag names,
CSS class names, or anything an identifier depends on. When user-visible text is
hardcoded in components, report it as an extraction task; extracting it yourself
edits application source.

## Scoping a large application

Whole-app localization in one pass is rarely the right unit. Prefer, in order:

1. the namespace or feature the user named,
2. the strings missing in the target locale,
3. the strings the review flagged,
4. everything else, in reviewable batches.

Say which batch you are working on and what remains. A partial, verified,
consistent localization is more useful than a complete unverified one.

## Git safety

Before writing anything in LOCALIZE mode:

```bash
git status --short          # note pre-existing modifications; leave them alone
git diff --stat             # what is already in flight
```

After writing, show the files changed and the validation results. Never `commit`,
`push`, `checkout`, `reset`, `stash`, or discard user changes — the user decides
what happens to the diff.
