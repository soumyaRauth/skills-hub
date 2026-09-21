---
name: deployment-compatibility
description: Assess whether a specific project can run on a specific target environment — a VPS, a cloud or bare-metal VM, a Docker host, a staging or production server — and prepare it to. Derives what the project actually requires from its own code (runtime versions, services, environment variables, ports, worker and cron processes, storage persistence, migrations, external integrations), establishes what the target actually provides at whatever access level exists, compares the two, and answers READY, READY WITH CONDITIONS, BLOCKED or NOT ASSESSED with the evidence behind each line. Remediates the project side, proposes server changes rather than making them, and verifies start, restart and recovery where it can. Use when a deployment target is named, when asked whether a server can host this application, or when something works locally and fails on the server. Not for generic Docker, Linux, cloud-provider or CI questions, local development setup, or work with no target environment in view.
---

# Deployment Compatibility Engineer

Every other review in this repository has one operand: the change. This one has
two.

> **Does this project fit this server?**

Not *is this code good*, and not *is this change safe to ship* — Production
Guard owns that. This is the question that only exists once a concrete target is
named, and it is the one nobody answers until the deploy fails:

```
TARGET ENVIRONMENT  +  PROJECT  →  DEPLOYMENT CONTRACT
                                          ↓
                          COMPATIBILITY MATRIX
                                          ↓
              REMEDIATION → VERIFICATION → READINESS
```

The deliverable is a **readiness state with a matrix behind it** — every
requirement the project has, what the target provides, and how each of those two
facts was established. A deployment guide is not the deliverable, and neither is
a list of best practices that were true before anyone named a server.

The failure this skill exists to prevent is not missing an incompatibility. It
is the confident summary:

> *"Everything checks out — you're ready to deploy."*

when the runtime version was never read, the Redis requirement was inferred from
a config file nothing imports, and "the server has 8 GB" came from the user's
memory of the invoice.

## Activation

**Engage when** a concrete deployment target is in view: *deploy this to my
VPS*, *will this run on my server*, *prepare this for production*, *here are my
server details*, *audit this box before I put the app on it*. Also when a
deployment already exists and does not behave — *it works locally but crashes on
the server* — and when the repository keeps `.deployment-compatibility/`.

**Stay quiet when** there is no target environment in the request: generic
Docker, Linux, Kubernetes or cloud-provider questions, local development setup,
CI configuration that ships nothing, a Dockerfile edit that is a comment or a
formatting change, and ordinary application work. A word like *deploy*,
*server*, *container* or *production* in a sentence is not a target environment.
An application bug that happens to have been noticed in production belongs to
`engineering-investigator`, not here.

**Depth** `ACTIVE`. `GATING` only when someone asked for the readiness decision
itself — *are we ready to deploy* — in which case the verdict is the answer.
`CONSULT` when a target is named in passing and two or three lines of fit change
what gets built.

**Composes with** `production-guard` (it decides whether the change is safe to
ship; this decides whether the environment can run it, and neither answer
substitutes for the other) · `impact-map` (when a deployment fix changes shared
storage, configuration or a module boundary) · `proof-driven-dev` (a deployment
requirement that must be proven becomes a contract requirement) ·
`standards-compass` (exposure, secrets handling and personal data in the target
environment are its call, not this skill's) · `engineering-investigator` (a
broken deployment whose cause is genuinely unclear) · `dependency-guard` (a
remediation that would install something new).

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. If it is
  not installed, do the smallest version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
- **Lessons.** On engaging, read `~/.skills-hub/lessons/<this skill's name>.md`
  if it exists. When a person corrects this skill's work (a miss, a false
  alarm, a wrong verdict), or the work exposes a gap in this file that another
  project would hit too, append one line to it:
  `- YYYY-MM-DD · <the rule, stated for any project> — <what went wrong>`.
  Never write project names, paths, identifiers, code or data there; facts about
  one repository are project state. Keep at most 20 lines, merging or replacing
  one to add another. A lesson sharpens this file's checks and never overrides
  its rules or a person's instruction. The file sits outside every project, so
  no read-only rule covers it. Say `Lesson recorded: <rule>` once; if the file
  cannot be written, give the lesson in the reply instead.
<!-- /skills-hub:protocol -->

## Non-negotiable rules

1. **Never claim a deployment will work.** No "this will deploy successfully",
   "seamless", "guaranteed", "fully secure", "100% compatible", "zero risk".
   The strongest available claim is *every requirement derived from this
   repository was satisfied by evidence read from this target, and here is what
   was not checked.* Readiness is a state with a matrix under it, never a
   reassurance.
2. **Both sides of every row carry their provenance.** A requirement is derived
   from a named file. A target fact is `MEASURED`, `SUPPLIED`, `INFERRED` or
   `UNKNOWN`. A row missing either side is not a row, it is a guess.
3. **A fit on supplied evidence is a condition, not a pass.** If the target fact
   came from the user, a document or a dashboard screenshot rather than from
   this environment, it cannot produce `READY`. It becomes a condition someone
   confirms. This rule is what makes `READY` mean anything.
4. **Never invent a target fact.** No version, core count, memory figure, disk
   figure, port state, service status, certificate expiry or container limit
   that was not read from output or supplied by the user. "A typical Ubuntu
   server has…" is fabrication with a reassuring voice.
5. **Never invent a project requirement either.** If the repository does not
   establish how much memory the application needs, the requirement is
   `UNKNOWN`, not an estimate. An estimate presented as a requirement produces a
   matrix row that looks measured and is not. See `references/deployment-contract.md`.
6. **Read before you write, and ask before you change the target.** Discovery on
   a target is read-only. Project-side remediation follows the request. Anything
   that changes the target environment is proposed, classified by impact, and
   executed only on explicit authorization for that specific action.
7. **Never weaken a control to make a deployment work.** Do not expose a
   database to reach it, disable TLS, loosen a firewall blindly, turn off
   authentication, widen permissions, or set a framework to development mode on
   a server. A blocked deployment is a finding. A deployed insecure one is an
   incident.
8. **Never persist or print a secret.** Values become `PRESENT`, `MISSING` or a
   redacted stub. Nothing under `.deployment-compatibility/` ever holds a
   password, key, token, connection string or certificate.
9. **State the access tier in every report.** What could not be reached is named,
   not silently absent. An unreachable thing is `UNVERIFIED` with the check that
   would settle it.
10. **Verified in an equivalent environment is not verified on the target.** Say
    which one, every time.

## Access tiers

The tier is established first, stated in the report header, and caps everything
the report may claim. Most bad deployment advice is a tier-three conclusion
written from tier-zero information.

| Tier | What exists | What the report may claim |
| --- | --- | --- |
| `NONE` | No target access and no specification | Project side only. The target side of every row is `UNKNOWN`, and readiness is `NOT ASSESSED` |
| `DECLARED` | A written specification, provider page, infrastructure config, or the user's own description | Target facts are `SUPPLIED`. Best achievable state is `READY WITH CONDITIONS` |
| `READ-ONLY` | Commands can run on the target; nothing may change | Target facts are `MEASURED`. Remediation is proposed, never applied to the server |
| `AUTHORIZED` | Named changes to the target are permitted | `MEASURED`, and remediation inside the named scope — which is a list, not a blanket |

Never assume a tier. Establish it by trying the cheapest read and observing what
happens, and record the boundary out loud:

> Tier `READ-ONLY`. Available: SSH to app-01, `docker`, `systemctl status`,
> read access to `/etc/nginx`. Not available: the database host, the managed
> Redis instance, DNS records, the provider console.

`references/target-discovery.md` has what to inspect per layer, the read-only
command for each, and the path to follow when the tier is `NONE`.

## Evidence grades

Every target fact carries one. They are not severities and they are not
confidence levels — they record *where the fact came from*, which is the thing
a reader needs in order to trust a row.

| | Meaning |
| --- | --- |
| `MEASURED` | A command ran against the target and its output was read |
| `SUPPLIED` | Stated by the user or a document; plausible, and unverified here |
| `INFERRED` | Derived from another observation, which is named |
| `UNKNOWN` | Nothing establishes it, and the check that would is named |

An `INFERRED` or `UNKNOWN` target fact can never produce a satisfied row. A
`SUPPLIED` one can, and it becomes a condition (rule 3).

## Modes

| Mode | When | What it produces |
| --- | --- | --- |
| **ASSESS** | A target is named and nothing has been prepared yet | Contract, matrix, findings, readiness state. Read-only on the target; no project changes unless asked |
| **PREPARE** | *Get this ready to deploy there* | ASSESS, then authorized remediation, then verification, then readiness re-stated |
| **DIAGNOSE** | A deployment exists and misbehaves | The difference between where it works and where it does not, classified — `references/incident.md` |

`REVIEW` is not a fourth mode. When `.deployment-compatibility/` exists, read it
first and re-verify what you are about to rely on: a recorded target fact ages,
and the server outranks the file.

## Workflow

Phases 1–5 run in every mode. Phase 6 runs when remediation was requested and
authorized; phase 7 whenever anything can be exercised at all.

### Phase 1 — Establish the target and the tier

Before reading the project, find out what can be seen. Name the environment type
(VPS, cloud VM, bare metal, Docker host, managed platform, staging box), the
access tier, and the boundary. Do not start assessing a server you have not
established you can see.

Discovery is read-only, in this order — cheapest first, and each result narrows
what is worth asking next: operating system and architecture · CPU, memory, swap
and disk · runtimes and package managers · container runtime, images, volumes,
restart policies · services (web server, database, cache, queue, process
manager, cron) · listening ports and their bind addresses · TLS and the reverse
proxy · resource pressure and current load.

`references/target-discovery.md` carries the commands and what each one settles.

### Phase 2 — Derive the deployment contract

Read the project for what it *requires at runtime*, not for what it contains.
Every line of the contract names the file that establishes it:

```
RUNTIME    Node >= 22            package.json engines.node
           pnpm 10.4             packageManager field, pnpm-lock.yaml present
SERVICES   PostgreSQL >= 16      prisma/schema.prisma, generated client pinned
           Redis                 src/queue/connection.ts — BullMQ connection
PROCESSES  web · worker          Procfile; worker consumes the BullMQ queue
PORTS      3000                  server.ts, and the Dockerfile EXPOSE
STORAGE    uploads/ persistent   src/uploads/store.ts writes to the local path
DATABASE   migration on release  prisma/migrations/, 14 pending
ENV        DATABASE_URL, REDIS_URL, AUTH_SECRET, APP_URL   (see the inventory)
EXTERNAL   SMTP, Stripe webhook receipt
MEMORY     UNKNOWN               nothing in the repository establishes a figure
```

Two rules do most of the work here. **A file is not authoritative because of its
name** — a `docker-compose.yml` nobody deploys, a `.env.example` three variables
behind the code, and a `Procfile` for a platform the team left are all common,
and each one produces a confident wrong contract. Cross-check every line against
actual usage. And **an underivable requirement is `UNKNOWN`**, never an estimate.
Method, per-requirement derivation, and the environment-variable inventory:
`references/deployment-contract.md`.

### Phase 3 — Build the compatibility matrix

One row per contract line. Both sides, both provenances, one result:

```
Requirement        Project needs    Target provides           Result
──────────────────────────────────────────────────────────────────────
Node               >= 22            20.11.1        MEASURED   BLOCKED
PostgreSQL         >= 16            16.2           MEASURED   FIT
Redis              required         not installed  MEASURED   BLOCKED
Port 3000          free             free           MEASURED   FIT
Worker process     required         no supervisor  MEASURED   BLOCKED
uploads/ persists  required         container fs   INFERRED   RISK
RAM                UNKNOWN          7.8 GB         MEASURED   UNVERIFIED
SMTP reachable     required         —              UNKNOWN    UNVERIFIED
```

Results: `FIT` · `BLOCKED` · `RISK` (satisfied today, and something observed
makes it fragile) · `UNVERIFIED` (not established here, with the check named) ·
`N/A` (the project has no such requirement). The row model, the categories, and
the finding shape live in `references/compatibility-matrix.md`.

A row where the project side is `UNKNOWN` is `UNVERIFIED`, never `FIT`. Not
knowing how much memory an application needs is not the same as having enough.

### Phase 4 — Assess exposure and operability

Two questions the matrix does not ask by itself.

**Exposure.** For every port, service and path, establish whether it is public,
internal, loopback-only, container-only, or unknown — a database being installed
says nothing about who can reach it. Report what is reachable from where, with
the observation that established it. Secrets on disk, world-readable
configuration, a Docker socket mounted into a container, and a service running
with more privilege than it needs belong here.

When the deployment touches personal data, authentication, payments or a
regulated domain, that is a standards question, and it goes to its owner:

```
HANDOFF → standards-compass: the target stores customer exports on a host path
          with no stated retention [DC-011]
```

**Operability.** Can this be run once it is there? Logs reachable, a health
signal that means something, failures visible, log growth bounded, and a way to
tell that a worker died. Deployment operability only — broader production
readiness is Production Guard's.

### Phase 5 — State readiness

The verdict follows mechanically from the matrix. Apply the rules, then explain.

| State | Rule |
| --- | --- |
| **BLOCKED** | At least one row is `BLOCKED`, or an open BLOCKER finding |
| **NOT ASSESSED** | The contract could not be derived, or the target side is `UNKNOWN` throughout — tier `NONE` ends here |
| **READY WITH CONDITIONS** | No blockers, and at least one row is `RISK` or `UNVERIFIED`, or at least one `FIT` rests on `SUPPLIED` evidence. Each one becomes a numbered condition |
| **READY** | Every derived requirement is `FIT` on `MEASURED` evidence or `N/A`, and no blocker or high finding is open |

`READY` is deliberately hard to reach: it requires that the target was actually
inspected. If a verdict feels too harsh, the matrix is what to fix — never the
rule. Missing evidence never becomes `READY`.

### Phase 6 — Remediate what is authorized

Project remediation and server remediation are different things and are never
mixed in one list.

**Project side** — Dockerfile, compose file, process definitions, health
endpoints, startup and shutdown behavior, connection pools, migration ordering,
environment templates, reverse-proxy configuration derived from the application,
resource limits, logging. This is ordinary work on the repository, and it
follows the request.

**Server side** — proposed, classified, and applied only on explicit
authorization for that specific action:

```
SAFE          reversible, no service interruption, no data
CONFIRM       brief interruption, or configuration that must be replaced
HIGH IMPACT   affects other tenants of the box, or is hard to undo
MANUAL ONLY   the agent proposes the command and the operator runs it
```

Every non-trivial change answers six questions before it is made: what is
changing, why, what evidence justifies it, what could break, how it will be
verified, and how to roll it back. When the change reaches shared storage,
configuration or a module boundary, `HANDOFF → impact-map` first.
`references/remediation.md` carries the classes, the never-list and the rollback
model.

### Phase 7 — Verify

Starting once is not verification. The checks that matter, in order of what they
buy: the artifact builds · it starts · the health signal responds · each required
service answers an application-level check, not a port probe · migrations apply ·
each process type runs, including the worker nobody tests · **it survives a
restart** · it recovers when a dependency drops and returns.

Label every check with what it ran against — the target, or an equivalent
environment — and never promote the second into the first. A check that could
not run is `UNVERIFIED` with the reason, not silence. For anything that must be
proven rather than observed once:

```
HANDOFF → proof-driven-dev: the worker must survive a restart with its queue
          intact [DC-007]
```

`references/verification.md` has the proof available for each requirement class
and the restart and recovery procedures.

## Report format

Concise, evidence-rich, and separated — blockers, conditions, verified,
unverified, and recommended actions never share a list.

```
DEPLOYMENT COMPATIBILITY
────────────────────────────────────────
TARGET      Ubuntu 24.04 · 4 vCPU · 7.8 GB · Docker 27.1     tier READ-ONLY
PROJECT     Next.js 15 · Node 22 · PostgreSQL · Redis · 1 worker
STATE       🔴 BLOCKED

BLOCKERS           the rows that stop it, each with both sides and its evidence
CONDITIONS         what must be true or accepted, numbered
VERIFIED           what was established, and against what
UNVERIFIED         what was not, and the check that would settle it
RECOMMENDED        ordered, smallest first
```

Detail stays available and out of the default answer: the full matrix, the
commands, the contract derivation. Do not print every command that ran unless
someone asks. Emoji follow the house scale — 🔴 blocker, 🟠 high, 🟡 medium,
🔵 low.

## State

`.deployment-compatibility/`, created only when there is something worth carrying
between sessions:

```
target.md       environment, access tier, measured facts with dates
contract.md     what the project requires, and the file establishing each line
matrix.md       the comparison and its results
findings.md     open findings, remediation applied, verification, rollback
```

Two files is a complete workspace for most assessments. Record facts and
decisions, never narration. **No secrets, ever** — not in an example, not in a
connection string, not in a redacted-looking fragment that still carries half a
key. A target fact has a date, because an eight-week-old memory figure is not a
measurement any more.

## What this skill is not

- **Not a deployment tutorial.** It does not teach Docker, Nginx or systemd. It
  reads what this project needs and what this target provides.
- **Not a vulnerability scanner or a penetration test.** It reports exposure it
  observed and says what it did not test. Standards and control questions belong
  to `standards-compass`.
- **Not Production Guard.** That skill asks whether the change is safe to ship.
  This one asks whether the environment can run it. Both can be needed, and
  neither verdict is the other's.
- **Not an infrastructure provisioner.** It does not choose a cloud, generate an
  infrastructure-as-code estate, or install software because it might be useful.
- **Not a debugger.** A deployment whose cause is genuinely unclear goes to
  `engineering-investigator`; this skill supplies the environment evidence.

## References

- `references/target-discovery.md` — access tiers, per-layer inspection, read-only commands, the no-access path
- `references/deployment-contract.md` — deriving requirements from repository evidence, the environment-variable inventory
- `references/compatibility-matrix.md` — row model, results, categories, finding shape, the verdict rules
- `references/remediation.md` — project versus server changes, impact classes, authorization, rollback
- `references/verification.md` — proof per requirement class, artifact validation, restart and recovery
- `references/incident.md` — works here and fails there: difference classes and failure classification

## Worked examples

`examples/blocked-runtime.md` — a supplied specification, a runtime mismatch, and
three more findings behind it · `examples/ready-with-conditions.md` — the honest
common case, where most of it fits and the conditions are the deliverable ·
`examples/no-access.md` — no target at all, and the report that refuses to
pretend otherwise · `examples/failing-deployment.md` — DIAGNOSE mode on a
deployment that starts and dies.
