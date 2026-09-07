# Guardrail mode — standards during ordinary development

The audit is the visible half of this skill. This is the half that prevents the
audit from finding anything.

The design constraint is restraint. A skill that comments on every request gets
turned off in week two, and then the password reset gets built without rate
limiting anyway. Silence on low-risk work is what buys the right to speak on
high-risk work.

## The cheap pass

Every implementation request, one question:

```
Does this touch identity, privilege, money, personal data, files, or a model?

  no  →  build it. Say nothing.
  yes →  classify → name the requirements → build accordingly → verify → one short note
```

## Risk classification

Depends on context, not on keywords. "Add a field" is `LOW` for a nickname and
`HIGH` for a national identifier.

| | Examples |
| --- | --- |
| `LOW` | Copy changes, styling, refactors with no boundary change, non-personal fields, internal reporting on existing data |
| `MEDIUM` | New user-facing forms, profile fields, list filters, new non-privileged endpoints, notifications, search |
| `HIGH` | Authentication changes, roles and permissions, payments, sensitive personal data, file uploads, bulk export, admin operations, webhooks, AI over user data |
| `CRITICAL` | Cryptographic infrastructure, password or token handling, privileged access paths, card data, tenant isolation boundaries, anything safety-relevant |

## Before implementing

`LOW`: nothing. Build it.

`MEDIUM` and up: one short block, then the work. Not a negotiation, not a
warning, not a request for permission.

```markdown
### Standards consideration

This touches authentication and account recovery, so I'll build it with:

- single-use, expiring, hashed reset tokens
- the same response whether or not the address exists
- rate limiting per address and per IP
- an audit entry on reset request and completion

Implementing now.
```

Four to six lines. If it runs longer than the change itself, cut it.

## Requirement sets by feature

The ones worth knowing by heart. Each is a starting point to adapt, not a
checklist to recite at the user.

**Password reset** — single-use token, short expiry, stored hashed, generic
response regardless of account existence, rate limiting, session invalidation on
change, notification to the account, audit record.

**File upload** — type and size limits enforced server-side, storage outside the
web root or in object storage, generated filenames, content-type not trusted
from the client, authorization on both upload and download, malware
consideration where files are shared between users, and a keyboard-accessible
alternative to any drag-and-drop interaction.

**Bulk export of personal data** — authorization at least as strict as viewing
the underlying records, tenant scoping in the query, audit record naming actor,
scope, and row count, rate or size limits, expiry of the generated artifact, and
a decision about whether the export lands somewhere permanent.

**Admin panel** — one authorization policy shared with the rest of the app,
audit trail on state-changing actions, no privilege escalation path through
role assignment, and negative tests per route.

**User deletion** — what actually happens to related records, whether deletion
is soft or hard, what remains in logs, analytics, caches, search indexes, and
backups, whether a legal retention obligation conflicts, and an audit record of
the deletion itself.

**Payments** — the integration model first (`payments.md`), never card data in
logs or the database, webhook signature verification, idempotency on retries,
and an audit trail on money movement.

**AI over user data** — what enters the prompt and whose data it is, retrieval
scoped per user or tenant, model output treated as untrusted before rendering or
executing, tool calls constrained to the user's own privileges, prompt and
output logging decided deliberately, and the provider's data handling checked
(`ai.md`).

**Authentication changes** — session lifetime and invalidation, credential
storage, MFA interaction, account enumeration, lockout and its own denial-of-
service risk, and what happens to existing sessions.

## During implementation

If the code being written would violate a relevant requirement, fix it in place
and say so in one line. Do not finish the insecure version and note it
afterwards.

> The reset token was going into the database in plaintext — storing a hash
> instead, so a database read cannot be replayed as a reset.

## After implementing

A compact check. Ticks for what is covered, warnings for what is not, and no
victory lap.

```markdown
### Standards check — password reset

✓ Token single-use, 30 min expiry, stored hashed
✓ Identical response for known and unknown addresses
✓ Rate limited — 5 per address per hour, 20 per IP
✓ All sessions invalidated on successful reset
⚠ No automated test for the rate limit yet
⚠ Reset emails go through the existing provider; their retention of the email
  body is outside this repository
```

Then record it in `.project-standards/` if state exists — one line, so the next
audit knows this area was deliberately built rather than accidentally correct.

## Diff and pull-request review

When a diff is available, assess the change, not the repository.

```markdown
Standards impact of this change

🔴 Authorization   HIGH    New route src/api/reports/export.ts does not use
                           requireRole(); every other export route does
🟠 Auditability    MEDIUM  Bulk export with no audit entry
🟢 Privacy                 No new personal data categories
🟢 Accessibility           No UI surface in this change
```

Four lines beats a re-run of the full audit. Prioritize changed files, then what
they call and what calls them, then the controls those paths implement.

## Regression

If a change removes or weakens a control that previously held, say so
immediately and name what it used to do:

> This moves the handler out from behind `requireRole()`. That check is what
> currently keeps non-admin members out of `/api/admin/exports` — is the new
> path intended to be public?

`project-state.md` covers how a recorded baseline makes this detectable across
sessions rather than only within one.

## What not to do

- Do not run a full audit because someone asked for a feature.
- Do not attach a standards note to a rename.
- Do not block work. Name the requirement, build it in, move on.
- Do not repeat a consideration the user has already dismissed for this project;
  record the exception (`project-state.md`) and stop raising it.
- Do not lecture. One block before, one block after, both short.
