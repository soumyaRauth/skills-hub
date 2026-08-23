# Worked example — Japanese (ja-JP)

A cross-platform note-taking app, English source, machine-assisted Japanese
locale already shipped. The user asks:

> Review the Japanese localization — it reads like a translation.

Illustrative only. Style guides differ by product and company; several of the
choices below are conventions, not rules.

## Why "reads like a translation" is diagnosable

Japanese sentence structure, politeness system and UI conventions differ enough
from English that a word-order-preserving translation is immediately visible.
Four recurring signals:

**1. Verb-form on buttons.** Product UIs commonly label buttons with a short
noun form — 保存, 削除, キャンセル — rather than a full polite sentence. A catalog
where every button reads as a complete sentence looks like prose pasted into
controls.

**2. Placeholder position.** Japanese is verb-final, so the interpolation moves:

```
Source   Delete {{name}}?
Wrong    削除しますか {{name}}     ← English order preserved
Better   「{{name}}」を削除しますか？
```

The placeholder *set* is unchanged, which is what validation checks — never
validate placeholder *order*. See `../references/pluralization.md` for the
related plural-wrapper checks.

**3. Politeness consistency.** Mixing plain and polite forms inside one flow is
one of the most noticeable defects. Establish the level once — for a consumer
app, the polite です・ます style in messages with noun-style labels on controls
is a common pairing — record it in the locale profile, and apply it everywhere.

**4. Punctuation and spacing.** Japanese uses full-width punctuation （）「」、。
and no spaces between words. A catalog containing ASCII commas and periods
inside Japanese sentences, or spaces inserted around interpolations, was
produced without a style pass.

## Findings, abbreviated

### #1 — Counters, and one key too many jobs

Japanese counts things with a classifier chosen by what is being counted.

```
Key       list.itemCount
Source    {count, plural, other {# items}}
Current   {count, plural, other {#個のアイテム}}
Problem   this key renders for notes, tags, collaborators and attachments.
          個 does not fit people, and the natural counter differs by object.
Category  Pluralization / context
Recommend split the key per object type so each string can carry its own
          counter — e.g. a dedicated key for people
Confidence HIGH — the four call sites are in the repository
```

The locale itself needs only the `other` category — this language does not
inflect nouns for number — so the plural wrapper stays, with one branch. Removing
the wrapper would break the message format.

### #2 — Register mismatch on a destructive action

```
Key          note.deleteConfirm
Source       Are you sure you want to delete this note?
Current      本当にこのノートを削除したいですか？
Recommended  このノートを削除してもよろしいですか？
Reason       The current form mirrors English "do you want to", which reads as
             asking about the user's desire rather than seeking confirmation.
             The recommended pattern is the common confirmation form in
             Japanese software.
Confidence   MEDIUM — convention, and consistent with two existing dialogs in
             this catalog
```

### #3 — Over-translation

```
Key          nav.inbox
Source       Inbox
Current      受信箱
Recommended  keep 受信箱 — no change
Note         Reviewed and left alone. Not every English-looking string needs a
             borrowed form; this native term is standard for the concept.
```

Recorded deliberately, so the next run does not "fix" it. Review must be able to
end in *no change* — see `../references/review-methodology.md`.

### #4 — Text contraction, not expansion

Japanese target strings are frequently shorter than the English source. That
does not break layout, but it does leave buttons and cards looking sparse where
the design assumed a longer label, and it hides a different risk: a fixed-width
container tuned to Japanese will then break in a language that expands.
Reported as an observation, not a defect (`../references/ui-fit.md`).

### #5 — Line breaking

Japanese has no inter-word spaces, so line breaks are governed by rules about
which characters may not begin or end a line. If the CSS relies on word-boundary
wrapping, long strings may break at typographically wrong points. Reported for a
CSS check; not modified.

## Locale mechanics

```
Dates        source strings contain the literal pattern MM/DD/YYYY in 2 keys;
             the common Japanese order is year-month-day with unit characters.
             Move to a formatter rather than translating the pattern
Numbers      grouping and decimal separator match the source convention — OK
Currency     one string hardcodes a foreign currency symbol next to a localized
             amount; report to the product team, do not convert values
Input        name fields assume given-name-then-family-name ordering, and a
             single full-name field would be safer here
Fonts        the bundled family covers the script — OK
```

## What this example does not claim

- That noun-form labels are correct for every Japanese product. Some style
  guides prefer the verb form on primary actions.
- That one politeness level suits every audience. It does not; pick it
  deliberately and record it.
- That machine-assisted translation is unusable — only that it does not make
  structural decisions, and those are what "reads like a translation" refers to.
