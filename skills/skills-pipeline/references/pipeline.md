# The menu

`SKILL.md` shows this list when the pipeline starts, and you pick the sequence
by number. The numbers are in the recommended build order, so `all` runs 1 to
10. Number 11 is for a bug or symptom, not a build, so pick it by number.
Numbers 12 to 15 cover the rest of a project's life: 12 before 1 on a new
project, 13 before a build that needs tickets, 14 and 15 after the ship gate.
Pick them by number. For working through a whole backlog, ask for the delivery
lead instead of the pipeline.
Edit this file to add, remove or renumber skills.

| # | Stage | Skill | Stops when |
| --- | --- | --- | --- |
| 1 | Frame | `project-compass` | A business rule the build depends on is undecided |
| 2 | Design | `architecture-engineer` | Options exist and a person must choose one |
| 3 | Standards | `standards-compass` | Never. Its requirements carry into Build |
| 4 | Contract | `api-contract-guard` | A decision consumers will depend on has no project convention to follow |
| 5 | Dependencies | `dependency-guard` | A verdict is DON'T ADD and the plan needs another way |
| 6 | Impact | `impact-map` | The map shows the change reaches further than the request said |
| 7 | Build | `proof-driven-dev` | BLOCKED |
| 8 | Localize | `practical-localizer` | Never |
| 9 | Deploy target | `deployment-compatibility` | BLOCKED |
| 10 | Ship gate | `production-guard` | DO NOT SHIP |
| 11 | Investigate | `engineering-investigator` | The cause is found and the fix is a decision a person has to make |
| 12 | Kickoff | `project-kickoff` | The repository already holds code (not a kickoff), or product questions are waiting for answers |
| 13 | Plan | `delivery-planner` | A ticket depends on a business rule nobody has decided |
| 14 | Release | `release-engineer` | A production deploy lacks a ship verdict or authorization, a rollback is untested, or a smoke check fails and rolls back |
| 15 | Observe | `observability-baseline` | Never. MISSING items carry into the ledger with their next step; it is not a gate |
