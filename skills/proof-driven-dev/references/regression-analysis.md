# Regression Analysis

Half of every contract is *the new thing works*. The other half is *the old
things still do*. The second half is where the expensive failures live, because
nobody is looking there.

## Deriving the regression surface

For the change under construction, ask what shares:

| Shared thing | Example |
| --- | --- |
| Code path | The function you edited, and its other callers |
| Data | The table, column, or key the change writes |
| Contract | The endpoint's other clients, the component's other parents |
| Configuration | The limit, flag, or setting the change reinterprets |
| Assumption | Code that assumed the old shape, count, order, or nullability |

Adding **bulk upload** puts all five in play: the single-upload path (shared
code), storage and quota accounting (shared data), the upload API's existing
clients (shared contract), the size limit (shared configuration), and anything
that assumed one file per request (shared assumption).

`git grep` for the symbol, then for the *string* — raw SQL, config keys, and
serialized payloads never appear in an import graph.

## Turning the surface into requirements

Important regressions become numbered requirements with `proof: { type:
regression }`, so they carry the same weight as new behavior:

```yaml
- id: UPLOAD-010
  description: "Single-file upload behaves exactly as before"
  priority: critical
  proof: { type: regression, note: "existing tests/upload/single.test.ts, unchanged" }

- id: UPLOAD-011
  description: "Storage quota accounting is correct after a batch upload"
  priority: high
  proof: { type: integration, note: "sum of file sizes equals the quota delta" }
```

Not every neighbor deserves a requirement. The ones that do: anything a user
would notice, anything that loses data, anything the change's own code path runs
through.

## Targeted first, broad when justified

```
1. The existing tests over the files this change touched
2. The suite for the feature area
3. The full suite — when risk, breadth, or a surfaced failure justifies it
```

On a large repository, running everything for a two-line change is a cost with
no matching information gain. On a migration or an auth change, skipping the
broad run needs a stated reason.

Never report "no regressions" from a targeted run. Report what ran:

```
Regression   existing suites for auth/ and session/ — 62 passed
             full suite not run (~14 min); risk: medium
```

## Baseline before blame

Capture the pre-change state of whatever you intend to cite later — ideally by
running the relevant suite before implementing. Without a baseline, a red test
at the end is unattributable, and the choice between "I broke it" and "it was
already broken" gets made by convenience.

Never establish a baseline by modifying the developer's working tree —
no stash, no reset, no checkout. Read: CI history, the test file's last change,
recent commits touching the failure's code.

## Tests are not the whole surface

Green tests over untested behavior prove nothing about it. When the regression
surface includes code the suite does not cover, say so — that is a Level C
requirement, not a passing one:

```
UPLOAD-012  Existing webhook receivers still get one event per file
  Proof     none available — no test covers the webhook dispatcher
  Status    HUMAN · Level D
  Note      dispatch is unchanged by this diff (git diff shows no edits under
            src/webhooks/), but no executed check demonstrates the behavior
```

Static reasoning belongs in the note, never in the status.

## Snapshots and fixtures

Two ways a suite stays green while behavior breaks:

- **Snapshot updated in the same run that changed the output.** Regenerating a
  snapshot is not verification; it records the new behavior as correct by
  definition. If a snapshot must change, the diff is evidence to *look at* and
  the change gets stated explicitly.
- **A fixture that no longer resembles production.** A fixture asserting the old
  shape keeps CI green while real payloads fail. When a change alters a data
  shape, the fixtures that encode the old one are part of the regression surface.
