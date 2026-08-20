# Example — Authentication change

**Risk: High.** Demonstrates authorization, session invalidation, privilege
escalation, and token behavior. Ends in 🟢 SHIP — included deliberately, because
a validation tool that never clears a change is not a gate, it is a filibuster.

```
╔══════════════════════════════════════════╗
║       PRODUCTION GUARD REPORT            ║
╚══════════════════════════════════════════╝

CHANGE
Allow users to change their own email address, requiring the current password
and confirmation from the new address before the change takes effect.

RISK CLASSIFICATION
High — email is an account-recovery identifier, so this is an account-takeover
surface.

VERDICT
🟢 SHIP

BLOCKERS  0      HIGH  0      MEDIUM  0      LOW  2

──────────────────────────────────────────

BASELINE
Scope:  full suite
Result: 486 passed, 0 failed

Current: 499 passed, 0 failed
Interpretation: 13 new tests, all passing; no regressions.

──────────────────────────────────────────

FUNCTIONAL VALIDATION     8/8   passed
REGRESSION VALIDATION     12/12 passed
SECURITY                  11/11 passed
DATA INTEGRITY            4/4   passed
FAILURE SCENARIOS         6/6   validated
OBSERVABILITY             3/3   passed

──────────────────────────────────────────

SECURITY CHECKS (all EXECUTED)

  Current password required                       PASS
  Wrong password rejected                         PASS
  Unauthenticated request rejected                PASS
  Cannot change another user's email              PASS
  user_id in the request body is ignored          PASS
  Confirmation token is single-use                PASS
  Confirmation token expires (1 hour)             PASS
  Token is not guessable (32 random bytes)        PASS
  Email uniqueness enforced by DB constraint      PASS
  Pending change does not free the old address    PASS
  Rate limited (5 attempts / hour / user)         PASS

FAILURE SCENARIOS

  SCENARIO                     EXPECTED        ACTUAL        STATUS
  ──────────────────────────────────────────────────────────────────
  Token used twice             rejected        rejected      PASS (executed)
  Expired token                rejected        rejected      PASS (executed)
  Target address already taken validation      validation    PASS (executed)
  Two concurrent requests      one succeeds    one succeeds  PASS (executed)
  Mail provider unavailable    change pending  change pending PASS (executed)
  User deleted mid-flow        token invalid   token invalid PASS (executed)

──────────────────────────────────────────

KEY VERIFICATIONS

Session invalidation — on confirmation, all other sessions for the user are
revoked and the acting session is re-issued
(EmailChangeService.php:71; tests/Feature/EmailChangeTest.php::test_other_sessions_revoked,
executed). This is the check most commonly missed in this kind of change: the
email is the recovery identifier, so a stale session held by an attacker would
survive the very change intended to lock them out.

Privilege escalation — the request DTO whitelists only current_password and
new_email; role and is_admin are not fillable
(UpdateEmailRequest.php:18). A test posting is_admin=true confirms it is
ignored (executed).

Audit trail — an EmailChanged audit record is written with actor, old value,
new value, timestamp, and IP (AuditLog::record, EmailChangeService.php:78).

──────────────────────────────────────────

⚠️ WARNINGS

🔵 LOW — No notification is sent to the *old* address when the change completes.

   Evidence:       Only the new address is mailed (EmailChangeService.php:64).
   Risk:           If an account is compromised, the legitimate owner gets no
                   signal that their email was changed. Low rather than high
                   because the password is required and other sessions are
                   revoked, so this is a detection gap rather than an exposure.
   Recommendation: Send a "your email was changed" notice to the previous
                   address.

🔵 LOW — The rate limit is keyed on user id only, not also on IP.

   Recommendation: Add an IP dimension to slow distributed attempts across many
                   accounts.

──────────────────────────────────────────

TESTS EXECUTED

  vendor/bin/phpunit                              →  499 passed
  vendor/bin/phpunit --filter EmailChange         →  13 passed
  vendor/bin/phpunit --filter Session             →  21 passed
  vendor/bin/phpstan analyse app/Auth             →  PASS
  vendor/bin/pint --test                          →  PASS

──────────────────────────────────────────

UNVERIFIED

- Deliverability behavior of the real mail provider (fake used locally)

──────────────────────────────────────────

RECOMMENDED ACTIONS

1. Notify the previous address on completion (LOW).
2. Add an IP dimension to the rate limit (LOW).

Neither is release-blocking.

FINAL VERDICT
🟢 SHIP — no blockers, no HIGH findings, and every category required for a
high-risk change was validated with executed checks. Session invalidation,
token single-use, and mass-assignment protection were each confirmed by test,
not by reading.
```
