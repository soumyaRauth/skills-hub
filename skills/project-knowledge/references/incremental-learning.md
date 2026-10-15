# Incremental learning

A run should cost in proportion to what changed, not to the size of the
repository. That is what makes it cheap enough to run every few commits.

## First run

Walk structure, not content:

1. The top-level tree, two levels deep, minus `node_modules`, `.git`, build
   output and vendored code.
2. Manifests and scripts: `package.json`, `pyproject.toml`, `go.mod`,
   `Makefile`, `docker-compose.yml`, CI workflows. These give the stack and the
   real commands.
3. The README, existing `CLAUDE.md` / `AGENTS.md`, `.env.example`.
4. Entry points: the server bootstrap, the router, the job runner, the CLI. Read
   enough to trace one request through.
5. Migrations or schema files: the data model's shape.
6. Recent history: `git log --oneline -50`, for the decisions that are still
   fresh.

Stop when `architecture.md` can say what each part is for and how a request
flows. A first run that reads every file has wasted most of what it read.

## Later runs

Cheapest view first, and stop once you know enough:

| Step | Command | Gives |
| --- | --- | --- |
| 1 | `git log --format='%h %s%n%b' <last>..HEAD` | the decisions and the why, in the authors' words |
| 2 | `git diff --stat <last>..HEAD` | which areas moved, and how much |
| 3 | `git diff <last>..HEAD -- <path>` | the detail, only for paths that change structure or contracts |

Paths that earn step 3: a new top-level directory, scripts in a manifest, env
and config files, migrations and schemas, route and handler registration,
message or event definitions, anything that changes how the parts connect.

Paths that never do: lockfiles, tests, fixtures, snapshots, generated code,
formatting-only changes.

## When the cursor is gone

The recorded commit is missing from history (a rebase, a squash, a shallow
clone): treat it as a first run, but keep the existing docs and update them
rather than starting over. Say so in the report.

## What is not worth a run

Copy changes, dependency patch bumps, test-only commits. The hook counts
commits, not significance, so a run over such a range ends quickly: read the
log, find nothing worth recording, move the cursor.
