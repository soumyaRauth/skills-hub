# Applicability

The product is here. Everything else — evidence, findings, remediation — is
downstream of getting this right, and a report that assesses the wrong standards
carefully is worth less than one that assesses the right ones roughly.

## The five states

| State | Meaning |
| --- | --- |
| `DIRECTLY APPLICABLE` | The project's own observed properties put it in scope |
| `POTENTIALLY APPLICABLE` | Conditional on a fact not visible in the repository — **name the fact** |
| `USEFUL / RECOMMENDED` | Not required; materially helpful for this product |
| `NOT CURRENTLY INDICATED` | Nothing observed puts it in scope — say what would |
| `UNKNOWN` | Cannot be determined without an answer nobody has given |

`NOT CURRENTLY INDICATED` is deliberately not "not applicable". A repository
does not have the standing to declare a standard inapplicable to an
organization; it can only report that nothing it can see puts the project in
scope.

## The record for each standard

```
Standard          WCAG 2.2 (W3C, technical standard, current)
Applicability     DIRECTLY APPLICABLE
Why               Public-facing web application with interactive user workflows —
                  forms, tables, modal dialogs
Basis             OBSERVED — app/(public)/* renders 14 routes; 9 forms across
                  src/components/forms/
Scope assessed    Core user-facing workflows: sign-up, sign-in, search, checkout
Legal status      Not itself law. Whether conformance is legally required
                  depends on jurisdiction and sector — UNKNOWN here
Limits            Static inspection reaches a minority of success criteria
```

Six lines. A standard that cannot fill them does not belong in the report.

## How to decide

1. **Read the profile**, not the code. Applicability is a property of what the
   software is and who it serves.
2. **Match against `applies_when`** in each registry entry. These are profile
   facts, not keywords: `web_application`, `processes_personal_data`,
   `accepts_card_payments`, `has_ai_functionality`, `users_in_eu`.
3. **Split conditions the repository cannot settle.** Anything depending on
   jurisdiction, organizational scope, contracts, or customer requirements is
   `POTENTIALLY APPLICABLE` with the condition stated — never `DIRECTLY`.
4. **Check `not_indicated_when`** and write the negative finding where it saves
   work.
5. **Cap the set.** A typical project has three to six standards worth
   assessing. A list of fifteen means the filter is not running.

## A worked set

```
Public SaaS · personal data · Stripe Checkout · AI assistant over customer data
· public web UI · unknown jurisdictions · production maturity

DIRECTLY APPLICABLE
  OWASP ASVS 5.0.0          Authenticated multi-tenant app with untrusted input
  OWASP API Security 2023   SPA and mobile clients call a JSON API directly
  WCAG 2.2                  Public web UI with interactive workflows
  OWASP LLM Top 10 (2026)   Model reads customer records and calls tools

USEFUL / RECOMMENDED
  ISO/IEC 25010             Vocabulary for the reliability and maintainability findings
  NIST CSF 2.0              Frames what a repository cannot see — Govern, Respond, Recover
  NIST SSDF                 Supply chain and vulnerability handling, given enterprise buyers

POTENTIALLY APPLICABLE   — each conditional on something nobody has told us
  GDPR                     If established in the EU or offering services to people there.
                           Personal data is present; jurisdiction is UNKNOWN
  PCI DSS v4.x             Payment architecture is hosted checkout, which usually
                           minimises scope — but scope is determined with the acquirer,
                           and the payment-page script requirements can still reach you
  ISO/IEC 27001            If the organization has or wants an ISMS, or a customer asks
  SOC 2                    If a customer has asked for a report
  ISO/IEC 42001            If AI governance must be demonstrated to customers
  EU AI Act                If the system is placed on the EU market. Tier looks low
                           (assistive, not decisional) but that is a legal determination

NOT CURRENTLY INDICATED
  HIPAA Security Rule      No clinical data, no healthcare integration, no covered
                           entity or business associate relationship evident.
                           This is an observation about the repository, not a
                           determination about the organization
  CIS Benchmarks           No infrastructure-as-code in the repository; the platform
                           appears managed. Revisit if infrastructure moves in-repo
```

Note what this list does *not* do: it does not turn a small SaaS product into an
ISO compliance programme, and it does not silently drop the standards that
depend on facts nobody has established.

## Traps

**Health-shaped data that is not PHI.** Fitness metrics, symptom notes in a
consumer app, an employer wellness tool. Health data raises privacy questions;
HIPAA applies to covered entities and business associates. Ask; do not conclude.

**Payments that are not in PCI scope — and payments that quietly are.** A hosted
checkout usually keeps card data out of the application. It does not always keep
the merchant out of scope entirely, because requirements about scripts on the
payment page reach even minimal integrations. Determine the architecture
(`payments.md`) before saying either thing.

**An AI feature is not an AI governance problem.** A summarization button is a
security and privacy question. An AI that reads customer data, calls tools, or
influences decisions about people is a governance question. Do not promote the
first into the second.

**Personal data is not GDPR.** It is the trigger to *ask*, and the finding when
nobody knows the answer is that nobody knows the answer.

**Infrastructure-as-code is not infrastructure.** Terraform is evidence of
intent. Cloud console state is the fact. Findings from IaC alone cap at MEDIUM
confidence.

**Enterprise frameworks in small projects.** ISO 27001, SOC 2 and 42001 exist
because organizations are asked to prove things. If nobody has asked, naming
them as applicable manufactures work.

## Restating applicability later

Applicability is not decided once. It changes when the project changes — the
first payment integration, the first EU customer, the first model call over
customer data, the first admin bulk export. When the profile moves, revisit the
set and record the change in `.project-standards/applicable-standards.yaml`
with the date and the trigger.
