# Drift detection

Drift is implementation activity becoming disconnected from any coherent
objective. It is not the same as moving fast, changing your mind, working on
several things, or having an untidy repository.

The whole difficulty is that drift and focused work produce nearly identical
evidence. This file is about telling them apart, and the default answer is
**not drift**.

## What drift is not

| Looks like drift | Actually is |
| --- | --- |
| Unrelated tasks in sequence | A backlog being worked through |
| Many changes to one module | A feature being built |
| Long runs of small fixes | A migration, or a stabilization phase |
| Three approaches tried and thrown away | A spike, working correctly |
| Scope expanding | A decision to expand scope — ask before diagnosing |
| Lots of questions | Someone learning the codebase |
| An unfinished feature abandoned | A priority change, which is management, not drift |

Before calling anything drift, name the ordinary explanation and say why it is
ruled out. If it cannot be ruled out, there is nothing to report.

## Signals that actually indicate drift

None is sufficient alone. Two, with the ordinary explanations excluded, is the
minimum.

**Escalating mechanism.** Each change is a bigger structural response to the
same unmeasured problem: timeout raised → retry → queue → cache → new service.
The escalation itself is the evidence — nobody escalates on a problem they have
measured.

**Corrective recursion.** Fixes for variants of one failure, in different
places, without the shared cause being named: duplicate request, duplicate
notification, duplicate job, duplicate row.

**Radial accumulation.** Features fanning out from one screen or entity with no
path through them. Search, filter, sort, saved views, bulk actions, export — each
reasonable, and none of them a workflow.

**Foundation inversion.** Building on top of something undefined: notifications
without an event model, permissions UI without an authorization rule, reports
without report definitions, offline sync without a conflict rule.

**Oscillation.** A decision made, reversed, remade, then made configurable.
Configurability as the resolution of an argument is drift's clearest tell —
"make it a setting" is what a project does when it cannot decide.

**Objective silence.** No entry in weeks touches the thing the project says it
is for, while the periphery grows. Only usable when the project *has* a stated
objective; otherwise this is an `UNKNOWN`, not a signal.

## Product drift

A distinct kind, worth separating: the *product* changes without anyone
noticing. An internal tool acquires accounts, then organizations, then
permissions, then billing, then notifications, then an audit log.

Each step is reasonable. The sum is a different product with different
obligations — support, migrations, uptime, data protection — that nobody has
signed up for.

Report it as an observation, never a criticism, and never as a request to stop:

> This is not behaving like the internal tool it started as. In the last two
> months it has grown accounts, orgs, roles and an audit trail — that is the
> shape of a multi-tenant product, with the support and upgrade obligations that
> come with it. Worth deciding whether that is the plan before the next layer.

The failure mode here is moralizing. State it once, and drop it.

## Architectural drift

Components accumulating faster than requirements: API, worker, queue, event bus,
cache, second service. Complexity is not the finding — plenty of systems need
all of that.

The question is whether each piece is meeting a stated requirement. Ask it about
the specific components:

> The queue and the cache both went in to make the report endpoint faster. Do we
> know which one helped, or how much? If not, the third thing we add will be a
> guess too.

Never oppose complexity generically, and never recommend removing a component
whose purpose is `UNKNOWN` — find out what it was for first. See the knowledge
debt section of `project-model.md`.

## Scope expansion

Expanding scope is not drift. *Unnoticed* expansion is.

The distinction is whether anyone decided. So do not diagnose it — ask:

> We started on X; the last eight changes are mostly Y. Did the goal change, or
> did we end up here?

Both answers are fine, and either one is worth writing into `decisions.md`. That
single question is often the entire intervention.

## Exploration

The `EXPLORATORY` state exists so this file does not fire on deliberate work.

Set it on any explicit signal — "let's try", "prototype", "spike", "benchmark
these", "throwaway", "I want to see what it looks like" — or on the artifacts of
exploration: parallel implementations, branches named after approaches,
benchmark harnesses, code with a stated expiry.

While `EXPLORATORY` is set for an area, drift detection is off there. Help
explore: make the comparison sharper, name what would decide it, keep the
throwaway throwaway.

It ends when the user says so, or when exploration output starts being
*extended* rather than replaced — the moment a prototype gets its second feature
it has become the implementation. That transition is worth exactly one line:

> Heads up — the spike from last week is now getting features. If it is the
> real thing now, it is worth saying so, because it was built to be thrown away.

## Reporting drift

Once, with evidence, humbly, and with the exit ramp open. The words matter:

```
Never   "You are drifting."          Never   "You seem lost."
Never   "You don't understand..."    Never   "This is a mess."
```

```markdown
### I think we may be circling something

Over the last three weeks: [instances, with dates and locations].

Each one is reasonable on its own. Together they look like [the shared cause],
which nothing has defined yet.

If that is deliberate, say so and I will drop it. If not, I would
[the smaller step] before the next one.
```

The last paragraph is not politeness. The user has context that is not in the
repository, and roughly a third of the time it makes the finding wrong.
