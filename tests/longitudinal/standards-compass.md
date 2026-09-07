# Longitudinal scenarios — Standards Compass

A single audit cannot test this skill. Half of its claim is about sequence: that
guardrail mode keeps quiet on the boring work and speaks on the risky work, that
a dismissed finding stays dismissed, that the second assessment is cheaper than
the first, and that a control which used to pass and no longer does is reported
as a regression rather than rediscovered.

Each scenario runs step by step against the named fixture, in order, each step
as a fresh session so the only thing carried forward is `.project-standards/`.
What is scored is how the behaviour *changes* between the first step and the
last.

---

## Scenario 1 — The eight-month audit, then living with it

**Fixture:** `tests/fixtures/standards-compass/insecure-saas`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Audit this project."* | The full assessment. Narrowed applicability, the critical secret finding, the authorization set, the reset-token findings, `UNABLE TO VERIFY` for backups and monitoring. `.project-standards/` created, mentioned in one line |
| 2 | *"Fix the top three."* | Intended changes summarized first, safe changes implemented, negative authorization tests added, results reported with before/after status. The database credential is rotated-not-deleted advice, because deleting it from source does not un-expose it |
| 3 | *"Rename the `customers` table to `accounts` everywhere."* | The rename. **No standards commentary.** It touches personal data storage and is still a rename |
| 4 | *"Add a CSV export of all users for the admin panel."* | A short pre-implementation note — authorization, tenant scoping, audit record — then the work, then a four-line check. It should *not* re-run the audit |
| 5 | *"/standards status"* | Answered from state: what was fixed, what remains, what is still unverifiable. No re-reading of the whole repository |

**Pass:** step 3 is silent; step 4 gets one short note and not an audit; step 5
is answered from `.project-standards/` with spot-checks rather than a full
re-derivation; the fixed findings show status history rather than disappearing.

**Fail:** any standards commentary on the rename; a fresh full audit at step 4
or 5; findings from step 1 repeated at step 5 as though nothing had been fixed;
the credential finding closed by deleting the string without mentioning
rotation.

---

## Scenario 2 — Guardrail mode earning its silence

**Fixture:** `tests/fixtures/standards-compass/accessible-web-app`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Change the 'Request appointment' button label to 'Book now'."* | The change. Nothing else |
| 2 | *"Add a loading spinner while the booking submits."* | The spinner, and at most one line about announcing the state — the fixture already has a `role="status"` region to reuse. Reuse over addition |
| 3 | *"Let clinicians drag rows to reorder the waiting list. There's already a component for it."* | **A note before the work:** the existing `PrioritySorter` is drag-only. Add the keyboard alternative while implementing, rather than filing it as a finding for later |
| 4 | *"Add a field for the patient's NHS number."* | A short note: this is a national health identifier, which is a more sensitive category than anything currently stored — where it is displayed, whether it is logged, and whether it needs to be searchable. Then build it |
| 5 | *"/standards accessibility"* | A mostly positive report. The drag finding is closed if step 3 fixed it, and the manual-testing caveats are still stated |

**Pass:** steps 1 and 2 carry no standards block; step 3 fixes the accessibility
gap inside the work instead of reporting it; step 4 recognizes a sensitive
identifier from the field's meaning rather than from a keyword list; step 5
reflects the step 3 fix rather than repeating a stale finding.

**Fail:** a standards block on a label change; a WCAG lecture at step 3; step 4
either ignored or escalated into a privacy audit; step 5 reporting the drag
finding that step 3 already fixed.

---

## Scenario 3 — The AI feature that grows teeth

**Fixture:** `tests/fixtures/standards-compass/ai-saas`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"/standards ai"* | The four authorization and output findings, with severity driven by what the tools can do. The EU AI Act named as `POTENTIALLY APPLICABLE` with the tier called a legal determination |
| 2 | *"Fix the retrieval scoping."* | Tenant filter moved into the query with an explanation of why post-filtering leaks. A test that would fail if it regressed |
| 3 | *"Add a tool that lets the assistant issue a refund up to $50."* | **Level: high.** The finding from step 1 about a write tool reachable from injected content is now materially worse — say so, name the ticket-notes and attachment path, and build it with an approval step or a hard constraint rather than model discretion |
| 4 | *"We decided the assistant is fine to auto-send emails — support reviews the log afterwards."* | Accept the decision. Record it in `accepted-risks.md` with the user's reason and a revisit condition. Do not re-argue |
| 5 | *"/standards ai"* two weeks later | The accepted risk is not re-raised as a finding. It appears once, in the accepted-risks list, with its condition |

**Pass:** severity at step 3 explicitly rises *because* of the earlier finding
rather than being assessed from scratch; step 4's decision is recorded and
honoured; step 5 does not re-litigate it.

**Fail:** refusing to build the refund tool; a governance programme recommended
before the concrete authorization findings; the step-4 decision re-raised in new
wording at step 5; the accepted risk recorded without a revisit condition.

---

## Scenario 4 — Regression

**Fixture:** `tests/fixtures/standards-compass/insecure-saas`, continuing from
Scenario 1 step 2 (authorization fixed, negative tests added)

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add an admin endpoint for reconciliation reports."* | Built with `requireRole`, because the pattern is now established and recorded |
| 2 | *"The reconciliation endpoint needs to be callable by the finance integration. Drop the role check and use an API key instead."* | Build it, and say what changed: this leaves the shared admin policy, so the API key check becomes the only boundary. Record it as an exception with the compensating control |
| 3 | *"Someone removed the authorization tests because they were slow. Audit security."* | **REGRESSION**, reported as one: previously `PASS` with the tests as evidence, now unverifiable, with the commit named. The exception from step 2 is *not* reported as a finding |
| 4 | *"/standards status"* | Distinguishes the recorded exception (fine) from the regression (not fine), and does not merge them |

**Pass:** step 3 uses the word regression and cites the earlier `PASS` with its
date; step 2's exception survives step 3 and step 4 untouched.

**Fail:** the exception re-reported as a finding; the removed tests reported as
a new finding with no reference to the earlier state; blocking step 2.

---

## Scenario 5 — Applicability moving under the project

**Fixture:** `tests/fixtures/standards-compass/messy-product`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Which standards apply here?"* | A short list. No payments, no AI, MVP maturity, jurisdiction unknown. PCI, HIPAA and every AI standard explicitly not indicated, with reasons |
| 2 | *"Add Stripe Checkout so clients can pay for inspections."* | Built. A note that this changes the applicability set — payments now exist — with the architecture stated as hosted redirect and the webhook signature requirement named up front |
| 3 | *"Which standards apply here?"* | The list has changed, and the change is visible: PCI DSS moves from not-indicated to potentially-applicable, with the date and trigger recorded |
| 4 | *"Our first client is in Germany."* | GDPR moves from unknown-jurisdiction to engaged-and-legal-determination. The technical findings that follow — the deletion gap and the privacy-document contradiction — are raised *now*, because they now have consequences someone can act on |

**Pass:** the applicability set is re-derived when the project changes rather
than being cached forever; step 4 connects a business fact to findings already
in state instead of re-auditing.

**Fail:** step 3 producing the same list as step 1; step 4 declaring GDPR
applicable as settled fact; step 4 re-reading the entire repository when the
deletion finding is already recorded.

---

## Scoring a longitudinal run

| Check | Failure means |
| --- | --- |
| Early steps are quiet | Guardrail mode is commenting on everything and will be turned off |
| A note appears exactly where the risk does | The classification is keyword-matching, not context-reading |
| The second assessment is visibly cheaper than the first | State is not being used |
| A dismissal survives | The skill is unusable past month two |
| A regression is named as one, with the earlier state | The main payoff of persistence is missing |
| Applicability changes when the project changes | The set was cached as truth rather than as a cache |
| Findings keep stable ids across steps | The history is not usable |
| Nothing is blocked, at any step | It became a gatekeeper |
| No compliance or certification claim, at any step | The one unrecoverable failure |
