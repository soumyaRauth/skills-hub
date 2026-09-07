# Payment assessment

The `/standards payments` focus. One rule dominates: **determine the payment
architecture before saying anything about PCI DSS.** Scope is a function of how
payments are integrated, and getting it wrong in either direction is expensive —
a false alarm wastes months, and a false all-clear leaves a real obligation
unaddressed.

## Establish the integration model

Read the code. The payment provider's SDK, the checkout components, the API
calls and the webhook handlers tell you which of these it is:

| Model | What it means | Typical scope effect |
| --- | --- | --- |
| Hosted payment page | The customer is redirected to the provider's page | Smallest scope. Card data never reaches the application |
| Provider-hosted fields / iframe | The provider's elements are embedded; the page is yours | Small scope, but the payment page itself is in scope for script integrity requirements |
| Tokenization in the client | Card data goes from browser to provider; a token comes back | Similar to above; verify the card fields are genuinely the provider's |
| Direct API | The application receives card data and forwards it | Large scope. Report this prominently |
| Storage of card data | PAN, and worse, CVV stored | Critical finding. CVV must never be stored after authorization |

Then check the claim against the evidence, because these often disagree: a team
that believes it uses a hosted page may have one form that posts card fields to
its own backend "just for the retry flow".

## What repository evidence can show

- Whether card numbers, CVV or expiry appear in code, schemas, fixtures, tests,
  seed data or logs. Search for the field names and for test card numbers.
- Which integration model is actually used, per flow — checkout, subscription
  update, retry, refund, admin-initiated charge. Flows diverge.
- Scripts loaded on the payment page, which matter under the v4.x requirements
  even for minimal integrations.
- Webhook handling: signature verification, replay protection, idempotency.
  Unverified payment webhooks are a straightforward financial-integrity finding
  independent of PCI.
- Idempotency on charge, refund and payout paths. A retried charge is a real
  incident, and retries are automatic.
- Authorization on refunds, credits and payment method changes — privileged
  money-moving operations that are frequently protected less carefully than the
  admin panel.
- Audit trail on money movement: who, what, when, how much, and the result.
- Amounts stored as integers in minor units rather than floats.

## What it cannot show

Cardholder data environment boundaries · network segmentation · merchant level ·
SAQ eligibility · validation status · the provider's own compliance · what
happens in the payment page at runtime. All external.

## Wording

```
Never   "PCI DSS compliant" / "not compliant" / "in scope" / "out of scope"
Never   "You only need SAQ A"
Do      "Payments use Stripe Checkout — the customer is redirected to Stripe's
         hosted page (src/api/billing/checkout.ts:22), and no card fields are
         rendered or received by this application. No PAN, CVV or expiry
         appears in the schema, code, or fixtures. That architecture typically
         minimises the applicable PCI DSS requirement set, but scope and
         validation are determined with your acquirer, and the v4.x
         requirements covering scripts on payment pages can still reach
         merchants with minimal integrations. Confirm with your acquirer or a
         QSA.

         Independent of PCI, two findings: the webhook handler does not verify
         the signature (src/api/webhooks/stripe.ts:9), and refunds are not
         idempotent, so a retried request issues a second refund
         (src/services/refund.ts:41)."
```

The second paragraph is often the one that matters most. Payment findings that
have nothing to do with PCI — unverified webhooks, non-idempotent charges,
missing authorization on refunds, float arithmetic on money — are concrete,
fixable, and cost real money when they go wrong.

## Beyond cards

If the product handles payouts, stored balances, lending, or holds customer
funds, financial regulation may be engaged and it is not this skill's to
determine. Raise it, name it as a question for the business, and focus the
engineering assessment on integrity: authorization, auditability, idempotency,
reconciliation, and whether the ledger can be reconstructed.
