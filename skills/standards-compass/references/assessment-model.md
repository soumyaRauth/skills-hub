# Assessment: status, gap type, confidence, severity, priority

Five separate judgments. Collapsing any pair of them is how standards reports
become untrustworthy — most commonly by turning "we could not verify this" into
"this failed", and by inheriting severity from whichever standard sounds
strictest.

## Status

```
PASS                    Evidence shows the control is implemented
PARTIAL                 Implemented in some paths, not others; or implemented weakly
FAIL                    Evidence shows the control is absent or incorrect where it is needed
NOT APPLICABLE          The requirement does not apply to this system — say why
UNABLE TO VERIFY        Expected evidence is not in the repository
REQUIRES MANUAL REVIEW  Only a human can settle it
```

The two on the right are not softer versions of `FAIL`. They mean something
different and they route to different people. A `FAIL` goes to an engineer. An
`UNABLE TO VERIFY` goes to whoever knows the answer. A `REQUIRES MANUAL REVIEW`
goes into someone's testing plan.

```
Wrong:  FAIL — no backup strategy
Right:  UNABLE TO VERIFY — no backup configuration, snapshot policy, or restore
        procedure found in the repository (searched: ops/, infra/, .github/,
        docs/, package scripts). Backups may exist in the cloud provider,
        managed by the database service, or in an operations runbook outside
        this repository. Verify externally.
```

## Gap type

Every non-passing status is one of five kinds of gap. This determines who can
act, and it is the distinction that most reports get wrong.

| Gap type | Means | Fixed by |
| --- | --- | --- |
| **Implementation** | The code does not satisfy the requirement | An engineer, in this repository |
| **Evidence** | It may satisfy it; nothing here shows it | Adding the evidence — a test, a config in-repo, a documented decision |
| **Process** | An organizational process cannot be established from a repository | The organization. **Never** by writing code |
| **Legal scope** | Applicability depends on facts outside the code | Legal or leadership, answering a question |
| **Manual verification** | Requires human testing | A tester, with a stated method |

Writing a `SECURITY.md` does not create an incident response capability. Adding
a retention comment does not create a retention policy. Where the honest answer
is "this is a process gap", say so and stop — a code change that papers over it
makes the next audit *less* accurate.

## Confidence

Confidence is about the finding, not about the risk.

| | Means |
| --- | --- |
| `HIGH` | Direct evidence, mechanism traced, would survive a reviewer opening the file |
| `MEDIUM` | Strong indication; some part of the path unverified |
| `LOW` | Plausible from partial evidence; stated as a question more than a claim |

```
Severity: HIGH · Confidence: MEDIUM
→ if this is what it looks like, it is serious, and the repository does not
  settle whether it is. Here is what would settle it.
```

Low confidence is not a reason to suppress a serious finding. It is a reason to
say what would raise it, and to put it in the verification section rather than
the fix-immediately list.

## Severity

`CRITICAL` · `HIGH` · `MEDIUM` · `LOW` · `INFORMATIONAL`

Judged from consequence in **this** system, weighing security impact, privacy
impact, safety, business impact, regulatory relevance, exploitability, how many
users are affected, data sensitivity, reversibility, and likelihood.

Never inherit severity from the standard. The same missing rate limit is
`INFORMATIONAL` on an internal read-only dashboard and `HIGH` on a public
password reset endpoint, and a rule that assigns it one severity everywhere is
not doing the work.

Anchors:

| | |
| --- | --- |
| `CRITICAL` | Exploitable now with serious consequence — exposed live credentials, unauthenticated access to customer data, cross-tenant leakage |
| `HIGH` | Serious, with a plausible path — privilege escalation, sensitive data in logs, missing authorization on privileged operations |
| `MEDIUM` | Real weakness, mitigating factors or narrower blast radius |
| `LOW` | Best-practice deviation with limited consequence here |
| `INFORMATIONAL` | Worth knowing; not a defect |

## Risk and ordering

```
risk ≈ impact × likelihood × exposure, adjusted for uncertainty
```

Qualitative. Do not manufacture numeric scores; a "7.4" implies a measurement
model this assessment does not have.

The default remediation order — security-critical exposure, sensitive-data
exposure, regulatory risk, data integrity, availability and recovery,
authorization, authentication, accessibility, quality and reliability,
maintainability, documentation — is a starting point, **not a rule**. Context
overrides it: a public-sector product's accessibility obligation can outrank an
internal hardening gap, and a data-integrity bug in a financial ledger outranks
almost everything.

## Maturity changes the bar

The same repository produces different reports at different maturities, and
pretending otherwise is what makes standards work feel like bureaucracy.

| Maturity | Report |
| --- | --- |
| Prototype | Dangerous mistakes only — exposed secrets, unauthenticated data access, plaintext credentials, obviously hostile input paths. No process findings. Say explicitly that the bar was set here |
| MVP | Add authorization consistency, personal data handling, dependency risk, basic accessibility of core flows |
| Production | Full technical assessment. Operational evidence — logging, monitoring, backups, incident path — becomes expected, and its absence is a real finding |
| Business-critical | Add availability, recovery, auditability, change management, tenant isolation depth |
| Regulated / high assurance | Traceability and evidence become findings in their own right. Absence of records is a gap, not a nuance |

A prototype told to build a governance programme ignores the whole report. A
regulated system told to "add some tests" has been failed by it.

## Over-compliance is a defect

Recommendations that fail this test do not go in the report:

- Encryption for data with no confidentiality requirement
- Audit trails for actions nobody will ever need to reconstruct
- Architectural change justified by a framework rather than by a risk
- Tooling a two-person team cannot operate
- Logging volume that becomes its own privacy problem

Every recommendation names the risk it reduces. If that sentence cannot be
written, delete the recommendation.
