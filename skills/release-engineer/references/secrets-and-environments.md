# Secrets and environments

Sources, checked 2026-09-28:
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- https://cli.github.com/manual/gh_secret_set (`--body` omitted reads standard input; `--env` for an environment secret)
- https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
- https://docs.fly.io/flyctl/secrets-set/
- https://docs.railway.com/reference/cli-api
- https://render.com/docs/deploy-hooks

## Where a secret may live

| Place | Allowed |
| --- | --- |
| CI secret store (repository or environment secrets) | Yes, referenced by name |
| Platform secret store (Fly secrets, Render/Railway environment settings) | Yes |
| An env file on the host, outside the repository, readable only by the app user | Yes, for a VPS |
| The repository, including `.env.example` values, workflow files, `.release/` | Never |
| A log line, commit message, PR comment, ticket, chat | Never |

## The human sets secrets; the agent names them

Give the command, never ask for the value in the conversation:

```bash
# GitHub, environment-scoped. Without --body the value is read from standard input
# (a prompt when typed), so it never lands in shell history.
gh secret set --env staging STAGING_SSH_KEY < ~/.ssh/deploy_staging
gh secret set --env staging STAGING_HOST
gh secret set --env staging STAGING_KNOWN_HOSTS
```

Reference it in a workflow as `${{ secrets.STAGING_SSH_KEY }}`. Secrets are not
passed to workflows triggered from a fork (except `GITHUB_TOKEN`), which is why
deploy jobs never run on pull requests. A sensitive value that is not a stored
secret is masked with `::add-mask::VALUE` before anything could print it.

Environment secrets are readable only by jobs that name the environment, and
only after its protection rules (required reviewers, allowed branches) pass.
Plan limits: GitHub Free has environments only for public repositories; private
repositories need Pro or Team.

## Environments record

`.release/environments.md`, one section each:

```
## staging
url          https://staging.shop.example
target       VPS over SSH, docker compose (fit: .deployment-compatibility/target.md, 2026-09-20)
deploy       on merge to main, ci.yml deploy-staging
secrets      STAGING_SSH_KEY, STAGING_HOST, STAGING_KNOWN_HOSTS   (names only)
health       /health
promotion    automatic (autonomy.deploy_staging: auto)
```

## Findings to raise

- A secret value committed at any point in history: live hazard. Rotating the
  credential is the fix; removing the line is not. One line, then continue.
- A deploy key with more reach than deploying (root, a personal key, a token
  with admin scope): `HANDOFF → standards-compass`.
- `StrictHostKeyChecking no`, `curl -k`, or a disabled check in a pipeline:
  never added by this skill; flagged when found.
