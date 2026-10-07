# Stack defaults and scaffold commands

## Contents

- Choosing
- Scaffold commands, by stack
- First CI check (GitHub Actions)
- Sources

The stack is chosen in this order: **what the developer already knows**, then
**where it must run**, then the boring default for that pair. A language the
developer knows beats a language that is theoretically better for the job.

Versions come from the official site or the registry at scaffold time, read
from output. Never from memory. Every package goes through `dependency-guard`.

## Choosing

| Developer knows | Must run | Default | Notes |
| --- | --- | --- | --- |
| Python, or nothing yet | Web, phone browser | Django, SQLite locally, PostgreSQL when deployed | Accounts, an admin screen and migrations are built in, which covers most booking, listing and tracking ideas with few packages |
| JavaScript / TypeScript | Web, phone browser | The Node web framework they have used, rendering pages on the server, SQLite locally | If they have used none, Node with one mainstream server framework, chosen through `dependency-guard`. No separate front-end app for v1 unless they already build that way |
| Another language with a mainstream web framework (Ruby, PHP, Java, C#, Go) | Web | That language's most established full-stack framework | Their knowledge outweighs any default in this table |
| Anything | Native store app, offline, device hardware, a customer's network | No default | `HANDOFF → architecture-engineer` with the requirement quoted |

A beginner who knows nothing yet gets the first row. Say why in one line, and
do not present a menu.

What is never a default for a new project: microservices, a message queue,
Kubernetes, a separate API plus single-page app for a beginner, a NoSQL store
chosen for "scale", a framework whose first stable release is under a year old.
Each can be right later; none is right before the first workflow works.

## Scaffold commands, by stack

Only the commands below were checked against official documentation. For any
other stack, read that stack's official getting-started page before running
anything, and cite it in the reply.

### Python · Django

| Step | Command | Source |
| --- | --- | --- |
| Create | `django-admin startproject <name> .` | Django tutorial part 1 |
| Run | `python manage.py runserver` | Django tutorial part 1 |
| Test | `python manage.py test` (discovers `test*.py`) | Django testing overview |
| Lint / format | `ruff check .` · `ruff format --check .` | Ruff documentation |

Django's current docs (6.1 at the time of checking) support Python 3.12 and
later. By default a new project uses SQLite, which ships with Python. The admin
site is active by default.

### Node

| Step | Command | Source |
| --- | --- | --- |
| Test | `node --test` (built-in runner, stable since Node 20; finds `*.test.js`, `test/**/*.js` and similar) | Node.js test runner docs |

The web framework, linter and formatter are `dependency-guard` decisions; take
their commands from their own documentation.

### Plain Python (no framework)

`python -m pytest` runs pytest and also adds the current directory to
`sys.path`, which a new project's imports usually need.

## First CI check (GitHub Actions)

Workflow files must live in `.github/workflows/`. Use the major versions the
actions' own repositories show at scaffold time; at the time of checking the
latest releases were `actions/checkout` v7, `actions/setup-node` v7 and
`actions/setup-python` v7. Pinning style (tag or commit SHA) follows the
project's policy; with no policy yet, `dependency-guard` decides.

```yaml
name: ci
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: ruff check . && ruff format --check .
      - run: python manage.py test
```

Another host (GitLab, Forgejo, none) gets the equivalent in its own format,
from its own documentation. No remote yet: write the file, and say it has not
run.

## Sources

Checked 2026-09-28:

- https://docs.djangoproject.com/en/stable/intro/tutorial01/ — `startproject`, `runserver`, Python 3.12+ for 6.1
- https://docs.djangoproject.com/en/stable/intro/tutorial02/ — SQLite default, admin active by default
- https://docs.djangoproject.com/en/stable/topics/testing/overview/ — `manage.py test`, `test*.py` discovery
- https://docs.astral.sh/ruff/ — `ruff check`, `ruff format`
- https://nodejs.org/api/test.html — `node --test`, default patterns, stable since v20.0.0
- https://docs.pytest.org/en/stable/how-to/usage.html — `python -m pytest` and `sys.path`
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax — `.github/workflows` location
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow — `on: [push, pull_request]`
- GitHub releases API for actions/checkout (v7.0.1), actions/setup-node (v7.0.0), actions/setup-python (v7.0.0)

Not verified here: commands for any other framework or CI host. Read their
official documentation before use.
