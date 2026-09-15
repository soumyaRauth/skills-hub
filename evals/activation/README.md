# Activation suite

Does the right skill show up without being named, and do the others stay out of
the way? This suite measures exactly that. It is a
[`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals) suite.
Each case copies a fixture repository from `tests/fixtures/` into an isolated
sandbox, sends a request phrased the way a developer would type it, and grades
the session on which Skills Hub skills it loaded.

Unlike the rest of `tests/`, this part is **deterministic in its grading**. A
`tool_used` grader counts Skill tool calls, and a `regex` grader reads the final
reply. What is non-deterministic is the model, which is why a case defaults to
three runs.

## Running it

From the repository root, which `.claude-plugin/plugin.json` makes a plugin:

```bash
# the full suite, three runs per case, one arm
claude plugin eval . --scaffold --allow-tools Write Edit --ablation none --no-publish

# one case, once, while tuning a description
claude plugin eval . --case quiet-patch-bump --runs 1 --scaffold --allow-tools Write Edit --ablation none

# the smaller core set
claude plugin eval . --tag core --scaffold --allow-tools Write Edit --ablation none
```

- `--scaffold` runs each case's `scaffold.sh`, which copies a fixture into the
  empty workspace (via `fixture.sh`). You wrote those scripts, or can read them:
  two lines each.
- `--allow-tools Write Edit` lets the agent build, as it would in a real session.
  It writes only into the throwaway sandbox. Without the grant, the agent spends
  turns looking for edit tools.
- `--ablation none` skips the no-plugin arm. A "must not load" check is trivially
  true without the plugin, so the second arm adds cost and no information here.
- Every run is a real model session on your credentials. A single run of one
  case costs roughly what a short Claude Code task does. Use `--max-cost-usd` for
  a hard ceiling. The suite is not in CI for that reason.

## How a case is graded

| Grader | Passes when |
| --- | --- |
| `engages-<skill>` | That skill was loaded at least once |
| `engages-<a>-or-<b>` | Either was loaded, where both are defensible |
| `quiet-<skill>` | That skill was never loaded (`min: 0`, `max: 0`) |
| `composes-two-or-more` | At least two Skills Hub skills were loaded |
| `no-activation-line` | The final reply has no `⚡` line (quiet cases) |
| `compass-silent` | The final reply does not announce Project Compass, which may still read its state passively |

Skills not named in a case are allowed either way. The suite does not reward
loading more skills. It rewards loading the right ones.

## Categories

`positive` — one discipline clearly applies · `composition` — several should ·
`contextual` — the same request shape goes different ways depending on the
repository · `quiet` — nothing should load · `keyword-trap` — a domain word with
no domain work behind it · `superficial-match` — the domain is sensitive, this
change is not · `low-risk-high-risk-project` — a trivial change inside a project
with real findings · `already-satisfied` — the requested property already holds
· `override` — the user named a skill, or opted out of one · `passive` — a skill
may read but must not speak · `new-skill` — covers `dependency-guard` and
`api-contract-guard` · `core` — the smaller set used for before/after comparisons.

## Cases

| Case | Request | Must engage | Must stay quiet | Why |
| --- | --- | --- | --- | --- |
| `im-rename-shared-status` | Rename the COMPLETED enrollment status to APPROVED. | impact-map | standards-compass, practical-localizer, engineering-investigator, dependency-guard | The stored value is read by raw SQL, a nightly job and two UI comparisons that share no symbol with the enum. |
| `im-explicit-invocation` | Use Impact Map before doing this: extend the order cancellation window from 15 to 30 minutes. | impact-map | standards-compass, practical-localizer, engineering-investigator, dependency-guard, api-contract-guard | The user named the skill. A small change, but an explicit request engages it regardless. |
| `pb-feature-archiving` | Add archiving to notes. | proof-driven-dev | standards-compass, practical-localizer, engineering-investigator, dependency-guard, api-contract-guard, production-guard | Meaningful behavior change with an unstated requirement (archived notes leave the default list). Nothing security-, locale- or contract-shaped. |
| `pb-bug-missing-records` | Customers say some records never appear in the list. Fix it. | proof-driven-dev / engineering-investigator | standards-compass, practical-localizer, dependency-guard, api-contract-guard | A symptom with a reproducible cause. Either proving the fix or investigating first is defensible; the audit skills are not. |
| `pg-release-refunds` | We're releasing tomorrow. Is the refund flow safe to ship? | production-guard | practical-localizer, project-compass, engineering-investigator, dependency-guard | An explicit ship decision on a money path. Production Guard gates; Standards Compass may contribute controls. |
| `pl-new-locale` | We're launching in Brazil — add Brazilian Portuguese. | practical-localizer | standards-compass, engineering-investigator, production-guard, dependency-guard, api-contract-guard, project-compass | A new locale in an ICU catalog app. Nothing else about it needs a discipline. |
| `ei-payments-failing` | Payments started failing randomly this morning. What's going on? | engineering-investigator | standards-compass, practical-localizer, dependency-guard, project-compass, api-contract-guard | An unexplained symptom. 'Payments' is a keyword trap for Standards Compass: nothing here is a standards question. |
| `pc-another-status-lifecycle` | Add a pending_review status for orders we want to hold before shipping. | project-compass | standards-compass, practical-localizer, engineering-investigator, dependency-guard | Four contradicting booleans and no lifecycle: the fifth flag deepens an undefined state machine. |
| `pc-what-next` | I don't know what to work on next. | project-compass | practical-localizer, engineering-investigator, dependency-guard, api-contract-guard, production-guard | A direct direction question, answered from the repository. |
| `sc-password-reset` | Clients keep forgetting their passwords. Add a password reset by email. | standards-compass | practical-localizer, engineering-investigator, dependency-guard | Account recovery: token handling, enumeration, rate limits. Standards Compass names them before the code. |
| `sc-file-upload` | Let customers attach a PDF purchase order to their invoice. | standards-compass | practical-localizer, engineering-investigator, project-compass | File upload: server-side type and size limits, storage outside the web root, download authorization. |
| `sc-admin-role` | Add a regional_manager role that can approve refunds in its region. | standards-compass | practical-localizer, engineering-investigator, dependency-guard | A new privilege over money. Project Compass may also engage — authorization is defined at seven call sites. |
| `sc-ai-summaries` | Add an AI-generated summary of each invoice using the Claude API. | standards-compass | practical-localizer, engineering-investigator | Customer data sent to a model, output rendered to users. Dependency Guard may engage for the SDK. |
| `dg-add-library` | Add lodash so we can debounce the customer search box. | dependency-guard | practical-localizer, engineering-investigator, project-compass | A new dependency for something the platform or a few lines already do. |
| `dg-major-upgrade` | Upgrade Express to version 5. | dependency-guard | practical-localizer, engineering-investigator, project-compass | A major version with breaking changes. Impact Map and Production Guard may follow. |
| `ac-outgoing-webhook` | Send a webhook to our customers' systems whenever an order ships. | api-contract-guard | practical-localizer, engineering-investigator, dependency-guard | A contract with systems that deploy independently: payload, signing, retries, ordering, versioning. |
| `ac-public-endpoint` | Add a public API endpoint so customers can list their invoices from their own systems. | api-contract-guard | practical-localizer, engineering-investigator | A public read API: pagination, error shape, authorization boundary, versioning — hard to take back. |
| `compose-admin-customer-export` | Add a CSV export of all customers, admin-only. | standards-compass + ≥2 skills | practical-localizer, engineering-investigator, dependency-guard | Personal data leaving the system behind a privilege check. More than one discipline should engage. |
| `compose-org-invitations` | Add organization-level member invitations with roles. | standards-compass + ≥2 skills | practical-localizer, engineering-investigator, dependency-guard | Identity, roles and tenancy in a project whose authorization is already scattered. |
| `compose-subscription-cancel` | Add subscription cancellation. | impact-map / standards-compass / api-contract-guard + ≥2 skills | practical-localizer, engineering-investigator | A billing lifecycle change touching the provider, webhooks and existing records. |
| `compose-split-customer-name` | Split the customer name field into firstName and lastName. | impact-map | standards-compass, practical-localizer, engineering-investigator, dependency-guard | A schema change with every reader in scope. It restructures personal data but adds none, so Standards Compass stays quiet. |
| `compose-duplicate-orders` | Users sometimes see duplicate orders after retrying checkout. | engineering-investigator | practical-localizer, dependency-guard, project-compass | An intermittent symptom first. Impact Map and ProofBuild may follow once a cause exists. |
| `compose-keyboard-table` | Make the customer table usable with a keyboard and a screen reader. | standards-compass | impact-map, practical-localizer, engineering-investigator, dependency-guard, api-contract-guard, production-guard | Accessibility implementation. Standards Compass owns it; there is no separate accessibility skill to compete. |
| `ctx-another-status-state-machine` | Add an on_hold state to adjustments. | — | standards-compass, practical-localizer, engineering-investigator, dependency-guard, api-contract-guard | The same request shape as pc-another-status-lifecycle, in a project with a declared state machine. Project Compass has nothing to say. |
| `ctx-button-copy-localized` | Change the 'Invite member' button to say 'Add teammate'. | — | standards-compass, impact-map, production-guard, engineering-investigator, dependency-guard, project-compass, api-contract-guard | Copy change in a translated app. Practical Localizer may add one line: the Bengali catalog still says the old thing. |
| `quiet-button-copy` | Change the 'Download PDF' button label to 'Get PDF'. | — | all | Copy change, no catalogs. No discipline improves it. |
| `quiet-readme-grammar` | In the README, change 'require manager approval' to 'require a manager's approval'. | — | all | A documentation edit. |
| `quiet-local-rename` | Rename the variable rec to reconciliation in src/reconcile/close.js. | — | all | A local rename the language resolves. |
| `quiet-reformat-flawed-project` | Reformat src/orders/cancel.js with 2-space indentation. | — | all | Formatting inside the project with the undefined lifecycle. The flaw is real and irrelevant to this request. |
| `quiet-comment-refund-keyword` | Update the comment at the top of src/services/refund.js to say refunds are issued through Stripe. | — | all | 'Refund' and 'Stripe' are keywords; the change is a comment. |
| `quiet-sort-requires-upload` | Sort the require statements at the top of src/api/upload.js alphabetically. | — | all | Lint-level change in a security-sensitive file with real findings in it. Not this request's business. |
| `quiet-css-spacing` | Add a bit more vertical spacing between rows in the appointment list. | — | all | Spacing. |
| `quiet-patch-bump` | Bump express from 4.18.2 to 4.18.3. | — | all | A routine patch bump of a dependency already present. |
| `quiet-migration-comment` | Add a one-line comment above the AddField in 0002_add_region.py explaining that region is used by the sales report. | — | all | 'Migration' is a keyword; the change is a comment. |
| `override-no-standards-review` | Add a CSV export of customers for admins. Don't run a standards review, just build it. | — | standards-compass, practical-localizer, engineering-investigator, dependency-guard | Explicit opt-out of a consultation the request would otherwise earn. |
| `already-satisfied-dialog` | Make sure the booking dialog moves focus in and restores it on close. | — | impact-map, production-guard, dependency-guard, engineering-investigator, practical-localizer, api-contract-guard, project-compass | Dialog.jsx already does both. Standards Compass may look; nothing should be built. |
| `quiet-internal-helper` | Add a helper in src/services/invoice.js that formats an amount in cents as a dollar string. | — | api-contract-guard, standards-compass, production-guard, dependency-guard, engineering-investigator, practical-localizer, project-compass, impact-map | New isolated code with no external consumer: no contract, no blast radius. |
| `passive-compass-healthy-project` | Add a notes field to adjustments so an approver can explain a rejection. | — | standards-compass, practical-localizer, engineering-investigator, dependency-guard, api-contract-guard | An ordinary feature in a healthy project that keeps .project-compass/. Compass may read its state; it must not speak. |

## What this does not test

- **Sequences.** Engagement that ends when the request changes ("add payment",
  then "rename the button"), dismissals that stay dismissed, and repeated
  requests are multi-turn behaviors. They live in
  [`tests/longitudinal/ecosystem.md`](../../tests/longitudinal/ecosystem.md).
- **What a skill does once loaded.** The fixture expectations in
  [`tests/README.md`](../../tests/README.md) cover that.
- **Other agents.** The sandbox is Claude Code. Descriptions are portable, but
  how another agent selects skills is not measured here.

## Adding a case

One directory with a `case.yaml` and a two-line `scaffold.sh` that sources
`../fixture.sh <skill>/<fixture>`. Name the skills that must engage and the ones
that must not, and say why in `description`. Add a row to the table above:
`scripts/validate.sh` checks that every case is listed here, that every skill
named in a grader exists, and that every skill has at least one case where it
must engage and one where it must stay quiet.
