# The pipeline minimum

## Contents

- The four stages
- GitHub Actions shape
- GitLab CI shape
- Other CI systems
- The smoke script

What every project this skill touches ends up with, and the shapes to write it
in. Extend the CI the project already has; these are shapes, not files to paste
over existing ones.

Sources, all checked 2026-09-28:
- GitHub Actions workflow syntax — https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- GitHub Actions secrets — https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- GitHub environments — https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
- GitHub Container Registry — https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- GitHub-hosted Ubuntu 24.04 runner software (Docker and Compose preinstalled) — https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md
- GitLab CI/CD YAML reference — https://docs.gitlab.com/ci/yaml/

## The four stages

| Stage | Must | Must not |
| --- | --- | --- |
| PR checks | Install from the lockfile (`npm ci`, `pip install -r` with pinned versions), then lint, test, build. Fail on the first red step | Deploy anything; read deploy secrets (secrets are not passed to workflows from forks, which is correct) |
| Artifact | Build once on main, tag with the full commit SHA, push, record the digest from the push output | Use `latest` as the deployed reference; rebuild per environment |
| Staging | Deploy the digest, run migrations once, smoke-check, roll back on a failed smoke | Deploy a digest the PR checks did not pass |
| Production | Promote a digest staging already ran and smoke-checked | Rebuild; run without the step 7 conditions in SKILL.md |

A missing `lint` or `test` script is reported `ABSENT`. It is not filled by
inventing a config.

## GitHub Actions shape

Pin every `uses:` to a full commit SHA. The SHA is not written from memory:
resolve it from the action's release, and route a new action through
`dependency-guard`. `<sha>` below is a placeholder, never a value to ship.

`.github/workflows/ci.yml`:

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  checks:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@<sha>        # pinned; version via dependency-guard
      - uses: actions/setup-node@<sha>
        with:
          node-version-file: .nvmrc          # or the engines field the project declares
      - run: npm ci
      - run: npm run lint                    # omit and report ABSENT if there is no script
      - run: npm test
      - run: npm run build --if-present

  image:
    if: github.event_name == 'push'
    needs: checks
    runs-on: ubuntu-24.04
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@<sha>
      - run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u "${{ github.actor }}" --password-stdin
      - run: docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
      - run: docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
      # read the digest from the push output and pass it on; never use :latest to deploy

  deploy-staging:
    needs: image
    runs-on: ubuntu-24.04
    environment:
      name: staging
      url: https://staging.example.com
    concurrency:
      group: deploy-staging
      cancel-in-progress: false             # never cancel a deploy halfway
    steps:
      - uses: actions/checkout@<sha>
      - run: ./deploy/deploy.sh staging "ghcr.io/${{ github.repository }}:${{ github.sha }}"
      - run: ./deploy/smoke.sh https://staging.example.com/health || { ./deploy/rollback.sh staging; exit 1; }
```

Note on `permissions`: once any permission is listed, every unlisted one is set
to none. That is the point; list only what the job needs.

Note on `ghcr.io/${{ github.repository }}`: registry image names must be
lowercase. If the owner or repository name has capitals, set the image name
explicitly.

`.github/workflows/deploy-production.yml`:

```yaml
name: deploy-production
on:
  workflow_dispatch:
    inputs:
      image:
        description: 'Image digest staging verified (ghcr.io/owner/app@sha256:...)'
        required: true
        type: string

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-24.04
    environment:
      name: production
      url: https://example.com
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@<sha>
      - run: ./deploy/deploy.sh production "${{ inputs.image }}"
      - run: ./deploy/smoke.sh https://example.com/health || { ./deploy/rollback.sh production; exit 1; }
```

Environment protection (required reviewers, deployment branches) gates the job
before it can read the environment's secrets. Availability depends on the plan:
GitHub Free gets environments only on public repositories; private repositories
need Pro or Team. On a plan without them, `workflow_dispatch` plus this skill's
step 7 is the gate, and the PIPELINE summary says so.

## GitLab CI shape

```yaml
stages: [check, build, deploy]

checks:
  stage: check
  image: node:<exact-version>          # pinned; via dependency-guard
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - npm ci
    - npm run lint
    - npm test
    - npm run build --if-present

deploy-staging:
  stage: deploy
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - ./deploy/deploy.sh staging "$IMAGE"
    - ./deploy/smoke.sh https://staging.example.com/health || { ./deploy/rollback.sh staging; exit 1; }

deploy-production:
  stage: deploy
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  environment:
    name: production
    url: https://example.com
  script:
    - ./deploy/deploy.sh production "$IMAGE"
    - ./deploy/smoke.sh https://example.com/health || { ./deploy/rollback.sh production; exit 1; }
```

The `build` job and how `$IMAGE` is derived follow the project's registry;
GitLab's registry variables were not checked for this file and are
`UNVERIFIED` here. Read them from the GitLab docs before writing that job.

## Other CI systems

Map the same four stages onto what the project uses. Check each keyword against
that system's official reference before writing it, and cite it in
`.release/environments.md`.

## The smoke script

```bash
#!/usr/bin/env bash
# deploy/smoke.sh <health-url>
set -euo pipefail
curl --fail --silent --show-error --max-time 10 \
     --retry 5 --retry-delay 3 --retry-all-errors "$1"
```

`--fail` exits non-zero on HTTP 400 and above; `--retry-all-errors` retries on
any error and is used together with `--retry`. Source: https://curl.se/docs/manpage.html
(checked 2026-09-28). A health endpoint that returns 200 without touching its
dependencies proves only that the process is up; say so in `SMOKE` when that is
all it checks.
