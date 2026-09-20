# Decision records

One file per decision, in `.architecture/decisions/`. Individual files rather
than one growing document, because rewriting an architecture document on every
change is how architecture documentation stops being written.

## Format

```markdown
# D-004 — Asynchronous payment confirmation

**Status**   Accepted · 2026-09-20

**Context**
Checkout charges the provider inside the HTTP request and marks the order paid
from the response. Provider webhooks already arrive twice for about 2% of
charges (OBSERVED — logs/webhooks-2026-09.log).

**Drivers**
- R-03  Payment confirmation must never be lost              STATED
- R-05  Provider webhooks may arrive twice, or late          OBSERVED

**Options**
- **A** Keep it synchronous in the request
- **B** Durable queue plus an idempotent consumer
- **C** Event-sourced payment ledger

**Decision** — B

**Why**
A loses confirmations whenever the browser closes or the process dies mid-call,
which R-03 forbids. C satisfies R-03 as well, and costs a consistency model, a
rebuild path and a versioning discipline that no stated requirement asks for.

**Trade-offs**
One more moving part to run and monitor. Confirmation becomes eventually
consistent, so the UI must show a pending state it does not have today.

**Consequences**
- The order lifecycle gains a `payment_pending` state
- Webhook handling needs an operation identity — provider event id
- Reconciliation for messages that never arrive becomes a real requirement

**Reversibility** — Cheap, while the queue carries only this message type.
Delete the consumer, call the handler inline, remove the pending state.

**Open** — R-07 (reporting staleness tolerance) is still ASSUMED and does not
block this decision.
```

Keep it proportional. A decision about a library is four lines; a decision about
a distribution boundary earns the full shape.

## Statuses

| Status | Meaning |
| --- | --- |
| `Proposed` | Written, not agreed. The normal state during a design session |
| `Accepted` | Agreed and in force |
| `Superseded by D-0NN` | Replaced. The file stays — the reasoning is the record |
| `Rejected` | Considered and declined, with why. Worth keeping; it stops the same option returning next quarter |

Never delete or silently edit an accepted decision. Supersede it. The value of
the record is that it explains why the system is the way it is, and a rewritten
history explains nothing.

## The rule that decides whether this is a decision at all

> **A decision resting on an `ASSUMED` or `UNKNOWN` requirement is not a
> decision.**

When the driver is not `STATED` or `OBSERVED`, there are two honest routes:

**Ask.** Usually correct when the decision is expensive to reverse.

**Record it as provisional**, with the assumption named inside it and the
trigger that would revisit it:

```markdown
**Status**  Proposed — provisional
**Drivers** R-07 reporting tolerates staleness up to a minute   ASSUMED
            breaks: if reporting must be read-after-write, the read replica
            in this decision is wrong and reads return to the primary
**Revisit** when anyone states the reporting freshness requirement
```

What is forbidden is the third route: quietly promoting the assumption to a fact
because it makes the design tidy.

## The reversibility gate

Before committing, ask what undoing this costs.

```
Cheap        a library, a cache layer, an internal module split, most
             framework choices, a naming convention
Expensive    a data model that will be populated, a public API contract, a
             distribution boundary, an external identifier scheme, a vendor
             with data gravity, a security or tenancy boundary
```

For anything in the right column, **summarize and check in before deciding**.
One short paragraph — the direction, the main trade-off, its reversibility, and
a direct question:

> Based on what you've said, I'd keep this as one deployable application with
> enforced module boundaries, PostgreSQL, and a queue for payment confirmation.
> The trade-off is that extracting a service later depends on keeping those
> module boundaries honest, which needs a lint rule and some discipline. It is
> reversible and it fits four engineers and your current scale. Shall I write
> that up as the target?

Not for every detail. For the decisions that will still be true in two years.

Under genuine uncertainty, prefer the reversible option even when it looks
slightly worse — being able to change your mind later is worth more than a
marginal improvement that is permanent.

## Linking decisions to requirements

Every decision names its drivers by id, and every requirement worth having is
the driver of something or is not a requirement. This is what makes the
architecture auditable later: when a requirement changes, the decisions it
drove are findable.

```
R-03  →  D-004 (async confirmation), D-006 (outbox), D-009 (reconciliation job)
```

When R-03 turns out to be wrong, those three are exactly what has to be
revisited. Without the link, nobody knows.

## What not to record

- Decisions nobody made. A pattern that arrived by default is not a decision; if
  it matters, decide it now and record that.
- Implementation detail. Which HTTP client, how a function is named, where a
  file sits. Record what constrains the future.
- Anything secret. Credentials, customer data, internal politics, judgments
  about people.
- A decision restated because the architecture document was rewritten. One
  record per decision, superseded when it changes.
