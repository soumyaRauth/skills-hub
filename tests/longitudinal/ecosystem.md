# Longitudinal scenarios — the skills together

The activation suite in [`evals/activation/`](../../evals/activation/README.md)
grades single requests. These scenarios cover what only a sequence can show:
engagement that ends when the request changes, an opt-out that stays scoped,
handoffs between skills, and a skill loaded earlier that must not keep
speaking.

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

## Scoring

| Check | Failure means |
| --- | --- |
| A skill loaded earlier says nothing on a later request that doesn't earn it | "Loaded is not engaged" is not being followed |
| The `⚡` line appears exactly where a skill shaped the work | Visibility is noisy, or missing |
| Opt-outs apply to what they named, and live hazards survive them | Overrides are too broad, or too weak |
| Later skills read earlier skills' output and state | Composition is decorative |
| A dismissed observation stays dismissed across requests | The skills will be switched off |
| The same request goes differently in different repositories | Activation is reading the prompt, not the project |
