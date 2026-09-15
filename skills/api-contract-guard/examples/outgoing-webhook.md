# Example — an outgoing webhook

Illustrative.

## Request

> Send a webhook to our customers' systems whenever an order ships.

## What was read

- No existing outgoing webhooks. `src/notify.js` sends email only.
- `db/schema.sql`: no table for subscriptions or deliveries.
- `src/orders/ship.js` sets `is_shipped` and writes a `shipments` row.
  `src/orders/cancel.js` can still cancel a shipped order. That is a lifecycle
  problem, and it is out of scope here, but it means a receiver could get
  `order.shipped` for an order that is later cancelled.

**Consumers:** customers' own systems. This is external by definition, and
there is no convention to follow yet, so this change sets one.

## Response

```
⚡ API Contract Guard — first outgoing webhook; this sets the convention

CONTRACT  POST <customer endpoint> — event order.shipped
DECIDES   delivery at least once; each event carries a unique id, and receivers
          dedupe on it · no ordering guarantee; payload includes occurred_at
          · signed: HMAC-SHA256 over "<timestamp>.<body>" in
          X-Signature, 5-minute replay window; per-customer secret, rotatable
          · retries on non-2xx or timeout (10 s), backoff over 24 h, then
          disabled with an email to the account · thin payload: order id,
          shipment id, tracking, occurred_at; receivers fetch the rest
          · payload carries "version": 1
NEW       webhook_endpoints and webhook_deliveries tables; the delivery runs
          from a job, not inside ship.js's request
OPEN      cancel.js allows cancelling a shipped order: send order.cancelled too,
          or treat shipped as final? Receivers will act on order.shipped.
HANDOFF → proof-driven-dev: signature verifies; replay older than 5 min rejected;
          redelivery carries the same event id; a failing endpoint is retried
          then disabled
HANDOFF → standards-compass: customer-supplied URLs mean outbound requests to
          arbitrary hosts (block private address ranges)
```

## Notes

- **Every line is a decision a receiver will build against.** The event id and
  at-least-once delivery are written down first, because a receiver that does
  not deduplicate gets a double delivery on the first retry.
- **The lifecycle gap was raised once**, as an open question about this
  contract, and left there. Deciding the order lifecycle belongs to the project,
  not to the webhook.
- **The server-side request forgery risk of a customer-supplied URL was handed
  over**, not reviewed here.
