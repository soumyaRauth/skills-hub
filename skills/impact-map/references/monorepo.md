# Monorepos

In a monorepo the blast radius stops being "which files" and starts being
"which packages, and who consumes them". Scope the analysis before searching it,
and state the scope in the report — an unscoped monorepo analysis is either
noise or a silent omission.

## Detect the workspace

| Marker | Tool |
| --- | --- |
| `pnpm-workspace.yaml` | pnpm workspaces |
| `workspaces` in `package.json` | npm / yarn / bun workspaces |
| `turbo.json` | Turborepo (task graph, `dependsOn`) |
| `nx.json`, `project.json` | Nx (project graph, tags) |
| `lerna.json` | Lerna |
| `rush.json` | Rush |
| `go.work` | Go workspace |
| `[workspace]` in `Cargo.toml` | Cargo workspace members |
| `settings.gradle(.kts)` `include` | Gradle multi-project |
| `pom.xml` `<modules>` | Maven multi-module |
| `*.sln` | .NET solution |
| `pyproject.toml` per directory, `uv.lock`, `poetry` path deps | Python workspace |

No marker does not mean no monorepo. Multiple manifests in sibling directories,
or `apps/` + `packages/` + `services/`, is the same problem without the tooling.

## Build the package graph before searching

1. List the packages and their manifest names — the **published name** is what
   dependents reference, and it is rarely the directory name.
2. For each package, read its dependencies and find the internal ones
   (`workspace:*`, `link:`, `file:`, path dependencies, or a name that matches
   another package in the repo).
3. Invert it: for the package holding the change, list every package that
   depends on it, directly and transitively.

```bash
# JS/TS: names and internal dependents
grep -h '"name"' packages/*/package.json apps/*/package.json
grep -rn '"@myorg/target-package"' --include=package.json .

# Cargo / Go / Gradle equivalents
grep -rn 'target-crate' --include=Cargo.toml .
grep -rn 'module-path' --include=go.mod .
grep -rn "project(':target')" --include='*.gradle*' .
```

Tool-native graph commands are read-only and faster when present:
`pnpm list --depth -1`, `pnpm why <pkg>`, `nx graph --file=/dev/stdout`,
`nx show projects --affected`, `turbo run build --dry=json`,
`cargo metadata --no-deps`, `go list ./...`.

Use them if they are already installed. Do not install anything to get a graph.

## Scope the analysis, then say so

Declare the scope in the report under `REPOSITORY SCOPE`:

```
REPOSITORY SCOPE

Workspace:     pnpm, 14 packages
Change origin: packages/domain
In scope:      packages/domain, packages/api, apps/web, apps/admin
               (direct or transitive dependents of the change origin)
Not inspected: apps/mobile — depends on @org/api-client only, no reference to
               the changed symbol found
Published:     @org/domain is published to the internal registry; consumers
               outside this repository cannot be enumerated here
```

Rules:

- Scope by the **dependency graph**, not by directory proximity. A sibling
  package that does not depend on the change origin is not in scope; a distant
  app that does is.
- A package that depends on the change origin is in scope **for inspection**,
  not automatically a finding. Inspect it, then classify it.
- Naming what you did not inspect, and why, is part of the deliverable.

## Where cross-package coupling hides

- **Path aliases and re-exports.** `tsconfig.json` `paths`, `compilerOptions.
  references`, barrel `index.ts` files, and `exports` maps mean an importer may
  reference a symbol through a name that grep never connects to the source file.
  Resolve the alias, then search both spellings.
- **Version pinning.** A dependent pinned to a published version does not pick
  up a workspace change until it is released. That changes the action, not the
  finding — say which dependents consume the workspace copy and which consume a
  registry version.
- **Generated clients and contracts.** OpenAPI/GraphQL/protobuf artifacts
  generated in one package and committed into another are a hard edge with no
  import between the source and the consumer.
- **Shared config packages.** ESLint, tsconfig, Tailwind, and build presets are
  consumed by every package; a change there has the widest surface in the repo
  and the least visible one.
- **Task graphs.** `turbo.json` `dependsOn`, Nx `implicitDependencies`, and
  Gradle task wiring encode relationships the source does not.
- **Shared fixtures and test utilities.** One package's factory feeding another
  package's suite.
- **Deployment boundaries.** Two packages in one repo can be two running
  services with independent deploy cadences — a shared type change is then a
  wire-compatibility change, not a compile-time one. Check CI and deployment
  manifests before assuming they ship together.

## Large repositories

When the graph is too large to inspect honestly:

1. Ask the user to name the entry packages, or pick them from the change
   statement and say which you picked.
2. Analyze the change origin and its direct dependents in full.
3. For transitive dependents, report the path and the fact that they were not
   inspected — as `NEEDS VERIFICATION`, not as silence.

Partial coverage that names its boundary is useful. Partial coverage presented
as complete is the failure this skill exists to prevent.

## Published packages

If the changed package is published — public registry or internal — its
consumers are not enumerable from this repository. State it once under
`REPOSITORY SCOPE` and again under `OPEN QUESTIONS`, and treat any claim about
those consumers as unverified.
