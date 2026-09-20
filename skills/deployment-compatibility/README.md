# Deployment Compatibility Engineer

An Agent Skill for the question that only exists once you name a server:

> **Does this project fit this target environment — and what has to change
> before it does?**

```bash
npx skills add soumyaRauth/skills-hub --skill deployment-compatibility
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill deployment-compatibility --agent claude-code
```

---

## Why it exists

Deployment failures are rarely code failures. They are **mismatches** — a
requirement the project has and the environment does not meet, discovered at the
worst possible moment:

```
the runtime is one major version behind what the lockfile was built for
the queue library is installed and no Redis is running
the app writes uploads to a local path on an ephemeral filesystem
the worker process has no supervisor, so it runs once and never again
the migration runs on every replica at once
an environment variable exists in .env.example and nowhere on the box
```

Every one of those is visible *before* the deploy, from two things that are
usually both available and never compared: what the repository requires, and
what the server provides.

The other half of the problem is the report. Ask a capable agent whether an app
will run on a server and you will get a confident yes, assembled from a
plausible mental model of Ubuntu. This skill is built so that answer cannot be
produced: every row of its matrix carries where each side came from, and the
readiness state is computed from those provenances rather than written by hand.

## What it does

```
target + project → deployment contract → compatibility matrix
                 → exposure & operability → remediation → verification
                 → READY · READY WITH CONDITIONS · BLOCKED · NOT ASSESSED
```

```
DEPLOYMENT COMPATIBILITY
TARGET   Ubuntu 24.04 · 4 vCPU · 7.8 GB · Docker 27.1      tier READ-ONLY
PROJECT  Next.js 15 · Node 22 · PostgreSQL · Redis · 1 worker
STATE    🔴 BLOCKED

Requirement        Project needs    Target provides           Result
──────────────────────────────────────────────────────────────────────
Node               >= 22            20.11.1        MEASURED   BLOCKED
PostgreSQL         >= 16            16.2           MEASURED   FIT
Redis              required         not installed  MEASURED   BLOCKED
Worker process     required         no supervisor  MEASURED   BLOCKED
uploads/ persists  required         container fs   INFERRED   RISK
RAM                UNKNOWN          7.8 GB         MEASURED   UNVERIFIED
```

Four worked examples: [a blocked runtime](examples/blocked-runtime.md) ·
[the honest common case](examples/ready-with-conditions.md) ·
[no server access at all](examples/no-access.md) ·
[a deployment that starts and dies](examples/failing-deployment.md)

## The rule that makes the verdict mean something

`READY` requires that the target was actually inspected.

A target fact is `MEASURED` (a command ran and its output was read), `SUPPLIED`
(the user or a document said so), `INFERRED`, or `UNKNOWN`. A row that fits on
`SUPPLIED` evidence **cannot** produce `READY` — it becomes a numbered condition
for someone to confirm. A row whose project side is `UNKNOWN` is `UNVERIFIED`,
never `FIT`, because not knowing how much memory an application needs is not the
same as having enough.

So the common honest answer is `READY WITH CONDITIONS`, and the conditions are
the deliverable. `NOT ASSESSED` is a real outcome rather than a failure: with no
access and no specification, the server side of every row is unknown, and saying
so is the correct report.

## Access tiers

The tier is established first and caps every claim the report can make.

| Tier | What exists | Ceiling |
| --- | --- | --- |
| `NONE` | No access, no specification | `NOT ASSESSED` |
| `DECLARED` | A spec, provider page, or the user's description | `READY WITH CONDITIONS` |
| `READ-ONLY` | Commands can run; nothing may change | Full assessment, no server changes |
| `AUTHORIZED` | Named changes permitted | Assessment and remediation within that named list |

Nothing here assumes a tier, and nothing pretends to a capability it does not
have. Where the target could not be reached, the report says so and names the
check that would settle it.

## When it activates

It activates on its own when a concrete deployment target is in view — *deploy
this to my VPS*, *will this run on my server*, *here are my server details*,
*prepare this for production* — and when a deployment already exists and
misbehaves.

It stays quiet for generic Docker, Linux, Kubernetes and cloud questions, local
development setup, CI that ships nothing, and ordinary application work. The
word *deploy* in a sentence is not a target environment.
See [Activation](SKILL.md#activation).

## What it will not do

- **Promise a deployment will work.** No "seamless", no "guaranteed", no "100%
  compatible". The strongest claim available is which requirements were
  satisfied, on what evidence, and what was not checked.
- **Invent a fact about your server.** Versions, memory, disk, ports, service
  states and certificate dates come from output actually read or from you. There
  is no library of typical servers to fall back on.
- **Change your server on its own.** Discovery is read-only. Server changes are
  proposed, classified by impact, and applied only when you authorize that
  specific action.
- **Weaken a control to get a deploy through.** It will not expose a database,
  disable TLS, loosen authentication, or turn on development mode on a server. A
  blocked deployment is a finding.
- **Keep your secrets.** Values are reported as `PRESENT`, `MISSING` or a
  redacted stub, and nothing is written into its state directory.

## Where it fits

[Production Guard](../production-guard/README.md) asks whether the change is
safe to ship. This asks whether the environment can run it. They answer
different questions and neither verdict substitutes for the other:

```
change → production-guard   → safe to ship?
project + server → deployment-compatibility → can it run there?
```

Standards and privacy questions raised by the environment go to
[Standards Compass](../standards-compass/README.md). A deployment fix that
reaches shared storage or a module boundary goes to
[Impact Map](../impact-map/README.md) first. A deployment failure whose cause is
genuinely unclear goes to
[Engineering Investigator](../engineering-investigator/README.md), and this
skill supplies the environment evidence.

## State

`.deployment-compatibility/` holds the target facts with their dates, the derived
contract, the matrix and the open findings — so a second session does not
re-derive the project or re-ask you for the server details. It never holds a
secret, and the server always outranks the file: a recorded fact is re-verified
before anything is built on it.

References: [`target-discovery.md`](references/target-discovery.md) ·
[`deployment-contract.md`](references/deployment-contract.md) ·
[`compatibility-matrix.md`](references/compatibility-matrix.md) ·
[`remediation.md`](references/remediation.md) ·
[`verification.md`](references/verification.md) ·
[`incident.md`](references/incident.md)

## Limitations

- It reads a repository and whatever the target lets it read. Behavior under
  real traffic, real data volume and real concurrency is not reproducible from
  either, and the report says so rather than estimating.
- A resource requirement that the repository does not establish stays `UNKNOWN`.
  This skill will not tell you how much memory your application needs.
- External integrations are reachable or not *from where the check ran*. A
  provider reachable from your laptop is not evidence about the server.
- An absent finding is not proof of absence, and a `FIT` row is a statement
  about one requirement at one moment, not about the deployment as a whole.
- The readiness state is advisory. A human owns the decision to deploy.

## License

MIT — see [`LICENSE`](../../LICENSE) at the repository root.
