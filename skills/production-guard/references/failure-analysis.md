# Failure Analysis

The signature phase. Happy-path validation tells you the feature can work;
failure analysis tells you what the product does when reality misbehaves.

Ask, for each significant change: **how does this fail in production?**

## Failure taxonomy

### Input failures

Missing, invalid, malformed, extreme, empty, duplicate. Extreme deserves
attention: the 10,000-item selection, the 500 MB upload, the deeply nested
payload, the unicode name.

### Dependency failures

Database unavailable, external API unavailable, timeout, connection reset,
malformed response, partial data returned, dependency slow rather than down.
Slow is the one most systems handle worst — a hung request holds a connection,
a worker, and a lock.

### Concurrency

Duplicate simultaneous requests, simultaneous updates to the same row, races
between read and write, stale state after a check, concurrent delete-and-update,
lock contention and deadlock.

The classic shape:

```
check("is this allowed?")   →   ...another request runs here...   →   act()
```

Anything between the check and the act is a race. Look for it around uniqueness
checks, balance checks, quota checks, and status guards.

### Retry behavior

User double-clicks. Client library retries on timeout. Load balancer retries.
Queue redelivers. Webhook sender retries on a non-2xx. Each is a duplicate
execution of the same logical operation.

### Partial failure

```
100 records requested
 47 succeed
  1 fails
 52 never attempted
```

Answer four questions:

- Is the operation **atomic**, or partially committed?
- What state remains in the database?
- Is it **recoverable** — can it be safely re-run?
- Is the partial result **visible to the user**, accurately?

An operation that is not atomic is not automatically wrong. An operation whose
partial-failure semantics are undefined always is.

### Recovery

Can the operation be retried safely? Can the user recover unaided? Can an
administrator? Is rollback possible? Does recovery require manual database
work — and if so, is that written down anywhere?

## Idempotency

For payments, orders, provisioning, emails, webhooks, queue jobs, and any
external mutation, answer explicitly: **what happens if this executes twice?**

```
POST /payments
  → request arrives, charge succeeds
  → network times out before the response
  → client retries the same request
  → one payment, or two?
```

Signals that idempotency is handled: an idempotency key accepted from the
client, a unique constraint on a natural key, a state guard that rejects
repeats, or a deduplication window. Absence of all of these on a money path is a
blocker, not a suggestion.

## The failure matrix

```
FAILURE SCENARIO          EXPECTED       ACTUAL      STATUS
────────────────────────────────────────────────────────────────
API timeout               graceful       graceful    PASS       (executed)
Duplicate request         idempotent     duplicate   FAIL       (executed)
DB failure at 50%         rollback       partial     FAIL       (executed)
Unauthorized user         rejected       rejected    PASS       (executed)
Malformed input           validation     —           UNVERIFIED (analyzed)
Worker dies mid-job       resumable      —           UNVERIFIED (analyzed)
```

Fill `ACTUAL` **only** when the scenario was actually exercised. A scenario you
reasoned about has no actual column value and carries `STATUS: UNVERIFIED`.
Reasoning is valuable and belongs in the report; presenting it as an observation
is falsification.

## Asynchronous work

For queues, workers, and scheduled jobs, add: retry policy and backoff,
duplicate execution, dead-letter handling, job timeout, partial processing,
progress visibility, failure visibility.

The question that finds the most real bugs:

> What happens if the worker dies **after** the external side effect but
> **before** marking the job complete?

If the answer is "the job re-runs and the side effect happens again", you have
found a duplicate-charge, duplicate-email, or duplicate-provisioning bug.

## External integrations

Timeouts and their values, retry policy, rate limits, malformed responses,
unavailability, partial failure, duplicate requests, version compatibility.
Assume the third party is unreliable, because it is.
