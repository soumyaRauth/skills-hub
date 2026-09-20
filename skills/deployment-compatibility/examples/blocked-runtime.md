# Example — a supplied specification, and four findings behind the obvious one

Illustrative. The repository and the server are invented; the shape of the
assessment is the point.

---

**Request:**

> Get this app ready to deploy on my Ubuntu VPS. I put the server details in
> `server-spec.md`.

---

## Phase 1 — Target and tier

No command channel to the box. A specification exists, so the tier is
`DECLARED`, and every target fact from it is `SUPPLIED`.

```
Tier        DECLARED
Source      server-spec.md, supplied in the repository
Available   the operator's own description of the host
Not         any command against the target; the database host; DNS; the provider console
```

That ceiling is decided before anything else is read: at this tier the best
reachable state is `READY WITH CONDITIONS`, because nobody has looked at the
server. It can still come out `BLOCKED`, and it does.

## Phase 2 — The deployment contract

```
RUNTIME    Node >= 22           package.json engines.node ">=22.0.0"
           pnpm 10.4            packageManager; pnpm-lock.yaml lockfileVersion 9
SERVICES   PostgreSQL >= 16     prisma/schema.prisma, provider postgresql
           Redis                src/queue/connection.ts — ioredis, REDIS_URL
PROCESSES  web                  src/server.ts
           worker               src/queue/worker.ts — consumes the "emails" queue
PORTS      3000, fixed          src/server.ts — app.listen(3000), no PORT read
STORAGE    ./uploads persists   src/uploads/store.ts — writeFile to a local path
DATABASE   2 pending migrations prisma/migrations/
ENV        6 required           inventory below
EXTERNAL   SMTP relay           src/mailer.ts
RESOURCES  UNKNOWN              nothing in the repository establishes a figure
```

Two contract lines came from reading code against the files that claim to
describe the deployment, and disagreed with them:

- `docker-compose.yml` defines one service, `app`. The project has **two**
  process types. The compose file is not the contract; `Procfile` and the worker
  entry point are.
- `.env.example` lists `SMTP_HOST` and `SMTP_PORT`. `src/mailer.ts` reads
  `SMTP_URL`. The example file is behind the code.

## Phase 3 — Matrix

```
Requirement        Project needs      Target provides            Result
────────────────────────────────────────────────────────────────────────
Node               >= 22              20.11.1        SUPPLIED    BLOCKED
pnpm               10.4               not listed     UNKNOWN     UNVERIFIED
PostgreSQL         >= 16              16.2           SUPPLIED    FIT
Redis              required           not installed  SUPPLIED    BLOCKED
Port 3000          fixed              free           SUPPLIED    FIT
Worker process     required           no manager     INFERRED    BLOCKED
uploads/ persists  required           no volume      INFERRED    BLOCKED
Migrations         2 pending          —              UNKNOWN     UNVERIFIED
SMTP_URL           required           —              UNKNOWN     UNVERIFIED
RAM                UNKNOWN            7.8 GB         SUPPLIED    UNVERIFIED
```

The last row is the one people argue about. 7.8 GB sounds like plenty. But the
project side is `UNKNOWN` — nothing in the repository establishes what this
application needs — so the row cannot be `FIT`. Having a number on one side of a
comparison is not a comparison.

## Findings

```
DC-001  RUNTIME · 🔴 BLOCKER · BLOCKED
Project declares Node >= 22; the specification states 20.11.1.
Evidence   package.json engines.node ">=22.0.0"
           server-spec.md line 4, SUPPLIED
Impact     The build tooling requires 22. `next build` fails before the app runs.
Recommend  Deploy in the project's own Node 22 image rather than raising the
           host runtime — the spec says two other services share this box.

DC-002  QUEUE · 🔴 BLOCKER · BLOCKED
The project requires Redis; the specification lists no Redis.
Evidence   src/queue/connection.ts — new IORedis(process.env.REDIS_URL)
           src/queue/worker.ts — BullMQ Worker("emails")
Impact     Without it the web process fails to start: the connection is opened
           at module load, not lazily. This is a startup failure, not a
           degraded feature.

DC-003  WORKER · 🔴 BLOCKER · BLOCKED
The project has two process types; the deployment defines one.
Evidence   Procfile declares web and worker; docker-compose.yml has one service
Impact     Email jobs are enqueued and never consumed. Nothing errors — the
           queue grows, and users see mail that never arrives.

DC-004  STORAGE · 🔴 BLOCKER · BLOCKED
Uploads are written to a local path with no persistent volume.
Evidence   src/uploads/store.ts — writeFile("./uploads/" + name)
           docker-compose.yml declares no volumes (INFERRED: container filesystem)
Impact     Every uploaded file is lost on the next deploy, silently.

DC-005  CONFIGURATION · 🟠 HIGH · UNVERIFIED
SMTP_URL is read by the code and documented nowhere.
Evidence   src/mailer.ts reads SMTP_URL; .env.example has SMTP_HOST/SMTP_PORT
Impact     It will be missing on the target, and mail fails at first send
           rather than at startup.
Status     PRESENT/MISSING on the target is unknown at this tier.

DC-006  EXPOSURE · 🟠 HIGH · RISK
The specification shows PostgreSQL listening on 0.0.0.0:5432.
Evidence   server-spec.md line 11, SUPPLIED
Impact     If no firewall rule covers it, the database is reachable from the
           internet. The spec does not state the firewall rules.
HANDOFF → standards-compass: a customer database potentially exposed to a
          public network [DC-006]
```

## The answer

```markdown
DEPLOYMENT COMPATIBILITY
────────────────────────────────────────
TARGET   Ubuntu 24.04 · 4 vCPU · 7.8 GB · Node 20.11.1      tier DECLARED
PROJECT  Next.js · Node 22 · PostgreSQL · Redis · web + worker
STATE    🔴 BLOCKED

Everything below is from your server-spec.md. Nothing was measured on the host.

BLOCKERS
1. Node 20.11.1 on the host, project requires >= 22          DC-001
2. Redis required and not installed — the web process will
   not start without it, not merely degrade                  DC-002
3. The worker has no execution model; compose defines one
   service and the project has two process types             DC-003
4. Uploads write to a local path with no volume — every
   file is lost on the next deploy                           DC-004

WARNINGS
· SMTP_URL is read by src/mailer.ts and is in no env template   DC-005
· PostgreSQL is listening on 0.0.0.0 per the spec; firewall
  rules were not stated                                        DC-006

VERIFIED   nothing on the target — no access at this tier
UNVERIFIED pnpm availability · migration state · SMTP reachability
           · what this app needs for memory (the repository does not say)

RECOMMENDED, in order
1. Build and run in a Node 22 image — smallest fix for DC-001, and it
   does not touch the runtime the other two services on this box use.
2. Add Redis to the deployment, and a named volume for uploads.
3. Add a worker service that runs the worker entry point.
4. Add SMTP_URL to .env.example and to the host's environment.
5. Send me `ss -tulpn` and `ufw status` so DC-006 can be settled.

Want me to make changes 1–4? They are all project-side and reversible.
```

## What this run did not do

- **It did not say the deployment would work after the four fixes.** Four
  blockers resolved is four rows moving; six rows are still unverified, and the
  verdict after remediation would be `READY WITH CONDITIONS` at best, because
  every target fact here is supplied.
- **It did not estimate memory.** 7.8 GB against `UNKNOWN` is not a fit, and
  "should be plenty for a Next.js app" is the sentence this skill exists to not
  write.
- **It did not touch the server.** There is no access, and inventing what a
  typical Ubuntu box has is fabrication whether or not it happens to be right.
- **It did not fix DC-006 by proposing a firewall change.** The rules were never
  read; changing a firewall from a guess is how access is lost.
- **It did not run a standards assessment** on the exposed database. It named
  it once, handed it over, and moved on.
