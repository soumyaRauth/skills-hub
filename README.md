# Skills Hub

Agent Skills for real engineering work — installable with the Skills CLI,
usable with Claude Code and other Agent Skills-compatible agents.

**[Browse the skills →](https://soumyaRauth.github.io/skills-hub/)**

| Skill | What it does | When |
| --- | --- | --- |
| **[impact-map](skills/impact-map/README.md)** | Maps the blast radius of a proposed change — what it affects, why, and how confident the analysis is | *Before* you write the code |
| **[proof-driven-dev](skills/proof-driven-dev/README.md)** | Turns a request into an outcome contract, implements it, and proves each requirement with evidence — you get VERIFIED / REVIEW / BLOCKED, not an essay | *While* you write it |
| **[production-guard](skills/production-guard/README.md)** | Validates whether a change is safe to ship: behavior, regressions, failures, security, data integrity, performance, operations | *After* you write it, before you merge |
| **[practical-localizer](skills/practical-localizer/README.md)** | Localizes an app into natural, context-aware target-language product copy instead of literal translation | *When* you take the product to another language |
| **[engineering-investigator](skills/engineering-investigator/README.md)** | Investigates a vague complaint by evidence — competing hypotheses, discriminating experiments, and a short conclusion that may be *not our fault* | *When* something is already broken and nobody knows why |
| **[project-compass](skills/project-compass/README.md)** | Keeps an evidence-based model of what the project is and where it is heading, and taps you on the shoulder when the requests stop adding up — rarely, and never twice | *Across* everything, quietly |
| **[standards-compass](skills/standards-compass/README.md)** | Works out which standards, security frameworks, accessibility requirements, privacy obligations and AI governance frameworks actually apply to your software — then audits it against them, with evidence | *Whichever* of those you never consciously chose |

```bash
npx skills add soumyaRauth/skills-hub --skill impact-map
npx skills add soumyaRauth/skills-hub --skill proof-driven-dev
npx skills add soumyaRauth/skills-hub --skill production-guard
npx skills add soumyaRauth/skills-hub --skill practical-localizer
npx skills add soumyaRauth/skills-hub --skill engineering-investigator
npx skills add soumyaRauth/skills-hub --skill project-compass
npx skills add soumyaRauth/skills-hub --skill standards-compass
```

They compose, and none requires the others:

```
ticket   → impact-map → proof-driven-dev → production-guard → ship
                                                            → practical-localizer → ship in another language

incident → engineering-investigator → cause → proof-driven-dev → production-guard → ship

project-compass sits underneath all of it, and answers a different question:
whether the ticket should have been written in the first place.

standards-compass sits underneath it too, and answers another one:
what this software should have been measured against all along.
```

---

# Impact Map

**A reusable AI engineering skill for understanding the blast radius of software
changes.**

Impact Map is an [Agent Skill](https://code.claude.com/docs/en/skills) that runs
*before* implementation. It analyzes a repository and produces an evidence-based
change impact report: what a proposed change affects, why, how confident the
analysis is, and what to do next — without touching a single file.

```bash
npx skills add soumyaRauth/skills-hub --skill impact-map
```

---

## The problem

```
ticket → find the obvious file → change it → discover later what broke
```

The obvious file is rarely what breaks. What breaks is the raw SQL in a report,
the string comparison in a nightly job, the fixture that keeps CI green while
the behavior is wrong, the policy that never learned about the new state.

Generic code search does not help much, because it returns this:

```
File A
File B
File C
```

— with no explanation of why any of it matters.

## The solution

Impact Map inserts a read-only analysis step and returns findings that carry
their reasoning:

```
ticket → impact map → architecture → dependencies → hidden coupling
       → tests → risks → implementation plan → coding
```

Every significant finding is classified and evidenced:

| | Meaning |
| --- | --- |
| 🟥 **MUST CHANGE** | Strong evidence this location requires modification. |
| 🟧 **LIKELY AFFECTED** | Strong relationship; needs confirmation. |
| 🟨 **NEEDS VERIFICATION** | Plausible relationship; check before implementing. |
| ⚠️ **HIDDEN COUPLING** | Indirect dependency — raw strings, SQL, config, duplicated logic, fixtures, serialization, co-change history. |
| ⬜ **OUT OF SCOPE** | Inspected, not materially related. |

Confidence is tracked separately (High / Medium / Low), and a low-confidence
finding is never promoted to MUST CHANGE. Speculation is never presented as
fact, and counts are never invented.

---

## Example

```
You:  Rename the COMPLETED enrollment status to APPROVED. Deep analysis please.

Agent: I'll map the impact surface before changing anything.

IMPACT MAP
────────────────────────────────────────

🟥 MUST CHANGE

backend/models/enrollment.py
  Symbol:       EnrollmentStatus.COMPLETED
  Evidence:     COMPLETED = "completed" — member name and stored string both
                carry the old name.
  Confidence:   High

⚠️ HIDDEN COUPLING

backend/reports/completion_report.py
  Coupling type: Raw SQL
  Evidence:      WHERE status = 'completed' — never touches the enum.
  Confidence:    High
  Action:        Silently returns zero rows after the rename.

backend/jobs/nightly_sync.py
  Coupling type: Raw string + direct data access
  Evidence:      if row["status"] == "completed" — bypasses the service layer.
  Confidence:    High

RISK

Risk score: 15 / 18 → High

Breadth             3   backend, frontend, jobs, and reporting all in scope
Coupling opacity    3   raw SQL, a direct-read job, a duplicated UI comparison
Test coverage       3   no test asserts report or sync behavior for this status
Reversibility       2   value rename with a backfill of existing rows
Consumer reach      3   a partner system reads the value; BI consumers are
                        suspected and not enumerable from this repository
Area volatility     1   normal churn, except one stale job

Nothing in CI fails if the string-coupled paths are missed.
```

Findings carry stable ids, so the architecture graph, the risk table, and the
implementation plan all point back at the same evidence. Say yes to the plan and
you get a handoff artifact — steps sized to one commit, each naming what it
resolves, how to verify it, and how to roll it back, with a coverage table
proving no MUST CHANGE finding was dropped.

Five full worked examples: [simple](skills/impact-map/examples/simple-change.md) ·
[API](skills/impact-map/examples/api-change.md) ·
[database](skills/impact-map/examples/database-change.md) ·
[cross-module](skills/impact-map/examples/cross-module-change.md) ·
[implementation plan](skills/impact-map/examples/implementation-plan.md)

---

---

# ProofBuild

**Don't read what the AI did. See whether it actually works.**

```bash
npx skills add soumyaRauth/skills-hub --skill proof-driven-dev
```

## The problem

```
prompt → code → explanation → you read all of it → you decide whether it works
```

You ask for password reset. You get working-looking code and a fluent paragraph
about it. Whether the feature *works* is still your problem, and the only ways
to find out are reading the diff or shipping it.

The failure is structural, not a matter of the agent trying harder: **"code was
written" and "the outcome happened" are different claims**, and one is being
reported as the other.

## The solution

An outcome contract, written *before* the code, and evidence for every
requirement in it:

```
intent → outcome contract → proof plan → implementation
       → verification → failure analysis → repair → re-verification → result
```

The contract is numbered and observable — someone outside the codebase could
tell whether each line holds:

```
objective: "Users can securely reset their password by email"
risk: high
  AUTH-001  A user can request a reset for their email          integration
  AUTH-003  An unknown email returns the same response          security
  AUTH-005  A token already used once is rejected on reuse      security
  AUTH-007  After reset, the old password no longer works       integration
  AUTH-008  Existing email/password login is unchanged          regression
```

Five of those eight were never in the request. That is where the defects live.

## Example

```
✓ VERIFIED

Password reset

Requirements   8/8
Tests          47/47
Regression     pass
Changed        6 files
```

That is the whole response for a change touching six files. When a decision is
genuinely yours, you get the decision instead of the narrative:

```
⚠ REVIEW REQUIRED

Bulk upload · 13/14 requirements verified

Decision required:
A duplicate filename inside one upload batch —

  [overwrite]   [reject the duplicate]   [keep both, suffix the name]
```

Detail is one question away — *show the contract*, *show evidence*, *explain the
proof for AUTH-005*, *show failed attempts*. What you never get is a green
checkmark meaning "I wrote some code and it looked right to me."

## The rule that matters most

When the agent's model of the code and the executed output disagree, the output
wins:

```
Reasoning   "the token is invalidated after use — consumeToken() sets used_at"
Observed    the same token reset the password twice, both returning 200

✗ CONTRADICTION — AUTH-005 is not satisfied
```

A confident, articulate, wrong claim of success is the most damaging thing an AI
agent produces. Repair is classified before any code changes and budgeted — three
attempts, two at high risk, one at critical — so a stubborn failure ends in
`✗ BLOCKED` with a diagnosis rather than a fourth guess.

Six worked examples: [feature development](skills/proof-driven-dev/examples/feature-development.md) ·
[bug fix](skills/proof-driven-dev/examples/bug-fix.md) ·
[refactoring](skills/proof-driven-dev/examples/refactoring.md) ·
[performance](skills/proof-driven-dev/examples/performance.md) ·
[security](skills/proof-driven-dev/examples/security.md) ·
[ambiguous request](skills/proof-driven-dev/examples/ambiguous-request.md)

## Safety

It runs your project's own checks — its framework, its commands, its
conventions — and does not install a testing stack you did not ask for. It will
not `git reset --hard`, `git clean -fd`, check out over your uncommitted work,
force push, commit or push automatically, drop databases, or touch production,
unless you explicitly ask for that operation.

**[Full documentation →](skills/proof-driven-dev/README.md)**

---

---

# Production Guard

**An AI-assisted production-readiness gate for software changes.**

> AI can write the code. Production Guard asks whether the resulting behavior is
> safe to ship.

## The problem

```
code generation ≠ production correctness
```

A change can pass its tests, compile, look reasonable, satisfy the ticket — and
still break an existing workflow, expose another tenant's data, corrupt records
under concurrency, double-charge on retry, time out at real data volumes,
silently swallow errors, or leave no trace of what it did at 3 AM.

## The solution

```
CODE CHANGE → behavior model → regression model → failure model
            → security / data / performance / operations
            → execute available validation
            → PRODUCTION READINESS REPORT
            → SHIP / CONDITIONAL SHIP / DO NOT SHIP
```

Two rules make the report worth reading:

**No invented scores.** Never `Code quality: 94%`. Instead, counts of checks
actually performed, and a verdict derived from explicit rules:

```
FUNCTIONAL VALIDATION     14/14 passed
REGRESSION VALIDATION     21/23 passed
SECURITY                   8/8  passed
DATA INTEGRITY             5/6  passed
FAILURE SCENARIOS          6/9  validated
```

**Executed ≠ analyzed.** Every check is labeled as a command that ran or as
reasoning, and a failure scenario only gets an observed result when it was
actually exercised.

| Verdict | Rule |
| --- | --- |
| 🟢 **SHIP** | No blockers, no unresolved HIGH findings, all risk-required categories validated |
| 🟠 **CONDITIONAL SHIP** | No blockers, but a HIGH finding or a required category left unverified |
| 🔴 **DO NOT SHIP** | At least one BLOCKER |

## Example

```
CHANGE    Add bulk deletion to user management.
VERDICT   🔴 DO NOT SHIP
BLOCKERS  2   HIGH 2   MEDIUM 1   LOW 1

🔴 #1 Authorization is checked once for the actor, never per target.
      Evidence:  BulkDeleteController.php:34 authorizes once, then deletes every
                 id in the request body. The single-delete path checks per record.
      Risk:      A team admin can delete users outside their team by supplying ids.

🔴 #2 Partial failure leaves the operation half-applied with no record.
      Evidence:  BulkDeleteService.php:28-41 commits per item inside a loop.
      Risk:      Failure at item 47 of 100 leaves an arbitrary subset deleted,
                 with no way to tell which or to safely retry.
```

Five full worked reports: [payment](skills/production-guard/examples/payment.md) ·
[bulk operation](skills/production-guard/examples/bulk-operation.md) ·
[API change](skills/production-guard/examples/api-change.md) ·
[database migration](skills/production-guard/examples/database-migration.md) ·
[authentication](skills/production-guard/examples/authentication.md)

One ends in 🟢 SHIP deliberately — a gate that never passes anything is not a
gate.

## Safety

Production Guard runs your project's own checks where it can. It will not drop
databases, reset environments, delete data, destroy containers, rewrite git
history, force push, deploy, or touch production-like systems. It reads git
state and never modifies it.

**[Full documentation →](skills/production-guard/README.md)**

---

---

# Practical Localizer

**Make your application speak like a local product — not like a translated
document.**

> Traditional translation asks: *"what does this sentence translate to?"*
> Practical Localizer asks: *"what would a real user expect this application to
> say here?"*

## The problem

A technically correct translation is not necessarily a natural one.

```
English:   Chair
Literal:   a dictionary-valid, formal/literary word
Practical: the borrowed word people actually use for the object
```

Both are "the translation". Only one sounds like a modern app — and which one
that is differs by language, product and audience. The same reasoning gives the
*opposite* answer in a neighbouring language where an ordinary native word is in
everyday use, which is exactly why no blanket rule works.

And the failure is rarely only stylistic:

```
"Hello, {{name}}"  →  "হ্যালো"          the placeholder is gone; nothing fails
t("remove")        →  "delete forever"  the handler was removeMember()
one concept        →  three target words, one per translation batch
{count, plural,…}  →  a single fixed form in a locale that needs six
```

## The solution

```
source application → localization architecture → language usage profile
   → existing terminology → context extraction → translation strategy
   → natural localization → technical validation → consistency review
```

Every meaningful term is classified — **TRANSLATE**, **TRANSLITERATE**,
**PRESERVE** or **ADAPT** — from context, existing project terminology and the
target locale's software conventions, and every non-trivial decision carries a
confidence level so the parts a human should check are visible.

Three modes: **analyze** (read-only inventory and plan), **localize** (writes
locale resources and nothing else), **review** (findings with source, current,
recommended, reason and confidence).

## Example

```
You:  Review the Bengali localization for naturalness and consistency.

Agent: LOCALIZATION REVIEW
       ────────────────────────────────
       Target  Bengali (bn-BD)   Reviewed  742 strings
       High-confidence 18 · Medium 27 · Technical 3

       #1  greeting.hello — BLOCKING TECHNICAL ISSUE
           Source "Hello, {{name}}" → current "হ্যালো"
           The interpolation was dropped; the name never renders.

       #2  team.remove — Context / terminology
           Current মুছে ফেলুন ("erase") → recommended সরিয়ে দিন
           Rendered in <TeamMemberRow>, handler removeMember(). The member is
           taken off the team, not deleted. Bengali distinguishes the two;
           English does not.

       #3  sign in — Terminology inconsistency
           লগইন (18 occurrences) · প্রবেশ করুন (2 occurrences)
           Recommend the established project term everywhere.
```

Five worked language examples: [Bengali](skills/practical-localizer/examples/bengali.md) ·
[Hindi](skills/practical-localizer/examples/hindi.md) ·
[Japanese](skills/practical-localizer/examples/japanese.md) ·
[Arabic](skills/practical-localizer/examples/arabic.md) ·
[European](skills/practical-localizer/examples/european-language.md)

## What it will not do

Never claim native authority — "this is the more common software convention",
not "native speakers say this". Never guess grammatical gender the source hides.
Never encode "language X always …". Never invent counts or claim a validation it
did not run. Never touch application source: hardcoded strings, concatenated
sentences and formatter bugs are reported, not silently refactored.

**[Full documentation →](skills/practical-localizer/README.md)**

---

# Engineering Investigator

**Don't ask the agent to find an explanation. Make it find out whether the
explanation is true.**

```bash
npx skills add soumyaRauth/skills-hub --skill engineering-investigator
```

Ask a coding agent why the app is slow and it will read the code, find something
genuinely suspicious, and tell you about it. That is the problem: *finding an
explanation* and *establishing a cause* are different activities, and one gets
delivered as the other. The query may have been there for two years, and the
affected customer may be on hotel wifi.

```
complaint → normalize the symptom → scope it by contrast → competing hypotheses,
each with a kill condition → the experiment that eliminates the most → what
survived, at its real confidence → verify → four lines
```

## Example

```
You:  The portal is unusably slow for one customer. They're threatening to churn.

Agent: Server processing for that account matches every other tenant (p95 210 ms
       vs 228 ms) and their response sizes are comparable, so the time is not in
       our processing. Their own network capture shows 6.4 s downloading a
       1.7 MB response with 173 ms of server time and 310 ms of browser work.

## Result

The application is responding normally for this customer — the time is going
into transferring data over their connection.

**Cause:** Low throughput on the affected connection (~2 Mbit/s)
**Confidence:** High

**Why:** Server times match every other tenant, sizes are comparable, and their
capture shows the time in transfer.

**Action:** Have them test on a different network. Separately, our dashboard
response is 1.7 MB — worth reducing, because it is what makes a weak connection
unusable rather than merely slow.

### Client response

"We've looked into the slowness and our systems are responding normally for your
account… "
```

Every hypothesis carries a **kill condition**, written before the evidence
arrives. Experiments are chosen for how many explanations they can eliminate,
not for how thorough they look. Evidence is typed `FACT` / `INFERENCE` /
`ASSUMPTION` / `UNKNOWN`, and code inspection never establishes production
behavior. The leading hypothesis gets attacked before the conclusion is written.

Depth is bought in the investigation state, never in the answer. A finalization
gate runs before you see anything: it keeps the evidence that *changed* the
conclusion and deletes the rest — no command counts, no file-by-file tour, no
`H1…H5` manufactured for a request that arrived with its own answer. Detail is
one question away, and is read back out of the state rather than re-derived.

Six worked investigations: [client network](skills/engineering-investigator/examples/client-network.md) ·
[deployment regression](skills/engineering-investigator/examples/deployment-regression.md) ·
[third-party dependency](skills/engineering-investigator/examples/third-party-dependency.md) ·
[insufficient evidence](skills/engineering-investigator/examples/insufficient-evidence.md) ·
[resuming a case](skills/engineering-investigator/examples/resumed-investigation.md) ·
[a clear feature request](skills/engineering-investigator/examples/implementation-request.md)

## What it will not do

Never invent a log line, a metric, a trace, a tool, or a customer's network
conditions — unavailable evidence is reported as unavailable. Never report
correlation with a deploy as a cause without a comparison that establishes it.
Never blame a customer, a vendor, or the network without a measurement, and never
blame the application without one either. Read-only by default: production data,
configuration, infrastructure and deployments are never touched without explicit
authorization for that specific action.

**[Full documentation →](skills/engineering-investigator/README.md)**

---

# Project Compass

**Your agent knows how to build things. This helps it understand where the
project is going.**

```bash
npx skills add soumyaRauth/skills-hub --skill project-compass
```

Coding agents execute well. Ask for search, a refactor, another permission
check, a dashboard — you get all of them, competently, one after another. That
is the whole problem: execution never asks whether the sequence adds up.

```
ACTIVITY   features added, code refactored, endpoints optimized
PROGRESS   the target problem solved, a real risk retired, a workflow completed
```

These come apart quietly. Nine permission exceptions, each reasonable, are an
authorization system nobody designed. Four fixes for four kinds of duplicate are
one missing idea about identity. Five performance changes with no measurement
anywhere are five guesses with deployments attached. The person making the
requests cannot see it — they see one request.

```
Normal coding agent          Project Compass

request                      request
  ↓                            ↓
implementation               project state — what is known, decided, recorded
                               ↓
                             does this fit the trajectory?
                               ↓
                             does it depend on something unresolved?
                               ↓
                             has this pattern happened three times?
                               ↓
                             is it worth interrupting for?   ── almost always no
                               ↓
                             implementation
```

## Example

```
You:    Add CSV export to the members table.

Agent:  Export added — all visible columns, respecting the current filter and
        sort, streamed so large orgs don't time out.

        One thing I'd flag. That's six controls on this table since August:
        search, filters, sorting, saved views, bulk actions, now export. Each
        made sense on its own, but they're pointing at a workflow nobody has
        written down — and it's already showing: saved views track role, status
        and joined date, bulk actions work on role and active, and export just
        took everything.

        Before the seventh, one sentence would settle it: who opens this screen,
        and what are they trying to finish? If it's "support checks whether
        someone still has access", the table needs three columns and a search
        box and half of what's there is in the way. If it's "an admin does
        quarterly access reviews", export is the main event and should probably
        be scheduled rather than clicked.
```

Nothing was refused, and the export was built and tested. The observation is
checkable in thirty seconds — six controls, five dates, three inconsistent
column sets.

## The harder half: knowing when to shut up

An agent that comments on direction four times a week gets uninstalled in week
two, and the one real observation it would have made in week nine never arrives.
So a pattern is reportable only when it clears **four gates** — three or more
instances with real locations, a shared *cause* rather than a shared topic, a
consequence stated in terms of work already asked for, and a next step smaller
than the work it prevents. Three out of four is a note in the project state, not
a sentence to you.

On top of that: one interruption per session, maximum, and

> **a dismissed observation is closed permanently.**

Say *"that's intentional"* and it is recorded as a decision with your reason,
and never raised again — not next week, not in different wording.

## What it remembers

```
.project-compass/
├── project.md          what this is, who it serves — labeled, dated
├── trajectory.md       dated entries: what changed, and which pattern it fed
├── decisions.md        settled questions, including "we discussed this, proceed"
├── open-questions.md   unresolved decisions affecting implementation
└── blind-spots.md      patterns that cleared the bar, and what closes them
```

This is the difference between the skill and asking an agent *"what am I
missing?"* — that question gets a fresh guess from nothing, every time. Renames,
formatting and dependency bumps are never recorded; a trajectory that logs
everything is a diary, and nobody finds a pattern in a diary. The repository
always outranks the state, and recorded claims are re-verified before anything
is built on them.

Seven worked sessions: [no intervention](skills/project-compass/examples/no-intervention.md) ·
[feature accumulation](skills/project-compass/examples/feature-accumulation.md) ·
[decision debt](skills/project-compass/examples/decision-debt.md) ·
[a drifting project](skills/project-compass/examples/drifting-project.md) ·
[what should I do next](skills/project-compass/examples/next-action.md) ·
[beginner](skills/project-compass/examples/beginner.md) ·
[senior](skills/project-compass/examples/senior.md)

## What it will not do

Never invent the project's purpose, users, market, deadlines, metrics, or
history — when the objective is undocumented, *"there is no documented
objective"* is the finding. Never block ordinary work: even a redirect ends with
the offer to build it as asked, because you have context the repository does
not. Never raise a dismissed observation again. Never produce a health score, a
percentage, or a generic backlog. Most of the time it says nothing at all, and
its second most common answer is *keep going*.

**[Full documentation →](skills/project-compass/README.md)**

---

# Standards Compass

**Which standards actually apply to this software — and does it meet them?**

Standards Compass is an [Agent Skill](https://code.claude.com/docs/en/skills)
for the question nobody asks until month eight: *are we compliant?* — at which
point nobody can say what "compliant" would mean for this product.

```bash
npx skills add soumyaRauth/skills-hub --skill standards-compass
```

The instinct is a checklist. Five hundred requirements produce five hundred
shallow answers, most of them irrelevant, and a team that now believes standards
work is theatre. The value is in the two steps a checklist skips:

```
Which of these applies to this software?
And what does the code actually show?
```

So it profiles the project, decides applicability with reasons — including for
the standards that do **not** apply — gathers evidence, and reports gaps that
carry their citations:

```
Applicable
  ✓ OWASP ASVS 5.0.0        authenticated multi-tenant app, untrusted input
  ✓ WCAG 2.2                public web UI with interactive workflows
  ⚠ GDPR                    personal data present; jurisdiction unknown
  ⚠ PCI DSS v4.x            hosted checkout; scope determined with your acquirer
  ✕ HIPAA                   no clinical data or healthcare relationship observed

🔴 3 high   🟠 8 medium   🟡 6 unable to verify

Three admin endpoints don't enforce the authorization rule the other eleven
use, and the export query at src/api/admin/exports.ts:31 has no tenant filter.
```

Two modes: an **auditor** for software that already exists, and a **guardrail**
that runs during ordinary development — noticing when a feature touches
identity, privilege, money, personal data, files or a model, building
accordingly, and staying silent otherwise.

Three things make it usable rather than alarming:

- **Not found is not failed.** No backup config in the repository means *no
  backup config was found in the repository*. That is `UNABLE TO VERIFY`, routed
  to whoever runs the infrastructure — not a failure in a findings list.
- **Gaps are typed.** Implementation, evidence, process, legal scope, manual
  verification. A process gap has no code fix, and writing one to close it makes
  the next audit less accurate.
- **It never claims compliance.** Not GDPR, not ISO 27001, not WCAG conformance,
  not PCI. None of those is available from reading a repository, and all of them
  get quoted to customers.

The registry is designed to be updated without touching the skill — one YAML
file per standard, 22 of them, each recording its version, status, official
source, and **when and how it was last verified**. `scripts/validate-registry.sh`
enforces the schema, including that an official URL sits on the publishing
body's own domain.

State in `.project-standards/` makes the second assessment cheaper than the
first, keeps a dismissed finding dismissed, and turns a control that used to
pass into a **regression** rather than a rediscovery.

[Read the full guide →](skills/standards-compass/README.md)

---

## Installation

```bash
# any Agent Skills-compatible agent
npx skills add soumyaRauth/skills-hub --skill impact-map
npx skills add soumyaRauth/skills-hub --skill proof-driven-dev
npx skills add soumyaRauth/skills-hub --skill production-guard
npx skills add soumyaRauth/skills-hub --skill practical-localizer
npx skills add soumyaRauth/skills-hub --skill engineering-investigator
npx skills add soumyaRauth/skills-hub --skill project-compass
npx skills add soumyaRauth/skills-hub --skill standards-compass

# Claude Code specifically
npx skills add soumyaRauth/skills-hub --skill impact-map --agent claude-code
npx skills add soumyaRauth/skills-hub --skill proof-driven-dev --agent claude-code
npx skills add soumyaRauth/skills-hub --skill production-guard --agent claude-code
npx skills add soumyaRauth/skills-hub --skill practical-localizer --agent claude-code
npx skills add soumyaRauth/skills-hub --skill engineering-investigator --agent claude-code
npx skills add soumyaRauth/skills-hub --skill project-compass --agent claude-code
npx skills add soumyaRauth/skills-hub --skill standards-compass --agent claude-code
```

Then just ask for what it does — installed skills are matched by description, so
no slash command is needed:

```
What's the blast radius of adding an approval step to course completions?
Before you change anything, map the impact of renaming this status.
Is this payment flow safe to ship?
Analyze this app for Bengali localization.
Review the French locale — I think it reads like a translation.
What should I work on next?
What do you think I'm missing here?
Which standards actually apply to this project?
Audit this application against the standards that matter.
```

## Supported agents

These skills are plain Agent Skills markdown. They require **no MCP server, no
custom CLI, no hosted service, and no proprietary API** — only the repository
inspection an agent already has.

| Agent | Status |
| --- | --- |
| Claude Code | Primary target; installable via the Skills CLI |
| Other Agent Skills-compatible agents | Expected to work — the skill uses no agent-specific features |

If your agent supports the Agent Skills format and can read files and search a
repository, it can run these skills.

---

## Repository structure

```
.
├── skills/
│   ├── impact-map/
│   │   ├── SKILL.md              ← the skill itself
│   │   ├── README.md             ← human documentation
│   │   ├── references/           ← deeper guidance the agent consults on demand
│   │   └── examples/             ← four worked impact maps
│   ├── proof-driven-dev/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── references/           ← ten proof and verification references
│   │   ├── examples/             ← six worked proof-driven tasks
│   │   └── templates/            ← contract, proof plan, report
│   ├── production-guard/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── references/
│   │   └── examples/             ← five worked readiness reports
│   ├── practical-localizer/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── references/           ← ten localization references
│   │   ├── examples/             ← five worked language examples
│   │   └── templates/            ← glossary, locale profile, review report
│   ├── engineering-investigator/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── references/           ← eleven investigation references
│   │   └── examples/             ← six worked investigations
│   ├── project-compass/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── references/           ← eleven project-intelligence references
│   │   └── examples/             ← seven worked sessions, one of which says nothing
│   └── standards-compass/
│       ├── SKILL.md
│       ├── README.md
│       ├── references/           ← eighteen assessment references, plus a template
│       ├── registry/             ← the standards registry: add a file, add a standard
│       └── examples/             ← eight worked assessments, one that refuses to grade
├── tests/
│   ├── fixtures/
│   │   ├── impact-map/           ← four repositories with hidden coupling to find
│   │   ├── proof-driven-dev/     ← six runnable projects, green until you break them
│   │   ├── production-guard/     ← four repositories with real production bugs
│   │   ├── practical-localizer/  ← six repositories with bad localizations
│   │   ├── engineering-investigator/  ← five incidents with the evidence to solve them, plus one plain feature request
│   │   ├── project-compass/      ← five projects with a hidden pattern, plus one healthy project where the right answer is silence
│   │   └── standards-compass/    ← five projects to assess, including one where most of the honest answer is "unable to verify"
│   ├── longitudinal/             ← multi-step scenarios: behavior that only shows up across sessions
│   └── README.md                 ← expected findings per fixture
├── scripts/
│   ├── validate.sh               ← structure + frontmatter validation, all skills
│   └── validate-registry.sh      ← standards registry schema, ids, sources, dates
└── .github/workflows/validate.yml
```

## Documentation

- **[Impact Map](skills/impact-map/README.md)** · [SKILL.md](skills/impact-map/SKILL.md)
- **[ProofBuild](skills/proof-driven-dev/README.md)** · [SKILL.md](skills/proof-driven-dev/SKILL.md)
- **[Production Guard](skills/production-guard/README.md)** · [SKILL.md](skills/production-guard/SKILL.md)
- **[Practical Localizer](skills/practical-localizer/README.md)** · [SKILL.md](skills/practical-localizer/SKILL.md)
- **[Engineering Investigator](skills/engineering-investigator/README.md)** · [SKILL.md](skills/engineering-investigator/SKILL.md)
- **[Project Compass](skills/project-compass/README.md)** · [SKILL.md](skills/project-compass/SKILL.md)
- **[Standards Compass](skills/standards-compass/README.md)** · [SKILL.md](skills/standards-compass/SKILL.md)
- **[Testing](tests/README.md)** — fixtures and expected reasoning behavior
- **[Contributing](CONTRIBUTING.md)** — how to improve them safely

---

## Contributing

Improvements to the methodologies, framework guidance, examples, and fixtures
are all welcome. Two hard rules:

- **Do not make the skills more speculative.** A finding without evidence is
  worse than no finding — it costs the reader time and teaches them to distrust
  the report.
- **No invented numbers.** No fabricated file counts, no quality percentages, no
  claiming a check ran when it did not.

See [CONTRIBUTING.md](CONTRIBUTING.md). Run `./scripts/validate.sh` before
opening a pull request.

## Roadmap

Ideas, not commitments.

**Impact Map**

| Version | Focus | Status |
| --- | --- | --- |
| v0.2 | Better monorepo awareness; git history, ownership, and changed-file analysis | shipped |
| v0.3 | Architecture graph output, dependency visualization, risk scoring | shipped |
| v0.4 | Tighter implementation-plan handoff | shipped |

**Production Guard**

| Version | Focus |
| --- | --- |
| v0.2 | Change-aware validation driven by git diff |
| v0.3 | Assisted test generation for unverified scenarios |
| v0.4 | CI integration |
| v0.5 | PR comment and report generation |

**Practical Localizer**

| Version | Focus |
| --- | --- |
| v0.2 | Richer framework detection; glossary management; more locale profiles |
| v0.3 | Screenshot-aware localization, UI layout inspection, length analysis |
| v0.4 | Human review workflow and translation approval metadata |
| v0.5 | CI localization quality gate |

Possible companions: `localization-guard`, catching localization regressions in
CI, and `locale-maintainer`, detecting newly added untranslated strings.

**Proof-Driven Development**

| Version | Focus |
| --- | --- |
| v0.2 | Richer evidence formats; sharper risk classification; project-specific proof strategies |
| v0.3 | Screenshot-aware verification, browser evidence, stored performance baselines |
| v0.4 | CI integration; detecting when a previously proven requirement regresses |
| v0.5 | Reusable project-level proof contracts |

**Project Compass**

| Version | Focus |
| --- | --- |
| v0.2 | Richer pattern detectors; better inherited-history reconstruction from git |
| v0.3 | Cross-session calibration — learning which observations this team acts on |
| v0.4 | Team-shared project state, reviewable in a pull request |

**All of them**

A further skill, `change-guard`, closing the loop: take an Impact Map and a
Production Guard report and verify that the implementation actually covered the
identified surface and resolved the identified risks. Where ProofBuild proves
the outcome it defined, `change-guard` would check that outcome against a
*separately* derived surface — a different question, and a useful cross-check.

## Limitations

These skills are instruction-driven, not static analyzers. None claims
completeness, and none can prove it.

- Results vary with the agent, the repository, and how the request is phrased
- Dynamic dispatch, reflection, runtime configuration, and generated clients are
  where they are weakest
- They only see this repository — cross-repo consumers and external systems
  surface as open questions at best
- Large monorepos need scoping
- Impact Map does not run anything; Production Guard runs only what the local
  environment allows, and labels the rest unverified
- Practical Localizer is not a replacement for a native reviewer. It produces
  context-aware, evidence-driven localization designed to be more natural than
  literal translation — not guaranteed native-quality output, and it says where
  it is unsure
- Standards Compass reads a repository: production configuration, organizational
  process, contracts and legal applicability are outside it, and it says so
  rather than guessing. Its bundled registry ages, and every entry carries the
  date and method of its last verification
- An absent finding is not proof of absence

Production Guard improves the evidence available before shipping. It does not
guarantee production safety, and a human owns the release decision.

## License

[MIT](LICENSE)
