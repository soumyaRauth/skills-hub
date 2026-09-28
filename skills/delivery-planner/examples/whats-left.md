# Example — "what's left?"

Illustrative. The project is invented.

## Request

> What's left before we can launch?

`.delivery/` exists, tracker Linear via the official MCP server.

## What it did

1. Pulled first: read every ticket's state from Linear and compared with the
   `synced` blocks. One change: T-012 had been moved to *In Progress* by a
   teammate. The file was updated.
2. Counted from the files, per milestone in `plan.md`. *Launch* is M3 in
   `plan.md`, so "before launch" means M1–M3.

## Response

```
⚡ Delivery Planner — what's left, from .delivery/ and Linear (pulled just now)

M1  Walking skeleton deployed   3/3 done
M2  Customers book and cancel   5/5 done
M3  Owner sees the week         2/4 done · T-012 in progress (Sam) · T-013 blocked on D2
NEXT      T-014 (ready; depends on T-012)
DECISION  D2: what happens to future bookings after a no-show? Blocks T-013.
```

## What it did not say

- No estimate of when launch will happen. Nobody supplied durations, and ticket
  counts are not days.
- No new tickets for things that "should probably" happen before launch. If the
  planner thinks something is missing (there is no ticket for backups, say),
  that is one line offering it, not a ticket created.
- Nothing about tickets in M4, which the question did not reach.
