# Compatibility

Every change to an existing contract gets one of three labels. The label is
about consumers, not about the diff: a one-character change can be breaking,
and a new endpoint is not.

## The three labels

| Label | Examples | Consumer impact |
| --- | --- | --- |
| **ADDITIVE** | New endpoint; new optional request field; new response field; new enum value *on an enum documented as open*; new event type | None, for consumers that ignore what they do not know |
| **BEHAVIORAL** | Same field, different meaning; a default that changed; sorting that changed; a status that now fires at a different point; a rounding rule | Consumers see valid data and act on it wrongly. **Treat it as breaking** |
| **BREAKING** | Field removed, renamed or retyped; newly required input; tighter validation; changed status code; changed pagination or ordering; a narrower auth scope; a new value on an enum that was never documented as open | Consumers fail, loudly or silently |

Tightening validation is the one most often mislabeled. It feels like a fix,
and it rejects requests that succeeded yesterday.

## Migration paths

Pick the one that fits, and write it down. Never assume consumers will adapt.

| Path | Fits | Cost |
| --- | --- | --- |
| **Add alongside, deprecate, remove** | Renames and retypes | Both fields maintained until the sunset date |
| **Versioned route or header** | Many changes at once; a public API with a version scheme already | A second surface to run and test |
| **Dual-emit** | Events and webhooks | Receivers must dedupe; emit both until consumers confirm |
| **Consumer-by-consumer** | A known, small set of internal consumers deploying separately | Coordination; the old shape stays until the last one moves |
| **Don't** | When the break buys little | Often the right answer |

## Telling consumers

A migration path nobody hears about is a breaking change on a delay. Where the
project has these, use them: a changelog addressed to integrators, `Deprecation`
and `Sunset` response headers, a version bump in a published SDK, a note in the
webhook payload's version field.

## Evidence for the label

The label rests on how consumers use the interface, which is often not visible
from the repository. When the only consumers are outside it, state the label
for the documented contract, and name what is unknown:

```
CHANGE      BREAKING for the documented contract (docs/api/orders.md:14 lists
            `state` as a response field) · consumers outside this repository
            unknown — no inventory exists here
```
