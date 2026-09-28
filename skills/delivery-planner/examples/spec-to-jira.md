# Example — a spec planned into milestones and synced to Jira Cloud

Illustrative. The repository is `tests/fixtures/delivery-planner/spec-no-tickets`
(a salon booking app); the Jira site, keys and ids are invented.

## Request

> Plan the build from the spec and put the tickets in Jira.

No `.delivery/` yet. `docs/spec.md` exists; `src/` has a health route and the
service list.

## 1. Guided setup, short because most of it was already there

Found: no tracker MCP tools in this session, no `.mcp.json`, `acli` not on the
path, `JIRA_EMAIL` and `JIRA_API_TOKEN` already exported in the shell (checked
for presence only). The guided flow (`SKILL.md`, *First run*) still runs, one
question at a time, but step 2 collapses to option c:

```
⚡ Delivery Planner — spec to milestones and Jira tickets

Tickets go to Jira. I see JIRA_EMAIL and JIRA_API_TOKEN in your shell — use them?
(Or: a) Atlassian's official MCP server with browser sign-in.) And your site URL?
```

> Use them. https://salon.atlassian.net

`tracker.py --tracker jira --url https://salon.atlassian.net whoami` →
`{"ok": true, "user": "Dana Reyes", …}`. Then `boards`:

```
Your Jira projects: 1 SAL Salon · 2 OPS Operations
Pick one, or: n) create a new project (needs a Jira admin)
```

> 1

`columns SAL` returns *To Do*, *In Progress*, *In Review*, *Done*. No *Blocked*,
no *Backlog*, and Jira statuses are workflow settings the helper will not
create:

```
Proposed mapping for SAL:
  backlog→To Do · ready→To Do · in_progress→In Progress · in_review→In Review · done→Done
  blocked → no status: label "blocked" + comment · dropped → Done + label "dropped"
OK? (A Jira admin can add a Blocked status later; I'll pick it up.)
```

> ok, and defaults for autonomy

`.delivery/config.yml` written with `type: jira`, `flavor: cloud`, `via: rest`,
`project: SAL`, `url`, `auth_env: [JIRA_EMAIL, JIRA_API_TOKEN]` and no
`auth_file` (the shell holds them). Proof:

```
CONNECTED  jira via rest as Dana Reyes · board SAL (Salon) · 5 of 7 statuses mapped
```

## 2. Plan

Read `docs/spec.md` and `src/`. `/health` and `/services` exist, so the
skeleton builds on them rather than re-planning them.

```
PLAN     docs/spec.md → 3 milestones · 10 tickets · 2 open decisions
M1       Walking skeleton deployed        T-001 T-002
M2       Customers book and cancel        T-003 T-004 T-005 T-006
M3       Owner runs the week              T-007 T-008 T-009 T-010
BLOCKED  T-006 on D1: can a customer cancel on the day of the appointment?
         T-010 on D2: what happens to future bookings after a no-show?
```

Two of the tickets, as written to `.delivery/tickets/`:

```markdown
---
id: T-001
title: Visitor sees today's free slots on the live site
milestone: M1
status: ready
depends_on: []
tracker_ref:
labels: [skeleton]
---
## Why
Proves the stack end to end, SQLite to the VPS, before any feature depends on it.

## Acceptance criteria
1. GET / on the staging URL returns a page listing Tuesday–Saturday 09:00–18:00 in 30-minute slots for today.
2. The slots are read from the SQLite database, not hard-coded (a slot removed from the table disappears from the page).
3. On a Sunday or Monday the page says the salon is closed and lists no slots.
4. The deploy is repeatable from a clean checkout with one documented command.
```

```markdown
---
id: T-004
title: Two customers cannot book the same slot
milestone: M2
status: ready
depends_on: [T-003]
tracker_ref:
labels: [booking]
---
## Why
The spec's reason for the whole app: phone bookings double-book.

## Acceptance criteria
1. Two booking requests for the same free slot submitted concurrently: exactly one succeeds.
2. The other gets "that slot has just gone" and no booking row, no email.
3. A colour (two slots) cannot be booked if its second slot is taken.
4. A slot freed by a cancellation can be booked again.
```

## 3. Sync

`create_tickets: auto` and the human asked, so the tickets go to Jira. For
each, in plan order:

1. **Find first.** `GET /rest/api/3/search/jql?jql=project=SAL AND labels="T-001"&fields=summary,status,labels,updated`.
   Empty. (The label, not `summary ~ "[T-001]"`: Jira does not index brackets
   or hyphens.)
2. **Create.** `POST /rest/api/3/issue` with `summary: "[T-001] Visitor sees
   today's free slots on the live site"`, `labels: ["T-001","skeleton"]`,
   `issuetype: Task`, and the description as ADF (v3 rejects a plain string).
3. **Read back** `GET /rest/api/3/issue/SAL-1`: summary and label present.
   `tracker_ref: SAL-1`, `synced` filled.
4. T-006 and T-010 are `blocked`: created, then labelled `blocked` and
   `decision-needed` with a comment carrying the question (ADF).

The first create for T-007 timed out. Before retrying, the search ran again and
found `SAL-7` with label `T-007`: the create had landed. It was linked, not
created twice.

```
TRACKER  jira · via rest · salon.atlassian.net · SAL
CREATED  10 (SAL-1 … SAL-10) · already there: 0 · 1 create timed out and was found on re-search (T-007 → SAL-7)
PENDING  none

Two decisions block two tickets; the rest of the plan can proceed:
D1  Can a customer cancel on the day of the appointment?          (T-006)
D2  What happens to a customer's future bookings after a no-show? (T-010)
```

## What it did not do

- Did not create a *Blocked* status or edit the Jira workflow: that is the
  project admin's, and nobody asked.
- Did not guess a cancellation window for T-006.
- Did not write the API token, its base64 form, or a `curl -v` trace anywhere.
- Did not start building T-001. Planning was the request.
