# Accessibility assessment

The `/standards accessibility` focus. WCAG 2.2 is the reference for web content;
EN 301 549 wraps it for European ICT procurement and adds requirements WCAG does
not cover.

The governing rule: **static inspection cannot establish conformance.** It finds
specific failures and specific absences of evidence. A clean automated pass
covers a minority of the success criteria, and reporting a conformance level
from source is one of the more damaging overclaims available, because
organizations publish accessibility statements based on it.

## What source review can actually find

| | |
| --- | --- |
| Form controls with no programmatic label | `<input>` with no `<label for>`, `aria-label`, or `aria-labelledby` |
| Images with no alternative text | Missing `alt`, or `alt` duplicating adjacent text |
| Non-semantic interactive elements | `<div onClick>` with no role, no `tabIndex`, no key handler |
| Missing document structure | No `lang`, no `<main>`, no landmarks, skipped heading levels |
| Focus suppression | `outline: none` with nothing replacing it; positive `tabIndex` |
| Inaccessible custom widgets | Modals, menus, comboboxes, tabs without the expected roles, states and keyboard model |
| Errors announced only visually | Validation messages with no association to the field and no live region |
| Drag-only interactions | Sortable lists, drag-and-drop upload with no single-pointer or keyboard alternative — WCAG 2.2 dragging movements |
| Target size | Small tap targets in dense controls, where the CSS is inspectable — WCAG 2.2 |
| Authentication friction | Blocked paste in password fields, cognitive puzzles with no alternative — WCAG 2.2 accessible authentication |
| Redundant entry | Re-asking for information already provided in the same process — WCAG 2.2 |
| Timing | Session or interaction timeouts with no extension path |
| Motion | Animation with no `prefers-reduced-motion` handling |

## What requires a human

Whether alternative text is *meaningful*. Whether focus order matches the visual
order. Whether the visible focus indicator is actually visible against its
background. Colour contrast as rendered, including over images and gradients.
Whether an error message tells someone how to fix the problem. Whether a screen
reader announces a custom widget usefully. Whether the flow can be completed by
keyboard end to end — which is the single highest-value manual test and the one
teams most often skip.

Say which is which, every time:

```markdown
Automatable      ✓ 9 form fields checked for programmatic labels — 2 missing
Partially        ⚠ Custom combobox has roles and states; behaviour unverified
Manual           ✕ Screen reader announcement of the multi-step checkout
External         ✕ Embedded payment iframe is the provider's markup
```

## Scope

Assess the workflows that matter — sign-up, sign-in, the core task, checkout,
account management — rather than every component. An accessibility finding on a
rarely-used admin screen is not the same as one on the path every customer takes.

## Framework notes

- **React / Vue / Svelte**: check the component library for a documented
  accessibility posture before auditing every component by hand. Look for
  `dangerouslySetInnerHTML` in interactive areas, click handlers on non-buttons,
  and modals that do not trap or restore focus.
- **Server-rendered templates**: labels and heading structure are usually easier
  to verify; check partials and shared layouts, where a single defect repeats
  everywhere.
- **Design systems**: one defect in a shared component is one finding with a wide
  blast radius, and one fix. Say so — it is the most efficient accessibility work
  available.
- **Mobile**: platform accessibility APIs rather than WCAG markup — accessible
  labels on controls, dynamic type support, touch target sizes, and whether
  custom-drawn UI is exposed to the accessibility tree at all.

## Wording

```
Bad   "The site isn't accessible."
Bad   "WCAG 2.2 AA compliant."
Good  "The password field in src/components/LoginForm.tsx:24 has no associated
       accessible name — no <label for>, aria-label, or aria-labelledby.
       This is relevant to the WCAG 2.2 requirements for labels and name/role/
       value. Static inspection cannot establish conformance overall."
```

## Legal framing

WCAG is a technical standard, not a law. Whether conformance is legally required
depends on jurisdiction, sector and contracts — EU public sector bodies, the
European Accessibility Act, US federal procurement and private B2B products are
in different positions, and the repository cannot tell you which one applies.
Name the standard, name the finding, and route the obligation question to
someone who can answer it.
