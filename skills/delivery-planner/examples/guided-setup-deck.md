# Example — first run, guided end to end (Nextcloud Deck)

Illustrative. The repository is `tests/fixtures/delivery-planner/spec-no-tickets`;
the Nextcloud server, user and ids are invented. The shape of the conversation
is the point: one question at a time, an action after each answer, no token in
the chat, nothing created before `CONNECTED`.

## Request

> Break the spec into tickets. We use Nextcloud Deck.

No `.delivery/`. The planner reads `docs/spec.md` and drafts the plan locally
first (planning does not wait on the tracker), then sets up the tracker.

## Step 1 · Which tracker

Detected, nothing printed: no tracker MCP tools, no `.mcp.json`, no `gh` or
`glab` login relevant here, `NEXTCLOUD_*` not set, no `.delivery/.env`. The
human already named Deck, so the question is only the server:

```
⚡ Delivery Planner — spec to tickets on Nextcloud Deck

Tickets will live on Nextcloud Deck. What's your Nextcloud address?
(e.g. https://cloud.example.org)
```

> https://cloud.salon-mira.example

## Step 2 · Connect

Deck has no official MCP server this server runs, so the helper is the
default:

```
Run this in your own terminal (not here), from the repository root:
  python3 <skills>/delivery-planner/scripts/tracker.py secret deck
It shows where to create an app password and asks for it with hidden input.
Reply "done" when it prints "ok": true.
```

What the human sees in their terminal (the password is never echoed):

```
Create the credential here:  Nextcloud: Personal settings → Security → Devices & sessions → enter an app name → create new app password
Least access it needs:       an app password acts as you: you need edit rights on the board
Input for secrets is hidden. Values go to .delivery/.env (git-ignored, mode 600).
Nextcloud URL, e.g. https://cloud.example.org: https://cloud.salon-mira.example
Nextcloud username: mira
App password:
{"written": ["DELIVERY_TRACKER", "DELIVERY_URL", "NEXTCLOUD_APP_PASSWORD", "NEXTCLOUD_USER"], "file": ".delivery/.env", "mode": "600", "whoami": {"user": "Mira Okafor", "id": "mira"}, "ok": true}
```

Before the first prompt, the script had added `.delivery/.env` to `.gitignore`
and confirmed `git check-ignore -q .delivery/.env`. Had that failed, it would
have written nothing and said why.

> done

The agent runs `tracker.py whoami` itself: `{"ok": true, "tracker": "deck",
"user": "Mira Okafor", "id": "mira"}`.

## Step 3 · Which board

`tracker.py boards`:

```
Your Deck boards: 1 Personal (4) · 2 Salon admin (9)
Pick one, or: n) create a new board "salon-booking"
```

> n

`tracker.py create-board salon-booking` → `{"ok": true, "created": {"id": 17,
"name": "salon-booking"}}`.

## Step 4 · Columns

`tracker.py columns 17` returns no stacks: a new Deck board starts empty.

```
The board has no lists yet. Create these five, in order?
  To do · Doing · Review · Blocked · Done
  (backlog → To do, dropped → Done + archived)
```

> yes

Five `tracker.py create-column 17 <name>` calls, each returning the new stack id.

## Step 5 · Autonomy

```
What may I do without asking?  [defaults]
  create tickets [auto] · move tickets [auto] · open PR [auto]
  merge [ask] · deploy staging [auto] · deploy production [ask]
Reply "defaults" or change any of them.
```

> defaults

## Step 6 · Config, proof, and the tickets

`.delivery/config.yml` written (no secret in it):

```yaml
tracker:
  type: deck
  via: rest
  project: "17"
  url: https://cloud.salon-mira.example
  auth_env: [NEXTCLOUD_USER, NEXTCLOUD_APP_PASSWORD]
  auth_file: .delivery/.env
status_map:
  backlog: "To do"
  ready: "To do"
  in_progress: "Doing"
  in_review: "Review"
  blocked: "Blocked"
  done: "Done"
  dropped: "Done"
autonomy: {create_tickets: auto, move_tickets: auto, open_pr: auto, merge: ask, deploy_staging: auto, deploy_production: ask}
```

Proof, read-only: `whoami`, then `columns 17`.

```
CONNECTED  deck via rest as Mira Okafor · board salon-booking (17) · 7 of 7 statuses mapped
```

Only now are the tickets created, each one searched for first by its `[T-nnn]`
marker (`references/sync.md`), with curl loading the credentials inside the
command: `set -a; . .delivery/.env; set +a; curl -sS -u
"$NEXTCLOUD_USER:$NEXTCLOUD_APP_PASSWORD" -H 'OCS-APIRequest: true' …`.

```
TRACKER  deck · via rest · board salon-booking (17)
CREATED  10 · already there: 0
PENDING  none
BLOCKED  T-006 on D1: can a customer cancel on the day? · T-010 on D2: no-show consequences
```

From here the fixed moments (picked up, PR opened, verified and merged,
blocked) move cards on their own, within `autonomy`.

## If it had failed

Step 6 against a mistyped board id:

```
{"ok": false, "error": "not_found", "status": 404, "fix": "Wrong board, project, repo or site URL, or this account cannot see it. Check the identifier and the URL."}
```

```
Not connected: board 71 was not found for mira (404). Did you mean salon-booking (17)?
Nothing was created; the plan is in .delivery/ locally.
```

A `401` would have pointed back to step 2 (create a new app password and run
`secret deck` again); a `403` to the board's sharing settings.

## What it did not do

- Ask for the password in chat, print it, or read `.delivery/.env` aloud.
- Create the board or its lists before an explicit yes.
- Create a single card before `CONNECTED`.
