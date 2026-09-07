# Reporting

Two audiences, one document. A manager needs to know how bad it is and what
happens next; an engineer needs the evidence and the fix. Serve the first in the
opening section and the second everywhere after it.

## Structure of a full audit

```
1.  Executive summary
2.  Project profile
3.  Applicable standards — and what is not indicated
4.  Overall assessment
5.  Critical findings
6.  High findings
7.  Medium findings
8.  Low and informational findings
9.  Unable to verify
10. Positive controls found
11. Recommended remediation order
12. Verification requirements
13. Limitations
```

Sections 9, 10 and 13 are not filler. Section 9 is where honesty lives, 10 is
what keeps the report from being read as an attack, and 13 is what stops it
being quoted as something it is not.

## Executive summary

Plain language, no jargon, no framework names in the first paragraph. Someone
who does not write code should be able to read it and know what to do.

```markdown
# Standards Assessment — Customer Management Platform

Assessed          2026-09-07 · repository at commit 4f2a9c1
Scope             Application source, configuration, schema, CI. Production
                  infrastructure and organizational processes not in scope
Overall posture   NEEDS ATTENTION

3 high-risk gaps · 8 medium · 6 areas that could not be verified from the code

The most serious issue is that three administrative operations do not enforce
the authorization rule the rest of the admin API uses, so a signed-in user with
a lower privilege level may be able to invoke them.

Separately, the repository contains no evidence about backups, recovery, or
incident handling. That is not the same as those things being absent — they
usually live outside a codebase — but nobody can confirm them from here.

First five actions
1. Fix the authorization inconsistency in the admin API.
2. Remove the customer email addresses currently written to application logs.
3. Add negative authorization tests so this cannot regress silently.
4. Confirm with whoever runs the infrastructure that backups exist and restore.
5. Decide whether EU users are in scope, which changes what privacy work applies.
```

Posture is words, never a number: `STRONG` · `REASONABLE` · `NEEDS ATTENTION` ·
`SIGNIFICANT GAPS` · `UNABLE TO ASSESS`.

## Finding format

```markdown
### [HIGH] Administrative endpoints bypass the shared authorization policy

Finding ID     STD-003
Control        authorization  (also: auditability)
Standards      OWASP ASVS · OWASP API Security Top 10 (API5) · NIST CSF PR.AA
Gap type       Implementation
Severity       HIGH        Confidence  HIGH

Evidence
  src/api/admin/users.ts:41-67      authenticates, no role check
  src/api/admin/exports.ts:22-40    same shape
  src/api/admin/billing.ts:15-33    same shape
  src/middleware/requireRole.ts     the policy the other 11 admin routes use

Current behaviour
  These three handlers call requireAuth() and proceed. Any authenticated
  session reaches them, including the `member` role.

Expected behaviour
  Privileged operations enforce the same role policy as the rest of the
  administrative API.

Impact
  A signed-in member can list all users, trigger a full customer export, and
  read billing records for their organization and, at exports.ts:31, for any
  organization, because the query is not tenant-scoped either.

Recommended fix
  Route the three handlers through requireRole('admin'), and scope the export
  query by tenant. Both are small changes against existing infrastructure.

Verification
  Add a negative integration test per endpoint asserting 403 for a member
  session, and one asserting an export cannot cross tenants.

Scope / limits
  Assessed from source only. Confirm no gateway-level rule already blocks
  these paths in production.
```

Everything in that block is checkable. That is the standard.

## Unable to verify

Its own section, phrased as questions with owners, never as accusations.

```markdown
## Unable to verify from the repository

| Area | What is missing | Who can answer |
| --- | --- | --- |
| Backup and restore | No backup configuration or restore procedure in-repo | Infrastructure owner |
| Incident response | No documented process or security contact | Engineering leadership |
| Production TLS and headers | Deployment configuration is not in this repository | Whoever owns the hosting |
| EU data subjects | Jurisdiction of users is unknown; determines privacy applicability | Business owner or legal |
| Screen reader behaviour | Static inspection cannot establish it | Accessibility testing |
```

## Positive controls

```markdown
## What is already working

✓ Password hashing with argon2id, parameters set in src/auth/hash.ts:12
✓ Centralized authorization middleware covering 11 of 14 admin routes
✓ Parameterized queries throughout the data layer — no string-built SQL found
✓ Dependency lockfile committed; CI runs the audit on every pull request
✓ Security headers configured in next.config.js, including a CSP without unsafe-inline
✓ Primary navigation and forms are keyboard operable with visible focus
```

Accurate praise is load-bearing: it tells the reader which parts of the system
not to break while fixing the rest.

## Language rules

| Never | Instead |
| --- | --- |
| "GDPR compliant" | "processes personal data; specific obligations may apply depending on jurisdiction" |
| "ISO 27001 compliant" | "repository evidence relevant to ISO/IEC 27001 Annex A themes" |
| "WCAG 2.2 AA conformant" | "no failures found in the criteria assessable from source; conformance requires manual testing" |
| "PCI DSS passed" | "the payment architecture appears to be hosted checkout, which typically minimises scope; scope is determined with your acquirer" |
| "There are no backups" | "no backup evidence found in the repository" |
| "Insecure" as a verdict | The specific weakness, the path, and the consequence |
| A percentage | A posture word, with the evidence behind it |

## If a score is demanded

Some organizations need a number for a dashboard. Give one only with:

- the exact scope it covers and what is excluded,
- the denominator — which controls were assessed and how many,
- the treatment of `UNABLE TO VERIFY` items, which must not be counted as passes,
- the date and commit,
- and a sentence stating it is an internal engineering indicator, not a
  compliance, certification or legal result.

Then never let it appear without those five things attached.

## Depth variants

| | |
| --- | --- |
| `QUICK` | Executive summary, applicability, top findings, first actions, limitations. One page |
| `STANDARD` | The full structure above |
| `DEEP` | Adds control-by-control tables, cross-framework references per control, and traceability from requirement to code to test |
| `FOCUSED` | The same structure narrowed to one domain, with the other domains explicitly out of scope |
