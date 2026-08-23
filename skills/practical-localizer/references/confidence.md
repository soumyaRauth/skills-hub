# Evidence and confidence

Every non-trivial localization decision carries a confidence level, and the
level must be supported by the evidence actually available — not by how
plausible the wording feels.

## Levels

**HIGH** — at least one of:

- the project already uses this term consistently for this concept,
- the platform or framework's own localization uses it,
- the source string is unambiguous, the context is fully resolved from the code,
  and the target construction is uncontroversial,
- multiple independent, reputable sources converge on the same form,
- the change is mechanical: a restored placeholder, a missing plural category,
  a fixed key.

**MEDIUM**

- the translation is natural, but more than one convention is in real use,
- the project has no established term and the ecosystem is not consistent,
- the context is inferred from a component or handler name rather than observed
  directly,
- register or tone required a judgement call,
- the term is domain-specific and the audience's familiarity is unknown.

**LOW**

- the source term is ambiguous and the codebase does not resolve it,
- the target language needs grammatical information the app does not carry,
- the wording is culturally loaded, regional, or generation-dependent,
- the decision rests only on general knowledge of the language with nothing in
  the repository to check it against.

LOW-confidence decisions are always surfaced for review. A LOW-confidence
translation may still be written in LOCALIZE mode — with the flag — but it is
never presented as settled.

## Language claims

Never claim native authority. The difference matters:

| Do not write | Write instead |
| --- | --- |
| "Native speakers always say X." | "X is the more common convention in modern software for this locale." |
| "Y is wrong." | "Y is dictionary-valid but reads as formal/literary for a UI of this kind." |
| "Everyone uses the English term here." | "This project and the platform's own UI use the English term; the native alternative appears rarely." |
| "This is the correct translation." | "This is the strongest option given the context; the alternatives were A and B, rejected because …" |

State the basis of the claim in the same breath as the claim. "More common in
contemporary product usage" is a claim about software convention and is often
checkable. "More natural" without a basis is an opinion wearing a lab coat.

Regional, generational, professional and register variation are real for every
language. Never write "language X always …" — write "for this product's
audience, X is the safer default, because …".

## Uncertainty is output, not failure

The valuable part of a localization report is often the list of things a human
must decide. Surface them as specific, answerable questions:

- "The confirm button and the dismiss button both read *Cancel* in English but
  need different target verbs — is `common.cancel` used for both?"
- "Does this product address users formally or informally? The source copy is
  ambiguous and the choice affects roughly every second string."
- "Are these amounts always in one currency, or per-tenant?"

Compare with the useless version: "some strings may need review".

## Fabrication rules

- Never invent counts of strings, files, occurrences or users.
- Never claim a validation ran if it did not.
- Never cite a source, corpus, style guide or usage statistic you did not read.
- Never present a memory of how some product localizes a term as a verified
  observation; label it as recollection, or check it.
- If web access is unavailable, say the decision rests on context and existing
  project terminology rather than external evidence.
