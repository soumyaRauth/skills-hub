# Example — where it says nothing

## A library

> Add structured logging to this package.

The repository is a published npm library with no server, no deploy config and
no running process. There is nobody to page and nothing to keep up. The request
is ordinary work (and maybe a Dependency Guard decision if a logger package
would come in). Observability Baseline stays quiet: no block, no ⚡ line.

## A log line

> Log the import file name when the CSV importer starts.

A code change. The word *log* is not a baseline request. Nothing about who finds
out first changes. Quiet.

## A prototype

> Throwaway demo for Friday, deploy it anywhere.

Declared throwaway, not headed to production. Quiet. If the same app later gets
a production deploy, the first-deploy trigger applies then.

## When the same repository would earn a line

- It gains a service that runs in production.
- Someone asks *how will we know if it breaks?*
- `release-engineer` is about to do its first production deploy and there is no
  `.observability/baseline.md`: a four-line CONSULT, never a gate.
