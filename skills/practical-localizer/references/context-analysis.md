# Context analysis

The single biggest quality difference between translation and localization is
whether the string was understood before it was rendered. English UI copy is
short, ambiguous and grammatically underspecified; most target languages need
information English never states.

## What to gather per string

| Source | What it tells you |
| --- | --- |
| Key path / namespace | `errors.auth.expired` vs `marketing.hero.expired` |
| Call sites | who renders it and with what data |
| Component name | `<DeleteAccountDialog>` resolves half the ambiguity |
| Handler name | `onSubmit`, `removeMember`, `archiveProject` |
| Element type | button, heading, label, status, toast, tooltip, `aria-label`, placeholder |
| Neighbouring copy | the dialog title explains its own confirm button |
| Interpolated values | what `{count}`, `{name}`, `{date}` actually hold |
| Comments / translator notes | sometimes the answer is written down |
| Tests | assertions reveal intended behavior |
| API and domain model | the record the string acts on |

Read the call site before the dictionary. `t("remove")` invoked inside
`removeMember(member)` on a team page means *take this person off the team* —
reversible, about a person. The same key rendered in a file manager means
*delete this file*. Many languages use different verbs for the two, and English
does not.

## Questions that decide the wording

1. **Is it an action or a state?** "Complete" as a button (do it) versus a badge
   (it is done) is a different part of speech in most languages.
2. **Who acts?** A button the user presses, a system message about what the
   product did, or an instruction to the user — different persons, moods and
   politeness forms.
3. **What is the object?** Deleting a file, a person, a subscription and a
   message may take different verbs, different agreement, different classifiers.
4. **Is it a fragment?** Strings concatenated at runtime are a defect for most
   languages — word order and agreement cannot survive it. Report concatenation
   rather than translating the pieces and hoping.
5. **Is it reversible?** Destructive actions carry heavier wording in most
   languages; softening a permanent deletion is a real harm.
6. **Is it addressed to one user or about many?** Some languages need to know.
7. **Does the target need grammatical information the source lacks?** Gender of
   the user or of the object, formality of address, animacy, a counter or
   classifier for the noun being counted.

## When the source hides required information

Common cases: gendered past-tense verbs, adjective agreement, honorifics,
counters, definiteness, and any string interpolating a name whose gender matters.

If the codebase can answer it (a `gender` field on the profile, a fixed object
type, a known audience), use that and note the dependency. If it cannot:

- choose the neutral or safest construction available in that language,
- record the choice in the locale profile so it stays consistent,
- mark the string `REVIEW REQUIRED` with the specific missing information.

Do not guess silently, and do not invent a grammatical feature the framework
cannot supply at runtime.

## The classic ambiguous terms

Resolve these from context every time; a project-wide default for them is a bug
waiting to ship: **Save, Remove, Delete, Cancel, Submit, Apply, Back, Continue,
Close, Open, Share, Account, User, Profile, Project, Workspace, Home, Settings,
Update, Post, Match, Order, Free, Right, Left, Set, Current, Second, Contact,
Address, Book, Type, Field, Key, Value, Enter, Return, Load, Play**.

Worked pattern:

```
Key      billing.cancel
Source   Cancel
Context  <CancelSubscriptionDialog> primary button, handler cancelSubscription()
Meaning  terminate an ongoing subscription — not "dismiss this dialog"
Note     the dialog's secondary button is also "Cancel" (dismiss) under the key
         common.cancel. Two concepts, two target terms required.
```

That second sentence is the finding. A translator working from a spreadsheet
never sees it.

## Practical extraction

```bash
# Where is this key used?
grep -rn "billing\.cancel" src/ --include=*.tsx --include=*.ts

# What does the surrounding component do?
grep -rn "cancelSubscription" src/

# Which keys does one component render?
grep -oE "t\(['\"][^'\"]+" src/components/BillingPanel.tsx
```

Keys that appear in exactly one component are cheap to localize well. Keys
shared across many, with different objects around them, are the ones to inspect
carefully — a shared key with divergent meanings is a defect to report, not a
puzzle to solve with a compromise translation.
