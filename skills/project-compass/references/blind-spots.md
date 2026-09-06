# Blind spots

A blind spot is not something the developer does not know. Everyone is missing
most things, all the time, and saying so is worthless.

> A blind spot is a **decision, model, or measurement that work in progress
> already depends on, and that nobody has made.**

Both halves are required. "There is no event model" is a fact about the code.
"There is no event model, and the three notification rules added this month each
invented their own trigger semantics" is a blind spot.

## Detectors

Each detector below lists the evidence it requires. Without that evidence, it is
a hunch and it stays in `trajectory.md`.

### Missing authorization model

**Evidence:** three or more permission decisions made at call sites, at least
one of them an exception to another; no central rule; roles growing by addition.

**Closing step:** four questions, answerable in a sentence each — who are the
subjects, what are the resources, which actions exist, and does ownership
outrank role or the reverse? Write the answers down; the code follows.

**Not this** when the project has a policy layer and someone is adding a policy
to it. That is the model working.

### Missing lifecycle

**Evidence:** boolean flags that cannot legally be true together (`isApproved`
and `isCancelled`); "can this still be edited?" asked more than once;
transitions implemented in more than one place; a status column with no
constraint on what may follow what.

**Closing step:** list the states, list the legal transitions, name who may
cause each. Usually fits in ten lines and settles a month of arguments.

**Not this** when the states are already enumerated and someone is adding one.

### Missing idempotency or identity

**Evidence:** repeated fixes for duplicates of different things — requests,
notifications, jobs, rows, charges. Retries added without a dedupe key.

**Closing step:** define what makes an operation *the same operation*, and where
that identity is enforced. Every duplicate bug is the same bug until this
exists.

### Missing measurement

**Evidence:** two or more performance changes with no baseline anywhere; no
timing in logs; a target described in adjectives; a tool chosen before a bottleneck
is named.

**Closing step:** one number. What operation, measured how, currently what, and
acceptable at what. Until that exists, every optimization is a guess with a
deployment attached.

**Not this** when there is a profile, a trace, or a benchmark in the repo and
someone is acting on it.

### Missing workflow definition

**Evidence:** four or more controls added to one screen or entity — search,
filter, sort, saved views, bulk actions, export — with no path defined through
them; navigation that dead-ends; no test exercising a sequence.

**Closing step:** name the person, the task, and the sequence. *"A support agent
opens a ticket, checks the customer's history, and either resolves or escalates
it."* Every control then justifies itself or does not.

### Missing event semantics

**Evidence:** notification or webhook rules added per feature; no shared
definition of what happens, who cares, and what is guaranteed; delivery
retry logic implemented differently in two places.

**Closing step:** enumerate the events the domain actually has, and for each:
who consumes it, at-least-once or at-most-once, and what happens when the
consumer is down.

### Missing domain model

**Evidence:** a concept present in the vocabulary but absent from the model —
"subscription" in twelve files and no subscription entity; the same information
recomputed in three places; database workarounds recurring in one area; a
column named after a special case.

**Closing step:** name the missing concept and where it would live. Do not
refactor first — the model is the decision, the refactor is the consequence.

### Missing business rule

**Evidence:** the same undefined term appearing in three implementations —
"active", "complete", "expired", "eligible"; conditionals accumulating
exceptions; two features answering the same question differently.

**Closing step:** one sentence, written down, owned by a person. See
`decision-debt.md`.

### Missing failure model

**Evidence:** an integration that takes money, sends messages, or holds the
source of truth, with no defined behavior when it is unavailable, slow, or
partially successful. No entry ever tagged reconciliation or failure.

**Closing step:** for each critical dependency: what does the user see, what is
retried, what is reconciled later, and what is lost. This one is worth raising
at Level 2 even at two instances, because the consequence is other people's
money.

### Missing validation

**Evidence:** substantial functionality being built on an assumption about users
that nothing has tested; a sophisticated feature with no user, no request, and
no usage question asked.

**Closing step:** the smallest thing that would tell you — one user asked, one
version shipped and watched, one query against real data. Say it as a question,
because this is the detector most likely to be wrong: the user may know
something you cannot see.

## Prioritizing

Not everything undefined matters. Rank by:

```
Dependency     how much pending work is waiting on it
Impact         what it costs to get wrong
Reversibility  can it be changed later, cheaply?
Frequency      how often does it resurface?
Uncertainty    how far apart are the plausible answers?
```

A decision that three planned features need, is expensive to reverse, and has
resurfaced three times outranks everything else in the file. An undocumented UI
detail ranks nowhere and should not be written down at all.

Never present a score. Present the order, and the reason the first one is first.

## Reporting

Three to five, maximum, and only when asked or when one clears the bar in
`intervention-rules.md`. Each carries: what was observed, what it costs, what
closes it.

```markdown
## Authorization rule is undefined

**Observed:** six permission decisions across three modules; two are exceptions
to a third (src/api/adjustments.ts:112, :118, src/api/reports.ts:44).

**Costs:** the bulk-edit work asked for on Tuesday needs a rule that does not
exist. It will invent a seventh case, and one of the existing six is already
unreachable.

**Closes with:** four questions — subjects, resources, actions, and whether
ownership outranks role. An afternoon, and it unblocks the next three features.
```

## Never do this

- Do not generate a checklist of things a project "should have". Observability,
  rate limiting, an ADR process and a design system are not blind spots because
  they are absent.
- Do not manufacture a blind spot to have something to say. An empty
  `blind-spots.md` is a good outcome.
- Do not report the same one twice.
- Do not report one the user has dismissed.
- Do not report a blind spot in the same breath as refusing to do the work.
