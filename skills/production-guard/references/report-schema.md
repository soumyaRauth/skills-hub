# Report Schema

The production-readiness report's structure. Formatting may adapt to context;
the semantic structure may not. Omit sections with nothing relevant to say —
except `VERDICT`, which is always present.

## Skeleton

```
╔══════════════════════════════════════════╗
║       PRODUCTION GUARD REPORT            ║
╚══════════════════════════════════════════╝

CHANGE
<one or two sentences>

RISK CLASSIFICATION
<Low | Medium | High> — <why>

VERDICT
🔴 DO NOT SHIP

BLOCKERS  2      HIGH  1      MEDIUM  3      LOW  2

──────────────────────────────────────────

BASELINE
Scope:  <full suite | targeted: what>
Result: <n passed, n failed>
Pre-existing failures: <list, or none>

──────────────────────────────────────────

FUNCTIONAL VALIDATION    14/14 passed
REGRESSION VALIDATION    21/23 passed
SECURITY                  8/8  passed
DATA INTEGRITY            5/6  passed
FAILURE SCENARIOS         6/9  validated
PERFORMANCE               3/4  validated
OBSERVABILITY             2/4  validated

──────────────────────────────────────────

🔴 BLOCKERS

#1 <one-line statement of the defect>

   Category:       <security | data integrity | idempotency | ...>
   Evidence:       <file:line, test output, query, or "static analysis">
   Risk:           <what happens in production>
   Confidence:     <High | Medium | Low>
   Recommendation: <the fix>

──────────────────────────────────────────

⚠️ WARNINGS
<HIGH, then MEDIUM, then LOW, same field shape>

──────────────────────────────────────────

TESTS EXECUTED
<command>  →  <result>

──────────────────────────────────────────

UNVERIFIED
- <check> — <why it could not be validated>

──────────────────────────────────────────

RECOMMENDED ACTIONS
1. …

FINAL VERDICT
🔴 DO NOT SHIP — 2 blocking issues must be resolved.
```

## Counts

Every count is `passed / attempted` for checks you actually performed. A
category you did not run is omitted or marked `not applicable`, never reported
as `0/0 passed`.

Never emit a percentage, a letter grade, or a composite score. `18/20` is a
fact; `90% quality` is an invention, and the difference is the entire point of
this skill.

## Finding fields

| Field | Required | Notes |
| --- | --- | --- |
| Statement | yes | One line naming the defect, not the topic. |
| Category | yes | Functional, regression, security, data integrity, idempotency, concurrency, performance, observability, UX. |
| Evidence | yes | `file:line`, test output, query, config — or `static analysis / inferred behavior`. |
| Risk | yes | The production consequence, concretely. |
| Confidence | yes | High / Medium / Low, describing the strength of the evidence. |
| Recommendation | yes | The specific fix, not "consider improving this". |

## EXECUTED vs ANALYZED

Mandatory distinction, everywhere:

```
EXECUTED
  npm test -- users/bulkDelete.test.ts     →  PASS (12 tests)
  npx tsc --noEmit                         →  PASS
  npm run lint                             →  2 warnings, 0 errors

ANALYZED (not executed)
  Behavior at 100k records                 →  STATUS: UNVERIFIED
  External payment gateway timeout         →  STATUS: UNVERIFIED — no sandbox
                                              credentials in this environment
```

An analyzed check may still produce a finding, including a blocker — reading a
loop is enough to prove a missing transaction. What it may not do is claim an
observed result.

## Verdict rules

| Verdict | Rule |
| --- | --- |
| 🔴 DO NOT SHIP | ≥ 1 BLOCKER |
| 🟠 CONDITIONAL SHIP | 0 blockers, and (≥ 1 HIGH, or a risk-required category left UNVERIFIED) |
| 🟢 SHIP | 0 blockers, 0 unresolved HIGH, all risk-required categories validated |

State the rule that produced the verdict. If a HIGH finding is being knowingly
accepted, record it as an accepted risk with who accepted it — that is what
makes CONDITIONAL SHIP meaningful rather than a softer failure.

## Anti-patterns

- Any percentage or composite score.
- `ACTUAL` values for scenarios that were only reasoned about.
- Blaming pre-existing failures on the change.
- Blocker inflation — style issues, missing comments, or preferences.
- A verdict that does not follow from the findings.
- Silent omission of what could not be checked.
