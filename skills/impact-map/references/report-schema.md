# Report Schema

The exact structure of an Impact Map report. Section order is fixed. Sections
with nothing relevant to say are omitted — an empty `AUTHORIZATION IMPACT`
heading is noise, not thoroughness.

## Skeleton

```
IMPACT MAP
────────────────────────────────────────

REQUEST

<the change statement, one or two sentences>

INTERPRETATION

<only when the request was ambiguous: the reading being used, and what was
 assumed away>

CHANGE SURFACE

Directly relevant:  <short list or summary>
Must change:        <count or list>
Likely affected:    <count or list>
Needs verification: <count or list>
Hidden coupling:    <count or list>

🟥 MUST CHANGE

<path/to/file>
  Symbol:         <class, function, component, column, route>
  Relationship:   <how it connects to the change>
  Evidence:       <what was observed, with line or snippet where useful>
  Confidence:     High | Medium | Low
  Action:         <what needs to happen here>

🟧 LIKELY AFFECTED

<same finding shape>

🟨 NEEDS VERIFICATION

<same finding shape; Action describes the check to run, not the edit>

⚠️ HIDDEN COUPLING

<same finding shape, plus Coupling type: raw string | raw SQL | config |
 duplicated logic | event name | serialization | fixture | generated code>

DEPENDENCY PATHS

<chain diagrams with the relationship named at each hop>

DATABASE IMPACT

<schema, migration, data, and backfill considerations>

API IMPACT

<request/response shape, compatibility, validation, versioning, consumers>

AUTHORIZATION IMPACT

<policies, guards, roles, visibility>

TEST IMPACT

<test groups, the behavior each protects, and coverage gaps>

RISK

Low | Medium | High

<why — breadth, hidden coupling, coverage, external consumers>

RECOMMENDED IMPLEMENTATION ORDER

1. …
2. …

OPEN QUESTIONS

- <decisions a human must make>
```

## Finding fields

| Field | Required | Notes |
| --- | --- | --- |
| Path | yes | Repository-relative. |
| Symbol | when meaningful | The specific class, function, column, or route — not the whole file. |
| Relationship | yes | One sentence describing the connection, in the direction that matters. |
| Evidence | yes | What was actually observed. "Imports X", "queries table Y", "compares against the literal `'completed'`". |
| Confidence | yes | High / Medium / Low, describing the strength of the evidence. |
| Action | yes | For MUST CHANGE / LIKELY AFFECTED: the edit. For NEEDS VERIFICATION: the check. |
| Coupling type | hidden coupling only | Which indirect mechanism was found. |

## CHANGE SURFACE rules

- Counts are optional. Include one only when it was actually produced by the
  analysis.
- "Files examined" is usually not reliably countable — prefer a phrase such as
  "reconnaissance across the API, service, and persistence layers".
- Never round, estimate, or invent a total to make the report look thorough.

## RISK calibration

| Level | Typical shape |
| --- | --- |
| Low | Single layer, no hidden coupling, existing tests cover the behavior, no external consumers. |
| Medium | Several layers, some indirect coupling, partial test coverage, internal consumers only. |
| High | Schema or contract change, hidden coupling found, weak or missing coverage, external or cross-team consumers, or irreversible data migration. |

Risk is argued, never asserted. State the two or three factors that set it.

## Anti-patterns

- A bare list of file paths with no relationship or evidence.
- MUST CHANGE on Low confidence.
- OUT OF SCOPE used to pad the report. Include it only where a reader would
  otherwise reasonably expect that file to appear.
- Invented consumers ("the mobile app probably reads this") without evidence.
- Producing code, diffs, or migrations inside the report.
