# Standards Compass

### Your code can work perfectly and still be missing things that matter.

Security controls. Accessibility. Privacy. Auditability. Quality. Lifecycle
practices. AI governance. Industry requirements.

Standards Compass is an [Agent Skill](https://code.claude.com/docs/en/skills)
that works out which of those actually matter for *your* software — and then
checks the project against them, with evidence.

```bash
npx skills add soumyaRauth/skills-hub --skill standards-compass
```

---

## The problem

Nobody decides which standards a product is built to. Not out of negligence —
because the question never appears in a ticket. Then eight months in, somebody
asks *"are we compliant?"* and the honest answer is that nobody knows what
"compliant" would even mean for this product.

The instinct at that point is a checklist:

```
Here are 500 requirements. Check each one.
```

Which produces 500 shallow answers, most of them irrelevant, none of them
trustworthy — and a team that now believes standards work is theatre.

The two hard questions are the ones a checklist skips:

```
Which of these actually applies to this software?
And what does the code actually show?
```

## What it does instead

```
PROJECT → PROFILE → APPLICABILITY → SCOPE → EVIDENCE → ASSESS
                                                          ↓
       REPORT ← PRIORITIZE ← DEDUPLICATE ← GAP TYPE ← STATUS + CONFIDENCE
```

Nine standards considered, four assessed against, five ruled out **with
reasons** — that ratio is the product. Telling a team that PCI DSS is not
indicated because payments are delegated to a hosted provider saves more work
than most findings create.

## Two modes

| | |
| --- | --- |
| **Guardrail** | You are building. It notices when a change has standards implications — uploads, permissions, payments, personal data, AI — builds accordingly, and reports in four lines. Silent otherwise |
| **Auditor** | It is already built. Profile, applicability, evidence, prioritized gaps, and an explicit list of what could not be verified |

## What an audit looks like

```
Developer:  "Audit this project."

Applicable
  ✓ OWASP ASVS 5.0.0        authenticated multi-tenant app, untrusted input
  ✓ OWASP API Top 10 2023   SPA and mobile clients call the API directly
  ✓ WCAG 2.2                public web UI with interactive workflows
  ⚠ GDPR                    personal data present; jurisdiction unknown
  ⚠ PCI DSS v4.x            hosted checkout; scope determined with your acquirer
  ✕ HIPAA                   no clinical data or healthcare relationship observed

Findings
  🔴 3 high    🟠 8 medium    🟡 6 unable to verify

Top issue
  Three administrative endpoints don't enforce the authorization rule the
  other eleven use, and the export query at src/api/admin/exports.ts:31 has
  no tenant filter — so a signed-in member may be able to export another
  organization's customers.

First step
  Route the three handlers through requireRole('admin'), scope the export
  query, and add a negative test per endpoint.
```

## The distinction that makes it trustworthy

Most standards tooling collapses five different things into "fail". These are
not the same, and they route to different people:

| | |
| --- | --- |
| **Implementation gap** | The code does not satisfy the requirement — an engineer fixes it |
| **Evidence gap** | It might; nothing here shows it |
| **Process gap** | The organization has to do something. **Never** fixed by writing code |
| **Legal scope gap** | Depends on facts outside the repository |
| **Manual verification gap** | A human has to test it |

And the rule underneath all of them:

> **Not found is not failed.**

No backup configuration in the repository means *no backup configuration was
found in the repository*. Backups usually live somewhere a codebase cannot see.
The status is `UNABLE TO VERIFY`, and it goes to the person who runs the
infrastructure — not into a findings list as a failure.

## What it will never say

```
"This software is GDPR compliant"
"The company is ISO 27001 compliant"
"WCAG 2.2 AA conformant"
"This application passed PCI DSS"
```

None of those is available from reading a repository, and all of them get
quoted to customers. Certification and legal compliance rest on organizational
process, policy, contracts, scope and independent assessment. What you get
instead:

```
"The repository appears to satisfy…"
"Evidence consistent with…"
"Gaps relevant to…"
"Unable to verify."
```

## Installation

```bash
npx skills add soumyaRauth/skills-hub --skill standards-compass
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill standards-compass --agent claude-code
```

No slash command required — installed skills are matched by description. It
engages on its own when a change touches identity, privilege, money, personal
data, files or a model, and answers directly when you ask:

```
Audit this project.
Which standards apply here?
Is this accessible?
What are we missing on privacy?
Does this change weaken anything?
/standards quick        /standards security      /standards ai
/standards applicable   /standards accessibility /standards payments
/standards gaps         /standards privacy       /standards fix
```

## The registry

Standards move. The registry is the part designed to be updated without touching
the skill:

```
registry/
├── registry.yaml     categories, types, statuses, authority domains, schema
├── controls.yaml     36 normalized control concepts
└── <category>/*.yaml one file per standard — add one, nothing else changes
```

22 entries at present, spanning security (ASVS, OWASP Top 10, API Top 10,
MASVS, NIST CSF, SSDF, ISO/IEC 27001), quality (ISO/IEC 25010), accessibility
(WCAG 2.2, EN 301 549), lifecycle (ISO/IEC/IEEE 12207), privacy (GDPR,
CCPA/CPRA, ISO/IEC 27701), AI (ISO/IEC 42001, NIST AI RMF, EU AI Act, OWASP LLM
Top 10), payments (PCI DSS), industry (SOC 2, HIPAA Security Rule) and cloud
(CIS Benchmarks).

Every entry records its version, status, official source, **and when and how it
was last verified** — `authoritative-source` with the URL, or `bundled-knowledge`
carried from training data. Reports say which. `scripts/validate-registry.sh`
enforces the schema, including that an `official_url` sits on the publishing
body's own domain, so a vendor blog cannot become a citation.

No copyrighted standard text is stored here. Names, identifiers, versions,
official links, applicability and original summaries — the text itself stays
with its publisher.

## One weakness, one finding

Five frameworks care about authorization. Reported five times, nobody reads the
second one. Findings are made against normalized controls, and the standards get
attached underneath:

```
Missing authorization on 3 admin endpoints        ← one finding
      └── OWASP ASVS · API Top 10 (API5) · NIST CSF PR.AA · ISO 27001 themes
```

Adding a standard extends every control it names, automatically. There is no
mapping table to maintain and nothing to drift.

## It gets better across sessions

```
.project-standards/
├── profile.md                  what this software is, labelled
├── applicable-standards.yaml   applicability decisions, and the negatives
├── findings.md                 findings with status history and stable ids
├── accepted-risks.md           what the team decided to live with, and why
├── exceptions.md               intentional deviations, with compensating controls
└── assessment-history.md       what was assessed when, and what changed
```

Which buys three things a one-shot audit cannot have: a dismissed finding stays
dismissed, the second audit is cheaper than the first, and a control that used
to pass and no longer does is reported as a **regression** — with the commit
that caused it — rather than rediscovered as a new problem.

Created only when there is something worth recording, mentioned once, and
dropped entirely if you would rather not have it.

## It scales down, and up

The same repository produces a different report at different maturities, because
otherwise this is bureaucracy:

| | |
| --- | --- |
| `Prototype` | Dangerous mistakes only. No process findings, no governance |
| `MVP` | Add authorization consistency, personal data, dependencies, basic accessibility |
| `Production` | Full technical assessment; operational evidence expected |
| `Business-critical` | Add availability, recovery, auditability, tenant isolation depth |
| `Regulated` | Traceability and evidence become findings in their own right |

A prototype told to build a governance programme ignores the whole report. A
regulated system told to "add some tests" has been failed by it.

## How it differs

| | |
| --- | --- |
| A static analyzer | finds code patterns |
| A vulnerability scanner | finds known vulnerabilities |
| A compliance checklist | hands you requirements |
| **Standards Compass** | works out what applies, reads the project, gathers evidence, separates gaps from unknowns, prioritizes by risk, helps fix them, and notices when a fix stops holding |

## Worked examples

- [**Existing project audit**](examples/existing-project-audit.md) — eight months
  of unexamined SaaS, and what the report actually says
- [**What applies here**](examples/applicable-standards.md) — an internal tool,
  five standards ruled out with reasons
- [**Continuous mode**](examples/continuous-feature.md) — "add document upload",
  handled in nine lines around the work
- [**AI assistant**](examples/ai-assistant-feature.md) — customer data, tools,
  and where governance starts and stops
- [**Payments**](examples/payment-app.md) — PCI scope reasoned from the
  architecture, plus the three findings that cost real money
- [**Beginner**](examples/beginner-project.md) — a first app, told which four
  standards to ignore entirely
- [**Regression**](examples/regression-detected.md) — a control that passed in
  September and does not now
- [**Insufficient evidence**](examples/insufficient-evidence.md) — the audit that
  refuses to produce a posture, and still finds the public bucket

## References

Loaded on demand.

| | |
| --- | --- |
| [`project-profile.md`](references/project-profile.md) | Reading what the software is: type, data, boundaries, maturity, and what code cannot tell you |
| [`applicability-engine.md`](references/applicability-engine.md) | The five applicability states, the record each standard must fill, and the traps |
| [`control-model.md`](references/control-model.md) | Why findings are made against controls, and how standards attach to them |
| [`evidence-model.md`](references/evidence-model.md) | Six evidence categories, citation discipline, executed vs analyzed, false positives, secrets |
| [`assessment-model.md`](references/assessment-model.md) | Status, gap type, confidence, severity, risk, and how maturity moves the bar |
| [`reporting.md`](references/reporting.md) | Report structure, finding format, the language rules, and what to do if a score is demanded |
| [`remediation.md`](references/remediation.md) | Roadmaps, `fix` mode, verification, and what must never be fixed in code |
| [`continuous-mode.md`](references/continuous-mode.md) | Guardrail behaviour: risk classes, per-feature requirement sets, diff review |
| [`project-state.md`](references/project-state.md) | `.project-standards/`, exceptions, accepted risks, regressions, staleness |
| [`registry.md`](references/registry.md) | Registry format, adding a standard, copyright, currentness, when to go to the web |
| [`limitations.md`](references/limitations.md) | The claims that are never available, and where to stop |
| [`security.md`](references/security.md) · [`accessibility.md`](references/accessibility.md) · [`privacy.md`](references/privacy.md) · [`ai.md`](references/ai.md) · [`software-quality.md`](references/software-quality.md) · [`lifecycle.md`](references/lifecycle.md) · [`payments.md`](references/payments.md) | The focused assessments |
| [`internal-standards.template.md`](references/internal-standards.template.md) | Copy into your project to give it your own rules, which outrank everything else |

## What it is not

- **Not a certification body, auditor, or legal adviser.** It is an engineering
  standards assessment and gap-analysis tool.
- **Not a vulnerability scanner.** It uses scanners as evidence and evaluates
  their output critically, including calling a result a false positive.
- **Not a reason to build bureaucracy.** Anything recommended beyond managing
  real risk is overhead with a citation attached.
- **Not a gate.** [Production Guard](../production-guard/README.md) decides
  whether a change is safe to ship; this decides what the software should be
  measured against in the first place.

## Limitations

- It reads a repository. Production configuration, organizational process,
  contracts, training and physical security are all outside it, and it says so
  rather than guessing.
- Legal applicability is never determined from code. Personal data means
  *ask about jurisdiction*, not *GDPR applies*.
- Accessibility findings from source are real; accessibility conformance is not
  establishable without manual testing, and the report says which criteria were
  assessed by which means.
- Infrastructure-as-code is evidence of intent. The cloud console is the fact.
- The bundled registry ages. Entries carry a verification date and method, and
  the report quotes them.
- Severity is judgment, informed by context. A finding that matters on a public
  endpoint may be informational on an internal one, and being overruled costs
  one sentence.

## License

[MIT](../../LICENSE)
