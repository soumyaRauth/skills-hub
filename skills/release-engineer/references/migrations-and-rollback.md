# Migrations and rollback

A rollback redeploys old code. It does not un-migrate a database. So the whole
discipline is keeping the old code able to run against the new schema, for at
least one deploy.

## Expand, deploy, contract

| Phase | Deploy N | What changes | Old code still works? |
| --- | --- | --- | --- |
| Expand | N | Add table, nullable column, column with a default, index, new enum value the old code ignores | Yes — rollback is safe |
| Migrate | N (code) | New code writes both shapes or the new one; backfill runs as a job, in batches | Yes |
| Contract | N+1 or later | Drop the old column, rename, add NOT NULL, remove the enum value | No — never in the same deploy as the code that stops using it |

A rename is add-new, copy, switch reads, then drop-old, over at least two
deploys. Whether a backfill or index is safe at production volume (locks,
batching, time) is `production-guard`'s question; the reach of a dropped column
across raw SQL and reports is `impact-map`'s.

## Where migrations run

- Once per deploy, from one place: a release step in the pipeline or the
  platform's release command, before new code takes traffic.
- Never from every container's startup when more than one instance runs; two
  instances race the same migration.
- A failed migration stops the deploy. The old code keeps running.

## The rollback script

One command, one argument set, no decisions inside:

```bash
#!/usr/bin/env bash
# deploy/rollback.sh <env> [image]
# Redeploys the previous image (or the one given). Never runs down-migrations.
set -euo pipefail
env="$1"
image="${2:-$(ssh "$DEPLOY_USER@$DEPLOY_HOST" cat /srv/app/previous-image)}"
./deploy/deploy.sh "$env" "$image"
./deploy/smoke.sh "$(./deploy/url.sh "$env")/health"
```

Shape for a VPS; on a platform, the rollback is the platform's own mechanism
(`deploy-targets.md`). Down-migrations run only on explicit human request, after
reading what they drop.

## The staging drill (before the first production deploy)

1. Deploy version A to staging; smoke passes.
2. Deploy version B; smoke passes.
3. Run the rollback; smoke passes on A. Confirm the running image is A's digest.
4. Roll forward to B.
5. Record in `.release/rollback.md`:

```
## staging — 2026-09-28
command   ./deploy/rollback.sh staging
from      ghcr.io/acme/shop@sha256:4be1…  → to  ghcr.io/acme/shop@sha256:91d0…
smoke     GET /health → 200 after rollback; 200 after roll-forward
```

Every value in that record is copied from output. If any step could not run,
the drill is not done and production stays blocked (SKILL.md rule 5).

## When a rollback cannot help

- A contract migration already ran: old code breaks on the new schema. Roll
  forward with a fix instead, and say so plainly.
- A secret or config changed alongside the deploy: rolling back code does not
  roll back config. Record config changes in the RELEASE block.
- Data was written in the new shape only: the old code may misread it.

Each is a reason to stop and ask, not to improvise.
