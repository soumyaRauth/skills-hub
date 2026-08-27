# Tool Discovery and Access Boundaries

Two failures live here, and they are opposites: claiming access you do not have,
and missing evidence that was sitting in the repository. Both are prevented by
spending sixty seconds enumerating what is actually reachable, before
investigating.

## Enumerate first

```bash
git rev-parse --is-inside-work-tree 2>/dev/null   # history
ls package.json composer.json pyproject.toml go.mod Makefile 2>/dev/null
ls -d logs log var/log storage/logs 2>/dev/null   # logs in the tree
ls -d .env* docker-compose* Dockerfile k8s deploy 2>/dev/null
```

Then check, without assuming:

- **Repository and history** — is there more than one commit, is it shallow, does
  it contain the service in question or only part of it?
- **Runnable project** — do the test, build, and dev commands exist and work?
- **Evidence in the tree** — committed logs, trace exports, profiling output,
  benchmark results, incident notes, `ops/` or `runbooks/`.
- **Connected tools** — which MCP servers and CLIs are actually available in
  *this* session: observability, cloud provider, database, browser, HTTP client.
  Availability is a fact you observe, not one you assume from the project's
  documentation. A `datadog` mention in the README is not a Datadog connection.
- **Environments** — can anything be run locally, is there a staging URL, is the
  production system reachable at all (and are you authorized to touch it —
  reachable is not the same as permitted).
- **What the user supplied** — a pasted log, a screenshot, a request id, a time
  window. This is often the only production evidence available, and it is easy
  to overlook while looking for a tool.

Write the result into `incident.md` as two lists — available, and not
available — and repeat the boundary in the answer whenever it limits the
conclusion.

## Three environments, three investigations

**Repository only.** No logs, no telemetry, nothing running. You can establish
what the code does, what changed and when, what the tests cover, what the
configuration says, and which mechanisms could produce the reported symptom. You
cannot establish what production did. Every conclusion is bounded by that, and
the honest output is usually a ranked set of candidate mechanisms plus the
minimal evidence that would discriminate between them — not a cause.

**Repository plus evidence** (logs, traces, an exported metric, a HAR file, a
user's request id). Now scope and timing become answerable, correlation becomes
checkable, and `HIGHLY LIKELY` becomes reachable. Read the evidence before the
code: it tells you which code to read.

**Repository plus live access** (observability tooling, a queryable database, a
staging environment, a browser). Reproduction and controlled comparison are
available, so `CONFIRMED` is reachable. This is also where the safety rules bind
hardest — see `production-safety.md`.

## Adapting, not pretending

When a capability is missing, name the substitute and its weakness:

| Missing | Substitute | What it cannot do |
| --- | --- | --- |
| APM traces | Application logs with timestamps and request ids | Attribute time within a request |
| Production metrics | Log-derived rates over a window | Cover what is not logged |
| Production database | Schema, migrations, and query text in the repo | Show real data volume, plans, or lock behavior |
| Staging environment | Local reproduction with seeded data | Reproduce scale, concurrency, or real integrations |
| Customer environment | The user's own report and one measurement they can run | Establish their network or device state |
| Deploy history | Git tags, release commits, changelog | Prove what is actually running in production |

Every substitute is written into the evidence with its limitation. A conclusion
built on substitutes carries a confidence level that reflects them.

## Asking the user to be the tool

When the missing evidence is on the other side of a boundary you cannot cross,
the user or the affected customer can often produce it in one step. Ask for
something specific and small:

```
Could you run this on the affected connection and paste the output?

  curl -o /dev/null -s -w 'ttfb=%{time_starttransfer} total=%{time_total} size=%{size_download}\n' <URL>
```

Or: one affected request id and one unaffected one; a browser network-tab
screenshot of the slow interaction; the response headers for one failed request;
the exact error text and its timestamp.

Prefer a request whose result is a number over one whose result is a
description, and never ask for more than about three things at once. If a step
requires production access or credentials, say what it would show and let them
decide whether to run it — do not ask for the credentials.

## Recording the boundary

The boundary belongs in the answer whenever it limits the conclusion:

> Production telemetry is not reachable from this environment, so the timing
> evidence here comes from the access log committed to the repository, which
> covers this service only.

That sentence is what separates an honest `LIKELY` from a dishonest `HIGH`, and
it is what tells the reader which extra access would upgrade the answer.
