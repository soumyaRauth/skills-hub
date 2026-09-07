# The control model

Five frameworks care about authorization. If the report says so five times, the
reader stops at the second. Findings are therefore made against **normalized
controls**, and standards are attached to findings rather than the other way
round.

```
Missing authorization on 3 admin endpoints        ← the finding
      │
      ├── control: authorization
      │
      └── referenced by: OWASP ASVS · OWASP API Security Top 10 · NIST CSF (PR.AA)
                         · ISO/IEC 27001 Annex A access control themes · SOC 2 CC6
```

One engineering problem. One fix. One verification. Several citations.

## Where the model lives

`registry/controls.yaml` — 36 concepts spanning identity, data, operations,
quality, supply chain and AI. Each carries the question it answers, the evidence
types that speak to it, and what to look for.

Standards entries list the controls they touch. Nothing maps in the other
direction, which means **adding a standard automatically extends the coverage of
every control it names**, with no mapping file to maintain and nothing to drift.

To answer "which standards care about `tenant-isolation`?", scan the entries for
that control id. That is the whole mechanism.

## Working with it during an assessment

1. **Evidence lands on a control**, not on a requirement. Reading
   `src/middleware/auth.ts` produces observations about `authentication`,
   `authorization` and `session-management`.
2. **A gap is opened against the control**, with its evidence, status,
   confidence and severity.
3. **Standards are attached at report time** by looking up which applicable
   entries name that control.
4. **Severity is judged from the engineering consequence**, never inherited from
   the strictest standard that happens to mention it.

## Why not map requirement-to-requirement

Cross-framework requirement mappings are large, contested, and stale on arrival.
They also encourage the failure this model exists to prevent: assessing the same
code five times because five documents phrase the same expectation differently.

The control layer is coarser and more honest. It says *this is the engineering
property in question*, and lets each standard's own document define its
requirement precisely. Where a specific requirement identifier is genuinely
useful in a report — an ASVS chapter, an API Top 10 entry, a NIST CSF outcome —
name it as a reference, and only when you can name it accurately.

## When one control is not enough

Some findings genuinely span controls. A bulk customer export with no audit
trail is `authorization` + `auditability` + `privacy`. Record the primary
control (the one the fix changes) and list the others. Do not split it into
three findings; a reader fixing one endpoint should see one item.

## The deduplication test

Before adding a finding, ask whether the underlying engineering problem is
already in the report under a different standard. If it is, extend that finding's
reference list instead. Two findings whose remediation is the same edit are one
finding.
