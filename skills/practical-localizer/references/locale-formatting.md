# Dates, times, numbers, currency, units

Text is the visible half of localization. The other half is everything the
product formats programmatically — and getting it wrong is more noticeable than
a slightly stiff button label, because it makes data look wrong.

## Rule one: format, do not translate

If a date, number or amount is produced by hardcoded string assembly, the fix is
not a better string — it is the platform's locale-aware formatter:

- JavaScript: `Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat`,
  `Intl.ListFormat`, `Intl.PluralRules`
- Date libraries: locale packs for `date-fns`, `dayjs`, `luxon`
- Backends: ICU-based formatters, `Babel` (Python), `I18n.l` (Rails),
  `NumberFormatter` (PHP `intl`), `NSNumberFormatter` / `DateFormatter` (Apple),
  `android.icu.text` (Android)

Report hardcoded formatting as a technical finding. Do not change application
code to fix it unless the user asks — that is a source change, not a
localization change.

## What varies

**Dates**

- Field order: year-month-day, day-month-year, month-day-year.
- Separators and whether leading zeros appear.
- Month and weekday names, and whether they inflect by grammatical case.
- First day of the week, and which days are the weekend.
- Era and calendar systems — some locales expect a non-Gregorian calendar, or a
  Gregorian date alongside a local one.
- Relative dates ("2 days ago") follow plural rules, not a fixed template.

**Times**

- 12-hour with locale-specific day-period markers, or 24-hour.
- Separator, and whether a leading zero is used.
- Time zone display and abbreviation localization.

**Numbers**

- Decimal separator and group separator, which can be `.` `,` a space, or none.
- Grouping *size*: three-digit grouping is common but not universal; the
  Indian system groups the leading digits in pairs and uses lakh and crore in
  everyday copy.
- Digit shapes: several locales may display digits in a non-Latin script, and
  usage often varies by region and context — decide with the user, and stay
  consistent within the product.
- Negative sign placement, percent sign placement and spacing.

**Currency**

- Symbol or code, before or after the amount, with or without a space.
- Decimal places: some currencies use none, some use three.
- Negative amounts: minus sign versus parentheses.
- Never convert amounts. Localizing text must not change what a price means.
  A `$` that becomes a local symbol on the same number is a data bug.

**Units and measures**

- Metric versus other systems, paper sizes, temperature scale.
- Unit names pluralize by the locale's rules and often need a space or none.
- Do not silently convert values; report the mismatch and let the product decide.

**Addresses, names, phone numbers**

- Field order, postal code position, whether a state or region field applies.
- Given/family name order, and whether a single full-name field is safer.
- Phone number grouping and international prefix.
- Validation rules that assume one country are a localization defect worth
  reporting even when no string changes.

**Sorting and search**

- Alphabetical order is locale-dependent; a code-point sort is wrong in many
  languages. Case-insensitive matching also differs by locale.

## Checklist for a review

- Is any date, time, number or money value assembled from string parts?
- Do format tokens (`YYYY`, `MM/DD`) appear inside translatable strings? They
  should be in code, not in the catalog — unless the framework deliberately
  exposes a per-locale pattern key, which is then a legitimate thing to localize.
- Does the target catalog contain a hardcoded currency symbol?
- Are relative-time strings plural-aware?
- Does the locale profile record the conventions actually chosen, so the next
  run does not re-decide them differently?
