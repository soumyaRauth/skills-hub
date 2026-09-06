# The project state directory

`.project-compass/` is what makes this skill longitudinal instead of a clever
prompt. It is also the thing most likely to rot into bureaucracy, so the rules
are mostly about restraint.

## Files

| File | Holds | Written when |
| --- | --- | --- |
| `project.md` | The model — a page, labeled, dated | Purpose, users, workflows, domain, architecture, or milestone change |
| `trajectory.md` | Dated entries: what changed, which pattern it fed | A request changes what the project is or does |
| `decisions.md` | Settled questions, including dismissed observations | A decision is made, stated, or inferred with High confidence |
| `open-questions.md` | Unresolved decisions currently affecting implementation | A question blocks or distorts work a second time |
| `blind-spots.md` | Patterns that cleared the bar, and what closes them | A pattern clears all four gates |

Create the smallest set that carries the state. A first session usually writes
`project.md` alone. `blind-spots.md` may never exist — that is a healthy
project, not a failed run.

Nothing else belongs in the directory. No `milestones.md` until there are
milestones (they live in `project.md` until there are more than five), no
`architecture.md` duplicating the repo's own docs, no per-session logs.

## Formats

**trajectory.md** — the substrate for every pattern claim. Terse, scannable,
one block per meaningful change:

```markdown
2026-08-19  authz    Managers can approve adjustments in their own warehouse
                     src/api/adjustments.ts:112
                     pattern: role-exception (1st)

2026-08-27  authz    Admins bypass the warehouse restriction
                     src/api/adjustments.ts:118
                     pattern: role-exception (2nd)

2026-09-02  billing  Refunds added; interaction with subscriptions undefined
                     src/billing/refund.ts — see open-questions.md#refund-window

2026-09-04  ---      User said the reporting rewrite is a throwaway spike.
                     State: EXPLORATORY for reporting/ until they say otherwise.
```

The concept tag in the second column is what makes patterns visible; without it
this is a diary. Use the project's own vocabulary where it has one.

**decisions.md** — including the ones made by dismissal:

```markdown
## Adjustments over the threshold need manager approval
Decided by  the existing operational process (stated by the user, 2026-08-19)
Constrains  bulk adjustment, the mobile flow, any auto-approval
Status      Active

## Role exceptions are acceptable for now
Decided by  the user, 2026-09-04, when the pattern was raised
Reason      "Shipping to the first customer this month; will revisit after."
Status      Accepted — do not raise again unless a new exception breaks an
            existing one, or the authorization surface reaches the public API
```

That second entry is the most important file in the directory. It is why the
skill can be lived with.

**open-questions.md** — each with impact, what it blocks, and how it gets
answered. Delete an entry when it is answered; move it to `decisions.md`.

```markdown
## Can an approved adjustment be edited?
Impact      High — permissions, audit trail, reporting totals
Blocks      bulk edit (asked for 2026-09-02), the approval UI
Surfaced    3 times: src/api/adjustments.ts:140, ui/EditPanel.tsx:22, tests gap
Answered by one sentence from whoever owns the process
Default     No, with an explicit reopen action that is itself audited
```

**blind-spots.md** — only what cleared the bar in `intervention-rules.md`, with
the evidence and the closing step. Never a list of things that are undefined.

## Size

Every file has a budget, because a state directory nobody can read is a state
directory nobody reads.

```
project.md         one page
trajectory.md      the last ~40 entries; older ones compress into project.md
decisions.md       unbounded, but each entry four lines
open-questions.md  five or fewer; if there are more, they are not all blocking
blind-spots.md     three or fewer open at a time
```

When `trajectory.md` outgrows its budget, compress: a run of twelve entries on
the same concept becomes one line naming the period, the concept, and the
outcome. Compression is not deletion — the conclusion survives, the instances
collapse.

## Staleness

State is a cache. The repository is the truth.

- Every claim in `project.md` sits under a `Verified` date.
- Re-verify a claim before building an intervention on it. One grep.
- When a re-check fails, fix the file before doing anything else, and consider
  whether the finding survives. Often it does not.
- On resuming after a long gap, check whether the recorded workflows and domain
  concepts still exist before quoting them back at the user.

## What never goes in

- Reasoning, deliberation, or narration. Facts and decisions only.
- Secrets, tokens, connection strings, customer names, personal data.
- Anything invented to make a pattern reach three instances.
- Speculation about people — who is slow, who keeps changing their mind.
- A copy of the code. Point at locations; do not quote files into the state.

## Committing it

Creating the directory is announced in one line, not negotiated. *Committing*
it is the thing to ask about, and it is worth asking: `.project-compass/` is
team knowledge, it survives machines, it is reviewable in a pull request, and a
decision the whole team can see is worth more than one only an agent remembers.

If the team would rather not have it in the repository, keep it local via
`.git/info/exclude` rather than a shared `.gitignore`. If the user does not want
it at all, do not create it — hold the model in the session and stop discussing
the directory.

## Resuming

**If `.project-compass/` exists, read it before answering anything.** Then:

- Honor `decisions.md`, including the dismissals. A closed observation stays
  closed.
- Continue the trajectory; do not restart it.
- Do not re-derive the project model from scratch when a dated one exists —
  verify the parts you are about to use.
- If the recorded state contradicts the repository, the repository wins and the
  file gets corrected in the same breath.
