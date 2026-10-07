# Workspace and Resume

## Workspace and resume

For STANDARD and INCIDENT work, persist state so the investigation survives the
session:

```
.agent-investigation/
├── incident.md      report, normalized symptom, scope, capabilities, status
├── hypotheses.md    the ledger: kill conditions, evidence, statuses
├── evidence.md      numbered observations, each typed and sourced
├── experiments.md   question, method, observation, what it eliminated
├── timeline.md      only when the sequence of events is itself evidence
└── conclusion.md    cause, confidence, verification, recommendation
```

Create the **smallest set that carries the state** — two files is a complete
workspace for most STANDARD investigations, and QUICK creates none. Write facts
and decisions, not narration, and never internal reasoning.

**If `.agent-investigation/` already exists, read it before doing anything
else.** Continue the case: honor disproven hypotheses, skip completed
experiments, pick up the highest-value open question. "Continue the
investigation" means resume, not restart. See
`references/investigation-workspace.md`.
