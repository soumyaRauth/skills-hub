# Example — Payment change

**Risk: High.** Money movement is always high risk. Demonstrates duplicate
requests, webhook retries, timeout behavior, transaction integrity, and
idempotency.

```
╔══════════════════════════════════════════╗
║       PRODUCTION GUARD REPORT            ║
╚══════════════════════════════════════════╝

CHANGE
Add a "Pay invoice" endpoint that charges a saved card through the payment
provider and marks the invoice paid.

RISK CLASSIFICATION
High — creates an irreversible external side effect and mutates financial state.

VERDICT
🔴 DO NOT SHIP

BLOCKERS  2      HIGH  1      MEDIUM  2      LOW  0

──────────────────────────────────────────

BASELINE
Scope:  targeted — tests/payments/ (full suite ~11 min, not run)
Result: 24 passed, 0 failed
Pre-existing failures: none in scope

──────────────────────────────────────────

FUNCTIONAL VALIDATION     6/6  passed
REGRESSION VALIDATION     9/9  passed
SECURITY                  4/4  passed
DATA INTEGRITY            2/4  passed
FAILURE SCENARIOS         3/7  validated
OBSERVABILITY             1/3  validated

──────────────────────────────────────────

🔴 BLOCKERS

#1 A retried request charges the customer twice.

   Category:       Idempotency
   Evidence:       PaymentController::pay() accepts no idempotency key and
                   performs no duplicate check before calling
                   provider.charge() (app/Http/Controllers/PaymentController.php:41).
                   Confirmed with a test: two sequential requests for the same
                   invoice produced two provider charges.
                   EXECUTED — tests/payments/duplicate_charge_test.py → FAIL
   Risk:           The client library retries on timeout. A charge that succeeds
                   at the provider but whose response is lost will be retried and
                   charged again. The customer is double-billed and the second
                   charge is not visible as a duplicate in our records.
   Confidence:     High — observed, not inferred.
   Recommendation: Accept an idempotency key from the client and forward it to
                   the provider, or add a unique constraint on
                   (invoice_id, status=succeeded) and check before charging.

#2 The provider is charged inside a database transaction that can roll back.

   Category:       Data integrity
   Evidence:       pay() opens a transaction, calls provider.charge(), then
                   writes the payment row and updates the invoice
                   (PaymentService.php:58-74). Any failure after the charge —
                   including the invoice update — rolls back the local rows.
   Risk:           The customer is charged and we have no record of it. The
                   invoice still shows unpaid, so a support retry charges again.
                   Reconciliation would have to come from provider exports.
   Confidence:     High — verified by reading the transaction boundary.
   Recommendation: Persist a pending payment row and commit *before* calling the
                   provider, then update it with the outcome. The external call
                   belongs outside the transaction.

──────────────────────────────────────────

⚠️ WARNINGS

🟠 HIGH — Webhook handler is not idempotent.

   Category:       Idempotency
   Evidence:       WebhookController::handle() marks the invoice paid and
                   dispatches SendReceipt on every payment_intent.succeeded
                   event, with no check on the event id (WebhookController.php:22).
   Risk:           Providers guarantee at-least-once delivery. A redelivered
                   event sends a second receipt and re-runs the paid transition.
   Confidence:     High.
   Recommendation: Store processed event ids and ignore repeats.

🟡 MEDIUM — Webhook signature is not verified.

   Evidence:       No signature check in the handler; the route is excluded from
                   CSRF and requires no authentication (routes/api.php:31).
   Risk:           Anyone who knows the URL can mark invoices paid. Not rated a
                   blocker only because the endpoint path is unguessable in
                   practice — that is obscurity, not a control.
   Recommendation: Verify the provider signature header before processing.

🟡 MEDIUM — No timeout is configured on the provider client.

   Evidence:       Client constructed with defaults (PaymentProvider.php:14).
   Risk:           A slow provider holds a request thread and its database
                   connection until the server's own timeout fires.
   Recommendation: Set an explicit connect and read timeout.

──────────────────────────────────────────

TESTS EXECUTED

  pytest tests/payments/ -q                  →  24 passed
  pytest tests/payments/duplicate_charge_test.py  →  FAIL (2 charges created)
  mypy app/payments                          →  PASS
  ruff check app/payments                    →  PASS

──────────────────────────────────────────

UNVERIFIED

- Provider timeout behavior — no sandbox credentials in this environment
- Partial refund path — not covered by tests and not exercised
- Concurrent payment of the same invoice from two sessions
- Currency rounding on multi-currency invoices — no fixture data

──────────────────────────────────────────

RECOMMENDED ACTIONS

1. Add an idempotency key and forward it to the provider (blocker #1).
2. Move the provider call outside the transaction; persist a pending row
   first (blocker #2).
3. Deduplicate webhook events by event id.
4. Verify webhook signatures.
5. Set explicit provider timeouts.
6. Add a test for concurrent payment of the same invoice.

FINAL VERDICT
🔴 DO NOT SHIP — 2 blocking issues. Both can double-charge a customer, and
neither is detectable from our own records after the fact.
```
