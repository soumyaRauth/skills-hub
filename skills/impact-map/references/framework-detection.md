# Framework Detection

Reconnaissance cues per ecosystem. These are *hints for where to look first*,
never a substitute for reading the actual tree. When convention and repository
disagree, the repository wins.

## Establishing the ecosystem

Read the manifests first — they identify language, framework, scripts, and test
runner in one pass.

| Signal | Ecosystem |
| --- | --- |
| `package.json`, `*-lock.yaml`, `tsconfig.json` | JavaScript / TypeScript |
| `composer.json`, `artisan` | PHP / Laravel |
| `pyproject.toml`, `requirements.txt`, `manage.py` | Python |
| `pom.xml`, `build.gradle` | Java / Kotlin |
| `go.mod` | Go |
| `Gemfile`, `config/routes.rb` | Ruby / Rails |
| `Cargo.toml` | Rust |
| `*.csproj`, `*.sln` | .NET |

Workspace markers — `pnpm-workspace.yaml`, `turbo.json`, `nx.json`,
`lerna.json`, Cargo `[workspace]`, Gradle `settings.gradle` — mean the change
surface spans packages.

## JavaScript / TypeScript

- Entry points and scripts in `package.json`; path aliases in `tsconfig.json`
  (aliases hide import relationships from naive grep — resolve them).
- Barrel files (`index.ts`) obscure who imports what; search the concrete module
  path too.

**Next.js** — `next.config.*`, plus `app/` (route handlers `route.ts`, layouts,
server components, `"use client"` boundaries, server actions) or `pages/` (page
components, `pages/api/`). Routing is by file path, so a route has no symbolic
reference anywhere. Data fetching, caching, and revalidation tags are coupling
points.

**React** — components, hooks, context providers, and state stores (Redux,
Zustand, Jotai, TanStack Query keys). Query keys and cache tags are string
coupling.

**Node backends** — routes/controllers/services/repositories, middleware,
workers, event handlers, and whatever ORM is present (Prisma schema, TypeORM
entities, Drizzle schema, Sequelize models).

## PHP / Laravel

`composer.json`, `app/Models`, `app/Http/Controllers`, `app/Http/Requests`,
`app/Http/Resources`, `app/Services`, `app/Policies`, `app/Jobs`, `app/Events`,
`app/Listeners`, `app/Notifications`, `app/Console/Commands`, `routes/*.php`,
`database/migrations`, `database/factories`, `database/seeders`, `config/`,
`tests/Feature`, `tests/Unit`.

Convention-heavy: models map to tables implicitly, policies bind to models by
name, events bind to listeners through the provider, and the scheduler lives in
the console kernel or `routes/console.php`. Expect real edges with no textual
reference.

## Python

**Django** — `manage.py`, `settings.py`, apps with `models.py`, `views.py`,
`serializers.py`, `urls.py`, `admin.py`, `signals.py`, and `migrations/`.
Signals are hidden coupling. The admin is a real consumer of model fields.

**FastAPI / Flask** — routers/blueprints, Pydantic or marshmallow schemas,
dependency-injected services, SQLAlchemy models and Alembic migrations.

**Celery** — task modules, beat schedules, queue routing. Task payloads are a
serialization contract.

## Java / Kotlin

Spring: `@RestController`, `@Service`, `@Repository`, `@Entity`, `@Component`,
`@Scheduled`, `@EventListener`, plus `application.yml` profiles. Component
scanning and annotation-driven wiring mean dependencies are often not visible as
direct constructor references. Flyway/Liquibase hold the schema history.

## Ruby on Rails

`app/models`, `app/controllers`, `app/jobs`, `app/serializers`, `db/migrate`,
`db/schema.rb`, `config/routes.rb`, `spec/` or `test/`. Callbacks, concerns, and
`ActiveSupport::Notifications` are hidden coupling.

## Go / Rust / .NET

Go: packages, handlers, interface implementations (implicit — search for the
method set), `go.mod` module path, `sqlc`/`ent`/`gorm` layers.
Rust: crates and workspace members, trait implementations, `sqlx` macros.
.NET: controllers, services, EF Core `DbContext` and migrations, DI
registrations in `Program.cs`/`Startup.cs`.

## Cross-cutting locations worth checking in any stack

- Database: migrations directory, schema snapshot, seeders, factories.
- Async: queues, workers, schedulers, brokers.
- Contracts: OpenAPI/GraphQL/protobuf definitions, generated clients.
- Config: `.env.example`, config directories, deployment manifests, CI files.
- Infrastructure: Terraform, Helm, Docker Compose — they carry env keys and
  scheduled task definitions.
- Feature flags: provider SDK usage and flag key strings.

## When the stack is unfamiliar

Fall back to structure: find the manifest, find the test directory, find the
directory names that repeat across the tree, and follow one request end to end.
The goal is to learn where *this* repository puts each layer — the framework
name is only a shortcut to that answer.
