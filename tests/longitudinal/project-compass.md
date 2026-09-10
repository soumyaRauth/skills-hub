# Longitudinal scenarios — Project Compass

A single prompt cannot test this skill. Its whole claim is that it gets more
useful across sessions, which means the unit of measurement is a **sequence**,
not a request.

Each scenario below is run step by step against the named fixture, in order,
starting each step as a fresh session so the only thing carried forward is
`.project-compass/`. What is being scored is how the behavior *changes* between
step 1 and the last step.

Two things are scored at every step:

```
Did it stay quiet when there was nothing worth saying?
When it did speak, did it end in something to do next?
```

The expected behavior for early steps is almost always **nothing**. A run that
intervenes at step 2 has failed the scenario even if its observation is correct,
because the evidence was not there yet. And a run that lands the right
observation at the right step but stops at *"there is no lifecycle"* has failed
just as completely — the deliverable is the step that comes before the next
feature, not the diagnosis.

Modes: `A` build it, say nothing about direction · `B` build it, flag one thing ·
`C` pause, guide, offer to proceed as asked.

---

## Scenario 1 — The authorization model that assembled itself

**Fixture:** `tests/fixtures/project-compass/saas-admin`
(ships `.project-compass/` with five recorded entries and no blind spots)

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add an endpoint that lets managers export their org's ticket list."* | **A.** The endpoint. A trajectory entry. No commentary |
| 2 | *"Support should be able to reopen a closed ticket in any org."* | **A**, or at most **B**. The change, plus a recorded pattern instance — the contradiction is not yet forced |
| 3 | *"Add a `regional_manager` role that can approve refunds in its region."* | **C.** Seven permission decisions across four modules, named. The escalation path — an admin may set any role including `owner` (`members.js:changeRole`), and `owner` is the only role billing accepts (`billing.js:getInvoices`) — surfaced as a concrete consequence, not as "security concerns" |
| 4 | *"Why is authorization getting so complicated?"* | The answer already exists in state. Same locations, same conclusion, no re-derivation, no new investigation |

**Pass:** the intervention lands at step 3 or 4, names at least four real
locations, identifies that authorization is being defined at call sites rather
than as a rule, and **ends in the step**: answer four questions — subjects,
resources, actions, whether ownership outranks role — then route the seven
existing checks through the answer, before `regional_manager` becomes the
eighth. The `admin → owner → billing` path is the highest-value find; it is
reachable from the code alone.

**Fail:** intervening at step 1 or 2; a generic "you should use RBAC"; refusing
to add the role; a security lecture; failing to notice the escalation path;
re-reading the whole repository at step 4 when the state already holds the
answer; stopping at *"there is no authorization model"* with no step attached.

---

## Scenario 2 — Five fixes for a problem nobody measured

**Fixture:** `tests/fixtures/project-compass/performance-project`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"The monthly report endpoint feels slow. Can you make it faster?"* | Before optimizing: there is no timing anywhere. `lib/logger.js` logs method, path and status only; no APM dependency; no benchmark. Propose one measurement. Building something is acceptable only if it is the measurement |
| 2 | *"Just add Redis — the in-process cache doesn't survive deploys."* | **C.** The escalation is in `CHANGELOG.md`: timeout → retry → background job → cache, four changes since 12 August, no number attached to any of them. Recommend stage timing first — named, sized, no new dependencies — and offer to add Redis anyway |
| 3 | *"We profiled it last month off-repo. The query is the bottleneck."* | Accept immediately. Record it in `decisions.md`. Build the Redis change. Do not re-argue |
| 4 | *"Should we shard the reports table?"* | The dismissal from step 3 is honored — no repeat of the measurement point. A new observation is allowed only if it rests on new evidence |

**Pass:** the missing measurement is raised once, with the searches that
establish its absence named, and with a concrete measurement to run rather than
*"you should measure first"*; the user's step-3 statement closes it permanently.

**Bonus find:** `workers/queue.js` awaits the report promise inside the request,
so the "background job" from 3.1.0 never made anything asynchronous. Nothing in
the fixture states this — it is visible only by reading the code the changelog
claims fixed the problem.

**Fail:** repeating the measurement point after step 3, in any wording; adding
Redis at step 2 with no comment at all; refusing to add Redis; asserting the
missing `created_at` index as the cause rather than as a low-confidence guess;
recommending "profiling" with no named operation, stage, or cost estimate.

---

## Scenario 3 — Controls accumulating on one screen

**Fixture:** `tests/fixtures/project-compass/productivity-app`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add a 'due this week' quick filter to the task list."* | **A.** The filter. Nothing else |
| 2 | *"Let people save the filter as a view."* | **A.** Saved views already exist (`ui/SavedViews.jsx`). Extend them. Still nothing else |
| 3 | *"Add CSV export to the task list."* | **B**, delivered with the working export. Seven controls since July, from `CHANGELOG.md`; the three inconsistent field sets — filters offer four fields, saved views persist two, bulk updates three — are the concrete consequence. The step: one sentence naming who opens the screen and what they are finishing, before the eighth control |
| 4 | *"What should we do next?"* | Answered from the project: the workflow question, plus the observation that nothing in this app closes a task-shaped loop — no detail view, no comments, no completion path beyond a status column. Ranked, with something explicitly deprioritized |

**Pass:** silence at steps 1–2; at step 3 the export works *and* the field-set
inconsistency is named with its three locations *and* the next step has a trigger
attached; at step 4 the answer is ordered by trajectory rather than by category.

**Fail:** flagging at step 1; a generic "consider your information architecture";
recommending a redesign; proposing a solution instead of asking who the screen
is for; withholding the export at step 3; at step 4, a generic backlog.

**State check after step 3:** `direction.md` should now exist and should record
the crossing — *becoming a list/query management workflow* — with the evidence
and, if nothing was said, a `Not yet said` line stating the trigger. A run that
raises the same point again at step 4 without being asked has failed; a run that
has to re-derive it at step 4 has failed differently.

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
indecision. The declared frame is recorded once and inherited by step 4.

**Fail:** any suggestion that the user is thrashing; "you seem to be trying
several approaches"; premature architecture; counting the prototypes as drift at
step 4; recommending that they pick one before they have benchmarked.

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
| 1 | *"Rename `rec` to `reconciliation` in the reconcile module."* | **A.** The rename. Nothing recorded, nothing said |
| 2 | *"The variance should be red when it's negative, not just non-zero."* | **A.** The change |
| 3 | *"Add a loading state to the export button."* | **A.** The loading state. The export column set is the deferred blind spot — it stays deferred |
| 4 | *"Bump express to 4.19 and fix what breaks."* | **A.** The bump |
| 5 | *"What should I work on next?"* | Now it may speak, because it was asked. The export gap is fair to raise here as an answer, not as an interruption — and it comes with the step, not just the observation |

**Pass:** four consecutive requests with zero project commentary, including the
one that touches the deferred item.

**Fail:** any observation at steps 1–4, including a friendly one; *"this looks
fine from a project perspective"*, which is commentary wearing a smile; *"this
fits the current direction"* as an opener; a session-opening summary of the
project state.

---

## Scenario 6 — The model improving

**Fixture:** `tests/fixtures/project-compass/startup-mvp` (no
`.project-compass/`; `FORMING`)

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"What is this project?"* | A reconstruction, labeled. Invoicing for freelancers is `OBSERVED`; who it is for beyond that is `INFERRED`; the objective is `UNKNOWN` — the README describes something narrower than the schema. `project.md` is written |
| 2 | *"Add a 'mark as paid' button to the invoice view."* | Here the partial-payment contradiction is unavoidable: `recordPayment` sets `status = 'paid'` for any amount and carries a `TODO` asking the question, `Dashboard.jsx` treats `status === 'paid'` as settled, `InvoiceView.jsx` computes outstanding from `paid_cents`. **C**, with a default offered |
| 3 | *"I don't know what to work on."* | Four half-built things, each with a location: recurring schedules that nothing runs, a reminders worker wired to no scheduler, a portal route that never checks `portal_key`, a PDF button wired to nothing. Ordered, labeled, with what *not* to do, and with the missing objective stated as a limit on the answer |

**Pass:** the day-1 model is honest about what it does not know; by step 3 the
answer is specific to this repository and could not have been written about any
other, and its first item is startable today.

**Fail:** a generic backlog (*add tests, set up CI, improve error handling*);
inventing an objective, a customer, or a deadline; missing the unauthenticated
portal route, which is the one real security finding in the fixture; ordering the
answer by category so that the coding tasks outrank the decision three things
depend on.

---

## Scenario 7 — The project that became something else

**Fixture:** `tests/fixtures/project-compass/emerging-admin`

The headline behavior. Every request is legitimate, every one is in a different
part of the codebase, and the finding exists only in the sequence.

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add a region filter to the customer list."* | **A.** The filter. A trajectory entry tagged with the project's own vocabulary |
| 2 | *"Let a saved segment remember the region too."* | **A**, or at most **B**. `saved_segments` has columns for `plan` and `status` only, so this needs a migration — a fair moment to note that the persisted set has drifted from the offered set, and no more than that |
| 3 | *"Add bulk delete to the customer list."* | **B.** `customers.deleted_at` exists and `list` filters on it; a hard `DELETE` on selected rows contradicts that. One paragraph, and the step: pick one meaning of deleted before the bulk path ships |
| 4 | *"Add an audit log of admin actions."* | **C.** Three of *who / what / to whom / under what authority* have no single answer. The crossing is named — this is an administration console now, not a lookup page — with the three questions that close it, sized at about an hour |
| 5 | *"What should I do next?"* | Answered from `direction.md` without re-deriving the project. `owner_staff_id` — written by `customers.reassign`, absent from the schema — is reported as a separate live bug, near the top |

**Pass:** silence or near-silence through step 2; the crossing is named at step 4
and not before; the recommendation is three questions rather than an
authorization rewrite; the `owner_staff_id` bug is never folded into the
structural narrative.

**Fail:** flagging the pattern at step 1 or 2 — four instances are not there yet;
presenting a count (*"nine features since June"*) as the finding; "your
architecture is unclear"; recommending a permissions library; a security lecture
about the two permission paths; building the audit log at step 4 with no comment
at all; refusing to build it.

**State check:** after step 4, `direction.md` records `Becoming: staff
administration console` with locations and a date. After step 5 it should not
have been rebuilt from scratch.

---

## Scenario 8 — The interface running ahead of the workflow

**Fixture:** `tests/fixtures/project-compass/startup-mvp`

Tests the distinction the skill gets wrong most often: which UI request is worth
stopping for, and which is just a UI request.

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add a print stylesheet to the invoice view."* | **A.** The stylesheet |
| 2 | *"Put the outstanding total at the top of the dashboard."* | **A.** The change |
| 3 | *"Show the status and an outstanding warning on the invoice page."* | **A.** The change. Pattern recorded, nothing said |
| 4 | *"Move the invoice number next to the logo and make the status a coloured pill."* | **A.** Ten minutes, independently correct, bakes in nothing. Still nothing said |
| 5 | *"Let's add invoice templates — three designs, one per client."* | **C.** Five presentation changes; the get-paid loop has two broken steps. `Download PDF` at `ui/InvoiceView.jsx:13` is `onClick={() => {}}`, so three designs would be three designs nobody receives |

**Pass:** four silent steps, then a recommendation about **order** rather than a
criticism of the UI work; the break is named with its location; the
partial-payment decision is ranked *above* the PDF button because three things
depend on it (`Dashboard.jsx:3`, `InvoiceView.jsx:4`, `workers/reminders.js:7`);
a default is offered; templates are not refused.

**Fail:** intervening at step 4 — the cosmetic one is the trap; *"focus on core
functionality before more UI"* with no break named; treating every interface
request as evidence of a sequencing problem; refusing templates; failing to
notice that the reminders worker is attached to no scheduler.

---

## Scenario 9 — One more status

**Fixture:** `tests/fixtures/project-compass/order-system`

| Step | Request | Expected |
| --- | --- | --- |
| 1 | *"Add an `is_gift` flag to orders."* | **A.** A flag with no lifecycle implications. Recorded, nothing said |
| 2 | *"Show 'awaiting payment' on the order row when it isn't paid yet."* | **A.** Display logic over an existing boolean |
| 3 | *"Add a `pending_review` status for orders we want to hold."* | **C.** The problem is not the status. Four booleans with no `status` column, sixteen representable states, and pairs that already contradict: `cancel.js` ignores `is_shipped`, `ship.js` ignores `is_cancelled`, `refund.js` refunds a cancelled order. `notify.js` and `reports/revenue.js` disagree about what "complete" means |
| 4 | *"Fine, but I need the hold behaviour this week."* | Build it, on a stated default, recorded as reversible. Do not re-argue the lifecycle |

**Pass:** step 3 names the four locations, frames it as *"the problem isn't the
new status — there's no lifecycle"*, and recommends ten lines of states and legal
transitions before the fifth flag: half an hour, explicitly smaller than what it
prevents. Step 4 is honored immediately and the decision is recorded with its
reason.

**Fail:** implementing a fifth boolean at step 3 with no comment; proposing event
sourcing, a workflow engine, or a rewrite; "your design is wrong"; refusing;
raising the lifecycle again after step 4; flagging anything at step 1 or 2.

---

## Scoring a longitudinal run

| Check | Failure means |
| --- | --- |
| Early steps are silent | The bar is not being applied; the skill will be uninstalled in week two |
| The intervention lands at the step where evidence first supports it | Either trigger-happy, or not reading the sequence at all |
| Every intervention ends in a step someone could start today | It produced a diagnosis and handed the work back |
| The recommended step is smaller than the work it prevents | It is proposing a rewrite, which nobody will do |
| What the project has become is named where the evidence supports it | It is counting features rather than reading the sequence |
| Instances are named with locations | It is pattern-matching on vibes |
| A dismissal is permanent, in every later step | The single most important behavior in the skill |
| A stated goal — prototype, experiment, already decided — reframes every later answer | It is arguing with the user's own context |
| State is read, not re-derived, on later steps | The persistence is decorative |
| `direction.md` changes when the direction changes, and not otherwise | It is either a diary or a fossil |
| Nothing was invented — no goals, users, metrics, or history | The worst failure available |
| The answer changes as the project changes | It is a static prompt with a state directory attached |
