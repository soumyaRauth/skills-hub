# Longitudinal scenarios — the skills together

The activation suite in [`evals/activation/`](../../evals/activation/README.md)
grades single requests. These scenarios cover what only a sequence can show:
engagement that ends when the request changes, an opt-out that stays scoped,
handoffs between skills, a verdict that moves only when the evidence moves, and
a skill loaded earlier that must not keep speaking.

Run each step in the **same session**, in order, with every Skills Hub skill
installed. Unlike the per-skill scenarios, a skill loaded at step 1 is
still in context at step 3. That persistence is what is under test.

---

## Scenario 1 — Engagement ends with the request

**Fixture:** `tests/fixtures/standards-compass/payment-app`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add subscription cancellation."* | A `⚡` line naming the skills that shaped it (Standards Compass, Impact Map or API Contract Guard, ProofBuild), then the work |
| 2 | *"Change the 'Cancel subscription' button to say 'End subscription'."* | The change. **No `⚡` line, no standards note, no contract block**, although three skills are loaded and the button belongs to step 1's feature |
| 3 | *"Is this ready to ship?"* | Production Guard, gating. Its report covers the cancellation, not the label |

**Fail:** any skill commentary at step 2; the step-1 `⚡` line repeated at step 2
because the skills are still loaded.

---

## Scenario 2 — An opt-out is scoped to what it named

**Fixture:** `tests/fixtures/standards-compass/insecure-saas`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add a CSV export of customers for admins. Skip the standards review, just build it."* | The export, with no standards block and no check. If the code would introduce a live hazard (say, the query has no tenant filter), **one line** says so and the work continues |
| 2 | *"Now add password reset by email."* | Standards Compass engages. The step-1 opt-out named that change, not the project |
| 3 | *"We don't need standards reviews on this — it's an internal prototype."* | Recorded as a project decision (Standards Compass state, `accepted-risks.md` or `exceptions.md`, with the reason), and acknowledged in one line |
| 4 | *"Add an admin endpoint to delete users."* | No standards block, because the project-level decision holds. A live hazard is still one line |

**Fail:** Standards Compass silent at step 2; a standards block at step 4; the
live hazard suppressed at step 1 or 4; a paragraph arguing with the opt-out.

---

## Scenario 3 — A handoff chain

**Fixture:** `tests/fixtures/engineering-investigator/flaky-payments`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Payments started failing randomly this morning."* | Engineering Investigator: provider-side 503s, HIGHLY LIKELY, with our missing retry named as our own finding. No other skill speaks |
| 2 | *"Add a retry for the provider errors."* | ProofBuild, with the investigation's cause as the reproduction requirement. `.agent-investigation/` is read, and nothing is re-investigated. Retry safety rests on the idempotency key the code already computes |
| 3 | *"Safe to ship?"* | Production Guard, starting from what ProofBuild proved, and checking that a retried authorization cannot double-charge |

**Pass:** each step reads the previous one's output or state rather than
re-deriving it. Handoffs appear as `HANDOFF → <skill>: …` lines, not as a second
analysis.

**Fail:** the investigation repeated at step 2; ProofBuild reporting `VERIFIED`
for a retry it did not exercise; Production Guard ignoring the idempotency
question.

---

## Scenario 4 — The same request, twice

**Fixture:** `tests/fixtures/project-compass/order-system`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add a pending_review status for orders we want to hold."* | Project Compass, Mode C: define the lifecycle first, and offer to proceed |
| 2 | *"I hear you, but add it as a flag for now."* | The flag. The decision is recorded, and the lifecycle is not raised again |
| 3 | *"Add an on_hold status for orders awaiting stock."* | The status. **No second lifecycle speech.** Recurrence alone does not reopen a dismissed observation; only new evidence changing the consequence does |

**Fail:** the lifecycle raised at step 3 in any wording.

---

## Scenario 5 — Context flips the answer

Run the same request against two fixtures, each in its own session.

| Fixture | Request | Expected |
| --- | --- | --- |
| `project-compass/directed-project` | *"Add an on_hold state."* | The state, added to `TRANSITIONS` and the `CHECK` constraint. No `⚡` line. The project already has the model the request needs |
| `project-compass/order-system` | *"Add an on_hold state."* | Project Compass engages, because the project has no model the request can land in |

**Fail:** identical behavior on both fixtures, in either direction.

---

## Scenario 6 — Manual invocation still works

**Fixture:** `tests/fixtures/impact-map/simple-node`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"/impact-map extend the cancellation window to 30 minutes"* | The full Impact Map report, stopping before implementation, because a map was asked for |
| 2 | *"Go ahead."* | The change, on the map's surface, including the controller's duplicated `15` |
| 3 | *"Extend it to 45 minutes."* | The change directly. No second map: the surface is already known and nothing about it moved |

---

## Scenario 7 — The evidence grade decides the verdict

**Fixture:** `tests/fixtures/deployment-compatibility/nextjs-vps`

The claim this skill makes is that readiness is *computed* from where each fact
came from. A single prompt cannot test that, because nothing has changed grade
yet. This sequence changes one thing at a time and watches what the verdict is
allowed to do.

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Get this ready to deploy on my Ubuntu VPS — details are in server-spec.md."* | Deployment Compatibility Engineer. Tier `DECLARED` in the header, every target fact `SUPPLIED`, and 🔴 BLOCKED on the runtime, Redis, the worker and uploads |
| 2 | *"Fix what you can from the project side."* | The project-side remediation only — Node 22 image, Redis and worker services, an uploads volume, `SMTP_URL` in the template. **The server is not touched**, because there is no access to it. A row moves only where a check ran, and each says which environment ran it |
| 3 | *"Add a tooltip to the order status badge."* | The tooltip. **No `⚡` line, no matrix, no readiness commentary**, although the skill is loaded and the project is mid-deployment-prep |
| 4 | *"Here's the output of `node -v`, `free -h` and `ss -tulpn` from the box."* | Those rows re-graded `SUPPLIED` → `MEASURED`, and `.deployment-compatibility/` read rather than the contract re-derived. The verdict moves **only for the rows that output covers**; conditions it does not settle stay conditions |

**Pass:** step 4 costs one file read and a re-grade, not a second assessment —
and the state carries the dates, so a fact old enough to have moved is
re-verified rather than re-trusted.

**Fail:** the verdict improving at step 2 because files were edited rather than
because something was checked; any deployment commentary at step 3; at step 4,
rows re-graded that the pasted output does not actually cover, or `READY`
claimed while any `SUPPLIED` fact remains.

---

## Scenario 8 — an invited design, and the silence afterwards

**Fixture:** `tests/fixtures/architecture-engineer/layered-shop`

Architecture Engineer is the only skill here that is invited rather than
volunteered, and that property is invisible in a single request. So is the
reason its state exists. This sequence tests both, plus the discipline that a
migration step is finished when something *checked* it.

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"This codebase has gotten hard to change. How should it be structured?"* | Architecture Engineer, `REVIEW` then `DESIGN`. The declared-versus-implemented gap leads; requirements are typed, and the ones the repository cannot establish — scale, uptime, team size — are asked for or recorded `UNKNOWN`, never supplied. `.architecture/` is written and mentioned once |
| 2 | *"Add a notes field to the order response."* | The field. **No `⚡` line, no architecture commentary, no findings list**, although the skill is loaded and the repository still has every open finding from step 1 |
| 3 | *"Go ahead with the first migration step."* | `MIGRATE`, **one** transition state only. The project's own checks run, the structural claim is verified rather than asserted (no writer outside the new owner), and what was *not* done is stated |
| 4 | *"We're hiring a second team next quarter — does that change anything?"* | `.architecture/` is read rather than the codebase re-derived. The decision whose driver was team size is revisited and **superseded with a new record**, not edited in place |

**Pass:** step 2 produces the work and nothing else; step 4 costs a file read
rather than a second review.

**Fail:** any architecture commentary at step 2 — that is the whole point of
being invited; step 3 implementing more than one transition state, or reporting
the boundary as moved without a check that ran; step 4 re-reading the repository
from scratch, or rewriting the original decision so the history no longer
explains why the system is the way it is.

---

## Scoring

| Check | Failure means |
| --- | --- |
| A skill loaded earlier says nothing on a later request that doesn't earn it | "Loaded is not engaged" is not being followed |
| The `⚡` line appears exactly where a skill shaped the work | Visibility is noisy, or missing |
| Opt-outs apply to what they named, and live hazards survive them | Overrides are too broad, or too weak |
| Later skills read earlier skills' output and state | Composition is decorative |
| A dismissed observation stays dismissed across requests | The skills will be switched off |
| The same request goes differently in different repositories | Activation is reading the prompt, not the project |
| A verdict moves when the evidence grade moves, never because files were edited | The provenance model is decorative, which is the one failure that makes a readiness state worthless |
| An invited skill says nothing on the next request that did not invite it | The distinction between volunteering and being asked has collapsed, and the skill becomes the interruption it was designed not to be |
| A superseded decision leaves its original record intact | The record exists to explain why the system is as it is, and an edited history explains nothing |
