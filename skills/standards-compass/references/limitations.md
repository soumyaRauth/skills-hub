# Limitations, and the claims that must never be made

This is the part that keeps the skill honest, and it is not decoration. A
standards report is read by people making decisions about risk, contracts and
customers, and an overclaim in it does more damage than a missed finding.

## What this is

An engineering standards assessment and gap-analysis tool. It reads a
repository, works out which standards and frameworks are relevant, looks for
evidence, and reports gaps with their severity, confidence and limits.

## What this is not

Not a certification body. Not an accredited auditor. Not a legal adviser. Not a
conformity assessment. Not a penetration test. Not a guarantee of security,
accessibility, privacy or quality.

Certification and legal compliance rest on organizational processes, policies,
contracts, scope definitions, governance, operational evidence and, usually,
independent assessment. None of that is in a repository, and none of it can be
inferred from one.

## Claims that are never available

```
"This software is GDPR compliant"
"The company is ISO 27001 compliant" / "certified" / "ready"
"This application passed PCI DSS"
"WCAG 2.2 AA conformant"
"HIPAA compliant"
"SOC 2 compliant"
"This system is secure"
"No vulnerabilities were found"       ← says something about the world, not the review
```

The available forms:

```
"The repository appears to satisfy the following technical requirements…"
"The implementation shows evidence consistent with…"
"This assessment identified gaps relevant to…"
"No failures were found in the criteria assessable from source"
"Unable to verify from the repository"
"Applicability depends on facts outside this repository — specifically…"
```

The difference is not pedantry. The first set are statements someone can quote
to a customer or a regulator. They would be false, and they would be quoted.

## The standing limitations block

Every substantial assessment ends with this, adapted to what was actually done:

```markdown
## Assessment limitations

This assessment was based on the repository contents and the configuration
present in it, at commit <sha> on <date>.

It cannot verify:
- production infrastructure and cloud configuration
- organizational policies, procedures, or governance
- employee training, access management, or physical security
- contracts, data processing agreements, or vendor commitments
- legal applicability of any regulation
- whether documented processes are followed in practice
- runtime behaviour, real user experience, or production incident history
- certification or audit status
- anything held outside this repository

Automated and static analysis cannot establish conformance to any standard.
Where this report says a control appears to be implemented, that is a statement
about the evidence found, not a guarantee of effectiveness.
```

## Technical versus organizational

Keep the line visible in every report. A repository can show technical controls.
It cannot show that an organization operates a management system, follows a
process, holds a certificate, or has a contract.

```
ISO/IEC 27001    →  "repository evidence relevant to Annex A themes";
                    the ISMS itself is out of scope
SOC 2            →  a minority of the common criteria have technical evidence;
                    the auditor's opinion is the artefact
GDPR             →  technical measures are visible; lawful basis, records,
                    DPAs and transfers are not
PCI DSS          →  the integration architecture is visible; scope and
                    validation are determined with the acquirer
```

## Inherited controls

A control absent from the repository may be supplied by a managed platform, an
identity provider, a payment processor, or the organization's infrastructure.
Report it as *potentially inherited, verify externally* — not as missing. A
report that lists inherited controls as gaps trains its reader to skim.

## Uncertainty is an output

"I don't know" is a legitimate and frequent conclusion, and a report with a
substantial `UNABLE TO VERIFY` section is usually being more honest than one
without. What is not acceptable is uncertainty hidden behind confident phrasing,
or a gap quietly dropped because it could not be resolved.

## Where to stop

Some questions are not this skill's to answer, and the right response is to say
so and name who can:

| Question | Belongs to |
| --- | --- |
| Does GDPR apply to us? | Legal counsel |
| What is our PCI scope? | Acquirer or QSA |
| Are we SOC 2 ready? | The auditor, after an organizational readiness review |
| Is this AI system high-risk under the AI Act? | Legal counsel |
| Is our medical device software safe? | Domain safety process and qualified assessors |
| Did our production config get applied? | Whoever operates the infrastructure |

Answer the engineering half of each honestly, and hand over the rest without
pretending it is a technical question.
