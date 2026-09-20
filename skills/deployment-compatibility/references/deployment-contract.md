# The deployment contract

What this project requires in order to run, derived from the project itself.
Every line names the file that establishes it. A contract without provenance is
a guess with a table around it.

## The two rules that do most of the work

**A file is not authoritative because of its name.** These are all common, and
each produces a confidently wrong contract:

| Looks authoritative | Often is not |
| --- | --- |
| `docker-compose.yml` | A local development convenience nobody deploys |
| `.env.example` | Three variables behind the code, and two ahead of it |
| `Procfile` | Left over from a platform the team moved off |
| `Dockerfile` | One of three, and not the one CI builds |
| `k8s/` | An experiment from a migration that did not happen |
| `README` deployment section | Accurate on the day it was written |

Cross-check every line against what the code actually does. When two sources
disagree, the code wins and **the disagreement is itself a finding** — a compose
file that starts a service the application never connects to means somebody's
mental model is wrong, and that is worth a line in the report.

**An underivable requirement is `UNKNOWN`.** Never an estimate. "A Next.js build
needs about 2 GB" is a plausible sentence that turns into a matrix row indistinguishable
from a measured one. If the repository does not establish it, the row says
`UNKNOWN`, and what would establish it is named — usually a measured build.

## Deriving each class

### Runtime

```
engines / packageManager / .nvmrc / .node-version   package.json
python_requires / .python-version / tool sections   pyproject.toml, setup.cfg
require.php / platform                              composer.json
go directive                                        go.mod
<java.version>, toolchain, sourceCompatibility      pom.xml, build.gradle
FROM <image>:<tag>                                  Dockerfile
image tag, language version                         CI workflow files
```

When several disagree, report the disagreement. A `Dockerfile` on Node 18, an
`engines` field demanding `>=22` and a CI matrix on 20 is three answers, and the
one that matters is whichever actually starts the process on the target.

The lockfile matters as much as the runtime. A lockfile produced by a newer
package manager than the target has can fail to install at all, and the error
message rarely says so plainly.

### Services

Derive from **client usage**, not from configuration files:

```
a database client, ORM or migration directory       → which engine, and a floor version
a queue or job library with a connection             → the broker it connects to
a cache client                                       → the cache, and whether it is optional
a search client                                      → the engine
```

The floor version is usually established by something specific: a generated
client pinned to a server version, a migration using a syntax introduced in a
release, an extension the schema requires, a driver's own minimum. Cite it. If
nothing establishes a floor, the requirement is the engine with no version bound
— say that rather than inventing `>= 14`.

A service the project *can* use but does not require is a different row. Mark it
`N/A` when the project will not use it in this deployment, and say why.

### Processes

Every process type the deployment needs, established from what runs it:

```
web          the HTTP server entry point
worker       a queue consumer — a separate process, not a thread of the web app
scheduler    periodic work: a cron entry, a timer, an in-app scheduler
realtime     a websocket or streaming process, when it is separate
```

The common and expensive finding: a project has a worker, and the deployment has
no execution model for it. The queue library is installed, jobs are enqueued,
and nothing consumes them. Enqueued work vanishing silently is worse than an
error, because nothing reports it.

Treat these as distinct requirements. A `docker-compose.yml` with one service
for a project with three process types is a `BLOCKED` row, not a detail.

### Ports

The port the application will actually bind, and whether it is configurable:

```
a literal in the server entry point                 → fixed
process.env.PORT with a default                     → configurable, with a default
EXPOSE                                              → documentation, not a binding
the reverse proxy's upstream                        → what the proxy expects
```

A fixed port that is occupied on the target is `BLOCKED`. A configurable one is
`FIT` with a condition naming the variable.

### Storage

The question is persistence, and it is answered by finding where the application
writes:

```
upload handlers        a local path, or an object-storage client?
generated artifacts    reports, invoices, exports, thumbnails, caches
session or lock files  a local path shared between processes?
temporary files        volume, size, and cleanup
logs                   a file, or standard output?
```

Then the dangerous pattern, which is worth stating explicitly because it is the
most common silent data loss in modern deployments:

```
the application writes uploads to a local path
+ the deployment target's filesystem is ephemeral (a container with no volume,
  an immutable image, a platform with an ephemeral disk)
= every upload disappears on the next deploy, with no error at any point
```

That is a finding whenever both halves hold. Establish the second half from
`docker inspect` mounts, the compose `volumes:` block, or the platform's
documented behavior — never from the assumption that a container is ephemeral.

### Database

```
migration mechanism     and whether it runs at release or at process start
pending migrations      count them
destructive operations  a drop, a non-nullable column with no default, a rename
connection pool         size per process × process count vs the server's limit
extensions              required, and whether they are present
SSL requirement         what the client demands, and what the server offers
```

Pool arithmetic is a real and frequently missed row: four web processes with a
pool of ten, plus two workers with a pool of five, is fifty connections against
a default `max_connections` of a hundred that something else is also using.

Migration-at-start plus multiple replicas is another: every replica runs the
migration at once, and whether that is safe depends on the tool's locking. Say
which it is rather than assuming.

### Environment variables

Build the inventory from **code usage first**, then reconcile:

```bash
grep -rn "process.env\.\|import.meta.env\.\|os.environ\|getenv\|ENV\[" src/ app/ lib/
```

Then compare against `.env.example`, the deployment files, the CI configuration
and the target's actual environment. Classify each:

```
REQUIRED / OPTIONAL      does the code fail without it, or fall back?
BUILD / RUNTIME          needed when the artifact is built, or when it runs?
PUBLIC / SECRET          does it reach the client bundle?
```

The findings this produces are specific and each one is a real deployment
failure:

- **Used and undocumented** — it will be missing on the target
- **Documented and unused** — the deployment carries a variable nothing reads
- **Build-time treated as runtime** — a value inlined at build time cannot be
  changed by setting it on the server, and the app will silently use the old one
- **Secret exposed to the client** — a key under a public prefix
  (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`) is in the bundle, and rotating it is
  the only fix
- **Missing on the target** — present in code and `.env.example`, absent where
  it runs

Report status only: `PRESENT`, `MISSING`, `REDACTED`. Never a value, never a
fragment of one.

### External integrations

Everything the deployment depends on that is not on the target: mail relay,
payment provider, object storage, OAuth provider, webhook senders and receivers,
external APIs, DNS.

Each one records **from where it was checked**. "Reachable" from a laptop is not
evidence about the server, and a webhook receiver needs the target reachable
from the outside, which is a different claim from the target reaching out.

### Resources

Only what the repository establishes:

| Derivable | Not derivable from a repository |
| --- | --- |
| A configured container memory limit | How much memory the app needs under load |
| Worker concurrency from configuration | The right concurrency for this hardware |
| A documented minimum in the project's own docs | A number from experience with similar apps |
| A build that failed at a known limit | Peak traffic behavior |

Everything in the right column is `UNKNOWN`. A measured build on the target, or
a single observed run, converts one of them — and until it does, the row says so.

## Shape

```
RUNTIME    Node >= 22               package.json engines.node
           pnpm 10.4                packageManager, pnpm-lock.yaml lockfileVersion 9
SERVICES   PostgreSQL >= 16         prisma/schema.prisma; client pinned to 16
           Redis                    src/queue/connection.ts — BullMQ
PROCESSES  web                      server.ts
           worker                   src/queue/worker.ts — consumes "emails"
PORTS      3000 (PORT)              server.ts, configurable, default 3000
STORAGE    uploads/ must persist    src/uploads/store.ts — local writes
DATABASE   14 pending migrations    prisma/migrations/; release-time, not start-time
           pool 10 per process      prisma datasource
ENV        7 required, 2 optional   inventory below
EXTERNAL   SMTP relay, Stripe webhook receipt (inbound)
RESOURCES  UNKNOWN                  nothing establishes a memory or CPU figure
```

Every line is a matrix row in the next phase. A contract line nobody can compare
against the target is not dropped — it becomes an `UNVERIFIED` row with the
check that would settle it.
