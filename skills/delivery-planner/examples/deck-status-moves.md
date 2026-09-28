# Example — automatic moves on a Nextcloud Deck board, and a human's move wins

Illustrative. The repository, board and ids are invented; the sequence is the
point.

## The project

`.delivery/config.yml`:

```yaml
tracker:
  type: deck
  via: rest
  project: "12"                         # Deck board id
  url: https://cloud.example.org
  auth_env: [NEXTCLOUD_USER, NEXTCLOUD_APP_PASSWORD]
status_map:
  backlog: "Backlog"
  ready: "To do"
  in_progress: "Doing"
  in_review: "Review"
  blocked: "Blocked"
  done: "Done"
  dropped: "Done"
autonomy:
  create_tickets: auto
  move_tickets: auto
  open_pr: auto
  merge: ask
  deploy_staging: auto
  deploy_production: ask
```

At setup, the board's stacks were read once (`GET
/index.php/apps/deck/api/v1.0/boards/12/stacks` with `OCS-APIRequest: true`),
and their ids are looked up by title on every move: a stack renamed on the board
is caught, not written into a stale id.

## 1. The developer starts a ticket

> Let's do T-004.

Nobody mentioned the board. `.delivery/` exists and a ticket was picked up, so
this is a fixed moment. The planner, passively:

1. Reads `.delivery/tickets/T-004.md`: `status: ready`, `tracker_ref: 311`,
   `synced.status: ready`.
2. Reads the card from the board's stacks: it is in stack *To do*. Tracker and
   `synced` agree, so nothing was changed by a human.
3. Moves the card: `PUT …/boards/12/stacks/7/cards/311/reorder` with
   `{"stackId": 8, "order": 0}` (stack 8 is *Doing*).
4. Comments through the OCS endpoint
   (`POST /ocs/v2.php/apps/deck/api/v1.0/cards/311/comments`):
   `[delivery-planner] T-004 → Doing · branch t-004-password-reset`.
5. Reads the stacks again: card 311 is in *Doing*. Updates the file:
   `status: in_progress`, `synced: {status: in_progress, …}`.

The reply to the developer carries one line, then the work:

```
Tracker: T-004 → Doing (deck · via rest)
```

## 2. The PR is opened

Proof-driven-dev reported `✓ VERIFIED · 4/4`, and a PR was opened
(`autonomy.open_pr: auto`). Same steps: read, the card is still in *Doing* as
`synced` says, move to *Review*, comment with the PR link, read back.

```
Tracker: T-004 → Review (PR #31)
```

## 3. Meanwhile, the owner moves a card

While T-004 was in review, the salon owner opened the board on her phone and
dragged **T-006** from *To do* to *Blocked*, with a comment: *"Wait, I need to
check the holiday dates with my landlord."*

The developer then says:

> T-004 is merged. Start T-006.

Two fixed moments. For T-004: merged and `VERIFIED` → *Done*, with the comment
`✓ VERIFIED · 4/4 · merged in 3f2a91c`. For T-006, *picked up* would mean
*Doing*. The planner reads the card first:

| | Local | `synced` | Board |
| --- | --- | --- | --- |
| T-006 status | `ready` | `ready` | *Blocked* |

The board changed and the file did not: a human moved it. The human wins. The
planner pulls the move into the file (`status: blocked`, the owner's comment
copied into *Notes / decisions*), updates `synced`, and does not move the card.

```
Tracker: T-004 → Done (✓ VERIFIED · merged 3f2a91c)
T-006 not started — the owner moved it to Blocked on the board at 13:52:
  "Wait, I need to check the holiday dates with my landlord."
Local file updated. Next ready ticket is T-008. Take that instead?
```

## What it did not do

- Did not move T-006 to *Doing* over the owner's decision, even though
  `move_tickets` is `auto`. Autonomy covers the fixed moments; it never covers
  overriding a person.
- Did not delete, recreate or re-rank anything on the board.
- Did not print or log the app password. Requests used basic auth built from
  `$NEXTCLOUD_USER` and `$NEXTCLOUD_APP_PASSWORD`.
- Did not report T-004 as *Done* before the read-back showed it there.
