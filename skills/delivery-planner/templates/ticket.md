---
id: T-004
title: Customer can reset password by email
milestone: M1
status: ready            # backlog | ready | in_progress | in_review | blocked | done | dropped
depends_on: [T-002]
tracker_ref:             # the tracker's own id or URL once synced; empty for tracker: local
labels: [auth]
synced:                  # planner-owned: what local and tracker last agreed on; empty until first sync
  at:
  status:
  title:
---
## Why

A customer who forgot their password can get back in without contacting the shop.

## Acceptance criteria

1. Requesting a reset for a registered email sends exactly one email with a single-use link.
2. Opening the link and entering a new password lets the customer sign in with it.
3. Requesting a reset for an unknown email shows the same confirmation and sends nothing.
4. A link that was already used, or is past the expiry, shows "link expired" and changes nothing.

## Notes / decisions

- Expiry length: decided in D2 (60 minutes, by the owner, 2026-09-28).
