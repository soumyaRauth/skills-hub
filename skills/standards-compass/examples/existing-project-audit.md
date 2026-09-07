# Existing project audit — eight months, no standards, one question

**Request:** *"We've been building this for eight months. We never consciously
followed any software standards. Tell me how bad the situation is."*

A 150k-line multi-tenant SaaS product. The wrong response is 300 best practices.
The right one starts by narrowing.

---

## The opening

> I'll work out which standards and frameworks are actually relevant to this
> application first, then assess the repository against those areas, separate
> real implementation gaps from things I simply cannot verify from a repository,
> and give you a prioritized list.
>
> Two things would change the assessment and aren't visible in the code: are
> your users in the EU or UK, and has any customer asked you for SOC 2 or ISO
> 27001? If you'd rather not decide now, I'll assess what applies either way and
> mark those as unresolved.

Then the work. No further commentary until there is something to say.

---

## The report

```markdown
# Standards Assessment — Customer Management Platform

Assessed          2026-09-07 · commit 4f2a9c1
Scope             Application source, configuration, schema, CI definitions.
                  Production infrastructure and organizational processes
                  are outside this assessment
Maturity assessed Production
Overall posture   NEEDS ATTENTION

3 high-risk gaps · 8 medium · 6 areas that cannot be verified from the code

The most serious issue is that three administrative operations don't enforce
the authorization rule the other eleven use, so a signed-in member may be able
to invoke them — including a customer export that isn't scoped to their own
organization.

The application also writes customer email addresses into application logs,
which spreads personal data into a system with its own retention and access
rules.

Separately, there's no evidence in the repository about backups, recovery, or
incident handling. That's not the same as their absence — those things normally
live outside a codebase — but nobody can confirm them from here.

First five actions
1. Fix the authorization gap in the admin API, and scope the export by tenant.
2. Stop logging customer email addresses.
3. Add negative authorization tests so this can't regress silently.
4. Confirm with whoever runs the infrastructure that backups exist and restore.
5. Decide whether EU users are in scope — it changes what privacy work applies.
```

## 3. Applicable standards

```markdown
DIRECTLY APPLICABLE
  OWASP ASVS 5.0.0         Authenticated multi-tenant app taking untrusted input
  OWASP API Security 2023  SPA and mobile clients call the JSON API directly
  WCAG 2.2                 Public web UI with interactive workflows

USEFUL
  ISO/IEC 25010            Vocabulary for the reliability findings below
  NIST SSDF                Supply chain, given you sell to enterprises

POTENTIALLY APPLICABLE
  GDPR                     Personal data is processed; jurisdiction UNKNOWN
  ISO/IEC 27001            If you hold or want an ISMS, or a customer asks
  SOC 2                    If a customer has asked for a report
  PCI DSS v4.x             Stripe Checkout is hosted, which usually minimises
                           scope; scope is determined with your acquirer

NOT CURRENTLY INDICATED
  HIPAA                    No clinical data or healthcare relationship observed
  ISO/IEC 42001, EU AI Act No AI functionality found in the repository
  CIS Benchmarks           No infrastructure-as-code here; platform appears managed
```

Nine standards considered, four assessed against. That ratio is the product.

## 5. Critical and high findings

```markdown
### [HIGH] Administrative endpoints bypass the shared authorization policy

STD-003 · control: authorization · gap: implementation
Standards: OWASP ASVS · API Security Top 10 (API5) · NIST CSF PR.AA
Severity HIGH · Confidence HIGH

Evidence
  src/api/admin/users.ts:41-67     authenticates, no role check
  src/api/admin/exports.ts:22-40   same, and the query is not tenant-scoped
  src/api/admin/billing.ts:15-33   same
  src/middleware/requireRole.ts    the policy the other 11 admin routes use

Impact  A signed-in member can list all users and trigger a customer export.
        At exports.ts:31 the export query has no tenant filter, so the export
        can reach other organizations' records.

Fix     Route the three handlers through requireRole('admin'); add the tenant
        filter to the export query. Both use infrastructure that already exists.

Verify  A negative integration test per endpoint (403 for a member session),
        and one asserting an export cannot cross tenants.
```

Two more at HIGH: customer email addresses in application logs
(`src/lib/logger.ts:28`, personal data spreading into a system with different
retention), and password reset tokens stored unhashed
(`prisma/schema.prisma:88` — a database read becomes an account takeover).

## 9. Unable to verify

```markdown
| Area | What is missing | Who can answer |
| --- | --- | --- |
| Backup and restore | No configuration or procedure in-repo | Infrastructure owner |
| Incident response | No documented process or security contact | Engineering leadership |
| Production TLS and headers | Deployment config not in this repository | Hosting owner |
| EU data subjects | Determines privacy applicability | Business owner or legal |
| Screen reader behaviour | Not establishable statically | Accessibility testing |
| Model provider terms | No AI in the repo; disregard unless that changes | — |
```

## 10. What is already working

```markdown
✓ argon2id password hashing with explicit parameters — src/auth/hash.ts:12
✓ Centralized authorization middleware covering 11 of 14 admin routes
✓ Parameterized queries throughout; no string-built SQL found
✓ Lockfile committed; CI runs the dependency audit on every pull request
✓ Security headers including a CSP with no unsafe-inline — next.config.js
✓ Keyboard-operable primary navigation with visible focus
```

## 13. Limitations

The standard block from `references/limitations.md`, with the specific
exclusions this run had.

---

## What the engineer got

Four standards that matter, six things already working, eleven meaningful gaps,
three of them serious, six items routed to people who can actually answer them —
and no claim that anything is or is not compliant with anything.
