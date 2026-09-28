# Observability Baseline

An Agent Skill that asks one question before an app goes live:

> **When this breaks in production, who finds out first — us or a user?**

```bash
npx skills add soumyaRauth/skills-hub --skill observability-baseline
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill observability-baseline --agent claude-code --copy
```

---

## Why it exists

First launches usually go out with `console.log`, no health endpoint and a plan
to "check the logs if something happens". Then something happens at night, a
user emails in the morning, and the logs say `error` with nothing to search for.
The gap is rarely a missing enterprise stack. Nothing was set up to tell a
human, and nothing was ever tried.

## What it does

```
read what exists (deploy config · logger · routes · tracker · backups · runbook)
  → seven items, each IN PLACE · ADDED · MISSING · NOT APPLICABLE
  → add what lives in the repo (logs, health, tracker SDK via Dependency Guard)
  → prove each one by making it fire (test error arrives · alert received · backup restored)
  → docs/runbook.md + .observability/baseline.md
```

```
OBSERVABILITY  bookshelf — first production deploy next week
LOGS           ADDED       JSON lines with request_id; test request found by id in the host logs
HEALTH         ADDED       /livez 200, /readyz 503 with the database stopped
ERRORS         ADDED       test error arrived in the tracker
UPTIME         MISSING     next: external HTTP check on /readyz
ALERT          MISSING     needs UPTIME; then stop staging and watch it arrive
BACKUPS        MISSING     never restored; next: restore into a scratch database
RUNBOOK        ADDED       docs/runbook.md
```

Examples: [a beginner's first launch](examples/first-launch.md) ·
[an alert proven on staging](examples/alert-proven-on-staging.md) ·
[quiet during an incident, then the missing signal](examples/after-incident.md) ·
[where it says nothing](examples/stays-quiet.md)

## When it activates

On its own when an app is heading for its first production deploy without
monitoring, when someone asks for logging, monitoring, alerting, error
tracking, uptime checks, backups or a runbook, or asks *how will we know if it
breaks?*, and after an incident that customers noticed first. It stays quiet
for prototypes, libraries, a live incident being diagnosed, and log-line edits.
See [Activation](SKILL.md#activation).

## What it will not do

- **Call something working because it is configured.** An alert that never
  fired, or a backup never restored, is `MISSING`.
- **Build an enterprise stack.** One alert, one uptime check, one tracker. A
  metrics or tracing platform is named once as a later step.
- **Put secrets or personal data in the signal.** Logs, events and the runbook
  hold variable names, never values.
- **Stop production, or anything, without a yes.** Alert tests run on staging.
- **Speak during an incident, or decide a release.** Engineering Investigator
  owns the incident; Production Guard owns the ship verdict.

References: [`baseline-items.md`](references/baseline-items.md) ·
[`tools.md`](references/tools.md) (vendor-neutral options, facts checked
against official docs) · templates: [`runbook.md`](templates/runbook.md) ·
[`baseline.md`](templates/baseline.md)

## License

MIT — see [`LICENSE`](../../LICENSE).
