# Example — an idea, taken to a decided architecture

Illustrative. The product is invented; the shape of the session is the point.

---

**Request:**

> I want to build a SaaS platform for managing factories.

---

## What this is not

A capable agent answers this immediately: multi-tenant, microservices for
ingestion and reporting, Kafka, a time-series database, Kubernetes. Well
presented, internally consistent, and chosen before anything was known about
factories, users, scale or the team.

Nothing in that answer is wrong. Nothing in it is *earned*.

## Phase 1 — Is this architectural?

Yes, and there is no system yet, so the mode is `DISCOVER`. There is nothing to
reconstruct and nothing to read — every requirement will have to be `STATED`.

## Phase 3 — The first block

Four questions, each with its reason, because a question whose purpose is
visible gets a better answer.

> 1. **Who opens this every day — operators on the factory floor, or managers
>    reading reports?** It decides whether this is an offline-tolerant system
>    with a sync model, or a dashboard over a database. Those are different
>    products.
> 2. **When a machine reports a fault, does someone need to see it within
>    seconds, or is a few minutes acceptable?** Seconds makes real-time
>    transport a requirement. Minutes makes it an expense.
> 3. **Is each customer's factory data isolated by contract or regulation, or
>    are these one company's factories?** Tenancy is cheap now and expensive to
>    retrofit.
> 4. **You said "manage factories" — is the machine data coming from equipment
>    automatically, or are people entering it?** An ingestion pipeline and a
>    CRUD application share almost nothing.

Not asked yet: language, cloud provider, database. None of them can be decided
before the four above, and asking now would signal that the answers do not
matter.

## The answers

> Managers and shift supervisors, on laptops and tablets, in the office. Faults
> within a minute or two is fine — nobody is standing at the machine watching
> this. Separate companies, so yes, isolated. Data comes from operators typing
> it in at shift end, plus a CSV from the maintenance system nightly. Maybe
> equipment integration later. Two developers. Eventually thousands of
> factories, hopefully.

## Phase 3 continued — the aspiration trap

> **"Eventually thousands of factories" — committed, or hoped for?**
>
> It changes the answer by roughly an order of magnitude of cost, and designing
> for the hope usually costs more than adding it later.

> *Hoped for. Realistically we have three customers lined up, maybe thirty
> factories between them.*

That single exchange is the most valuable thing in the session. It is the
difference between a distributed ingestion platform and an application.

## Requirements

```
R-01  Users are office staff on laptops and tablets            STATED
R-02  Fault visibility within ~1 minute is acceptable          STATED
R-03  Customer data must be isolated between companies         STATED
R-04  Data arrives by manual entry plus a nightly CSV import   STATED
R-05  Committed scale — 3 customers, ~30 factories             STATED
R-06  Team is two developers                                   STATED
R-07  Equipment integration is possible, not committed         STATED
R-08  Uptime expectations                                      UNKNOWN
      would settle it: does a shift stop if this is down for an hour?
R-09  Regulatory retention on maintenance records              UNKNOWN
      blocks: data lifecycle, not the overall shape
```

## Phase 5 — Options, and the complexity budget

R-02 removes real-time transport. R-04 removes streaming ingestion — a nightly
CSV is a scheduled job. R-05 and R-06 remove nearly everything else.

```
Component            Driving requirement                    Grade
Web application      R-01                                   STATED
PostgreSQL           R-03, R-04 relational, transactional   STATED
Background job       R-04 nightly import must survive a      STATED
                     failed run and be re-runnable
Kafka                —                                      none — removed
Time-series database —                                      none — removed
Separate services    R-07, not committed                     UNKNOWN — deferred
Kubernetes           —                                      none — removed
```

Four of the seven components in the reflex answer had no requirement behind
them.

## Phase 6 — The decision, and the check-in

The genuinely open decision is tenancy, because it is the expensive one to
reverse (rule 7).

> R-03 says data must be isolated. Three ways to do that, and they differ mostly
> in what they cost later:
>
> - **Row-level** — one database, `company_id` on every table, every query
>   filtered. Cheapest now. The risk is a forgotten filter, which is a data
>   breach rather than a bug.
> - **Schema per customer** — stronger isolation, migrations run per schema.
>   Fine at 30 customers, painful at 3,000.
> - **Database per customer** — strongest, and two developers should not be
>   operating 30 databases.
>
> I'd take row-level, with the filter enforced in one place rather than
> remembered at each call site, and a test that fails if a query reaches the
> database without it. At your committed scale it is the right trade, and it is
> reversible: schema-per-customer later is a migration, not a rewrite.
>
> The one thing I'd want before committing: if a customer ever contractually
> demands their own database, is that a deal-breaker for you? That is the case
> where this choice is wrong.

That is the reversibility gate — summarize, name the trade-off, ask the one
question that would change the answer.

## The result

```markdown
# D-001 — Row-level tenancy with enforced scoping

Status    Accepted · 2026-09-20
Drivers   R-03 customer isolation                     STATED
          R-05 committed scale ~30 factories          STATED
          R-06 two developers                         STATED
Options   A row-level · B schema per customer · C database per customer
Chosen    A, with scoping enforced centrally rather than per query
Why       B and C buy isolation this scale does not need and add operational
          work two people would carry forever
Trade-off A missing filter is a cross-tenant leak, so the enforcement point
          has to be structural — not a convention
Reverses  Migration to B is mechanical while the schema is shared. Recheck if
          a customer contractually requires their own database
Open      R-08 uptime is unknown and does not block this
```

Target: one deployable application, PostgreSQL, a scheduled import job, tenancy
enforced in the data-access layer. Written to `.architecture/`, with R-08 and
R-09 in `risks.md`.

## What this run did not do

- **Did not answer in the first reply.** The four questions changed the
  architecture by roughly an order of magnitude of cost.
- **Did not treat "eventually thousands" as a requirement.** One question
  turned it from a design driver into a note.
- **Did not recommend a single pattern by name for its own sake.** Every
  component names the requirement forcing it, and four were removed for having
  none.
- **Did not claim the design is scalable, clean or future-proof.** It fits the
  stated requirements, and the record says what would make it wrong.
- **Did not ask about languages, clouds or frameworks.** None of those could
  change anything yet.
