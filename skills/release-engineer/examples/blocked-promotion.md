# Example — a production promotion stopped by DO NOT SHIP

The pipeline exists. Staging runs the refunds change, smoke-checked. The
rollback drill is recorded. `delivery-lead` hands over milestone M2:

> Milestone M2 is merged. Release it.

`.delivery/config.yml` says `deploy_production: auto`.

---

## 1. Step 7, row by row

```
tested rollback              ✓ .release/rollback.md, staging, 2026-09-21
staging ran this digest      ✓ .release/deploys.md: sha256:7ac3… smoke 200, 2026-09-28
ship verdict for 5e81d0a     production-guard: 🔴 DO NOT SHIP
```

The third row matches, so the table stops there. Autonomy being `auto` does not
matter: it authorizes a deploy, and it is not a verdict.

## 2. The reply

```
⚡ Release Engineer — M2 promotion requested; stopped at the ship verdict

RELEASE     production · ghcr.io/acme/shop@sha256:7ac3…  (commit 5e81d0a)
BLOCKED     production-guard returned DO NOT SHIP for 5e81d0a
            (its blocker: refund endpoint is not idempotent under retry)
RAN         nothing in production
STAGING     unchanged, still sha256:7ac3…
ROLLBACK    not needed; production still runs sha256:91d0…
```

The blocker is quoted from the Production Guard report, not restated or
softened. This skill says nothing about whether the blocker is serious; that
was decided already.

```
HANDOFF → delivery-planner: M2 release blocked by DO NOT SHIP; T-012 back to in_progress with the blocker
```

## 3. What would unblock it

Either of these, and nothing else:

- The fix lands, `production-guard` runs again on the new commit and returns
  SHIP (or CONDITIONAL SHIP with its conditions shown met), and the new digest
  passes staging first.
- The human, having seen the blocker, says in this session: *deploy
  sha256:7ac3… to production anyway*. The RELEASE block then records
  `OVERRIDE  human, 2026-09-28, against DO NOT SHIP` verbatim.

## What did not happen

- No "it's probably fine, the blocker is edge-case" commentary.
- No rebuild of the commit to "try again".
- No deploy on the strength of `deploy_production: auto`.
- No ticket moved directly; the planner moves it.
