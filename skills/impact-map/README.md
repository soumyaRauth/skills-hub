# Impact Map

An Agent Skill that answers one question before you write any code:

> **Before I change this, what else could this change affect?**

Impact Map turns a change request into an evidence-based blast-radius report:
what is affected, *why* it is affected, how it is connected, how confident the
analysis is, and what should happen next.

---

## Why it exists

The common failure mode:

```
ticket → find the obvious file → change it → discover later what broke
```

What actually breaks is rarely the obvious file. It is the raw SQL in a report,
the string comparison in a nightly job, the fixture that keeps the test suite
green while the behavior is wrong, the policy that never learned about the new
state.

Impact Map inserts a read-only analysis step:

```
ticket → impact map → architecture → dependencies → hidden coupling
       → tests → risks → implementation plan → coding
```

---

## What makes it different from "find related files"

A generic search gives you:

```
File A
File B
File C
```

Impact Map gives you, for each finding: the symbol, the relationship, the
evidence observed in the repository, a confidence level, and the concrete action.
Findings are classified:

| | Meaning |
| --- | --- |
| 🟥 **MUST CHANGE** | Strong evidence this location requires modification. |
| 🟧 **LIKELY AFFECTED** | Strong relationship; needs confirmation. |
| 🟨 **NEEDS VERIFICATION** | Plausible relationship; check before implementing. |
| ⚠️ **HIDDEN COUPLING** | Indirect dependency — raw strings, SQL, config, duplicated logic, fixtures, serialization. |
| ⬜ **OUT OF SCOPE** | Inspected, not materially related. |

Speculation is never presented as fact, and low-confidence findings are never
promoted to MUST CHANGE.

---

## When to use it

- Before changing business logic, shared services, or state machines
- Before schema or API contract changes
- When working in an unfamiliar or legacy codebase
- When a change crosses modules, layers, or teams
- Before touching authentication, authorization, or permissions
- Before changing anything consumed by jobs, reports, exports, or integrations
- During code review, to check whether a change covered its surface

## When not to use it

- Typos, copy changes, formatting, dependency bumps
- Greenfield code with no existing consumers
- You already know the surface and the change is one file
- You need the code written *now* — Impact Map deliberately stops before
  implementation

Running it on a two-line change is not dangerous, just slower than reading the
file.

---

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill impact-map
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill impact-map --agent claude-code
```

The CLI writes the skill into your agent's skills directory; no other setup,
server, or API is required.

### Invoking it

Installed skills are selected by their description, so you invoke Impact Map by
asking for what it does — no slash command:

```
What's the blast radius of adding an approval step to course completions?
Before you change anything, map the impact of renaming this status.
Deep impact analysis on switching the notification provider.
```

You can also name it directly: *"Use the impact-map skill on this ticket."*

---

## Usage

### Normal analysis

```
You:   Add approval status to course completion.

Agent: I'll map the impact surface before changing anything.
       …
       IMPACT MAP
       ────────────────────────────────────────
       REQUEST
       Introduce approval_status into course completion and expose it
       through the existing API and UI.
       …
       Want me to turn this into an implementation plan?
```

### Deep analysis

Trigger with *deep analysis*, *full impact analysis*, *blast radius*,
*thorough*, or *comprehensive*. Deep mode adds sweeps for reverse references,
raw strings, raw SQL, configuration, generated artifacts, events, jobs,
permissions, reports, fixtures, external boundaries, and duplicated business
logic.

Deep mode means more investigation, not a longer file list.

| | Normal | Deep |
| --- | --- | --- |
| Repository reconnaissance | ✅ | ✅ |
| Direct dependency tracing | ✅ | ✅ |
| Cross-layer inspection | ✅ | ✅ |
| High-value hidden coupling | ✅ | ✅ |
| Exhaustive string / SQL / config sweep | — | ✅ |
| Events, jobs, schedules, permissions | as relevant | ✅ |
| Fixtures, generated code, external boundaries | as relevant | ✅ |

### Example output

Abbreviated. Full worked examples are in [`examples/`](examples/) — illustrative reports written to show the expected shape and rigor, not transcripts of a particular run.

```
🟥 MUST CHANGE

app/Services/CourseCompletionService.php

  Symbol:         CourseCompletionService::complete()
  Relationship:   Writes CourseCompletion.status during the completion workflow.
  Evidence:       Line 42 sets $completion->status = CompletionStatus::COMPLETED
                  and is the only writer found for that field.
  Confidence:     High
  Action:         Set approval_status alongside status in the transition.

⚠️ HIDDEN COUPLING

app/Reports/CompletionReport.php

  Coupling type:  Raw SQL
  Evidence:       WHERE status = 'completed' — string literal, not the enum.
  Confidence:     High
  Action:         Decide whether the report should now count approved
                  completions only.

RISK

Medium — additive schema change, but the surface spans persistence,
authorization, async work and a raw-SQL report, and the historical data
decision has no reversible default.
```

---

## How it works

There is no engine, index, or server. The skill is a **workflow and reasoning
methodology** that directs the coding agent's own repository inspection:

1. **Understand the request** → a one-sentence change statement
2. **Repository reconnaissance** → the actual structure, not assumed conventions
3. **Find primary concepts** → progressive search across naming conventions
4. **Dependency analysis** → upstream callers and downstream dependencies
5. **Cross-layer analysis** → UI → API → service → model → database, plus
   events, jobs, permissions, reports
6. **Hidden coupling** → strings, SQL, config, duplicated logic, fixtures
7–11. **Database, API, authorization, test, and external boundary impact**

Then classification, confidence, and the report.

Reference material the agent consults when it needs depth:

- [`references/report-schema.md`](references/report-schema.md) — report structure and finding fields
- [`references/dependency-analysis.md`](references/dependency-analysis.md) — upstream/downstream tracing
- [`references/hidden-coupling.md`](references/hidden-coupling.md) — indirect-coupling search patterns
- [`references/framework-detection.md`](references/framework-detection.md) — per-ecosystem reconnaissance

---

## Read-only by design

During impact analysis the skill does not modify source files, create
migrations, edit configuration, install packages, delete files, commit, push, or
"fix" what it finds. It reads files, git metadata, and dependency manifests.

Implementation happens only when you explicitly ask for it, after the map.

---

## Team customization

Copy [`references/company-architecture.template.md`](references/company-architecture.template.md)
to `references/company-architecture.md` and fill in your conventions — domain
boundaries, layer locations, naming patterns, shared modules, integrations,
business terminology, standing risks. The skill reads it during reconnaissance,
where it overrides generic framework assumptions.

Keep internal details out of public forks.

---

## Limitations

- **Instruction-driven, not a static analyzer.** Results depend on the agent
  and the repository. Coverage is not guaranteed or provable.
- **It can miss things.** Dynamic dispatch, reflection, runtime configuration,
  and generated clients are exactly where automated reasoning is weakest.
- **It only sees this repository.** Consumers in other repos, other services, or
  a data warehouse appear as open questions at best.
- **Large monorepos** need scoping — point it at the relevant packages.
- **It does not run your tests** and cannot prove a finding is complete.
- Treat the output as a well-evidenced starting point for engineering judgment,
  not a certificate of completeness.

---

## License

MIT — see [`LICENSE`](../../LICENSE) at the repository root.
