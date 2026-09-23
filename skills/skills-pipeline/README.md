# Skills Pipeline

An Agent Skill that runs the other Skills Hub skills in a sequence you choose,
and only when you ask for it.

```bash
npx skills add soumyaRauth/skills-hub --skill skills-pipeline
```

For Claude Code specifically:

```bash
npx skills add soumyaRauth/skills-hub --skill skills-pipeline --agent claude-code --copy
```

---

## Why it exists

The other skills choose themselves, one request at a time, and stay quiet when
they have nothing to add. That is the right default. Sometimes you want the
opposite: a new app, or a feature you care about, taken through every
discipline you pick, in order, with nothing dropped along the way. This skill
is that override. It never engages on its own.

## How to use it

```
/skills-pipeline add subscription billing
```

It prints a numbered menu and waits:

```
1. Frame · project-compass
2. Design · architecture-engineer
...
10. Ship gate · production-guard
11. Investigate · engineering-investigator

Sequence? e.g. 1,6,7,10 · all · and the task, if not given yet
```

Reply with numbers in the order you want them, such as `1,3,6,7,10`, or `all`
for 1 to 10. To skip the menu, put the sequence first:
`/skills-pipeline 1,6,7,10 add billing`. In agents without slash commands, ask
for "the skills pipeline" by name.

## What strict means

- **Every chosen stage ends with a status.** It is `RAN`, `INLINE` (the skill
  is not installed and its smallest check ran inline), `SKIPPED (by you)` or
  `STOPPED`. Nothing drops out silently.
- **It stops where a person decides.** Examples are an undecided business rule,
  a choice between architectures, `BLOCKED`, and `DO NOT SHIP`.
- **`DO NOT SHIP` goes back to Build once.** If it fails again, the run stops
  and reports.
- **Verdicts belong to the skills.** Each stage's result is that skill's own
  verdict. The pipeline adds no score and no verdict.
- **It ends with a ledger**, one row per stage, in the order run.

## Changing the menu

The menu is [`references/pipeline.md`](references/pipeline.md): number, stage,
skill, and where it stops. Edit it to add, remove or renumber skills.

## Examples

| Example | Shows |
| --- | --- |
| [`menu-then-run.md`](examples/menu-then-run.md) | The menu, a typed sequence, a stop for a decision, and the ledger |
| [`sequence-inline.md`](examples/sequence-inline.md) | The sequence given with the command, and `DO NOT SHIP` sent back to Build once |
| [`not-invoked.md`](examples/not-invoked.md) | A large feature that does not name the pipeline, and why the pipeline stays out |
