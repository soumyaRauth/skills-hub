# Symptom Normalization

The report you receive is a compression of someone else's experience. "The app
is slow" is what remains after a user's frustration, a support agent's summary,
and a manager's relay have each dropped detail. Normalization recovers the shape
of the missing detail before any theorizing starts.

## The investigation statement

Rewrite the report into fixed slots. Every slot gets a value **and** a type.

```
Symptom     what is observably wrong, in behavior terms
Who         which users, accounts, tenants, roles
Where       which environment, region, network, device, browser
What        which operation, endpoint, page, job
Since       when it started, and how that was determined
Frequency   always / intermittent / a rate / a burst
Impact      what it costs — failed orders, wrong data, waiting users
```

Example:

```
Report:  "Users are reporting that the application is very slow."

Symptom     Perceived slowness on unspecified operations   FACT (report)
Who         "users" — count and identity unknown           UNKNOWN
Where       Unknown; production assumed                    ASSUMPTION
What        Unknown                                        UNKNOWN
Since       Unknown                                        UNKNOWN
Frequency   Unknown                                         UNKNOWN
Impact      Unknown; no failure reported, only slowness    PARTIAL
```

Seven slots, six unknown. That picture is the point: it shows that generating
hypotheses now would be generating them from nothing, and it shows exactly which
question is worth asking.

## Symptom words are not diagnoses

Translate the vocabulary of the report into observable behavior. Each of these
maps to several distinct phenomena, and the mapping is the first fork in the
investigation:

| Report says | Could be |
| --- | --- |
| slow | server processing, data transfer, rendering, a blocking dependency, a queue backlog, perceived slowness from a spinner that never resolves |
| broken | error response, silent no-op, wrong result, timeout, a UI that never updates |
| randomly / intermittently | a subset of users, a subset of records, a subset of instances, a time window, a race, a retry that usually succeeds |
| wrong data | stale cache, replication lag, a mis-scoped query, a partial write, a client-side merge |
| down | unreachable, erroring, slow past patience, or one feature failing on an otherwise healthy site |

Never carry the reporter's word forward as if it were a measurement. "Slow"
becomes a number, or it stays `UNKNOWN`.

## Fill slots from what you can reach — before asking

Most slots are answerable without the user. Look, in roughly this order,
stopping when the slot is filled:

```bash
git log --oneline -20                       # what changed recently
git log --since="7 days ago" --stat         # and how much of it
ls logs/ log/ var/log/ storage/logs/ 2>/dev/null
rg -n "error|exception|timeout" logs/ | tail -50
```

- **Since** — deploy history, changelog, migration timestamps, the last commits
  touching the implicated area.
- **What** — the routes, jobs, or components that plausibly own the reported
  behavior; the error strings the report's wording resembles.
- **Where** — environment configuration, feature flags, region settings, CDN
  configuration.
- **Frequency** — retry counts, error-rate patterns, log density over time.
- **Who** — tenancy model, role checks, and per-account configuration that could
  make one account behave differently.

Anything the repository answers is not a question for the user. A questionnaire
sent before looking is how an investigation loses its first hour and its
credibility.

## The minimal ask

When information genuinely blocks progress, ask for the smallest set that
discriminates — normally at most three items, phrased concretely.

Bad:

> Can you tell me which users are affected, what browsers they use, what times
> this occurs, whether it happens on mobile, what their network conditions are,
> whether they use a VPN, and which pages are slow?

Good:

> Three things would let me narrow this quickly:
> 1. One affected account and roughly when it last happened.
> 2. One account that is *not* affected, if you know of one.
> 3. Whether it happens on every page or one particular action.

The second item is the one people forget to ask for and the one that eliminates
the most. A working comparison case is worth more than three more descriptions
of the failure.

Ask once. Investigate what you can while you wait. When an answer arrives, write
it into the slot with its source (`FACT (user)`), and re-derive scope before
continuing.

## Re-normalizing

Normalization is not a one-time gate. Re-run it when:

- an experiment shows the symptom is not what the report described — the "slow
  checkout" is one slow *step* in checkout;
- the scope narrows sharply, e.g. from "users" to "one tenant";
- every hypothesis is disproven, which usually means the symptom statement was
  wrong rather than the system being inexplicable.

Update `incident.md` in place and note what changed, so the ledger's earlier
eliminations can be re-read against the corrected symptom. A hypothesis
disproven against the *old* symptom statement may need to be reopened — and that
is one of the few legitimate reasons to reopen one.
