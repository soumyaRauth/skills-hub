# Reconstructing the current architecture

What the system *is*, established from evidence — as opposed to what its
directory layout, its README, or its original design document claims.

## The core distinction

```
Declared architecture      what the structure, the names and the docs assert
Implemented architecture   what the dependencies, the data writes and the call
                           paths actually do
```

The gap between them is usually the most useful finding available, because every
decision made on the declared version has been quietly wrong.

```
Declared                          Implemented
domain/ application/              domain/ imports the ORM in 14 files
infrastructure/
"service layer"                   two controllers write to the table directly
"orders owns orders"              billing and reporting both write order_status
"events"                          one publisher, no subscriber since March
"microservices"                   three deploy units sharing one database
"repository pattern"              repositories returning ORM query builders
                                  that callers extend
```

**A directory name is a hypothesis.** Test it before repeating it back.

## Read order

Cheapest and most decisive first. Stop when the question in front of you is
answered — a full reconstruction is rarely what a request needs.

### 1. Deployment units

How many things start, and what starts them. This is the one architectural fact
that cannot be faked by structure: a repository organized into "services" that
ships as one process is a modular monolith, whatever the folders say.

Read process definitions, container and compose files, CI deploy jobs, and
whatever the runtime supervises.

### 2. Data ownership

The most important and least documented property. For each significant table or
collection, find **every writer**.

```
grep for the table name across the repository, not just in the module that
"owns" it — then check raw SQL, migrations, jobs, reports and seed scripts
```

One writer is ownership. Several writers in different modules is shared mutable
state across a boundary, and it is the finding that most often explains why
changes are expensive.

Also establish: who reads it, what enforces its invariants, and whether anything
outside the repository writes to it.

### 3. Dependency direction

Which module imports which, and whether the arrows point the way the declared
architecture claims. A domain layer importing infrastructure is the classic
inversion, and it is visible in one pass over the import statements.

Look for cycles between top-level modules. A cycle means the two modules are one
module with extra steps, and no amount of directory structure changes that.

### 4. Call paths for the main workflows

Follow two or three workflows that matter, entry point to persistence. Not every
path — the ones the business would notice.

What this exposes, reliably: layers that are bypassed, business rules
implemented twice, transactions that do not span what they should, and external
calls made from places that cannot retry.

### 5. Transaction and consistency boundaries

Where transactions begin and end, what happens inside them, and what does not.
Two things worth finding specifically: an external call inside a transaction,
and a write that should be atomic with another and is not.

### 6. What crosses a process boundary

HTTP calls, queue messages, shared tables, shared caches, shared files. Each one
is a real architectural edge with a failure mode, whether or not anyone designed
it.

A shared database between two deploy units is an integration mechanism nobody
declared, and it couples them more tightly than an API would.

### 7. Configuration, authentication and trust

Where identity is established, where authorization decisions are made (one place
or many), what is assumed trusted, and what configuration changes behavior in
ways the structure does not reveal.

### 8. Tests

What the tests actually exercise tells you which boundaries are real. A boundary
with no test crossing it is a boundary the team does not rely on; heavy mocking
at one seam often marks where the real coupling is.

## Evidence discipline

Findings carry the same labels the rest of this skill uses, and a finding
without evidence is an opinion with a number attached.

| | Meaning |
| --- | --- |
| `OBSERVED` | Read directly — a file and line, a schema, a config value |
| `INFERRED` | Concluded from observations, with what would overturn it |
| `ASSUMED` | Taken as true to proceed, with what breaks if wrong |
| `UNKNOWN` | Established as not known, with what would settle it |

```
A-014   Order rules implemented in two places       INFERRED (High)

Evidence    app/Http/Controllers/OrderController.php:88 recomputes the
            cancellation window inline; app/Services/OrderService.php:42 holds
            the other implementation. They disagree above 15 minutes
Consequence Business-rule ownership is ambiguous. Changing the rule means
            finding both, and nothing fails if one is missed
Question    Which is intended to be authoritative?
Direction   One owner for the lifecycle rule; the other becomes a caller
Overturned  by evidence that the controller path is dead
```

Four rules:

1. **Cite locations.** A claim about coupling names the files.
2. **Count before generalizing.** "Business logic is scattered" is a feeling.
   "Order rules appear in three places — two controllers and one service" is a
   finding.
3. **Do not infer intent from structure.** That a `domain/` directory exists
   says someone once intended a domain layer, not that there is one.
4. **Report the gap, not the ideal.** The finding is the distance between what
   this system claims and what it does, not the distance between this system and
   a textbook.

## What the shapes usually mean

Each of these needs its own evidence before it is said out loud.

| Observed | Usually means | Confirm by |
| --- | --- | --- |
| Several modules write one table | No owner for that entity | Listing every writer |
| A module imports infrastructure directly | The layering is aspirational | Counting the imports |
| A rule implemented twice | Ownership was never decided | Diffing the two implementations |
| Deploy units sharing a database | Distribution without isolation | Checking the connection strings |
| A publisher with no subscriber | An abandoned mechanism | Searching for consumers |
| Authorization decided at call sites | No authorization model | Counting the sites |
| One enormous module everything imports | A missing boundary, or a real kernel | Checking whether its parts are used together |
| Queue used for work that must be immediate | A mismatch between mechanism and requirement | Finding what waits on the result |

The middle column is a hypothesis. The right column is what makes it a finding.

## Sizing the report

A reconstruction is only useful if it is read. Lead with the three or four
findings that are actually costing something — expensive changes, ambiguous
ownership, a failure mode nobody handles — and put the rest in `current.md`.

Every finding needs a consequence stated in terms of work that exists or has
been asked for. *"This violates layering"* is a style note. *"Changing the
cancellation window requires finding two implementations, and the test suite
passes if you miss one"* is a finding.

## Recording it

`current.md` is a view of now, rewritten rather than appended to:

```markdown
# Current architecture — observed 2026-09-20

**Shape**        One Laravel app and one Next.js app, deployed separately,
                 sharing one MySQL database                        OBSERVED
**Owns data**    Laravel writes 14 tables; Next.js API routes write 3, two of
                 which Laravel also writes                         OBSERVED
**Boundaries**   No module boundary enforced; app/Services exists and is
                 bypassed by 6 of 19 controllers                   OBSERVED
**Async**        One queue, used for mail only. Payment confirmation is
                 synchronous in the request                        OBSERVED
**Auth**         Laravel session for the app; the Next.js side re-implements
                 token checks in middleware                        OBSERVED
**Unknown**      Whether the Next.js writes are deliberate or historical
```

That last line matters as much as the others. It is the question the next
session starts from instead of re-deriving the whole system.
