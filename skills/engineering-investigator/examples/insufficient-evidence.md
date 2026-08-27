# Example — No telemetry, no invented cause

The most common real environment: a repository, a vague complaint, and no
production access at all. The failure mode is producing a confident answer
anyway.

---

**Report:**

> The app is sometimes slow. Can you figure out why?

---

## Phase 0 — Access, honestly

```bash
git rev-parse --is-inside-work-tree   # true, 1,847 commits
ls -d logs log var/log storage/logs   # nothing
ls -d .env* docker-compose*           # .env.example only
```

```
Available      repository, git history, test suite, configuration templates
Not available  production or staging telemetry, logs, metrics, traces, database,
               the affected environment, any example of a slow request
```

No connected observability tooling in this session. That is a fact about this
environment, and it is written down before anything else — because it sets the
ceiling on every conclusion that follows.

Lane: **STANDARD**, and likely to end without a cause. Workspace: `incident.md`
only.

## Phase 1 — Normalize

```
Symptom     Perceived slowness                    FACT (report)
Who         Unknown                               UNKNOWN
Where       Unknown — production assumed          ASSUMPTION
What        Unknown                               UNKNOWN
Since       Unknown                               UNKNOWN
Frequency   "sometimes" — intermittent            PARTIAL
Impact      Unknown                               UNKNOWN
```

Six unknowns. Generating hypotheses from this would be generating them from
nothing — the shape of the report is itself the first finding.

## Phase 2 — What the repository *can* answer

Not "what is slow" — that is unanswerable here — but "where could intermittent
slowness plausibly originate in this system", which narrows what to ask for.

```
E1  FACT  Express API, PostgreSQL via Prisma, Redis cache, BullMQ workers,
          Stripe and SendGrid integrations
          source: package.json, src/
E2  FACT  Two endpoints run unbounded queries without pagination:
          GET /api/reports/activity (src/routes/reports.ts:44)
          GET /api/customers (src/routes/customers.ts:19)
          — response time scales with row count
E3  FACT  src/services/invoice.ts:88 calls Stripe inside the request path with
          no timeout configured; the default is 80 s
E4  FACT  Redis cache TTL is 60 s for the dashboard aggregate
          (src/services/dashboard.ts:31) — every minute one request rebuilds it
E5  FACT  No APM, no request timing middleware, no slow-query logging anywhere
          in the codebase
E6  FACT  Connection pool size 10 (prisma schema), 4 worker processes
          — 40 connections against a database whose max is not set in this repo
```

Each is a mechanism that *could* produce intermittent slowness. None is evidence
that any of them *did*.

## Phase 3 — Hypotheses, all untestable here

```
H1  Unbounded query on a large table (E2)      Blocked — needs production timing
H2  External call without a timeout (E3)        Blocked — needs error/latency data
H3  Cache stampede at TTL expiry (E4)           Blocked — needs cache metrics
H4  Connection pool contention under load (E6)  Blocked — needs pool metrics
H5  Client-side or network causes               Blocked — needs one measurement
H6  Something not visible in this repository    Blocked
```

Six hypotheses, six `Blocked`. That is not a failed investigation — it is the
accurate state, and it makes the next request specific instead of generic.

The alternative, and the thing this skill exists to prevent, is picking E2 —
which does look suspicious — and reporting "the unbounded query on /api/reports
is causing your slowdown". It might be. Nothing here says it is, and the report
never mentioned reports being slow.

## Phase 4 — The minimal ask

Three items, each of which discriminates between the blocked hypotheses:

1. **One example**: what someone was doing when it was slow, roughly when, and
   how slow — "the dashboard took about 8 seconds around 2pm yesterday".
   Splits H1/H4 (specific operation) from H5 (everything for one person).
2. **Whether it is one user or many.** Splits H5 from everything server-side.
3. **Any response-time or error data that exists** — a hosting dashboard graph,
   a load-balancer log, a screenshot of the browser network tab. Splits transfer
   from processing, which is the fork that decides where to look at all.

Not asked for: browser versions, device models, VPN usage, a list of every slow
page. None of those change what gets investigated next.

## The answer

```markdown
## Result

We cannot reliably determine the cause yet — this environment has the code but no
production telemetry, and nothing here shows what actually happened during a slow
request.

**What we know:** The codebase contains four plausible sources of intermittent
slowness: two endpoints that query without pagination (`/api/reports/activity`,
`/api/customers`), a Stripe call in the request path with no timeout, and a
60-second dashboard cache that one request per minute has to rebuild. There is
no request timing, slow-query logging, or APM in the project, which is why no
one can tell which of these — if any — is involved.

**What is missing:** Any observation of a slow request: a timestamp, an
operation, a duration, or one browser network capture.

**Next step:** Three things would narrow this quickly —
1. One example: what was slow, roughly when, and roughly how slow.
2. Whether it affects one person or many.
3. Any response-time data that already exists — a hosting dashboard graph, a
   load balancer log, or a screenshot of the browser's network tab during a slow
   action.

Separately, adding request timing middleware and slow-query logging would make
the next occurrence answerable in minutes rather than in guesses.
```

No client response section: nobody non-technical is waiting on an answer yet.

## What this example demonstrates

- The access boundary was established first and stated plainly in the answer.
- The repository was used for what it can establish — candidate mechanisms — and
  not for what it cannot: what production did.
- Six hypotheses stayed `Blocked` rather than one being promoted because it
  looked suspicious.
- The ask is three items chosen for discriminating power, not a questionnaire.
- The instrumentation gap is reported as the actionable finding it is.
