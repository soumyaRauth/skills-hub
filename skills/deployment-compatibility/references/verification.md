# Verification

Turning deployment requirements into things that were observed. The rule this
whole file exists to enforce: **starting once is not verification**, and
*verified somewhere else* is not *verified here*.

## Where the check ran

Every result carries one of these, and they are never blurred:

```
ON TARGET               ran against the deployment target
EQUIVALENT ENVIRONMENT  ran against something built to match it — say how it matches
LOCAL                   ran on the development machine
NOT RUN                 with the reason, and what would let it run
```

An equivalent environment is legitimate and often the only safe option — you do
not rehearse a deploy on a production box. It is worth stating what makes it
equivalent (same base image, same runtime version, same service versions) and
what does not (real data volume, real traffic, real network paths, the target's
own configuration). A rehearsal that shares the image but not the database
version has verified the build, not the migration.

## Proof per requirement class

Prefer the cheapest observation that actually establishes the requirement.

| Requirement | What establishes it | What does not |
| --- | --- | --- |
| Runtime version | The version the process itself reports at startup | The version on the interactive shell's `PATH` |
| Dependencies install | The install command completing from the lockfile | The lockfile existing |
| Build | The build command producing the artifact | The build script being present |
| Application starts | A health response after startup | The container reaching `running` |
| Database reachable | A query through the application's own configuration and credentials | A port being open, or `pg_isready` |
| Cache reachable | The application's client performing a round trip | The service being listed as running |
| Migrations | Applying them and reading the resulting schema version | A migration directory being present |
| Worker runs | Enqueue one job, observe it consumed | The worker process existing |
| Scheduler runs | A timer or cron entry firing once, observed | A crontab line existing |
| Static assets | Fetching one through the proxy, not from the app | The build output directory existing |
| TLS | A request completing, and the certificate's dates and names | The certificate file existing |
| Uploads persist | Write a file, restart, read it back | A volume appearing in the compose file |
| External service | A connect test **from the target** | Reachability from anywhere else |

The right-hand column is where false verification comes from. Every entry in it
is a real thing that a report can honestly say it observed, and none of them is
evidence for the requirement in the left-hand column.

## The application-level check

The distinction that matters most, because it is the one that passes when the
deployment is broken:

```
port probe        something is listening on 5432
service status    postgresql.service is active (running)
application check the app connected with its own credentials, to its own
                  database, and read a row
```

Only the third establishes the requirement. Wrong credentials, wrong database
name, an unmet SSL requirement, a `pg_hba` rule that rejects the app's host, a
connection limit already exhausted — all of them pass the first two.

## Restart and recovery

The deployment that starts once and never again is the outcome this section
exists to catch. Each of these is a separate check, and each fails independently.

```
process restart     stop the process; does the supervisor bring it back?
container restart    docker restart; does it come back healthy, unaided?
host reboot          will it start on boot, or only because someone started it?
dependency blip      stop the database, restart it; does the app reconnect,
                     or does it need a restart of its own?
deploy over it       redeploy; does uploaded data survive? does state?
proxy reload         reload the proxy; do in-flight requests survive?
```

Two of them deserve naming in most reports:

**Will it start on boot?** A container run without a restart policy, or a service
that was started by hand and never enabled, works perfectly until the host
reboots. This is readable rather than testable when a reboot is not available:
the restart policy, or whether the unit is enabled, is a `MEASURED` fact.

**Does it reconnect?** A pool that does not recover from a database restart turns
a thirty-second maintenance window into an outage that lasts until someone
notices. Testable safely in an equivalent environment, and worth doing there.

When a check cannot be run safely on the target, say what it would take rather
than skipping it:

```
UNVERIFIED  survives a host reboot
            The restart policy is "no" (docker inspect, MEASURED), so it will
            not. Setting it to unless-stopped and rebooting a staging host
            would settle it.
```

## Validating the artifact, not the source

The thing being deployed is an image, a bundle, a binary or a release — not the
repository. They differ, and the differences are where deployments fail:

```
does the build succeed from a clean checkout, not from the working tree?
is the runtime inside the artifact the one the contract requires?
are production dependencies present, and development ones absent?
are the files the app reads at runtime actually in the artifact?
is configuration read at runtime, or baked in at build time?
are build-time public variables the right ones for this environment?
is a secret baked into a layer? (it stays in the image history after deletion)
does it run as a non-root user, and can that user write where it must?
does the declared port match what the process binds?
does the health check inside the artifact point at a path that exists?
```

The secret in a layer is worth checking specifically: a `COPY .env` followed by
a `RUN rm .env` leaves the file in the image, retrievable by anyone who can pull
it. Deleting it in a later layer does not remove it.

## The rehearsal

Where an equivalent environment is available, run the deployment path in order
and record each step's real result. Stop at the first failure — the steps after
it have not been verified, and reporting them as untested is the honest thing:

```
1. build the artifact from a clean checkout
2. start it with the target's configuration shape, secrets redacted
3. health endpoint responds
4. each required service answers an application-level check
5. migrations apply, from the schema version the target actually has
6. one job through the queue, consumed by the worker
7. a request through the proxy, including a static asset
8. restart; healthy again, and data still present
```

Label the whole rehearsal with where it ran. "Verified in an equivalent
environment: same base image and service versions; the target's data volume and
network paths were not reproduced."

## Handing proof over

When a requirement must be proven rather than observed once — it has to keep
holding, or it needs a test that fails without it — that is a contract
requirement and it belongs to the skill that owns proof:

```
HANDOFF → proof-driven-dev: the worker must survive a restart with in-flight
          jobs requeued rather than lost [DC-007]
```

This skill establishes that a deployment requirement is satisfiable in this
environment. It does not own `VERIFIED` as a status word, and it never reports
a check as run when it did not run.
