# Evidence Model

Evidence is what makes a status a claim rather than an opinion. It is judged on
five properties:

- **Relevant** — it demonstrates *this* requirement, not a neighboring one.
- **Reproducible** — it names the command, so someone else can run it.
- **Minimal** — the lines that decide the outcome, not the whole log.
- **Machine-readable** — structured, so it survives past the conversation.
- **Traceable** — attached to exactly one requirement id.

```
Bad     "I checked it and it looks fine."
Bad     "The token logic is correct — it sets used_at."
Good    Command   npm test -- reset-password.test.ts -t "rejects reused token"
        Expected  second use of a consumed token is rejected
        Actual    PASS — 1 passed · POST /auth/reset/confirm → 400 token_invalid
        Status    PASS · Level A
```

The difference between the second and third lines is the whole skill: the second
describes the code, the third describes what happened when it ran.

## Evidence record

One JSON file per requirement, under `.proofbuild/evidence/`:

```json
{
  "requirement": "AUTH-005",
  "description": "A reset token cannot be used twice",
  "method": "integration",
  "command": "npm test -- reset-password.test.ts -t \"rejects reused token\"",
  "expected": "Second use of a consumed token is rejected",
  "actual": "PASS — 1 passed. Response: 400 {\"error\":\"token_invalid\"}",
  "status": "PASS",
  "level": "A",
  "attempts": 2,
  "notes": "First attempt failed: used_at was written after the response."
}
```

Fields: `requirement` and `status` are required; `command`, `expected`, and
`actual` are required whenever something ran. `level` is A–D. `attempts` records
repair iterations. Add `timestamp` when the environment supplies one — do not
invent it. Extra fields are fine; a missing `command` on a `PASS` is not.

`status` is one of `PASS`, `FAIL`, `BLOCKED`, `HUMAN`. `BLOCKED` carries the
reason the check could not run. `HUMAN` carries what a person must judge.

## What never goes in evidence

Tokens, API keys, passwords, session cookies, authorization headers, connection
strings, private keys, customer names, email addresses, payment details, and
anything else from a real dataset.

This matters more here than in a log file, because `.proofbuild/` is committed.
Redact by shape, keeping what makes the evidence meaningful:

```
Actual    401 {"error":"invalid_token"} for Authorization: Bearer <redacted>
Actual    inserted 1 row into password_resets (user_id=<test-user-1>, token=<redacted>)
```

Test fixtures with obviously fake values are fine. Anything copied from a real
environment is not — and if a check requires real credentials to run, the
credential belongs in the environment, never in the record of the run.

Keep output small: the assertion, the status line, the counts, the specific
error. A 4,000-line stack trace becomes the first frame in your code plus the
error. If a long log is genuinely needed, keep the relevant excerpt and say what
was elided.

## The artifact directory

```
.proofbuild/
├── contract.yml            objective, risk, assumptions, requirements
├── proof-plan.yml          mechanism, command, and stage per requirement
├── evidence/
│   ├── AUTH-001.json
│   └── AUTH-005.json
├── reports/
│   └── latest.md           the compressed result, in full
└── history/
    └── 001-contract.yml    superseded versions
```

Write it when the work is substantial, spans sessions, or is high risk. Skip it
for a typo — an artifact nobody reads is noise in the diff.

Two rules about the directory itself. It is *yours to write*, but committing it
is the developer's decision, like any other file: do not commit automatically.
And when a repository is not yours to add directories to, keep the contract
inline in the conversation instead. Mention `.gitignore` once if the developer
would rather not track it; do not edit their ignore file uninvited.

## Evidence outlives the conversation

The reason for structure rather than prose: a later session — or another agent,
or the developer in six weeks — can read `contract.yml` plus `evidence/` and
know exactly what was claimed, what was run, and what was never verified. A
transcript cannot give them that.

That is also why `history/` exists. A contract that was amended mid-run tells a
story worth keeping: the requirement that turned out to be wrong is usually
where the interesting part of the problem was.
