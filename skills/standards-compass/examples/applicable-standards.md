# `/standards applicable` — what actually applies here

**Request:** *"Which standards should this project care about?"*

The most valuable command in the skill, because it is the one that prevents
work rather than creating it.

**Project:** internal expense approval tool. ~12k lines. Django, Postgres, no
public signup, SSO through the corporate identity provider, receipts uploaded as
images, approvals routed by manager hierarchy. No payments — reimbursement is
handed to a payroll system by CSV.

---

## Response

```markdown
## What applies to this project

I profiled the repository first: internal Django web application, SSO-only
authentication, personal data limited to employee names, emails and expense
records, file uploads (receipts), no payment processing, no AI, no public
surface. Maturity looks like Production — real releases, staging config, error
tracking.

### Directly applicable

**OWASP ASVS 5.0.0** — authenticated application handling uploads and approval
workflows. Aim at Level 1; the data is employee-sensitive but not regulated,
and Level 2 would be over-specifying for an internal tool behind SSO.

**WCAG 2.2** — it's a web UI your colleagues have to use, and internal tools
are where accessibility obligations to employees most often get forgotten.
Whether AA is contractually required here is an HR and legal question, not
something the code answers.

### Useful

**ISO/IEC 25010** — vocabulary for the reliability findings, particularly
around the approval state machine.

### Potentially applicable — each conditional on something I can't see

**GDPR** — you process employee personal data. If the organization is
established in the EU or the employees are, obligations are engaged, and the
relevant technical ones are retention of receipts and what deletion means for a
departed employee. That determination is legal.

**Your organization's own security standard** — an internal tool is usually
covered by internal policy long before any external framework. If there is one,
point me at it and it takes precedence over everything above
(`references/internal-standards.template.md`).

**ISO/IEC 27001** — only if your organization already runs an ISMS and this
system falls inside its scope. If so, this application contributes evidence for
a subset of Annex A themes and nothing more.

### Not currently indicated

**PCI DSS** — no card data and no payment processing. Reimbursement leaves via
a CSV handed to payroll. This is an observation about the repository, not a
scope determination.

**HIPAA** — no health data observed.

**ISO/IEC 42001, EU AI Act, OWASP LLM Top 10** — no AI functionality found.
Revisit if receipt scanning or categorization gets a model behind it, which is
the usual next feature for a tool like this.

**SOC 2** — internal tool, no external customers receiving a report.

**CIS Benchmarks** — no infrastructure-as-code in the repository.

### What I'd actually do

Two standards to assess against, ASVS and WCAG, and one question to answer
internally about employee data retention. That's the whole list. An internal
expense tool does not need a governance programme, and building one would be
the more expensive mistake here.
```

---

## What makes this correct

- Five standards ruled out **with reasons**, which is what stops someone
  re-raising them next quarter.
- The internal standard is named as the highest authority, because for an
  internal tool it is.
- ASVS level is chosen and justified rather than defaulting to the strictest.
- The likely future trigger (AI on receipts) is named without being treated as
  a present obligation.
- It ends by making the list smaller, not longer.
