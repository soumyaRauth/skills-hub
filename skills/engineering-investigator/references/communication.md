# Communication

The investigation is for you. The answer is for them. A reader who has to
reconstruct the case from a transcript received a worse product than one who got
four lines and a confidence level.

## Default shape

```markdown
## Result

[One-sentence conclusion — what is actually happening.]

**Cause:** [short cause]
**Confidence:** [High / Medium / Low]

**Why:** [one or two sentences: the evidence that decided it]

**Action:** [what should happen next, and who does it]

### Client response

[Two or three plain sentences, sendable as written.]
```

Adapt it. Drop the client response when no non-technical audience is waiting.
Add a `Residual uncertainty` line when something real remains open. Never
include a section with nothing in it, and never pad `Why` to look thorough — the
strongest `Why` is usually one contrast and one measurement.

## When there is no conclusion

```markdown
## Result

We cannot reliably determine the cause yet.

**What we know:** [established facts, including what has been eliminated]

**What is missing:** [the specific evidence, and why it is out of reach]

**Next step:** [the smallest thing that would settle it — at most three items]
```

This is a legitimate outcome, and it is far better than a plausible cause with
nothing behind it. What makes it useful is specificity: "no production telemetry
is reachable from this environment" and "one affected request id with a
timestamp" beat "more information is needed".

## When it is not the application

Two sentences that mean different things, and the evidence decides which one you
have earned:

> Our application servers responded normally throughout the window, while the
> affected connection transferred data far more slowly than the others we
> measured. On the available evidence, the connection is the most likely cause.

versus:

> We have found no evidence of an application-side problem, but we do not yet
> have enough information to say whether the user's connection is responsible.

The first requires: our side healthy in the same window, an unaffected
comparison, and a measurement of the external factor. Without all three, write
the second. See `system-boundaries.md`.

Never write "it's your internet", "works on our end", "must be a browser issue",
or "the vendor is broken" without the measurement in hand. Blame with no
evidence is the fastest way to lose a customer's trust and to be wrong in
writing.

## Writing the client response

The client version is not the technical version with the words swapped. It
answers three things: what is happening, whether it is being handled, and what
they should do.

| Technical | Client |
| --- | --- |
| Client download throughput is 0.8 Mbps | The affected connection is transferring data much more slowly than normal |
| N+1 query regression in the cart serializer | A recent update made the checkout page do far more database work than it should |
| Elevated 5xx from the payment provider | Our payment provider is returning errors |
| p95 latency rose from 310 ms to 2.1 s | Checkout is taking around two seconds instead of a third of a second |
| Cache invalidation on deploy | The system had to rebuild its temporary data after an update |
| Connection pool exhaustion under load | The service ran out of available connections when many people used it at once |
| The failures correlate with provider error code 503 | The failures line up exactly with errors coming back from that provider |

Rules for the client paragraph:

- No `HTTP`, `latency`, `throughput`, `Redis`, `pool`, `N+1`, `CPU`, `p95`, or
  service names they do not use.
- Honest about fault. If it was our regression, say we introduced it in an
  update. Vague passive voice reads as evasion.
- No timelines you cannot keep and no promises about a fix that does not exist.
- No internal detail — no file names, commit hashes, vendor contract terms, or
  another customer's data.
- Say what they should do, or that nothing is needed from them.

Three sentences is usually right. If it runs longer than five, it is a status
update, not an answer.

## What never appears in the response

- The hypothesis ledger, unless asked
- Every command run, or a file-by-file tour
- Raw log excerpts beyond the one or two lines that decided it
- Internal reasoning, deliberation, or the order you thought of things
- Hedging stacked on hedging: "it might possibly be related to what could be…"
- A confidence level that contradicts the words around it — "definitely the
  database (Confidence: Low)" is two different answers

## Confidence, in words

| Level | Says |
| --- | --- |
| **High** | Reproduced, or multiple independent lines of direct evidence agree and the alternatives are eliminated |
| **Medium** | Direct evidence points here; a plausible alternative remains untested |
| **Low** | Consistent with the evidence, nothing excludes the alternatives — treat as a lead |

Match the verb to the level. High: *is*. Medium: *is most likely*. Low: *is
consistent with, and worth testing next*. Do not soften High into mush, and do
not let Low be written as fact — the level and the sentence must agree.

## Depth on demand

The compression is only acceptable because the detail is one question away. Be
ready for, and answer directly:

```
show the evidence          show the hypotheses        what did you rule out?
how do you know?           what would change this?    show the experiments
what did you not check?    is it safe to deploy?      what if you're wrong?
```

"What did you not check?" deserves a real answer: the layers excluded, the
hypotheses left `Blocked`, and the evidence that was out of reach. An
investigator who cannot say what they did not look at has not been keeping the
ledger.
