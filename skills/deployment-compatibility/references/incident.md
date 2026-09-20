# DIAGNOSE — it works here and fails there

A deployment that exists and misbehaves. The method is comparison, not
inspection: two environments, one of which works, and the difference between
them is the answer.

## What this mode is, and is not

This mode applies when **the environment is a live candidate** — the same
artifact behaves differently in two places, or a deployment that used to work
stopped when something about the environment changed.

It does not apply to an application defect that was noticed in production. If
the same input fails everywhere, the environment is not the variable, and the
request belongs elsewhere from the start:

```
HANDOFF → engineering-investigator: checkout fails on the server and reproduces
          locally with the same payload — the environment is not the difference
```

Escalate the same way when the comparison produces no difference that explains
the symptom. Competing hypotheses, kill conditions and discriminating
experiments are that skill's machinery, and manufacturing a worse version of it
here helps nobody. This skill supplies the environment evidence and takes the
compatibility question back afterwards.

## Method

### 1. State the symptom as an observation

What fails, where, since when, how often, and what the failure actually looks
like — the exit code, the log line, the HTTP status, the container state. "It
doesn't work on the server" is a report, not a symptom.

Most valuable and most often skipped: **does it fail immediately or after a
while?** A process that dies at startup and one that dies after forty minutes
have almost disjoint cause sets.

### 2. Establish both sides

The working environment is evidence, and it is usually the cheaper one to read.
Gather the same facts from both, so the comparison is like for like — same
commands, same fields.

### 3. Difference classes

Walk these in order of how often they are the answer. Stop when one explains the
symptom; do not collect all of them.

| Class | What differs | How it usually presents |
| --- | --- | --- |
| **Configuration** | An environment variable set in one place and not the other | Fails at startup, or a feature silently takes a default path |
| **Runtime** | Version, architecture, or which binary the process manager resolves | Fails at startup; syntax or exec-format errors |
| **Dependencies** | Installed from a lockfile in one place, resolved fresh in the other; dev dependencies absent | Module not found, at startup or at first use of a path |
| **Build vs runtime** | A value inlined at build time differs from the one set on the server | The app uses a value nobody can find in its environment |
| **Filesystem** | A path that exists locally and not there; relative paths resolved from a different working directory | Not-found errors naming a path that obviously exists |
| **Permissions** | The process runs as a different user; it cannot write where it must | Permission denied, often on a temp or upload directory |
| **Network** | A service reachable on loopback locally and on another host there; egress blocked | Connection refused, or a timeout that takes exactly the client's timeout |
| **DNS** | A name that resolves differently, or an internal name not resolving | Timeouts, or connections to the wrong thing |
| **TLS** | A certificate the client does not trust; hostname mismatch; expiry | Handshake errors; works with verification disabled, which is not a fix |
| **Resources** | Less memory; a container limit; a smaller disk; fewer cores | Killed after a while, not at startup. Check the kernel log for an OOM kill |
| **Process management** | No supervisor, no restart policy, a unit that was never enabled | Works once, gone after a crash or a reboot |
| **Concurrency** | One process locally, several replicas there | Duplicate work, migration races, lock contention, unshared in-memory state |
| **State** | A local database with a schema that the target's does not have | Column or relation does not exist |
| **External services** | Sandbox credentials locally, live ones there; a different endpoint | Auth failures; webhooks that never arrive |

### 4. Confirm the difference is the cause

A difference is a candidate, not a conclusion. Two environments differ in dozens
of ways and most of them are irrelevant. Promote a candidate only when one of
these holds:

```
the symptom reproduces when the difference is introduced into the working side
the symptom disappears when the difference is removed on the failing side
the mechanism is direct and complete — the log line names it
```

The second is usually the cheapest and safest, and it must be reversible before
it is attempted on anything live. When neither is available, say the difference
is the leading candidate and name what would confirm it. Do not promote a
plausible difference to a cause because it was the most interesting one found.

### 5. Classify the failure

Say which kind it is, because it decides what happens next:

```
BUILD            the artifact never got made
STARTUP          the process exits before serving
RUNTIME          it serves, then fails
CONFIGURATION    a value is missing, wrong, or read at the wrong time
DEPENDENCY       a required service or package is absent or unreachable
DATABASE         connectivity, credentials, schema, or permissions
MIGRATION        applied partially, raced between replicas, or not at all
NETWORK          routing, firewall, DNS, or egress
TLS              certificate, chain, hostname, or expiry
PERMISSION       filesystem or process privilege
RESOURCE         memory, disk, inodes, file descriptors, connections
PROCESS          not supervised, not restarted, not enabled at boot
REVERSE_PROXY    routing, headers, limits, timeouts, upstream health
EXTERNAL         a third party the deployment depends on
DATA_PERSISTENCE state that was expected to survive and did not
UNKNOWN          the honest answer when nothing above is established
```

`UNKNOWN` is a legitimate classification. "Deployment failed" is not.

### 6. Close the loop

A fixed deployment is not an assessed one. After the cause is addressed, run the
matrix rows it touched and re-state readiness — the difference that caused this
failure is usually a contract line nobody had written down, and writing it down
is what stops the next environment from repeating it.

## Two patterns worth recognizing on sight

**Works once, then never.** Almost always process management: no restart policy,
a unit that was never enabled, or a container started by hand. The process is
fine; nothing brings it back. Readable without reproducing anything.

**Fine for a while, then dies.** Almost always resources or a leak that a
restart hides: memory growing to a container limit, disk filling with logs,
connections or file descriptors exhausted. The kernel log naming an OOM kill,
or `df -h` against a disk that was fine yesterday, settles it in one command.

Both are environment properties rather than code defects, which is why they land
here rather than with an investigation — and both are invisible to a deployment
that was declared successful because it responded once.
