# Knowledge format

The files in `.agents/knowledge/` are the contract. The skill writes them, the
MCP server reads them, and a developer can read them in any editor. A future
hosted hub would store and serve the same files. Keep them plain markdown, with
`## ` headings as section boundaries: the MCP server's search returns whole
sections, so one topic per section is what makes a search hit useful.

## architecture.md

Living document, updated in place. Suggested sections, each kept short:

```markdown
# Architecture

## What this is
One paragraph: what the system does and for whom.

## Run it
Install, run, test, migrate, as the scripts actually define them.

## Layout
| Path | What it is |
| --- | --- |
| `apps/api/` | HTTP API; Express + Postgres |

## How a request flows
The path one representative request takes, naming the modules.

## Configuration
| Variable | Controls |
| --- | --- |
| `QUEUE_URL` | Where jobs are published; unset runs jobs inline |
```

One `## ` section per area, so an incremental run replaces exactly the
sections whose area changed.

## decisions.md

Append-only log, newest last.

```markdown
## 2026-07-08 — Jobs moved from cron to the queue
Why: cron runs overlapped on long nights and double-sent invoices.
Rejected: a lock table (still double-sends when a run crashes mid-batch).
Source: commit 3f2a91c, PR description.
```

`Source:` keeps the entry checkable. A decision the history does not explain is
not invented; it goes to `gotchas.md` as an open question.

## gotchas.md

```markdown
## Deleting a customer does not delete their invoices
The FK is ON DELETE SET NULL on purpose: finance keeps invoices for seven years.
Don't "fix" it with CASCADE.
```

```markdown
## Unclear: why the retry limit is 3
Set in a commit with no message; nothing in the code depends on the value.
```

Remove a gotcha once the code fixes it, and log the fix in `decisions.md`.

## .learn-state.json

```json
{ "last_learned_commit": "<40-char sha>", "updated_at": "2026-07-08" }
```

Committed. One cursor for every clone, so knowledge learned on one machine is
not re-learned on another.
