# Risk Model

Risk decides three things: how deep verification goes, how many repair attempts
are allowed, and how early the loop stops for a human. Getting it wrong in
either direction is expensive — over-verifying a copy change wastes the
developer's time, under-verifying a payment change spends their money.

## Levels

### Low

Copy, styling, isolated UI, documentation, comments, log messages, dead-code
removal.

Blast radius is the thing itself. Proof floor: build/lint/typecheck plus the one
check that would catch a mistake — often just rendering the component.

### Medium

CRUD behavior, business logic, API request/response shape, UI state, additive
schema changes, new endpoints, background jobs with bounded effects.

Blast radius is one feature and its callers. Proof floor: a targeted check per
requirement, plus the existing suites covering the touched area. Regression
matters here for the first time — this is where "it works" and "everything else
still works" diverge.

### High

Authentication, authorization, data migration, destructive operations,
multi-tenancy, external integrations, permission models, anything touching
personal data, and anything whose failure is silent.

Proof floor: the Medium floor, plus explicit negative and boundary cases, plus
regression evidence for the surrounding feature. Repair budget drops to 2 — a
high-risk change that needs three attempts is a change that needs a human.

### Critical

Financial transactions, credential handling, irreversible data operations,
infrastructure changes with wide blast radius, anything that moves money or
cannot be undone.

Proof floor: the High floor, plus replay/idempotency evidence, plus rollback
behavior. Repair budget 1. Prefer stopping with `⚠ REVIEW REQUIRED` and a clear
question over a second automated attempt at something irreversible.

## Signals that raise the level

Any one of these promotes the change a level:

- Money, credentials, or personal data are involved.
- The operation is irreversible, or its failure mode is silent.
- Multi-tenant data boundaries are in play.
- The change touches something many callers depend on.
- It runs unattended — a cron, a queue consumer, a webhook handler.
- It has no existing test coverage, and you are changing behavior.
- Recent history shows the area is volatile — repeated fixes, reverts.

When two levels are defensible, take the higher one and say why in one line.

## What each level changes

| | Low | Medium | High | Critical |
| --- | --- | --- | --- | --- |
| Contract persisted | no | if it spans sessions | yes | yes |
| Negative cases required | no | for validation paths | yes | yes |
| Regression evidence | no | targeted | targeted + surrounding suite | broad |
| Idempotency / replay | no | if async | yes | yes, explicit |
| Rollback verified | no | for schema changes | for migrations | yes |
| Repair budget | 3 | 3 | 2 | 1 |
| Stop and ask on ambiguity | rarely | material only | material, readily | readily |

## Checklists by change type

**Authentication / authorization** — unauthenticated access rejected;
authenticated-but-unauthorized rejected; cross-tenant access rejected; expired
credential rejected; token reuse rejected; identifier tampering rejected;
existing login paths still work.

**Payments** — the same operation run twice charges once; a provider timeout
does not double-charge; a failed charge leaves no fulfilled order; a refund path
exists for every charge path; amounts and currency survive the round trip
exactly; webhook replay is idempotent.

**Data migration** — the migration applies to a copy of realistic data; rollback
either works or is documented as one-way *before* running; existing rows satisfy
the new constraints; the application works against both old and new shapes if
the deploy is not atomic; indexes exist for the queries that will hit the new
columns; nothing runs against production.

**Destructive operations** — the scope of deletion is bounded and verified by a
count before and after; cascades are enumerated; there is a confirmation or a
dry run; the operation is logged with who and what; partial failure leaves a
recoverable state.

**External integrations** — timeouts are set; failures degrade rather than hang;
retries are safe to repeat; the response is validated before use; credentials
come from configuration, never from source.

Report what the tested properties showed. Not that the system is secure, correct,
or safe — those are claims no test set can support.
