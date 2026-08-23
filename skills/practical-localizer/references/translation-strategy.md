# Translation strategy

Every meaningful term gets exactly one of four strategies, chosen from evidence,
not habit.

## TRANSLATE

Use the natural target-language equivalent when the language has a current,
ordinary word for the concept and users would find the borrowed form odd.

Applies well to: actions (delete, send, share), everyday nouns, status and
error copy, and any string the user reads as a sentence.

Watch for over-translation: a formal or literary equivalent can be *correct* and
still wrong for a UI, because it belongs to a register users do not associate
with software.

## TRANSLITERATE

Write the borrowed source word in the target script when that borrowed word is
what people actually say.

This is not laziness — for many languages the transliterated form is the
established, unmarked term, while the "pure" native coinage reads as a textbook
exercise. It is also not universal: the same English word may be transliterated
in one language and translated in the neighbouring one. Decide per language, per
term, per product.

Signals that transliteration is right:

- the concept arrived with the technology and has no pre-existing native word,
- major products in that locale use the transliterated form,
- the project already uses it for sibling terms,
- the native alternative is longer, rarer, or ambiguous.

Signals it is wrong:

- an ordinary native word already covers it in daily speech,
- the target locale's product ecosystem consistently translates it,
- the audience is not tech-fluent.

Whichever you pick, be consistent: mixing forms across the app is worse than
either choice made uniformly. See `terminology.md`.

## PRESERVE

Leave the source form untouched when translating destroys meaning or breaks
something:

- brand, product and feature names, trademarks,
- protocol and format names used as identifiers (`HTTP`, `JSON`, `SQL`, `CSV`),
- code, URLs, file extensions, keyboard shortcut names, identifiers echoed from
  the API,
- units and symbols that are internationally written the same way.

Preserve is a decision, not a default. "Technical term" alone does not justify
it — many languages have established, widely used terms for *password*,
*download*, *file*, *network* or *server*, and preserving English there makes
the product feel untranslated. Check what the target locale's software ecosystem
actually does.

## ADAPT

Rewrite the phrase so it does the same job in the target language, when a
word-for-word rendering would be unidiomatic or grammatically forced.

Typical triggers:

- calls to action ("Get Started", "Learn more", "Try it free"),
- marketing copy, empty states, onboarding,
- English noun stacks ("Account settings sync status"), which many languages
  must unpack into a phrase,
- idioms and metaphors,
- strings whose English grammar cannot survive the target's word order.

Adapt preserves *intent and tone*, not sentence structure. It is not licence to
invent new product claims, change what a button does, or add information the
source did not carry.

## Choosing between them

Ask, in order:

1. What does the source actually mean **here**? (`context-analysis.md`)
2. Does the project already have a term for it? → reuse it.
3. Does the target language's software ecosystem have an established term?
4. Would the native equivalent read as ordinary, or as a textbook?
5. Does anything technical depend on the exact characters? → PRESERVE.
6. Does the grammar survive word-for-word? If not → ADAPT.

Record the outcome in the glossary with a confidence level. A term that took
five minutes to decide should never be re-decided differently three files later.

## Tone

Determine the product's register before writing anything: formal, professional,
friendly, casual, technical, enterprise, consumer. Evidence is in the source
copy — contractions, exclamation marks, humour, imperative vs. polite forms,
how errors are worded.

Then map it onto what the target language offers, which is usually a different
set of choices: politeness levels, formal and informal second person, verb
endings, honorifics, imperative vs. nominal styles.

- Do not turn a casual consumer app into legal prose because the formal register
  felt safer.
- Do not make an enterprise admin console chatty because the source used an
  exclamation mark once.
- Be consistent: switching between formal and informal address inside one flow
  is one of the most noticeable localization defects.
- Errors and destructive confirmations usually sit one notch more formal than
  the rest of the product, in most registers.

When the language forces a choice the source does not encode (formality, gender
of the addressee, inclusive/exclusive we), pick the safest option for the
audience, record it in the locale profile, apply it everywhere, and list it as a
review item.
