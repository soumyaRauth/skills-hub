# Implementing improvements

Moving from findings to changes in a product or a manuscript, without
breaking what works, overriding the owner, or claiming more than was checked.

## Contents

- Before changing anything
- What needs approval first
- Software
- Common product fixes, done properly
- Books and documents
- Verifying the result
- Reporting what changed

## Before changing anything

1. The findings exist, with root causes. Fix causes, not symptoms.
2. The request covers the change: "fix the error messages" does not authorize
   removing sign-up fields.
3. You have read the existing work in full for the scope: the components and
   their tests, or the chapter and its neighbours.
4. You know what is good and must survive.
5. You know how you will check the result.

## What needs approval first

Propose and wait, with the reason and the alternatives, before:

- **Content direction:** changing a book's audience, promise, scope, chapter
  order, running example, voice, or technical stack and versions; removing or
  merging chapters or sections.
- **Product behaviour:** removing or adding steps, fields or features;
  changing defaults, pricing presentation, notifications, or what happens to
  data.
- **Privacy and consent:** anything that changes what is collected, how
  consent is asked, or who sees what. Hand the obligations to
  `standards-compass`.
- **Irreversible or outward-facing actions:** deleting content, publishing,
  sending, overwriting a shared document without suggestion mode.
- **Large rewrites** where a smaller change would serve.

Small, clearly in-scope improvements (a clearer error message, a label tied to
its field, a defined term, a fixed code example) can proceed under an
improvement request.

## Software

- **Follow the house:** existing architecture, components, design system,
  copy conventions, i18n mechanism, test patterns. An improvement that adds a
  second way of showing errors makes the product less consistent.
- **Smallest change that fixes the cause.** Keeping form state on error is
  usually a few lines; it does not need a new form library.
- **Copy goes where copy lives.** If the project has message catalogs, change
  the catalog; if other locales exist, note that their translations now hold
  the old meaning and hand off to `practical-localizer`.
- **Accessibility fixes** use native elements and attributes first (`label`,
  `button`, `aria-describedby`, `aria-live`), custom ARIA only when needed.
- **Test what you changed:** add or update tests for the behaviour (input
  preserved after a failed submit; the error associated with its field; the
  button disabled during submission). Run the existing tests. For anything
  beyond a small change, `proof-driven-dev` owns proving the outcome.
- **Never weaken a control to remove friction.** When a password policy,
  verification step or consent requirement is the friction, keep the control
  and fix how it is presented (rules stated up front, a strength meter, a
  clear reason). If the control itself seems wrong for the people using it,
  raise it with its owner and `standards-compass`; do not change it here.
- **Avoid unnecessary redesigns.** The finding was "people lose their input",
  not "the form should look different".

## Common product fixes, done properly

| Finding | Fix that addresses the cause |
| --- | --- |
| Generic error for every failure | Map each known failure to a message saying what happened and what to do; keep a plain fallback for the unknown; never show raw codes alone |
| Input lost on error | Keep form state; on server errors, keep everything except secrets the platform must not retain; move focus to the first error |
| Requirements revealed only after failure | State them before the attempt, next to the field; validate as the person goes, without shouting before they finish typing |
| Placeholder as label | A visible `<label>`; placeholder only for an example format, if at all |
| Errors not announced | `aria-describedby` linking field and message; an `aria-live` region or focus movement for form-level errors |
| Disabled button with no reason | Keep it enabled and explain on submit, or show what is missing |
| Pre-ticked marketing consent, confirmshaming | Unticked by default, neutral wording, separate from terms |
| Too many fields up front | Ask only what the first value needs; defer the rest to when it is needed, with the reason shown |
| No loading feedback, double submission | Disable during the request, show progress, make the request idempotent where possible (`api-contract-guard` and `proof-driven-dev` own the server side) |
| Empty state says "No data" | Say why it is empty and offer the first action |

## Books and documents

- **Work in the source,** not the exported PDF: Markdown, LaTeX, Word,
  Google Docs, the docs site. Rebuild the output afterwards.
- **Reviewable edits** for manuscripts that belong to someone else: suggestion
  mode, tracked changes, a branch with a diff. Never silently overwrite a
  shared manuscript.
- **Preserve the author:** meaning, voice, examples they care about,
  technical claims (changed only when verified).
- **Keep the book consistent:** maintain the terminology list; when a term,
  variable, file name or version changes, change every occurrence in prose,
  listings, exercises, answers, downloadable code, index and glossary.
- **Cross-references:** update "see section X" and figure numbers after
  moving content.
- **Verify technical changes** by running them (`technical-accuracy.md`).
- **Visual changes** go into the stylesheet, template or document styles, not
  into individual pages, so they stay consistent.
- **Re-render and re-inspect** the output: the changed pages, a contact sheet
  of the whole document for regressions, and the navigation (bookmarks,
  links, TOC page numbers).

## Verifying the result

Re-inspect the way you inspected the original, and say what kind of check
each one was:

- **Product:** re-run the journey including the failure paths; run tests;
  re-check keyboard and screen-reader basics if they were in scope.
- **Book:** re-read the revised section in context, from the previous section
  onward, as the reader; re-run code; re-render pages.

Everything you checked is a check of the artifact. Whether people now have a
better experience is still a hypothesis. Say so, and name the smallest test
with real people that would confirm it.

## Reporting what changed

```
IMPLEMENTED
  F1  Form keeps all input after a server error         SignupForm.jsx · test added · tests pass
  F2  Password rules shown before the first attempt     SignupForm.jsx, messages.js
  F4  Marketing consent unticked, neutral wording       SignupForm.jsx — product decision confirmed by you
NOT IMPLEMENTED
  F3  Remove phone and company-size fields              Needs your decision: sales uses company size
VERIFIED BY
  Tests (12 pass, 2 new) · code paths re-read · running app not available
NOT VERIFIED
  Whether completion improves: compare sign-up completion for two weeks before and after,
  and run three think-aloud sessions with new freelancers
```
