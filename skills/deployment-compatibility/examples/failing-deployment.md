# Example — DIAGNOSE: it starts, then dies

The mode that gets confused with debugging. The discipline is comparison, and
the discipline about *when to stop* matters as much.

---

**Request:**

> The API is fine locally and on staging. On production it serves for about
> forty minutes and then starts returning 502s until we restart it. Been
> happening since Tuesday.

---

## Phase 1 — The symptom, as an observation

```
What        502 from the proxy; the upstream container is not serving
Where       production only. Staging runs the same image and is fine
Since       Tuesday — to be established, not accepted
Frequency   roughly every 40 minutes, recovers on restart
Shape       serves correctly first, then fails. NOT a startup failure
```

The shape is the most valuable line. A process that serves for forty minutes and
dies has a nearly disjoint cause set from one that never starts — configuration,
runtime version and missing dependencies are effectively excluded before
anything is read, because none of them would let it serve at all.

## Phase 2 — Both sides

Same artifact, by digest, on both. So the code is not the variable, and the
question is which environment property differs.

```
                        staging (works)        production (fails)
image digest            sha256:9f3c…            sha256:9f3c…      identical
container memory limit  none                    512 MB            MEASURED
replicas                1                        4                 MEASURED
requests/min            ~15                      ~900              MEASURED
restart policy          unless-stopped           unless-stopped    MEASURED
Node                    v20.11.1                 v20.11.1          MEASURED
```

## Phase 3 — Difference classes

Walked in order, stopped at the one that explains the shape:

| Class | Differs? | Explains "serves, then dies"? |
| --- | --- | --- |
| Configuration | env sets differ by 2 values, both endpoints | No — would fail at startup or on first use |
| Runtime | identical | — |
| Dependencies | identical image | — |
| Permissions | identical | — |
| Network | different proxy, same shape | No — would fail immediately |
| **Resources** | **512 MB limit in production, none in staging** | **Yes** |
| Concurrency | 4 replicas vs 1 | Possibly, and it does not explain a 40-minute cycle by itself |

One command settled it:

```
T-21  MEASURED  journalctl -k --since -3d | grep -i 'out of memory'
                4 entries, the most recent 12 minutes ago:
                "Memory cgroup out of memory: Killed process … node"
```

The kernel killed the process. The container's restart policy brought it back,
which is why it recovers without anyone doing anything and why the symptom
reads as intermittent rather than as a crash.

```
T-22  MEASURED  docker inspect api --format '{{.HostConfig.Memory}}' → 536870912
T-23  MEASURED  docker inspect api --format '{{.RestartCount}}' → 61
```

Sixty-one restarts. Nothing alerted, because the health check passes as soon as
the replacement is up.

## Phase 4 — Confirm the difference is the cause

A difference is a candidate. Three things promote this one:

- The mechanism is direct and the log names it — an OOM kill inside the memory
  cgroup, on this process.
- The restart count matches the symptom's frequency over the window.
- The reverse test is available and safe: staging has no limit. Applying the
  same 512 MB limit to staging and holding it under comparable load would
  reproduce it. That was *proposed*, not run — it changes a shared environment,
  and the evidence above already meets the bar.

What was deliberately not concluded: that the application has a memory leak. The
evidence establishes that it exceeds 512 MB under production load. Whether usage
is stable-but-higher or genuinely growing needs a measurement over time, and
those two have different fixes. The report says so rather than picking the more
interesting one.

## Phase 5 — Classification and close

```
Failure class   RESOURCE
Cause           The production container has a 512 MB memory limit that the
                application exceeds under production load. The kernel kills it;
                the restart policy revives it; the proxy serves 502 in between.
Confidence      High — the kernel log names the process and the cgroup, and the
                restart count matches the symptom's period.
Not established Whether consumption is stable above 512 MB or growing. Different
                fix, and a measurement over a few hours decides it.
```

The contract gained a line it never had:

```
RESOURCES   memory   UNKNOWN → observed: exceeds 512 MB under ~900 req/min
                     source: production OOM kills, 2026-09-16 to 2026-09-20
```

Which is the durable outcome of this session. The matrix row moved from
`UNVERIFIED` to `BLOCKED` against the current limit, and the missing requirement
that let a 512 MB limit be set in the first place is now written down.

## The answer

```markdown
## Result

Production is killing the API for exceeding its container memory limit, and the
restart policy is bringing it straight back — which is why it looks intermittent
rather than like a crash.

**Failure class:** RESOURCE
**Confidence:** High

**Why:** The kernel log has four OOM kills naming this process in its memory
cgroup, most recently 12 minutes ago, and the container has restarted 61 times.
Production limits it to 512 MB; staging, which runs the identical image and does
not fail, has no limit.

**Now:** Raise the production limit, or remove it to match staging, and watch it
for an hour. That stops the 502s today.

**Then, separately:** I cannot tell yet whether the application sits stably above
512 MB or is growing. Those need different fixes, and a few hours of memory
readings decide which. Worth knowing before you pick a number.

**Also worth fixing:** 61 restarts produced no alert, because the health check
passes as soon as the replacement is up. That is why this ran from Tuesday to
Friday before anyone traced it.
```

## Where this stopped

The request could have become an investigation, and it did not need to be one.
One explanation was live after the comparison, and the kernel log named it —
there was nothing competing to discriminate between, so building a hypothesis
ledger would have been ceremony charged to an outage.

Had the comparison produced no difference that explained the shape, or several
that equally did, the handoff was the next step and not a fallback:

```
HANDOFF → engineering-investigator: the production and staging environments
          differ in four ways and none of them explains a 40-minute cycle
```

Equally, had the same failure reproduced on staging under the same limit, the
environment would not have been the variable at all, and the memory behaviour
itself becomes the question — which is that skill's, not this one's.
