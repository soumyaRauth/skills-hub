# Example — a first-time builder with an idea

## Contents

- Repository
- Request
- Stage 1 — the one interruption
- The user answers
- Stage 2 — spec (excerpt)
- Stage 3 — stack
- Stage 4 — scaffold, and what it says to a beginner
- Stage 5
- What it did not do

Illustrative. The gym is invented; the shape of the exchange is the point.

## Repository

Only `README.md`: members book classes by messaging the front desk, and the
idea is that members see this week's classes, book a spot and cancel;
instructors see who is booked. State: **IDEA-ONLY**.

## Request

> I want to build an app where our climbing gym's members can book classes.
> I've never built a full app before — where do I start?

## Stage 1 — the one interruption

The README already answers *who* (members, instructors) and most of the
workflow. Still unknown, and each would change v1: how a class fills up,
payment, what the developer knows, a deadline. Where it runs is assumed.

```
⚡ Project Kickoff — new app from an idea, empty repo

WAITING FOR ANSWERS

Your README already tells me who uses it and what they do. Four questions
before I write anything. Short answers are fine; "you decide" is an answer too.

1. Does each class have a maximum number of people? If a class is full, what
   should happen: nothing, or a waiting list?
2. Should members pay for classes inside the app in the first version, or not yet?
3. What do you already know how to program in, if anything?
4. Is there a date this needs to be working by?

Meanwhile I am assuming: a website that works well on phones (no app store),
one gym location, members sign in with email and password, and the front desk
adds classes. Say so if any of that is wrong.
```

No stack menu, no framework question, nothing written to disk.

## The user answers

> Yes, max 12 per class, no waiting list for now. No payments, they pay at the
> desk. I did a bit of Python at school. No date, I'd like it by spring but no
> pressure.

## Stage 2 — spec (excerpt)

Member accounts store names and emails, so Standards Compass engages in the
same turn:

```
⚡ Project Kickoff · Standards Compass — new app from an idea; v1 has member accounts
HANDOFF → standards-compass: member sign-in and stored contact details [spec §Users, §Constraints]
```

```markdown
## Core workflow (v1)
1. A member signs in. [assumed: changes if members should book without an account]
2. They see this week's classes with spots left. [you said]
3. They book a class; a full class (12) cannot be booked. [you said]
4. They see their bookings and cancel one. [you said]
5. An instructor sees who is booked into their class. [you said]
6. Front desk staff add and edit classes in the admin screen. [assumed: changes if instructors add their own]

## Non-goals (not in v1)
- Payments — members pay at the desk. [you said]
- Waiting list. [you said]
- Native phone app. [assumed: changes if an app store listing is needed]

## Constraints
- Deadline: none stated; "by spring, no pressure". [you said]
- Standards: <what standards-compass named for sign-in and stored emails>

## Open decisions
- How late can a member cancel? — blocks: cancellation rules
- Can a member book the same class twice for a friend? — blocks: booking rules
```

"By spring" is recorded as their words, not turned into a date.

## Stage 3 — stack

```
STACK   Python 3.12+ · Django · SQLite locally, PostgreSQL when deployed
WHY     You know some Python; Django has sign-in, an admin screen for the front
        desk and database changes built in, so v1 needs few extra packages.
HANDOFF → dependency-guard: django, ruff for the scaffold
```

## Stage 4 — scaffold, and what it says to a beginner

The README's idea text is kept, and a *Run it* section is added below it.

```
SCAFFOLD PROOF
install   pip install -r requirements.txt                  exit 0
lint      ruff check . && ruff format --check .            exit 0
test      python manage.py test                            1 passed
run       python manage.py runserver → GET / returned 200  checked, then stopped
CI        .github/workflows/ci.yml written                 not run here (runs on first push)

What these do:
- install downloads the libraries the project needs. Run it once, and again when requirements.txt changes.
- lint and format check the code for common mistakes and consistent layout.
- test runs the automatic checks. Right now there is one: the home page loads.
- runserver starts the site on your computer at http://127.0.0.1:8000.
```

## Stage 5

```
READY TO BUILD

Spec      docs/spec.md · 8 [you said] · 5 [assumed] · 2 open decisions
Stack     Python · Django · SQLite (PostgreSQL when deployed)
Scaffold  install ✓ · lint ✓ · 1/1 tests ✓ · runs ✓ · CI written
Next      HANDOFF → delivery-planner: milestone 1 = walking skeleton deployed

Check the [assumed] lines in docs/spec.md — each one is a guess I made.
```

## What it did not do

- Invent a class schedule, a price, a member count or a launch date.
- Build sign-in, booking or the class list. Those are the first tickets.
- Suggest React, a mobile app, or microservices.
- Create a GitHub repository or push. Nobody asked, and it is outward-facing.
