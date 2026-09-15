# Example — the endpoint that gets no contract block

## Request

> Add an endpoint the dashboard can call to get this week's order count.

## What was read

- `web/` is this repository's only frontend. It is built and deployed with the
  API from the same workflow job, and it calls relative `/api/...` paths.
- No mobile app, no published API document, no API keys, no `/v1` prefix on
  `/api/*` routes.

## Response

The endpoint, following the existing `/api/dashboard/*` handlers, and the
dashboard wired to it.

No decisions block and no `⚡` line.

## Why

Every consumer of `/api/dashboard/*` ships in the same deploy as the endpoint.
If its shape is wrong, the fix is one commit that changes both sides at once.
Nothing here is promised to anyone who deploys on another schedule.

## When the same request would earn a block

- The dashboard is also a **mobile app** with installed builds that outlive a
  deploy.
- The web app is a **cached single-page app** whose old bundles keep calling the
  API after a release, and the change removes or retypes a field those bundles
  read.
- The endpoint is **documented for customers**, or reachable with an API key.
