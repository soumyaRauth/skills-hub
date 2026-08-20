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

**[Browse the skills →](https://soumyaRauth.github.io/skills-hub/)**

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

## Installation

```bash
# any Agent Skills-compatible agent
npx skills add soumyaRauth/skills-hub --skill impact-map

# Claude Code specifically
npx skills add soumyaRauth/skills-hub --skill impact-map --agent claude-code
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
│   └── impact-map/
│       ├── SKILL.md              ← the skill itself
│       ├── README.md             ← human documentation
│       ├── references/           ← deeper guidance the agent consults on demand
│       └── examples/             ← four worked impact maps
├── tests/
│   ├── fixtures/                 ← four small fake repositories
│   └── README.md                 ← expected findings per fixture
├── scripts/validate.sh           ← structure + frontmatter validation
└── .github/workflows/validate.yml
```

## Documentation

- **[Skill documentation](skills/impact-map/README.md)** — usage, modes, output,
  limitations, team customization
- **[The skill](skills/impact-map/SKILL.md)** — the instructions themselves
- **[Testing](tests/README.md)** — fixtures and expected reasoning behavior
- **[Contributing](CONTRIBUTING.md)** — how to improve it safely

---

## Contributing

Improvements to the methodology, framework guidance, examples, and fixtures are
all welcome. The one hard rule: **do not make the skill more speculative.** A
finding without evidence is worse than no finding, because it costs the reader
time and teaches them to distrust the report.

See [CONTRIBUTING.md](CONTRIBUTING.md). Run `./scripts/validate.sh` before
opening a pull request.

## Roadmap

Ideas, not commitments.

| Version | Focus |
| --- | --- |
| **v0.2** | Better monorepo awareness; git history, ownership, and changed-file analysis |
| **v0.3** | Architecture graph output, dependency visualization, risk scoring |
| **v0.4** | Tighter implementation-plan handoff and change verification |
| **v0.5** | A second skill, `change-guard`, that takes an Impact Map and checks whether an implementation actually covered the identified surface |

## Limitations

Impact Map is instruction-driven, not a static analyzer. It does not claim
completeness, and it cannot prove one.

- Results vary with the agent, the repository, and how the request is phrased
- Dynamic dispatch, reflection, runtime configuration, and generated clients are
  where it is weakest
- It only sees this repository — cross-repo and warehouse consumers surface as
  open questions at best
- Large monorepos need scoping
- It does not run tests and does not verify its own findings

Treat the output as a well-evidenced starting point for engineering judgment.

## License

[MIT](LICENSE)
