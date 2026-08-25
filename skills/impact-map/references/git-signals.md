# Git Signals

History is the only source of coupling evidence that does not live in the code:
which files real engineers keep changing together, which parts of the system
churn, and who to ask. It is read-only — `git log`, `git blame`, `git diff`,
`git show` — and stays inside the skill's read-only rule.

Treat every signal here as **indirect evidence**. History shows correlation, and
correlation earns NEEDS VERIFICATION or HIDDEN COUPLING, never MUST CHANGE on
its own.

## Check availability first

```bash
git rev-parse --is-inside-work-tree     # is there history at all
git rev-parse --is-shallow-repository   # true → counts are meaningless
git log --oneline -n 1                  # is there more than one commit
```

History is unusable or misleading when:

- the repository is a shallow or single-commit clone (CI checkouts usually are);
- the project squash-merges, so one commit represents a whole branch and
  co-change counts inflate;
- the code was imported from another repository, so everything shares one
  founding commit;
- the path was renamed and the search does not use `--follow`.

Say which of these applies rather than reporting a number the reader will
over-trust. No history is a stated gap, not a silent one.

## Change source: analyzing work that already exists

The request is not always prose. When the user points at a diff — uncommitted
work, a branch, a PR, a commit range — derive the change statement from it
instead of asking them to describe it.

```bash
git status --short                       # uncommitted
git diff --stat                          # unstaged shape
git diff --cached --stat                 # staged shape
git diff --stat main...HEAD              # branch vs merge base
git diff --name-only main...HEAD         # the changed set
git log --oneline main..HEAD             # what the branch claims to do
git show --stat <sha>                    # one commit
```

Then invert the usual question. Instead of *what will this change touch*, ask
**what does this change already touch that it has not accounted for**:

1. Read the diff and write the change statement from what the code now does —
   not from the branch name or the commit message.
2. Treat every symbol, column, route, string literal, and enum value the diff
   introduces or modifies as a primary concept for Phase 3.
3. Run the normal analysis on those concepts.
4. Subtract the files already in the diff. **What remains is the finding**: the
   surface the change touches but has not visited.

Report that remainder plainly — "changed: 6 files; unvisited surface: 4 files" —
and keep the already-changed files out of MUST CHANGE unless they are wrong, not
merely present.

## Co-change coupling (temporal coupling)

Files that keep being committed together are coupled, whether or not any import
says so. This finds the fixture, the doc, the config key, and the sibling
service that a static search will never connect.

```bash
# every commit that touched the file, then every file in those commits
git log --format=%H -- path/to/file \
  | xargs -n1 git show --pretty=format: --name-only \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -20
```

Read the result as a ratio, not a count: a file appearing in 9 of the target's
12 commits is a strong signal; 2 of 40 is noise. Discard lockfiles, changelogs,
formatting sweeps, and generated output — they co-change with everything.

For a renamed file, collect the hashes with `--follow`:

```bash
git log --follow --format=%H -- path/to/file
```

A strong co-change partner that the dependency analysis never found is one of
the highest-value findings in the report:

```
⚠️ HIDDEN COUPLING
  Coupling type:  Temporal (co-change)
  Evidence:       Changed in 9 of the 12 commits that touched
                  EnrollmentStatus, with no import or reference between them.
  Confidence:     Medium
  Action:         Read it before implementing; history says the two move
                  together for a reason this analysis has not yet found.
```

Never assert *why* two files co-change. Report the pattern and hand the reader
the check.

## Churn and hotspots

```bash
git log --since='12 months ago' --format=%H -- path/to/dir \
  | xargs -n1 git show --pretty=format: --name-only \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -20
```

High churn inside the change surface means the area is unsettled: more likely to
have half-finished migrations, duplicated logic, and stale tests. Low churn plus
old last-touch dates means the opposite risk — nobody currently understands it.

Both feed `RISK`; neither is a finding by itself.

## Ownership

Ownership answers "who reviews this and who do I ask", not "who is to blame".

```bash
cat CODEOWNERS .github/CODEOWNERS docs/CODEOWNERS 2>/dev/null
git shortlog -sn --no-merges HEAD -- path/to/file    # contributor counts
git log -1 --format='%ad %an' --date=short -- path/to/file   # last touch
git blame -L 40,60 --date=short -- path/to/file      # who wrote these lines
```

Rules:

- `CODEOWNERS` is authoritative when it exists; commit counts are a fallback.
- Report ownership as a **routing hint**: which team or reviewer the change
  needs, and which findings sit outside the requester's usual area.
- One contributor with every commit and no recent activity is a bus-factor note
  worth stating once, under `OPEN QUESTIONS`.
- Never characterize a person's work quality, and never use `git blame` output
  to attribute a defect. Names appear only to route the change.

## What history is worth in the report

| Signal | Where it lands |
| --- | --- |
| Strong co-change with no code reference | ⚠️ HIDDEN COUPLING, Medium confidence |
| Weak or noisy co-change | Not reported |
| Churn in the change surface | A factor in `RISK`, with the observation named |
| Last touched years ago | `RISK` and, if it matters, `OPEN QUESTIONS` |
| CODEOWNERS entries for affected paths | `HISTORY & OWNERSHIP`, as routing |
| Files already changed by the current diff | `REPOSITORY SCOPE`, and excluded from the unvisited surface |

Counts come from a command that actually ran. If the command was not run, the
signal is not in the report.
