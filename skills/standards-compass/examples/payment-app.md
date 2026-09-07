# `/standards payments` — PCI scope reasoned from the architecture

**Request:** *"We take payments. Are we PCI compliant?"*

The question cannot be answered, and saying so badly is unhelpful. Saying so
well is one of the more valuable things this skill does.

---

## What the repository shows

```
src/api/billing/checkout.ts:22   stripe.checkout.sessions.create({...})
                                 → redirect to Stripe-hosted page
src/api/webhooks/stripe.ts:9     handler reads req.body, no signature check
src/services/refund.ts:41        refund by charge id, no idempotency key
prisma/schema.prisma             payments table: provider_charge_id, amount_cents,
                                 currency, status, last4, brand
                                 → no PAN, no CVV, no expiry
src/components/Invoice.tsx       renders last4 from the payments table
```

Searches for `cardNumber`, `cvv`, `card_number`, `pan`, and the standard test
card prefixes return nothing outside the Stripe SDK's own types.

---

## Response

```markdown
## Payments — what I can and cannot tell you

**I can't tell you whether you're PCI compliant, and neither can any
repository.** Scope and validation are determined with your acquirer, and
compliance is an organizational status, not a property of source code. What I
can do is describe the architecture accurately, which is what that conversation
starts from.

### The architecture, as the code shows it

You use Stripe Checkout. The customer is redirected to a page Stripe hosts
(`src/api/billing/checkout.ts:22`); no card fields are rendered by your
application and no card data reaches your servers. Your `payments` table stores
a charge id, amount, currency, status, and the last four digits and brand —
none of which is cardholder data in the sense that drives PCI scope.

That architecture typically puts a merchant in the smallest applicable
requirement set. Two caveats, both real:

- Minimal integrations are not automatically out of scope. The v4.x
  requirements covering scripts on payment pages reach merchants who never
  touch a card number, and your checkout entry page is yours.
- Scope determination and the validation route are decided with your acquirer,
  or a QSA. Anything I say here is an input to that, not a substitute.

### Three findings that have nothing to do with PCI, and cost real money

**[HIGH] The Stripe webhook handler doesn't verify signatures**
`src/api/webhooks/stripe.ts:9` — the handler parses the body and marks the
payment as paid. Anyone who can reach the endpoint can post a forged event and
mark an order paid. Stripe's SDK provides `constructEvent` with the endpoint
secret; this is a small change.
Control: api-security · Confidence HIGH

**[HIGH] Refunds are not idempotent**
`src/services/refund.ts:41` — a retried request issues a second refund. Retries
happen automatically from queues, load balancers and impatient support agents.
Pass an idempotency key derived from the refund request.
Control: reliability · Confidence HIGH

**[MEDIUM] No audit trail on money movement**
Refunds and manual charge adjustments write to `payments` with no record of
who did it. When a customer disputes a refund in four months, nothing answers
"who issued this, and when".
Control: auditability · Confidence HIGH

### What to do

Fix the webhook signature check today — it's the one with a straightforward
abuse path. Then idempotency, then the audit trail. And when you talk to your
acquirer about PCI, the useful sentence is: "we use Stripe Checkout, hosted
redirect, we store no cardholder data" — then let them tell you what validation
that implies.
```

---

## The two ways to get this wrong

**Overclaiming:** *"You use hosted checkout, so PCI DSS doesn't apply."* Scope
is not the code's to determine, and the payment-page requirements are a real
exception.

**Alarmism:** *"You process payments, so all of PCI DSS applies — here are 300
requirements."* A hosted-checkout merchant does not have the obligations of one
handling card data directly, and treating them the same buries the three
findings that actually matter.
