# Branches, commits and pull requests

Plain git works in every agent. The forge CLIs are optional; when none is
available, push the branch and give the human the compare URL instead of
claiming a PR exists.

## Branch

```bash
git fetch origin
git switch <default-branch>
git merge --ff-only origin/<default-branch>     # fails rather than rewriting anything
git switch -c t/T-004-book-a-class
```

Read the default branch from the remote (`git symbolic-ref
refs/remotes/origin/HEAD`) rather than assuming `main`. With no remote, branch
from the local default branch and say that no PR can be opened.

## Commit

```
T-004: Book a class

Acceptance criteria 1–4 proven (ProofBuild VERIFIED).
Tracker: PROJ-17
```

The first line starts with the ticket id. Stage only the files the ticket
changed (`git add <paths>`), never `git add -A` on a tree with anything else in
it. Never `--no-verify`, never `--amend` a pushed commit.

## Pull request

GitHub (`gh`), flags checked against https://cli.github.com/manual/gh_pr_create
on 2026-09-28:

```bash
gh pr create --base <default-branch> --head t/T-004-book-a-class \
  --title "T-004: Book a class" --body-file <file with criteria + ProofBuild block>
```

GitLab (`glab`), flags checked against https://docs.gitlab.com/cli/mr/create/
on 2026-09-28:

```bash
glab mr create --source-branch t/T-004-book-a-class --target-branch <default-branch> \
  --title "T-004: Book a class" --description "<criteria + ProofBuild block>"
```

Other forges: push the branch and hand the human the URL the push prints.

## Merge (only with `autonomy.merge: auto` or a yes in this session)

GitHub, flags checked against https://cli.github.com/manual/gh_pr_merge on
2026-09-28: `--merge`, `--squash` or `--rebase` choose the method;
`--delete-branch` removes the branch after merging; `--auto` merges once
requirements are met.

```bash
gh pr merge <number> --squash      # use the method the repository already uses
```

Read the method from history (`git log --merges` present → merge commits;
single commits referencing PR numbers → squash). Do not pass `--delete-branch`
unless the project already deletes merged branches; deleting is a separate
yes.

GitLab: `glab mr merge` exists; its flags were not verified for this file.
Read `glab mr merge --help` before using one.

## Checks before merging

`gh pr checks <number>` (GitHub) or the forge's equivalent. A failing required
check means back to the build once, not a merge. A repository with no CI still
merges only on ProofBuild `VERIFIED`, and the ledger says `no CI`.
