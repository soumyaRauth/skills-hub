# Observability

One question:

> If this fails in production at 3 AM, how would the team find out, and what
> would they have to work with?

## What earns a requirement

Risk sets the bar. Trivial functions need nothing. These need real coverage:

- Money movement and financial state changes
- Authentication, authorization, and role changes
- Destructive operations
- Anything asynchronous — the user is not watching when it fails
- External integrations — someone else's outage becomes your incident
- Bulk operations — partial success is invisible without a record

## What good looks like for a mutation

For an important state change, the system should be able to answer, after the
fact:

- **Who** performed the action
- **What** changed, from what to what
- **When**
- **Which entity** was affected
- **What the outcome** was, including partial outcomes

That is an audit record, not a log line, when the entity is sensitive. Logs
rotate; audit records are supposed to survive.

## Failure visibility

- Are errors reported somewhere a human will see, or only caught and logged?
- Does a **swallowed exception** hide the failure entirely? `except: pass`, an
  empty catch block, or a `.catch(() => null)` turns an incident into a mystery.
- For background jobs: is failure distinguishable from "still running"? Is there
  a dead-letter path, and does anyone look at it?
- For partial failures: is the partial outcome recorded, or only the exception?

## Diagnosability

When someone investigates, can they correlate? Look for a request/correlation
id, the entity id in log context, and structured fields rather than
interpolated prose. A log line reading `Failed to process` with no identifiers
is indistinguishable from no log line at all.

## What not to do

- Do not demand logging in every function.
- Do not recommend logging sensitive values — tokens, passwords, full payment
  details, personal data. That converts an observability gap into a security
  finding.
- Do not treat a missing metric as a blocker unless the operation is genuinely
  unmonitorable and high-risk.

## Reporting

```
🟠 HIGH — Bulk deletion produces no audit record.

Evidence:  Individual deletion calls AuditLog::record() (UserService.php:88);
           the bulk path deletes directly via the query builder and never does
           (BulkDeleteService.php:31).
Risk:      Deletions performed in bulk are unattributable after the fact. The
           single-delete path is auditable, so the discrepancy is silent — the
           audit trail looks complete while missing the highest-volume path.
Confidence: High — verified by comparing both code paths.
Recommendation: Emit one audit record per deleted user in the bulk path, with
           the acting admin and the operation id.
```
