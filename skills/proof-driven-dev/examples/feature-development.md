# Example — Feature development

A high-risk feature, one failed verification, one repair, and a four-line
answer.

---

**Developer:**

> Add password reset.

---

## 1. Investigate before asking

```
Repository       Node + TypeScript, Express, Prisma (PostgreSQL)
Tests            Vitest — `npm test`; integration tests hit a test database
Existing auth    src/auth/{login,session,invites}.ts
Related pattern  src/auth/invites.ts — single-use, hashed, 1h TTL token
Mailer           src/mail/send.ts, mocked in tests via src/mail/__mocks__
```

Everything the request left open is answered by `invites.ts`: token shape,
storage, expiry, and how the mailer is faked in tests. No question is asked.

## 2. Contract

Risk: **high** — authentication, credential handling, silent failure modes.

```yaml
objective: "Users can securely reset their password by email"
risk: high
assumptions:
  - "Tokens expire in 1h and are stored hashed — matches src/auth/invites.ts:22"
  - "Reset email is sent through src/mail/send.ts, mocked in tests as invites are"
requirements:
  - { id: AUTH-001, priority: critical, description: "A user can request a reset for their email",        proof: { type: integration } }
  - { id: AUTH-002, priority: critical, description: "A valid request creates one single-use token bound to that user", proof: { type: integration } }
  - { id: AUTH-003, priority: critical, description: "An unknown email returns the same response as a known one", proof: { type: security } }
  - { id: AUTH-004, priority: critical, description: "A token past its expiry is rejected",                proof: { type: security } }
  - { id: AUTH-005, priority: critical, description: "A token already used once is rejected on reuse",     proof: { type: security } }
  - { id: AUTH-006, priority: critical, description: "After reset, the new password authenticates",        proof: { type: integration } }
  - { id: AUTH-007, priority: critical, description: "After reset, the old password no longer authenticates", proof: { type: integration } }
  - { id: AUTH-008, priority: high,     description: "Existing email/password login is unchanged",         proof: { type: regression } }
```

Five of the eight were never in the request. AUTH-003, AUTH-004, AUTH-005 and
AUTH-007 are where password reset is usually broken; AUTH-008 is what the change
could break on its way past.

## 3. Proof plan

```
Stage 1  npm run typecheck · npm run lint            always
Stage 2  npm test -- tests/auth/reset.test.ts        AUTH-001..007
Stage 3  npm test -- tests/auth/                     AUTH-008 + regression
Baseline npm test -- tests/auth/   →  31 passed      captured before implementing
```

## 4. Implement, then verify

```
Stage 1   typecheck pass · lint pass
Stage 2   npm test -- tests/auth/reset.test.ts
          15 passed, 1 failed

FAIL  "rejects a token that was already used"
      expected  400 token_invalid
      received  200 { ok: true }
```

## 5. Contradiction

```
Reasoning   consumeToken() marks the token used, so reuse cannot succeed
Observed    the same token reset the password twice, both 200
```

The reasoning is wrong, not the test. Evidence wins.

## 6. Classify, then repair

```
Classification  IMPLEMENTATION_ERROR
Diagnosis       consumeToken() writes used_at AFTER the response is sent
                (src/auth/reset.ts:64) — the guard on the second request reads
                a row that has not been updated yet.
Fix             mark the token consumed inside the same transaction as the
                password write, before responding.
Attempt         1 of 2 (high risk)
```

Re-verify the failing requirement **and** the ones that already passed — the fix
moved a write inside a transaction, which is exactly the kind of change that
breaks a neighbor.

```
Stage 2   npm test -- tests/auth/reset.test.ts     16 passed
Stage 3   npm test -- tests/auth/                  47 passed
```

## 7. Evidence

```json
{
  "requirement": "AUTH-005",
  "method": "integration",
  "command": "npm test -- tests/auth/reset.test.ts -t \"rejects a token that was already used\"",
  "expected": "Second use of a consumed token is rejected",
  "actual": "PASS — 1 passed. Response: 400 {\"error\":\"token_invalid\"}",
  "status": "PASS",
  "level": "A",
  "attempts": 2,
  "notes": "First attempt failed: used_at was written after the response."
}
```

## 8. What the developer sees

```
✓ VERIFIED

Password reset

Requirements   8/8
Tests          47/47
Regression     pass (existing auth suite, 31 → 47)
Changed        6 files

Ask for details, evidence, or the contract.
```

Not shown by default: the six files, the repair, the transaction reasoning, the
token design. All of it is one question away — *show failed attempts* returns
section 6 in full.

---

## What this example demonstrates

- The repository answered every question the request left open. Nothing was
  asked.
- Five of the eight requirements were unstated by the developer, and one of them
  caught a real defect.
- A test disagreed with confident reasoning. The reasoning lost.
- The failure was classified before any code changed — the diagnosis
  (write-after-response) is what made the fix correct rather than plausible.
- Repair re-verified everything, not just the failing requirement.
- The final message is four lines for a change that touched six files.
