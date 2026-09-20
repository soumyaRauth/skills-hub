# Options and trade-offs

Generating real alternatives, comparing them on the dimensions that matter here,
and refusing to hide a judgment inside a number.

## Two genuine options, or an explanation

Whenever a decision is not forced, produce at least two options that a competent
engineer could actually defend. A strawman pair is worse than one option,
because it disguises a decision already made as a comparison.

When only one option is viable, say so and say why the others are excluded. That
is shorter, more honest, and more useful than a manufactured comparison:

> There is only one sensible option here. The data is relational, the queries
> join across five entities, and you have transactional invariants — a document
> store would mean reimplementing joins and constraints in application code. The
> real decision is not which database, it is whether reporting runs against the
> same instance, and that one is open.

## Compare on what the requirements make relevant

There is no fixed scoring sheet. The dimensions come from the requirements —
comparing options on "scalability" when nothing about scale is established is
theatre.

Typical dimensions, selected as needed:

```
complexity now            how much there is to build and understand
operational burden        what has to be deployed, monitored, backed up, paged
failure modes             what breaks, how visibly, and what the user sees
consistency              what is guaranteed, and what is eventual
latency                  on the paths that matter
cost                     infrastructure and, more often, people
team capability          whether this team can run it on a bad night
testing                  what becomes easy, what becomes impossible locally
deployment               how many units, and whether they must move together
reversibility            what undoing it costs later
```

## No scores

Never produce a weighted total, a rating out of ten, or a percentage fit. The
repository forbids invented numbers generally, and this is the place they are
most tempting and most misleading: a score launders a judgment into arithmetic,
and the weights were chosen to produce the answer.

```
Never                          Instead
Option A: 8.5/10               Option A costs one more deploy unit and buys
Option B: 7.2/10               independent scaling of the part that is
                               actually hot. Nothing here says it is hot yet
```

A comparison table is fine — one row per dimension, one column per option, words
in the cells. What is forbidden is a total.

## The complexity budget

The mechanism that keeps a design proportionate to its problem.

Every moving part is a permanent cost: another thing to deploy, configure,
monitor, secure, back up, upgrade, and be woken up by at 3 AM. The cost is paid
by whoever operates it, every week, forever. So each one names the requirement
that forces it:

```
Component        Driving requirement                          Grade
Queue + worker   R-03 payment confirmation must not be lost   STATED
Read replica     R-11 reporting must not slow checkout        OBSERVED
Redis cache      —                                            none — removed
Second service   R-09 unknown scale                           UNKNOWN — deferred
Search cluster   R-14 full-text search over 12k rows          STATED, but
                                                              PostgreSQL covers
                                                              it — removed
```

Three outcomes: the component stays because a requirement forces it, it is
removed because nothing does, or it is **deferred** because the requirement that
would force it is unknown. Deferred is not rejected — it is recorded in
`risks.md` with the trigger that would revisit it.

The last row is the most common one. A requirement can be real and still not
justify a component, because something already present satisfies it.

## Patterns need a requirement

Each of these is a legitimate answer to a specific problem and a liability
without one. Before adopting any of them, name the requirement it is the
cheapest answer to.

| Pattern | The requirement that justifies it | Without it |
| --- | --- | --- |
| Microservices | Parts must deploy, scale or fail independently — usually organizational before technical | Distributed monolith: every failure mode of distribution, none of the independence |
| Event-driven | Producers must not know their consumers, or work must outlive the request | Indirection that makes every flow harder to follow |
| CQRS | Read and write loads or shapes genuinely diverge | Two models to keep in sync for one workload |
| Event sourcing | History is the product, or audit demands every transition | A rebuild path and a versioning problem you did not need |
| Message bus | Several consumers per event, or delivery must survive restarts | A queue with extra vocabulary |
| Kubernetes | Real orchestration needs — many services, autoscaling, self-healing | A second system to operate, larger than the first |
| Hexagonal layering | The domain must be testable and swappable against real infrastructure | Ceremony around CRUD |
| Multi-region | Users are far away, or the business requires survival of a region | Consistency problems in exchange for nothing |

The honest version of the recommendation usually sounds like this:

> A modular monolith with enforced module boundaries. You have four engineers,
> one deploy pipeline, and no requirement that any part scale independently.
> Boundaries enforced in code cost a lint rule; boundaries enforced by the
> network cost a distributed system. If the reporting load ever forces it out,
> the module is already the seam.

## Reversibility changes the process, not just the answer

Cheap to reverse: decide, record the assumption, move on. Expensive to reverse:
raise the evidence bar, and check in before committing.

```
Cheap        a library, a cache layer, an internal module split, a naming
             convention, most framework choices
Expensive    a data model that will be populated, a public API contract, a
             distribution boundary, an external identifier scheme, a vendor
             with data gravity, a security or tenancy boundary
```

Under uncertainty, prefer the reversible option even when it is slightly worse
on paper — the option that can be changed later is worth more than the one that
is marginally better and permanent.

## Presenting a comparison

Short, structured, ending in a recommendation with its reason:

```markdown
**Decision:** where order-status writes live.

**A — keep writes at call sites.** No work now. Three modules keep writing the
column; the rule stays implemented twice and the next writer makes it three.

**B — one owning module, others call it.** A day of work. One writer, the rule
in one place, a lint rule keeps it that way. Callers take a function call
instead of a query.

**C — extract an order service.** Two weeks, a network boundary, a deploy unit,
and its failure modes. Buys independent deployment nothing has asked for.

**Recommend B.** R-04 says the cancellation rule must be consistent across the
app, and B is the cheapest thing that makes it structurally true. C solves a
scaling problem you do not have evidence of; the module boundary from B is the
seam it would need anyway, so B is also the first step of C if that changes.

**Trade-off:** reporting gets a function call where it had a query, which is
slightly slower and materially harder to get wrong.
```

Note what that does: it names the requirement that decides it, prices the
options in real units, refuses the fashionable one for a stated reason, and
observes that the recommended option is the first step of the rejected one —
which is what makes it reversible.
