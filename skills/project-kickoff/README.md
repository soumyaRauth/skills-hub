# Project Kickoff

An Agent Skill for the first session of a new project:

> **What exactly are we building first, on what, and is the empty repo ready to build in?**

```bash
npx skills add soumyaRauth/skills-hub --skill project-kickoff
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill project-kickoff --agent claude-code --copy
```

---

## Why it exists

New projects go wrong before the first feature. The idea is never pinned down,
so work starts on login screens while the one workflow that matters is still
vague. Or the repository starts on sand: no test runs, nobody wrote down how to
start it, a real key sits in a committed file.

Coding agents make both worse. Given *"an app where members book classes"*,
they invent the business's rules, pick a stack from a blog post, and generate
dozens of files. A beginner cannot tell what was decided and what was made up.

## What it does

```
idea ─▶ product frame: at most five plain questions, in one block (or none, if you said it all)
     ─▶ docs/spec.md: problem, users, core workflow, v1 scope, non-goals, open decisions
                      every line labelled [you said] or [assumed]
     ─▶ stack: a boring default you already know, with one line of reason
     ─▶ scaffold: runs, one passing test, lint, .env.example, README, first CI check
                  install · test · run actually executed and shown
     ─▶ handoff to planning: milestone 1 = walking skeleton deployed
```

```
READY TO BUILD

Spec      docs/spec.md · 8 [you said] · 5 [assumed] · 2 open decisions
Stack     Python · Django · SQLite (PostgreSQL when deployed)
Scaffold  install ✓ · lint ✓ · 1/1 tests ✓ · runs ✓ · CI written
Next      HANDOFF → delivery-planner: milestone 1 = walking skeleton deployed
```

Three worked examples: [a first-time builder's idea](examples/beginner-climbing-gym.md) ·
[an experienced developer who gives everything up front](examples/experienced-full-brief.md) ·
[an existing codebase, where it stays out](examples/existing-repo-quiet.md)

## When it activates

On its own, when someone wants to start a new app or product from an idea, or
the repository is empty or holds only notes and the request is to build
something whole. It stays quiet in an existing codebase, for throwaway spikes,
and for questions about an idea nobody intends to build yet. See
[Activation](SKILL.md#activation).

## What it will not do

- **Invent your world.** Users, prices, schedules and deadlines come from you,
  or they are written down as `[assumed]` for you to check.
- **Ask you technical questions you cannot answer.** Language, database and
  hosting get safe defaults; you are asked about the product.
- **Pick exotic technology.** No microservices, queues or brand-new frameworks
  for a first project.
- **Scaffold over existing code, or overwrite a file without asking.**
- **Claim the scaffold works without running it.** A step that could not run
  is reported as not run.
- **Push, create remote repositories or deploy** without your yes.

It hands off rather than absorbs: packages go through Dependency Guard,
sign-in, payments and personal data through Standards Compass, a genuinely
unusual requirement to Architecture Engineer, pipelines to Release Engineer,
and the spec to Delivery Planner.

References: [`product-questions.md`](references/product-questions.md) ·
[`spec-format.md`](references/spec-format.md) ·
[`stack-defaults.md`](references/stack-defaults.md)

## License

MIT — see [`LICENSE`](../../LICENSE).
