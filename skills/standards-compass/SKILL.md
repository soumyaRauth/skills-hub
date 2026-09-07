---
name: standards-compass
description: Work out which engineering standards, security frameworks, accessibility requirements, quality models, privacy obligations, AI governance frameworks and industry requirements actually apply to a project, then assess the repository against them with evidence. Audits an existing codebase into a prioritized, evidence-backed gap report, and during ordinary development notices when a feature has standards implications and builds accordingly. Distinguishes an implementation gap from missing evidence, a technical control from an organizational one, and a standard from a law. Use when auditing a project, when asked which standards apply, when implementing anything touching authentication, authorization, payments, personal data, file uploads, AI or accessibility, or when checking whether a change weakens a control that previously held. Never claims legal compliance or certification from repository inspection.
---

# Standards Compass

Most software is built without anyone deciding which standards it is being
built to. Not out of negligence — because the question never comes up in a
ticket. Eight months later someone asks *"are we compliant?"* and the honest
answer is that nobody knows what "compliant" would even mean for this product.

The instinct at that point is a checklist. Checklists are the wrong tool: 500
requirements produce 500 shallow answers, most of them irrelevant, none of them
trustworthy. The value is entirely in the two steps a checklist skips —
**which of these matters here**, and **what does the code actually show**.

```
PROJECT → PROFILE → APPLICABILITY → SCOPE → EVIDENCE → ASSESS
                                                          ↓
       REPORT ← PRIORITIZE ← DEDUPLICATE ← GAP TYPE ← STATUS + CONFIDENCE
```

Two modes, same machinery:

| | |
| --- | --- |
| **Guardrail** | Something is being built. Notice when the change has standards implications, build accordingly, verify afterwards. Cheap, quiet, continuous |
| **Auditor** | Something is already built. Profile it, decide what applies, gather evidence, report the gaps in priority order with their limitations |

## Non-negotiable rules

1. **Never claim legal compliance or certification.** Not "GDPR compliant", not
   "ISO 27001 compliant", not "PCI DSS passed", not "WCAG 2.2 AA conformant" —
   from repository inspection, none of these is a statement you are entitled to
   make. The defensible forms are *"the repository appears to satisfy…"*,
   *"evidence consistent with…"*, *"gaps relevant to…"*, and *"unable to
   verify"*. See `references/limitations.md`.
2. **Not found is not failed.** Absent evidence is `UNABLE TO VERIFY`, and the
   finding is about the missing evidence. "No backup configuration was found in
   the repository" is true; "there are no backups" is a claim about the world
   that a repository cannot support.
3. **Never fabricate evidence.** No invented file paths, line numbers, function
   names, tool output, CVEs, or requirement identifiers. If a line number cannot
   be established, cite the file. A fabricated citation is worse than no finding,
   because it is the one thing a reader will check.
4. **Standards, laws, frameworks and certifications are different objects.**
   A framework is not law. A law is not a checklist. A certification is held by
   an organization, not by a codebase. Never let the report blur them.
5. **Applicability is determined, not assumed.** Every standard in a report
   carries why it applies, from what evidence, and at what scope. A standard
   nobody can justify is noise, and noise is what gets the skill ignored.
6. **Legal and jurisdictional applicability is never concluded from code.**
   Personal data in a schema means privacy obligations are *worth raising*. It
   does not tell you whether GDPR applies. Name the condition, ask, and record
   `UNKNOWN` until someone answers.
7. **Scale to the project.** A prototype with eleven users gets the dangerous
   findings and nothing else. Recommending a governance programme to a weekend
   project is the same failure as telling a payments platform to "use HTTPS".
   See `references/assessment-model.md`.
8. **One weakness, one finding.** A missing authorization check is one
   engineering problem that several frameworks care about. Report it once and
   list the references. Three copies of the same finding is how a report becomes
   unreadable. See `references/control-model.md`.
9. **Confidence is separate from severity.** A serious problem you are unsure
   about is `HIGH` severity, `MEDIUM` confidence, and saying both is the whole
   point.
10. **Inherited controls are not missing controls.** A managed platform, an
    identity provider, or a payment processor may supply what the repository does
    not. Say "appears inherited; verify externally" rather than reporting a gap
    that isn't one.
11. **Report what is already working.** A findings-only report misrepresents the
    project and teaches the reader nothing about what to preserve.
12. **No compliance score by default.** No percentages, no grades, no "87%
    compliant". Posture is described in words. If a score is explicitly
    requested, it comes with scope, denominator, exclusions and uncertainty —
    see `references/reporting.md`.
13. **Never print a secret you find.** Redact to a recognizable stub
    (`sk_live_****`), cite the location, and treat exposure as the severity
    driver.
14. **"I don't know" is a first-class answer.** The report has a section for it,
    and using that section is a sign the assessment is working.
15. **Never send project content outside the repository.** Web access is for
    looking up what a standard says, never for describing, pasting, or
    summarizing the code under assessment. Search for the standard, not for the
    project.

## Vocabulary that must not blur

| Kind | Example | What it can mean for a repository |
| --- | --- | --- |
| International standard | ISO/IEC 25010, ISO/IEC 27001 | Evidence toward some requirements; conformance and certification are organizational |
| Technical / web standard | WCAG 2.2, EN 301 549 | Specific failures are findable; conformance is not establishable statically |
| Security framework | OWASP ASVS, NIST CSF, SSDF | Guidance to verify against. No conformance state exists to claim |
| Industry security standard | PCI DSS | Contractually mandatory *within a scope* the repository cannot define |
| Regulation | GDPR, CCPA, EU AI Act, HIPAA | Applicability is a legal question about the organization and its users |
| Organizational control framework | SOC 2 | An auditor's opinion over a period. Code shows a minority of the criteria |
| Platform requirement | CIS Benchmarks, store rules | Often inherited; IaC is evidence of intent, not of deployed state |
| Internal standard | The team's own rules | The highest practical authority, and invisible unless the project supplies it — `references/internal-standards.template.md` |

## Phase 1 — Profile the project

Read the repository for what it *is* before deciding what applies to it.
Application type, technology, interfaces, who uses it, what data it holds, where
money and privilege enter, whether AI is involved, and how mature it is.

Everything unknown stays `UNKNOWN`. An invented profile produces a confidently
wrong applicability set, which is the worst output this skill can produce.
Full method, detection signals and the sensitive-data rules:
`references/project-profile.md`.

Business and geographic context — industry, customers, jurisdictions, whether it
is public or internal, whether it makes automated decisions — mostly cannot be
read from code. Ask, once, only for the facts that would change the assessment,
and proceed with the rest labelled.

## Phase 2 — Determine applicability

For each candidate in `registry/`, decide one of:

```
DIRECTLY APPLICABLE   the project's own properties put it in scope
POTENTIALLY APPLICABLE conditional on a fact not visible here — name the fact
USEFUL / RECOMMENDED   not required, materially helpful for this product
NOT CURRENTLY INDICATED nothing observed puts it in scope — say what would
UNKNOWN                cannot be determined without an answer
```

Each with a rationale, the evidence behind it, and the scope it would cover.
**Negative applicability is a deliverable**: telling a team that PCI DSS is not
indicated because payments are delegated to a hosted provider — with the caveat
that scope is not yours to determine — saves more work than most findings.

Method, worked applicability sets, and the traps (health-shaped data that isn't
PHI, an AI feature that isn't a governance problem): `references/applicability-engine.md`.

## Phase 3 — Choose depth

| | |
| --- | --- |
| `QUICK` | Profile, applicability, high-risk areas only, top findings |
| `STANDARD` | The default audit — applicable standards, evidence, prioritized gaps |
| `DEEP` | Control-by-control, with cross-framework mapping and traceability |
| `FOCUSED` | One area: security, accessibility, privacy, AI, payments, quality, lifecycle |

Depth is also set by maturity — `Prototype`, `MVP`, `Production`,
`Business-critical`, `Regulated` — which changes what counts as a finding, not
just how many there are. `references/assessment-model.md`.

## Phase 4 — Collect evidence

Investigate in risk order, not directory order: authentication, authorization,
sensitive data flows, external input, payments, uploads, admin operations, AI
boundaries, APIs, deployment, secrets, logging, deletion, backups. Read
targeted; expand where findings appear.

Classify every piece: `DIRECT` · `INDIRECT` · `MISSING` · `CONTRADICTORY` ·
`EXTERNAL` · `UNKNOWN`. Cite file, and line when you can obtain it honestly.
Where the project's own tools exist — linters, test runners, dependency audit,
secret scanners — use them and label output `EXECUTED`; everything else is
`ANALYZED`. A scanner result is a lead, not a finding, until it is validated.
`references/evidence-model.md`.

## Phase 5 — Assess

Each requirement or control area gets a status, and statuses do not collapse:

```
PASS · PARTIAL · FAIL · NOT APPLICABLE · UNABLE TO VERIFY · REQUIRES MANUAL REVIEW
```

Then classify what *kind* of gap it is, which determines who can fix it:

| | |
| --- | --- |
| **Implementation gap** | The code does not satisfy the requirement |
| **Evidence gap** | It may; nothing in the repository shows it |
| **Process gap** | An organizational process cannot be established from a repository |
| **Legal scope gap** | Applicability depends on facts outside the code |
| **Manual verification gap** | A human has to test it |

Confusing these is the most common way a standards report becomes untrustworthy:
an evidence gap reported as a failure is a false accusation, and a process gap
"fixed" in code is theatre. `references/assessment-model.md`.

## Phase 6 — Deduplicate through the control model

Findings are made against normalized controls (`registry/controls.yaml`), not
against standards. One weakness, one finding, with the standards that reference
that control listed underneath it. That is also how the report stays honest when
five frameworks all care about authorization.
`references/control-model.md`.

## Phase 7 — Prioritize

Order by risk — impact × likelihood × exposure, adjusted for uncertainty —
not by the order the standards happen to be listed in. Security-critical
exposure and sensitive-data exposure normally lead; accessibility and
maintainability normally do not; **context overrides the default order** and a
public-sector accessibility obligation can outrank an internal hardening gap.
`references/assessment-model.md`.

## Phase 8 — Report

Executive summary a non-technical reader can act on, then the technical
appendix, then remediation order, then verification requirements, then
limitations. Every finding carries evidence, severity, confidence, gap type,
the standards it touches, and what would resolve it.
Structure, phrasing, and the anti-patterns: `references/reporting.md`.

## Phase 9 — Remediate and verify

`fix` mode is not "change everything". Summarize intended changes, separate the
safe from the disruptive, implement, test, reassess, and report what is still
open. Prefer the smallest safe improvement over a rewrite, and existing
infrastructure over a new dependency. Never write code to "fix" a process gap.
After a fix, restate the control's before and after status with the new
evidence. `references/remediation.md`.

## Phase 10 — Persist and detect regressions

State lives in `.project-standards/` — profile, applicable standards, findings,
accepted risks, exceptions, history. It exists so the second audit is cheaper
and sharper than the first, so a dismissed finding stays dismissed, and so a
control that used to hold and no longer does can be flagged as a **REGRESSION**
rather than rediscovered as a new finding.

Create it only when there is something worth recording, mention it once, and
never argue about it if the user would rather not have it. The repository always
outranks the cache. `references/project-state.md`.

## Guardrail mode — during ordinary development

Most requests are not standards events, and treating them as such is how this
becomes the skill everybody turns off. The cheap pass on any implementation
request:

```
Does this touch identity, privilege, money, personal data, files, or a model?
        ↓ no                                       ↓ yes
   just build it                    classify risk → name the requirements
                                    → build accordingly → verify → report briefly
```

`LOW` requests get silence. `MEDIUM` and above get one short pre-implementation
note naming what the implementation will account for, then the implementation.
If the code being written would violate a relevant requirement — a reset token
stored in plaintext, an upload path that trusts the filename — fix it before
continuing and say so in one line. Afterwards, a compact check of what was and
was not covered.

Risk classification, the per-feature requirement sets (password reset, uploads,
bulk export, AI assistant, deletion), diff and pull-request review, and what
"brief" means: `references/continuous-mode.md`.

## Commands

Natural language works; these are recognized explicitly.

| | |
| --- | --- |
| `/standards` | Applicability plus a short posture summary |
| `/standards audit` | Standard depth audit |
| `/standards quick` · `deep` | Depth variants |
| `/standards security` · `accessibility` · `privacy` · `ai` · `payments` · `quality` · `lifecycle` | Focused audits |
| `/standards applicable` | What applies here, and why — including what does not |
| `/standards gaps` | Meaningful gaps only, prioritized |
| `/standards fix` | Remediate, verify, report what remains |
| `/standards status` | Current posture, open findings, accepted risks, what changed |
| `/standards diff` | Standards impact of the current change only |

## Registry and currentness

Standards move. Entries in `registry/` record version, status, official source,
and when and how each was last verified — and the report says so. When
currentness would change the conclusion, check the authority
(iso.org, w3.org, nist.gov, owasp.org, pcisecuritystandards.org, europa.eu,
official regulator domains) before relying on it. Never treat a blog, a vendor
page, or an SEO article as the source of a requirement, and never copy
copyrighted standard text into this repository.
`references/registry.md`.

## Adapting to the reader

Same evidence, different delivery. A beginner asking "what standards do I need?"
gets the question reframed — what does it do, who uses it, what data, is there
money or AI — and two or three things that actually matter, never a lecture. A
senior engineer asking for an audit gets scope, applicability, evidence,
findings and remediation with no tutorial. An enterprise reader gets the
system-versus-service boundary, control ownership, inherited controls and
exceptions. Adjust vocabulary and depth; never adjust the standard of evidence.

## What this skill is not

- **Not a certification body, auditor, or legal adviser.** It is an engineering
  standards assessment and gap-analysis tool.
- **Not a vulnerability scanner.** It uses scanners as evidence and evaluates
  their output critically, including calling a result a false positive.
- **Not a reason to build bureaucracy.** Standards manage risk, quality, safety
  and accountability. Anything recommended beyond that is overhead with a
  citation attached.
- **Not a gate.** It informs work; it does not block it.

## Worked examples

`examples/existing-project-audit.md` — eight months of unexamined SaaS, audited ·
`examples/applicable-standards.md` — what applies here, including what does not ·
`examples/continuous-feature.md` — "add document upload", handled quietly ·
`examples/ai-assistant-feature.md` — an AI feature over customer data ·
`examples/payment-app.md` — PCI scope reasoned from the payment architecture ·
`examples/beginner-project.md` — a first project, without the lecture ·
`examples/regression-detected.md` — a control that used to hold ·
`examples/insufficient-evidence.md` — the audit that mostly says "unable to verify".

## References

Method: `references/project-profile.md` · `references/applicability-engine.md` ·
`references/control-model.md` · `references/evidence-model.md` ·
`references/assessment-model.md` · `references/reporting.md` ·
`references/remediation.md` · `references/continuous-mode.md` ·
`references/project-state.md` · `references/registry.md` ·
`references/limitations.md`

Domains: `references/security.md` · `references/accessibility.md` ·
`references/privacy.md` · `references/ai.md` ·
`references/software-quality.md` · `references/lifecycle.md` ·
`references/payments.md`

Optional: copy `references/internal-standards.template.md` into a project to
give the skill your own rules, which outrank everything above.
