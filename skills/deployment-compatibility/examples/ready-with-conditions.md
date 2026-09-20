# Example — the honest common case

Most assessments of a reasonably prepared project end here, and the conditions
are the deliverable. Illustrative; the repository and host are invented.

---

**Request:**

> We deploy tomorrow. I've given you read-only SSH to app-02 — is it ready?

---

## Phase 1 — Target and tier

The request asks for the readiness decision itself, so this runs `GATING`.

```
Tier        READ-ONLY
Available   SSH to app-02 as deploy; docker; systemctl status; read /etc/nginx
Not         the managed PostgreSQL host, DNS records, the provider console
```

`READ-ONLY` was not assumed — `uname -srm` answered, and the user granted
nothing beyond reading. No server change is applied in this run, including the
one that would resolve a condition.

## Phase 3 — Matrix

```
Requirement          Project needs     Target provides             Result
──────────────────────────────────────────────────────────────────────────
Node                 >= 20             v20.11.1       MEASURED     FIT
Architecture         amd64 image       x86_64         MEASURED     FIT
PostgreSQL           >= 14             15.6           MEASURED     FIT
  reachable          app credentials   connected      MEASURED     FIT
Redis                >= 6              7.2.4          MEASURED     FIT
Port 8080            configurable      free           MEASURED     FIT
web process          required          compose svc    MEASURED     FIT
worker process       required          compose svc    MEASURED     FIT
Restart policy       survives reboot   unless-stopped MEASURED     FIT
uploads/             persists          named volume   MEASURED     FIT
TLS                  required          valid, 67 d    MEASURED     FIT
Proxy upload limit   25 MB             25m            MEASURED     FIT
Disk                 build headroom    41 GB free     MEASURED     FIT
Connection pool      30 total          max_conn 100   SUPPLIED     FIT
Migrations           3 pending         release step   MEASURED     RISK
SMTP relay           required          —              UNKNOWN      UNVERIFIED
Memory               UNKNOWN           7.8 GB         MEASURED     UNVERIFIED
```

Fifteen rows fit. Three do not, and they are the report.

**The pool row** is `FIT` on `SUPPLIED` evidence. `max_connections` is 100
according to the operator; the database host is outside the access boundary, so
it was not read. Under the promotion rules that cannot produce `READY` — it
becomes a condition. This is the rule earning its keep: the arithmetic is fine
if the number is right, and nobody here checked the number.

**The migration row** is `RISK`, not `BLOCKED`. Migrations run as a release step
rather than at container start, which is correct. But one of the three adds a
non-nullable column to a populated table, and the compose file starts two
replicas of `web`. The old replica is briefly live against the new schema.

**Memory** is `UNVERIFIED` for the usual reason: 7.8 GB is measured, and the
project side is `UNKNOWN`. The build was run here and peaked at 1.9 GB, which is
a real observation — and it is a measurement of the build, not of the
application under traffic.

## Verification

```
ON TARGET (read-only)
  container images present, digests match the release tag       ✓
  postgres reachable with the app's own credentials             ✓  application-level
  redis round trip via the app's client                         ✓
  TLS: valid, expires in 67 days, renewal timer enabled         ✓
  restart policy unless-stopped on both services                ✓

EQUIVALENT ENVIRONMENT (same base image, same service versions)
  build from clean checkout                                     ✓  peak 1.9 GB
  start → /health responds, and reports its database dependency ✓
  one job enqueued → consumed by the worker                     ✓
  restart → healthy, uploaded file still present                ✓
  database restarted underneath → pool reconnected in 4 s       ✓

NOT RUN
  SMTP connect from app-02 — egress on 587 was not tested, and
  read-only access does not include opening a socket outward
  behavior under real traffic and real data volume
```

The equivalent environment matched on base image and service versions. It did
not reproduce the target's data volume, its network paths, or the managed
database. Saying so is what keeps the first block meaningful.

## The answer

```markdown
DEPLOYMENT COMPATIBILITY
────────────────────────────────────────
TARGET   Ubuntu 24.04 · 4 vCPU · 7.8 GB · Docker 27.1        tier READ-ONLY
PROJECT  Node 20 · PostgreSQL · Redis · web + worker
STATE    🟠 READY WITH CONDITIONS

No blockers. Fifteen of eighteen requirements were measured on app-02 and fit.

CONDITIONS
1. Confirm PostgreSQL max_connections is 100. You told me it is; the database
   host is outside my access. At 30 pooled connections you are fine at 100 and
   over-subscribed at 50. `SHOW max_connections;` settles it.
2. Decide how migration 0003 lands. It adds a non-nullable column to a populated
   table, and compose runs two web replicas — during the rollout the old replica
   is live against the new schema. Either make it nullable-then-backfill, or
   take the brief single-replica window deliberately.
3. Accept that SMTP was not tested from app-02. Egress on 587 is unverified;
   `nc -z relay.example.net 587` from the host settles it.

VERIFIED ON TARGET
✓ Node 20.11.1, amd64, matches the image
✓ PostgreSQL 15.6 reachable with the application's own credentials
✓ Redis 7.2.4 reachable through the app's client
✓ TLS valid, 67 days, renewal timer enabled
✓ Both services restart unless-stopped, so a reboot brings them back
✓ uploads/ is a named volume, not container filesystem

VERIFIED IN AN EQUIVALENT ENVIRONMENT — not on app-02
✓ Build, start, health, one queued job consumed
✓ Survives restart with uploaded data intact
✓ Reconnects when the database restarts underneath it (4 s)

UNVERIFIED
? SMTP reachability from the host          (condition 3)
? Behaviour under real traffic and data volume — not reproducible here
? Memory required by the application. The build peaked at 1.9 GB in the
  equivalent environment; nothing establishes what it needs under load.

Conditions 1 and 3 are one command each and I cannot run either — both are
outside read-only access. Condition 2 is a decision, and I would take the
single-replica window.
```

## What makes this the honest outcome

- **Fifteen fits did not become `READY`.** One supplied fact and two unverified
  rows are exactly what the rules say they are. The temptation is to call this
  ready and list the three as notes; the rule removes the temptation.
- **Every condition is one action by one person.** Not "monitor the
  deployment", not "ensure adequate resources".
- **The two verification blocks are separate**, and the second one says what the
  equivalent environment did not reproduce.
- **The memory row stayed unverified even with a real measurement**, because the
  measurement was of the build and the requirement is about load. A number does
  not resolve a row it does not answer.
