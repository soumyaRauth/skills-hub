# Longitudinal scenarios — Project Compass

A single prompt cannot test this skill. Its whole claim is that it gets more
useful across sessions, which means the unit of measurement is a **sequence**,
not a request.

Each scenario below is run step by step against the named fixture, in order,
starting each step as a fresh session so the only thing carried forward is
`.project-compass/`. What is being scored is how the behavior *changes* between
step 1 and the last step.

The expected behavior for early steps is almost always **nothing**. A run that
intervenes at step 2 has failed the scenario even if its observation is correct,
because the evidence was not there yet.

---

## Scenario 1 — The authorization model that assembled itself

**Fixture:** `tests/fixtures/project-compass/saas-admin`
(ships `.project-compass/` with five recorded entries and no blind spots)

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add an endpoint that lets managers export their org's ticket list."* | The endpoint. A trajectory entry. No commentary |
| 2 | *"Support should be able to reopen a closed ticket in any org."* | The change, plus a recorded pattern instance. At most a Level 1 nudge — the contradiction is not yet forced |
| 3 | *"Add a `regional_manager` role that can approve refunds in its region."* | **Level 2.** Seven permission decisions across four modules, named. The escalation path — an admin may set any role including `owner` (`members.js:changeRole`), and `owner` is the only role billing accepts (`billing.js:getInvoices`) — surfaced as a concrete consequence, not as "security concerns" |
| 4 | *"Why is authorization getting so complicated?"* | The answer already exists in state. Same locations, same conclusion, no re-derivation, no new investigation |

**Pass:** the intervention lands at step 3 or 4, names at least four real
locations, and identifies that authorization is being defined at call sites
rather than as a rule. The `admin → owner → billing` path is the highest-value
find; it is reachable from the code alone.

**Fail:** intervening at step 1 or 2; a generic "you should use RBAC"; refusing
to add the role; a security lecture; failing to notice the escalation path;
re-reading the whole repository at step 4 when the state already holds the
answer.

---

## Scenario 2 — Five fixes for a problem nobody measured

**Fixture:** `tests/fixtures/project-compass/performance-project`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"The monthly report endpoint feels slow. Can you make it faster?"* | Before optimizing: there is no timing anywhere. `lib/logger.js` logs method, path and status only; no APM dependency; no benchmark. Propose one measurement. Building something is acceptable only if it is the measurement |
| 2 | *"Just add Redis — the in-process cache doesn't survive deploys."* | **Level 2 or 3.** The escalation is in `CHANGELOG.md`: timeout → retry → background job → cache, four changes since 12 August, no number attached to any of them. Recommend timing by stage first; offer to add Redis anyway |
| 3 | *"We profiled it last month off-repo. The query is the bottleneck."* | Accept immediately. Record it in `decisions.md`. Build the Redis change. Do not re-argue |
| 4 | *"Should we shard the reports table?"* | The dismissal from step 3 is honored — no repeat of the measurement point. A new observation is allowed only if it rests on new evidence |

**Pass:** the missing measurement is raised once, with the searches that
establish its absence named; the user's step-3 statement closes it permanently.

**Bonus find:** `workers/queue.js` awaits the report promise inside the request,
so the "background job" from 3.1.0 never made anything asynchronous. Nothing in
the fixture states this — it is visible only by reading the code the changelog
claims fixed the problem.

**Fail:** repeating the measurement point after step 3, in any wording; adding
Redis at step 2 with no comment at all; refusing to add Redis; asserting the
missing `created_at` index as the cause rather than as a low-confidence guess.

---

## Scenario 3 — Controls accumulating on one screen

**Fixture:** `tests/fixtures/project-compass/productivity-app`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add a 'due this week' quick filter to the task list."* | The filter. Nothing else |
| 2 | *"Let people save the filter as a view."* | Saved views already exist (`ui/SavedViews.jsx`). Extend them. Still nothing else |
| 3 | *"Add CSV export to the task list."* | **Level 1**, delivered with the working export. Seven controls since July, from `CHANGELOG.md`; the three inconsistent field sets — filters offer four fields, saved views persist two, bulk updates three — are the concrete consequence |
| 4 | *"What should we do next?"* | Answered from the project: the workflow question, plus the observation that nothing in this app closes a task-shaped loop — no detail view, no comments, no completion path beyond a status column |

**Pass:** silence at steps 1–2; at step 3 the export works *and* the field-set
inconsistency is named with its three locations.

**Fail:** flagging at step 1; a generic "consider your information architecture";
recommending a redesign; proposing a solution instead of asking who the screen
is for.

---

## Scenario 4 — Deliberate exploration, which is not drift

**Fixture:** any. `startup-mvp` is the sharpest, because it looks messy.

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"I want to try three approaches to the PDF export — server-side, client-side, and a hosted service. Throwaway code is fine."* | Help. Record `EXPLORATORY` for that area. No architecture advice |
| 2 | *"Try the client-side one differently — see if it handles the logo better."* | Help. Still no drift signal |
| 3 | *"Benchmark all three on a 40-page invoice."* | Help. Make the comparison sharper — same input, same measure, and name what would decide it |
| 4 | *"What should I do next?"* | The exploration is acknowledged as deliberate. Direction is answered from the *rest* of the project, and the three prototypes are not counted as churn |

**Pass:** nothing in the run treats steps 1–3 as accumulation, escalation, or
indecision.

**Fail:** any suggestion that the user is thrashing; "you seem to be trying
several approaches"; premature architecture; counting the prototypes as drift at
step 4.

**Then:** *"actually let's add page numbers to the client-side one, and a cover
page"* — the throwaway is being extended. One line is now correct: the spike has
become the implementation, and it was built to be discarded.

---

## Scenario 5 — Silence under provocation

**Fixture:** `tests/fixtures/project-compass/directed-project`
(ships `.project-compass/` containing a **deferred** blind spot and an
*Accepted — do not raise again* decision)

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Rename `rec` to `reconciliation` in the reconcile module."* | The rename. Nothing recorded, nothing said |
| 2 | *"The variance should be red when it's negative, not just non-zero."* | The change |
| 3 | *"Add a loading state to the export button."* | The loading state. The export column set is the deferred blind spot — it stays deferred |
| 4 | *"Bump express to 4.19 and fix what breaks."* | The bump |
| 5 | *"What should I work on next?"* | Now it may speak, because it was asked. The export gap is fair to raise here as an answer, not as an interruption |

**Pass:** four consecutive requests with zero project commentary, including the
one that touches the deferred item.

**Fail:** any observation at steps 1–4, including a friendly one; *"this looks
fine from a project perspective"*, which is commentary wearing a smile; a
session-opening summary of the project state.

---

## Scenario 6 — The model improving

**Fixture:** `tests/fixtures/project-compass/startup-mvp` (no
`.project-compass/`; `FORMING`)

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"What is this project?"* | A reconstruction, labeled. Invoicing for freelancers is `OBSERVED`; who it is for beyond that is `INFERRED`; the objective is `UNKNOWN` — the README describes something narrower than the schema. `project.md` is written |
| 2 | *"Add a 'mark as paid' button to the invoice view."* | Here the partial-payment contradiction is unavoidable: `recordPayment` sets `status = 'paid'` for any amount and carries a `TODO` asking the question, `Dashboard.jsx` treats `status === 'paid'` as settled, `InvoiceView.jsx` computes outstanding from `paid_cents`. **Level 2**, with a default offered |
| 3 | *"I don't know what to work on."* | Four half-built things, each with a location: recurring schedules that nothing runs, a reminders worker wired to no scheduler, a portal route that never checks `portal_key`, a PDF button wired to nothing. Ordered, labeled, with what *not* to do, and with the missing objective stated as a limit on the answer |

**Pass:** the day-1 model is honest about what it does not know; by step 3 the
answer is specific to this repository and could not have been written about any
other.

**Fail:** a generic backlog (*add tests, set up CI, improve error handling*);
inventing an objective, a customer, or a deadline; missing the unauthenticated
portal route, which is the one real security finding in the fixture.

---

## Scoring a longitudinal run

| Check | Failure means |
| --- | --- |
| Early steps are silent | The bar is not being applied; the skill will be uninstalled in week two |
| The intervention lands at the step where evidence first supports it | Either trigger-happy, or not reading the sequence at all |
| Instances are named with locations | It is pattern-matching on vibes |
| A dismissal is permanent, in every later step | The single most important behavior in the skill |
| State is read, not re-derived, on later steps | The persistence is decorative |
| Nothing was invented — no goals, users, metrics, or history | The worst failure available |
| The answer changes as the project changes | It is a static prompt with a state directory attached |
