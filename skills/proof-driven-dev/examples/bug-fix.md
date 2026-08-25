# Example — Bug fix

A bug fix has a stricter proof obligation than a feature: the first requirement
is that the bug **reproduces**. Without that, a passing test at the end may be
passing for reasons that have nothing to do with the fix.

---

**Developer:**

> Checkout is broken for some customers. Fix it.

---

## 1. Compile the intent

"Broken" is a symptom. The contract cannot be written until the symptom is a
behavior. Ask *only* what cannot be found by looking, and look first:

```
git log --oneline -12 -- src/checkout/
  a4f1c92  Add promotional code support to checkout      (3 days ago)
Sentry / error log in repo?     no
Failing tests today?            npm test -- tests/checkout/  →  38 passed
```

The suite is green, so the bug is outside its coverage. One question is
unavoidable, and it is material — without it there is nothing to reproduce:

```
What do the affected customers see — an error, a wrong total, or a
checkout that never completes?
```

> **Developer:** Wrong total. Some orders are charged less than they should be.

Money, silently wrong. Risk: **critical**.

## 2. Reproduce before fixing

```
CHECKOUT-000  The bug reproduces in a test
```

Requirement zero, and the whole fix depends on it. Reading `promotions.ts`
suggests a stacking problem; a test settles it:

```
test: two 20%-off promotions applied to a $100 cart
expected  $100 → one promotion applies → $80
actual    $100 → both apply, compounding → $64

FAIL — confirmed. The bug is real and now has a red test.
```

## 3. Contract

```yaml
objective: "A cart charges the correct total when promotions overlap"
risk: critical
requirements:
  - { id: CHECKOUT-000, priority: critical, description: "The wrong-total bug reproduces in a failing test", proof: { type: unit } }
  - { id: CHECKOUT-001, priority: critical, description: "Two applicable promotions apply the better one, not both", proof: { type: unit } }
  - { id: CHECKOUT-002, priority: critical, description: "A single promotion still applies exactly as before", proof: { type: regression } }
  - { id: CHECKOUT-003, priority: critical, description: "Stacking-allowed promotions still stack, per the promotions.stackable flag", proof: { type: unit } }
  - { id: CHECKOUT-004, priority: critical, description: "Order total, tax, and payment amount agree to the cent", proof: { type: integration } }
  - { id: CHECKOUT-005, priority: high,     description: "Existing checkout suite passes unchanged", proof: { type: regression } }
  - { id: CHECKOUT-006, priority: high,     description: "Orders already placed at the wrong total are identified, not silently left", proof: { type: database } }
```

CHECKOUT-003 exists because the naive fix — never stack — would break the
`stackable` flag the schema already has. CHECKOUT-006 exists because a
money bug that already ran has consequences the code fix does not address.

## 4. Fix the cause, not the symptom

```
Cause    applyPromotions() reduces over every matching promotion
         (src/checkout/promotions.ts:41). The stackable flag added three days
         ago is read into the row but never consulted.
Fix      partition by stackable: stack the ones flagged stackable, take the
         single best of the rest.
```

The symptom fix — capping the discount at 20% — would leave the same bug for
every other discount pair. The cause fix is smaller and covers all of them.

## 5. Verify

```
Stage 2  npm test -- tests/checkout/promotions.test.ts
         CHECKOUT-000  now passes  →  the fix addresses the reproduced bug
         CHECKOUT-001  pass   two 20% promotions → $80
         CHECKOUT-003  pass   two stackable promotions → $64
         CHECKOUT-002  pass   single promotion → unchanged
Stage 3  npm test -- tests/checkout/            43 passed  (38 + 5 new)
Stage 3  CHECKOUT-004  pass   order.total === payment.amount, 12 seeded carts
```

CHECKOUT-006 is a query, not a code change:

```
SELECT count(*) FROM orders o JOIN order_promotions p ON …
WHERE o.created_at > '<the deploy of a4f1c92>' AND promo_count > 1
  AND NOT all_stackable

→ 23 orders, total under-charge $1,847.20
```

No repair is applied to those rows. Refunding, re-charging, or leaving them is a
business decision — the skill reports it and stops.

## 6. What the developer sees

```
⚠ REVIEW REQUIRED

Checkout — overlapping promotions compounded instead of taking the best one.
Cause: the stackable flag added in a4f1c92 was never read.

Requirements   7/7 verified
Tests          43/43 (5 new, including the failing reproduction)
Regression     pass

Decision required:
23 orders placed since a4f1c92 were under-charged by $1,847.20 total.
They are listed in .proofbuild/evidence/CHECKOUT-006.json — nothing was
changed. Refund the difference, re-charge, or leave them?
```

---

## What this example demonstrates

- One material question was asked, because "broken" cannot be reproduced.
- The bug had to fail a test *before* it was fixed. A fix without a reproduction
  is a guess with a green suite.
- The cause fix beat the symptom fix on both correctness and diff size.
- A near-miss regression (`stackable`) became a requirement instead of a
  post-mortem.
- The already-corrupted data was surfaced as a decision — money that has already
  moved is never repaired automatically.
- Status is `⚠ REVIEW REQUIRED` even though every requirement passed, because a
  decision is open. Green checks do not overrule an open decision.
