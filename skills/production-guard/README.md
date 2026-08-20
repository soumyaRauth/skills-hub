# Production Guard

An Agent Skill that answers the question a code review does not:

> **What happens to the product when this change reaches real users?**

Production Guard validates a change's behavior, regressions, failure modes,
security boundaries, data integrity, performance, and operational readiness —
running the checks your project already has where it can, reasoning where it
cannot, and always telling you which was which. It ends in one verdict:
🟢 SHIP, 🟠 CONDITIONAL SHIP, or 🔴 DO NOT SHIP.

---

## Why it exists

AI agents made code generation cheap. They did not make it safe:

```
code generation ≠ production correctness
```

A change can pass its tests, compile, look reasonable, satisfy the ticket — and
still break an existing workflow, expose another tenant's data, corrupt records
under concurrency, double-charge on retry, time out at real data volumes,
silently swallow errors, or leave no trace of what it did at 3 AM.

Production Guard exists to find those before production, and to be honest about
what it could not check.

## What makes it different from code review

| Code review asks | Production Guard asks |
| --- | --- |
| Does this code look correct? | What happens when this reaches real users? |
| Are there bugs in the diff? | What existing behavior could this break? |
| Is this readable and idiomatic? | How does this fail, and can it recover? |
| Does it have tests? | What do the tests *prove*, and what is still unverified? |
| — | If this runs twice, does it do the thing twice? |
| — | If it fails halfway, what state is left behind? |

It is behavior-oriented, not diff-oriented. The diff is where it starts, not
what it grades.

## No invented scores

The single most important rule. Production Guard never emits:

```
Code quality: 94%     Security: 87%     Overall: 91%
```

Those numbers feel authoritative and mean nothing. Instead it reports what it
actually did:

```
FUNCTIONAL VALIDATION     14/14 passed
REGRESSION VALIDATION     21/23 passed
SECURITY                   8/8  passed
DATA INTEGRITY             5/6  passed
FAILURE SCENARIOS          6/9  validated
```

and derives the verdict from explicit rules:

| Verdict | Rule |
| --- | --- |
| 🔴 **DO NOT SHIP** | At least one BLOCKER |
| 🟠 **CONDITIONAL SHIP** | No blockers, but a HIGH finding or a required category left unverified |
| 🟢 **SHIP** | No blockers, no unresolved HIGH findings, all risk-required categories validated |

If the verdict looks wrong, the findings are wrong. The rule is not negotiable.

## Executed vs analyzed

The other rule that makes the report trustworthy. Every check is labeled:

```
EXECUTED
  pytest tests/payments/ -q          →  24 passed
  npx tsc --noEmit                   →  PASS

ANALYZED (not executed)
  Behavior at 100k records           →  STATUS: UNVERIFIED
  Provider timeout handling          →  STATUS: UNVERIFIED — no sandbox creds
```

Reasoning is legitimate evidence — reading a loop is enough to prove a missing
transaction. Presenting reasoning as an observed test result is not. A failure
matrix only gets an `ACTUAL` column value when the scenario was actually run.

---

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill production-guard
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill production-guard --agent claude-code
```

No MCP server, no CLI, no hosted service. The skill uses the repository
inspection and command execution your agent already has.

### Invoking it

Installed skills are matched by description, so ask for what it does:

```
Is this change safe to ship?
Run a production readiness check on the bulk delete feature.
Validate this before I merge it — it touches payments.
What breaks in production if I ship this?
```

## Usage

```
You:   I finished the bulk delete feature. Is it safe to ship?

Agent: I'll validate this before you merge. It's destructive and multi-record,
       so I'm treating it as high risk.

       [establishes baseline, builds the behavioral model, runs the suite,
        probes failure scenarios, checks authorization and data integrity]

       ╔══════════════════════════════════════════╗
       ║       PRODUCTION GUARD REPORT            ║
       ╚══════════════════════════════════════════╝

       VERDICT  🔴 DO NOT SHIP
       BLOCKERS 2   HIGH 2   MEDIUM 1   LOW 1
       …

       Want me to fix the blockers?
```

It stops at the report. Fixes happen only when you ask.

### Risk-based depth

Not every change earns every check. The skill classifies first:

| Risk | Examples | What runs |
| --- | --- | --- |
| **Low** | Copy, styling, isolated UI, docs | Functional, regression, basic UX |
| **Medium** | Business logic, API changes, schema changes, shared components | + failure, security, data integrity, relevant performance |
| **High** | Payments, auth, destructive operations, migrations, multi-tenancy, external integrations | + concurrency, idempotency, observability, recovery, integration behavior |

Say "quick check" for a lighter pass, or "full production readiness review" to
force the high-risk depth.

## How it executes tests

It reads your project's manifests, `Makefile`, and CI config to learn how the
project actually builds and tests itself, then works outward:

```
targeted tests → type check → lint → related integration tests → build → wider suite
```

Three constraints:

1. **Baseline first.** It establishes which failures already existed, so a
   pre-existing failure is never blamed on your change. When it cannot tell, it
   says `UNDETERMINED`.
2. **Scope is stated.** A targeted run is never reported as if it were the full
   suite.
3. **Nothing destructive.** It will not drop databases, reset environments,
   delete data, destroy containers, rewrite git history, force push, deploy, or
   touch production-like systems. It reads git state and never modifies it — no
   commits, no resets, no stashing.

If the environment cannot run a check, that is an `UNVERIFIED` entry, not a
failure and not a silence.

## Example output

Five full worked reports ship with the skill:
[payment](examples/payment.md) ·
[bulk operation](examples/bulk-operation.md) ·
[API change](examples/api-change.md) ·
[database migration](examples/database-migration.md) ·
[authentication](examples/authentication.md)

They are illustrative reports written to show the expected shape and rigor, not
transcripts of a particular run. One of them ends in 🟢 SHIP on purpose — a gate
that never passes anything is not a gate.

## How it works

Fourteen phases, driven by the risk classification:

1. Understand the change — including whether it is reversible, idempotent, and
   concurrency-safe
2. Establish baseline
3. Build the behavioral model and its invariants
4. Identify the regression surface
5. Failure-first analysis
6. Security boundaries
7. Data integrity
8. Idempotency
9. Performance and scale
10. Observability and recovery
11. Execute available validation
12. Inspect results against the baseline
13. Classify findings
14. Produce the verdict

Reference material the agent consults when it needs depth:

- [`behavioral-validation.md`](references/behavioral-validation.md) — contracts and regression matrices
- [`failure-analysis.md`](references/failure-analysis.md) — failure taxonomy, idempotency, partial failure, recovery
- [`security-validation.md`](references/security-validation.md) — authorization, tenancy, exposure
- [`data-integrity.md`](references/data-integrity.md) — transactions, constraints, destructive ops, state machines
- [`performance.md`](references/performance.md) — scale reasoning, N+1, memory, indexes
- [`observability.md`](references/observability.md) — logging, audit trails, alerting
- [`report-schema.md`](references/report-schema.md) — report structure and finding fields
- [`change-type-checklists.md`](references/change-type-checklists.md) — payments, auth, migrations, uploads, bulk, API

## Team customization

Copy [`references/team-standards.template.md`](references/team-standards.template.md)
to `references/team-standards.md` and fill in your test commands, risk
overrides, additional blocking criteria, accepted risks, and what your local
environment can and cannot exercise. The skill reads it during baseline, where
it overrides the generic defaults.

## Pairs with Impact Map

[Impact Map](../impact-map/README.md) runs *before* implementation and maps what
a change will touch. Production Guard runs *after* and validates that what was
built is safe to ship.

```
ticket → impact-map → implement → production-guard → ship
```

Neither requires the other.

## Adopting it as a team

Start advisory, tighten later:

```
ticket → implement → production guard → fix blockers → PR review → CI → merge
```

Run it on the changes that scare you first — payments, auth, migrations,
destructive operations — before making it routine. Once the team trusts the
blocker classification, it can become a PR gate. That gate is deliberately not
built here; the skill stays independent of any CI integration.

### Measuring whether it helped

Do not claim an improvement you have not measured. Baseline these before
adoption, then compare:

- Production regressions per release
- Escaped defects found by users
- Rollback frequency
- Post-release hotfixes
- Security issues caught before release vs after
- Performance regressions caught before release
- Test failures caught before merge
- Time from implementation to release

The honest version of the pitch is "this improves the evidence available before
shipping", and the numbers above are how you find out whether that mattered.

## Limitations

Production Guard improves the evidence available before shipping. It does not
guarantee production safety, and no tool that reads your code can.

- **Dynamic runtime behavior can be hidden** — reflection, dynamic dispatch,
  runtime configuration, and feature flags defeat static reasoning
- **External systems may be unavailable** locally, so integration behavior is
  often reasoned rather than observed
- **Production traffic differs from local tests** — concurrency, data volume,
  and infrastructure limits usually cannot be reproduced
- **Static analysis cannot prove completeness** — an absent finding is not proof
  of absence
- **AI reasoning can miss dependencies**, particularly indirect ones
- **Unexecuted checks are not equivalent to executed ones** — the report labels
  them separately for exactly this reason
- **The verdict is advisory.** A human owns the release decision.

## License

MIT — see [`LICENSE`](../../LICENSE) at the repository root.
