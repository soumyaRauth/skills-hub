# Security Validation

Behavior-oriented, not checklist-oriented. The question is not "does this code
mention authorization?" but "can someone do something here they should not?"

## Authentication

Is authentication required for this path? Are unauthenticated requests rejected
by the server, with a status that does not leak whether the resource exists?
Does a new route inherit the middleware everyone assumes it does — or was it
registered outside the protected group?

## Authorization

The highest-yield area in most reviews.

- Can a **different role** perform the operation?
- Can a user act on an **object they do not own** by changing an ID?
- Are **object-level** permissions enforced, or only route-level? Route-level
  auth answers "may this user use this endpoint"; it does not answer "may this
  user touch *this record*".
- In a **bulk** operation, is every item authorized, or only the first?
- Does the **backend** enforce what the UI enforces?

That last one is the recurring finding. A hidden button is not a permission
check. Verify the server rejects the request when the UI would not have sent it.

## Input manipulation

Can IDs be enumerated or substituted? Can a client send fields the UI never
exposes — role, price, status, owner — and have them mass-assigned? Can filters
or sort parameters reach a query builder unvalidated? Can a path parameter
escape its intended directory?

## Data exposure

Check what actually leaves the system:

- API responses, including nested and serialized relations
- Error messages and stack traces
- Logs, especially structured logs that dump whole objects
- Exports, reports, webhooks
- Cache keys and URLs

Look for credentials, tokens, password hashes, internal IDs, other users' data,
and personal information that the endpoint has no reason to return.

## Multi-tenancy

If the repository has tenants, organizations, workspaces, or accounts, verify
that tenant A cannot reach tenant B's data:

- Is the tenant scope applied at the query layer, or remembered by convention at
  each call site? Convention fails eventually.
- Does a new query path include the scope?
- Do bulk, export, report, admin, and job paths include it too? These are where
  scoping is most often forgotten, because they were written by someone thinking
  about volume rather than isolation.

## Destructive and privileged operations

Deletion, role changes, impersonation, credential resets, and financial
mutations deserve: explicit authorization, an audit record identifying the
actor, confirmation for irreversible actions, and rate limiting where
enumeration or abuse is plausible.

## Reporting security findings

Give the concrete path, not a category name:

```
🔴 BLOCKER — Bulk deletion authorizes only the requesting user's role,
not each target record.

Evidence:  BulkDeleteController::destroy() calls authorize('bulkDelete', User::class)
           once, then deletes every id in the payload without a per-record check
           (app/Http/Controllers/BulkDeleteController.php:34).
Risk:      A team admin can delete users outside their team by supplying their ids.
Confidence: High — the ids come straight from the request body.
Recommendation: Authorize each target, or scope the query to the actor's team
           before deleting.
```

Do not report theoretical vulnerabilities with no path to them, and do not
escalate a missing defense-in-depth measure to a blocker when no exploit exists.
Precision is what makes the blockers believable.
