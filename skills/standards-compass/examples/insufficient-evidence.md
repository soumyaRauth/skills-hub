# The audit that mostly says "unable to verify"

**Request:** *"Audit this for compliance."*

**Project:** an 800-line Terraform repository plus a thin deployment wrapper. No
application code — the application lives in three other repositories the agent
has not been given.

Half of a good standards report is knowing when the evidence is not there. This
example exists because the tempting response is to produce a full-looking report
from a repository that cannot support one.

---

## Response

```markdown
## Standards assessment — infrastructure repository

I need to start with what this repository is, because it changes what an audit
can honestly say.

This repository contains Terraform for the AWS account and a deploy script. It
contains no application code. Most of what a standards assessment looks at —
authentication, authorization, data handling, input validation, accessibility,
privacy behaviour — is not here. I can assess the infrastructure definitions,
and I should be clear that this is a small fraction of a compliance picture.

If you point me at the application repositories I can assess those properly. If
this is the only repository, here is what it supports.

### What I can assess

**Applicable**
  CIS Benchmarks (AWS)     Infrastructure-as-code is exactly what this covers
  NIST SSDF                Build and deployment integrity
  ISO/IEC 27001 themes     A subset — access control and configuration only,
                           if an ISMS is in play

**Findings from the Terraform**

[HIGH] S3 bucket policy allows public read
  infra/storage.tf:34 — `acl = "public-read"` on the uploads bucket. If this
  bucket receives user uploads, they are world-readable.
  Confidence HIGH that the configuration says this. MEDIUM that it is deployed —
  Terraform is evidence of intent, and I cannot see the AWS console.

[MEDIUM] Security group allows 0.0.0.0/0 on port 22
  infra/network.tf:56 — SSH open to the internet on the bastion.

[MEDIUM] RDS instance has no automated backup retention set
  infra/database.tf:19 — `backup_retention_period` is not specified, so it
  takes the provider default. Whether that default meets your recovery
  expectations is a decision nobody appears to have recorded.

### What I cannot assess, and this is most of it

| | |
| --- | --- |
| Everything about the application | Not in this repository |
| Whether deployed state matches this code | Terraform is intent; the console is fact. No state file or plan output available |
| Personal data handling | No schema, no application code |
| Accessibility | No user interface here |
| Authentication and authorization | No application code |
| Backups, beyond the RDS setting | No backup jobs, snapshot policies, or restore procedures in this repository |
| Organizational anything | Out of reach of any repository |

### What I would not do

I'm not going to produce a compliance posture for the system from this. It
would look like an assessment and it would be one repository's worth of
infrastructure standing in for a product. If someone needs a posture, the three
application repositories are where most of the answer lives.

### One thing worth doing today

The public-read bucket at `infra/storage.tf:34`. If that is the uploads bucket
and it is deployed as written, customer documents are publicly readable, and
that is worth checking in the console in the next ten minutes regardless of
anything else in this report.
```

---

## What makes this correct

- It states the scope limit **first**, before any finding, so nothing that
  follows can be read as broader than it is.
- It still delivers real findings, with real paths. "Insufficient evidence" is
  not a reason to deliver nothing.
- Confidence is split from severity on the S3 finding: the configuration says
  one thing, and whether it is deployed is a separate question.
- It refuses to produce an overall posture, and says why in a sentence rather
  than apologizing.
- It ends with the one action that shouldn't wait for the rest of the process.
