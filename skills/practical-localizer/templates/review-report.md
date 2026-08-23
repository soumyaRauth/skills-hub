# Localization review — <target locale>

<!--
Template for REVIEW mode output. Delete every section that has no content
rather than filling it with padding, and delete a count you did not actually
produce. See references/review-methodology.md.
-->

## Scope

| | |
| --- | --- |
| Source locale | |
| Target locale | |
| Files reviewed | |
| Strings reviewed | |
| Passes run | coverage · technical · terminology · register · naturalness · mechanics |
| Not reviewed | <what was skipped, and why> |
| Evidence | <in-repo context only, or external sources consulted> |

## Summary

| Severity | Count |
| --- | --- |
| Blocking technical | |
| High | |
| Medium | |
| Low | |

Terminology conflicts: ·  Missing translations: ·  Untranslated (identical to source):

## Blocking technical issues

```
#1
  Key          
  Source       
  Current      
  Problem      <placeholder / ICU / plural / structure defect>
  Effect       <what the user sees>
  Fix          
  Confidence   HIGH (mechanical)
```

## Language findings

```
#2
  Key          
  Source       
  Current      
  Recommended  
  Category     naturalness | terminology | tone | grammar | transliteration
               | should-stay-source | cultural fit | locale format | UI fit
  Reason       <what the recommendation rests on — project evidence first>
  Confidence   HIGH | MEDIUM | LOW
  Fix scope    <single key | every occurrence of this term | needs a key split>
```

## Terminology

| Concept | Terms in use | Occurrences | Recommended | Confidence |
| --- | --- | --- | --- | --- |
| | | | | |

## Locale mechanics

| Area | Observation | Action |
| --- | --- | --- |
| Dates / times | | |
| Numbers | | |
| Currency | | |
| Direction | | |
| UI fit | | |

## Review required

Items no amount of context resolves — each with the specific missing
information and the options considered.

- **<key>** — <what the target language needs and the source does not carry>

## Recommended order of work

1. Blocking technical fixes — mechanical, no linguistic judgement needed
2. Terminology alignment — one change per concept, applied everywhere
3. High-severity language findings
4. Locale mechanics, in application code
5. Medium and low findings

## Not verified

<what could not be checked: rendering, native review, external terminology
evidence, runtime data. State it plainly rather than letting the report imply
the locale is ready.>
