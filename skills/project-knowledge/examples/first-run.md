# Example — First run

**Request:**

> Learn this codebase so the next person doesn't have to.

There is no `.agents/knowledge/.learn-state.json`, so this is a first run: a
walk of the structure, not of every file.

## What gets read

The top-level tree, `package.json` scripts, `docker-compose.yml`, the CI
workflow, the README, `.env.example`, the server bootstrap and router, the
migrations directory, and the last fifty commit subjects. Not the tests, not the
lockfile's contents, not every handler.

## What gets written

`architecture.md`:

```markdown
## Run it
`pnpm install`, `pnpm db:up` (Postgres in Docker), `pnpm migrate`, `pnpm dev`.
Tests: `pnpm test` (in-memory Postgres; no database needed).

## How an order flows
POST /orders → `orders/create.ts` → row in `orders` + job on the queue →
`worker/charge.ts` charges the card → provider webhook → `payments/webhooks.ts`
marks the order paid.

## Configuration
| Variable | Controls |
| --- | --- |
| `QUEUE_URL` | Job queue; unset runs jobs inline, which tests rely on |
| `PAYMENT_WEBHOOK_SECRET` | Verifies provider webhooks; must match the provider dashboard |
```

`gotchas.md`:

```markdown
## The in-memory test database rejects some SQL Postgres accepts
Tests run the migrations on an in-memory Postgres. Partial indexes and some
ALTER forms fail there although production accepts them; run the tests after
writing a migration.
```

`decisions.md` gets the decisions the history explains, each with its commit.

`CLAUDE.md` gets one line pointing at `.agents/knowledge/`. The cursor moves to
`HEAD`.

## The report

```
First run at a41c9e2. Wrote architecture.md (run, layout, order flow, config),
gotchas.md (3), decisions.md (4, from commit history). Pointer added to CLAUDE.md.
Nothing committed — commit .agents/knowledge/ and CLAUDE.md with your next change.
```

## What this example demonstrates

The variable table names `PAYMENT_WEBHOOK_SECRET` and what it controls, and never its
value. The first run read the entry points and stopped once an order could be
traced end to end.
