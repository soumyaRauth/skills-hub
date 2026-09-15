---
name: api-contract-guard
description: Settle what a new or changed interface promises before consumers depend on it — HTTP and GraphQL APIs, webhooks, events and queue messages, public SDK or library APIs, CLI output other tools parse. Reads the project's existing conventions (naming, error shape, pagination, auth, idempotency, versioning, money and time formats) so the new surface matches them; writes down the decisions that cannot be taken back once someone integrates (identifiers, field types and nullability, enum openness, error codes, idempotency and retry safety, pagination stability, webhook delivery and signing); and classifies a change as additive, behavioral or breaking, with a migration path. Use when adding or changing an interface that consumers deploy separately from — mobile apps, partners, other services, public API users, webhook receivers. Not for internal functions, UI-only work, or endpoints whose every consumer ships in the same deploy.
---

# API Contract Guard

> **What does this interface promise — and which of those promises can never be
> taken back?**

Code is cheap to change, and a promise to someone who deploys on their own
schedule is not. Once a mobile build ships, a partner integrates, or a webhook
receiver is written against a payload, every field name, status code and retry
behavior carries weight. *We'll fix it in v2* means running v1 for years.

Coding agents produce endpoints well. What they miss is that this endpoint is
the first in the API to use offset pagination where the others use cursors, or
that `POST /refunds` without an idempotency key will refund twice on the
client's first retry.

The deliverable is a short block of decisions, written before the code:

```
CONTRACT  GET /v1/invoices — public, API-key clients
FOLLOWS   error envelope {error:{code,message}} (src/api/errors.js:3) · cursor
          pagination ?cursor=&limit=, max 100 (GET /v1/payments) · amounts as
          integer minor units + currency · timestamps ISO-8601 UTC
DECIDES   order by (created_at, id) so cursors stay stable under inserts ·
          status is an open enum, clients must tolerate new values · another
          customer's invoice returns 404, identical to a missing one
CHANGE    additive
HANDOFF → proof-driven-dev: contract tests for page stability and cross-customer 404
```

## Activation

**Engage when** a change adds or alters an interface that someone else deploys
against: a public or partner HTTP or GraphQL API, a webhook sent or received, an
event or message another service consumes, a published SDK or library API, CLI
output or exit codes that scripts parse, a file format others import. Also
engage on changes to the response shape, status codes, errors, pagination,
authentication or versioning of such an interface.

**Stay quiet when** every consumer ships in the same deploy, such as an
internal endpoint only this repository's own frontend calls, unless old clients
outlive a deploy (cached single-page apps, installed mobile builds). Also stay
quiet for internal functions and modules, whose callers are Impact Map's
concern, for UI-only work, and for refactors behind an unchanged interface.

**Depth** `CONSULT`: the decisions block, then the work. `ACTIVE` when designing
a new public API or making a breaking change. Never `GATING`.

**Composes with** `impact-map` (who consumes the interface today, found in the
repository; this skill decides what it should promise) · `proof-driven-dev`
(each decision becomes a contract test) · `production-guard` (verifies
idempotency and retries after the fact) · `standards-compass` (authorization,
rate limiting and data exposure: the security half of an API stays there).

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. If it is
  not installed, do the smallest version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
<!-- /skills-hub:protocol -->

## Non-negotiable rules

1. **Conventions are read, not assumed.** Before recommending a shape, find how
   this API already does it: an existing endpoint, the error helper, the OpenAPI
   or GraphQL schema, the SDK. Cite the location. A recommendation that ignores
   the house convention is a new inconsistency, however good it is in the
   abstract.
2. **Deviations are explicit.** When the new surface must differ, write it as a
   `NEW DECISION` with its reason. Never introduce a second style quietly.
3. **Consumers are evidenced.** Claim an external consumer only from evidence:
   a mobile app in the repository, a published OpenAPI document, versioned
   routes, API keys, webhook subscriptions, documentation addressed to
   integrators, a package published to a registry. Otherwise it is an open
   question.
4. **Every change is classified.** `ADDITIVE`: a new optional field, a new
   endpoint. `BEHAVIORAL`: the same shape with a different meaning, which is the
   dangerous one. `BREAKING`: a field removed, renamed or retyped; a newly
   required input; tighter validation; a changed status code, ordering or
   pagination; a changed auth scope. A behavioral change is breaking for every
   consumer that relied on the old meaning.
5. **Irreversible decisions are written down**, in the decisions block and, when
   the project keeps one, in the schema or API documentation in the same change.
6. **No best-practice lecture.** Every line in the block is a convention followed
   (with its location), a decision made (with its reason), or a question for a
   person. Anything else is deleted.
7. **Short.** The block fits in about ten lines. Detail is available when asked
   for.

## Workflow

### 1. The surface and its consumers

Name the kind of interface: HTTP, GraphQL, webhook, event, SDK, CLI or file. Name
its visibility: public, partner, internal but separately deployed, or internal
and same-deploy. Then state the consumer evidence. For same-deploy only, stop
here. If the code is shared, Impact Map covers its callers.

### 2. Harvest the conventions

Find two or three existing interfaces of the same kind, and read off:

- naming and casing, and ID format
- the error envelope and code vocabulary
- pagination style, parameter names and maximum page size
- filtering and sorting syntax
- authentication and scopes
- idempotency header
- versioning scheme
- timestamps and time zones, money representation
- null versus absent, envelopes versus bare arrays
- rate-limit headers
- webhook signing and retry schedule

Each becomes a `FOLLOWS` line with its location. If nothing comparable exists,
say so: this surface sets the convention, and that is itself a decision.

### 3. Decide what cannot be taken back

`references/contract-decisions.md` lists the decisions per interface kind, and
what goes wrong later when each is left implicit. The ones that come up most:

- **Any interface:** identifiers, field names, types, nullability, whether an
  enum is open, machine-readable error codes, default ordering.
- **Writes:** idempotency and retry safety, concurrency control, partial
  success in batch operations.
- **Lists:** page stability under inserts, maximum page size, and whether to
  return totals, which are expensive to compute and impossible to withdraw.
- **Webhooks and events:** at-least-once delivery and the event id receivers
  deduplicate on, ordering, signing with a timestamp and replay window, the
  retry schedule, payload versioning.

### 4. Classify a change to an existing contract

Go field by field: `ADDITIVE`, `BEHAVIORAL` or `BREAKING`. A breaking change
needs a stated migration path, and `references/compatibility.md` has the usual
ones: add alongside and deprecate, a new version, dual-emit for events, a sunset
date. Also say how consumers find out.

### 5. Write it down, then hand off

Put the decisions block before the work. Update the contract document the
repository keeps in the same change. Hand the decisions to `proof-driven-dev`
as contract tests: the shape, error codes, page stability, idempotent retry, and
signature verification.

## What this skill is not

- **Not an API style guide.** The house style is whatever this repository
  already does. The skill enforces consistency with it, not a preference.
- **Not a security review.** Authorization depth, rate limiting and data
  exposure belong to Standards Compass. This skill states which principal the
  contract lets see what, and hands the rest over.
- **Not an impact map.** It decides what an interface should promise. Impact
  Map finds who, in this repository, already depends on what it promises now.

## References

- `references/contract-decisions.md` — the decisions per interface kind, and what goes wrong later without them
- `references/compatibility.md` — additive, behavioral and breaking changes, and migration paths

## Worked examples

`examples/public-list-endpoint.md` — a public list API that follows the house
conventions · `examples/outgoing-webhook.md` — a webhook's delivery contract ·
`examples/breaking-rename.md` — a field rename that a separate service consumes ·
`examples/internal-endpoint.md` — the endpoint that gets no contract block.
