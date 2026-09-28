# Example — a new session resumes after a crash mid-ticket

Illustrative. The previous session ended abruptly (the laptop slept, the
terminal closed) while it was building T-005.

## Request (new session)

> Continue the run.

## What the lead reads

`.delivery/runs/2026-09-28.md`, last block:

```
RUN 2026-09-28 11:02 · milestone M1 · 1 of 5 tickets · status running
T-004  Book a class               done         VERIFIED · PR #13 merged
T-005  Cancel a booking           started      t/T-005-cancel-a-booking
```

The header still says `running`: the session crashed. Through the planner, the
tracker says T-005 is `in_progress`; nobody moved it by hand.

`git status` on `t/T-005-cancel-a-booking`: two modified files, one new test,
nothing committed. `.proofbuild/contract.yml` exists for T-005 with five
requirements.

## What it does

```
⚡ Delivery Lead — resuming a crashed run at T-005
RESUME  T-005 was mid-build · branch kept · 2 files changed, 0 commits · proof starts over
```

1. Appends `Resumed 2026-09-28 13:20 in a new session` to the old block and
   sets its header to `stopped`.
2. Starts a new block with T-005 first.
3. Keeps the uncommitted work, and hands ProofBuild the existing contract.
   ProofBuild runs every requirement again: nothing from before the crash is
   evidence. Result: 4/5 pass; `CANCEL-004` (cancelling twice is a no-op)
   fails. ProofBuild repairs it and reports `VERIFIED`, 5/5.
4. Review, commit `T-005: Cancel a booking`, PR, merge, planner → `done`.

```
[1/5] T-005 Cancel a booking — done · VERIFIED · PR #14 merged · tracker local
```

The run continues with T-006.

## What it did not do

- Did not trust the crashed session's work because tests had been written.
- Did not discard the uncommitted changes, stash them, or reset the branch.
- Did not start a fresh branch and leave the old one behind.
- Did not count T-005 twice: the budget restarted for the new run.
