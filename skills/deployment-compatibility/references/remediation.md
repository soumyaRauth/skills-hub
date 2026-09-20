# Remediation

Fixing what can be fixed, proposing what must not be fixed unilaterally, and
never buying a successful deployment with a weakened control.

## The two lists never merge

**Project remediation** is ordinary work on the repository. It follows the
request like any other change, and it is reversible through version control.

**Server remediation** changes a machine that other things may depend on, that
may be serving traffic, and whose previous state may not be recoverable. It is
proposed, classified, and applied only on explicit authorization for that
specific action.

A report that mixes them invites someone to run the second list because they
approved the first.

## Project side

What genuinely belongs here — each one a deployment property of the project
rather than a property of the server:

```
container image        base image, runtime version, build stages, non-root user
compose / manifests    services per process type, volumes, restart policy, limits
process definitions    web, worker, scheduler — each with its own entry point
health endpoint        one that checks its dependencies, not one that returns 200
startup                fail fast on missing configuration, with the name in the error
graceful shutdown      handle the termination signal; finish or requeue in-flight work
connection pools       sized against the server's real connection limit
migrations             release-time rather than every-replica-at-start
environment template   .env.example reconciled with actual code usage
reverse proxy config   derived from this application's limits and timeouts
logging                to standard output where the platform collects it, bounded otherwise
retry and backoff      on the dependencies that legitimately blip
```

The health endpoint is worth singling out. `return 200` proves the process is
alive and nothing else, so a container that cannot reach its database stays in
rotation and every request fails. A health check that verifies its critical
dependencies is the single highest-value project-side change available in most
assessments.

When a project change reaches shared storage, configuration or a module
boundary — moving uploads to object storage, changing how configuration is
loaded, splitting a process — map it before making it:

```
HANDOFF → impact-map: moving uploads from the local path to object storage
          touches the upload handler, the report generator and two tests [DC-009]
```

## Server side

### Impact classes

| Class | Meaning | Authorization |
| --- | --- | --- |
| `SAFE` | Reversible, no interruption, touches no data — creating a directory, writing a new file that nothing reads yet | Within an `AUTHORIZED` scope that names it |
| `CONFIRM` | Brief interruption, or replaces configuration — restarting the app, reloading the proxy, installing a package | Ask, every time, naming the interruption |
| `HIGH IMPACT` | Affects other things on the box, or is hard to undo — a firewall change, a shared service restart, a version upgrade | Ask, with blast radius and rollback stated |
| `DESTRUCTIVE` | Removes or overwrites something that may not come back | Propose the command; the operator runs it |
| `MANUAL ONLY` | Cannot be safely automated from here regardless of authorization | Propose only |

When two classes could apply, take the higher one and say so. A package install
that pulls a new version of a shared library is not `SAFE` because the install
command exits zero.

### Never, regardless of authorization

These are not held back for caution. Each one converts a blocked deployment into
a worse outcome than not deploying:

```
delete or reset a database, drop a table, truncate, or run a destructive migration
delete files, volumes or images whose contents were not established
remove a package or a service whose other consumers were not established
change firewall rules in a way that can lock out the current access path
expose a database, cache or admin interface to the public network
disable TLS, or replace a valid certificate with a self-signed one
turn off authentication, widen permissions, or run a service as root to avoid
  a permissions problem
set a framework to development or debug mode on a server
overwrite configuration whose current contents were not read first
install arbitrary software the contract does not require
commit, push, deploy or roll back on someone's behalf
```

The general rule behind the list: **never weaken a control to make a deployment
work.** If the only way past a blocker is to remove a protection, the blocker
stands and the finding says so. A deployment that did not happen is recoverable.

### The six questions

Every non-trivial change, project or server, answers these before it is made.
Where the answer to the last one is "it cannot be", that is itself the reason to
ask a human first.

```
What is changing?      the specific file, setting or package, and its current value
Why?                   the finding id it resolves
What evidence?         the observation that established the finding
What could break?      what else reads this, and what depends on the current value
How is it verified?    the check that will run afterwards, named now
How is it rolled back?  the state to restore, captured before the change
```

### Capture before you change

Rollback is only real if the previous state was recorded. Before replacing
configuration, read it and keep it — in the report or in
`.deployment-compatibility/findings.md`, with secrets redacted:

```
Before   /etc/nginx/sites-available/app  client_max_body_size 1m
After    client_max_body_size 25m   — project accepts 25 MB uploads (src/uploads/limits.ts)
Rollback restore the previous value and reload
```

Some things do not roll back, and saying so is part of the proposal: an applied
destructive migration, a deleted file, a rotated credential, a released
certificate. When rollback is not available, the change stops being a
remediation and becomes a decision for the operator.

## Order

Blockers first, and among them the ones that other rows depend on. Then anything
that risks data. Then the conditions that would otherwise remain in the report.
Then the rest.

Prefer the smallest change that resolves the finding. A version mismatch
resolved by pinning the project's own base image is better than upgrading a
runtime shared by three other services on the same box, and the report should
say why it chose the smaller one.

## After remediating

Re-run the matrix rows the change touched, and say what moved:

```
DC-014  RUNTIME  BLOCKED → FIT
        Dockerfile base node:20-alpine → node:22-alpine
        Verified in an equivalent local container; not yet on app-01.
```

A row does not move on the strength of having edited a file. It moves when
something was checked, and the label says which environment checked it. A
remediation whose verification could not run leaves the row where it was, with
the change recorded and the check named.
