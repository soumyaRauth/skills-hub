# Evidence

Everything this skill claims rests on something it read or ran. The difference
between a useful standards report and a generic one is not the standards — it is
whether a senior engineer can check the citations and find them accurate.

## Categories

| | Meaning | Typical use |
| --- | --- | --- |
| `DIRECT` | Code or configuration explicitly demonstrates the control | Supports `PASS` or `FAIL` at `HIGH` confidence |
| `INDIRECT` | Supporting signals suggest it without demonstrating it | Supports `PARTIAL`, or `PASS` at `MEDIUM` |
| `MISSING` | Expected evidence searched for and not found | Supports `UNABLE TO VERIFY` — **not** `FAIL` |
| `CONTRADICTORY` | Different parts of the system disagree | Often the highest-value finding available |
| `EXTERNAL` | The control lives outside the repository | Supports `REQUIRES MANUAL REVIEW`, inherited-control note |
| `UNKNOWN` | Not enough information to categorize | Say so |

`CONTRADICTORY` deserves special attention. Two authorization paths that
disagree, a retention policy in the docs that no job implements, a security
header set in one environment and not another — these are where the real
problems live, because both halves look correct in isolation.

## Sources, in rough order of strength

```
Running code and executed tool output  →  strongest, when the environment allows it
Application source                     →  what the system does
Database schema and migrations         →  what it stores, and what it lets happen
Configuration and infrastructure code   →  what it intends to deploy
Dependency manifests and lockfiles      →  what it pulls in
CI/CD definitions                       →  what is enforced before merge
API definitions                         →  the contract, if it is real
Tests                                   →  which claims are actually checked
Documentation                           →  what someone believed at some point
Git history                             →  when and why something changed
```

Documentation is evidence of intent, not of behaviour. Where a document and the
code disagree, the code wins and the disagreement is itself a finding.

## Citations

- File path always. Line numbers **only when actually obtained** from a read or
  a search result. Never estimate a line number, never adjust one to look
  precise. A wrong line number destroys the reader's trust in every other
  citation in the document.
- A range is fine when the finding spans a block: `src/api/admin/users.ts:41-67`.
- For a pattern across many files, cite two or three real examples and state the
  count you actually observed.
- For an absence, cite the search: *"no match for `backup|snapshot|pg_dump`
  across the repository, and no scheduled job definitions under `ops/`"*. An
  unevidenced absence is an assumption wearing a finding's clothes.

## Executed versus analyzed

Label every check. Where the project's own tooling exists and the environment
allows it, run it — a dependency audit, the test suite, a linter, a type check,
a secret scanner — and label the result `EXECUTED`, quoting what the tool
actually printed. Everything else is `ANALYZED`.

Claiming to have run something you did not is the most serious failure available
here, ahead of missing a finding.

## Tool output is a lead, not a finding

A scanner reporting 100 issues has produced 100 leads. Classify each:

| | |
| --- | --- |
| `CONFIRMED` | Traced into the code and the mechanism is real |
| `LIKELY` | Consistent with the code, not fully traced |
| `POTENTIAL` | Plausible, needs a human |
| `FALSE POSITIVE` | The path is unreachable, the input is trusted, the pattern is misread — say why |
| `NEEDS REVIEW` | Cannot be adjudicated from the repository |

Report the confirmed ones as findings and summarize the rest by count and class.
"npm audit reports 43 vulnerabilities" is not an assessment; "3 reach reachable
code paths, 12 are dev-only, 28 are transitive under a dependency that does not
call the affected function" is.

A dependency being old is not a vulnerability. Say "outdated" and reach for a
vulnerability source before saying "vulnerable".

## Secrets

If credentials appear in the repository:

- **Never print the value.** Redact to a stub that identifies the kind:
  `sk_live_****`, `-----BEGIN ... PRIVATE KEY-----` (elided), `AKIA****`.
- Cite the file and, where relevant, the commit that introduced it.
- Severity depends on exposure: a live credential in a public repository is
  critical; a placeholder in an example file may be informational.
- Check git history — a removed secret that remains in history is still exposed,
  and the remediation is rotation, not deletion.

## Evidence for what is working

Positive evidence is collected with the same discipline as negative. "Password
hashing uses argon2id with parameters set in `src/auth/hash.ts:12`" belongs in
the report. A findings-only document tells the reader nothing about what to
avoid breaking.

## Large repositories

Do not read everything. Investigate in risk order — identity, privilege, money,
personal data, external input, uploads, AI boundaries, deployment, secrets — and
expand where the first pass finds something. Record which areas were assessed
and which were not; an audit with a stated scope is credible, and one that
implies total coverage it did not perform is not.
