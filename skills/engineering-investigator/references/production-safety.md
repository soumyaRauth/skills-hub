# Production Safety

An investigation that causes a second incident has failed regardless of what it
found. The default is observation; anything else is a decision with a stated
cost.

## Classify every action

| Class | Definition | Authorization |
| --- | --- | --- |
| `OBSERVE` | Reads state, changes nothing: logs, metrics, traces, `SELECT`, `git`, config reads, response headers, a single request that the system already expects | Proceed |
| `REPRODUCE` | Creates load or state in an environment you were told you may disturb: local, dev, staging, a test tenant | Proceed in that environment; never assume production is one |
| `MUTATE` | Changes production data, configuration, infrastructure, deployments, or traffic | Explicit authorization for that specific action |

Say the class out loud when it is not obvious, especially near a boundary:
querying a production replica is `OBSERVE`; running the same query against the
primary during an incident may not be.

## Never, without being asked for that exact operation

- Delete, update, or backfill production data
- Change production configuration, environment variables, secrets, or flags
- Restart, scale, fail over, or drain services
- Deploy, roll back, or revert on a production system
- Run migrations
- Generate load against a live system
- Disable, weaken, or bypass a security control, rate limit, or auth check
- Modify monitoring, alerting, or logging configuration in production
- Access customer data beyond what the investigation needs, or export it
- Print secrets, tokens, connection strings, or personal data into the workspace,
  the answer, or a log

"The user asked me to investigate" is not authorization for any of these.
Investigation authority is read authority.

## Read-only is usually enough

Most decisive evidence is observable:

```
logs, error rates, traces, request ids       what happened, when, to whom
read-only queries, EXPLAIN plans             cost and shape, without writing
response headers, status endpoints           edge behavior, versions, cache state
deploy history, git, configuration diffs     what changed in the window
one request, made the way a client makes it  end-to-end timing
```

Prefer a replica over a primary, a sampled window over a full scan, and a
bounded query (`LIMIT`, an indexed range, a short time window) over one that
could take a production database's resources. A `SELECT` that table-scans a
large table during an incident is not the harmless action it looks like.

## Asking for a mutation

When the decisive experiment mutates, do not perform it and report afterward.
Present it in four lines and stop:

```
Experiment    Revert a4f1c92 on production and watch checkout p95 for 10 minutes.
Blast radius  All checkout traffic; gift-wrap options disappear from the cart.
Undo          Re-deploy the current release; ~4 minutes.
Expectation   If a4f1c92 is the cause, p95 returns to ~300 ms within one minute
              of the rollout completing. If it does not, H2 is disproven.
```

Stating the expectation first is what makes the mutation an experiment rather
than a hope, and it is what lets the result eliminate something either way.

If authorization is refused or unavailable, say what the missing evidence would
have settled and continue with what remains. Never do a smaller version of the
forbidden thing "just to check".

## Reproduction environments

Reproduce in the least-privileged environment where the symptom can appear:
local, then a test tenant, then staging, then production with authorization.
Before reproducing anywhere shared, consider whether the reproduction itself has
side effects — emails sent, webhooks fired, payments authorized, inventory
reserved, third-party rate limits consumed.

Use test fixtures, sandbox credentials, and idempotency keys where they exist.
If reproduction would charge a real card or notify a real customer, it needs the
same authorization as a mutation.

## Data handling

Investigations touch customer data. Take the least: one affected record rather
than a table, ids rather than contents, aggregates rather than rows. Redact
before writing anything down, and keep customer identifiers out of the workspace
unless they are the evidence — in which case use the id, not the person.

## When the investigation implies urgent action

If the evidence points at ongoing harm — data being corrupted, money moving
wrongly, a security exposure — say so immediately and plainly, at the top of the
answer, with what you observed and what you did not. Recommend the mitigation;
do not perform it. Speed of *telling* is the investigator's contribution;
mutating production is the operator's decision.
