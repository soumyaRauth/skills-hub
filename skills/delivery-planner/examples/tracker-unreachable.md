# Example — the tracker is unreachable; local continues and reconciles

Illustrative. The project and ids are invented.

## The project

GitLab, self-hosted, `via: cli (glab)`, `project: shop/storefront`.
`status_map` uses scoped labels (a GitLab Premium feature this instance has):
`status::ready`, `status::in-progress`, `status::in-review`, `status::blocked`,
and closing the issue for `done`.

## 1. The tracker goes down mid-session

`delivery-lead` picks T-009. The planner reads the local file, then tries to
read issue #57:

```
$ glab issue view 57
error connecting to gitlab.example.com: dial tcp: i/o timeout
```

One retry after a short pause: the same timeout. The planner stops trying and
carries on locally:

- `.delivery/tickets/T-009.md` → `status: in_progress`. The `synced` block is left
  as it was (`status: ready`), so the difference stays visible.
- The reply says it plainly:

```
tracker: out of sync — gitlab.example.com timed out (glab); T-009 is in_progress locally only
```

`delivery-lead` writes the same line into its run ledger. The planner does not
write `runs/`.

Work continues. Proof comes back `✓ VERIFIED`, a PR is opened (GitLab is still
down, so the push of the branch fails too, and the lead reports that itself).
Locally T-009 becomes `in_review`, still `PENDING`.

## 2. What it does not say

Not *"moved T-009 to In Progress"*. Not *"the board is updated"*. Not a guess of
what the board shows. The only tracker facts reported are the ones read.

## 3. The next run reconciles

The next morning, GitLab answers. Before anything else, the planner reconciles
every ticket file against the tracker:

| Ticket | Local | `synced` | GitLab | Action |
| --- | --- | --- | --- | --- |
| T-009 | `in_review` | `ready` | `status::ready` | push: label to `status::in-review`, comment with the PR |
| T-010 | `ready` | `ready` | `status::blocked` + a comment by a teammate | pull: a human blocked it overnight |
| T-011 | `ready` | `ready` | `status::ready` | nothing |

Pushing T-009 means one comment covering the whole gap, not a replay of every
move: `[delivery-planner] T-009 → In Review · was in progress while the tracker
was unreachable · MR !14`. The move itself is made with `glab issue update 57
--label status::in-review --unlabel status::ready` and then read back.

```
TRACKER  gitlab · via cli (glab) · shop/storefront
PUSHED   T-009 ready → in_review (MR !14; missed while the tracker was down)
PULLED   T-010 ready → blocked (a teammate blocked it at 07:40; local updated)
CREATED  none · already there: 11
PENDING  none
```

`PENDING none` is printed only because every push was read back.
