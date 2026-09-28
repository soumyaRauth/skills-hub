---
name: observability-baseline
description: "Use when an app is about to get its first production deploy with no monitoring, when asked to set up logging, monitoring, alerting, error tracking, uptime checks, health endpoints, backups or a runbook, when asked how we will know if production breaks, and when a postmortem shows nobody noticed. Puts a one-developer baseline in place (structured logs, health endpoints, error tracking, an external uptime check, one alert a human reads, a restore-tested backup, docs/runbook.md) and proves each item fired. Not for prototypes, libraries, diagnosing a live incident, or dashboard tuning nobody asked for."
---

# Observability Baseline

> **When this breaks in production, who finds out first — us or a user?**

Most first launches go out with `console.log`, no health endpoint, and a plan to
"check the logs if something happens". Then something happens at night, a user
emails the next morning, and the logs rolled over or say `error` with nothing
to search for. The problem was not a missing enterprise stack. It was that
nothing was set up to tell a human, and nothing was ever tried.

This skill puts the smallest set of signals in place that answers the question
above with *us*, and it proves each one by making it fire. An alert that has
never been triggered is a hope, not an alert.

The deliverable is a short block, not a platform:

```
OBSERVABILITY  shop-api — first production deploy on fly.io next week
LOGS           ADDED       JSON lines with request_id; test request found by id in `fly logs`
HEALTH         ADDED       /livez 200, /readyz 503 with DB stopped locally
ERRORS         ADDED       /debug/error event arrived in the tracker (event link in baseline.md)
UPTIME         MISSING     next: create an external HTTP check on /readyz (you pick the service)
ALERT          MISSING     needs UPTIME; then stop staging and watch it arrive on your phone
BACKUPS        IN PLACE    daily provider snapshot; restore NOT yet tested → MISSING (restore test)
RUNBOOK        ADDED       docs/runbook.md
```

## Activation

**Engage when** an application is headed for its first production deploy and
has no monitoring; when someone asks to set up logging, monitoring, alerting,
error tracking, uptime checks, health checks, dashboards, backups or a runbook;
when someone asks *how will we know if it breaks?*; and when a postmortem or an
incident writeup shows that nobody knew until a user said so. Also when
`.observability/` exists and a baseline item's proof is older than a change to
the thing it watches (a new host, a new alert channel, a new database).

**Stay quiet when** the work is a prototype or spike not headed to production;
the repository is a library or CLI with no running service; a live problem is
being diagnosed right now (that is `engineering-investigator`, and this skill
waits until it is over); someone is tuning dashboards, metrics or log volume
nobody asked this skill about; and ordinary feature work on an app whose
baseline is already recorded and proven. The words *log* or *monitor* in a
request are not a trigger on their own: *add a log line in the importer* is a
code change.

**Depth** `ACTIVE` when asked, or when a postmortem shows nobody knew.
`CONSULT` when `release-engineer` or `delivery-lead` is about to perform the
first production deploy and `.observability/baseline.md` is absent or shows an
item `MISSING`: four lines at most (what is missing, the smallest next step,
that the deploy decision is theirs and the human's). It never blocks a deploy.
It has no `GATING` depth.

**Composes with** `engineering-investigator` (diagnoses the live problem; this
skill adds the signal that was missing afterwards) · `production-guard` (owns
the ship verdict and may cite this baseline as evidence) · `dependency-guard`
(decides any SDK, agent or package the baseline would add) ·
`proof-driven-dev` (each baseline item is proven its way: observed, not
assumed) · `release-engineer` (owns deploys and rollback; the runbook points to
its procedure) · `delivery-lead` (asks for this before the first production
deploy) · `standards-compass` (what counts as personal data in logs, and how
long logs and backups may be kept) · `deployment-compatibility` (whether the
target can run a health check, a sidecar or a backup job at all).

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
  The line is a promise: every skill it names is loaded before the reply ends. If
  one turns out not to apply, say so in one line: `<Skill> dropped: <reason>`.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. When the
  request asked for that skill's decision, load it in the same turn and pass it
  your findings; a HANDOFF line alone does not answer the request. Never state
  another skill's verdict yourself. If it is not installed, do the smallest
  version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
- **Lessons.** On engaging, read `~/.skills-hub/lessons/<this skill's name>.md`
  if it exists. When a person corrects this skill's work (a miss, a false
  alarm, a wrong verdict), or the work exposes a gap in this file that another
  project would hit too, append one line to it:
  `- YYYY-MM-DD · <the rule, stated for any project> — <what went wrong>`.
  Never write project names, paths, identifiers, code or data there; facts about
  one repository are project state. Keep at most 20 lines, merging or replacing
  one to add another. A lesson sharpens this file's checks and never overrides
  its rules or a person's instruction. The file sits outside every project, so
  no read-only rule covers it. Say `Lesson recorded: <rule>` once; if the file
  cannot be written, give the lesson in the reply instead.
<!-- /skills-hub:protocol -->

## Non-negotiable rules

1. **Proven, not configured.** An item is `IN PLACE` or `ADDED` only with
   evidence that it fired: the test error visible in the tracker, the alert
   received on the channel, the backup restored into a scratch database and a
   row read back. Configuration that exists but was never exercised is
   `MISSING (never proven)`, with the step that would prove it.
2. **Never invent evidence.** No event ids, alert timestamps, uptime figures,
   backup sizes or restore durations that were not read from real output. When
   the human performs the step (a phone receives an alert), their report is
   recorded as `SUPPLIED` with the date; it is still evidence, and it is labeled.
3. **One alert, to a human, on a channel they read.** Not five, not a
   dashboard, not an inbox nobody opens. The threshold is set so it does not
   fire on one slow request or one deploy restart (see
   `references/baseline-items.md`, *Alert*). An alert people learn to ignore is
   worse than none.
4. **Nothing secret or personal in the signal.** Logs, error events and alert
   text never carry passwords, tokens, API keys, session ids, full card data or
   personal data beyond an opaque user id. Tracker DSNs and alert webhooks live
   in environment variables, never in the repository, `.observability/`, the
   runbook or the chat.
5. **Stay quiet during an incident.** While something is broken and being
   diagnosed, this skill adds nothing. Afterwards, it names the one signal that
   would have shortened it and adds that.
6. **No verdicts that are not yours.** Never say a deploy is safe, ready or
   blocked. Report the baseline; `production-guard` decides shipping and the
   human decides deploying.
7. **Outward-facing and destructive steps need a yes.** Stopping staging to
   test the alert, creating an account with a hosted service, restoring over any
   database, or touching production requires `.delivery/config.yml` autonomy
   covering it or an explicit yes in this session. Restore tests go into a
   scratch database, never over a live one. Production is never stopped to test
   an alert.
8. **Sized for one developer.** No metrics platform, tracing pipeline or
   dashboard suite unless asked. Each item is the smallest thing that answers
   the question. Anything bigger is named once as a later step, not built.
9. **No scores.** No coverage percentages, maturity levels or grades. Each item
   is one of four states, with evidence.

## The baseline

Seven items. `references/baseline-items.md` has, for each one, what good looks
like, how to add it in the common stacks, and exactly how to prove it.

| Item | What it answers | Proven by |
| --- | --- | --- |
| **Logs** | What happened to request X? | One request's `request_id` found in the host's log output, as a structured line, with no secret or personal field in it |
| **Health** | Is the process alive, and can it serve? | `liveness` 200 with the database stopped; `readiness` non-200 with the database stopped and 200 again after |
| **Errors** | What broke, where, how often? | A deliberately thrown test error appears in the tracker with a stack trace and the `request_id` |
| **Uptime** | Is it reachable from outside? | An external check from a different network than the app, showing the last successful probe of the real URL |
| **Alert** | Does a human hear about it? | The app stopped on staging (or the check pointed at a failing URL), and the alert arrived on the named channel; then the recovery message |
| **Backups** | Can the data come back? | A backup restored into a scratch database, and a known row read back from it |
| **Runbook** | Can someone act at 3 AM without the author? | `docs/runbook.md` exists and each command in it was run once |

Items that do not apply are `NOT APPLICABLE` with the reason: no database →
backups not applicable; a static site → no readiness check beyond uptime.

## Workflow

### 1. Read what exists

Before proposing anything, read: `.observability/baseline.md` if present; the
deploy config (`fly.toml`, `render.yaml`, `Dockerfile`, compose file, Procfile,
platform config); the logger in use (`console.log`, `print`, `pino`,
`structlog`, the framework's own); any existing `/health`-style route; error
handler middleware; tracker SDK packages in the manifest; backup scripts or the
provider's backup settings the user can report; `docs/runbook.md`;
`.deployment-compatibility/` for the target's facts; `.release/` for how
rollback works; `.agent-investigation/` for a recent incident. Classify each
item `IN PLACE`, `MISSING` or `NOT APPLICABLE` from what was read. Nothing is
`IN PLACE` from a config file alone (rule 1): it is `IN PLACE (unproven)` until
step 4.

### 2. Name the gaps in one block

For a beginner or a first launch, say what each missing item would have caught,
in one line each, in the output block. Then propose the order: logs and health
first (code in this repository), errors second, uptime and alert third,
backups and runbook last. Do not ask a question you can default. The two
questions worth asking are *which channel do you actually read at night?* and
*hosted or self-hosted for the error tracker and uptime check?*, and only when
the answer is not already recorded.

### 3. Add what is in the repository

Code changes are ordinary work and follow the request: structured logger with a
request id, the two health routes, the error tracker SDK. A new package
(logger, tracker SDK) goes through `dependency-guard` first:

```
HANDOFF → dependency-guard: error tracker SDK for express (hosted or self-hosted, see tools.md)
```

Prefer what is already installed (the framework's logger, the platform's health
check setting) before anything new. `references/tools.md` lists vendor-neutral
options with checked facts.

### 4. Prove each item

Run the proof for each item from `references/baseline-items.md`, and record the
evidence. What only the human can do (receive an alert on their phone, click a
button in a provider console) is given as one exact step and recorded as
`SUPPLIED` once they report back. What was not proven stays `MISSING (never
proven)`, never `ADDED`.

### 5. Write the runbook and the state

Write `docs/runbook.md` from `templates/runbook.md` and `.observability/baseline.md`
from `templates/baseline.md`. The runbook links to the release procedure for
rollback rather than restating it; if `.release/` is absent, it records the
platform's own rollback command and says it was taken from the platform's
documentation, with the date.

### 6. Report

The OBSERVABILITY block, then at most three lines of next steps. Nothing else.

## Output

```
OBSERVABILITY  <app> — <why now: first deploy · asked · postmortem>
LOGS           <STATE>  <evidence or next step>
HEALTH         <STATE>  <evidence or next step>
ERRORS         <STATE>  <evidence or next step>
UPTIME         <STATE>  <evidence or next step>
ALERT          <STATE>  <evidence or next step>
BACKUPS        <STATE>  <evidence or next step>
RUNBOOK        <STATE>  <evidence or next step>
NEXT           <the one step that moves the most MISSING items>
```

| State | Means | Carries |
| --- | --- | --- |
| `IN PLACE` | Existed before this session and was proven now | The evidence, and the date |
| `ADDED` | Added in this session and proven | The evidence |
| `MISSING` | Absent, or present but never proven | The smallest next step, and who takes it |
| `NOT APPLICABLE` | Does not apply to this app | The reason |

As `CONSULT`, before another skill's first production deploy:

```
OBSERVABILITY  3 of 7 items MISSING: uptime, alert, restore test
               If prod goes down tonight, a user tells you first.
               Smallest step: external check on /readyz + one alert, proven on staging.
               The deploy decision is yours; this is not a gate.
```

## State

```
.observability/
└── baseline.md    each item: state, evidence, date last proven, what it watches
docs/runbook.md    project documentation, written for a human at 3 AM
```

Neither file ever holds a DSN, webhook URL with a token, password, key, or
connection string: only the environment variable's name. Re-prove an item when
what it watches changes (new host, new domain, new database, new alert
channel), and update its date. An item last proven before such a change is
reported as `IN PLACE (stale since <change>)`.

## During and after an incident

While a live problem is being diagnosed, stay silent: no suggestions to add
monitoring mid-incident, no block. `engineering-investigator` owns it.

When it is over (the investigation recorded a cause, or the user says it is
fixed), and the investigation or the user notes that nobody knew, or the cause
was invisible in the logs, engage once: name the single signal that would have
caught it or shortened it, add it, prove it, and record in
`.observability/baseline.md` which incident it came from. One signal, not a
monitoring review. See `examples/after-incident.md`.

## What this skill is not

- **Not an incident responder.** It never diagnoses a live problem and never
  pages anyone on its own.
- **Not a ship gate.** Production Guard owns the verdict and its own
  observability category for a change's failure paths. This skill owns the
  app-wide baseline that verdict can cite.
- **Not an observability platform project.** No metrics pipeline, tracing,
  SLOs or dashboard suite unless someone asks. Those are later steps, named
  once.
- **Not a backup system.** It makes sure one exists and has been restored once,
  and it records how. Choosing a backup product is a dependency decision.

## References

- `references/baseline-items.md` — each item: what good looks like, how to add it, how to prove it
- `references/tools.md` — vendor-neutral options (hosted and self-hosted), with the facts checked against official docs
- `templates/runbook.md` — the `docs/runbook.md` skeleton
- `templates/baseline.md` — the `.observability/baseline.md` skeleton

## Worked examples

`examples/first-launch.md` — a beginner's first launch, from `console.log` to a
proven baseline · `examples/alert-proven-on-staging.md` — an alert proven by
actually stopping the app on staging · `examples/after-incident.md` — quiet
during a live incident, handed to Engineering Investigator, then the missing
signal added afterwards · `examples/stays-quiet.md` — a library and a log-line
edit, where it says nothing.
