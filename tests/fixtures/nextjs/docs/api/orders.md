# GET /api/orders

Returns every order for the current session.

## Response

```json
[
  { "id": "ord_1", "state": "pending", "total": 25 }
]
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Order identifier |
| `state` | string | One of `pending`, `paid`, `cancelled`, `shipped` |
| `total` | number | Order total in currency units |
