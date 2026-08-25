# Response Compression

The developer's attention is the scarce resource. Every sentence in the final
message competes with the work they were doing before they asked.

Optimize for **decision density**, not explanation length.

## What the final message must answer

1. Is it done?
2. Is it proven?
3. What failed?
4. What do I need to decide?

Anything that does not answer one of those is optional, and optional means
"available if asked", not "included by default".

## The three shapes

```
✓ VERIFIED

Password reset

Requirements   8/8
Tests          47/47
Regression     pass
Changed        6 files
```

```
⚠ REVIEW REQUIRED

Bulk upload · 13/14 requirements verified

Decision required:
A duplicate filename inside one upload batch —

  [overwrite]   [reject the duplicate]   [keep both, suffix the name]
```

```
✗ BLOCKED

Checkout · 11/12 requirements verified

CHECKOUT-009  Session expires on wall-clock time, not idle time — an active
              user is signed out mid-checkout.
Cause         expiry derives from session.createdAt; no activity timestamp
              exists on the session record.
Attempts      3 (refresh-on-request, sliding expiry, lastSeenAt column)
Blocker       lastSeenAt changes a schema shared with the mobile token contract.

Decision required: extend the session record, or scope expiry to web only?
```

The BLOCKED shape is longer on purpose. A blocked run is exactly when the
developer needs detail — but it is detail about the *problem*, not about the
process.

## Not in the default response

- "First I… then I… I also…"
- A file-by-file tour of the diff.
- The reasoning behind each design decision.
- Test code, unless a test *is* the answer to a question.
- Anything already visible in the diff.
- Reassurance. "This should work well now" adds no information and costs trust.
- An offer to explain, in three sentences. One line, at most: `Ask for details,
  evidence, or the contract.`

## Numbers must be real

`47/47 tests` comes from the runner's output. If the count is not in front of
you, describe instead of counting: `existing auth suite passed`. A fabricated
count is worse than no count, because it is the part a developer trusts without
checking.

The same applies to `0 regressions` — only when regression checks actually ran,
and the line should say which ones if the scope was partial.

## Detail on demand

Answer these fully when asked, and only when asked:

| Request | Response |
| --- | --- |
| *Show the contract* | The full contract: objective, risk, requirements, assumptions |
| *Show evidence* | Every requirement with its command, expected, actual, level |
| *Why is this verified?* | Requirement-by-requirement mapping from claim to executed check |
| *Explain the proof for X* | That requirement's mechanism, what it demonstrates, what it does not |
| *Show what changed* | The diff summary, grouped by requirement rather than by directory |
| *Show failed attempts* | Each repair iteration: what failed, the classification, the fix, the result |
| *Show the tests* | The tests written or run, with what each one establishes |

The compressed answer and the detailed one describe the same run. Detail is
retrieved from the contract and evidence, never re-derived — if the detailed
answer contains anything the compressed one contradicts, the compression was
wrong.

## Compression is not omission

Three things are never compressed away:

- **A decision the developer must make.** Hiding it to keep the message tidy
  defeats the purpose.
- **A requirement that could not be verified.** `13/14` with no explanation of
  the fourteenth is a misleading message, not a concise one.
- **A change to the contract.** If a requirement was amended, one line says so.

The goal is not fewer words. It is a developer who has to know less, and still
knows everything that matters.
