# Example — when the declared architecture and the real one disagree

Illustrative. The repository is invented; the reasoning is the point.

---

**Request:**

> This Laravel + Next.js app has gotten messy. Help me improve the architecture.

---

## Phase 1 — Mode

A system exists, so `REVIEW` first. Designing a target before establishing what
is actually there would be designing for an imagined system.

`.project-compass/` exists and is read first — it records that permission
handling has come up three times since August. That is context, not a finding to
repeat back.

## Phase 4 — Declared versus implemented

The repository declares a familiar shape: `app/Services/`, `app/Domain/`,
`app/Http/Controllers/`, and a Next.js frontend that "just calls the API".

What the evidence shows:

```
Declared                            Implemented
app/Services owns business rules    6 of 19 controllers write models directly
                                    (OBSERVED — grep for ::create and ->save
                                    outside app/Services)
app/Domain is the domain layer      app/Domain/Order.php extends Eloquent and
                                    queries in 4 methods
Next.js calls the Laravel API       3 Next.js route handlers open their own
                                    MySQL connection (lib/db.ts, used by
                                    app/api/orders, /reports, /admin)
One database, one owner             both apps write orders.status
```

The last line is the finding. Everything else is untidy; that one is a system
without an answer to *what is true*.

## Findings

```
A-001   Two applications write order state                     OBSERVED

Evidence    app/Services/OrderService.php:42 sets status on payment;
            web/app/api/orders/route.ts:31 sets it on admin edit, via its own
            connection. No shared validation of legal transitions
Consequence There is no authority for an order's state. A rule added in one
            place is silently absent in the other, and the Next.js path does
            not know which transitions are legal
Question    Which application is intended to own order lifecycle?
Direction   One writer; the other calls it

A-002   Cancellation rule implemented twice                    OBSERVED

Evidence    OrderController.php:88 recomputes the 15-minute window inline;
            OrderService.php:42 holds the other implementation. They disagree
            above 15 minutes — the controller uses >=, the service uses >
Consequence A one-minute window where the two paths give different answers.
            Tests pass either way, because neither exercises the boundary

A-003   Database shared between two deploy units               OBSERVED

Evidence    Both applications' connection config points at the same MySQL;
            two Dockerfiles, two deploy jobs in .github/workflows/deploy.yml
Consequence The two deploy independently and are coupled through the schema —
            tighter coupling than the API boundary they were meant to have.
            A migration must be compatible with both, and nothing enforces it

A-007   Authorization decided at call sites                    INFERRED (High)

Evidence    11 distinct role checks across 7 controllers; two disagree about
            whether a manager may act outside their own region
            (OrderController.php:120 allows, ReportController.php:44 denies)
Consequence Nobody can state the effective policy. It is whatever the call
            sites sum to
HANDOFF → standards-compass: the effective authorization policy cannot be
          stated, over order and refund operations [A-007]
```

Four findings, not fifteen. Each names locations and what it costs.

## What was deliberately not reported

- That `app/Domain/Order.php` extends the ORM. True, and it costs nothing here
  — the team has no requirement to test the domain without a database, and
  removing it is weeks of work buying a property nobody asked for.
- Directory naming, file sizes, missing interfaces. Style, not architecture.
- A recommendation to adopt hexagonal architecture. No requirement asks for it.

## Phase 5 — The question that decides the target

Before options, one question, because everything else depends on it:

> Is the Next.js side supposed to be a frontend that calls the Laravel API, or
> is it a second backend that happens to share the database?
>
> Both are defensible. But right now it is neither deliberately, and that is
> what makes A-001 and A-003 expensive. Everything else I'd propose depends on
> the answer.

> *It was supposed to be a frontend. The direct DB access was a shortcut when
> the API was slow.*

That settles it, and converts a design problem into a migration.

## The target, and the path

```
R-01  Laravel owns order lifecycle and is the only writer      STATED
R-02  Next.js is a frontend; no direct database access         STATED
R-03  The 15-minute cancellation rule has one implementation   STATED
```

Migration, in states that each ship:

```
1  Add the missing API endpoints the three Next.js handlers need.
   Nothing moves yet. Reversible.
2  Point the three handlers at the API; keep lib/db.ts present but unused.
   Validation — no query from web/ reaches MySQL (the connection is removed
   from the container's network policy in staging first).
3  Delete lib/db.ts and its credentials. Rollback window closes here.
4  Collapse the duplicate cancellation rule into OrderService; the controller
   calls it. Add the boundary test that neither implementation has.
5  Add an import rule so no controller writes a model directly.
```

Step 1 was slow API responses, which is why the shortcut existed. That is a
real constraint, and it is worth measuring before step 2 rather than assuming it
has gone away:

```
HANDOFF → engineering-investigator: the direct-DB shortcut was added because
          the API was slow; whether that is still true is unestablished
HANDOFF → impact-map: moving order-status writes behind OrderService — every
          current writer, including reporting SQL [A-001]
```

## What this run did not do

- **Did not propose a rewrite.** The system is not end-of-life and the data
  model is fine.
- **Did not design a target before asking the one question that decides it.**
- **Did not trust the directory names.** `app/Domain` and `app/Services` both
  describe intentions the code does not keep.
- **Did not report every smell it found.** Four findings that cost something,
  and an explicit note of what was left out and why.
- **Did not modify code.** `REVIEW` writes `.architecture/` and nothing else;
  the migration runs when the user asks for it.
