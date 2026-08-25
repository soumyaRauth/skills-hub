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

REPOSITORY SCOPE

<only for a monorepo or a diff-driven analysis>
Workspace:      <tool and package count>
Change origin:  <package or the changed file set>
In scope:       <packages inspected, and why they are in scope>
Not inspected:  <packages skipped, and why>
Published:      <packages whose consumers live outside this repository>

CHANGE SURFACE

Directly relevant:  <short list or summary>
Must change:        <count or list>
Likely affected:    <count or list>
Needs verification: <count or list>
Hidden coupling:    <count or list>

🟥 MUST CHANGE

<F1> · <path/to/file>
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
 duplicated logic | event name | serialization | fixture | generated code |
 temporal (co-change)>

DEPENDENCY PATHS

<chain diagrams with the relationship named at each hop>

ARCHITECTURE GRAPH

<only when the surface branches or spans three or more layers>
<mermaid flowchart: one subgraph per real layer, nodes labelled by finding id,
 every edge labelled, solid = hard edge, dashed = soft edge>
<one line naming the convergence points, bypasses, and edges leaving the repo>

HISTORY & OWNERSHIP

<only when git history was usable; one line saying why not, when it was not>
Co-change:   <files that move with the change surface, as a ratio>
Churn:       <what is unsettled, what has not been touched in years>
Ownership:   <CODEOWNERS entries or contributor counts, as review routing>

DATABASE IMPACT

<schema, migration, data, and backfill considerations>

API IMPACT

<request/response shape, compatibility, validation, versioning, consumers>

AUTHORIZATION IMPACT

<policies, guards, roles, visibility>

TEST IMPACT

<test groups, the behavior each protects, and coverage gaps>

RISK

Risk score: <total> / 18 → Low | Medium | High

Breadth             <0-3>   <the observation that set it>
Coupling opacity    <0-3>   <…>
Test coverage       <0-3>   <…>
Reversibility       <0-3>   <…>
Consumer reach      <0-3>   <…>
Area volatility     <0-3|?> <…>

<the two or three factors that actually drive the band>

RECOMMENDED IMPLEMENTATION ORDER

<the coarse sequence only; the executable plan is a separate artifact, produced
 on request — see implementation-plan.md>
1. …
2. …

OPEN QUESTIONS

- <decisions a human must make>
```

## Finding fields

| Field | Required | Notes |
| --- | --- | --- |
| Id | yes | `F1`, `F2`, … in report order. Stable within the report; never reused. |
| Path | yes | Repository-relative. |
| Symbol | when meaningful | The specific class, function, column, or route — not the whole file. |
| Relationship | yes | One sentence describing the connection, in the direction that matters. |
| Evidence | yes | What was actually observed. "Imports X", "queries table Y", "compares against the literal `'completed'`". |
| Confidence | yes | High / Medium / Low, describing the strength of the evidence. |
| Action | yes | For MUST CHANGE / LIKELY AFFECTED: the edit. For NEEDS VERIFICATION: the check. |
| Coupling type | hidden coupling only | Which indirect mechanism was found. |

## REPOSITORY SCOPE rules

- Include the section whenever the repository is a monorepo, or the analysis
  started from a diff, branch, or commit range. Omit it otherwise.
- Scope is set by the dependency graph, not by directory proximity.
- `Not inspected` is a required line whenever anything was skipped. Naming the
  boundary is what makes partial coverage usable.
- For a diff-driven analysis, list the already-changed files here and keep them
  out of MUST CHANGE unless they are wrong, not merely present.

## HISTORY & OWNERSHIP rules

- Every number comes from a command that actually ran. No estimates.
- Co-change is reported as a ratio ("9 of the 12 commits"), never as a bare
  count, and never with an asserted reason for the correlation.
- History alone caps a finding at Medium confidence.
- Ownership is review routing. Never attribution, never a judgment about the
  people named, and `git blame` output is not evidence of a defect.
- When history is unusable — shallow clone, squash merges, single founding
  commit — say which one applies instead of omitting the section silently.

## CHANGE SURFACE rules

- Counts are optional. Include one only when it was actually produced by the
  analysis.
- "Files examined" is usually not reliably countable — prefer a phrase such as
  "reconnaissance across the API, service, and persistence layers".
- Never round, estimate, or invent a total to make the report look thorough.

## ARCHITECTURE GRAPH rules

- The graph renders findings already in the report; it introduces nothing.
- Linear surface → chains only. Branching or three-plus layers → graph and
  chains. More than ~20 nodes → collapse to modules and name what was collapsed.
- Every edge is labelled with the observed relationship; unlabelled arrows are
  decoration.
- Solid = hard edge (import, call, foreign key). Dashed = soft edge (string,
  raw SQL, config, convention, co-change).
- Conventions and the ASCII alternative: `architecture-graph.md`.

## RISK rules

Six factors, each 0–3, each printed with the observation that set it; total
bands at 0–4 Low, 5–10 Medium, 11–18 High. Full rubric: `risk-scoring.md`.

- The factor table is mandatory. A total without its factors is an invented
  number.
- An unassessable factor is scored `?`, and the total is then reported as a
  lower bound (`9+ / 18`). Never rounded down.
- Floors — irreversible migration, unreachable external consumer, untested plus
  string-coupled — set a minimum band regardless of the total.
- The band may be raised with a stated reason; never lowered.
- The score is not a quality metric, not a percentage, and not comparable across
  repositories.

## Anti-patterns

- A bare list of file paths with no relationship or evidence.
- MUST CHANGE on Low confidence.
- OUT OF SCOPE used to pad the report. Include it only where a reader would
  otherwise reasonably expect that file to appear.
- Invented consumers ("the mobile app probably reads this") without evidence.
- Producing code, diffs, or migrations inside the report.
