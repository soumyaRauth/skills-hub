# Pluralization

Plural handling is where a confident translation quietly breaks. English has two
forms; the number of forms a language needs ranges from one to six, and the rule
that selects them is not "is n equal to 1".

## Two things to establish first

1. **Which plural categories does the target locale use?** Use the locale's CLDR
   plural rules as the source of truth rather than intuition. The category names
   are `zero`, `one`, `two`, `few`, `many`, `other`, and a language uses a subset.
2. **What mechanism does the app have?** Never fake pluralization by
   concatenation or a ternary when the framework offers a real mechanism, and
   never invent categories the framework will not look up.

Category names are labels, not quantities. `one` in some languages selects 21
and 31; `few` in others covers 2–4 or 3–10; `zero` may exist as a category even
where 0 is grammatically plural, and in several languages 0 takes the singular
form. Look the rule up; do not derive it from the name.

## Mechanisms

**ICU MessageFormat** (react-intl, next-intl, Flutter `.arb`, Java):

```
{count, plural,
  =0 {No notifications}
  one {# notification}
  other {# notifications}}
```

`=0` is an exact-value match, evaluated before categories — useful for a special
empty-state wording, and independent of whether the locale has a `zero`
category. Keep `#`, the placeholder name, and any `offset:` exactly as they are.

**i18next** — suffixed keys, one per category the locale needs:

```json
{
  "notification_one": "{{count}} notification",
  "notification_other": "{{count}} notifications"
}
```

The target file may need more or fewer keys than the source. A locale needing
`_few` and `_many` must have them; a locale with a single form needs only
`_other`. Missing categories fall back and render the wrong form.

**gettext** — the `Plural-Forms` header defines `nplurals` and the selecting
expression; `msgstr[0..n-1]` must be filled in that order.

**Laravel** — `trans_choice` with `|`, optionally with explicit ranges:
`{0} None|{1} One|[2,*] :count items`.

**Rails I18n** — `:zero` / `:one` / `:other` sub-keys per locale's rules.

**Android** — `<plurals name="…">` with `<item quantity="one">`; quantities not
used by the locale are ignored, missing ones fall back.

**Apple** — `.stringsdict` with `NSStringPluralRuleType` and one entry per
category.

## Validation checklist

- Every category the target locale requires is present — no more, no fewer.
- The count placeholder survives in every form, including the ones where the
  number is not shown as a digit.
- No form was produced by copying the singular and adding a suffix by analogy.
- The source's `=0` / explicit-range branches are preserved.
- Nothing was pluralized by string concatenation ("`" " + count + " items"`").
- Ordinals (`{n, selectordinal, …}`) use ordinal rules, which differ from
  cardinal rules in the same locale.
- Ranges ("2–5 items") may take their own form in some languages; if the app
  builds them from a plural string, flag it.

## Counters and classifiers

Several languages require a classifier or counter word between a number and a
noun, chosen by what is being counted. The English string carries no signal of
which one to use, so the noun must be known at translation time.

If one plural string is reused for several different nouns, the correct
classifier cannot be chosen. Report that as a key-splitting task rather than
picking one classifier and hoping.

## When gender or case interacts with number

In some languages the counted noun changes case or the verb changes agreement
depending on the number. That is not a plural-category problem the framework can
solve — the whole clause must be written per form. Write full sentences inside
each plural branch rather than assembling them around the placeholder.

## Reporting

Plural findings are technical, not stylistic:

```
BLOCKING TECHNICAL ISSUE   notifications.unread
  Source   {count, plural, one {# unread} other {# unread}}
  Target   plural wrapper removed; renders a single fixed form
  Effect   the number is dropped and the form is wrong for every count
```
