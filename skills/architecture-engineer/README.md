# Architecture Engineer

An Agent Skill for the work that happens before the code, and for the work of
finding out what the code actually became:

> **The architecture is not the first answer. It is what is left after the
> reasoning.**

```bash
npx skills add soumyaRauth/skills-hub --skill architecture-engineer
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill architecture-engineer --agent claude-code --copy
```

---

## Why it exists

Ask a capable agent to design a system and you get an architecture in the first
reply. It is usually well-presented, internally consistent, and assembled from
patterns rather than from anything about your problem — because nothing about
your problem had been established yet.

That is the failure this skill is built to prevent. Not *bad* architecture:
**unearned** architecture, which looks identical to the earned kind and costs
years to undo.

So the deliverable is a chain, and every link carries where it came from:

```
what is actually required   →  what the system really is today
        ↓                              ↓
   the options that fit        the gap between them
        ↓                              ↓
   the trade-offs             →  a decision, recorded, with what reverses it
        ↓
   the target, the migration, and evidence the result matches
```

## The rule that does the most work

Requirements are graded by how they were established — `STATED`, `OBSERVED`,
`INFERRED`, `ASSUMED`, `UNKNOWN` — and the grade travels into every decision
built on it. Then:

> **A decision resting on an `ASSUMED` or `UNKNOWN` requirement is not a
> decision. It is an open question with a leading candidate.**

That is what stops a design session from quietly becoming a guess with a
diagram. If the architecture hinges on how much staleness reporting tolerates,
and nobody knows, that is not a detail to resolve later — it is the thing
blocking the decision, and it gets asked.

Two more constraints follow from the same instinct:

- **Reversibility sets the discovery threshold.** Cheap to undo? Decide and move
  on. Expensive — a populated data model, a public contract, a distribution
  boundary, a vendor commitment — and the bar rises, with a check-in before
  committing.
- **Every moving part names the requirement that forces it.** A queue, a cache,
  a second datastore, another service: each is a permanent operational cost. A
  component that cannot name its driving requirement comes out of the design.
  This is the anti-cargo-cult rule, made checkable.

## Declared architecture vs implemented architecture

For an existing system, the most useful sentence is usually the gap between what
the codebase claims and what it does:

```
Declared                          Implemented
domain/ application/              domain/ imports the ORM in 14 files
infrastructure/
"service layer"                   two controllers write to the table directly
"orders owns orders"              billing and reporting both write order_status
"events"                          one publisher, no subscriber, since March
```

A `services/` directory is not a service architecture. A `domain/` directory is
not a domain model. A class called `Repository` proves nothing. Architecture is
read from dependency direction, data ownership, call paths and transaction
boundaries — directory names are a hypothesis at best.

## Five modes

| Mode | When | Writes |
| --- | --- | --- |
| **DISCOVER** | No system yet, or the deciding requirements are unknown | `.architecture/` only |
| **DESIGN** | Enough is known to choose — options, trade-offs, decision, target | `.architecture/` only |
| **REVIEW** | A system exists — reconstruct what it really is, name the drift | `.architecture/` only |
| **MIGRATE** | A target is agreed — a staged path, implemented when asked | The project, against a plan |
| **VERIFY** | Something was built — does the structure match what was decided? | Nothing, unless asked |

## What a session looks like

```
You:    I want to build a SaaS platform for managing factories.

Agent:  Before I design anything, four questions that would each change the
        shape of it:

        1. Who opens this every day — plant operators on the floor, or managers
           reading reports? It decides whether this is an offline-tolerant
           system or a dashboard.
        2. When a machine reports a fault, does anyone need to see it within
           seconds, or is a few minutes fine? This decides whether real-time
           transport is a requirement or an expense.
        3. Is factory data isolated per customer by contract or regulation, or
           is it one company's factories? Tenancy is expensive to add later.
        4. You mentioned "eventually thousands of factories" — is that a
           committed plan or a hope? I'll design for what is committed and
           leave room for the rest.
```

Four questions, each with its reason, each capable of changing the answer. Not a
questionnaire, and not an architecture.

Four worked examples: [greenfield discovery](examples/greenfield-discovery.md) ·
[a codebase whose real architecture differs from its declared one](examples/existing-review.md) ·
[monolith or services, answered without fashion](examples/monolith-or-services.md) ·
[the request that sounds architectural and isn't](examples/quiet-feature.md)

## When it activates

It activates when architectural work is **invited**: design a system, structure
an application, review or rework an architecture, choose between architectural
options, decide where a responsibility belongs, plan a migration. It also picks
up work handed over by another skill, and resumes when `.architecture/` exists.

It stays quiet for ordinary features, bug fixes, refactors inside one module,
renames, formatting and dependency bumps. **A large or messy codebase is not an
invitation.** Noticing that a project has quietly become a system nobody
designed is [Project Compass](../project-compass/README.md)'s job, and it holds
the interruption budget for it. This skill does not volunteer an architecture
review because the code looks bad. See [Activation](SKILL.md#activation).

## What it will not do

- **Lead with an architecture.** Patterns are answers to requirements; naming
  the pattern before the requirement has the reasoning backwards.
- **Invent a requirement.** Scale figures, latency targets, availability
  expectations and compliance obligations are stated, observed, or unknown.
- **Recommend microservices, event sourcing, CQRS, a message bus or Kubernetes
  by default.** Each needs a requirement it is the cheapest answer to.
- **Score options out of ten.** Weighted totals invent precision nothing here
  supports. Trade-offs are stated in words.
- **Call an architecture best, clean, correct or future-proof.** The defensible
  claim is that an option fits these requirements better than the alternatives,
  and here is what it costs.
- **Modify your code while designing.** `DISCOVER`, `DESIGN` and `REVIEW` write
  nothing but `.architecture/`. Only `MIGRATE` changes the project, only when
  you ask, and only against a plan.
- **Propose a rewrite** where an evolutionary path exists — and every transition
  state has to ship.

## Where it fits

[Project Compass](../project-compass/README.md) notices that eight reasonable
features have become an authorization model nobody defined, and names the
decision. This skill is what you call when you want that decision answered:

```
project-compass     "there is no authorization model, and three features
                     already disagree"
        ↓
architecture-engineer  the questions, the options, the decision, the target,
                       the migration
        ↓
impact-map          what moving that boundary actually touches
        ↓
proof-driven-dev    the behavior that must survive the move
        ↓
production-guard    is the result safe to ship
```

[Standards Compass](../standards-compass/README.md) supplies security, privacy
and retention obligations as *requirements* rather than opinions.
[Engineering Investigator](../engineering-investigator/README.md) establishes a
cause before anyone redesigns around a guess.
[Deployment Compatibility Engineer](../deployment-compatibility/README.md) says
whether the target environment can actually run the result.

## State

`.architecture/` holds the typed requirements, the reconstructed current state,
the decided target, one ADR per decision, the risks and open questions, and
where the migration actually stands. It exists so the second session does not
re-derive the system or re-ask you the same questions.

ADRs are individual files on purpose: rewriting one large architecture document
on every change is how architecture documentation dies. The repository always
outranks the state, and a recorded claim is re-verified before anything is built
on it.

## Limitations

- It reasons from the repository and from what you tell it. Business strategy,
  budget, politics, team skill and roadmap are things you supply — it will ask,
  and it will not invent them.
- Scale and performance requirements cannot be derived from source code. Absent
  a number, they stay unknown and the design says so rather than guessing.
- A reconstructed architecture is as good as the evidence. Dynamic dispatch,
  runtime configuration and generated code hide real edges, and an absent
  finding is not proof of absence.
- Fitness checks verify structure, not behavior. That a domain module no longer
  imports the ORM says nothing about whether the feature still works — that is
  `proof-driven-dev`'s question.
- Architecture is contextual. A recommendation here is fitted to the
  requirements and constraints as established, and it changes when those change.

## License

MIT — see [`LICENSE`](../../LICENSE) at the repository root.
