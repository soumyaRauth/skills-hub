# Deploy targets

The common targets for a first deployment, and for each: how the pipeline
deploys, where secrets go, and the rollback. Every flag here was checked against
the provider's official documentation on 2026-09-28, with the URL beside it.
Anything not listed was not checked: check it before writing it, or mark it
`UNVERIFIED`.

Whether the target can run the app at all (runtime, memory, services, ports) is
`deployment-compatibility`'s verdict. This file assumes it, or hands off.

## Choosing, for a beginner with no target yet

| App | Default | Why |
| --- | --- | --- |
| Static or frontend-only (built HTML/JS) | Vercel or Netlify | Every deploy is kept; rollback is republishing an earlier one |
| Web app with a `Dockerfile`, wants a managed platform | Fly.io, Render or Railway | The platform keeps releases and runs the container |
| Web app, already has a VPS or wants one fixed-cost box | VPS over SSH with Docker Compose | Nothing new to learn but SSH and Compose; rollback is the previous digest |
| Kubernetes | Only when manifests or a cluster already exist | Never introduced by this skill |

Offer the choice once; do not compare pricing (not checked, and it changes).

## VPS over SSH, Docker Compose

Sources: https://docs.docker.com/reference/cli/docker/compose/up/ ·
https://docs.docker.com/reference/cli/docker/compose/pull/ ·
https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/
(checked 2026-09-28)

On the host, `compose.yaml` references the image through a variable, so the
pipeline chooses the digest and the file never changes:

```yaml
services:
  web:
    image: ${APP_IMAGE:?APP_IMAGE must be set}
    env_file: .env.production        # lives only on the host, never in git
    restart: unless-stopped
    ports: ["127.0.0.1:3000:3000"]    # behind the reverse proxy
```

`${VAR:?error}` stops with an error when the variable is unset or empty. Shell
environment variables take precedence over the `.env` file for interpolation.

`deploy/deploy.sh <env> <image>` runs, over SSH:

```bash
ssh "$DEPLOY_USER@$DEPLOY_HOST" "cd /srv/app \
  && { cp current-image previous-image 2>/dev/null || true; } \
  && echo '$IMAGE' > current-image \
  && APP_IMAGE='$IMAGE' docker compose pull web \
  && APP_IMAGE='$IMAGE' docker compose up -d --wait web"
```

`--wait` waits for services to be running or healthy and implies detached mode;
give the service a `healthcheck` so *healthy* means something. `pull` fetches
the image without starting it, so a failed pull leaves the running version
alone.

Rollback: the same command with the digest in `previous-image`. Migrations are
not reversed (see `migrations-and-rollback.md`).

SSH in CI: the private key, host and the host's public key line
(`known_hosts`) are secrets or variables in the CI store. Write the key to a
file with mode 600 on the runner, and pass `known_hosts`. Never disable host key
checking. Use a dedicated deploy user, not root.

**systemd instead of Compose** (no Docker on the host): deploy a versioned
release directory (`/srv/app/releases/<sha>`), switch a `current` symlink, and
`systemctl restart <unit>`. Rollback switches the symlink back. The unit file
itself is `deployment-compatibility`'s territory when the host is unassessed.

## Fly.io

Sources: https://docs.fly.io/flyctl/deploy/ · https://docs.fly.io/flyctl/releases/ ·
https://docs.fly.io/flyctl/secrets-set/ (checked 2026-09-28)

| Need | Command |
| --- | --- |
| Deploy a built image | `fly deploy --app <app> --image <registry/app@sha256:…>` |
| Choose the replacement strategy | `--strategy` — `canary`, `rolling` (default), `bluegreen`, `immediate` |
| Separate staging and production | one app per environment, `--app` or `--config` per environment |
| See what each release ran | `fly releases --app <app> --image` |
| Set a secret | `fly secrets set --app <app> NAME=VALUE` (the human runs it); `--stage` sets without redeploying |
| Roll back | `fly deploy --app <app> --image <previous image from fly releases --image>` |

No dedicated `rollback` command was found in the pages checked; redeploying the
previous image is the documented building block.

## Render

Sources: https://render.com/docs/deploy-hooks · https://render.com/docs/rollbacks
(checked 2026-09-28)

- Deploy from CI with the service's **deploy hook**: a plain `GET` or `POST` to
  its URL. The URL is a secret; store it as one. For an image-backed service,
  append `imgURL` to deploy a specific tag or digest.
- Rollback: the dashboard (Deploys → a successful deploy → Rollback) or the
  API's roll-back-deploy endpoint.
- Caveats from Render's docs: a dashboard rollback turns autodeploy off (the API
  rollback does not); rollbacks skip the build, so environment-group changes are
  not rolled back; an image referenced by tag is re-pulled and may differ, so
  deploy by digest; only deploys whose artifacts are still retained can be
  rolled back.

## Railway

Source: https://docs.railway.com/reference/cli-api (checked 2026-09-28)

| Need | Command |
| --- | --- |
| Deploy from CI | `RAILWAY_TOKEN` set as a CI secret, then `railway up --service <svc> --environment <env> --detach` |
| Redeploy the latest deployment | `railway redeploy` |
| Remove the latest deployment | `railway down` |

No rollback-to-a-chosen-deployment command was found in the page checked. Use
the dashboard's deployment history, and write the exact rollback step into
`.release/rollback.md` only after it has been done once on staging.

## Vercel (frontends)

Source: https://vercel.com/docs/cli/rollback (checked 2026-09-28)

- Rollback: `vercel rollback [deployment-id or url]`; `vercel rollback status`
  shows a pending rollback; `--timeout` bounds the wait.
- On the Hobby plan, rollback reaches only the previous production deployment.
- Undo a rollback with `vercel promote [deployment-id or url]`, which also
  re-enables automatic production domain assignment.

## Netlify (frontends)

Sources: https://cli.netlify.com/commands/deploy/ ·
https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview/
(checked 2026-09-28)

- Deploy from CI: `NETLIFY_AUTH_TOKEN` as a CI secret, then
  `netlify deploy --dir <build-dir> --site <site-id>` for a preview and add
  `--prod` for production.
- Rollback: **Publish deploy** on an earlier successful deploy in the UI. It is
  instant and does not rebuild. It does **not** stop auto publishing: the next
  Git-triggered production deploy overwrites it unless auto publishing is
  locked. No CLI rollback command was found in the page checked.

## Kubernetes (only if already present)

Source: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_undo/
(checked 2026-09-28)

- Deploy by setting the image digest in the manifest the project already uses,
  then wait for the rollout.
- Rollback: `kubectl rollout undo deployment/<name> -n <ns>`; `--to-revision=<n>`
  for an older revision; `--dry-run=server` to preview.
