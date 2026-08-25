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
   fine, as is reading an existing `git diff`. Running the project's own test
   suite is not part of analysis.
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

Phases 1–7 run for every analysis. Phases 8–12 run when the change actually
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

**When the change already exists** — the user points at uncommitted work, a
branch, a PR, or a commit range — read the diff and write the change statement
from what the code now does, not from the branch name. Every symbol, column,
route, literal, and enum value the diff touches becomes a primary concept for
Phase 3. Run the analysis on those concepts, then **subtract the files already
in the diff: what remains is the finding** — the surface this change touches but
has not visited. Commands and the rest of the recipe: `references/git-signals.md`.

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

**In a monorepo, scope before searching.** Read the workspace config
(`pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `go.work`, Cargo `[workspace]`,
Gradle `settings.gradle`, Maven `<modules>`), list the packages and their
*published* names, find which package the change originates in, and invert the
graph to get its dependents. Scope by that dependency graph, not by directory
proximity, and report the scope — including the packages you did not inspect and
why — under `REPOSITORY SCOPE`. A published package has consumers this
repository cannot enumerate; say so rather than implying the surface is closed.
See `references/monorepo.md`.

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

### Phase 5 — History and ownership

Git records coupling that no import graph holds: which files engineers actually
change together, which parts of the surface churn, and who reviews them.

- **Co-change.** For each primary concept, list the commits that touched it and
  the other files in those commits. A file that appears in most of them with no
  code reference between the two is temporal coupling — a ⚠️ HIDDEN COUPLING
  finding at Medium confidence, never higher on history alone.
- **Churn.** High churn in the change surface means unsettled code: half-done
  migrations, duplicated logic, stale tests. A file untouched for years carries
  the opposite risk — nobody currently holds it in their head. Both feed `RISK`;
  neither is a finding by itself.
- **Ownership.** `CODEOWNERS` first, contributor counts as a fallback. Report it
  as routing — which reviewer or team this change needs — never as attribution
  or as a judgment about anyone's work.

Check that history is usable before trusting it: a shallow clone, a squash-merge
workflow, a single founding commit, or an untracked rename all produce numbers
that mislead. When history is unusable, say which condition applies and move on.
Commands, ratios, and reporting rules: `references/git-signals.md`.

### Phase 6 — Cross-layer analysis

Walk the layers this repository actually has, typically:

```
UI → API → Controller → Service/Domain → Model/Repository → Database
```

Then check the layers that sit beside the request path: events, jobs, scheduled
tasks, notifications, permissions, reports/exports, integrations. Do not invent
layers a repository does not have, and do not skip one because the framework
"usually" handles it.

### Phase 7 — Hidden coupling

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
- **Temporal coupling** — files git history says change together, with no
  reference between them (Phase 5).
- **Documentation** — API docs or runbooks that go stale on this change.

Everything found here is **indirect evidence** and must be labeled as such.
Search patterns per category: `references/hidden-coupling.md`.

### Phase 8 — Database impact

When persisted data is involved: migrations, schema, models/entities,
relationships, repositories, raw SQL, indexes, constraints, seeders, factories,
fixtures, reports, exports.

For schema changes also consider existing rows, defaults, nullability,
backward compatibility, migration ordering, and whether a data backfill is
required. Do not invent requirements — anything needing a human decision goes
under `OPEN QUESTIONS`.

### Phase 9 — API impact

Routes, controllers, request validation, response serializers, DTOs/schemas, API
clients, frontend and mobile consumers, contract tests, documentation. Assess
request shape, response shape, backward compatibility, validation, authorization,
and versioning. Distinguish a consumer you found in the repository from a
consumer that may exist outside it.

### Phase 10 — Authorization impact

If the change touches approval, status transitions, roles, permissions,
ownership, visibility, or administrative actions, inspect policies, guards,
middleware, role checks, permission constants, UI permission checks, API
authorization, and their tests.

Changing business logic does not update authorization. A new state usually needs
a new answer to "who may move a record into it, and who may see it there."

### Phase 11 — Test impact

Identify unit, integration, feature, API, component, E2E, and contract tests,
plus factories, fixtures, and snapshots. For each relevant group state **what
behavior it protects**, not just that it exists.

Missing coverage is a finding:

> No existing test covers the transition `pending → approved`.

### Phase 12 — External boundaries

External APIs, webhooks, message brokers, mobile clients, other frontends,
third-party integrations, imports/exports, scheduled syncs, reporting systems.
Only claim an external consumer when repository evidence supports it; otherwise
report it as an open question.

## Classification

Every significant finding carries a stable id — `F1`, `F2`, … in report order —
and exactly one classification. The ids are what the architecture graph, the
risk table, and the implementation plan point at, so they must not be reused or
renumbered inside a report.

| Category | Meaning |
| --- | --- |
| 🟥 **MUST CHANGE** | Strong evidence this location requires modification for the change to work. |
| 🟧 **LIKELY AFFECTED** | Strong relationship established; whether it changes needs confirmation. |
| 🟨 **NEEDS VERIFICATION** | Plausible relationship that must be checked before implementation. |
| ⚠️ **HIDDEN COUPLING** | Indirect dependency via strings, SQL, config, duplicated logic, generated code, conventions, serialization, fixtures, or co-change history. |
| ⬜ **OUT OF SCOPE** | Inspected and found not materially related. Use sparingly — only where a reader would otherwise expect the file to appear. |

## Confidence

- **High** — direct reference or unambiguous dependency observed in the code.
- **Medium** — strong behavioral relationship with some inference.
- **Low** — plausible relationship that requires verification.

Confidence describes the *evidence*, classification describes the *action*. Low
confidence caps a finding at NEEDS VERIFICATION.

```
F1 · app/Services/CourseCompletionService.php

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
REQUEST · INTERPRETATION · REPOSITORY SCOPE · CHANGE SURFACE
🟥 MUST CHANGE · 🟧 LIKELY AFFECTED · 🟨 NEEDS VERIFICATION · ⚠️ HIDDEN COUPLING
DEPENDENCY PATHS · ARCHITECTURE GRAPH · HISTORY & OWNERSHIP
DATABASE IMPACT · API IMPACT · AUTHORIZATION IMPACT · TEST IMPACT
RISK · RECOMMENDED IMPLEMENTATION ORDER · OPEN QUESTIONS
```

`REPOSITORY SCOPE` appears when the repository is a monorepo or the analysis
started from a diff; it states what was in scope, what was not, and why.
`HISTORY & OWNERSHIP` appears when git history was usable, and is omitted with a
one-line reason when it was not.

### Architecture graph

When the surface branches or crosses three or more layers, draw it — a mermaid
`flowchart` with one subgraph per layer this repository actually has, nodes
labeled by finding id, and **every edge labeled with its relationship**. Solid
edges are hard (import, call, foreign key); dashed edges are soft (string, raw
SQL, config, convention, co-change) and are where the incidents come from. A
single linear path needs no graph — emit the chain and move on.

The graph renders findings that are already in the report. Never draw a node
without a location in the repository or an explicit "outside this repository"
marker, and never draw a suspected edge as fact. Conventions, an ASCII
alternative, and collapsing rules: `references/architecture-graph.md`.

### Risk

`RISK` is a scored argument, not a verdict: six factors — breadth, coupling
opacity, test coverage, reversibility, consumer reach, area volatility — each
scored 0–3 from what the analysis observed, each printed with the observation
that set it, summed into a Low / Medium / High band.

Show the factor table. A total without its factors is exactly the invented
number rule 4 forbids. A factor that could not be assessed is scored `?` and
makes the total a lower bound — never rounded down to make a change look safe.
Floors (an irreversible migration, an unreachable external consumer) override
the total upward, and the band is never lowered below it.
Rubric: `references/risk-scoring.md`.

## Normal vs deep mode

**Normal** (default): reconnaissance and scoping → primary concepts → direct
dependency tracing → history signals on the primary concepts → cross-layer
inspection → relevant tests → high-value hidden-coupling checks → report.

**Deep** — triggered by "deep analysis", "full impact analysis", "blast radius",
"thorough", "comprehensive": additionally sweep reverse references, raw strings,
raw SQL, configuration, generated artifacts, events, jobs, permissions, reports,
fixtures, external boundaries, duplicated business logic, co-change history for
every primary concept, and — in a monorepo — every dependent package rather than
the direct ones alone.

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

Only on an explicit yes, convert the map into a plan. The plan is a **handoff
artifact**: written so an engineer, or a fresh agent session with no memory of
the analysis, can execute it without re-reading anything. It still contains no
code.

Each step carries: the files, the finding ids it **resolves**, what it depends
on, the change in prose, the one-line evidence from the map, how to **verify**
it, and how to roll it back.

Three rules make it a handoff rather than a to-do list:

- **Coverage is explicit.** A closing table maps every finding id to its step.
  Each 🟥 is resolved by exactly one step; a 🟥 with no step is an invalid plan.
  🟧 is mapped or explicitly deferred with a reason; every ⚠️ gets a step or a
  recorded decision; every 🟨 becomes a **prerequisite** resolved before the
  steps that depend on it, never a check buried inside one.
- **Every step leaves the system working.** Order by dependency and
  reversibility: prerequisites, then compatibility (dual-read, dual-emit), then
  the change innermost outward, then data backfills, then the coverage for the
  quiet paths, then removing the shim. Size each step to one commit.
- **Verification is an observation**, not "verify it works" — an existing test
  path, a described assertion, or a command whose output shows the change took
  effect. A step that cannot be verified says so.

Unresolved decisions stay visible as prerequisites or `Stop if:` conditions,
never as assumptions baked into a step. If implementation shows the map was
wrong, stop and say which finding changed instead of re-planning quietly. The
plan's last line names what to validate afterwards — the hidden-coupling
findings and the factors that set the risk band.

Full structure and rules: `references/implementation-plan.md`. Worked example:
`examples/implementation-plan.md`.

Never jump silently from analysis to editing code.

## References

- `references/report-schema.md` — full report structure and finding fields
- `references/dependency-analysis.md` — upstream/downstream tracing tactics
- `references/hidden-coupling.md` — indirect-coupling search patterns
- `references/framework-detection.md` — per-ecosystem reconnaissance cues
- `references/git-signals.md` — co-change, churn, ownership, diff-driven analysis
- `references/monorepo.md` — workspace detection, package graph, scoping
- `references/architecture-graph.md` — graph conventions and honesty rules
- `references/risk-scoring.md` — the six-factor risk rubric
- `references/implementation-plan.md` — the plan structure and handoff contract

If `references/company-architecture.md` exists in this skill directory, read it
during Phase 2 — it carries team-specific conventions that override generic
framework assumptions.
