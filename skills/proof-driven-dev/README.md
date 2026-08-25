# ProofBuild

### Don't read what the AI did. See whether it actually works.

ProofBuild is an [Agent Skill](https://code.claude.com/docs/en/skills) that
changes what an AI coding agent hands back. Instead of code plus an explanation
of the code, you get an outcome contract, evidence that each requirement in it
holds, and one of three answers.

```bash
npx skills add soumyaRauth/skills-hub --skill proof-driven-dev
```

---

## The problem

You ask for password reset. Twenty minutes later:

> *"I've implemented password reset. I created a `PasswordResetToken` model,
> added two endpoints, wired up the mailer, and updated the auth service.
> The token is invalidated after use and expires after an hour…"*

Now what? The explanation is fluent and the code compiles. Whether the feature
*works* is still your problem — and the only way to find out is to read the
diff, or ship it and wait.

The failure is structural, not a matter of the agent trying harder. **"Code was
written" and "the outcome happened" are different claims**, and one is being
reported as the other.

## The change

```
Before                              After

prompt                              intent
  ↓                                   ↓
code                                outcome contract
  ↓                                   ↓
explanation                         proof plan
  ↓                                   ↓
you read everything                 implementation
  ↓                                   ↓
you decide if it works              verification
                                      ↓
                                    repair
                                      ↓
                                    ✓ VERIFIED
```

The developer's job moves from *reconstructing what the AI did* to *reading one
line and, occasionally, making one decision*.

---

## What you actually see

```
✓ VERIFIED

Password reset

Requirements   8/8
Tests          47/47
Regression     pass
Changed        6 files
```

That is the whole response for a change touching six files. Behind it: a
contract with eight numbered requirements, a proof for each one, a failed
verification, a diagnosis, a repair, and a re-verification — all available if you
ask, none of it in your way if you don't.

When a decision is genuinely yours:

```
⚠ REVIEW REQUIRED

Bulk upload · 13/14 requirements verified

Decision required:
A duplicate filename inside one upload batch —

  [overwrite]   [reject the duplicate]   [keep both, suffix the name]
```

When it doesn't work:

```
✗ BLOCKED

Checkout · 11/12 requirements verified

CHECKOUT-009  Session expires on wall-clock time, not idle time — an active
              user is signed out mid-checkout.
Cause         expiry derives from session.createdAt; no activity timestamp
              exists on the session record.
Attempts      3 (refresh-on-request, sliding expiry, lastSeenAt column)
Blocker       lastSeenAt changes a schema shared with the mobile token contract.

Decision required: extend the session record, or scope expiry to web only?
```

Three answers. The one thing you never get is a green checkmark that means
"I wrote some code and it looked right to me."

---

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill proof-driven-dev
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill proof-driven-dev --agent claude-code
```

Skills are selected by their description, so there is no command to remember.
It applies when you ask for work to be done — and you can invoke it explicitly:

```
Use proof-driven development for this.
Implement password reset and prove the acceptance criteria.
Fix this bug — don't mark it complete until the behavior is verified.
```

Mid-run and afterward, plain requests get the detail back:

```
show the contract          show evidence          explain the proof for AUTH-005
show what changed          show failed attempts   why is this verified?
```

---

## How it works

```
1  Compile the intent            objective, not a task list
2  Investigate the repository    the code answers most "ambiguity"
3  Classify risk                 low · medium · high · critical
4  Resolve ambiguity             ask only what changes the implementation
5  Write the outcome contract    numbered, observable requirements
6  Plan the proof                what evidence would establish each one
7  Implement
8  Verify in stages              static → targeted → integration → broad
9  Classify failures             before touching any code
10 Repair, with a budget         3 attempts, fewer at high risk
11 Determine status              from the evidence, not from an impression
12 Respond compressed            detail on demand
```

Steps 1–6 happen **before** any code is written. That ordering is the whole
design: you cannot prove an outcome that was never defined, and a suite written
after the implementation tends to assert what the code does rather than what was
wanted.

## Outcome contracts

Every meaningful task becomes a contract first:

```yaml
objective: "Users can securely reset their password by email"
risk: high
requirements:
  - { id: AUTH-001, description: "A user can request a reset for their email",   proof: { type: integration } }
  - { id: AUTH-003, description: "An unknown email returns the same response",   proof: { type: security } }
  - { id: AUTH-005, description: "A token already used once is rejected",        proof: { type: security } }
  - { id: AUTH-007, description: "After reset, the old password no longer works", proof: { type: integration } }
  - { id: AUTH-008, description: "Existing email/password login is unchanged",   proof: { type: regression } }
```

A requirement is *observable* — someone outside the codebase could tell whether
it holds. "Token handling is secure" is not a requirement; "a reset token is
rejected after its first successful use" is.

Most of the value is in the requirements you did not ask for: the negatives, the
boundaries, and the existing behavior that must survive. In the worked example
in [`examples/feature-development.md`](examples/feature-development.md), five of
eight requirements were unstated — and one of them caught a real defect.

Details: [`references/outcome-contracts.md`](references/outcome-contracts.md).

## Verification

Proof is whatever demonstrates the requirement, chosen for cost:

| | |
| --- | --- |
| Static | typecheck · lint · build |
| Tests | unit · integration · API · E2E, using the project's own framework |
| Runtime | probes, database inspection, filesystem checks |
| Visual | browser interaction, screenshots |
| Measured | benchmarks against a recorded baseline |
| Regression | the suites that already exist |

Staged, so cost tracks risk:

```
Stage 1  typecheck · lint · build          seconds, catches the common case
Stage 2  targeted tests per requirement
Stage 3  integration · API · database
Stage 4  E2E · browser · full regression   when risk or breakage demands it
```

And the check that matters most — **contradiction detection**. When the agent's
model of the code and the executed output disagree, the output wins:

```
Reasoning   "the token is invalidated after use — consumeToken() sets used_at"
Observed    the same token reset the password twice, both returning 200

✗ CONTRADICTION — AUTH-005 is not satisfied
```

That is the difference between a system that verifies and one that narrates.

Details: [`references/proof-strategies.md`](references/proof-strategies.md),
[`references/verification-loops.md`](references/verification-loops.md).

## The repair loop

A failing check is classified before any code changes:

`IMPLEMENTATION_ERROR` · `TEST_ERROR` · `CONTRACT_ERROR` · `ENVIRONMENT_ERROR` ·
`EXISTING_REGRESSION` · `UNRELATED_FAILURE` · `UNKNOWN`

A missing dependency is not a broken implementation. A test that was red before
you started is not your regression. Misattribution is how an agent starts
rewriting working code to satisfy a failure it never understood.

Repair is budgeted — three attempts per requirement, two at high risk, one at
critical — and the budget running out produces `✗ BLOCKED` with a diagnosis, not
a fourth attempt. Weakening a test to make it pass is never a repair.

Details: [`references/failure-analysis.md`](references/failure-analysis.md).

## Risk levels

| Risk | Examples | Proof floor | Repairs |
| --- | --- | --- | --- |
| **Low** | Copy, styling, docs | Build/lint/typecheck + the one check that would catch a mistake | 3 |
| **Medium** | CRUD, API shape, UI state | Targeted checks per requirement + existing suites for the area | 3 |
| **High** | Auth, migrations, destructive ops, multi-tenancy | The above + negative and boundary cases + regression evidence | 2 |
| **Critical** | Payments, credentials, irreversible operations | The above + replay/idempotency + rollback — and stop for a human sooner | 1 |

Evidence proportional to risk, in both directions: a typo does not get a 40-test
suite, and a payment path does not get a typecheck and a shrug.

Details: [`references/risk-model.md`](references/risk-model.md).

## Evidence

For substantial work, proof is written down in a form that outlives the
conversation:

```
.proofbuild/
├── contract.yml            objective, risk, assumptions, requirements
├── proof-plan.yml          the mechanism chosen per requirement
├── evidence/AUTH-005.json  command, expected, actual, status, level
├── reports/latest.md       the full result
└── history/                superseded contracts
```

```json
{
  "requirement": "AUTH-005",
  "command": "npm test -- reset-password.test.ts -t \"rejects reused token\"",
  "expected": "Second use of a consumed token is rejected",
  "actual": "PASS — 1 passed. Response: 400 {\"error\":\"token_invalid\"}",
  "status": "PASS",
  "level": "A"
}
```

Never in evidence: tokens, keys, cookies, connection strings, or real customer
data. Redacted by shape, so the record stays meaningful and safe to commit.

Details: [`references/evidence-model.md`](references/evidence-model.md).

## Human judgment

Some requirements no check can settle. Saying so is what keeps the rest
credible.

```
"Make the settings page feel premium"

  ✓ Level A   Every control reachable by keyboard
  ✓ Level A   Contrast meets WCAG AA           (axe: 0 violations)
  ✓ Level A   Layout holds at 320 / 768 / 1440 (screenshots attached)
  ✓ Level B   Interaction states for every control
  ⚠ Level D   Whether it reads as "premium"    ← yours
```

Four levels: **A** an executed check demonstrates it · **B** several independent
checks support it · **C** partly unreachable in this environment · **D** human
judgment. A Level C or D requirement means `⚠ REVIEW REQUIRED` — it never
rounds up to verified.

Details: [`references/human-judgment.md`](references/human-judgment.md).

## Examples

| | |
| --- | --- |
| [`feature-development.md`](examples/feature-development.md) | Password reset — a contradiction caught, classified, and repaired |
| [`bug-fix.md`](examples/bug-fix.md) | Checkout — the bug must fail a test *before* it is fixed |
| [`refactoring.md`](examples/refactoring.md) | The contract whose objective is that nothing changes |
| [`performance.md`](examples/performance.md) | Measured baseline, and an honest "not measurable here" |
| [`security.md`](examples/security.md) | Seven of ten requirements are negative cases; the defect lived in one |
| [`ambiguous-request.md`](examples/ambiguous-request.md) | Nine questions raised, eight answered by the repository, one asked |

## Limitations

- **It does not replace your tests.** It orchestrates the verification your
  project already has around explicit outcomes. In a repository with no test
  infrastructure, proof is thinner and the skill says so.
- **It cannot verify what the environment cannot run.** No database, no
  credentials, no browser — those requirements come back `BLOCKED`, not passed.
- **It cannot verify taste.** Visual quality, API elegance, and "is this the
  right architecture" are Level D by construction.
- **It is not a security audit.** It proves the properties it tested. That set
  is always smaller than "secure".
- **Contract quality bounds everything.** A requirement nobody wrote is a
  requirement nobody proved — which is exactly why the contract is reviewable
  before implementation starts.
- **It costs more than "just write the code."** Defining outcomes and verifying
  them takes real time. That is the trade: on a typo it is overhead, on a
  payments change it is the cheapest part of the week.

## Roadmap

| | |
| --- | --- |
| **v0.1** *(this release)* | Core skill: outcome contracts, staged verification, failure classification, repair budget, compressed results |
| v0.2 | Richer evidence formats, sharper risk classification, project-specific proof strategies |
| v0.3 | Screenshot-aware verification, browser evidence, stored performance baselines |
| v0.4 | CI integration; detecting when a previously proven requirement regresses |
| v0.5 | Reusable project-level proof contracts |
| Later | Proof artifacts that survive across agents, team quality policies, historical proof comparison |

## Positioning, honestly

Verification systems, testing agents, and code-review agents already exist.
ProofBuild is not the first of anything. What it combines:

**an outcome contract written before implementation** + **evidence traced to
each requirement** + **classified failures with budgeted repair** + **output
optimized for the developer's attention rather than for completeness**.

It is not a test generator (tests are one mechanism, chosen before the code), not
a code reviewer (the question is whether the outcome happened, not whether the
code looks right), and not a QA pass (it starts before implementation, because
an undefined outcome cannot be proven).

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md). Fixtures for this skill live in
[`tests/fixtures/proof-driven-dev/`](../../tests/fixtures/proof-driven-dev), and
what a correct run looks like on each one is documented in
[`tests/README.md`](../../tests/README.md).

## License

MIT — see [LICENSE](../../LICENSE).
