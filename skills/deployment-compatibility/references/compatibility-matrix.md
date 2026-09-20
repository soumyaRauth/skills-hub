# The compatibility matrix

The comparison itself: one row per contract line, both sides carrying their
provenance, one result each, and a verdict computed from the results rather than
written by hand.

## The row

```
Requirement   Project needs   [why]      Target provides   [grade]   Result
```

Both sides are mandatory. A row with no project side is a server audit; a row
with no target side is a wish list. Neither is a compatibility assessment.

```
Node          >= 22    engines      20.11.1      MEASURED    BLOCKED
PostgreSQL    >= 16    schema       16.2         MEASURED    FIT
Redis         required queue conn   absent       MEASURED    BLOCKED
Port 3000     default  configurable free         MEASURED    FIT
Worker        required Procfile     no manager   MEASURED    BLOCKED
uploads/      persists store.ts     container fs INFERRED    RISK
RAM           UNKNOWN  —            7.8 GB       MEASURED    UNVERIFIED
SMTP          required mailer.ts    —            UNKNOWN     UNVERIFIED
Sentry DSN    optional  —           —            —           N/A
```

## Results

| Result | Meaning |
| --- | --- |
| `FIT` | The requirement is met, and evidence on both sides says so |
| `BLOCKED` | The requirement is not met, and evidence says so. Deployment cannot succeed as it stands |
| `RISK` | Met today, and something observed makes it fragile: an ephemeral filesystem, a certificate expiring in nine days, a pool that fits with no headroom, a service with no restart policy |
| `UNVERIFIED` | Not established here. Names the check that would settle it |
| `N/A` | The project has no such requirement in this deployment. Say why, so a reader can disagree |

## Promotion rules

These are the mechanism, not advice. They are what keeps a matrix from drifting
into optimism one row at a time.

1. **A `FIT` needs evidence on both sides.** A requirement derived from the
   repository, and a target fact that is `MEASURED` or `SUPPLIED`.
2. **An `INFERRED` or `UNKNOWN` target fact can never produce `FIT`.** The best
   available result is `RISK` or `UNVERIFIED`.
3. **A `FIT` on `SUPPLIED` evidence becomes a condition.** It is a real fit and
   it was not checked here. It appears in the matrix as `FIT` and in the report
   as a numbered condition, and it prevents `READY`.
4. **An `UNKNOWN` project side yields `UNVERIFIED`, never `FIT`.** Not knowing
   what an application requires is not evidence that the target satisfies it.
5. **A version comparison uses the real constraint.** `>= 16` against `16.2` is
   a fit; `^16.0` against `17.1` is not. Read the operator, and prefer the
   project's own declared range over a judgment about what probably works.
6. **Four service facts, not one.** Installed, running, reachable and compatible
   are separate. A row is `FIT` only when all four hold; when reachability was
   not tested, the row is `UNVERIFIED` however healthy the service looks.

## Categories

Every finding names one. Use the ones that materially apply and leave the rest
out — a report that lists a category per empty section is padding.

```
RUNTIME      DEPENDENCY   BUILD        ARTIFACT
DATABASE     MIGRATION    CACHE        QUEUE        STORAGE
NETWORK      PORT         DNS          TLS          REVERSE_PROXY
PROCESS      WORKER       CRON         RESOURCE     PERFORMANCE
CONFIGURATION SECRETS     EXPOSURE     PERMISSIONS
EXTERNAL_SERVICE          OBSERVABILITY             RECOVERY
DEPLOYMENT   ROLLBACK     DATA_INTEGRITY
```

## Severity

The house scale. Severity is about consequence; the result is about evidence,
and they are set independently.

| | Meaning here |
| --- | --- |
| 🔴 **BLOCKER** | The deployment cannot succeed, or succeeds and loses data, or exposes something it must not |
| 🟠 **HIGH** | Real risk of failure or data loss under conditions that will occur |
| 🟡 **MEDIUM** | Meaningful, and survivable for now |
| 🔵 **LOW** | Worth fixing, not worth delaying a deploy for |

Do not inflate. A missing runtime is a blocker; a reverse-proxy timeout that is
generous is not. Calling everything a blocker destroys the signal that makes the
readiness state worth reading.

## The finding

Keep it to what changes what the reader does. The last four fields appear only
when a change was actually made.

```
DC-014

Category      RUNTIME
Severity      🔴 BLOCKER
Result        BLOCKED

Finding       The project declares Node >= 22; the target provides 20.11.1.
Evidence      package.json engines.node ">=22.0.0"
              node --version → v20.11.1 on app-01, MEASURED 2026-09-20
Impact        The lockfile was produced by pnpm 10, which requires Node 20.11+
              to install and 22 to run the build's own tooling. `next build`
              fails before the application starts.
Recommend     Build and run in the project's Node 22 image, or raise the
              runtime on the host through whatever manages it.

Remediation   Dockerfile base moved from node:20-alpine to node:22-alpine.
Verification  Image built; container started; /api/health returned 200.
              Verified in an equivalent local container, not on app-01.
Rollback      Revert the Dockerfile line and rebuild.
Confidence    High — both sides measured.
```

Confidence describes the evidence. Severity describes the consequence. A serious
problem you are unsure of is a high severity at medium confidence, and saying
both is the point.

## The verdict

Apply mechanically, then explain the reasoning. If the state feels wrong, a row
is wrong — fix the row, never the rule.

| State | Rule |
| --- | --- |
| 🔴 **BLOCKED** | At least one `BLOCKED` row, or an open BLOCKER finding |
| ⬜ **NOT ASSESSED** | The contract could not be derived, or the target side is `UNKNOWN` throughout — tier `NONE` ends here |
| 🟠 **READY WITH CONDITIONS** | No blockers, and at least one row is `RISK` or `UNVERIFIED`, or at least one `FIT` rests on `SUPPLIED` evidence |
| 🟢 **READY** | Every derived requirement is `FIT` on `MEASURED` evidence or `N/A`, and no blocker or high finding is open |

Three consequences worth being explicit about:

- **`READY` requires that the target was inspected.** At tier `DECLARED`, every
  target fact is `SUPPLIED`, so the ceiling is `READY WITH CONDITIONS` by
  construction. That is correct, not pedantic: nobody has looked at the server.
- **`READY WITH CONDITIONS` is the normal good outcome.** Its conditions are the
  deliverable, numbered, each one something a person can confirm or accept.
- **`NOT ASSESSED` is a result.** It is what honest output looks like when there
  is nothing to assess against, and it is never rounded up because the project
  side looked fine.

## Conditions

A condition is actionable by one person in one step, and says who confirms it:

```
1. Confirm the target has 8 GB of memory — supplied in the request, not measured.
   `free -h` on the host settles it.
2. Confirm the uploads volume in docker-compose.yml is mounted on the host and
   is on persistent storage. Without it, uploads are lost on the next deploy.
3. Accept that SMTP reachability from the target was not tested. A connect test
   from the host to the relay settles it.
```

Not conditions: "monitor the application", "be careful with migrations", "ensure
adequate resources". Those are true of every deployment and actionable in none.
