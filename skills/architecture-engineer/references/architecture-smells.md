# Architecture smells

A catalog of what to look for, each entry with the evidence it requires before
it may be said and the consequence that makes it worth saying.

Two rules govern the whole file:

- **Evidence before naming.** Every entry below has an evidence column. Without
  it the finding is a style opinion with an official-sounding label.
- **Consequence or silence.** A smell that costs nothing here is a fact about
  software, not a finding. State what it makes expensive, in terms of work that
  exists or has been asked for.

Report the three or four that are actually costing something. A list of fifteen
gets skimmed and nothing changes.

## Boundaries

| Smell | Evidence required | Consequence |
| --- | --- | --- |
| **No owner for an entity** | Every writer of the table listed, in two or more modules | Nobody can change the entity's rules safely; invariants live in whichever writer remembered them |
| **Dependency inversion violated** | Import statements from the inner layer to the outer one, counted | The layering is aspirational. Infrastructure cannot be changed or tested independently |
| **Cycle between modules** | The import path both ways | They are one module. Any boundary claim about them is false |
| **God module** | Its size, and how many modules import it | Every change touches it; it cannot be reasoned about or replaced |
| **Shared internals** | Imports reaching past a module's public surface | The boundary exists in the directory tree and nowhere else |
| **Boundary with no test crossing it** | Absence of any test exercising the seam | The team does not rely on it, which is why it drifts |

## Business logic

| Smell | Evidence required | Consequence |
| --- | --- | --- |
| **Rule implemented twice** | Both locations, and where they disagree | Changing it means finding both. Nothing fails if one is missed |
| **Rules in controllers** | The rule, in a handler, not reachable except by HTTP | Not testable without the transport, and not reusable by a job |
| **Rules in the UI** | The client-side computation, and the absence of a server check | The rule is advisory. A direct API call bypasses it |
| **Persistence shaping the domain** | Domain code branching on ORM or query concerns | The database schema is now the model, and changing it changes business code |

## Data

| Smell | Evidence required | Consequence |
| --- | --- | --- |
| **Two authorities for one fact** | Both writers, and the field they disagree about | The system has no answer to "what is true"; reconciliation becomes a permanent job |
| **Database as an integration bus** | Two deploy units on one database, writing the same tables | Coupled deploys and no contract. Tighter than the API they avoided |
| **Transaction not matching the business operation** | The transaction boundary, and the write outside it | Partial states are reachable and nothing detects them |
| **External call inside a transaction** | The call site inside the transaction block | A rollback undoes the local record and not the external effect |
| **Cache treated as authoritative** | A read path with no fallback to the source | Stale or evicted data becomes wrong answers, silently |
| **Derived data stored without a rebuild path** | The denormalized field, and no recomputation anywhere | It drifts, and nothing can correct it |

## Distribution and asynchrony

| Smell | Evidence required | Consequence |
| --- | --- | --- |
| **Distributed monolith** | Services that must deploy together, or share a database | Every cost of distribution, none of the independence |
| **Synchronous dependency chain** | The call path across three or more services | Availability multiplies downward; the slowest link sets the latency |
| **Retry without idempotency** | The retry, and the absence of an operation identity | Duplicate effects under exactly the conditions retries exist for |
| **No timeout** | A client constructed without one | One slow dependency exhausts the pool and takes the caller down |
| **Event with no consumer** | The publisher, and no subscriber | Dead mechanism. Someone will assume it works |
| **Event ownership unclear** | Two publishers of the same event | Consumers cannot rely on its meaning |
| **Queue used for work that must be immediate** | Something waiting on the result | Latency and failure modes bought for nothing |

## Scale and reliability

| Smell | Evidence required | Consequence |
| --- | --- | --- |
| **Unbounded work** | A query or loop with no limit, over data that grows | Fine until it is not, and the failure arrives at the worst time |
| **N+1 across a boundary** | The loop and the per-item call | Cost scales with data, and worse across a network |
| **Single point of failure** | The dependency every path needs, with no degradation | One failure is a full outage |
| **No graceful degradation** | A hard dependency on something optional | A non-essential outage becomes a total one |
| **Startup order dependency** | A service failing permanently if a dependency is not up | Restarts require choreography nobody documented |

## Security boundaries

| Smell | Evidence required | Consequence |
| --- | --- | --- |
| **Authorization at call sites** | The count of sites, and at least two that disagree | The effective policy is whatever they sum to. Nobody can state it |
| **Trust assumed inside the boundary** | An internal endpoint with no identity check | Any foothold inherits full access |
| **Identity conflated with permission** | Authentication middleware that also decides access | Roles cannot change without touching the auth path |

When a finding lands in authorization, personal data, retention or a regulated
domain, it is a standards question and belongs to its owner:

```
HANDOFF → standards-compass: order exports include customer addresses and
          nothing states a retention period [A-021]
```

## Operations

| Smell | Evidence required | Consequence |
| --- | --- | --- |
| **No failure ownership** | A failure path that logs and returns success | Nobody learns it happened |
| **Infrastructure coupled to application logic** | Deployment concerns inside business code | Neither can change independently |
| **Architecture that cannot roll back** | A migration without a reverse, or a dual-deploy requirement | The escape hatch does not exist when it is needed |

## Two anti-smells

Worth stating, because a review that only finds problems is read as an attack
and distrusted:

- **A monolith is not a smell.** It is the correct architecture for most
  systems. A monolith with enforced module boundaries is a better system than
  most service estates.
- **Duplication is not always coupling's opposite.** Two similar implementations
  that serve genuinely different rules are correct, and merging them creates a
  shared abstraction that fits neither.

## Naming a smell without moralizing

```
Bad     "The codebase violates separation of concerns and lacks proper
         architectural boundaries."
Good    "Order rules exist in OrderController.php:88 and OrderService.php:42,
         and they disagree above 15 minutes. Whichever one a change misses
         stays wrong, and the tests pass either way."
```

The second names locations, states the disagreement, and says what it costs. It
is also the version that can be acted on this afternoon.
