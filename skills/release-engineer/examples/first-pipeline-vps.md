# Example — a beginner's first pipeline, to a VPS

A small Node web app with a `Dockerfile` and tests, no CI, and one VPS the
developer already rents. The request:

> Set up CI/CD so every merge to main runs the tests and deploys to staging.

---

## 1. Read what exists

```
package.json     scripts: start, test (node --test) — no lint, no build
Dockerfile       node base image, EXPOSE 3000, CMD node src/server.js
src/server.js    GET /health → 200 {"ok":true}
.github/         absent
.release/        absent
.deployment-compatibility/target.md   staging VPS, READY WITH CONDITIONS, 2026-09-20
.delivery/config.yml                  autonomy.deploy_staging: auto, deploy_production: ask
```

The target's fit is recorded, so no handoff to `deployment-compatibility`. The
repository is on GitHub, so GitHub Actions: no second CI system.

## 2. The announcement and the plan

```
⚡ Release Engineer — no CI; merge to main should reach staging
```

Staging, in one line for a beginner: *a copy of production that nobody depends
on, where every merge lands first.*

## 3. What gets written

- `.github/workflows/ci.yml` — `checks` (npm ci, npm test) on every PR and on
  main; `image` builds once and pushes `ghcr.io/<owner>/<app>:<sha>` on main;
  `deploy-staging` deploys that image and smoke-checks it.
- `deploy/deploy.sh`, `deploy/smoke.sh`, `deploy/rollback.sh`, from
  `references/deploy-targets.md` and `references/migrations-and-rollback.md`.
- `.release/environments.md` with the staging section: secret names only.

Two actions are needed, `actions/checkout` and `actions/setup-node`:

```
HANDOFF → dependency-guard: two GitHub Actions to pin by commit SHA
```

No lint script exists. The workflow runs what exists and the summary says
`ABSENT`; adding a linter is a separate change, not slipped in here.

No production workflow yet: rule 5 says production waits for a rollback that
was tried on staging.

## 4. The report

```
PIPELINE    GitHub Actions · .github/workflows/ci.yml
PR CHECKS   install ✓ · lint ABSENT (no script) · test ✓ · build ABSENT (no script; image built in `image`)
STAGING     on merge to main → VPS over SSH, docker compose, image by commit SHA
PRODUCTION  not written yet — needs a staging rollback drill first
ROLLBACK    ./deploy/rollback.sh staging · NOT RUN
STATUS      WRITTEN, NOT RUN — secrets not set: STAGING_SSH_KEY, STAGING_HOST, STAGING_KNOWN_HOSTS
NEXT        run these three, then open a PR and watch `checks` run:
              gh secret set --env staging STAGING_SSH_KEY < ~/.ssh/deploy_staging
              gh secret set --env staging STAGING_HOST
              ssh-keyscan <your-host> | gh secret set --env staging STAGING_KNOWN_HOSTS
```

`ssh-keyscan` trusts whatever answers; the reply asks the developer to compare
the printed fingerprint with the one their provider's console shows before
setting it.

`test ✓` is marked because `npm test` was run locally in this session and its
output read (`# pass 3`). The workflow itself has not run, so the status is
`WRITTEN, NOT RUN`, not "working".

## 5. After the secrets are set and the first merge lands

```
RELEASE     staging · ghcr.io/<owner>/<app>@sha256:<from push output>  (commit <sha>)
RAN         ci.yml run #1: checks ✓ (3 passed) · image ✓ · deploy-staging ✓
MIGRATIONS  none
SMOKE       GET https://staging.<domain>/health → 200 on attempt 1
ROLLBACK    ./deploy/rollback.sh staging · NOT RUN (first deploy; nothing to roll back to)
```

The second merge gives the rollback drill something to return to. After it,
`.release/rollback.md` holds the drill's output, and the production workflow is
the next step.

## What did not happen

- No production deploy, and no production workflow yet.
- No `latest` tag anywhere a deploy reads it.
- No secret value in the chat, the repository or `.release/`.
- No readiness verdict. Nobody asked, and it is `production-guard`'s.
