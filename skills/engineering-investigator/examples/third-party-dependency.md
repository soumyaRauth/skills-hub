# Example — When the failure belongs to a vendor

"Payments are randomly failing" is a report about our system. The evidence may
not be.

---

**Report:**

> Payments are failing randomly. Some go through, some don't. Started this
> morning I think.

---

## Phase 0 — Access

```
Available      repository, git history, application error log with request ids
               (logs/app-2026-08-27.log), the payment provider's status page
Not available  provider dashboard, production database, APM
```

Lane: **INCIDENT** — money path, intermittent, an external party involved.

## Phase 1 — Normalize

```
Symptom     A fraction of payment attempts fail          FACT (report)
Who         Unknown — not yet scoped                     UNKNOWN
What        Payment authorization; which step unknown    PARTIAL
Since       "this morning"                               UNKNOWN (imprecise)
Frequency   "random"                                     UNKNOWN — needs a rate
Impact      Failed orders                                INFERENCE
```

"Random" is the word that most often hides a pattern. Getting a rate and a shape
is the first job.

## Phase 2 — Scope and shape

```
E1  FACT  Payment attempts 08-27: 2,140 total, 187 failed (8.7%)
          Hourly failure rate: 00–06 → 0.2% · 07:00 → 0.4% · 08:00 → 9.1% ·
          09:00 → 11.2% · 10:00 → 8.4%
          source: logs/app-2026-08-27.log, counted by result field
E2  FACT  Failures span 141 distinct customers, 3 regions, all card brands
          present in the sample, amounts from $12 to $980
E3  FACT  Failed and successful attempts interleave for the same customer —
          17 customers have both within 10 minutes
```

Not random: a step change at 08:00, ~9% since, spread across every axis we can
group by. E3 is decisive for scoping — the same customer, same card, succeeding
and failing minutes apart, rules out anything deterministic about the input.

## Phase 3 — Hypotheses

```
H1  Provider-side errors
    Kill: our failures carry no provider error, or the provider's responses are
          normal in the window
H2  Our recent change broke a fraction of payment paths
    Kill: nothing shipped in the window, or the failures do not follow the
          changed code path
H3  Timeouts from our own resource exhaustion (pool, workers, CPU)
    Kill: failures are provider-attributed, or other endpoints are unaffected
H4  Retry or idempotency handling turning transient errors into failures
    Kill: no retry path exists, or failures happen on first attempt
H5  Expired or rotated credentials
    Kill: failures would be total, not fractional — and would carry an auth error
```

H5's kill condition is satisfied by E1 alone (8.7%, not 100%), so it is
`Disproven` immediately and recorded as such.

## Phase 4 — The discriminating experiment

```
Experiment 1 — what does the failure actually contain?

Method     Extract the last 50 failure records with their provider response
           fields; compare against 50 successes in the same window.
Predicts   H1 → failures carry provider error codes and provider request ids
           H2 → failures cluster in one code path, absent from successes
           H3 → failures are our own timeouts, with no provider response
           H4 → failures appear only after a retry

Observed   E4  FACT  173 of 187 failures carry provider_status=503 and a
                     provider request id · error "service temporarily unavailable"
           E5  FACT  The remaining 14 are our own 30 s client timeout, no
                     provider response body
           E6  FACT  Median time-to-error on the 503s: 340 ms — the provider is
                     answering quickly, with an error
Eliminates H3 disproven (we received provider responses; other endpoints normal,
           E7). H2 weakened sharply — a code bug does not produce the vendor's
           own 503 with the vendor's request id.
```

```
E7  FACT  No deploy since 08-24; git log shows nothing touching payments in
          14 days
E8  FACT  Provider status page, checked 10:40: "Elevated error rates —
          investigating", posted 08:05
```

E7 disproves H2. E8 corroborates H1 — and is treated as corroboration, not
proof: a status page is the vendor's own claim, and our 503s with their request
ids are the stronger evidence.

## Phase 5 — Attack the survivor

The comfortable conclusion is "it's the vendor". Look for what would break it:

- *Are we sending something wrong that provokes a 503?* Failed and successful
  requests for the same customer are byte-identical apart from ids and amount.
  A malformed request would not succeed on retry with the same shape. (E3, E9)
- *Are the 14 timeouts ours?* Possibly — they carry no provider response. They
  stay as a separate, unresolved item rather than being folded into the vendor's
  column. (E5)
- *Is our retry policy making it worse?* One attempt, no retry on 503, and the
  customer sees a hard failure. That is our contribution: a transient vendor
  error is being turned into a lost order. (E10)

E10 is why the answer is not simply "not our problem". The vendor's error is the
cause; our handling of it is why the customer feels it.

## Phase 6 — Cause

```
Cause       Provider-side 503 responses on payment authorization (~9% of
            attempts since 08:00)
Confidence  HIGHLY LIKELY

Chain       failures carry the provider's own error code and request id (E4)
            → no change on our side in 14 days (E7)
            → same customer succeeds and fails minutes apart (E3)
            → our other endpoints are healthy in the same window (E7)
            → the provider reports elevated errors from 08:05 (E8)

Contributing: no retry on transient provider errors (E10) — ours to fix
Unresolved:   14 client-side timeouts with no provider response (E5)
```

Not `CONFIRMED`: confirming would mean reproducing against the provider or
seeing their internal telemetry. Neither is available, and the level says so.

## The answer

```markdown
## Result

The payment failures are coming from the external payment provider, not from our
application.

**Cause:** Provider returning 503 "service temporarily unavailable" on about 9%
of authorization attempts since 08:00
**Confidence:** High

**Why:** 173 of 187 failures carry the provider's own error code and request id,
nothing has shipped on our side in 14 days, the same customer succeeds and fails
minutes apart, and the provider's status page reports elevated errors from 08:05.

**Action:** Two things, in order. Now: our payment client does not retry
transient provider errors, so a recoverable 503 becomes a lost order — adding a
bounded retry with the existing idempotency key would recover most of these.
Also: 14 failures were our own 30 s timeouts with no provider response; those
have not been explained yet and are worth a separate look once the provider
recovers.

### Client response

"We've identified the cause of the payment failures: the payment service we use
is currently returning errors on a portion of transactions, and it began at
around 8am. Our own systems are running normally, and payments that go through
are being processed correctly. We're monitoring the provider's recovery, and
we're adding an automatic retry so that temporary errors like this one don't
result in a failed order for the customer."
```

## What this example demonstrates

- "Random" was replaced with a rate and a shape before any theorizing.
- The vendor's error code and request id — attribution at the boundary — did the
  eliminating, not the status page.
- The status page corroborated; it was not treated as proof.
- Our own contribution (no retry) is reported rather than buried under
  "third-party issue", and the 14 unexplained timeouts stay unexplained instead
  of being absorbed into the tidy answer.
- The client response says what we are doing, not just whose fault it is.
