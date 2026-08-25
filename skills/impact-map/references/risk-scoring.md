# Risk Scoring

`RISK` used to be a judgment with an argument attached. The score makes the
argument explicit: six factors, each scored from evidence already in the report,
each carrying the observation that set it.

The score exists to make the reasoning inspectable and comparable between two
options for the *same* change. It is **not** a quality metric, not a percentage,
and not comparable across repositories or teams.

## The factors

Each is 0–3. Score from what the analysis observed — never from a feeling about
the change.

### 1. Breadth

| Score | Criterion |
| --- | --- |
| 0 | One file, one layer. |
| 1 | One layer, several files, or one package. |
| 2 | Three or more layers, or two or more packages in a workspace. |
| 3 | Multiple runtimes or deploy units (backend + frontend + jobs + reporting). |

### 2. Coupling opacity

| Score | Criterion |
| --- | --- |
| 0 | Only hard edges — imports, calls, type references. |
| 1 | One soft edge, in code that is tested. |
| 2 | Several soft edges: raw strings, raw SQL, config keys, duplicated logic. |
| 3 | Soft edges on a critical path, or duplicated business logic in three or more places, or coupling found only in git history. |

### 3. Test coverage of the surface

| Score | Criterion |
| --- | --- |
| 0 | Every MUST CHANGE location has a test that would fail if the change is wrong. |
| 1 | The main path is covered; edges are not. |
| 2 | Partial coverage, and the hidden-coupling findings are untested. |
| 3 | No test exercises the changed behavior — nothing in CI fails if the change is missed. |

Coverage is judged by **reading the tests**, not by counting files. A test that
asserts the fixture rather than the behavior counts as absent.

### 4. Reversibility

| Score | Criterion |
| --- | --- |
| 0 | Pure code change, revert is a revert. |
| 1 | Additive schema or additive field: reversible, sequencing matters. |
| 2 | Contract change (wire format, response shape, event payload) with consumers to coordinate. |
| 3 | Destructive or lossy data migration, or a change that cannot be rolled back once deployed. |

### 5. Consumer reach

| Score | Criterion |
| --- | --- |
| 0 | One caller, in this repository. |
| 1 | Several callers, all in this repository, all inspected. |
| 2 | Cross-team consumers, or a published package with in-repo dependents. |
| 3 | Consumers outside this repository — partner systems, mobile clients, a warehouse, or a registry release — that cannot be enumerated here. |

### 6. Area volatility

| Score | Criterion |
| --- | --- |
| 0 | Stable, actively maintained, clear ownership. |
| 1 | Normal churn. |
| 2 | High churn, or half-finished migrations visible in the surface. |
| 3 | No CODEOWNERS and no recent commits — nobody currently holds this code in their head — or churn concentrated in exactly the files being changed. |

Factor 6 comes from Phase 5. With no usable git history, mark it `?` (see below)
rather than scoring it 0.

## Bands

| Total | Risk |
| --- | --- |
| 0–4 | **Low** |
| 5–10 | **Medium** |
| 11–18 | **High** |

Floors that override the total:

- Reversibility 3 → at least **High**.
- Consumer reach 3 with no compatibility window → at least **High**.
- Test coverage 3 combined with coupling opacity 3 → at least **High**. Nothing
  fails loudly, and there are quiet edges to miss.

The band may be raised above the total with a stated reason. It is **never**
lowered below the total or below a floor.

## Unassessed factors

A factor that could not be assessed — no history, a package that could not be
inspected, tests that were not readable — is scored `?`, not 0.

With any `?` present, the total is reported as a **lower bound**:

```
Risk score: 9+ / 18  →  Medium (lower bound; area volatility not assessed —
                        shallow clone, no usable history)
```

Never round a `?` down to make a change look safe. An unknown is a reason the
number could only go up.

## Reporting

Show the factor table. A total without its factors is exactly the invented
number this skill forbids.

```
RISK

Risk score: 15 / 18 → High

Breadth             3   backend, frontend, jobs, and reporting all in scope
Coupling opacity    3   raw SQL, a direct-read job, and a duplicated string
                        comparison in the UI
Test coverage       3   no test asserts report or sync behavior for this status
Reversibility       2   value rename with an existing-row backfill
Consumer reach      3   a partner system reads the value through the sync job;
                        BI consumers are suspected and not enumerable here
Area volatility     1   normal churn, CODEOWNERS names the platform team

The three critical paths are string-coupled and untested: nothing in CI fails
if they are missed.
```

Every factor line names the observation that set it. The sentence under the
table states the two or three factors that actually drive the band — the score
supports the argument, it does not replace it.

## What the score is not

- Not a quality, health, or confidence percentage.
- Not comparable to another repository's score, or to another team's.
- Not a gate. Nothing here says "do not ship" — that is
  [Production Guard](../../production-guard/README.md)'s job, after the code
  exists.
- Not a substitute for the reader's judgment. It is the argument, written down
  so it can be disagreed with.
