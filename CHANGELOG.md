# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this repository ships
instructions rather than executable code, so versions describe changes in
methodology and documentation.

## [Unreleased]

### Added

- `standards-compass` v0.1.0 — **software standards intelligence and compliance
  gap analysis.** Nobody decides which standards a product is built to, because
  the question never appears in a ticket. Eight months later someone asks whether
  the project is compliant, and nobody can say what compliant would mean for this
  product. The reflex at that point is a checklist, which produces five hundred
  shallow answers, most of them irrelevant, and a team that concludes standards
  work is theatre.

  So the skill is built around the two steps a checklist skips: **which of these
  applies to this software**, and **what does the code actually show**. It
  profiles the project, assigns each candidate standard one of five applicability
  states with a rationale and a scope — including `NOT CURRENTLY INDICATED`, with
  the reason, because ruling PCI DSS out for a hosted-checkout merchant saves
  more work than most findings create — then gathers evidence, assesses, and
  reports.

  Two modes from one machine. **Auditor** for software that already exists:
  profile, applicability, targeted evidence collection in risk order, prioritized
  gaps, and an explicit list of what could not be verified. **Guardrail** during
  ordinary development: a cheap pass on every request, silence for the ones that
  touch nothing, and for the rest a short note naming what the implementation
  will account for, then the work, then a four-line check. A rename gets nothing.
  A bulk customer export gets authorization, tenant scoping and an audit record
  before anyone asks.

  The distinctions that make it trustworthy are all separations other tools
  collapse. Status has six values, not two, and **absence of evidence is
  `UNABLE TO VERIFY`, never `FAIL`** — no backup configuration in a repository
  means none was found in a repository. Every gap is typed as implementation,
  evidence, process, legal scope, or manual verification, which determines who
  can act: a process gap has no code fix, and writing one to close it makes the
  next audit less accurate. Severity and confidence are independent, so a serious
  finding on partial evidence reads as `HIGH` severity, `MEDIUM` confidence, and
  says what would settle it. And the standard, the law, the framework and the
  certification are four different objects that the report is never allowed to
  blur.

  Above all: **it never claims compliance or certification.** Not GDPR, not ISO
  27001, not WCAG conformance, not PCI. None is available from reading a
  repository, and all of them get quoted to customers.

  Findings are made against 36 normalized controls rather than against standards,
  so one missing authorization check is one finding with five references
  underneath it instead of five copies. Standards entries name their controls;
  nothing maps back, so adding a standard extends every control it touches with
  no mapping table to drift.

  The registry is 22 entries across nine categories — ASVS 5.0.0, OWASP Top
  10:2025, API Security Top 10, MASVS, NIST CSF 2.0, SSDF, ISO/IEC 27001:2022,
  ISO/IEC 25010:2023, WCAG 2.2, EN 301 549 V4.1.1, ISO/IEC/IEEE 12207:2017, GDPR,
  CCPA/CPRA with the 2026 ADMT and risk-assessment regulations, ISO/IEC
  27701:2025, ISO/IEC 42001:2023, NIST AI RMF, the EU AI Act, the OWASP GenAI LLM
  Top 10 (2026), PCI DSS v4.0.1, SOC 2, the HIPAA Security Rule, and CIS
  Benchmarks. Seventeen were verified against the publishing body's own site on
  2026-09-07; five are marked as carried from bundled knowledge, because a
  falsely verified entry is worse than an honestly unverified one. No copyrighted
  standard text is stored — names, identifiers, versions, official links,
  applicability and original summaries only.

  `scripts/validate-registry.sh` reads the schema out of `registry.yaml` rather
  than hardcoding it, so adding a category or an authority is a registry edit.
  It enforces unique ids, required and unknown fields, enum membership,
  category-directory agreement, date formats and future dates, control references
  that resolve, verification sources that exist when claimed, and — the check
  that matters most — that an `official_url` sits on a domain belonging to the
  body that publishes the standard, so a vendor blog cannot become a citation.

  State in `.project-standards/` buys three things a one-shot audit cannot have:
  a dismissed finding stays dismissed, the second assessment is cheaper than the
  first, and a control that used to pass is reported as a **regression** with the
  commit that caused it rather than rediscovered as a new problem.

  Eighteen references plus an internal-standards template, eight worked examples
  — including one that refuses to produce a posture from an infrastructure-only
  repository, and one that tells a beginner which four standards to ignore
  entirely. Five fixtures under `tests/fixtures/standards-compass/`, five
  multi-step scenarios in `tests/longitudinal/standards-compass.md`, and a table
  of anti-tests scored purely on absence, because for this skill the worst
  available failure is a confident sentence somebody forwards to their auditor.

- `project-compass` v0.1.0 — **persistent project intelligence.** A skill for
  the gap between *activity* and *progress*: an agent executes each request
  competently and nothing ever reads the requests as a sequence. Nine permission
  exceptions, each reasonable, are an authorization system nobody designed; four
  fixes for four kinds of duplicate are one missing idea about identity; five
  performance changes with no measurement are five guesses with deployments
  attached. The person making the requests cannot see it, because they make them
  one at a time.

  State lives in `.project-compass/` — a labeled project model, a trajectory of
  what actually changed, decisions, open questions, and blind spots that cleared
  the bar. That persistence is the design: *"what am I missing?"* asked of a
  stateless agent gets a fresh guess every time, and this accumulates instead.

  The harder half is restraint, so intervention is gated rather than judged.
  A pattern is reportable only when it clears four gates — **recurrence** (three
  or more instances, each with a nameable location), **convergence** (a shared
  cause, not a shared topic), **consequence** (what breaks next, in terms of work
  already asked for), and **actionability** (a step smaller than the work it
  prevents). Two exceptions fire on a single instance: irreversibility and
  contradiction of a recorded decision. On top of that, one interruption per
  session, and **a dismissed observation is closed permanently** — recorded as a
  decision with the user's own reason, never raised again in any wording. That
  last rule is what makes the skill survivable past month two.

  Four engineering states (`FORMING` · `DIRECTED` · `EXPLORATORY` · `DRIFTING`),
  with exploration suppressing drift detection outright; four evidence labels
  (`OBSERVED` · `INFERRED` · `ASSUMED` · `UNKNOWN`) on every claim, including the
  project's objective, which is frequently `UNKNOWN` and is reported as such
  rather than invented. Ten blind-spot detectors, each with the evidence it
  requires. Eleven references, seven worked examples — one of which is entirely
  about the requests that earn no commentary at all.

  Six fixtures under `tests/fixtures/project-compass/`, three seeded with a
  `.project-compass/` directory holding evidence rather than conclusions, plus
  `directed-project`, a healthy repository whose correct output is silence.
  Six multi-step scenarios in `tests/longitudinal/project-compass.md`, because a
  single-prompt test cannot measure a skill whose claim is that it improves
  across sessions.

### Changed

- `engineering-investigator` v0.2 — **routing and a finalization gate.** Two
  correctives, both to the layer between the investigation and the reader.
  *Routing:* a new first stage asks how many explanations are actually live, and
  a fourth lane — **DIRECT** — handles requests that name their own change
  (*"only CSV upload is allowed, I need XLSX too"*) without normalizing a
  symptom or manufacturing `H1…H5` for a question that arrived with its answer.
  DIRECT keeps the discipline that matters — read the real path, reuse what
  exists, verify, never claim a check that did not run — and skips the
  hypothesis machinery, which exists to discriminate between competitors and has
  nothing to do when there is one. *Finalization:* Phase 9 is now a gate rather
  than a template. It answers four questions (what was established, which
  evidence *changed* the conclusion, how confident, what happens next), then
  runs six checks over the draft — narration compressed, tool activity deleted,
  unasked-for implementation detail reduced to a clause, internal reasoning
  dropped, one screen as the target. A new rule forbids reporting agent activity
  at all: no counts of commands run, files read, patterns searched, or context
  files loaded, during the work as well as at the end. `### Client response` is
  now explicitly conditional on somebody outside the team waiting for one.
  Three things are never compressed away: a decision the user must make, a check
  that could not be run, and a second contributing cause. Detail on demand is
  specified as *retrieval* from the investigation state — the state itself is
  unchanged, and remains the memory of the case. New example
  `implementation-request.md`; new runnable fixture
  `tests/fixtures/engineering-investigator/csv-upload-only`; response-quality
  and routing checks added to the scoring tables in `tests/README.md`

### Added

- `engineering-investigator` skill v0.1 — **evidence-driven investigation of
  vague engineering complaints.** A report is treated as a symptom, not a
  diagnosis: it is normalized into an investigation statement with typed unknown
  slots, scoped by contrast (affected vs unaffected, version vs version, region
  vs region), and turned into three to six competing hypotheses, each carrying a
  **kill condition written before any evidence is collected**. The next action is
  chosen by discriminating power over cost rather than by how much code is left
  to read, and every observation is typed `FACT`, `INFERENCE`, `ASSUMPTION`, or
  `UNKNOWN` with its provenance. Root cause is graded `CONFIRMED` /
  `HIGHLY LIKELY` / `LIKELY` / `POSSIBLE` / `UNKNOWN`, where timing correlation
  with a deploy earns `LIKELY` at best until a reproduction, version comparison,
  or revert promotes it. The skill can conclude that the application is **not**
  responsible — but only with our side healthy in the same window, an unaffected
  comparison, and a measurement of the external factor. Read-only by default:
  every action is `OBSERVE`, `REPRODUCE`, or `MUTATE`, and mutations require
  explicit authorization for that specific action. Three investigation depths
  (QUICK / STANDARD / INCIDENT) and explicit stop conditions keep cost
  proportional; an optional `.agent-investigation/` workspace carries the ledger
  across sessions so "continue the investigation" resumes a case instead of
  restarting it. Output is a one-screen result with a confidence level plus a
  jargon-free client paragraph. Eleven references, five worked examples, and five
  test fixtures that ship the evidence — access logs, a worker log, a support
  ticket, a deploy log — needed to reach the documented conclusions
- `proof-driven-dev` skill (ProofBuild) v0.1 — **outcome contracts instead of
  implementation explanations.** A development request becomes a numbered
  outcome contract *before* any code is written; each requirement carries the
  proof mechanism that will establish it; verification runs in escalating stages
  (static → targeted → integration → broad); failures are classified
  (`IMPLEMENTATION_ERROR`, `TEST_ERROR`, `CONTRACT_ERROR`, `ENVIRONMENT_ERROR`,
  `EXISTING_REGRESSION`, `UNRELATED_FAILURE`, `UNKNOWN`) before any repair, and
  repair is budgeted — 3 attempts, 2 at high risk, 1 at critical — so the loop
  terminates in `✗ BLOCKED` rather than recursing. Evidence is traced per
  requirement and graded A–D, where D means human judgment and never rounds up
  to verified. The developer-facing output is one of `✓ VERIFIED`,
  `⚠ REVIEW REQUIRED`, `✗ BLOCKED`, with detail available on request. Optional
  `.proofbuild/` artifacts (contract, proof plan, per-requirement evidence,
  report, history) carry proof across sessions, with secrets redacted by shape.
  Ten references, six worked examples, three templates, and six runnable
  zero-dependency fixtures
- `impact-map` v0.2 — **monorepo awareness, history, and diff-driven analysis.**
  Phase 2 scopes a workspace by its package graph rather than by directory
  proximity and reports what it did *not* inspect; a new Phase 5 reads git for
  co-change coupling, churn, and `CODEOWNERS` routing; Phase 1 accepts a diff,
  branch, or commit range as the change source and reports the surface a change
  touches but has not visited. New report sections `REPOSITORY SCOPE` and
  `HISTORY & OWNERSHIP`; new coupling type: temporal (co-change), capped at
  Medium confidence because history proves correlation, not causation. New
  references: `git-signals.md`, `monorepo.md`
- `impact-map` v0.3 — **architecture graph and scored risk.** Findings carry
  stable ids (`F1`, `F2`, …); a new `ARCHITECTURE GRAPH` section renders the
  surface as a mermaid flowchart with one subgraph per real layer, labelled
  edges, and solid/dashed marking hard versus soft coupling — rendering only
  findings already in the report. `RISK` becomes a six-factor rubric (breadth,
  coupling opacity, test coverage, reversibility, consumer reach, area
  volatility) scored 0–3 each with the observation that set it; unassessable
  factors are scored `?` and make the total a lower bound. New references:
  `architecture-graph.md`, `risk-scoring.md`
- `impact-map` v0.4 — **implementation-plan handoff.** The plan is now a defined
  artifact executable by a session that never saw the analysis: per-step files,
  resolved finding ids, dependencies, evidence, verification, and rollback, plus
  a closing coverage table where every 🟥 maps to exactly one step and 🟨
  findings become prerequisites. Ordering rules keep every step deployable on
  its own, and drift is reported rather than silently re-planned. New reference
  `implementation-plan.md` and a fifth worked example, `implementation-plan.md`

### Changed

- `scripts/validate.sh` executes the fixtures that are meant to run
  (`tests/fixtures/proof-driven-dev/`) and fails when one is red; it skips the
  check when Node is unavailable
- The repository ships five skills; the hub table, install commands, and the
  composition diagram in the top-level README now route
  `impact-map → proof-driven-dev → production-guard`, with
  `incident → engineering-investigator → cause` as a second entry point
- Impact Map's workflow is 12 phases (was 11); the four existing examples carry
  finding ids and scored risk tables, and the cross-module example gains an
  architecture graph and a history-and-ownership section

## [0.3.0] — 2026-08-23

### Added

- `practical-localizer` skill: a context-aware application localization
  methodology with three modes — ANALYZE (read-only inventory and plan),
  LOCALIZE (writes localization resources only), REVIEW (findings with
  recommendations)
- Four-way strategy classification per term — translate, transliterate,
  preserve, adapt — chosen from context, existing project terminology and the
  target locale's software conventions rather than from a blanket rule
- Blocking technical validation: placeholder parity across every syntax
  (`{name}`, `{{name}}`, `%s`, `%1$s`, `:name`, `<0>…</0>`), plural-category
  coverage per locale, key and structure preservation. Placeholder *order* is
  deliberately not checked, because verb-final languages move the interpolation
- Terminology management and translation memory: established project terms win
  over new synonyms, and conflicts are reported with occurrence counts
- Explicit prohibition on native-authority claims and blanket language rules;
  HIGH/MEDIUM/LOW confidence on every non-trivial decision
- References: localization workflow, translation strategy, terminology, context
  analysis, pluralization, locale formatting, RTL, UI fit, confidence, review
  methodology
- Templates: `glossary.yml`, `locale-profile.yml`, `review-report.md`
- Five worked language examples: Bengali, Hindi, Japanese, Arabic, and a
  European three-language pass — each stating what it does not claim
- Six test fixtures with intentionally bad localizations (`basic-json`,
  `nextjs`, `react`, `laravel`, `i18next`, `mixed-localization`) and documented
  expected findings

### Changed

- `scripts/validate.sh` validates a skill's `templates/` directory when one is
  present
- Top-level README, `tests/README.md` and `CONTRIBUTING.md` cover three skills;
  CONTRIBUTING gains a third hard rule against unsupported linguistic claims
- Documentation site gains a Practical Localizer page

## [0.2.0] — 2026-08-20

### Added

- `production-guard` skill: a 14-phase production-readiness validation workflow
  producing a report that ends in 🟢 SHIP, 🟠 CONDITIONAL SHIP, or 🔴 DO NOT SHIP
- Verdict derived from explicit rules rather than judgement; four-level severity
  (blocker, high, medium, low) with evidence, confidence, and recommendation on
  every finding
- Mandatory `EXECUTED` vs `ANALYZED` labelling, so reasoning is never presented
  as an observed test result
- Baseline establishment, so pre-existing failures are never blamed on the change
- Explicit prohibition on invented quality scores, enforced by the validator
- Risk-based depth (low / medium / high) selecting which categories run
- References: behavioral validation, failure analysis, security validation, data
  integrity, performance, observability, report schema, change-type checklists
- Team customization template (`team-standards.template.md`)
- Five worked examples: payment, bulk operation, API change, database migration,
  authentication — one ending in SHIP
- Four test fixtures containing intentional production bugs (payment,
  bulk-operation, api, migration) with documented expected findings

### Changed

- Fixtures are now grouped per skill: `tests/fixtures/<skill>/<name>/`
- `scripts/validate.sh` discovers every skill under `skills/` instead of
  hardcoding one; adds orphan-reference, invented-score, and per-skill fixture
  checks
- Top-level README is now a two-skill catalog
- `tests/README.md` and `CONTRIBUTING.md` cover both skills

## [0.1.0] — 2026-08-20

Initial release.

### Added

- `impact-map` skill: an 11-phase read-only blast-radius analysis workflow
  producing an evidence-based impact report
- Five-way finding classification (must change, likely affected, needs
  verification, hidden coupling, out of scope) with separate High/Medium/Low
  confidence tracking
- Hidden-coupling analysis: raw strings, raw SQL, direct data access, duplicated
  business logic, configuration, events, jobs, serialization, fixtures,
  generated code, documentation
- Normal and deep analysis modes
- Reference documents: report schema, dependency analysis, hidden coupling,
  framework detection
- Team customization template (`company-architecture.template.md`)
- Four worked examples: simple business logic, API response, database schema,
  cross-module enterprise workflow
- Four test fixtures (`simple-node`, `nextjs`, `laravel`, `mixed-architecture`)
  with documented expected findings
- `scripts/validate.sh` and a GitHub Actions workflow running it

[Unreleased]: https://github.com/soumyaRauth/skills-hub/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/soumyaRauth/skills-hub/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/soumyaRauth/skills-hub/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/soumyaRauth/skills-hub/releases/tag/v0.1.0
