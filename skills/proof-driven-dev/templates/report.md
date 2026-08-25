# Proof report — `.proofbuild/reports/latest.md`

The full record. The message the developer sees is the compressed form at the
top; everything below it is available on request.

---

```
✓ VERIFIED

<Objective in three words>

Requirements   8/8
Tests          47/47
Regression     pass
Changed        6 files
```

---

## Contract

**Objective** — one sentence.
**Risk** — level, and why.

**Assumptions**
- Resolved without asking, with the evidence that made it safe.

## Requirements

| id | Requirement | Priority | Status | Level | Evidence |
| --- | --- | --- | --- | --- | --- |
| AREA-001 | … | critical | PASS | A | `evidence/AREA-001.json` |
| AREA-002 | … | critical | PASS | A | `evidence/AREA-002.json` |
| AREA-005 | … | normal | HUMAN | D | screenshots |

Status: `PASS` · `FAIL` · `BLOCKED` · `HUMAN`
Level: **A** executed check demonstrates it · **B** several independent checks
support it · **C** partly unreachable here · **D** human judgment.

## Verification

```
Stage 1  typecheck · lint · build          pass
Stage 2  targeted tests                    <real counts from the runner>
Stage 3  integration                       <real counts>
Stage 4  full suite                        <ran / not run, and why>
```

Only numbers copied from real output. No estimates.

## Regression

What ran, and what did not:

```
Existing suites for <area>/  —  62 passed
Full suite not run (~14 min); risk: medium
```

## Repair history

| # | Requirement | Failure | Classification | Fix | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | AREA-002 | … | IMPLEMENTATION_ERROR | … | pass |

## Not verified

Every requirement that is `BLOCKED` or `HUMAN`, with the reason — the section
that makes the rest of the report trustworthy.

```
AREA-007  BLOCKED · environment
  Needed   <the missing service, credential, or fixture>
  Effect   <which behavior is unverified as a result>
```

## Contract amendments

```
AREA-004  expiry 24h → 1h  (matches existing invite TTL; 24h was assumed)
```

Omit the section when nothing was amended. Never omit it when something was.

## Changed files

Grouped by requirement, not by directory — the developer's question is *what
satisfies AREA-002*, not *what is in src/*.
