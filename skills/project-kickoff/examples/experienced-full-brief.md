# Example — everything given up front

Illustrative. The project is invented.

## Repository

Empty apart from `LICENSE`. State: **EMPTY**.

## Request

> New project: an internal tool for our support team to log refund requests and
> have a lead approve or reject them. Users: support agents and two leads. Flow:
> agent logs a request with order number, amount and reason; a lead approves or
> rejects with a note; the agent sees the outcome. No payment integration, the
> refund itself still happens in the payment dashboard. Node 22 + Express +
> Postgres, that's what the team runs. Hosted on our existing internal server.
> Set it up.

## Stage 1 — skipped

Users, workflow, scope, money, stack and where it runs are all stated. No
questions. The reply opens straight into the work:

```
⚡ Project Kickoff · Standards Compass — new internal tool, fully specified; approvals over money
```

## Stage 2 — spec (excerpt)

Nearly every line is `[you said]`. Two are not:

```markdown
- Agents and leads sign in with the company's existing login. [assumed: changes if the tool keeps its own accounts]
- A lead cannot approve a request they logged themselves. [assumed: changes if leads also log requests and self-approve]

## Open decisions
- Is there an amount above which a second approval is needed? — blocks: approval rules
```

The second assumption is flagged, not silently built: separation of duties on
money is a business rule the user owns. Standards Compass engaged because the
tool records approval decisions over money; what it named goes into the
constraints section, in its words.

## Stage 3 — stack

```
STACK   Node 22 · Express · PostgreSQL [you said]
HANDOFF → dependency-guard: express, pg, the test and lint tooling for the scaffold
HANDOFF → deployment-compatibility: must run on the team's internal server; its runtime and Postgres access are unknown
```

No `architecture-engineer`: nothing stated forces a non-default choice.

## Stage 4 — scaffold

One route (`GET /health` returning 200), one test that calls it through the
built-in runner, lint config, `.env.example` with `DATABASE_URL=` and a
comment, `.gitignore` with `.env` and `node_modules/`, a README with the
commands below, and `.github/workflows/ci.yml`.

```
SCAFFOLD PROOF
install   npm ci                                    exit 0
lint      npm run lint                              exit 0
test      node --test                               1 passed
run       npm start → GET /health returned 200      checked, then stopped
CI        .github/workflows/ci.yml written          not run here (no remote yet)
```

No database connection in the scaffold: the health route does not need one,
and the first ticket that stores a refund request adds it with its migration.

## Result

```
READY TO BUILD

Spec      docs/spec.md · 12 [you said] · 2 [assumed] · 1 open decision
Stack     Node 22 · Express · PostgreSQL
Scaffold  install ✓ · lint ✓ · 1/1 tests ✓ · runs ✓ · CI written
Next      HANDOFF → delivery-planner: milestone 1 = walking skeleton deployed
```

No explanations of what `npm ci` does. The developer did not need them.
