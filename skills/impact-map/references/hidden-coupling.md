# Hidden Coupling

Dependencies that no import graph will show. This is the phase that separates an
impact map from a code search, and the source of most "we didn't expect that to
break" incidents.

Everything found here is **indirect evidence**. Label the mechanism, keep the
confidence honest, and give the reader the check to run.

## Raw strings shadowing a typed value

The domain has `CompletionStatus.COMPLETED`; somewhere else the code compares
against `"completed"`.

Search the literal value in every casing and separator style used by the
repository, and look in serializers, validation rules, config, templates, and
query builders.

```
grep -rn --include=* -e '"completed"' -e "'completed'" -e '`completed`'
```

Why it matters: renaming or splitting the enum leaves the literal silently
matching nothing.

## Raw SQL

Query builders and ORMs are traceable; raw SQL is not.

Search for the table and column names, plus SQL keywords near them — `SELECT`,
`INSERT`, `UPDATE`, `WHERE`, `JOIN` — across application code, migrations,
reports, analytics jobs, and `.sql` files. Views, materialized views, and
stored procedures count.

## Temporal coupling

Files that git history says keep being committed together, with no import,
call, or shared symbol between them. This is the only coupling mechanism in this
document that is invisible in the working tree — it exists only in the log.

Read it as a ratio (a file in most of the target's commits, not two of forty),
discard lockfiles and formatting sweeps, and cap the finding at Medium
confidence: history proves correlation, not causation. Commands and reporting
rules: `git-signals.md`.

## Direct data access bypassing the domain

Code reaching the table without going through the service or repository that
owns it: a controller running a query inline, a job updating rows directly, an
admin script, a seeder. Each one is a second implementation of the rule you are
about to change.

## Duplicated business logic

The same decision expressed in more than one place:

```
status === "completed"
$completion->status === CompletionStatus::COMPLETED
WHERE status = 'completed'
```

Find them by searching the *decision*, not the symbol. Every copy has to move
together, and the copies rarely live in the same layer.

## Configuration

Environment variables, config keys, feature flags, permission identifiers,
plan/tier names, cron expressions. Search `.env.example`, config directories,
deployment manifests, CI files, and infrastructure-as-code. Flag any key whose
meaning changes even when its name does not.

## Events and listeners

Subscribers usually bind by event name string or by convention, so the producer
has no reference to them. Search the event name, the payload field names, and
the listener registration mechanism. Include cross-service events on a broker —
the consumer may not be in this repository at all.

## Jobs, workers, and schedules

Queued payloads carry a serialized shape. Changing that shape breaks jobs
already sitting in the queue during deploy. Search job classes, worker
definitions, scheduler entries (cron, Celery beat, scheduled commands), and any
payload keys matching the affected fields.

## Serialization and contracts

API resources, DTOs, serializers, GraphQL schemas, OpenAPI documents, protobuf
definitions, generated clients, CSV/Excel export column headers, webhook
payloads. A field name in any of these is a public contract even when it never
appears as a symbol.

## Tests, factories, and fixtures

Factories with hardcoded state values, JSON fixtures, snapshot files, seeded
databases, VCR/HTTP cassettes. These break in ways that read as "the test is
wrong" rather than "the change is incomplete". Search the affected values inside
test directories specifically.

## Generated code

Generated API clients, ORM types, migration snapshots, `*.generated.*` files,
protobuf output. Do not propose editing generated files — identify the generator
and its source of truth, and note that regeneration is required.

## Documentation and runbooks

API docs, README examples, onboarding guides, support runbooks, and inline
comments describing the old behavior. Stale documentation about a status
workflow is a real defect for the next person.

## Search discipline

- Search values, not only identifiers.
- Try every casing convention the repository uses: `snake_case`, `camelCase`,
  `PascalCase`, `kebab-case`, `SCREAMING_SNAKE`.
- Include tests, fixtures, config, docs, and infrastructure directories.
- Exclude vendor and dependency directories, but check lockfile-adjacent
  workspace packages in a monorepo.
- Prefer a handful of high-signal hits with explanations over an exhaustive dump
  of every match.

## Reporting

For each finding: path, the exact matched text, the coupling type, why it
connects to the change, confidence, and the concrete check or edit. A hidden
coupling entry with no matched text is speculation — either find the evidence or
move it to OPEN QUESTIONS.
