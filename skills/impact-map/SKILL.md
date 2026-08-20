---
name: impact-map
description: Analyze the blast radius of a proposed software change before implementation. Use when a developer asks what files, modules, APIs, database structures, tests, integrations, permissions, or hidden dependencies may be affected by a change. Produces an evidence-based impact map and implementation handoff without modifying source code.
---

# Impact Map

Answer one question before any code is written:

> Before I change this, what else could this change affect?

The deliverable is an **evidence-based blast-radius report**: what is affected,
why it is affected, how it is connected, how confident you are, and what should
happen next. A list of filenames is not the deliverable.

## Non-negotiable rules

1. **Read-only.** During impact analysis do not edit, create, delete, or move
   files; do not write migrations, install packages, run formatters, commit, or
   push. Inspecting files, `git log`/`git blame`, and dependency manifests is
   fine. Running the project's own test suite is not part of analysis.
2. **Evidence or nothing.** Every classified finding names the file (and symbol
   or line where useful) plus the observation that supports it. If you did not
   see it in the repository, say so and mark it for verification.
3. **Never promote a guess.** A low-confidence finding may never be reported as
   MUST CHANGE. Downgrade instead of rounding up.
4. **No fabricated numbers.** Only report counts you actually produced. Prefer
   "several files inspected" over an invented total. Counts are optional;
   accuracy is not.
5. **No implementation.** Stop at the report. Offer the implementation plan;
   produce it only when the user asks. Produce code only when the user asks for
   code.
6. **Report the gaps.** Name the parts of the system you could not inspect
   (generated code, private packages, external repos) rather than leaving them
   silently missing.

## Workflow

Phases 1–6 run for every analysis. Phases 7–11 run when the change actually
touches that layer — skip a phase explicitly rather than inventing content for
it.

### Phase 1 — Understand the request

Extract requested behavior, domain concepts, entities, fields, state/status
transitions, user-facing behavior, API changes, data changes, integrations, and
stated constraints. Compress it into one **CHANGE STATEMENT**:

> Introduce `approval_status` into course completion and expose it through the
> existing API and UI.

If the request is ambiguous, pick the most reasonable reading, state it under
`INTERPRETATION`, and continue. Do not stall the analysis on a clarification you
can flag as an open question.

### Phase 2 — Repository reconnaissance

Learn the actual repository before searching it. Read the manifests
(`package.json`, `composer.json`, `pyproject.toml`, `go.mod`, `pom.xml`,
`Gemfile`, `Cargo.toml`), the top-level tree, and any workspace config.
Identify language, framework, monorepo layout, and where the layers really live:
frontend, API, domain/services, persistence, migrations, jobs/queues, events,
notifications, authorization, configuration, integrations, generated code, tests.

Never assume `src/`, `app/`, `lib/`, or `controllers/` exist. Look. When the
repository contradicts framework convention, the repository wins. See
`references/framework-detection.md`.

### Phase 3 — Find primary concepts

Search progressively, starting from the vocabulary in the change statement:
class, function, and component names; tables and columns; enums and status
values; routes; event names; domain terms.

Expand across naming conventions before concluding something does not exist —
`CourseCompletion`, `course_completion`, `course-completion`, `courseCompletion`,
`completion_status`, `completed`, `approval`, `approve`, `approved`. Exact
identifier matching alone will miss the interesting coupling.

### Phase 4 — Dependency analysis

For each primary concept, trace **both** directions:

- **Upstream (who depends on this):** importers, callers, consumers, queries,
  API callers, components, jobs, event producers and listeners.
- **Downstream (what this depends on):** services invoked, models written,
  tables touched, serializers, API responses, UI, notifications, events, queues.

Record the paths as chains, not sets, and explain the link at each step:

```
CourseCompletionService  → writes CourseCompletion.status
CourseCompletion         → serialized by CourseCompletionResource
CourseCompletionResource → returned by GET /api/course-completions
/api/course-completions  → consumed by CourseCompletion.tsx
```

Details and search tactics: `references/dependency-analysis.md`.

### Phase 5 — Cross-layer analysis

Walk the layers this repository actually has, typically:

```
UI → API → Controller → Service/Domain → Model/Repository → Database
```

Then check the layers that sit beside the request path: events, jobs, scheduled
tasks, notifications, permissions, reports/exports, integrations. Do not invent
layers a repository does not have, and do not skip one because the framework
"usually" handles it.

### Phase 6 — Hidden coupling

The highest-value phase, and the one generic code search skips. Look for
relationships that do not appear as imports:

- **Raw strings** — `"completed"` where the domain uses `CompletionStatus.COMPLETED`.
- **Raw SQL** — queries naming the affected tables or columns.
- **Direct data access** — code bypassing the domain/service layer.
- **Duplicated business logic** — the same `status === "completed"` decision in
  several places.
- **Configuration** — environment variables, config keys, feature flags,
  permission identifiers.
- **Events and listeners** — subscribers matched by string name.
- **Jobs, workers, schedules** — queue payloads carrying the affected shape.
- **Serialization** — JSON field names, API resources, DTOs, schemas, contracts.
- **Tests and fixtures** — factories, fixtures, snapshots, hardcoded states.
- **Documentation** — API docs or runbooks that go stale on this change.

Everything found here is **indirect evidence** and must be labeled as such.
Search patterns per category: `references/hidden-coupling.md`.

### Phase 7 — Database impact

When persisted data is involved: migrations, schema, models/entities,
relationships, repositories, raw SQL, indexes, constraints, seeders, factories,
fixtures, reports, exports.

For schema changes also consider existing rows, defaults, nullability,
backward compatibility, migration ordering, and whether a data backfill is
required. Do not invent requirements — anything needing a human decision goes
under `OPEN QUESTIONS`.

### Phase 8 — API impact

Routes, controllers, request validation, response serializers, DTOs/schemas, API
clients, frontend and mobile consumers, contract tests, documentation. Assess
request shape, response shape, backward compatibility, validation, authorization,
and versioning. Distinguish a consumer you found in the repository from a
consumer that may exist outside it.

### Phase 9 — Authorization impact

If the change touches approval, status transitions, roles, permissions,
ownership, visibility, or administrative actions, inspect policies, guards,
middleware, role checks, permission constants, UI permission checks, API
authorization, and their tests.

Changing business logic does not update authorization. A new state usually needs
a new answer to "who may move a record into it, and who may see it there."

### Phase 10 — Test impact

Identify unit, integration, feature, API, component, E2E, and contract tests,
plus factories, fixtures, and snapshots. For each relevant group state **what
behavior it protects**, not just that it exists.

Missing coverage is a finding:

> No existing test covers the transition `pending → approved`.

### Phase 11 — External boundaries

External APIs, webhooks, message brokers, mobile clients, other frontends,
third-party integrations, imports/exports, scheduled syncs, reporting systems.
Only claim an external consumer when repository evidence supports it; otherwise
report it as an open question.

## Classification

Every significant finding carries exactly one:

| Category | Meaning |
| --- | --- |
| 🟥 **MUST CHANGE** | Strong evidence this location requires modification for the change to work. |
| 🟧 **LIKELY AFFECTED** | Strong relationship established; whether it changes needs confirmation. |
| 🟨 **NEEDS VERIFICATION** | Plausible relationship that must be checked before implementation. |
| ⚠️ **HIDDEN COUPLING** | Indirect dependency via strings, SQL, config, duplicated logic, generated code, conventions, serialization, or fixtures. |
| ⬜ **OUT OF SCOPE** | Inspected and found not materially related. Use sparingly — only where a reader would otherwise expect the file to appear. |

## Confidence

- **High** — direct reference or unambiguous dependency observed in the code.
- **Medium** — strong behavioral relationship with some inference.
- **Low** — plausible relationship that requires verification.

Confidence describes the *evidence*, classification describes the *action*. Low
confidence caps a finding at NEEDS VERIFICATION.

```
app/Services/CourseCompletionService.php

  Symbol:       CourseCompletionService::complete()
  Relationship: Writes CourseCompletion.status during the completion workflow.
  Evidence:     Line 42 sets $completion->status = CompletionStatus::COMPLETED
                and is the only writer found for that field.
  Classification: 🟥 MUST CHANGE
  Confidence:   High
  Action:       Set approval_status alongside status in the transition.
```

## Report format

Emit the sections in `references/report-schema.md`, in this order, omitting any
section with nothing relevant to say:

```
IMPACT MAP
────────────────────────────────────────
REQUEST · INTERPRETATION · CHANGE SURFACE
🟥 MUST CHANGE · 🟧 LIKELY AFFECTED · 🟨 NEEDS VERIFICATION · ⚠️ HIDDEN COUPLING
DEPENDENCY PATHS · DATABASE IMPACT · API IMPACT · AUTHORIZATION IMPACT · TEST IMPACT
RISK · RECOMMENDED IMPLEMENTATION ORDER · OPEN QUESTIONS
```

`RISK` is Low / Medium / High plus the reason — driven by breadth of the change
surface, amount of hidden coupling, weakness of test coverage, and whether
external consumers are involved.

## Normal vs deep mode

**Normal** (default): reconnaissance → primary concepts → direct dependency
tracing → cross-layer inspection → relevant tests → high-value hidden-coupling
checks → report.

**Deep** — triggered by "deep analysis", "full impact analysis", "blast radius",
"thorough", "comprehensive": additionally sweep reverse references, raw strings,
raw SQL, configuration, generated artifacts, events, jobs, permissions, reports,
fixtures, external boundaries, and duplicated business logic.

Deep mode means more *investigation*, not a longer file listing. Every extra
finding still needs evidence and a classification, and irrelevant files stay out
of the report.

## Interactive flow

```
User:  Add approval status to course completion.
Agent: I'll map the impact surface before changing anything.
       [analysis]
       IMPACT MAP …
       Want me to turn this into an implementation plan?
```

Only on an explicit yes, convert the map into an ordered plan grounded in the
findings — each step naming the files it touches and the findings it resolves.
A typical order:

1. Database field and migration
2. Domain model / state representation
3. Service transition logic
4. API serialization
5. Authorization
6. UI
7. Jobs, notifications, reports
8. Tests
9. Verify the hidden-coupling and needs-verification findings

Never jump silently from analysis to editing code.

## References

- `references/report-schema.md` — full report structure and finding fields
- `references/dependency-analysis.md` — upstream/downstream tracing tactics
- `references/hidden-coupling.md` — indirect-coupling search patterns
- `references/framework-detection.md` — per-ecosystem reconnaissance cues

If `references/company-architecture.md` exists in this skill directory, read it
during Phase 2 — it carries team-specific conventions that override generic
framework assumptions.
