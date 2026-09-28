# Release Engineer

An Agent Skill that builds the path from a verified change to users, and back:

> **How does a verified change get to users, repeatably, and back out again?**

```bash
npx skills add soumyaRauth/skills-hub --skill release-engineer
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill release-engineer --agent claude-code --copy
```

---

## Why it exists

A change that passes on a laptop is not yet a change users have. Without a
pipeline, every deploy is a hand-typed ritual: a rebuild on the server, a
secret pasted into a file, and no way back when the new version answers 503.
Beginners meet this on their first deploy; experienced developers meet it at
the worst moment.

## What it does

```
PR → install · lint · test · build
main → build the artifact once → staging (migrate · deploy · smoke · roll back on failure)
production → promote the same artifact, only with a ship verdict and authorization
every deploy → a RELEASE block from real output, and a rollback that was tried first
```

```
RELEASE     staging · ghcr.io/acme/shop@sha256:4be1…c09a  (commit 3f2a91c)
RAN         ci.yml #41: install ✓ lint ✓ test ✓ (38 passed) build ✓ · deploy-staging ✓
MIGRATIONS  1 applied (0007_add_order_note — expand only)
SMOKE       GET https://staging.shop.example/health → 200 in 3 attempts
ROLLBACK    ./deploy/rollback.sh staging sha256:91d0…7e2b   (tested on staging 2026-09-28)
```

Three worked examples: [a first pipeline to a VPS](examples/first-pipeline-vps.md) ·
[a promotion stopped by DO NOT SHIP](examples/blocked-promotion.md) ·
[a failed smoke check and the rollback](examples/failed-smoke-rollback.md)

## When it activates

It activates on its own when you ask to set up or fix CI/CD, automated deploys,
staging or production environments, secrets in CI, rollback, or a
migration-safe deploy, or to *deploy this* when no repeatable path exists. It
stays quiet for comments or formatting in CI files, generic questions about CI
products, local setup, and the question of whether a change is safe to ship.
See [Activation](SKILL.md#activation).

## What it will not do

- **Decide whether a change is safe to ship.** Production Guard does. A
  production deploy needs its SHIP (or CONDITIONAL SHIP with the conditions
  met), or your explicit go-ahead, and authorization in `.delivery/config.yml`
  or in the session.
- **Rebuild for production.** Production gets the exact artifact staging ran.
- **Touch a secret value.** It names secrets and gives you the command to set
  them. Values stay in the CI or host secret store.
- **Report a deploy that did not run.** A written pipeline is `WRITTEN, NOT RUN`
  until a run's output says otherwise.
- **Judge whether a server fits the app.** Deployment Compatibility does.

References: [`pipeline-minimum.md`](references/pipeline-minimum.md) ·
[`deploy-targets.md`](references/deploy-targets.md) ·
[`migrations-and-rollback.md`](references/migrations-and-rollback.md) ·
[`secrets-and-environments.md`](references/secrets-and-environments.md)

## License

MIT — see [`LICENSE`](../../LICENSE).
