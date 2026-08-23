# UI fit

A translation can be linguistically excellent and still break the product. Text
length changes, and interfaces built around English string widths are the ones
that break.

## What to expect

Text length changes in both directions, and the effect is strongest exactly
where space is tightest: short strings expand proportionally more than long
ones, so buttons, tabs, table headers, badges and menu items are the highest
risk while paragraphs are the lowest.

Other length-adjacent risks:

- **Compounding** — languages that form long single words have no place to wrap,
  so a narrow column overflows instead of breaking.
- **Vertical growth** — some scripts need more line height, and diacritics or
  ascenders can clip in fixed-height rows.
- **Contraction** — CJK translations are often much shorter, which can leave
  buttons looking unbalanced or a layout looking empty rather than broken.
- **No spaces** — scripts that do not use spaces between words need
  line-breaking rules the CSS may not have enabled.
- **Numbers and dates** grow when localized formats are longer.

## Where it shows up

| Element | Failure mode |
| --- | --- |
| Buttons with fixed width | truncation, ellipsis, or text overflowing the shape |
| Navigation and tab bars | wrapping to a second row, or horizontal scroll |
| Table headers | column collapse, unreadable stacked words |
| Badges and chips | text clipped or the pill distorted |
| Modal and card titles | wrap pushes the body content out of view |
| Fixed-height rows | vertical clipping of diacritics |
| Tooltips | overflow of a fixed max-width |
| Mobile viewports | everything above, one size worse |
| Email templates | fixed-width tables with no reflow |

## How to report it

You can read the code; you usually cannot see the rendering. Say so. Use
`POTENTIAL UI FIT ISSUE`, name the evidence, and never invent pixel widths,
character limits or screenshots you did not observe.

```
POTENTIAL UI FIT ISSUE
  Key        nav.notifications
  Source     Alerts (6 characters)
  Target     <target string> (n characters)
  Evidence   rendered in <TopNav> as a tab; the container sets a fixed width
             and `white-space: nowrap` (components/TopNav.tsx)
  Options    shorter target wording · allow the nav to wrap · verify in-browser
  Confidence Medium — length is measured, rendering is not
```

If real constraints exist in the code — `maxLength`, a fixed `width`, a
`truncate` class, a character counter — cite them; that turns a guess into an
observation.

## Shortening without damaging the language

When a shorter target string is genuinely needed:

- prefer the noun or the bare verb stem over a full polite sentence, if that
  register is acceptable for the element,
- drop the object when the UI already shows it ("Delete" next to the file name),
- use the established short form the local software ecosystem uses,
- never abbreviate with invented contractions or truncate mid-word,
- never drop a politeness marker that the rest of the product uses, purely for
  width — flag the conflict instead.

Truncation with an ellipsis is a last resort, and in some scripts it hides
grammatical information that the reader needs to parse the phrase at all.

## Verification

The honest end state is: "length measured, rendering not verified." If the
project has visual regression tests, a Storybook, or a locale preview, say that
a pass in the target locale is the check that would close this. Recommending the
check is better than pretending to have run it.
