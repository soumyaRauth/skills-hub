# Lifecycle assessment

The `/standards lifecycle` focus, using ISO/IEC/IEEE 12207 as the process
vocabulary. Assess this when someone asks how the software is developed and
maintained — a customer questionnaire, a regulated context, a contract, or a
team that genuinely wants to know which processes leave no trace.

For most projects this is the least useful focus available, and offering it
unprompted to a five-person team building a SaaS product is exactly the
bureaucracy this skill exists to avoid.

## Two rules before anything else

**Agile is not a deviation.** 12207 describes processes to be performed, not a
development methodology, and explicitly does not require a waterfall. A team
doing continuous delivery with trunk-based development performs requirements,
architecture, verification and change management continuously. The question is
whether they leave evidence, not whether they hold phase gates.

**Repository evidence is not process evidence.** A repository can show that
something was recorded. It cannot show that a process is followed, that people
are competent, or that an organization has agreed anything. Keep the line
visible.

## What to look for

| Process area | Repository evidence | Frequently absent |
| --- | --- | --- |
| Requirements | Issue links in commits, specs, acceptance criteria, ADRs | Any record of *why* something was built |
| Architecture | ADRs, design docs, module boundaries that match a stated intent | Rationale for the significant choices |
| Implementation | Coding standards, review requirements, linters in CI | — |
| Verification | Test suites, CI gating, coverage of core paths | Tests for the security-relevant paths |
| Validation | Acceptance criteria, UAT records, feature flags with real evaluation | Any evidence users were consulted |
| Configuration management | Version control, branching, tagging, lockfiles, IaC | Nothing usually — this is normally the strongest area |
| Change management | Branch protection, review rules, migration procedures, release notes | Who may approve what |
| Release | Versioning, changelog, release automation, rollback path | A documented rollback |
| Operation | Runbooks, health checks, monitoring config, on-call references | Usually entirely outside the repository |
| Maintenance | Dependency updates, deprecation notes, issue triage in history | A stated support window |
| Retirement | Data export, deprecation notices, decommissioning notes | Almost always absent, and rarely worth a finding |

## Version discipline

Name the edition being assessed against, explicitly, and never substitute
silently. Where the registry records a current edition and a newer one whose
status is unconfirmed, say that and let the user choose — a team contractually
aligned to an older edition needs that edition, not the newest one.

## Reporting

Report which processes have visible evidence, which do not, and which cannot be
established from a repository at all. Do not grade. Do not describe a project as
conforming to or violating 12207: process conformance is assessed against a
defined process set at organizational level, by people, over time.

```markdown
Life cycle process evidence — ISO/IEC/IEEE 12207:2017 as the reference frame

Strong     Configuration management — git, lockfiles, tagged releases,
           protected main branch requiring review
Partial    Verification — 140 tests, CI on every PR, but no tests over the
           authorization or payment paths
Partial    Change management — reviews are required; no record of who may
           approve a production migration
Absent     Requirements — no issue references in commits, no specs, no ADRs.
           Nothing records why the current design was chosen
External   Operation and maintenance — runbooks, on-call and monitoring are
           not in this repository
```

The `Absent` row is a real finding for a regulated or long-lived system, and
noise for a six-month-old startup product. Say which one you think this is, and
why.
