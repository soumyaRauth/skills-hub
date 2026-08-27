# Example — Resuming a case

A second session, days later, with a workspace on disk. The job is to continue
the case, not to reopen it.

---

**Request:**

> Continue the investigation.

---

## Read the state first

```bash
ls .agent-investigation/
# incident.md  hypotheses.md  evidence.md  experiments.md
```

`incident.md`:

```
Symptom     Order confirmation emails arrive 20–60 minutes late
Who         All tenants, ~15% of orders                       (E2)
Since       2026-08-20, gradual, not a step change            (E3)
Frequency   Intermittent — most orders are fine               (E2)
Capabilities  repo, git, worker log (logs/worker-*.log), Redis CLI on staging
              Not available: production Redis, provider dashboard
Status      Leading: H3 (queue backlog). Confidence Medium.
Next        Establish whether the delay is queue wait or job runtime.
```

`hypotheses.md`:

```
H1  Email provider is slow to deliver          Disproven — E5: provider accepted
                                               at send time; our own send
                                               timestamp is already late
H2  Retry loop delaying sends                  Disproven — E6: 94% of delayed
                                               jobs succeeded on first attempt
H3  Queue backlog                              Investigating · Medium
                                               Kill: queue wait is short and the
                                               time is inside the job
H4  Slow job runtime (PDF attachment)          Investigating · Low
                                               Kill: job duration is short and
                                               the wait is before the job starts
H5  Scheduler/cron misconfiguration            Blocked — no production scheduler
                                               access
```

`experiments.md`: two experiments, both recorded with their outcomes.

## What resuming means

Four things happen before any new work:

1. **Reconstruct** — symptom, scope, capabilities, live hypotheses (H3, H4), dead
   ones (H1, H2), blocked ones (H5), the open question from `Next`.
2. **Check freshness** — has anything changed since?

   ```bash
   git log --since="2026-08-26" --oneline     # 3 commits, none touching workers
   ls -la logs/                                # worker log now covers 08-27, 08-28
   ```

   No fix was deployed; the symptom is presumably still live. Two more days of
   worker log exist — new evidence, same case.
3. **Honor the eliminations.** H1 and H2 stay dead. Nothing is re-run to "make
   sure", because the evidence that killed them is recorded and still stands.
4. **Take the open question.** `Next` is still the right question: queue wait, or
   job runtime? Nothing since invalidates it.

What does *not* happen: re-normalizing the symptom, re-reading the codebase from
scratch, re-listing hypotheses that were disproven on 08-26, or asking the user
to re-describe the problem.

## Continue: the open question

```
Experiment 3 — is the delay before the job or inside it?

Method     For 200 delayed jobs in logs/worker-2026-08-27.log, compute
           enqueued→started (wait) and started→finished (runtime); compare
           against 200 on-time jobs.
Predicts   H3 → wait dominates for delayed jobs, runtime comparable
           H4 → runtime dominates, wait comparable

Observed   E7  FACT  Delayed jobs: wait p50 31 min · runtime p50 2.4 s
           E8  FACT  On-time jobs: wait p50 1.1 s · runtime p50 2.2 s
Eliminates H4 disproven — runtime is identical for both groups.
           H3 supported: the time is spent waiting to start.
```

One experiment, one elimination, and the leading hypothesis now has direct
evidence. But "the queue is backed up" is a restatement of the symptom, not a
cause. The ledger gets a new child hypothesis rather than a conclusion:

```
H6  Worker concurrency insufficient for the arrival rate
    Kill: workers are idle during the backlog, or concurrency exceeds arrival
H7  A subset of jobs blocks the workers (one slow job type starving the queue)
    Kill: no long-running jobs in the log during backlog windows
H8  Workers are restarting or dying, losing capacity
    Kill: no restarts or crashes in the worker log during backlog windows
```

```
E9   FACT  Backlogs begin at 09:00, 13:00, and 17:00 on both days
E10  FACT  A `daily-report` job type runs at those times: 41 jobs, runtime
           p50 4.9 min each, on the same queue as transactional email
E11  FACT  Worker concurrency is 4 (workers/index.ts:12); during backlog
           windows all 4 are inside `daily-report` jobs
E12  FACT  No worker restarts or crashes in the log (kills H8)
```

H7 supported with a mechanism, H8 disproven, H6 reframed: capacity is not
generally insufficient — it is being consumed by long jobs sharing one queue
with time-sensitive ones.

## Cause

```
Cause       Report jobs (~5 min each) share a single 4-worker queue with
            transactional email; three times a day they occupy every worker and
            confirmation emails wait behind them
Confidence  HIGHLY LIKELY

Chain       delay is queue wait, not runtime (E7, E8)
            → backlogs start at three fixed times daily (E9)
            → those times match the report job schedule (E10)
            → all four workers are inside report jobs during the windows (E11)
            → no restarts or capacity loss (E12)

Would prove it wrong: a backlog window with no report jobs running, or delayed
emails outside the three windows. Neither appears in two days of log.
```

Not `CONFIRMED` — that would take a controlled run with the report job on a
separate queue, which is a staging experiment, not a production one. It is
proposed as the verification step.

## The answer

```markdown
## Result

Confirmation emails are late because they wait behind daily report jobs — both
run on the same queue, and the report jobs occupy all four workers for several
minutes at a time.

**Cause:** Long-running report jobs sharing one worker queue with transactional
email
**Confidence:** High

**Why:** For delayed emails the time is spent waiting to start (31 min median),
not sending (2.4 s, identical to on-time emails), and the backlogs begin exactly
at the three times the report jobs run, when all four workers are inside them.

**Action:** Move report jobs to their own queue, or give transactional email a
dedicated worker. Verifying on staging — running the report schedule with the
queues split and confirming email wait stays under a second — would settle it
before the change ships.

### Client response

"We found why some order confirmation emails were arriving late: they were
queued behind large daily reports that run three times a day, which held up the
emails behind them for up to an hour. The emails themselves were being sent and
delivered correctly once they started. We're separating the two so that
confirmations always go out immediately."
```

## What this example demonstrates

- The workspace was read before anything else, and the answer continues the case
  rather than restarting it.
- Disproven hypotheses (H1, H2) were not re-tested; blocked ones (H5) stayed
  visible.
- Freshness was checked — new log days, no deploys — instead of assuming the old
  evidence still described the system.
- One experiment answered the open question, and the answer produced *new*
  hypotheses rather than being mistaken for a cause: "the queue is backed up" is
  a symptom restated.
- The response reports this session's outcome, not a recap of the whole case.
