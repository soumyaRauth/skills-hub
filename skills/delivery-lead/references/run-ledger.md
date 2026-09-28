# The run ledger

One file per day in `.delivery/runs/`, named `YYYY-MM-DD.md`. A second run on
the same day appends a new `RUN` block to that day's file. This directory is the
only part of `.delivery/` the lead writes.

The ledger has two readers: the human, who wants to know what happened in a
screen, and the next session, which has to pick up where this one stopped. It
is written as the run goes, not reconstructed at the end.

## Shape

```
RUN 2026-09-28 14:02 · milestone M1 · 4 of 5 tickets · status stopped
T-003  Class list page            done         VERIFIED · PR #12 merged
T-004  Book a class               done         VERIFIED · PR #13 merged
T-005  Cancel a booking           blocked      REVIEW REQUIRED — refund rule undecided (question below)
T-006  Staging deploy             done         release-engineer: staging smoke ok
Tracker  Trello · in sync
Next     T-007 (ready) · answer the T-005 question to unblock it

Decisions
- (none this run)

Question
1. T-005 — refund when a booking is cancelled <24h before class? [full] [none] [credit]
```

The header's `status` is one of `running`, `stopped`, `finished` (milestone
shipped or nothing left). A crashed run is the one whose header still says
`running`.

## Ticket line

```
<id>  <title, padded>  <state>  <evidence>
```

| State | Written when | Evidence column |
| --- | --- | --- |
| `started` | the ticket is picked | the branch name |
| `in_review` | the PR is open and the merge waits for `ask` | ProofBuild status · PR link |
| `done` | proven and merged | ProofBuild status · PR merged |
| `blocked` | proof did not reach `VERIFIED`, review failed twice, or a dependency is missing | the owning skill's status and the one-line reason |
| `skipped` | the human said to skip it in this session | who said so |

Evidence is copied: `VERIFIED` is what ProofBuild printed, `PR #13` is the
number the forge returned. A skill that ran inline is marked `INLINE`
(`production-guard INLINE: …`).

## Tracker line

`Tracker  <type> · in sync` only when every move of this run was read back from
the tracker. Otherwise `out of sync — <n> moves pending, reconciled next run`,
or `local` for `tracker: local`. The line reports what `delivery-planner`
returned; the lead never checks or writes the tracker itself.

## Resume algorithm

A new session asked to continue:

1. Open the newest ledger. Find the last `RUN` block.
2. Header says `stopped` or `finished` → a new run; answers to its question are
   applied first (through the planner).
3. Header says `running` → the session crashed. Append
   `Resumed <date time> in a new session` under it and set it to `stopped`.
   Start a new `RUN` block that lists the unfinished ticket first.
4. For each ticket line still `started`:
   - read its status through the planner (the tracker may have moved — a human
     may have finished or dropped it; the tracker wins);
   - if still `in_progress`, check out its branch. Uncommitted changes on it are
     the crashed session's work: keep them, and run ProofBuild from its contract
     (`.proofbuild/contract.yml` if present, else from the ticket's acceptance
     criteria). Nothing before the crash counts as evidence;
   - if the branch does not exist, start the ticket over from step 4 of the loop.
5. For each ticket `in_review`: find the PR; if merged, move to `done`; if open
   and authorized, merge; else it joins the question.

A ledger that disagrees with git or the tracker is wrong; git and the tracker
win, and the new block says what was corrected.
