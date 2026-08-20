# Change-Type Checklists

Starting points, not a closed list. When a change does not match anything here,
derive the checks from the failure taxonomy instead.

## Payments and financial mutations

Always **high risk**.

- Duplicate charge on client retry — is there an idempotency key?
- Duplicate charge on network timeout where the charge succeeded but the
  response was lost
- Webhook delivered twice (providers guarantee at-least-once, not exactly-once)
- Webhook signature verification
- Transaction boundary around the local record and the external charge
- Currency, rounding, and precision — integer minor units or decimal, never float
- Refund and partial refund paths
- Authorization: whose payment method, whose account, whose invoice
- Audit trail for every state change
- Reconciliation: can local state be compared against the provider?

## Authentication and session changes

Always **high risk**.

- Login, logout, and failed-login behavior
- Session invalidation on password change, role change, and logout-everywhere
- Token expiry, refresh, and revocation
- Privilege escalation via role or claim manipulation
- Password reset: token entropy, single use, expiry, and account enumeration
- Account takeover paths — email change, recovery, linked identities
- Rate limiting and lockout
- Whether existing sessions survive the change in a way that is intended

## Authorization changes

- Every route touched by the change still enforces authentication
- Object-level checks, not only route-level
- Bulk paths authorize every item
- Backend enforces what the UI hides
- Tenant scoping applied in every new query path
- Admin and impersonation paths audited

## Database migrations

- New non-nullable columns have a safe default for existing rows
- Backfill is batched and resumable, not one statement over a large table
- Locking duration on large tables; index creation strategy
- Deploy ordering: can old code run against the new schema during rollout?
- Reversibility, and what the down path loses
- Constraint additions that existing rows may violate
- Whether the new column needs an index for the queries introduced with it

## File uploads

- Size limits enforced server-side
- MIME type and extension validated server-side, not trusted from the client
- Path traversal in filenames
- Executable or archive content handling
- Storage failure mid-upload
- Duplicate uploads and name collisions
- Access control on retrieval — is the URL guessable?
- Cleanup of orphaned files when the owning record fails to save

## Bulk operations

- Partial failure semantics: atomic, or per-item with a result set
- Per-item authorization
- Transaction strategy and batch size
- Timeout against the number of items the UI permits selecting
- Memory growth with input size
- N+1 queries across the item loop
- Concurrent execution of the same bulk operation
- Retry safety
- Progress and per-item outcome reported to the user
- Audit records for every affected entity, not one for the batch

## API changes

- Backward compatibility of request and response shape
- Existing consumers in this repository; unknown consumers outside it
- Validation on every new or changed field
- Authorization unchanged or tightened, never accidentally loosened
- Error semantics: status codes and error body shape
- Versioning or dual-emission strategy for breaking changes
- Contract tests and documentation updated

## Background jobs and queues

- Idempotency — the job will run twice eventually
- Retry policy, backoff, and maximum attempts
- Dead-letter handling and whether anyone monitors it
- Job timeout versus realistic work duration
- Partial processing and resumability
- Worker death after an external side effect but before completion
- Payload shape compatibility with jobs already enqueued during deploy

## External integrations

- Timeout values set explicitly, not left to library defaults
- Retry policy and whether retries are safe for that endpoint
- Rate limits and backoff
- Malformed or unexpected response shape
- Dependency unavailable — degrade or fail?
- Version compatibility and deprecation notices
- Secrets handling and rotation
