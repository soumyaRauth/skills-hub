# Dependency Analysis

How to trace what connects to a concept, in both directions, without drowning
the report in noise.

## Two directions, different questions

**Upstream — who depends on this?** Determines what breaks when the concept
changes. This is where most of the blast radius lives.

**Downstream — what does this depend on?** Determines what constrains the
change: the contracts, data shapes, and services the concept must keep honoring.

Trace upstream first. A change that breaks nothing upstream is a small change,
whatever its downstream complexity.

## Finding upstream references

1. **Symbol search.** Grep the class/function/component name across the
   repository, including tests and configuration.
2. **Import search.** Grep for the module path, not just the symbol —
   re-exports and barrel files hide direct references.
3. **String search.** Route paths, event names, queue names, permission keys,
   and table names are referenced as strings, not symbols.
4. **Convention search.** Some frameworks bind by naming convention with no
   textual reference at all: Rails/Laravel model↔table, Next.js file↔route,
   Spring component scanning, Django app registries.
5. **Data search.** For a column or field, grep the column name across
   migrations, raw SQL, serializers, fixtures, and exports.

## Tracing downstream

Read the implementation and record what it actually touches: services called,
models written, tables queried, events emitted, external calls made. Stop
descending when a hop can no longer be affected by the change — depth without
relevance inflates the report.

## Depth heuristics

- Follow a chain until it reaches a boundary (HTTP response, queue, database,
  external API) or stops being sensitive to the change.
- Two or three hops covers most real changes. Beyond that, stop and note the
  boundary rather than speculating.
- Prefer breadth at hop 1 (find *all* direct callers) over depth on one path.

## Writing dependency paths

Name the relationship at each hop, and mark the hop that carries the change:

```
CompletionStatus (enum)                       ← the change
  ↓ compared in
CourseCompletionService::complete()
  ↓ persists to
course_completions.status
  ↓ serialized by
CourseCompletionResource
  ↓ returned by
GET /api/course-completions
  ↓ rendered by
web/components/CompletionBadge.tsx
```

A path with unlabeled arrows is a file list drawn vertically. The labels are the
analysis.

## Distinguishing hard and soft edges

- **Hard edge** — import, call, foreign key, type reference. Breaks loudly at
  build or test time. High confidence.
- **Soft edge** — string match, convention, configuration, reflection, dynamic
  dispatch, generated client. Breaks quietly at runtime. Medium or low
  confidence, and usually belongs under HIDDEN COUPLING.

Soft edges are where post-deploy incidents come from; they deserve the most
attention and the most careful confidence labeling.

## Monorepos

- Read the workspace config (`pnpm-workspace.yaml`, `turbo.json`, `nx.json`,
  `lerna.json`, Gradle settings, Cargo workspace members) before searching.
- A shared package changing means every dependent package is in scope — check
  each package manifest for the dependency rather than assuming.
- Published packages have consumers outside the repository. Say so under
  OPEN QUESTIONS rather than claiming the surface is fully mapped.

Workspace detection, package-graph construction, scoping rules, and where
cross-package coupling hides: `monorepo.md`.

## Knowing when to stop

Stop when new searches return only files already classified, or files with no
relationship to the change statement. Report what remains unexplored — private
packages, generated clients, external repositories — instead of leaving a silent
gap.
