# Right-to-left localization

Languages written right-to-left — Arabic, Hebrew, Persian, Urdu among them —
need more than translated strings. The text will render; the interface may not.

The skill's job here is to **report**, precisely. Layout and CSS are application
source: change them only when explicitly asked.

## What actually changes

**Direction, not mirroring of everything.** The document direction flips
(`dir="rtl"`), and with it reading order, alignment, and the meaning of "start"
and "end". Numbers and embedded Latin text still run left-to-right inside an
RTL line — this is normal bidirectional text, not a bug.

**Layout.** Anything positioned with `left`/`right`, `margin-left`,
`padding-right`, `text-align: left`, `float`, or a fixed-side drawer is a
candidate. Logical properties (`margin-inline-start`, `inset-inline-end`,
`text-align: start`) handle both directions with no per-locale rules; report
physical properties on user-facing layout as an RTL readiness finding.

**Icons and motion.** Directional affordances flip: back/forward arrows, undo
and redo, next/previous, progress and stepper direction, indentation and
list nesting, chevrons on expanders, send arrows, breadcrumb separators.
Non-directional icons must *not* flip: clocks, logos, checkmarks, media
play buttons in most conventions, images of objects.

**Wording.** Copy that says "on the left", "the panel on your right", "swipe
left" describes an interface that no longer exists in that direction. These are
translation findings, not CSS findings — reword to the element's name or its
role.

**Punctuation and mixed content.** Question marks, commas and parentheses have
mirrored forms or mirrored placement; a filename, URL, code snippet or product
name inside an RTL sentence needs isolation (`<bdi>`, `dir="auto"`, or the
Unicode isolate characters) or its punctuation drifts to the wrong end.

**Numerals and dates.** Some RTL locales use Latin digits, some use another
digit set, and usage varies by region and context. Pick one with the user,
record it in the locale profile, and apply it consistently. Do not assume.

## What to inspect

- The root element: is `dir` set from the active locale, or hardcoded `ltr`?
- Is there a per-locale direction map, and does the new locale appear in it?
- Stylesheets: physical side properties, `transform: translateX`, `left:`/`right:`
  positioning, one-sided borders and shadows on components users read.
- Icon components with a fixed rotation or a directional name.
- Any component that measures or animates horizontally.
- Fonts: does the bundled font cover the script, and does the line height suit
  it? Many scripts need more vertical room than Latin at the same size.
- Existing RTL locales in the project — if one already ships, most of this work
  is done and the finding list is much shorter.

## Reporting

```
RTL READINESS
  dir attribute        set from locale in app/layout.tsx — OK
  Logical properties   12 components use margin-left / text-align: left
  Directional icons    ArrowBack, StepperChevron rotate by a fixed transform
  Direction wording    3 strings refer to left/right position
  Mixed content        filenames interpolated into sentences without isolation
  Fonts                bundled family has no coverage for this script

  POTENTIAL LAYOUT ISSUE — none of the above is fixed by translation alone.
  Recommend a layout pass before shipping this locale.
```

Say plainly that string localization is complete and layout is not, rather than
letting a green translation report imply the locale is ready.
