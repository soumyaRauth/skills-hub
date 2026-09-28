# Example — a milestone completes, staging deploys, production asks

Illustrative. `config.yml` has `merge: auto`, `deploy_staging: auto`,
`deploy_production: ask`, and a Trello tracker reached through an MCP server.
This is the project's first production deploy.

## Request

> Keep going until M1 is done.

## The last ticket

```
[3/5] T-008 Waitlist when a class is full — done · VERIFIED · PR #17 merged · tracker in sync
```

Every M1 ticket is now `done` or `dropped`. The milestone is complete.

## The gate

The lead loads `production-guard` and passes it the M1 PRs (#12–#17) and each
ticket's ProofBuild line. Its verdict, quoted:

```
🟠 CONDITIONAL SHIP — 1 condition
   Booking confirmation email has no retry when the provider times out
```

The lead does not soften, restate or argue with it.

## Staging

`deploy_staging: auto`. `release-engineer` deploys and runs its smoke check:

```
staging  https://staging.example.test · smoke ok (4/4)
```

## Before production

This is the first production deploy, and `observability-baseline` engages on
its own: there is no `docs/runbook.md` and no error alerting. It adds error
reporting and a health check alert, recorded in the runbook. That work goes
through ProofBuild like any other change, on its own branch
(`t/T-009-production-signal`, a ticket the planner created at the lead's
`HANDOFF → delivery-planner`).

```
[4/5] T-009 Production signal — done · VERIFIED · PR #18 merged · tracker in sync
```

## Production asks

`deploy_production: ask`, and Production Guard's condition is still open. The
run stops.

```
RUN 2026-09-28 16:40 · milestone M1 · 4 of 5 tickets · status stopped
T-007  Member profile             done         VERIFIED · PR #16 merged
T-008  Waitlist                   done         VERIFIED · PR #17 merged
M1     production-guard           —            CONDITIONAL SHIP — no retry on confirmation email
M1     staging                    —            release-engineer: staging smoke ok
T-009  Production signal          done         VERIFIED · PR #18 merged
Tracker  Trello · in sync
Next     production deploy of M1 · waits for your answer

STOPPED  autonomy: deploy_production is ask · 1 approval, 1 condition

1. Production Guard's condition: the confirmation email is not retried on a
   provider timeout.  [fix it first (new ticket)]  [accept and deploy]
2. Deploy M1 to production?  [yes]  [not yet]
```

## Reply

> 1 fix it first, 2 yes after that.

The planner creates T-010; the lead builds it (`VERIFIED`), merges, asks
Production Guard again (`🟢 SHIP`), and `release-engineer` promotes to
production on the session's yes. The ledger records the answer under
Decisions.

## What it did not do

- Did not deploy production on the strength of `CONDITIONAL SHIP` alone, or on
  `deploy_staging: auto`.
- Did not decide the observability work was unnecessary; that skill decided.
- Did not count the gate and the staging deploy against the ticket budget.
