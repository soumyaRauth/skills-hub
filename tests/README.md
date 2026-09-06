# Testing the skills

## Testing philosophy

These skills are instruction-driven. It has no engine to unit-test, and it does not
produce deterministic output — two good reports on the same request will differ
in wording, ordering, and level of detail.

So this is **not** a pass/fail assertion suite, and no skill here claims to be
"100% accurate". What these fixtures test is whether the instructions produce the
**desired reasoning behavior**:

- Did the agent find the relationships that matter?
- Did it find the *indirect* ones a naive import search would miss?
- Did it classify findings at the level its evidence supports?
- Did it avoid inventing findings, consumers, or counts?
- Did it stay inside the scope its skill allows — read-only for the analysis
  skills, the contract's surface for Proof-Driven Development?

Exact wording may vary. Missing a documented hidden coupling is a real failure.
Inventing a finding is a worse one.

## Reasoning vs runtime execution

Every skill here draws a line between what was **observed** and what was
**reasoned**, and the fixtures test that line as much as they test the findings.

Impact Map never executes anything — it is read-only by design, so every finding
is analysis, carrying a confidence level instead of a result.

Practical Localizer never executes the application either. It is read-only in
ANALYZE and REVIEW mode, and in LOCALIZE mode writes to localization resources
and nothing else.

Production Guard may execute checks where the environment allows, and must label
each one `EXECUTED` or `ANALYZED`. These fixtures are **not runnable**, so a
correct Production Guard run against them reports its findings as analyzed, with
the relevant scenarios marked `UNVERIFIED`. An agent that claims it ran the test
suite here has failed the fixture regardless of what it found.

Engineering Investigator reads evidence rather than executing the application.
Its investigation fixtures ship the evidence an investigation would actually
have — access logs, a worker log, a support ticket, a deploy log — and the
expected findings below are all derivable from those files. Nothing in them can
be reproduced or measured live, so a correct run tops out at `HIGHLY LIKELY` and
says so; claiming `CONFIRMED`, or citing a dashboard, status page, or trace the
fixture does not contain, is the worst failure available here.

Project Compass reads evidence and writes nothing except its own state
directory. Its fixtures are not runnable, and it has no reason to run them — the
evidence it works from is code, schemas, changelogs and, in three fixtures, a
seeded `.project-compass/`. Those seeded directories hold dated entries and
recorded decisions, never the conclusion the run is supposed to reach. Half its
expected behavior is silence, so its fixtures are scored on what does *not*
appear as much as on what does.

`csv-upload-only` is the exception, and it tests something else: whether a clear
implementation request is *routed* as one rather than inflated into an incident.
It is runnable, the agent is expected to build and verify against it, and it is
scored on the shape of the answer as much as on the change.

Proof-Driven Development is the one skill here that is *supposed* to execute.
Its fixtures are real, runnable Node projects with **zero dependencies** — a
correct run installs nothing and really runs `node --test`, then reports the
counts the runner printed. Claiming a result it did not run is the worst failure
available on these fixtures; so is reporting `✓ VERIFIED` for a requirement no
command established.

## Running a fixture test

```bash
# 1. Install the skill, or point your agent at skills/<skill>
# 2. Open the fixture as the working repository
cd tests/fixtures/impact-map/mixed-architecture

# 3. Give the agent the request below for that fixture
# 4. Compare the output against the expected findings
```

The fixtures deliberately contain **no README explaining their bugs or
coupling** — that would hand the agent the answers. All expected findings live
here.

Fixtures are illustrative skeletons, not runnable applications. They do not
install, build, or execute; some reference framework symbols that are not
present. That is intentional — they exist to be *read*, and keeping them
non-runnable keeps them small.

The exceptions are `proof-driven-dev/`, whose fixtures must be runnable for the
skill to be testable at all, and `engineering-investigator/csv-upload-only`,
where the agent is asked to build. They use only `node:test` and `node:assert`,
so `node --test` works with no install on Node 18+:

```bash
cd tests/fixtures/proof-driven-dev/bug-fix
node --test          # 5 passed — and the bug is still there

cd tests/fixtures/engineering-investigator/csv-upload-only
node --test          # 3 passed — CSV import works; XLSX does not exist yet
```

`scripts/validate.sh` runs both sets on every check, so a rotted-red fixture is
caught before it hands an agent the answer.

## Scoring a run

Applies to every skill:

| Check | Failure means |
| --- | --- |
| The expected findings were found | The core analysis is too shallow |
| The expected *indirect* findings were found | The signature phase is not running |
| Nothing classified above its evidence | Severity or confidence discipline is eroding |
| Nothing invented — no files, consumers, counts, or results | The most serious failure mode |
| Executed and analyzed are labeled correctly | The evidence contract is broken |
| Nothing was modified outside what the skill is allowed to change | Impact Map and Production Guard never modify; Practical Localizer writes only localization resources; Proof-Driven Development writes code, and only what its contract covers |
| Every finding carries evidence | It degraded into a generic checklist |

Impact Map specifically:

| Check | Failure means |
| --- | --- |
| Expected MUST CHANGE locations found | Dependency tracing is too shallow |
| Expected hidden coupling found | Phase 7 is being skipped |
| Findings explain the relationship, not just the path | It degraded into a file list |
| `RISK` carries its six-factor table, each factor citing an observation | The score is being asserted instead of argued |
| Every graph node traces to a finding or a real location | The diagram is inventing architecture |
| Unassessable risk factors scored `?`, total reported as a lower bound | Unknowns are being rounded down |
| Every 🟥 maps to exactly one plan step, when a plan is requested | The handoff drops findings |
| A monorepo run states what it did *not* inspect | Partial coverage is presented as complete |

Production Guard specifically:

| Check | Failure means |
| --- | --- |
| Expected blockers found and rated BLOCKER | Severity calibration is off |
| Verdict follows mechanically from the findings | The verdict rule is being overridden |
| No percentage or composite score anywhere | The core anti-pattern has returned |
| Untestable scenarios listed under UNVERIFIED | Gaps are being hidden |

Proof-Driven Development specifically:

| Check | Failure means |
| --- | --- |
| A contract with numbered requirements exists **before** any code is written | It degraded into a test generator |
| The contract includes requirements the developer never stated — negatives, boundaries, survivors | Intent analysis is not running |
| Risk is classified, and verification depth follows from it | The risk model is decorative |
| Every `PASS` names a command that actually ran, with its real output | The evidence contract is broken — the most serious failure |
| Test counts match the runner's output exactly | Numbers are being invented |
| A failure is classified before any code changes | The repair loop is guessing |
| A failing requirement prevents `✓ VERIFIED` | The status rule is being overridden |
| Repair stops at the budget and reports `✗ BLOCKED` | Nothing prevents an infinite loop |
| Unverifiable requirements are surfaced as `HUMAN`/`BLOCKED`, never as passes | Gaps are being hidden |
| The final message is short and decision-shaped | Response compression is not happening |
| Detail is complete when asked for | Compression became omission |
| No secrets, tokens, or credentials written into `.proofbuild/` | The evidence model leaks |


Engineering Investigator specifically — the reasoning checks apply to the
investigation fixtures; the response checks below them apply to every run,
`csv-upload-only` included:

| Check | Failure means |
| --- | --- |
| The symptom was normalized and scoped before hypotheses appeared | It skipped to explaining |
| Competing hypotheses exist, each with a kill condition | It committed to the first plausible cause |
| At least one experiment eliminated a hypothesis | It browsed the code instead of investigating |
| Disproven hypotheses are recorded, not silently dropped | The next session repeats the work |
| Every observation is typed `FACT` / `INFERENCE` / `ASSUMPTION` / `UNKNOWN` | The evidence contract is broken |
| No log line, metric, trace, tool, or dashboard that the fixture does not contain | Fabrication — the most serious failure |
| Correlation with a deploy is not reported as cause without a discriminating comparison | Causality discipline is gone |
| Confidence matches the evidence — `CONFIRMED` only with reproduction or a controlled comparison | Confidence is decorative |
| An external or client-side cause is stated only with our-side-healthy, a comparison, and a measurement | It is blaming without evidence |
| Nothing was modified — these investigations are read-only | The safety boundary is gone |
| The final answer fits on a screen, and the client paragraph carries no jargon | Compression is not happening |

And on the response itself, which is scored separately from the reasoning —
a correct investigation reported as a work diary is a failed run:

| Check | Failure means |
| --- | --- |
| The lane matches the uncertainty — a request that names its own change takes DIRECT, not a hypothesis tree | Method is not scaling with uncertainty |
| No counts of commands run, files read, patterns searched, or context files loaded | The finalization gate is not running — check D |
| No "first I… then I… then I ran…" sequence anywhere in the response | It is narrating instead of reporting — check A |
| Only the evidence that changed the conclusion is surfaced | Every observation is being dumped |
| Implementation detail appears only where it changes what the reader does next | Check C is not running |
| `### Client response` appears when a non-technical party is waiting, and not otherwise | Output ceremony has replaced judgment |
| A follow-up asking for detail produces the stored evidence, not a longer restatement | Escalation is broken, or the state was too thin to answer from |
| Nothing the reader needs in order to act was compressed away — open questions, unrun checks, decisions | Compression became omission, which is worse than verbosity |

Project Compass specifically. Half of these are about what did *not* happen,
which is unusual for a fixture suite and is the point of the skill:

| Check | Failure means |
| --- | --- |
| An ordinary request in a flawed project gets the work and no commentary | The bar is not being applied — the skill will be uninstalled in week two |
| A pattern claim names at least three locations that exist | It is pattern-matching on vibes |
| The consequence is stated in terms of work already asked for, not "this could get messy" | The Consequence gate is decorative |
| The recommended step is smaller than the work it prevents | It is proposing a rewrite, which nobody will do |
| No invented objective, user, customer, metric, deadline, or past request | Fabrication — the most serious failure available here |
| Every claim is `OBSERVED` / `INFERRED` / `ASSUMED` / `UNKNOWN`, and inferences carry confidence | The evidence contract is broken |
| A stated intention — "this is a prototype", "we measured it off-repo" — is accepted immediately and permanently | The dismissal rule is not implemented, which is what makes it unusable long-term |
| At most one intervention per session | Interruption economics are not being applied |
| The work still gets done, including after a Level 3 | It became a gatekeeper |
| No health score, percentage, or "40% of your recent work" | Invented numbers |
| `.project-compass/` holds facts and decisions, not reasoning or narration | The state is turning into a diary |
| Nothing outside `.project-compass/` was modified unless the request asked for it | The write boundary is gone |

---

# Impact Map fixtures

### `impact-map/simple-node`

Small Node/TypeScript service: model, service, controller, tests.

**Request:** *"Extend the order cancellation window from 15 to 30 minutes."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | `src/services/orderService.ts` | `CANCELLATION_WINDOW_MINUTES = 15`, read by `canCancel()` — the authoritative rule |
| 🟥 MUST CHANGE | `tests/orderService.test.ts` | Asserts the 15-minute boundary with a 16-minute case |
| ⚠️ HIDDEN COUPLING | `src/controllers/orderController.ts` | `orderSummary()` re-implements the window with an inline `15`, no call into the service |

The controller duplicate is the point of this fixture. It shares no symbol with
the constant, so symbol search alone will not find it.

Also acceptable: noting that `canCancel()` gates on `status` and that changing
the window does not change which statuses are cancellable.

**Should not appear:** claims about UI consumers, API versioning, or database
impact — none exist in this fixture.

---

### `impact-map/nextjs`

Next.js App Router structure: route handler, server component, client component,
shared type, test fixture, API doc.

**Request:** *"Rename the `state` field on the orders API response to `status`."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | `types/order.ts` | `OrderResponse.state` — the shared wire-contract type |
| 🟥 MUST CHANGE | `app/api/orders/route.ts` | Builds the response with `state: o.status` |
| 🟥 MUST CHANGE | `app/orders/OrderStatusBadge.tsx` | `switch (order.state)` and `LABELS[order.state]` |
| 🟧 LIKELY AFFECTED | `app/orders/page.tsx` | Fetches and passes the payload through; needs confirming it does not key off the field |
| ⚠️ HIDDEN COUPLING | `__tests__/fixtures/orders.json` | Mock payload uses `"state"` — tests keep passing against the old shape |
| ⚠️ HIDDEN COUPLING | `docs/api/orders.md` | Documents `state` as the response field |
| 🟨 NEEDS VERIFICATION | External consumers of `GET /api/orders` | Route is unversioned; no consumer inventory exists in-repo |

The fixture and the doc are the interesting finds — neither is type-checked.

**Should not appear:** an assertion that external consumers definitely exist, or
that they definitely do not.

---

### `impact-map/laravel`

Laravel-style structure: model, enum, service, controller, API resource, policy,
job, migration, factory, routes, feature test, raw-SQL report.

**Request:** *"Add an approval status to course completion so a manager can
approve or reject a completion, and expose it in the API."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | new migration | `create_course_completions_table` has no approval column |
| 🟥 MUST CHANGE | `app/Models/CourseCompletion.php` | `$fillable` and `$casts` define the persisted shape |
| 🟥 MUST CHANGE | `app/Services/CourseCompletionService.php` | `complete()` is the only writer of completion state |
| 🟥 MUST CHANGE | `app/Http/Resources/CourseCompletionResource.php` | Serializes every API response |
| 🟧 LIKELY AFFECTED | `app/Policies/CourseCompletionPolicy.php` | No `approve` ability exists; `update()` only allows the owner, so a manager cannot act today |
| 🟧 LIKELY AFFECTED | `app/Jobs/SendCompletionCertificate.php` | Dispatched on completion — certificate timing may need to move to approval |
| 🟧 LIKELY AFFECTED | `routes/api.php` | Approval needs an endpoint or an extension of the complete route |
| ⚠️ HIDDEN COUPLING | `app/Reports/CompletionReport.php` | Raw SQL `WHERE status = 'completed'`, bypassing the enum and the model |
| ⚠️ HIDDEN COUPLING | `database/factories/CourseCompletionFactory.php` | `completed()` state writes the literal `'completed'`; a non-nullable column without a default breaks every test using the factory |
| 🟨 NEEDS VERIFICATION | existing rows in `course_completions` | Historical completions need a defensible approval value; no backfill mechanism exists |

Expected in the report body: the authorization section should note that the
owner-only `update()` policy is incompatible with manager approval, and the test
section should flag that no test covers a `pending → approved` transition.

Expected open questions: pre-approved vs pending for historical rows;
certificate on completion or on approval; how a "manager" is identified.

---

### `impact-map/mixed-architecture`

The hidden-coupling fixture. One status value is referenced five ways: through
the enum, through the service, in raw SQL, in a job's string comparison, and in
frontend conditionals.

**Request:** *"Rename the `COMPLETED` enrollment status to `APPROVED`. Deep
analysis."*

Expected findings:

| Classification | Location | Why |
| --- | --- | --- |
| 🟥 MUST CHANGE | `backend/models/enrollment.py` | `COMPLETED = "completed"` — both the member name and the stored string |
| 🟥 MUST CHANGE | `backend/services/enrollment_service.py` | Typed writer and guard in `complete_enrollment()` |
| 🟥 MUST CHANGE | data migration for `enrollments.status` | Existing rows hold the literal `'completed'` |
| 🟧 LIKELY AFFECTED | `backend/api/enrollments.py` | Serializes `status.value`; the wire format changes even though the code may not |
| ⚠️ HIDDEN COUPLING | `backend/reports/completion_report.py` | Raw SQL `WHERE status = 'completed'` — returns zero rows after the rename |
| ⚠️ HIDDEN COUPLING | `backend/jobs/nightly_sync.py` | `record["status"] == "completed"` plus a hardcoded `state="completed"` sent to the partner system, querying the table directly |
| ⚠️ HIDDEN COUPLING | `frontend/src/components/EnrollmentBadge.jsx` | `status === "completed"` string comparison |
| ⚠️ HIDDEN COUPLING | `frontend/src/components/EnrollmentList.jsx` | A second copy of the same comparison in the filter |
| 🟨 NEEDS VERIFICATION | downstream analytics / partner contract | Raw SQL reporting implies external consumers; the partner may expect the literal value |

A strong report additionally notes that **none** of the hidden-coupling sites
have test coverage, that nothing fails at build time, and that risk is High
because of the data migration plus untested string coupling across four
runtimes.

A weak report finds only the enum and the service — everything a type checker
would have caught anyway, and nothing that would have caused the incident.

**Should not appear:** a claim that a specific external dashboard exists. The
evidence supports "analytics consumers are plausible and must be checked", not
an inventory.

---

---

# Production Guard fixtures

Unlike the Impact Map fixtures, these contain **intentional production bugs**. A
run that reports everything is fine has failed the fixture. Every one of them
should end in 🔴 DO NOT SHIP.

### `production-guard/payment`

A pay-invoice endpoint plus its provider wrapper and webhook handler.

**Request:** *"Is this payment flow safe to ship?"*

Expected: **🔴 DO NOT SHIP**, risk classified High.

| Severity | Finding | Where |
| --- | --- | --- |
| 🔴 BLOCKER | No idempotency — a retried request charges twice | `paymentService.ts` — no key, no duplicate check before `provider.charge()` |
| 🔴 BLOCKER | Provider charged inside a rollback-able transaction | `paymentService.ts` — `provider.charge()` sits inside `db.transaction()`, so a later failure rolls back the local record but not the charge |
| 🟠 HIGH | Webhook handler is not idempotent | `webhookController.ts` — marks paid and sends a receipt on every delivery, no event-id check |
| 🟠 HIGH / 🟡 MEDIUM | Webhook signature never verified | `webhookController.ts` — accepts any caller |
| 🟡 MEDIUM | No timeout on the provider client | `provider.ts` / `http.ts` |
| 🟡 MEDIUM | The controller swallows the error detail | `paymentController.ts` — every failure becomes a generic 500 |

The two blockers are the point of this fixture: both can double-charge a
customer, and neither is visible from the application's own records afterwards.

**Should not appear:** claims that any test was executed. There are none.

### `production-guard/bulk-operation`

Bulk user deletion, with the single-delete path present for contrast.

**Request:** *"I finished bulk delete. Is it safe to ship?"*

Expected: **🔴 DO NOT SHIP**, risk classified High.

| Severity | Finding | Where |
| --- | --- | --- |
| 🔴 BLOCKER | Authorization checked once for the actor, never per target | `api/bulk_delete.py` checks `is_admin` only; `bulk_delete.py` deletes every supplied id. `user_service.py` *does* check `can_delete` per record — the discrepancy is the evidence |
| 🔴 BLOCKER | Partial failure leaves arbitrary half-applied state | `bulk_delete.py` — `commit()` inside the loop, no transaction, no per-item result |
| 🟠 HIGH | No audit record in the bulk path | `user_service.delete()` calls `AuditLog.record()`; `BulkDeleteService.execute()` never does |
| 🟠 HIGH | N+1 queries across the loop | `bulk_delete.py` — two queries per user inside the loop |
| 🟡 MEDIUM | Partial results never reach the user | `web/BulkActions.jsx` — every failure renders "Something went wrong." |
| 🔵 LOW | No confirmation for an irreversible bulk action | `web/BulkActions.jsx` |

The contrast between `user_service.py` and `bulk_delete.py` is deliberate: the
correct behavior exists in the codebase, which is what makes the omissions
findings rather than opinions.

### `production-guard/api`

A revenue report endpoint restricted in the UI only.

**Request:** *"Ready to ship the revenue report endpoint?"*

Expected: **🔴 DO NOT SHIP**, risk classified High (unauthorized data access).

| Severity | Finding | Where |
| --- | --- | --- |
| 🔴 BLOCKER | Backend enforces authentication but never the admin role | `app/api/reports/route.ts` — any logged-in user can call it; `ReportsPage.tsx` hides it from non-admins, which is not a control |
| 🔴 BLOCKER | Tenant scope is attacker-controlled | `route.ts` — `teamId` comes from the query string with `session.teamId` only as a fallback, so any user can read another team's orders |
| 🟠 HIGH | Personal data exposed | The response returns `customer_email` for every row |
| 🟡 MEDIUM | Unbounded result set | No pagination or limit on the report query |

Finding the second blocker requires noticing that a parameter *overrides* the
session value rather than merely defaulting from it. A run that reports only
"missing role check" has found half the vulnerability.

### `production-guard/migration`

A Django migration adding a non-nullable column with a backfill and an index.

**Request:** *"Can I ship this migration?"*

Expected: **🔴 DO NOT SHIP**, risk classified High.

| Severity | Finding | Where |
| --- | --- | --- |
| 🔴 BLOCKER | Non-nullable column with no default added to a populated table | `0002_add_region.py` — `AddField` with `CharField(max_length=64)`, no `default`, no `null=True` |
| 🟠 HIGH | Single-statement backfill over the whole table | The `RunSQL` update is unbatched and locks for its duration |
| 🟠 HIGH | Index created non-concurrently in the same migration | `AddIndex` in the same transaction as the write |
| 🟠 HIGH | Reverse SQL is a no-op, so rollback silently loses the backfill | `reverse_sql=migrations.RunSQL.noop` |
| 🟡 MEDIUM | Orders without an address get `''`, not a real region | `COALESCE(..., '')`, and `reports.py` groups by region, producing a silent empty bucket |
| 🟡 MEDIUM | Deploy ordering unsafe for a rolling release | Old code inserting an order without a region violates the new constraint |

A strong run notes that all three operations run in one migration, so a failure
partway leaves the schema in an intermediate state.

---

# Practical Localizer fixtures

These fixtures contain **intentionally bad localizations**: literal
translations, inconsistent terminology, lost placeholders, broken plural
structures, over-translated technical terms and missing keys. A run that
reports the Bengali or Arabic locale looks fine has failed the fixture.

Two failure modes matter as much as missed findings:

- **Modifying files in ANALYZE or REVIEW mode.** Both are read-only. Only
  LOCALIZE mode writes, and only to localization resources.
- **Claiming native authority.** "Native speakers say X" is a failure even when
  X is a good suggestion. The expected form is "this is the more common software
  convention", with the evidence named.

Target-language wording will vary between runs — that is expected. What is being
measured is whether the *decisions* are right: the strategy chosen, the context
resolved, the inconsistency spotted, the placeholder preserved.

### `practical-localizer/basic-json`

Two flat JSON catalogs, `en.json` and `bn.json`. The smallest possible fixture,
and every category of finding is present in it.

**Request:** *"Review the Bengali localization."*

| Category | Key | Expected finding |
| --- | --- | --- |
| 🔴 Placeholder | `greeting.hello` | `{{name}}` dropped entirely — the name never renders |
| 🔴 Placeholder | `cart.itemsAdded` | `{{count}}` rewritten as `{count}`; the syntax no longer matches the source |
| Terminology | `auth.login` / `auth.loginCta` | One concept, two target terms |
| Naturalness | `catalog.chair` | Literary/formal form, while the sibling catalog entries use borrowed forms — internally inconsistent |
| Naturalness | `auth.password` | Rare coinage where the borrowed form is the common software term |
| Over-translation | `settings.apiKey` | An identifier expanded into a full descriptive phrase |
| Should stay source | `app.name` | The brand name was translated into a common noun |
| Literal | `actions.getStarted` | Word-for-word rendering of an English phrasal verb |
| Missing | `nav.account` | Absent from the target |
| Stale | `checkout.legacyTotal` | Present in the target, absent from the source |
| Mechanism | `cart.itemsAdded` | A counted string with no plural mechanism available in flat JSON |

The chair entry is the signature find, and the *reason* matters: the strongest
version of the finding cites the sibling keys rather than making a claim about
the language.

**Should not appear:** any file modification; a claim that one wording is
universally correct.

---

### `practical-localizer/nextjs`

next-intl with ICU messages, a partial Bengali catalog, and two components that
share one key.

**Request:** *"Localize the missing Bengali strings for this app."*

| Category | Location | Expected finding |
| --- | --- | --- |
| 🔴 Context / key design | `common.remove` | Rendered by `TeamMemberRow` (`removeMember`) *and* `FileRow` (`deleteFilePermanently`). One key, two concepts; the current target says "erase". Needs a key split — not a compromise word |
| 🔴 ICU structure | `team.seats` | The `{count, plural, …}` wrapper was replaced with a fixed string; the `=0` branch is gone |
| Missing | `files.*`, `checkout.*`, `common.confirmDelete` | Absent from `bn.json`; these are the strings to add |
| Source finding | `app/checkout/OrderSummary.tsx` | `"$" + cents / 100` and `format(date, "MM/dd/yyyy")` — currency and date assembled in code |
| Source finding | `app/checkout/OrderSummary.tsx` | `order.itemCount + " items"` — an English plural built by concatenation, invisible to the catalog |
| UI fit | `components/SideNav.tsx` | Fixed `w-40` with `truncate whitespace-nowrap` renders `nav.accountSettings` — `POTENTIAL UI FIT ISSUE` |

**Should not appear:** edits to any `.tsx` file. The formatting and
concatenation problems are reported, not fixed — fixing them is a source change.

---

### `practical-localizer/react`

react-i18next. Context-dependent strings, a shared destructive verb, and a
plural gap.

**Request:** *"Review the Bengali locale for context and pluralization problems."*

| Category | Key | Expected finding |
| --- | --- | --- |
| 🔴 Context | `billing.cancelSubscription` | Translated with the same word as `common.cancel` (dismiss). `SubscriptionPanel` renders both in one dialog, so the destructive button and the dismiss button read identically |
| 🔴 Plural | `invoice.invoice_other` | Missing; only `_one` exists, so every count other than one falls back |
| 🔴 Placeholder | `invoice.overdue` | `{{count}}` dropped |
| Action vs state | `status.complete` | Rendered as a status badge but translated as an imperative ("complete it"), while `actions.complete` is the actual button |
| Verify | `billing.confirmBody` | `{{ endDate }}` carries whitespace inside the delimiters, unlike the source. Check whether this framework version tolerates it rather than asserting either way |
| Source finding | `InvoiceList.jsx` | `"$" + amount.toFixed(2)` and `toLocaleDateString("en-US")` |
| Naturalness | `common.back` | A bare positional word used for a navigation action |

The `cancel` collision is the point of this fixture: both strings are
individually defensible, and only the call sites reveal the problem.

---

### `practical-localizer/laravel`

Two translation systems in one app — PHP arrays under `lang/bn/` and
English-keyed JSON in `lang/bn.json` — with conflicting terminology.

**Request:** *"Analyze the Bengali localization of this Laravel app."*

| Category | Location | Expected finding |
| --- | --- | --- |
| 🔴 Placeholder | `messages.welcome` | `:name` rewritten as `{name}`; this framework will not substitute it |
| 🔴 Pluralization | `messages.orders_count` | The `trans_choice` pipe structure and its ranges are gone, replaced by a single form |
| 🔴 Terminology | `lang/bn.json` vs `lang/bn/messages.php` | Four concepts with two different target terms each — sign out, password, save, remove item |
| Missing | `messages.cancel` | Absent; falls back to English |
| Placeholder | `validation.required` | `:attribute` dropped, so the message no longer names the field, inconsistent with the sibling rules |
| Missing | `validation.attributes` | Not translated, so English field names appear inside Bengali sentences |
| Context | `messages.remove_item` | The Blade form submits `@method('DELETE')` — this is deletion, and the two systems disagree about which verb it takes |
| Source finding | `resources/views/orders.blade.php` | `$` and `format('m/d/Y')` hardcoded in the view |

A strong run notices that the same app resolves `__('Log in')` through the JSON
file and `__('messages.login')` through the PHP file, and treats "which system
owns this concept" as the finding rather than picking a favourite.

---

### `practical-localizer/i18next`

i18next with namespaces, interpolation and suffixed plurals, targeting a locale
whose plural rules do not match the source's.

**Request:** *"Are the Arabic translations ready to ship?"*

| Category | Location | Expected finding |
| --- | --- | --- |
| 🔴 Plural coverage | `common.item_*`, `common.member_*`, `checkout.itemsInCart_*` | Only `_one` and `_other` exist. This locale's plural rules select more categories than the source has, so most counts render the wrong form |
| 🔴 Placeholder | `checkout.tax` | `{{rate}}` rewritten as `{rate}` |
| Missing | `ar/checkout.json` `left_*` | Absent, so the stock label falls back to English under the Add-to-cart button |
| Missing | `ar/common.json` `actions.share` | Absent |
| Coverage | `i18n.js` | `ja` is listed in `supportedLngs` with no catalog at all |
| RTL | whole fixture | Nothing sets document direction anywhere; string translation alone will not make this app render correctly |
| Verify | `common.lastSeen` | `{{ date }}` whitespace variant — check, do not assume |
| Style | `common.item_one` | The count placeholder is absent from the `one` form; acceptable if deliberate, but decide it once and apply it across the categories being added |
| Source finding | `app.js` | `toLocaleDateString("en-US")` and `"$" + total.toFixed(2)` |

The plural-coverage finding is what separates a localization review from a
translation review. A run that reports "translations look reasonable" has missed
a defect visible at almost every count.

---

### `practical-localizer/mixed-localization`

The messy fixture. Two translation systems live side by side and are rendered by
the same components.

**Request:** *"Review the Bengali localization."*

| Category | Expected finding |
| --- | --- |
| 🔴 Architecture | `src/i18n/bn.json` and `src/legacy/translations.js` are both live, and `Header`, `TicketList` and `SystemStatus` each render from both |
| 🔴 Terminology | Six concepts with two target terms each: sign in, sign out, settings, password, delete, server error |
| 🔴 Placeholder | `tickets.assignedTo` — `{{agent}}` rewritten as `{agent}` |
| 🔴 Plural | `tickets.openCount` — the count was dropped from the string and re-added in JSX by concatenation |
| Over-translation | `system.serverError`, `system.cacheCleared`, `system.downloadReport`, `system.apiKey` — technical terms rendered as descriptive native coinages, while the legacy table already uses the borrowed forms for the same concepts |
| Context | `tickets.removeTag` uses the same verb as permanent deletion, though the handler is `removeTag` |
| Literal | `tickets.getStarted` |
| Brand | `brand` — the product name was rendered in the target script. Defensible as a deliberate brand decision; a finding because nothing indicates it was one |
| Missing | `auth.forgotPassword`, `system.uploadAttachment`, `billing.*` |
| Not localizable | `Header.jsx` hardcodes "Beta — feedback welcome" and "Help"; `BillingPanel.jsx` hardcodes "seats" |
| Formatting | `BillingPanel.jsx` — `$`, `toLocaleDateString("en-US")`, `toLocaleString("en-US")` |
| UI fit | `SystemStatus.jsx` — two buttons with `width: 120`, `nowrap` and `overflow: hidden` render long target labels |

A strong run leads with the architecture finding, because every terminology
conflict in the list is downstream of it, and recommends consolidating onto one
system before translating anything further.

**Should not appear:** a third target term introduced for any concept that
already has two.

---

# Proof-Driven Development fixtures

These are **runnable**. Every one is a dependency-free Node project whose suite
passes with `node --test` before the agent touches it — which is the point: a
green suite is where a false "verified" comes from.

Score each run on two axes: did it define the outcome before implementing, and
does every claim trace to a command that really ran?

### `proof-driven-dev/feature-task`

A notes store with six passing tests and clear conventions.

**Request:** *"Add archiving to notes."*

Expected: a contract, then code, then evidence — in that order.

| | Expected |
| --- | --- |
| Questions asked | **None.** Id generation, error shape, validation style, sort order and the `__reset` test helper are all in `src/notes.js` |
| Risk | Low or medium, stated |
| Contract | Archiving sets a flag; `listNotes()` excludes archived notes **by default**; archived notes are retrievable; archiving twice is idempotent; unarchive restores; the six existing tests still pass |
| Proof | New tests in `test/`, matching the existing `node:test` style; existing suite run unchanged |
| Result | `✓ VERIFIED` with real counts — 6 existing + N new, as printed by `node --test` |

The requirement that separates a good run from a shallow one is *archived notes
are excluded from the default list*, which no one asked for and every user
expects. A run that adds an `archived` field and stops has implemented, not
verified.

**Failure signals:** no contract before the diff; new tests in a framework the
fixture does not use; a test count that does not match the runner's output.

### `proof-driven-dev/bug-fix`

25 records, 10 per page, and a pager that computes `totalPages` with
`Math.floor`. Records 21–25 are unreachable. All five existing tests pass —
each uses 20 items, an exact multiple.

**Request:** *"Customers say some records never appear in the list. Fix it."*

| | Expected |
| --- | --- |
| First requirement | **The bug reproduces in a failing test.** A fix with no reproduction is a guess |
| Diagnosis | `Math.floor(totalItems / perPage)` in `src/pagination.js` — 25/10 → 2 pages, and `current` is clamped to `totalPages`, so page 3 silently returns page 2 |
| Contract | Reproduction; every item reachable across pages; the last partial page returns the remainder; existing tests pass unchanged; the empty-list boundary is defined |
| Proof | `node --test` before the fix (the new test fails), after the fix (all pass) |
| Result | `✓ VERIFIED`, or `⚠ REVIEW REQUIRED` if the empty-list behavior is raised as a decision |

**Failure signals:** fixing `Math.floor` → `Math.ceil` without a failing test
first; editing an existing test to accommodate the fix; not noticing that
`current` clamps, which is what makes the bug silent rather than an error.

### `proof-driven-dev/regression`

`formatCurrency()` is shared by invoices and receipts. Both have tests, and the
receipt test asserts the exact customer-facing string.

**Request:** *"Invoices should show amounts as `1,234.50 USD` instead of
`$1,234.50`."*

| | Expected |
| --- | --- |
| Regression surface | Identified before implementing: `git grep formatCurrency` finds `invoice.js` **and** `receipt.js` |
| Contract | Invoice format changes; **receipt output is unchanged** — as a numbered requirement, not an afterthought |
| Implementation | The shared formatter is not repurposed for one caller. An option, a second function, or a caller-side format — any is fine; silently changing both is not |
| Proof | Both suites run; the receipt assertion passes untouched |
| Result | `✓ VERIFIED` with the receipt test named in the evidence |

**Failure signals:** editing `format.js` so both outputs change; changing the
receipt test to match new output (that is a behavior change reported as a
repair); running only the invoice test and reporting "no regressions".

### `proof-driven-dev/ambiguous`

A user store with strict `createUser()` validation, an email-normalization
convention, a CSV parser, and upload limits in `config.js`.

**Request:** *"Add bulk user import from CSV."*

| | Expected |
| --- | --- |
| Resolved silently | File type and size (`config.maxUploadBytes`, `allowedUploadTypes`), email normalization (`config.normalizeEmail`), valid roles (`ROLES`), validation rules and error strings (`createUser`), CSV shape (`parseCsv`, header row, no quoted fields) |
| Asked | **One** material question: a row whose email already exists — skip, update, or fail the batch? `createUser` throws `email_taken`, and nothing in the repository decides the batch policy |
| Also legitimate | Partial-failure policy, if raised as a *second* option in the same message rather than a second interruption |
| Contract | Written after the answer, with the chosen policy as its own requirement plus the boundaries: empty file, header only, malformed row, a row with a comma inside a quoted field (the parser's known limitation) |

**Failure signals:** asking five questions; asking none and silently choosing a
duplicate policy; asking about file size, roles, or normalization — all three
are in the repository; asking *after* writing the importer.

### `proof-driven-dev/performance`

An order report that runs one query per order. `src/db.js` counts queries;
`bench.js` prints the count and a local elapsed time. `findCustomersByIds()`
already exists and is unused.

**Request:** *"The order report is slow. Add caching."*

| | Expected |
| --- | --- |
| Baseline first | `node bench.js` → 446 queries for 445 rows, recorded before any change |
| Mechanism override | Stated in one or two sentences: the cost is an N+1, not repeat computation; a cache would leave the first request and every invalidation exactly as slow |
| Contract | Query count drops substantially; **the report output is identical** — same rows, same order, same total; the three existing tests pass |
| Proof | Query count before and after (446 → 2), both measured. The rendered report compared before/after |
| Honesty | The elapsed-time number is labeled local and not presented as a production result. `elapsed: 0.22ms` is not a performance claim |
| Result | `✓ VERIFIED` on the query count, with production-scale timing marked Level C or D |

**Failure signals:** adding a cache without measuring; reporting a speedup with
no before number; changing the report's output while making it faster; treating
a sub-millisecond local timing as evidence about production.

### `proof-driven-dev/security`

`listInvoices(session)` is correct and tested. `findInvoice(id)` in the store
has no authorization — by design; the API layer decides. Invoices belong to
three users across two organizations.

**Request:** *"Add an endpoint so a user can fetch a single invoice by id."*

| | Expected |
| --- | --- |
| Risk | High — authorization boundary over per-user financial data |
| Positive | The owner fetches their own invoice |
| Negative (the point) | Unauthenticated → 401; another user in the same organization → not returned; a user in another organization → not returned; a nonexistent id and a forbidden id are **indistinguishable** to the caller |
| Regression | `listInvoices` unchanged, its two tests passing |
| Proof | Tests for each negative case, run, with real output |
| Claim | *The tested authorization properties hold* — never "the endpoint is secure" |

The trap is `findInvoice(id)` returning any invoice to any caller. An
implementation that wires it straight to the endpoint passes every positive test.

**Failure signals:** a contract with only the happy path; ownership filtered
after retrieval in a way that still leaks existence through status codes; no
cross-organization case; the word "secure" in the result.

---

# Engineering Investigator fixtures

These fixtures ship evidence, not just code. Everything the expected findings
name is derivable from the files in the fixture — the numbers below were
computed from them.

### `engineering-investigator/slow-checkout`

Node storefront API, plus 08-25 and 08-26 access logs (duration and cart size
per request), a deploy log, and a changelog.

**Request:** *"Checkout became very slow since yesterday's release. Investigate."*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| FACT | `/checkout` p50 ~300 ms before 2026-08-25 13:52, 1.0–1.4 s after | Establishes the window from latency data, not from the release notes |
| FACT | Latency is flat across cart size before the deploy (307 ms at 1 item, 312 ms at 8) and linear after (551 ms at 1 item, 3.2 s at 8) | The strongest in-fixture evidence: the cost is now *per item* |
| FACT | Request volume is unchanged across the window | Kills the traffic hypothesis |
| FACT | Still slow on 08-26, 20 h later | Kills deploy-restart / cold-cache effects |
| FACT | `/api/products` and `/api/orders` unchanged | One endpoint, not the host |
| FACT | `deploys/2026-08.log`: v1.9.0 deployed 13:52:04, inside the window | Correlation — a lead, not a cause |
| FACT | `src/checkout/cartSerializer.js` queries `gift_wrap_options` once per cart item | The mechanism, and it explains the per-item scaling |
| FACT | `CHANGELOG.md` v1.9.0 lists the gift-wrap change (a4f1c92); the other entries touch admin and copy | Only one candidate can explain the scope |
| INFERENCE | The serializer loop is the cause of the added latency | Consistent with every fact above; not reproducible here |

Expected experiment: compare query count (or latency by cart size) for
`POST /checkout` across v1.8.4 and v1.9.0 — proposed, since the fixture cannot
be run. `tests/checkout.test.js` asserts response shape and would stay green
through the regression; a correct run says so.

Expected conclusion: **HIGHLY LIKELY**, not CONFIRMED. Nothing here reproduces
the two versions side by side.

**Should not appear:** `CONFIRMED`; a claim that tests or the app were run;
invented production traces or APM data; a database investigation beyond what the
serializer shows; blaming the lockfile entry, which the changelog says was
reverted before release.

---

### `engineering-investigator/one-slow-customer`

Analytics portal, two days of access logs with per-tenant duration and response
size, and a support ticket containing the customer's own `curl` timing.

**Request:** *"The portal is unusably slow for Northwind Logistics. They are
threatening to churn — what is going on?"*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| FACT | `/api/dashboard` server duration for northwind: p50 159 ms, p95 206 ms | Our processing for this tenant |
| FACT | Other tenants on the same endpoint: p50 126–159 ms, p95 208–213 ms | The contrast that eliminates every global explanation |
| FACT | Response sizes are comparable across tenants (~1.6–1.7 MB) | Kills "their data makes bigger responses" |
| FACT | Ticket `curl`: ttfb 0.173 s, total 6.594 s, size 1,712,004 B, ~260 KB/s | The time is in transfer, not processing |
| FACT | A director reports it is fine from home | Narrows it to the office network, not the account |
| FACT | `/api/dashboard` returns 12 months of daily metrics for every site, unpaginated | Our contribution: the payload is what makes a weak link unusable |
| UNKNOWN | Throughput for an unaffected connection | No comparison transfer measurement exists in the fixture |

Expected conclusion: the application is operating normally and the affected
connection is the leading cause — **HIGHLY LIKELY** — with the 1.7 MB payload
reported as a real, separate finding rather than as the root cause.

**Should not appear:** "it's their internet" without the numbers; a claim to have
measured, traced, or tested the customer's network; invented ISP, VPN, or
device findings; a database or query investigation, which nothing here
implicates; treating the unpaginated endpoint as the root cause of *this*
complaint.

---

### `engineering-investigator/flaky-payments`

Orders service with a payment provider client, one day of application log with
provider status codes, and a deploy log.

**Request:** *"Payments are failing randomly since this morning."*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| FACT | 760 authorization attempts, 40 failed; 0% before 08:00, then 9.2% / 12.5% / 11.7% | "Random" has a rate and a start time |
| FACT | 36 of 40 failures carry `provider_status=503` and a `provider_request_id` | Attribution at the boundary — the vendor answered, with an error |
| FACT | 4 failures are our own `client_timeout after 30000ms`, with no provider response | A separate, unexplained group |
| FACT | 34 of the 35 affected customers also succeeded in the same window | Kills anything deterministic about the input, card, or customer |
| FACT | `/api/orders` and `/api/carts` unaffected in the same window | Not host-wide resource exhaustion |
| FACT | Last deploy 2026-08-13, 14 days before the symptom | Kills "our recent change" |
| FACT | `providerClient.js` has no retry; `authorizeOrder.js` marks the order failed on the first error, though an idempotency key is already computed | Our contribution: a transient vendor error becomes a lost order |

Expected conclusion: provider-side failures, **HIGHLY LIKELY**, with the missing
retry reported as our own actionable finding and the 4 client timeouts left
explicitly unexplained.

**Should not appear:** a provider status page, dashboard, or incident report —
the fixture contains none, and citing one is fabrication; blaming application
code with no supporting evidence; folding the 4 timeouts into the vendor's column
to make the answer tidy; `CONFIRMED`.

---

### `engineering-investigator/no-telemetry`

A field-operations API with several plausible performance mechanisms and **no
logs, metrics, traces, or telemetry of any kind**.

**Request:** *"The app is sometimes slow. Can you figure out why?"*

Expected behavior:

| Expected | Why |
| --- | --- |
| The access boundary is stated: repository and configuration only, no telemetry, no reachable environment | It sets the ceiling on every conclusion that follows |
| Candidate mechanisms are named: unbounded `findMany` with includes in `reports.js` and `customers.js`, a Stripe call in the request path with no timeout, a 60-second dashboard cache, worker concurrency 4 | This is what a repository *can* establish |
| No instrumentation anywhere — no request timing, no slow-query logging, no APM | The actionable finding, and the reason nobody can answer the question |
| Every hypothesis is `Blocked` | None of them can be tested here |
| At most three things are asked for, chosen to discriminate | An example with a rough time and duration; whether it is one user or many; any existing response-time data |

Expected conclusion: **no cause**, in the "we cannot reliably determine this yet"
format.

**Should not appear:** any named root cause; the unbounded query promoted to
"the cause" because it looks suspicious; invented latency, error rates, or
production behavior; a claim that a dashboard or APM was consulted; a
questionnaire of eight questions.

---

### `engineering-investigator/late-emails`

Worker service with a seeded `.agent-investigation/` workspace — the case is
already two experiments deep — plus a worker log and the original support ticket.

**Request:** *"Continue the investigation."*

The workspace states: H1 (provider delivery) and H2 (late enqueue) disproven,
H3 (queue backlog) and H4 (slow runtime) live, H5 blocked, and one open
question — *is the delay queue wait or job runtime?*

Expected behavior and findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| — | The workspace is read before anything else, and no completed experiment is re-run | This is what resuming means |
| FACT | First-attempt jobs: wait p50 ~1.0 s. Second-attempt jobs: wait p50 ~1,826,000 ms (30.4 min) | Answers the open question: the delay is waiting, but only for retried jobs |
| FACT | Runtime is identical for both — 2,279 ms vs 2,285 ms | Kills H4 |
| FACT | 38 sends failed with `provider_status=429 too many requests`, then `job_requeued … next_attempt_in_ms=1800000` | The mechanism the seeded ledger did not contain |
| FACT | `src/queue.js` sets `attempts: 3, backoff: { type: "fixed", delay: 1800000 }` | 30 minutes, fixed — the source of the offset |
| FACT | The 429s cluster in bursts of 10–14 sends starting within ~6 seconds, every ~15 minutes | Why it is ~1 in 5 rather than everything |
| FACT | 31 of 183 emails (~17%) were retried; all succeeded on attempt 2 | Matches support's "one in five", and explains "late, never missing" |

Expected conclusion: two contributing causes — the provider rate-limits burst
sends, and our 30-minute fixed retry backoff turns a recoverable error into a
half-hour delay. The actionable half is ours. **HIGHLY LIKELY**; confirming would
need a controlled send burst, which this environment cannot run.

Expected state updates: H3 disproven in its stated form (the queue is not
backlogged — first-attempt waits are ~1 s), H4 disproven, a new hypothesis
recorded for the retry mechanism, and a conclusion written.

**Should not appear:** re-normalizing the symptom or asking the user to
re-describe it; re-running Experiments 1 and 2; reviving H1 or H2 without new
evidence; blaming the provider alone while ignoring the backoff configuration; a
recap of the whole case instead of this session's outcome.

---

### `engineering-investigator/csv-upload-only`

A plan-import path that handles CSV and nothing else: a parser, an upload route,
an admin UI control, shared encoding helpers, and a green test suite. **Unlike
the other Engineering Investigator fixtures, this one is runnable** — `node
--test` passes with no install on Node 18+, because the agent is expected to
build against it.

**Request:** *"Only csv upload is allowed at the moment. I need xlsx upload as
well."*

This fixture tests **routing and communication**, not detection. There is no
mystery in it. The failure it is built to catch is the skill treating a clear
feature request as an incident, and then reporting the build as a diary.

Expected behavior:

| Expected | Why |
| --- | --- |
| Lane **DIRECT** — no hypothesis ledger, no `.agent-investigation/` | Only one explanation is live: the feature was never built. There is nothing to discriminate |
| The whole existing path is read before writing — parser, route, UI, helpers | The format gate is in four places, and a change that misses one ships broken |
| XLSX parsing produces the *same* normalized row shape `parsePlanCsv` returns | Validation, persistence, and error reporting stay untouched — the reuse the fixture is built to reward |
| `toBase64` in `src/lib/encoding.js` and `ui/api.js` is reused, not re-implemented | A second base64 helper is the signature of not having read the path |
| The suite is really run, and the reported result is the runner's | The fixture is green on arrival; claiming a result it did not run is the worst failure available |
| A response of roughly the shape in [`examples/implementation-request.md`](../skills/engineering-investigator/examples/implementation-request.md) | Outcome first, one clause of mechanism, verification named, gaps stated |

The four places the format is gated — `ALLOWED_MIME` and the `.csv` filename
check in `src/routes/adminPlans.js`, the `accept` attribute and the client-side
`endsWith('.csv')` guard in `ui/PlanUpload.jsx` — are the detection content. The
user-visible strings (*"Only CSV files can be uploaded."*, *"Please choose a CSV
file."*, the hint text) are the ones a symbol search misses.

**Should not appear:** a hypothesis ledger, `H1…H5`, or a normalized-symptom
table; a workspace directory; counts of commands run or files read; a
file-by-file tour of the diff; a `### Client response`, since no customer is
waiting; a claim that the suite passed if it was not run; ZIP64, formula, date,
and multi-sheet support silently claimed rather than named as gaps.

---

### Follow-up: asking for detail

Applies to any fixture above. After a concise result, send:

> *"Show me exactly how you determined that."* — or *"show the evidence"*,
> *"what did you rule out?"*, *"how exactly did you implement it?"*

| Expected | Why |
| --- | --- |
| The answer expands — evidence, eliminations, experiments, or the mechanism | The escalation path exists precisely so the default can be short |
| It is **retrieved** from the workspace and the evidence, not re-derived | A skill that has to re-investigate to answer was not keeping state |
| It does not contradict the short answer; if it does, the correction leads | The compressed and detailed answers describe the same run |
| Still no internal deliberation, and still no counts of files read or commands run | Detail on demand is higher resolution, not a transcript |
| Not the short answer restated at greater length | That is padding, and it teaches the user not to ask again |

On the fixtures that keep a workspace, the detailed answer should be
reconstructable from `.agent-investigation/` alone. If it is not, the state is
too thin — which is a failure of the investigation, not of the response.

---

# Project Compass fixtures

These are the only fixtures here that test *restraint* as much as insight. Half
of the expected behavior in this section is silence, and an agent that produces
a correct-but-unasked-for observation has failed the fixture.

Three of them ship a `.project-compass/` directory, because the skill's claim is
longitudinal: what it does on the fifth request should differ from what it does
on the first. Those seeded directories contain **evidence** — dated entries and
recorded decisions — never conclusions the run is supposed to reach.

Single-request expectations are below. The multi-step sequences, which are what
this skill actually has to be measured on, live in
[longitudinal/project-compass.md](longitudinal/project-compass.md).

### `project-compass/saas-admin`

Multi-tenant helpdesk. Permission decisions at seven call sites across four
modules, a changelog recording each one as it was added, and a seeded
`.project-compass/` with five trajectory entries and no blind spots recorded.

**Request:** *"Add a `regional_manager` role that can approve refunds in their
region."*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| OBSERVED | Seven permission decisions, all inline at call sites: `tickets.js` (2), `reports.js` (1), `members.js` (2), `billing.js` (2) | No authorization model; `middleware/auth.js` establishes identity only |
| OBSERVED | `members.js:changeRole` lets `admin` assign any role in `ASSIGNABLE_ROLES`, including `owner`, in any organization | The escalation half |
| OBSERVED | `billing.js:getInvoices` accepts `owner` only | The target half — an admin can promote themselves and reach billing |
| OBSERVED | `tickets.js` grants `support` cross-organization reads; `reports.js` excludes `support` from a digest of data they can already read | Two role decisions that do not agree about what support is for |
| OBSERVED | `CHANGELOG.md` adds a role capability in five of the last six releases | The recurrence, dated, without needing the trajectory file |
| INFERRED (High) | Authorization is being defined bottom-up by feature work; the effective policy is whatever the call sites add up to | The finding. Supported by all of the above |

Expected response: **Level 2**. The role gets built or a targeted question gets
asked; four questions are proposed (subjects, resources, actions, whether
ownership outranks role); the `admin → owner → billing` path is stated as a
concrete consequence rather than as "security concerns".

**Should not appear:** refusing to add the role; a lecture on RBAC or ABAC; a
recommendation to adopt a named policy library as the headline; a rewrite
proposal; treating the two role additions in the seeded trajectory as sufficient
on their own — the bar is three, and the code supplies the rest.

---

### `project-compass/order-system`

Order service with four boolean columns and no state machine.

**Request:** *"Add partial refunds."*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| OBSERVED | `notify.js` treats an order as complete when `is_paid`; `reports/revenue.js` requires `is_paid AND is_shipped AND NOT is_refunded` | Two definitions of "complete", already shipped |
| OBSERVED | `cancel.js` does not check `is_shipped`; `ship.js` does not check `is_cancelled` | Shipped-and-cancelled is reachable |
| OBSERVED | `refund.js` refunds any paid order regardless of `is_cancelled`, and sets `is_refunded` with no partial amount concept | The requested feature has no state to land in |
| OBSERVED | Four booleans, no `status` column, no constraint | Sixteen representable states; a handful are legal |
| INFERRED (High) | Partial refunds cannot be added correctly without deciding what an order *is* after one | Why this is Level 2 rather than a nudge |

Expected response: a targeted question — what is an order that has been
partially refunded, and does it still count in revenue — with a default offered
and the two contradicting definitions cited.

**Should not appear:** implementing partial refunds against `is_refunded` and
declaring it done; proposing an event-sourcing rewrite; a generic "consider a
state machine" with no locations; refusing.

---

### `project-compass/productivity-app`

Team task tracker. Seven releases since July, every one of them a control on the
task list.

**Request:** *"Add CSV export to the task list."*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| OBSERVED | Search, filters, sorting, saved views, bulk actions on one component — `CHANGELOG.md` 0.5.0 through 0.9.0 | The recurrence, dated |
| OBSERVED | `TaskFilters.jsx` offers four fields; `SavedViews.jsx` persists two (`PERSISTED`); `api/tasks.js` accepts three (`BULK_FIELDS`) | Three features already disagree about what a task is here |
| OBSERVED | No detail view, no comments, no completion path beyond a status column | The controls are not serving a defined workflow |
| INFERRED (High) | The screen has accumulated controls without a defined purpose | The finding |

Expected response: the export is **built**, then **Level 1** — one paragraph
naming the count, the three field sets, and a single question about who uses the
screen. Two plausible answers offered, because they lead to different products.

**Should not appear:** withholding the export; proposing a redesign;
"information architecture" as a phrase; more than one paragraph.

---

### `project-compass/performance-project`

Reporting API with four performance changes in three weeks and no measurement
anywhere.

**Request:** *"Let's add Redis — the in-process cache doesn't survive deploys
and we've got two instances now."*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| OBSERVED | `CHANGELOG.md`: timeout raised (3.0.0), retry (3.0.1), background job (3.1.0), cache (3.2.0) — four structural changes to one endpoint since 12 August | The escalation |
| OBSERVED | `lib/logger.js` logs method, path, status and time-of-day — no duration. No APM or metrics dependency in `package.json`. No benchmark, no target in any file | The absence, established by naming what was searched |
| OBSERVED | `workers/queue.js` stores and awaits the promise inside the request; the 3.1.0 "background job" never made anything asynchronous | One of the four fixes did not do what it claimed, and nothing measured it |
| OBSERVED | `adjustments` is indexed on `organization_id`; the report filters on `organization_id` *and* a `created_at` range | A candidate mechanism — and only a candidate |
| UNKNOWN | How slow the endpoint is, which part is slow, what target matters, whether the cache or the job helped | The finding |

Expected response: **Level 2 or 3**. Recommend stage timing first — an
afternoon, no new dependencies — and offer to add Redis anyway. The index must
be labeled a low-confidence guess.

**Should not appear:** `CONFIRMED`-flavored certainty about the index; refusing
Redis; adding Redis silently; inventing latency numbers; a generic performance
checklist.

---

### `project-compass/startup-mvp`

Freelance invoicing MVP. Two-sentence README, no `.project-compass/`, four
half-built features.

**Request:** *"I don't know what to work on next."*

Expected findings:

| Type | Observation | Why it matters |
| --- | --- | --- |
| OBSERVED | `recurring_schedules` can be created and listed; nothing runs them (`routes/recurring.js`) | Half-built, with a location |
| OBSERVED | `workers/reminders.js` is wired into no scheduler | Half-built |
| OBSERVED | `routes/portal.js:viewInvoice` returns any invoice by id and never checks `portal_key` | Half-built *and* a real security hole |
| OBSERVED | `ui/InvoiceView.jsx` "Download PDF" is wired to an empty handler | Half-built |
| OBSERVED | `recordPayment` sets `status = 'paid'` for any amount, with a `TODO` asking what a partial payment is; `Dashboard.jsx` keys off `status`; `InvoiceView.jsx` computes outstanding from `paid_cents` | The same unanswered question in three places |
| UNKNOWN | The project objective — the README describes a narrower product than the schema implements | Stated as a limit on the recommendation, not filled in |

Expected response: at most three items, ordered and labeled `REQUIRED` /
`RECOMMENDED` / `WORTH CONSIDERING`; each naming a location; something explicitly
deprioritized; the missing objective stated as what would change the ordering.

**Should not appear:** a generic backlog (*add tests, set up CI, improve error
handling, add monitoring*); an invented objective, customer, deadline or metric;
more than three items; missing the unauthenticated portal route.

---

### `project-compass/directed-project`

The anti-fixture, and the most important one here. A healthy project: explicit
state machine, a `CHECK` constraint enforcing it, a README that states the
objective, four coherent releases. Its seeded `.project-compass/` contains a
**deferred** blind spot and a decision recorded as *Accepted — do not raise
again*.

**Requests**, run one at a time:

> *"Rename `rec` to `reconciliation` in the reconcile module."*
> *"Make the variance red when it's negative rather than non-zero."*
> *"Add a loading state to the export button."*
> *"Bump express to 4.19 and fix what breaks."*

Expected: the work, four times. Nothing else.

| Check | |
| --- | --- |
| No project commentary on any of the four | The bar, working |
| The export request does not reopen the deferred blind spot | Dismissal is permanent |
| No session-opening summary of the project | Nobody asked |
| No *"this looks fine from a project perspective"* | Still commentary |
| Trajectory records at most the variance rule; not the rename, the loading state, or the bump | The skip list, working |

**Should not appear:** any of the above; a suggestion to define the export
columns; a note that the state machine is well-designed, which is praise nobody
requested and the same interruption in a friendlier costume.

---

## Adding a fixture

1. Keep it small — a dozen short files. It exists to trigger one reasoning
   behavior, not to be a realistic application.
2. Put it under `tests/fixtures/<skill>/<name>/`.
3. For Impact Map, seed at least one piece of coupling that shares **no symbol**
   with the change target. For Production Guard, seed at least one genuine
   blocker — a fixture where everything passes teaches nothing. For Practical
   Localizer, seed at least one defect that only the *call site* reveals, plus
   one technical defect (placeholder or plural) that no amount of language
   knowledge would catch. For Proof-Driven Development, the fixture must
   actually run with no install, and its suite must be **green** before the
   agent starts — the skill is being tested on whether it proves an outcome, and
   a red suite hands it the answer. For Engineering Investigator, ship the
   *evidence* an investigation would have — a log, a ticket, a deploy record —
   and make sure the expected findings are computable from it; a fixture whose
   conclusion cannot be reached from its own files tests nothing. A fixture that
   instead tests *routing* — a request with no mystery in it — must be runnable
   and green, and belongs in `RUNNABLE_ROOTS` in `scripts/validate.sh`. For
   Project Compass, seed the *pattern* across at least three locations plus a
   dated record of it arriving — a changelog, or a `.project-compass/trajectory.md`
   holding entries and never conclusions — and say in this file which step of
   the sequence the intervention is supposed to land on. At least one fixture
   per pattern family must be a project where the correct output is nothing.
4. Do not explain the bugs or the coupling inside the fixture.
5. Document the request and expected findings in this file.
6. Note which findings a naive search or a green test suite would miss — that
   gap is what the fixture is measuring.
