# Skills Hub

Agent Skills for real engineering work — installable with the Skills CLI,
usable with Claude Code and other Agent Skills-compatible agents.

**[Browse the skills →](https://soumyaRauth.github.io/skills-hub/)**

| Skill | What it does | When |
| --- | --- | --- |
| **[impact-map](skills/impact-map/README.md)** | Maps the blast radius of a proposed change — what it affects, why, and how confident the analysis is | *Before* you write the code |
| **[production-guard](skills/production-guard/README.md)** | Validates whether a change is safe to ship: behavior, regressions, failures, security, data integrity, performance, operations | *After* you write it, before you merge |

```bash
npx skills add soumyaRauth/skills-hub --skill impact-map
npx skills add soumyaRauth/skills-hub --skill production-guard
```

They compose, and neither requires the other:

```
ticket → impact-map → implement → production-guard → ship
```

---

# Impact Map

**A reusable AI engineering skill for understanding the blast radius of software
changes.**

Impact Map is an [Agent Skill](https://code.claude.com/docs/en/skills) that runs
*before* implementation. It analyzes a repository and produces an evidence-based
change impact report: what a proposed change affects, why, how confident the
analysis is, and what to do next — without touching a single file.

```bash
npx skills add soumyaRauth/skills-hub --skill impact-map
```

---

## The problem

```
ticket → find the obvious file → change it → discover later what broke
```

The obvious file is rarely what breaks. What breaks is the raw SQL in a report,
the string comparison in a nightly job, the fixture that keeps CI green while
the behavior is wrong, the policy that never learned about the new state.

Generic code search does not help much, because it returns this:

```
File A
File B
File C
```

— with no explanation of why any of it matters.

## The solution

Impact Map inserts a read-only analysis step and returns findings that carry
their reasoning:

```
ticket → impact map → architecture → dependencies → hidden coupling
       → tests → risks → implementation plan → coding
```

Every significant finding is classified and evidenced:

| | Meaning |
| --- | --- |
| 🟥 **MUST CHANGE** | Strong evidence this location requires modification. |
| 🟧 **LIKELY AFFECTED** | Strong relationship; needs confirmation. |
| 🟨 **NEEDS VERIFICATION** | Plausible relationship; check before implementing. |
| ⚠️ **HIDDEN COUPLING** | Indirect dependency — raw strings, SQL, config, duplicated logic, fixtures, serialization. |
| ⬜ **OUT OF SCOPE** | Inspected, not materially related. |

Confidence is tracked separately (High / Medium / Low), and a low-confidence
finding is never promoted to MUST CHANGE. Speculation is never presented as
fact, and counts are never invented.

---

## Example

```
You:  Rename the COMPLETED enrollment status to APPROVED. Deep analysis please.

Agent: I'll map the impact surface before changing anything.

IMPACT MAP
────────────────────────────────────────

🟥 MUST CHANGE

backend/models/enrollment.py
  Symbol:       EnrollmentStatus.COMPLETED
  Evidence:     COMPLETED = "completed" — member name and stored string both
                carry the old name.
  Confidence:   High

⚠️ HIDDEN COUPLING

backend/reports/completion_report.py
  Coupling type: Raw SQL
  Evidence:      WHERE status = 'completed' — never touches the enum.
  Confidence:    High
  Action:        Silently returns zero rows after the rename.

backend/jobs/nightly_sync.py
  Coupling type: Raw string + direct data access
  Evidence:      if row["status"] == "completed" — bypasses the service layer.
  Confidence:    High

RISK

High — spans four runtimes, requires a data migration, and three critical
paths are string-coupled with no test coverage. Nothing in CI fails if they
are missed.
```

Four full worked examples: [simple](skills/impact-map/examples/simple-change.md) ·
[API](skills/impact-map/examples/api-change.md) ·
[database](skills/impact-map/examples/database-change.md) ·
[cross-module](skills/impact-map/examples/cross-module-change.md)

---

---

# Production Guard

**An AI-assisted production-readiness gate for software changes.**

> AI can write the code. Production Guard asks whether the resulting behavior is
> safe to ship.

## The problem

```
code generation ≠ production correctness
```

A change can pass its tests, compile, look reasonable, satisfy the ticket — and
still break an existing workflow, expose another tenant's data, corrupt records
under concurrency, double-charge on retry, time out at real data volumes,
silently swallow errors, or leave no trace of what it did at 3 AM.

## The solution

```
CODE CHANGE → behavior model → regression model → failure model
            → security / data / performance / operations
            → execute available validation
            → PRODUCTION READINESS REPORT
            → SHIP / CONDITIONAL SHIP / DO NOT SHIP
```

Two rules make the report worth reading:

**No invented scores.** Never `Code quality: 94%`. Instead, counts of checks
actually performed, and a verdict derived from explicit rules:

```
FUNCTIONAL VALIDATION     14/14 passed
REGRESSION VALIDATION     21/23 passed
SECURITY                   8/8  passed
DATA INTEGRITY             5/6  passed
FAILURE SCENARIOS          6/9  validated
```

**Executed ≠ analyzed.** Every check is labeled as a command that ran or as
reasoning, and a failure scenario only gets an observed result when it was
actually exercised.

| Verdict | Rule |
| --- | --- |
| 🟢 **SHIP** | No blockers, no unresolved HIGH findings, all risk-required categories validated |
| 🟠 **CONDITIONAL SHIP** | No blockers, but a HIGH finding or a required category left unverified |
| 🔴 **DO NOT SHIP** | At least one BLOCKER |

## Example

```
CHANGE    Add bulk deletion to user management.
VERDICT   🔴 DO NOT SHIP
BLOCKERS  2   HIGH 2   MEDIUM 1   LOW 1

🔴 #1 Authorization is checked once for the actor, never per target.
      Evidence:  BulkDeleteController.php:34 authorizes once, then deletes every
                 id in the request body. The single-delete path checks per record.
      Risk:      A team admin can delete users outside their team by supplying ids.

🔴 #2 Partial failure leaves the operation half-applied with no record.
      Evidence:  BulkDeleteService.php:28-41 commits per item inside a loop.
      Risk:      Failure at item 47 of 100 leaves an arbitrary subset deleted,
                 with no way to tell which or to safely retry.
```

Five full worked reports: [payment](skills/production-guard/examples/payment.md) ·
[bulk operation](skills/production-guard/examples/bulk-operation.md) ·
[API change](skills/production-guard/examples/api-change.md) ·
[database migration](skills/production-guard/examples/database-migration.md) ·
[authentication](skills/production-guard/examples/authentication.md)

One ends in 🟢 SHIP deliberately — a gate that never passes anything is not a
gate.

## Safety

Production Guard runs your project's own checks where it can. It will not drop
databases, reset environments, delete data, destroy containers, rewrite git
history, force push, deploy, or touch production-like systems. It reads git
state and never modifies it.

**[Full documentation →](skills/production-guard/README.md)**

---

## Installation

```bash
# any Agent Skills-compatible agent
npx skills add soumyaRauth/skills-hub --skill impact-map
npx skills add soumyaRauth/skills-hub --skill production-guard

# Claude Code specifically
npx skills add soumyaRauth/skills-hub --skill impact-map --agent claude-code
npx skills add soumyaRauth/skills-hub --skill production-guard --agent claude-code
```

Then just ask for what it does — installed skills are matched by description, so
no slash command is needed:

```
What's the blast radius of adding an approval step to course completions?
Before you change anything, map the impact of renaming this status.
Deep impact analysis on switching the notification provider.
```

## Supported agents

Impact Map is plain Agent Skills markdown. It requires **no MCP server, no
custom CLI, no hosted service, and no proprietary API** — only the repository
inspection an agent already has.

| Agent | Status |
| --- | --- |
| Claude Code | Primary target; installable via the Skills CLI |
| Other Agent Skills-compatible agents | Expected to work — the skill uses no agent-specific features |

If your agent supports the Agent Skills format and can read files and search a
repository, it can run this skill.

---

## Repository structure

```
.
├── skills/
│   ├── impact-map/
│   │   ├── SKILL.md              ← the skill itself
│   │   ├── README.md             ← human documentation
│   │   ├── references/           ← deeper guidance the agent consults on demand
│   │   └── examples/             ← four worked impact maps
│   └── production-guard/
│       ├── SKILL.md
│       ├── README.md
│       ├── references/
│       └── examples/             ← five worked readiness reports
├── tests/
│   ├── fixtures/
│   │   ├── impact-map/           ← four repositories with hidden coupling to find
│   │   └── production-guard/     ← four repositories with real production bugs
│   └── README.md                 ← expected findings per fixture
├── scripts/validate.sh           ← structure + frontmatter validation, all skills
└── .github/workflows/validate.yml
```

## Documentation

- **[Impact Map](skills/impact-map/README.md)** · [SKILL.md](skills/impact-map/SKILL.md)
- **[Production Guard](skills/production-guard/README.md)** · [SKILL.md](skills/production-guard/SKILL.md)
- **[Testing](tests/README.md)** — fixtures and expected reasoning behavior
- **[Contributing](CONTRIBUTING.md)** — how to improve them safely

---

## Contributing

Improvements to the methodologies, framework guidance, examples, and fixtures
are all welcome. Two hard rules:

- **Do not make the skills more speculative.** A finding without evidence is
  worse than no finding — it costs the reader time and teaches them to distrust
  the report.
- **No invented numbers.** No fabricated file counts, no quality percentages, no
  claiming a check ran when it did not.

See [CONTRIBUTING.md](CONTRIBUTING.md). Run `./scripts/validate.sh` before
opening a pull request.

## Roadmap

Ideas, not commitments.

**Impact Map**

| Version | Focus |
| --- | --- |
| v0.2 | Better monorepo awareness; git history, ownership, and changed-file analysis |
| v0.3 | Architecture graph output, dependency visualization, risk scoring |
| v0.4 | Tighter implementation-plan handoff |

**Production Guard**

| Version | Focus |
| --- | --- |
| v0.2 | Change-aware validation driven by git diff |
| v0.3 | Assisted test generation for unverified scenarios |
| v0.4 | CI integration |
| v0.5 | PR comment and report generation |

**Both**

A third skill, `change-guard`, closing the loop: take an Impact Map and a
Production Guard report and verify that the implementation actually covered the
identified surface and resolved the identified risks.

## Limitations

Both skills are instruction-driven, not static analyzers. Neither claims
completeness, and neither can prove it.

- Results vary with the agent, the repository, and how the request is phrased
- Dynamic dispatch, reflection, runtime configuration, and generated clients are
  where they are weakest
- They only see this repository — cross-repo consumers and external systems
  surface as open questions at best
- Large monorepos need scoping
- Impact Map does not run anything; Production Guard runs only what the local
  environment allows, and labels the rest unverified
- An absent finding is not proof of absence

Production Guard improves the evidence available before shipping. It does not
guarantee production safety, and a human owns the release decision.

## License

[MIT](LICENSE)
