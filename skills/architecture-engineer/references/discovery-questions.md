# Discovery questions

The questions are the work. An architecture produced without them is a pattern
applied to a stranger's problem.

## The one test every question must pass

> **Which decision does this answer change, and how?**

If nothing changes, the question is curiosity and it costs the user attention
they will not give back. Before asking anything, name the decision it unblocks.

```
Earns its place   "Must a manager see a fault within seconds, or is a few
                  minutes fine?" → decides whether real-time transport is a
                  requirement or an expense
Does not          "What is your tech stack preference?" → decides nothing
                  until the requirements are known
Does not          "Do users belong to one organization?" → the schema says so;
                  read it
```

## Order by impact, not by category

Ask what changes the *shape* first. Ask what tunes it later, or never.

| Order | What it decides |
| --- | --- |
| 1 | What the system is for, and which workflows must not break |
| 2 | What must be immediately consistent, and what may settle later |
| 3 | What must never be lost |
| 4 | Committed scale, and the shape of the load |
| 5 | Integrations, and which of them you control |
| 6 | Where it runs, and who operates it |
| 7 | Non-negotiable constraints — regulatory, contractual, organizational |
| 8 | Team size, skills and on-call reality |

Rows 2 and 3 are the ones most often skipped and most often decisive. They
separate a single transactional database from a design with queues, outbox
tables and reconciliation.

## Batch size

Three to six questions, each with the reason it is being asked. Then stop and
listen.

A visible reason produces a better answer, because the user can correct the
premise rather than answer the literal question:

```
Weak    "What is your expected scale?"
Better  "You mentioned thousands of factories — is that committed or hoped
        for? I will design for what is committed, because designing for the
        hope usually costs more than adding it later."
```

Thirty questions at once is an intake form, and it gets intake-form answers.

## The aspiration trap

The single most expensive misreading in architecture work.

```
"eventually maybe 500,000 users"      aspiration
"we have 400,000 users today"         fact
"the contract requires 500,000 by Q3" commitment
```

Those three sentences produce three different systems and three different costs.
Always establish which one you have. A number mentioned in passing is `ASSUMED`
at best, and rule 3 forbids building a decision on it.

The same applies to *"it has to be really fast"*, *"we can never go down"*, and
*"it needs to be secure"*. Each is a feeling until someone attaches a number, a
workflow, or a consequence to it.

## Do not ask what the repository answers

For an existing system, most factual questions are already answered in the code
and asking them is how credibility is lost in the first minute.

```
Read it                          Ask it
Do users belong to one org?      Should a user ever belong to two?
Which tables exist?              Which of these is the source of truth?
Is there a queue?                Is the queue operationally mandatory, or
                                 incidental and removable?
What does the API return?        Who consumes it that you do not control?
How many services deploy?        Do they have to deploy independently, or is
                                 that accidental?
```

The pattern: **read the facts, ask about intent, authority and the future.** The
right-hand column is also where the architecture actually gets decided.

## Follow the system, not a checklist

Once the domain is known, the questions come from it. Ask only the sets the
system actually contains.

### Payments and money

Which system is authoritative for a payment's state · what happens if the
provider is unreachable when a customer pays · can the same payment arrive twice
(it can) and what makes two requests the same operation · who may refund, and
does a refund change the order's state · is reconciliation manual or automated ·
must a charge and its local record be atomic, and what happens when they are not.

### Organizations and tenancy

Is isolation a contract or a convenience · can anything cross tenants — support
staff, shared catalogs, aggregate reporting · does a user belong to one
organization or several · who may change who belongs · is data partitioned by
row, schema or database, and would a customer ever demand their own · what does
deleting an organization mean.

### Files and uploads

Who owns the bytes, and where they live · does a file survive a redeploy · who
may read one, and is that checked on download or only on listing · is processing
synchronous or deferred · size and type limits, and what enforces them · what
happens to files when the record referencing them is deleted · retention.

### AI and model calls

Which provider, and is that a commitment · what latency is acceptable and what
happens when it is exceeded · what data leaves the system, and is that
permitted · what happens when the model is unavailable or returns nonsense · is
output rendered as trusted content · are prompts and versions managed · what
does a bad answer cost.

### Real-time and collaboration

Must two users see the same thing at the same moment, or is a delay acceptable ·
what is the fan-out, and to how many · does ordering matter · what happens on
reconnect, and is missed state replayed · is presence required · is the
connection count a scaling constraint.

### Reporting and analytics

Can reports tolerate staleness, and how much · are they read by humans or
systems · do they run against the transactional store, and does that already
hurt · what is the largest result anyone will ask for · is historical data
immutable.

### Background work

What must complete even if the user closes the browser · what may be retried,
and is retrying safe · what must run exactly once, and what enforces that · what
happens when a job fails permanently · does order matter between jobs · what
happens to in-flight work during a deploy.

### Integrations

Who owns each side of the contract · what is the failure behavior when the
partner is down — queue, reject, degrade · are webhooks verified, and can they
arrive out of order · who is notified when an integration silently stops.

## Conflicting requirements

When requirements compete, do not resolve it silently. Name the conflict, show
the trade-off, and ask which one wins.

```
You have asked for strongly consistent data across regions, sub-100 ms reads
everywhere, and minimal infrastructure cost. Any two of those are achievable
together; all three are not, at any budget.

  Consistency + low latency  → replicate everywhere, pay for it
  Consistency + low cost     → one region, users far away see higher latency
  Low latency + low cost     → cached reads, and some are briefly stale

Which of the three matters least? That answer decides the data architecture.
```

This is the most valuable thing a design session produces, and it only appears
if the conflict is stated rather than averaged away.

## Knowing when to stop

Stop when the remaining unknowns cannot change the decision in front of you.
Record them in `risks.md` with what they block, and proceed.

```
Enough      the deciding requirements are STATED or OBSERVED
Not enough  the leading option depends on an ASSUMED requirement — ask
Too much    asking about the retention policy before deciding whether this is
            one service or three
```

An architecture that waits for perfect information never ships, and one that
asks nothing designs for a system nobody has.
