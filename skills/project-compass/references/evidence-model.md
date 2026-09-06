# Evidence model

A recommendation is only worth as much as the weakest claim under it. This file
is how claims get priced.

## The four labels

| Label | Means | Written with |
| --- | --- | --- |
| `OBSERVED` | Read directly, and re-readable | The location — file, path, commit, or "the user said so" |
| `INFERRED` | Concluded from observations. Carries **High** or **Low** | The observations it rests on, and what would overturn it |
| `ASSUMED` | Believed to make progress, unverified | What breaks if it is wrong |
| `UNKNOWN` | Established as not established | What would settle it |

Everything in `project.md` carries one. So does every claim inside an
intervention. A statement with no label is a statement nobody can check.

```
Payments are provider-authorized, never stored              OBSERVED
    src/payments/provider.ts; no PAN column in schema.sql

Users belong to exactly one organization                    INFERRED (High)
    from: users.organization_id NOT NULL, no membership table, every repo
          query filters on it
    overturned by: a membership table, or one user in two orgs

The reporting screen is for finance, not operations         INFERRED (Low)
    from: currency formatting and fiscal-quarter grouping only
    overturned by: asking anyone

Refund windows are 30 days                                  ASSUMED
    from: one hardcoded constant, no policy doc
    breaks: any refund logic built on it, and the customer emails after

Why orders are soft-deleted rather than cancelled           UNKNOWN
    settled by: git log on the migration, or asking whoever wrote it
```

## Strong versus weak inference

The difference is not how confident you feel. It is how many independent
observations point the same way, and whether anything points elsewhere.

**High** requires: two or more independent sources agreeing, no contradicting
evidence found, and a stated way to be wrong. Schema plus query patterns plus UI
is three. Three files in the same module is one.

**Low** is everything else, and Low inferences do not carry interventions. They
can be offered as a question — *"is this screen for finance?"* — which is often
the cheapest evidence available.

## Source hierarchy

```
1  What the user explicitly said about intent, users, or priorities
2  Documentation written to be read: README, ADRs, specs, RFCs
3  The database schema and its migrations
4  The code, and especially the code that runs on every request
5  Git history and commit messages
6  Configuration, environment, deployment manifests
7  The shape of the UI, and the vocabulary in it
8  Tests — what they assert, and conspicuously what they do not
9  Inference across all of the above
```

Two rules on top of the ordering:

**Never let inference overrule a stated fact.** If the user says the project is
an internal tool, it is an internal tool, even if it has grown organizations and
billing. That mismatch is a *finding* — see `drift-detection.md` — not a licence
to overwrite what they told you.

**Never let a document overrule the schema.** READMEs describe intentions,
sometimes from two years ago. Schemas describe what the system actually holds.
When they disagree, record the disagreement — a stale README is itself evidence
about how the project runs.

## Absence of evidence

Absence counts only when the observation could have shown presence.

```
Counts     No authorization module anywhere in src/, and role checks appear
           inline in 6 handlers — searched for the usual names and found none
Counts     No test asserts what happens to an approved application on edit
Not        "I didn't see any documentation" — where did you look?
Not        "There's probably no monitoring" — probably is not a label
```

If a search would settle it, run the search before writing the claim.

## Staleness

Recorded evidence rots. Code moves, schemas change, decisions get reversed in a
commit nobody wrote down.

Every claim in `project.md` carries the date it was last verified. Before
building an intervention on a recorded claim, **re-check it** — one grep, one
file read. It costs seconds and it prevents the failure that ends the skill's
credibility permanently: confidently citing something that stopped being true
three weeks ago.

When a re-check fails, correct the file first, then reconsider whether the
intervention still stands. Often it does not, and the silent correction is the
whole contribution.

## What is never evidence

- A pattern's popularity elsewhere. "Most SaaS products have an audit log" says
  nothing about this one.
- What the code *could* be used for. Capability is not intent.
- Your own prior recommendation. A conclusion cannot cite itself as support.
- The user's frustration. "Why is this so complicated?" is a signal worth
  reading, not proof of any particular cause.
- Anything from a previous session that has not been re-verified and is load
  bearing.

## Anti-fabrication

The failure mode this exists to prevent is inventing project context, because it
is invisible to the reader — a fabricated business goal reads exactly like a
discovered one.

Never invent: the objective, the users, market demand, deadlines, team size,
usage numbers, customer feedback, past incidents, or a decision that "was
probably made". Never write a plausible history into `trajectory.md` to make a
pattern reach three instances.

When the objective is undocumented, write:

```
Project objective    UNKNOWN
    Not stated in README, docs, or any commit message. The code is evidently
    for [what it does], but why it exists has not been recorded.
```

Then say so out loud the first time it matters. On a project with no written
objective, that sentence is frequently the most useful output of the session.
