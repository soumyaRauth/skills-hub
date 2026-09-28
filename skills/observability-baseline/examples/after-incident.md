# Example — quiet during an incident, then the missing signal

Illustrative.

## During

> Orders stopped going through about an hour ago. Customers are emailing. What's going on?

This is a live problem being diagnosed. Observability Baseline adds nothing:
no block, no "you should have had monitoring", no ⚡ mention. Engineering
Investigator owns the reply. It establishes that the payment provider's webhook
secret was rotated, every webhook has returned 401 since, and the only record
was a line `error Unauthorized` with no request id.

## After

> OK it's fixed. How do we not find out from customers next time?

The incident is over and the user asks. The investigation in
`.agent-investigation/` records who noticed first: customers.

```
⚡ Observability Baseline — incident found by customers first

OBSERVABILITY  shop — after incident 2026-09-27 (webhook 401s)
ERRORS         IN PLACE    tracker receives unhandled errors; this 401 was handled and never reported
ALERT          IN PLACE    uptime alert only; the app was up the whole time
NEXT           One signal: report a rejected webhook to the tracker with request_id, and alert on it
```

The work, with a yes:

1. The webhook handler's signature-failure branch reports to the error tracker
   with the provider event id and `request_id`, never the payload or the secret.
2. An alert in the tracker on that error type, to the same channel as the uptime
   alert, threshold above a single stray request.
3. Proof on staging: a webhook sent with a wrong signature shows up in the
   tracker, and the alert arrives (SUPPLIED by the developer).
4. `.observability/baseline.md` history: *2026-09-28 · Errors/Alert · added
   webhook-rejection alert after incident 2026-09-27*.

## What it did not do

- Speak during the incident.
- Re-diagnose the cause. Engineering Investigator established it.
- Turn one missed signal into a monitoring overhaul.
