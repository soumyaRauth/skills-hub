# Sync: local files and the tracker

The local ticket file is the working copy. The tracker is where people look,
and where they sometimes change things. Sync keeps both telling the same story
without losing anyone's edit and without creating anything twice.

## The `synced` block

Each ticket file records what both sides last agreed on:

```yaml
synced:
  at: 2026-09-28T14:05:00Z      # when local and tracker last matched
  status: in_review              # neutral status at that moment
  title: Customer can reset password by email
```

It is the common ancestor for a three-way comparison. Without it, "the tracker
says In Progress and the file says ready" cannot tell a human's move from a
stale file. Empty `synced` means never synced.

## One write, step by step

1. **Load** the local ticket.
2. **Find** the tracker item:
   - `tracker_ref` set → fetch it directly.
   - empty → search for the marker `[T-004]` (see *Idempotent create*). Found →
     write its id into `tracker_ref`, treat as step 3. Not found → create.
3. **Read** the item: status (column, list, stack, state), title, labels, text,
   last-updated time.
4. **Compare** each field three ways: local, tracker, `synced`.

   | Local vs synced | Tracker vs synced | Action |
   | --- | --- | --- |
   | same | same | nothing to do |
   | changed | same | push the local value |
   | same | changed | **pull**: a human changed it; update the local file |
   | changed | changed, same value | nothing to push; update `synced` |
   | changed | changed, different | **the human wins**: pull, keep the local intent as a comment on the item and a line in the ticket's notes, report it as a conflict |

5. **Write** only the fields still different after pulling. A status move uses
   the tracker's own mechanism (`references/trackers.md`) and is followed by
   its comment (rule 5).
6. **Read back** the item and confirm the write took. A write the read-back does
   not show is a failure, and is reported as one.
7. **Update** `synced` (`at`, `status`, `title`) and save the file.
8. **Report** one line per ticket that changed.

A fixed-moment move that loses to a human edit is not retried and not
overridden. Report it: `T-006: not moved to In Review — a human moved it to
Blocked at 13:52; local updated to blocked. Move it anyway?`

### What counts as the ticket's text

The tracker description is rendered from the local file:

```
<Why>

Acceptance criteria
1. …
2. …

Depends on: T-002 (PROJ-15)
Managed from .delivery/tickets/T-004.md — edits here are pulled back.
```

If the tracker's description changed after `synced.at` and differs from the
rendering of the local file, a human edited it: pull the new text into the local
body (criteria stay numbered; if the human's text breaks the numbering, keep
their text and note the break). The earlier local text survives in git history.

## Idempotent create

- The marker is the title prefix: `[T-004] Customer can reset password by
  email`. Where the tracker supports labels cheaply, also add a `T-004` label;
  the title prefix is still the one relied on.
- **Search by listing, not only by full-text search.** Several trackers'
  search tokenizes or strips brackets. Prefer listing the board, project or
  repository's items (open and closed/archived) and matching the prefix
  exactly. Use the tracker's search only to narrow a large project, then match
  exactly on what it returns.
- Found more than one item with the same marker: do not pick one. Link none,
  report the duplicates, and ask the human which is canonical. The others are
  moved to `dropped`/closed only on their yes, never deleted.
- A create that timed out may still have happened. Before retrying, search
  again.

## Never delete

No tracker item and no local ticket file is deleted. Work that will not happen:
status `dropped`, mapped to the tracker's closest equivalent (closed as *not
planned* on GitHub, archived on Trello or Deck, a `Won't Do`-type status on Jira
or Linear if it exists, else done with a `dropped` label), with a comment saying
why and who decided.

## Out of sync

When the tracker is unreachable, times out, rate-limits past its retry advice,
or rejects the credentials:

1. Make the change in the local file anyway. Leave `synced` untouched, so the
   difference is visible on the next run.
2. Report `tracker: out of sync — <what failed, in one line>` and list the
   ticket under `PENDING`. When `delivery-lead` is running, it records the same
   line in its run ledger; this skill does not write `runs/`.
3. Never report the tracker write as done, and never report a guess about the
   tracker's state as its state.
4. Do not retry in a loop. One retry after the tracker's own `Retry-After` (or
   a short pause when it gives none), then stop and carry on locally.

A credential that was rejected (401/403) is not retried at all: ask the human to
check the env var named in `config.yml`. Never ask them to paste the token.

## Reconciliation

On the next sync (asked for, or at the next fixed moment), before anything
else:

1. For every ticket file, run steps 2–7 above. Local changes made while offline
   push; changes humans made meanwhile pull; both changed → the human wins.
2. For items in the tracker carrying a `[T-nnn]` marker with no local file:
   report them; create the local file only on a yes (someone may have copied a
   card).
3. For items without a marker: ignore them. They are not this skill's.
4. Print the sync report (`SKILL.md`, *Sync*). `PENDING` is `none` only when
   every local change was read back from the tracker.

## Comments

Every status move is followed by a comment, short and factual:

```
[delivery-planner] T-004 → In Review
PR: https://github.com/acme/salon/pull/31
```

```
[delivery-planner] T-004 → Done
✓ VERIFIED · 6/6 requirements · merged in 3f2a91c
```

```
[delivery-planner] T-007 → Blocked
✗ BLOCKED on D1: can a customer cancel inside 24 hours? The spec is silent.
```

No tokens, no internal file paths beyond `.delivery/…`, no stack traces, no
customer data.
