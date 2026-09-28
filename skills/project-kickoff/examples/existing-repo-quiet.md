# Example — an existing codebase, where it stays quiet

Illustrative. The repository is invented.

## Repository

A Django project with `manage.py`, `requirements.txt`, four apps, migrations
and a test suite. State: **EXISTING**.

## Request

> Start a new booking module so customers can reserve a table.

## What happens

Project Kickoff reads the tree, sees application code and a manifest with real
dependencies, and does not engage. *New* and *start* describe a feature, not a
project. No questions, no `docs/spec.md`, no scaffold, no stack line.

The request goes where features go: `proof-driven-dev` turns it into
requirements and builds it; `standards-compass` may add a few lines if booking
stores customer contact details; `impact-map` if it changes something other
code depends on.

## When the skill is loaded anyway

If Project Kickoff was already loaded earlier in the session, or the user
names it (*use project kickoff for this*), it answers in one line and stops:

```
NOT A KICKOFF — this repository already has an application (manage.py, 4 apps, tests). Building the booking module as a feature instead.
```

## Other requests where it stays quiet

| Request | Why |
| --- | --- |
| *Quick throwaway script to test the weather API, I'll delete it* | Declared spike |
| *Is a booking app for gyms a good business idea?* | No intent to build |
| *Add a new microservice for notifications* (in an existing repo) | A new part of an existing system; `architecture-engineer` if the structure is the question |
| *Set up a new React component library folder in our monorepo* | Existing codebase |
