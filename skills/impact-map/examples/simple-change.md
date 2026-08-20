# Example 1 — Simple business logic change

A single-layer change in a small Node/TypeScript service. Shows what a *short*
impact map looks like: the value here is confirming the surface is small, and
catching the one place that would have been missed.

## Request

> Customers should be able to cancel an order within 30 minutes of placing it,
> instead of the current 15.

**CHANGE STATEMENT:** Extend the order cancellation window from 15 to 30 minutes.

## Change surface

Directly relevant: the cancellation rule in the order service, one duplicated
copy of the rule in the UI, and the tests pinning the current window.

## 🟥 MUST CHANGE

```
src/services/orderService.ts

  Symbol:         CANCELLATION_WINDOW_MINUTES, canCancel()
  Relationship:   Defines the window constant and the only server-side check
                  that enforces it.
  Evidence:       `const CANCELLATION_WINDOW_MINUTES = 15` at line 8, read by
                  canCancel() at line 24.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Change the constant to 30.
```

```
tests/orderService.test.ts

  Symbol:         "rejects cancellation after the window"
  Relationship:   Asserts the current 15-minute boundary directly.
  Evidence:       Test constructs an order placed 16 minutes ago and expects
                  canCancel() to be false.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Update the boundary fixtures; keep one case just inside and
                  one just outside the new window.
```

## ⚠️ HIDDEN COUPLING

```
web/src/components/OrderActions.tsx

  Symbol:         isWithinCancelWindow()
  Relationship:   Reimplements the same rule client-side to decide whether to
                  render the Cancel button.
  Coupling type:  Duplicated business logic
  Evidence:       `Date.now() - placedAt < 15 * 60 * 1000` at line 31. No import
                  from the service; the value 15 is inlined.
  Classification: ⚠️ HIDDEN COUPLING
  Confidence:     High
  Action:         Update alongside the service, or better, have the API return a
                  `cancellableUntil` timestamp so the rule lives in one place.
```

```
docs/support/order-cancellation.md

  Relationship:   Support runbook tells agents the window is 15 minutes.
  Coupling type:  Documentation
  Evidence:       "within 15 minutes of placing the order".
  Classification: ⚠️ HIDDEN COUPLING
  Confidence:     High
  Action:         Update the runbook in the same change.
```

## Dependency paths

```
CANCELLATION_WINDOW_MINUTES        ← the change
  ↓ read by
orderService.canCancel()
  ↓ called by
orderController.cancel()  →  POST /orders/:id/cancel
  ↓ response consumed by
web OrderActions.tsx  (which also re-implements the rule locally)
```

## Test impact

- `tests/orderService.test.ts` protects the boundary behavior — must be updated.
- No test covers `OrderActions.tsx`'s client-side window check, so the duplicated
  rule can drift silently. Worth a small component test as part of this change.

## Risk

**Low** — one constant, one duplicate, no schema or contract change, and the
server-side rule is authoritative. The only real failure mode is updating the
service and leaving the UI hiding the Cancel button after 15 minutes.

## Recommended implementation order

1. Update `CANCELLATION_WINDOW_MINUTES` in `orderService.ts`.
2. Update the boundary tests.
3. Update `OrderActions.tsx` (or remove the duplicate rule in favor of an
   API-provided value).
4. Update the support runbook.

## Open questions

- Should the new window apply to orders placed before the deploy? The check is
  evaluated at request time, so it will — confirm that is intended.
