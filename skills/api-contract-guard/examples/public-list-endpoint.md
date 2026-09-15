# Example — a public list endpoint

Illustrative. The repository is invented; the shape of the decisions is the point.

## Request

> Add an endpoint so API customers can list their invoices.

## What was read

- `src/api/payments.js`: `GET /v1/payments`, the only existing list. It uses
  cursor pagination (`?cursor=&limit=`, `limit` capped at 100, `next_cursor` in
  the body), orders by `created_at` descending, and filters on
  `req.apiKey.accountId`.
- `src/api/errors.js:3`: every error goes through
  `sendError(res, status, code, message)`, which produces
  `{ "error": { "code", "message" } }`.
- `src/api/refunds.js`: `POST /v1/refunds` honours an `Idempotency-Key` header.
  Not relevant to a read, but noted as the house convention for writes.
- `docs/openapi.yaml`: documents `/v1/payments` and `/v1/refunds`, and is
  published at `/docs`.
- `src/db/schema.sql`: `invoices.amount_cents` integer plus `currency`;
  `status` with `draft | open | paid | void`.

**Consumers:** external. The route is under `/v1`, authenticated by API key,
and documented in a published OpenAPI file.

## Response

```
⚡ API Contract Guard — public API, consumers deploy separately

CONTRACT  GET /v1/invoices — public, API-key clients
FOLLOWS   cursor pagination ?cursor=&limit=, max 100, next_cursor (GET /v1/payments)
          · error envelope via sendError (src/api/errors.js:3) · amount_cents +
          currency · ISO-8601 UTC timestamps · scoped to req.apiKey.accountId
DECIDES   order by (created_at DESC, id DESC): payments orders by created_at
          alone, so its cursor can skip rows on a timestamp tie — not copied here
          · status is an open enum, documented as such, since 'uncollectible' is
          on the roadmap in docs/billing.md · no total count
CHANGE    additive
OPEN      should `void` invoices appear by default? (payments has no equivalent)
HANDOFF → proof-driven-dev: page stability with tied timestamps, another account's
          key gets an empty list, limit=101 → 400 invalid_limit
```

Then the endpoint, following `payments.js`, with `docs/openapi.yaml` updated in
the same change.

## Notes on what it did

- **It did not copy a flaw.** The house convention is followed, except the one
  place it is broken: ordering by a non-unique key. That appears as a decision
  with its reason, and the existing endpoint is not silently changed.
- **It deferred the enum question.** Declaring the enum open now costs nothing.
  Declaring it later breaks every client that switched exhaustively.
- **It left out totals.** A total count is expensive, and it can never be
  withdrawn once clients display it.
- **The open question went to a person**, and the default is stated.
