# Decisions that cannot be taken back

For each kind of interface, the decisions a consumer comes to depend on, and
what goes wrong when a decision is left implicit. A decision the code makes
implicitly is still made. It is just made without anyone noticing.

Every line in a decisions block is one of three things: a convention followed,
with its location; a decision made, with its reason; or a question for a
person. Use this list to find the decisions. Do not recite it at the user.

## Any interface

| Decision | Left implicit, it becomes |
| --- | --- |
| **Identifier format.** Opaque string, integer, UUID, prefixed (`inv_…`) | Clients parse or sort ids. Changing the format later breaks them |
| **Field names and casing.** Match the house style | A second casing style in one API, forever |
| **Types and units.** Money as integer minor units plus currency; timestamps ISO-8601 with zone | Float rounding in someone else's ledger; local-time bugs across zones |
| **Nullability, and null versus absent** | Clients crash on the first `null` a field was never documented to hold |
| **Enum openness.** Can a new value appear? Say so, and clients must handle unknowns | Adding a status breaks every client that switched exhaustively |
| **Error model.** Status code plus a machine-readable code; the house envelope | Clients match on message text, and a copy edit becomes an outage |
| **Default ordering** | Clients rely on the order they happened to see first |

## Writes: create, update, delete, actions

| Decision | Left implicit, it becomes |
| --- | --- |
| **Idempotency.** An `Idempotency-Key`, or a natural key the server dedupes on | A retry after a timeout charges, refunds or sends twice |
| **Retry safety per status.** Which failures a client may retry | Clients retry a 400, or give up on a 503 |
| **Concurrency.** `ETag`/`If-Match`, a version field, or last write wins stated as such | Silent lost updates |
| **Partial success in batches.** Atomic, or a per-item result set | Clients cannot tell what happened to item 47 |
| **Response body.** The resource, an id, or nothing | Clients make a second round trip, or depend on fields you meant as internal |

## Lists and search

| Decision | Left implicit, it becomes |
| --- | --- |
| **Pagination style.** Cursor or offset, per house convention | Offset pages skip and duplicate items under inserts |
| **Stable ordering key.** Unique, for example `(created_at, id)` | Cursors that repeat or lose items at ties |
| **Maximum page size** | One client asks for `limit=100000` |
| **Totals.** Returned or not | An expensive count query nobody can ever remove |
| **Filter syntax** | A second filter dialect in one API |

## Webhooks and events

| Decision | Left implicit, it becomes |
| --- | --- |
| **Delivery.** At least once, stated; an event id receivers deduplicate on | Receivers double-process on redelivery |
| **Ordering.** Guaranteed or not; include a timestamp or sequence | Receivers apply `shipped` before `paid` |
| **Signing.** HMAC over the body plus a timestamp; replay window; secret rotation | Forged or replayed events, and no path to rotate a leaked secret |
| **Retries.** Schedule, give-up point, what a non-2xx means | Receivers are hammered, or events silently lost |
| **Payload.** Thin (id, then fetch) or full snapshot; version field | Every payload change is breaking, or receivers act on stale snapshots |
| **Event names.** Past tense, namespaced (`order.shipped`) | Names that describe commands rather than facts |

## SDKs, libraries, CLIs, files

| Kind | Decisions |
| --- | --- |
| SDK or library | Semver policy, exported names, error types, default values, supported runtimes |
| CLI | Output stability, `--json`, exit codes, stderr versus stdout |
| File formats | Header row, encoding, delimiter, date and number format, versioning |

## The authorization boundary

State the rule the contract implies (*a key sees its own account's invoices
only; another account's id returns 404, the same as a missing one*) and hand
the enforcement depth to Standards Compass. Returning 403 for another tenant's
id tells a caller which ids exist, and that is a decision too.
