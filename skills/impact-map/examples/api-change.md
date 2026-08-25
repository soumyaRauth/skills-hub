# Example 2 — API response change

A Next.js application where a response field is renamed. Shows how a
"one-line serializer change" reaches consumers, tests, and documentation.

## Request

> Rename the `state` field on the orders API response to `status` so it matches
> the rest of our APIs.

**CHANGE STATEMENT:** Rename the `state` field to `status` in the orders API
response payload.

**INTERPRETATION:** Treated as a rename of the *response* field only. The
database column and internal type names are assumed to stay as they are — see
Open Questions.

## Change surface

The route handler and its response type, every frontend reader of the field, the
API contract document, and one fixture. External consumers could not be
confirmed from this repository.

## 🟥 MUST CHANGE

```
F1 · app/api/orders/route.ts

  Symbol:         GET handler response mapping
  Relationship:   Constructs the response object containing `state`.
  Evidence:       `return Response.json(orders.map(o => ({ id: o.id, state: o.status })))`
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Emit `status` instead of `state`.
```

```
F2 · types/order.ts

  Symbol:         OrderResponse
  Relationship:   Shared type describing the API payload; imported by both the
                  route handler and the client components.
  Evidence:       `state: OrderStatus` at line 12, imported in three files.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Rename the property. TypeScript will surface the direct
                  consumers at build time.
```

```
F3 · app/orders/OrderStatusBadge.tsx

  Symbol:         OrderStatusBadge({ order })
  Relationship:   Reads `order.state` to choose the badge variant.
  Evidence:       `switch (order.state)` at line 9.
  Classification: 🟥 MUST CHANGE
  Confidence:     High
  Action:         Read `order.status`.
```

## 🟧 LIKELY AFFECTED

```
F4 · app/orders/page.tsx

  Symbol:         server component data fetch
  Relationship:   Fetches the route and passes the payload down.
  Evidence:       Fetches `/api/orders` and passes results into the badge
                  component; does not name `state` itself.
  Classification: 🟧 LIKELY AFFECTED
  Confidence:     Medium
  Action:         Verify no sorting or filtering keys off `state` before
                  assuming it is pass-through.
```

## 🟨 NEEDS VERIFICATION

```
F5 · Unknown external consumers of GET /api/orders

  Relationship:   The route is public and unversioned; consumers outside this
                  repository would break on the rename.
  Evidence:       No API key gate or allowlist found on the route; no client SDK
                  in this repository. Absence of evidence, not evidence of
                  absence.
  Classification: 🟨 NEEDS VERIFICATION
  Confidence:     Low
  Action:         Check access logs or ask the API owner before renaming. If
                  external consumers exist, emit both fields for a deprecation
                  window instead.
```

## ⚠️ HIDDEN COUPLING

```
F6 · __tests__/fixtures/orders.json

  Coupling type:  Fixture
  Relationship:   Mock payload used by component tests, contains `"state"`.
  Evidence:       `"state": "pending"` in each of the three fixture objects.
  Classification: ⚠️ HIDDEN COUPLING
  Confidence:     High
  Action:         Update the fixture; otherwise tests keep passing against the
                  old shape and hide the break.
```

```
F7 · docs/api/orders.md

  Coupling type:  Contract documentation
  Relationship:   Documents the response schema with `state`.
  Evidence:       Response example block, line 34.
  Classification: ⚠️ HIDDEN COUPLING
  Confidence:     High
  Action:         Update in the same change.
```

## Dependency paths

```
types/order.ts :: OrderResponse.state       ← the change
  ↓ shapes
app/api/orders/route.ts (GET)
  ↓ HTTP response consumed by
app/orders/page.tsx
  ↓ props passed to
app/orders/OrderStatusBadge.tsx  →  reads order.state
  ↓ mirrored by
__tests__/fixtures/orders.json
```

## API impact

- **Backward compatibility:** breaking for any consumer not in this repository.
- **Mitigation available:** emit both `state` and `status` for one release, mark
  `state` deprecated in the docs, then remove.
- **Validation/authorization:** unaffected — the field is response-only.
- **Versioning:** the route is unversioned, so there is no compatible path other
  than dual-emission.

## Test impact

- Component tests protect badge rendering per status — they read the fixture, so
  update fixture and test together.
- No contract test asserts the response shape. Adding one during this change
  would catch the next rename automatically.

## Risk

**Risk score: 8+ / 18 → Medium** (lower bound — one factor unassessed)

```
Breadth             2   route handler, shared type, components, docs, fixture
Coupling opacity    1   the type is a hard edge; the fixture and the contract
                        doc carry the field name as a string
Test coverage       2   component tests read the fixture; no test asserts the
                        response shape itself
Reversibility       2   wire-format change on an unversioned route
Consumer reach      ?   whether consumers exist outside this repository could
                        not be determined here
Area volatility     1   normal churn, no stale files in the surface
```

The internal change is small and type-checked; the exposure is entirely in the
unassessed factor. Dual-emission does not make it Low — it takes reversibility
to 1 and settles consumer reach at 1, giving 8 / 18 — but it removes the
open-ended factor, which is the point.

## Recommended implementation order

1. Confirm whether external consumers exist.
2. Rename in `types/order.ts` and follow the type errors.
3. Update the route handler (add `status`; keep `state` if dual-emitting).
4. Update `OrderStatusBadge.tsx` and verify `page.tsx`.
5. Update fixtures and tests; add a response-shape assertion.
6. Update `docs/api/orders.md`.
7. Schedule removal of `state` if dual-emitted.

## Open questions

- Should the database column and internal `OrderStatus` type be renamed too, or
  only the wire format?
- Is there a deprecation policy for this API that dictates the dual-emission
  window?
