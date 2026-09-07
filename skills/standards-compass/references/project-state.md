# Project state

Without state, every audit starts from zero, re-derives the same profile,
re-reports findings the team already rejected, and cannot tell a new problem from
an old one. State is what turns this from a report generator into something that
gets more useful over time.

```
.project-standards/
├── profile.md                  what this software is, labelled
├── applicable-standards.yaml   the applicability decisions and why
├── findings.md                 open findings, with status history
├── accepted-risks.md           findings the team decided to live with
├── exceptions.md               intentional deviations, with compensating controls
└── assessment-history.md       dated assessments: what was checked, what changed
```

## Rules

1. **Create it only when there is something to record** — normally after the
   first real audit, not after answering a question.
2. **Mention it once**, in a line: *"Recording the assessment in
   `.project-standards/` so the next one can tell what changed."* Never mention
   it again.
3. **If the user does not want it**, keep the state in the session and say
   nothing further. The skill degrades to single-session reasoning; it does not
   argue about a directory.
4. **The repository outranks the cache.** Re-verify any recorded finding before
   repeating it. A finding fixed three weeks ago and still listed as open is the
   fastest way to lose the reader.
5. **Never write secrets, customer data, or personal data into these files.**
   Redacted references only.
6. **Write nothing else, anywhere.** State plus the work that was asked for.

## profile.md

The Phase 1 profile with its labels intact, plus the maturity level and the date.
Re-verify anything load-bearing; a profile that says "no payments" six months
after Stripe arrived poisons the whole applicability set.

## applicable-standards.yaml

```yaml
assessed_at: "2026-09-07"
maturity: production
standards:
  - id: owasp-asvs
    applicability: directly-applicable
    why: Authenticated multi-tenant application with untrusted input
    scope: Application source and configuration
  - id: gdpr
    applicability: potentially-applicable
    why: Personal data is processed; jurisdiction of users is unknown
    unresolved_question: Are users or the organization in the EU or UK?
    asked_on: "2026-09-07"
  - id: hipaa-security-rule
    applicability: not-currently-indicated
    why: No clinical data, healthcare integration, or covered entity relationship observed
    revisit_if: Health data or a healthcare customer appears
```

Recording the negatives is what stops the next audit re-litigating them.

## findings.md

One entry per finding, keyed by a stable id, carrying status history.

```markdown
### STD-003 — Administrative endpoints bypass the shared authorization policy

control: authorization · severity: HIGH · confidence: HIGH · gap: implementation
first_seen: 2026-09-07
evidence: src/api/admin/{users,exports,billing}.ts
status:
  2026-09-07  OPEN
  2026-09-19  FIXED — routed through requireRole(); tests/authz/admin-routes.test.ts
  2026-09-19  VERIFIED — 14 negative tests executed, 14 passed
```

Ids are stable forever. A finding that returns reopens its own entry rather than
becoming a new one, which is how you see that it has now happened twice.

## accepted-risks.md

```yaml
- finding: STD-014
  status: accepted-risk
  reason: Internal tool behind SSO; brute-force risk judged immaterial
  accepted_by: "recorded from the user's own statement on 2026-09-12"
  expires: "2027-01-01"
  revisit_if: The tool is exposed outside the corporate network
```

**Never invent an approver.** Record who the user said approved it, or record
that it was accepted in conversation without a named approver. An expiry or a
revisit condition is required — an acceptance with neither is just a suppressed
finding.

## exceptions.md

```markdown
### POST /api/webhooks/stripe — anonymous access is intentional

Reason                Payment provider callbacks cannot authenticate as a user
Compensating control  Signature verification against the endpoint secret,
                      src/api/webhooks/stripe.ts:18
Status                Accepted exception, recorded 2026-09-07
```

Once recorded, do not report it again. Re-raising a settled exception in new
wording is the single fastest way to make the skill unwelcome. The one thing
that reopens it is the compensating control disappearing — and that is a
regression, reported as such.

## assessment-history.md

```markdown
2026-09-07  STANDARD audit · ASVS, API Top 10, WCAG 2.2, LLM Top 10
            17 findings (3 high, 8 medium, 6 unable-to-verify)
2026-09-19  FOCUSED security re-check after authorization fixes
            7 resolved · 0 new · 1 regression (STD-021 test deleted)
```

Which lets a later report open with something a team can feel:

> Since the September assessment: 7 findings resolved, 4 new, 1 regression.

## Regression detection

A regression is a control that previously passed and no longer does. It is the
highest-value output of persistent state, because nobody discovers it by
reading a diff.

```markdown
### REGRESSION — authorization

Previously  PASS (2026-09-19) — all 14 admin routes behind requireRole()
Currently   FAIL — src/api/admin/reports.ts:12 authenticates only
Cause       New route added 2026-10-02; did not adopt the shared middleware
Severity    HIGH · Confidence HIGH
Fix         Route through requireRole('admin') and add the negative test the
            other 14 routes have
```

Check for regressions whenever a previously assessed area changes, whenever an
audit runs against an existing baseline, and whenever a diff touches a file
cited as evidence for a passing control.

## Staleness

State is a cache. Treat it as stale when the profile has moved (a new
integration, a new data category, a new interface), when the recorded commit is
far behind, or when a cited evidence file no longer contains what was cited.
Re-verify the affected areas and correct the file. Do not carry forward a
finding you have not re-checked, and do not carry forward a `PASS` either.

## Baseline comparison

```markdown
Compared with 2026-09-07

Improved     7 findings resolved, including both high-severity authorization gaps
Regressed    1 — negative authorization tests removed in commit 8c1f0a2
New          4 — all in the new billing module
Unchanged    6 unable-to-verify items; still no infrastructure evidence in-repo
```
