# Example — Incremental run, prompted by the hook

Claude finishes a reply, and the Stop hook blocks the stop once:

> Project knowledge is 7 commits behind HEAD. Run the project-knowledge skill
> now (incremental from .agents/knowledge/.learn-state.json), then give the user
> its few-line report.

## Step 1 and 2 — cheapest first

`git log` over the seven commits:

```
c3e1f0a fix(worker): retry a charge once on a provider timeout
9b2d7e4 feat(dev-setup): one-command local stack
8a01c55 chore: bump eslint
...
```

`git diff --stat` shows a new top-level `dev-setup/` directory and a changed
`package.json`. Those two paths get a full diff. The worker fix, the lint bump and
the test changes do not: the commit messages say enough.

## Step 3 and 4

- `architecture.md`, section *Run it*: replaced, to start from
  `./dev-setup/setup.sh` and `./dev-setup/start.sh`.
- `gotchas.md`, appended:

  ```markdown
  ## start.sh must be stopped with Ctrl-C, not by closing the terminal
  The trap that stops every server runs on SIGINT; a closed terminal leaves
  the database port bound.
  ```

- `decisions.md`: nothing. A setup script is not a decision anyone would
  revisit.

## The report

```
Incremental, 4b1e2d9..c3e1f0a (7 commits). Updated architecture.md (Run it);
1 new gotcha (start.sh and Ctrl-C). Cursor moved to c3e1f0a.
```

## What this example demonstrates

Seven commits cost two targeted diffs. The run updated one section in place
instead of rewriting the document, and a change with no decision in it produced
no decision entry.
