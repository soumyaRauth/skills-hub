# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this repository ships
instructions rather than executable code, so versions describe changes in
methodology and documentation.

## [Unreleased]

### Added

- **Lessons: every skill now keeps what it learns from being corrected.** Until
  now a skill was the same file on its hundredth project as on its first. Project
  state made it smarter about one repository, and nothing made it better at its
  own discipline. A new `Lessons` rule in the shared protocol has each skill read
  `~/.skills-hub/lessons/<skill>.md` when it engages. When a person corrects a
  miss, a false alarm or a wrong verdict, the skill appends one dated rule there.
  The file lives outside the installed skill, so updates do not wipe it, and
  outside the repository, so a lesson from a private project is never committed
  here. Lessons are general rules, never project facts. They are capped at twenty
  lines and never override a skill's rules or a person's instruction. They reach
  `SKILL.md` only by hand, through the usual review.
- **Uninstalling takes one command, and the documentation says it is your
  right.** The README and the site now have an *Uninstalling* section, marked as
  important and linked from the top of the README. It gives one `npx skills
  remove` command that removes the eleven skills from every agent. It names
  them, because `--skill '*'` would take every other skill on the machine with
  them, and names that are not installed are skipped. The section also covers
  the plugin route and lists what stays behind (lessons, project state, the
  optional Claude Code extras) with how to remove each. `scripts/validate.sh`
  fails if either command stops naming exactly the skills in `skills/`, so a
  twelfth skill cannot be left out of the uninstall.

- `architecture-engineer` v0.1.0 — **the architecture is not the first answer;
  it is what is left after the reasoning.** Ask a capable agent to design a
  system and it produces an architecture in the first reply, assembled from
  patterns rather than from anything about the problem, because nothing about
  the problem had been established. The failure is not bad architecture but
  *unearned* architecture, which looks identical to the earned kind and costs
  years to undo.

  So the deliverable is a chain where every link carries its provenance.
  Requirements are graded `STATED` / `OBSERVED` / `INFERRED` / `ASSUMED` /
  `UNKNOWN`, and one rule does most of the work: **a decision resting on an
  `ASSUMED` or `UNKNOWN` requirement is not a decision, it is an open question
  with a leading candidate.** *"Eventually maybe 500,000 users"* therefore earns
  one question — committed, or hoped for — because the answer changes the design
  by an order of magnitude of cost. Two further constraints keep it
  proportionate: **reversibility sets the discovery threshold**, so cheap
  decisions are made and expensive ones are checked in on first; and a
  **complexity budget** where every moving part names the requirement forcing it
  or comes out of the design, which is the anti-cargo-cult rule made checkable.

  For existing systems it reads the architecture that is *implemented*, not the
  one that is declared — a `services/` directory is not a service architecture
  and a `domain/` directory that imports the ORM is not a domain model — and the
  gap between the two is usually the most useful sentence available. Migration
  is evolutionary by default, in transition states that each ship, and a
  migration step is complete when something *checked* the structure, not when
  code was edited. Five modes: `DISCOVER`, `DESIGN`, `REVIEW`, `MIGRATE`,
  `VERIFY`, of which only `MIGRATE` touches the project and only when asked.

  It is also the first skill here that is **invited rather than volunteered**. A
  messy codebase is not an invitation: noticing that a project has become
  something nobody designed stays with Project Compass, which holds the
  interruption budget for it. Seven references, four worked examples — one of
  which is entirely about not engaging — one fixture whose README declares
  layers its code does not keep, and three activation cases.

  This **reverses** the "Architecture Guardian — not added" entry in
  [`ECOSYSTEM.md`](ECOSYSTEM.md#skills-considered-and-not-added), and the
  original reasoning is kept there alongside the reversal. Project Compass does
  detect emerging state machines and authorization models — it *notices* them
  and names the one decision that would settle it, which is deliberately where
  it stops. Nothing then answered that decision: no greenfield discovery, no
  option comparison, no recorded trade-off, no target, no migration, no fitness
  check.

- `deployment-compatibility` v0.1.0 — **does this project fit this server?**
  Every other skill in this repository takes one operand: the change, the
  project, the symptom. This one takes two, and the second is a machine. That
  is the gap it fills — Production Guard decides whether a change is safe to
  ship and never inspects a host, and Engineering Investigator treats
  infrastructure as a *suspected cause* rather than as something to assess
  against a requirement. Nothing derived what a project needs at runtime and
  compared it against what a named target provides, which is where deployments
  actually fail.

  It derives a **deployment contract** from the repository — runtime and
  package-manager versions, services with their floor versions, process types,
  ports, storage persistence, migrations, environment variables, external
  integrations — with the file that establishes each line, and two rules that do
  most of the work: a file is not authoritative because of its name (the
  `docker-compose.yml` nobody deploys, the `.env.example` three variables behind
  the code), and a requirement the repository cannot establish is `UNKNOWN`
  rather than an estimate. Then it compares that contract against the target,
  row by row, and each row carries **both sides and both provenances**.

  The anti-overclaim mechanism is the part worth reviewing. A target fact is
  `MEASURED`, `SUPPLIED`, `INFERRED` or `UNKNOWN`, and the readiness state is
  computed from those grades rather than written by hand: a `FIT` resting on a
  fact the *user* supplied cannot produce `READY` — it becomes a numbered
  condition — and a row whose project side is `UNKNOWN` is never `FIT`, because
  not knowing what an application requires is not evidence that the target
  satisfies it. So `READY` is reachable only when the target was actually
  inspected, `READY WITH CONDITIONS` is the normal good outcome, and
  `NOT ASSESSED` is a real result rather than a failure. An **access tier** —
  `NONE`, `DECLARED`, `READ-ONLY`, `AUTHORIZED` — is established before anything
  else, stated in the report header, and caps every claim the report can make.
  Asked whether an app will run on "a standard Ubuntu VPS", the correct output
  is the project contract and three commands, not a confident yes assembled from
  a mental model of Ubuntu.

  Discovery is read-only. Project remediation and server remediation are kept in
  separate lists so that approving the first cannot be read as approving the
  second, server changes are classified `SAFE` / `CONFIRM` / `HIGH IMPACT` /
  `DESTRUCTIVE` / `MANUAL ONLY` and applied only on authorization for that
  specific action, and one rule overrides convenience: **never weaken a control
  to make a deployment work** — no exposed database, no disabled TLS, no
  development mode on a server. Verification separates what ran on the target
  from what ran in an equivalent environment, insists on application-level
  checks rather than port probes, and treats restart and recovery as the point,
  since a deployment that starts once has not been verified. No secret is ever
  printed or persisted. Six references, four worked examples — one of which
  refuses to assess anything — two fixtures that ship *both* operands, three
  activation cases, and a longitudinal scenario for the one claim a single
  prompt cannot test: that the verdict moves when the evidence grade moves, and
  never because files were edited.
- **Automatic activation across the whole set.** The skills no longer depend on
  anyone remembering a slash command, and the fix is not a router. Agents that
  support Agent Skills already show the model each skill's description and let
  it decide what to load. What was missing was descriptions that say when a
  skill should *not* load, a contract for how deep a loaded skill goes, and a way
  for several skills to share one task without talking over each other.
  [`ECOSYSTEM.md`](ECOSYSTEM.md) documents the design: four depths (`PASSIVE`,
  `CONSULT`, `ACTIVE`, `GATING`), a relationship graph, conflict order,
  overrides, and the rule that matters most in Claude Code, where a loaded skill
  stays in context for the rest of the session. **Loaded is not engaged**: every
  skill re-decides on every request.
- **An activation contract in every skill.** Each description now says when to
  use the skill and when not to (`Not for …`), and stays within the 1024
  characters `skills-ref` allows. Each `SKILL.md` gains an `## Activation`
  section (what it engages on, what it stays quiet on, its depth, whom it hands
  work to) and a shared protocol block, copied verbatim so that a skill installed
  alone still carries it. The protocol covers the one-line `⚡` announcement, a
  single interruption per request however many skills engage, `HANDOFF → skill`
  lines, conflict order, opt-outs that never suppress invented evidence, an
  unrun check or a live hazard, and reading sibling skills' state instead of
  re-deriving it.
- `evals/activation/` — **38 activation cases for `claude plugin eval`.** Each
  copies a fixture repository into a sandbox, sends a request phrased the way a
  developer would type it, and grades which skills the session loaded, with
  deterministic `tool_used` graders on the Skill tool. Every skill has at least
  one case where it must engage and one where it must stay quiet. The quiet
  cases cover trivial edits, keyword traps (*refund* in a comment, *payments* in
  an incident), low-risk edits in high-risk files, a requirement that already
  holds, an explicit opt-out, and the same request shape in two repositories
  that should get different answers. Measured on `claude-opus-5`, one run per
  case:
  - **skills alone:** 30/38
  - **with the Claude Code standing instruction:** 37/38
  - **false alarms:** none in either setup (15/15 quiet, trap and contextual
    cases held)
  - **before this change:** 10 of the 16 core cases passed, every failure a
    skill that should have loaded and did not
- `dependency-guard` v0.1.0 — **should this dependency come in, and is it the
  one we think it is?** It climbs a necessity ladder first: codebase, standard
  library, installed dependencies, a few lines. Then it resolves the package
  name before anything installs it, because names that sound right and do not
  exist are what squatters register. It reports install scripts and transitive
  growth from a dry run or the lockfile diff, never from memory, follows the
  house pinning policy, and answers `USE EXISTING` / `ADD` /
  `ADD WITH CONDITIONS` / `DON'T ADD` in a few lines. Routine patch bumps get
  nothing. Two references, four examples, three fixtures.
- `api-contract-guard` v0.1.0 — **what does this interface promise, and which
  of those promises can never be taken back?** Before an endpoint, webhook,
  event or SDK surface that others deploy against ships, it reads the house
  conventions from the existing interfaces and writes a short block of
  decisions consumers will build against: identifiers, enum openness, error
  codes, idempotency, page stability, webhook delivery and signing. Changes are
  labeled additive, behavioral or breaking by their effect on consumers, with a
  migration path in which every step deploys safely. Internal same-deploy
  endpoints get nothing. Two references, four examples, two fixtures.
- `integrations/claude-code/` — optional and Claude Code-only: a ten-line
  standing instruction for `CLAUDE.md`, and `statusline-skills.py`, a status line
  segment that shows the skills invoked in the current turn in color. The
  status line is the Claude Code surface where ANSI color is documented. The
  segment clears on the next prompt, respects `NO_COLOR`, and comes with a
  self-check that `validate.sh` runs.
- `.claude-plugin/plugin.json` — the repository is now also a Claude Code
  plugin, which is what lets `claude plugin eval` run the activation suite and
  `claude --plugin-dir` load all ten skills at once. `npx skills add` is
  unaffected.
- `tests/longitudinal/ecosystem.md` — six multi-request scenarios across
  skills: engagement ending when the request changes, opt-outs scoped to what
  they named, a handoff chain from investigation to proof to release, a
  dismissal that survives repetition, context flipping the answer, and manual
  invocation.
- **One-command installation.** `.claude-plugin/marketplace.json` makes the
  repository installable as a Claude Code plugin in one step, with
  `/plugin marketplace add soumyaRauth/skills-hub` followed by
  `/plugin install skills-hub@skills-hub`, and updatable in one step after
  that. For every other agent, the documented install collapses from eleven
  `npx skills add` lines to `npx skills add soumyaRauth/skills-hub --skill '*'
  -g -y`. The Skills CLI's own `--all` is documented as the one to avoid: it
  expands the agent list to every agent the CLI supports rather than the ones
  present, and writes skill directories into all of them.

### Considered and not added

Architecture, data-architecture, release and migration, observability, and
accessibility skills were each evaluated against what the existing skills
already own. Project Compass, Impact Map, Production Guard and Standards Compass
cover them respectively, and a second skill would split an authority rather than
add one. The reasoning is in [`ECOSYSTEM.md`](ECOSYSTEM.md#skills-considered-and-not-added).

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

- `project-compass` v0.1.0 — **a project-aware engineering guide.** One question,
  asked before every non-trivial request and answered from the repository rather
  than from general advice: *given everything I know about this project, what
  should this developer do next, and why?* Usually the answer is the thing they
  just asked for, and the skill builds it and says nothing. Occasionally it is
  not, and on those occasions the answer is worth more than the implementation
  would have been. The developer rarely knows that this is the question they are
  asking, which is the whole point.

  It exists for the gap between *activity* and *progress*: an agent executes each
  request competently and nothing ever reads the requests as a sequence. Nine
  permission exceptions, each reasonable, are an authorization system nobody
  designed. Five performance changes with no measurement are five guesses with
  deployments attached. And the expensive one — *add search, filtering, sorting,
  export, bulk delete, saved filters, groups, permissions* — is eight legitimate
  requests that together say **we are building an administration system and
  nobody has defined the administration workflow.** No single request could
  produce that sentence, and the person making them cannot see it, because they
  see one at a time.

  Every request resolves into one of **three modes**: **A** build it and say
  nothing about direction (the overwhelming default), **B** build it and flag one
  thing in a paragraph delivered with the work, **C** pause and guide — rare,
  never a refusal, always ending with the offer to build it as asked. Mode A is
  not the absence of the skill: the model is read, the sequence is updated, and
  the guidance that falls out is *build exactly this*. Manufacturing a strategic
  concern for a simple request is the failure the skill is most likely to make,
  and it is named as an anti-pattern in the instructions, the tests and the
  anti-tests.

  **Every finding ends in an action.** *"There is no order lifecycle"* is half a
  sentence; *"define the order lifecycle before adding a fifth status — ten
  lines, half an hour"* is the deliverable. Each of the eleven blind-spot
  detectors carries a closing step, and when several things could be done they
  are ranked by what most improves the trajectory: blocking decisions, then
  broken core workflows, then domain-model problems, then boundaries getting
  expensive, then security and data integrity, and only then debt, performance
  and polish. Technical issues do not automatically outrank product and workflow
  ones.

  State lives in `.project-compass/` — a labeled project model, `direction.md`
  holding what the project is becoming and the current next step, a trajectory of
  what actually changed, decisions, open questions, and gaps that cleared the bar.
  That persistence is the design: *"what should I do next?"* asked of a stateless
  agent gets a fresh guess every time, and this accumulates instead. The purpose
  of every file is better guidance later, never a record of what happened.

  The harder half is restraint, so speaking is gated rather than judged. A gap is
  reportable only when it clears four gates — **recurrence** (three or more
  instances, each with a nameable location), **convergence** (a shared cause, not
  a shared topic), **consequence** (what breaks next, in terms of work already
  asked for), and **actionability** (a step smaller than the work it prevents).
  Two exceptions fire on a single instance: irreversibility and contradiction of a
  recorded decision. On top of that, one intervention per session; **a dismissed
  observation is closed permanently**, recorded with the user's own reason and
  never raised again in any wording; and **a stated goal settles it** — *"this is
  a throwaway prototype"*, *"I'm experimenting"*, *"we've already decided"* become
  the frame every later recommendation is measured against, because the developer
  knows the goal and the repository does not.

  Four engineering states (`FORMING` · `DIRECTED` · `EXPLORATORY` · `DRIFTING`),
  with exploration suppressing gap detection outright; four evidence labels
  (`OBSERVED` · `INFERRED` · `ASSUMED` · `UNKNOWN`) on every claim, including the
  project's objective, which is frequently `UNKNOWN` and is reported as such
  rather than invented. Thirteen references and nine worked examples — one
  entirely about the requests that earn no commentary at all, one about eight
  scattered features that turned out to be an administration console, and one
  about the fifth UI pass that was worth stopping for and the fourth that was
  not.

  Seven fixtures under `tests/fixtures/project-compass/`, three seeded with a
  `.project-compass/` directory holding evidence rather than conclusions;
  `emerging-admin`, whose pattern is spread across four areas so that it is
  visible only in the sequence; and `directed-project`, a healthy repository
  whose correct output is silence. Nine multi-step scenarios in
  `tests/longitudinal/project-compass.md`, each naming the step the intervention
  should land on, the mode, and the next action it must produce — plus a table of
  Project Compass anti-tests scored purely on absence, in which ending at an
  observation is failed as firmly as inventing one.

### Changed

- **All seven existing skills: rewritten descriptions, plus an `## Activation`
  section.** The methodology of each skill is unchanged, with one behavioral
  change. **Impact Map**, loaded on a request to *make* a change rather than to
  map one, now runs as a compact pre-step: MUST CHANGE, HIDDEN COUPLING and open
  questions. The requested change then proceeds on that surface, instead of the
  session stopping at a full report nobody asked for. An explicit request for a
  map still gets the full read-only report and stops. The Project Compass,
  Standards Compass and Engineering Investigator descriptions were shortened to
  make room for their quiet clauses.
- `scripts/validate.sh` holds every skill to the activation contract. The
  description needs a `Not for` clause. The Activation section needs its four
  labels and may name only skills that exist. The protocol block must match
  `ECOSYSTEM.md`. And every skill needs one activation case where it must engage
  and one where it must stay quiet. It also checks that every activation case
  is valid and listed, runs the status line self-check, and parses the plugin
  manifest.
- `CONTRIBUTING.md` gains a fifth hard rule, **activation is earned**: a change
  that makes a skill engage more often comes with a case where it must stay
  quiet.
- The top-level README, the site, and `tests/README.md` cover ten skills and
  how they activate. Each skill page on the site gains a *When it activates*
  section.

### Compatibility

- `npx skills add soumyaRauth/skills-hub --skill <name>` works exactly as before.
  Frontmatter still uses only fields the Agent Skills specification allows.
  Claude Code's `when_to_use` was deliberately not used, because `skills-ref
  validate` rejects it.
- Nothing requires Claude Code. The `⚡` line and handoffs are plain text, and
  everything Claude Code-specific lives in `integrations/claude-code/` and
  `.claude-plugin/`.
- Installing a skill both with `npx skills` and as a plugin shows it twice. The
  plugin form is namespaced, as `skills-hub:<name>`.

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
