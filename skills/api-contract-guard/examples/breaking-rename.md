# Example — a rename another service consumes

Illustrative.

## Request

> Rename `trackingNo` to `trackingNumber` in the order.shipped event — it's been
> bugging me.

## What was read

- `services/orders/src/events.js:18` publishes `order.shipped` to the `orders`
  topic, with `trackingNo`.
- `services/fulfillment/src/consumers/shipped.js:9` reads `event.trackingNo`.
- The two services each have their own `package.json` and `Dockerfile`, and
  `.github/workflows/` deploys them in separate jobs. They ship independently.
- No schema registry, and no version field on the event.

## Response

```
⚡ API Contract Guard · Impact Map — event field rename, separately deployed consumer

CHANGE    BREAKING — fulfillment reads event.trackingNo
          (services/fulfillment/src/consumers/shipped.js:9); the services deploy
          in separate jobs, so for some window the new producer meets the old
          consumer
PATH      dual-emit: publish both trackingNo and trackingNumber → move the
          consumer to trackingNumber, falling back to trackingNo → remove
          trackingNo after fulfillment has deployed
DECIDES   add "version": 1 to the payload in the same change, so the next change
          has somewhere to go
HANDOFF → impact-map: consumers of the orders topic outside services/ — none
          found in this repository; the topic is not documented as private
```

Step one, the dual-emit, is implemented now. The consumer change and the removal
are separate steps, listed with the order to deploy them in.

## Notes

- **The label is about the consumer, not the diff.** A rename is a one-word
  change, and here it breaks the fulfillment service during the deploy window.
- **The migration path is the smallest one that keeps both sides working at
  every step.**
- **Consumers outside the repository are an open question.** None is claimed,
  and none is ruled out.
