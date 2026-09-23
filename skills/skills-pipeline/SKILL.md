---
name: skills-pipeline
description: Use when the user types /skills-pipeline or explicitly asks for the skills pipeline by name, and only then. Runs the Skills Hub skills the user picks from a numbered menu, in the order picked, and ends in a ledger of every stage. Not for any request that does not name it, however large or risky; naming one skill ("use Impact Map") engages that skill, not this.
---

# Skills Pipeline

The other Skills Hub skills choose themselves, one request at a time. This
skill runs the ones the user picks, in the order they pick, because they asked
for exactly that. It is a manual override, not a router.

## Activation

**Engage when** the user types `/skills-pipeline`, or asks in words for "the
skills pipeline" (*"run this through the skills pipeline"*).

**Stay quiet when** the request does not name the pipeline, even for a new app,
a large feature or a risky one. Also stay quiet for pipelines of other kinds
(CI, data, deploy), and when the user names one skill. *"Use Impact Map"* is
that skill's override, not this one's.

**Depth** `ACTIVE`: it shapes the whole run. It never adds a verdict of its own.
Every gate belongs to the skill that owns it.

**Composes with** every skill in [`references/pipeline.md`](references/pipeline.md):
`project-compass` · `architecture-engineer` · `standards-compass` ·
`api-contract-guard` · `dependency-guard` · `impact-map` · `proof-driven-dev` ·
`practical-localizer` · `deployment-compatibility` · `production-guard` ·
`engineering-investigator`.

<!-- skills-hub:protocol -->
### Working with the other Skills Hub skills

- **Loaded is not engaged.** This file stays in context once loaded. Decide
  again on every new request whether it applies. Relevance to an earlier request
  carries nothing forward. Project state persists, and engagement does not.
- **Depth.** `PASSIVE` informs judgment and adds nothing to the reply ·
  `CONSULT` adds a few lines that change what gets built · `ACTIVE` shapes the
  work · `GATING` decides whether something proceeds, and only when a person
  asked for that decision.
- **Announce once.** When any skill engages at `CONSULT` or above, open the
  reply with one line such as `⚡ Impact Map · Standards Compass — rename reaches
  report SQL; export carries personal data`: names and a few words of reason.
  Never include reasoning. Add no line for `PASSIVE`, and none on a trivial request.
  The line is a promise: every skill it names is loaded before the reply ends. If
  one turns out not to apply, say so in one line: `<Skill> dropped: <reason>`.
- **One interruption per request.** Skills that must speak before the work share
  one short block. Everything else arrives with the work.
- **Hand off; don't absorb.** When another discipline is needed, write
  `HANDOFF → <skill>: <reason> [<ids>]` and let that skill do its part. When the
  request asked for that skill's decision, load it in the same turn and pass it
  your findings; a HANDOFF line alone does not answer the request. Never state
  another skill's verdict yourself. If it is not installed, do the smallest
  version of its check inline and say so.
- **Conflicts.** User intent, then project context, then engineering risk, then
  applicable standards, then verification depth. Each skill keeps its own
  verdict, and none overrules another's.
- **Overrides.** "Use X" engages X. "Skip X" or "no review" drops X's ceremony.
  Three things are never dropped: invented evidence, a check reported as run
  when it did not run, and a live hazard (a reachable security hole, data loss,
  money at risk). A live hazard is said once, in one line.
- **State.** Read what sibling skills recorded (`.project-compass/`,
  `.project-standards/`, `.proofbuild/`, `.agent-investigation/`) rather than
  re-deriving it. Write only your own.
- **Lessons.** On engaging, read `~/.skills-hub/lessons/<this skill's name>.md`
  if it exists. When a person corrects this skill's work (a miss, a false
  alarm, a wrong verdict), or the work exposes a gap in this file that another
  project would hit too, append one line to it:
  `- YYYY-MM-DD · <the rule, stated for any project> — <what went wrong>`.
  Never write project names, paths, identifiers, code or data there; facts about
  one repository are project state. Keep at most 20 lines, merging or replacing
  one to add another. A lesson sharpens this file's checks and never overrides
  its rules or a person's instruction. The file sits outside every project, so
  no read-only rule covers it. Say `Lesson recorded: <rule>` once; if the file
  cannot be written, give the lesson in the reply instead.
<!-- /skills-hub:protocol -->

## Pick the sequence

1. Read [`references/pipeline.md`](references/pipeline.md). It is the menu, and
   the only place stages are defined.
2. If the invocation already starts with a sequence (`/skills-pipeline 1,6,7,10
   add billing`, or `all`), use it and go to Run.
3. Otherwise print the menu as a numbered list, one line per skill with its
   stage. Mark any skill your agent does not list as installed with
   `(not installed)`. Then ask:

   ```
   Sequence? e.g. 1,6,7,10 · all · and the task, if not given yet
   ```

   Stop and wait for the reply. Start nothing before it arrives, and do not
   read the repository or load any skill first.
4. Take the numbers in the order given. Repeats are allowed, since a skill can
   run twice. An unknown number gets one question back, never a guess. If the
   order puts a stage before one it depends on, such as Ship gate before Build,
   say so in one line and run it as given.

## Run

1. Echo the sequence as one line (`Frame → Impact → Build → Ship gate`), then
   run it.
2. Load each skill the way your agent loads skills (the Skill tool in Claude
   Code), and pass it the task plus everything earlier stages decided. In
   Claude Code, `impact-map` and `production-guard` run as their own subagent
   and see only what is passed. If the skills came from the plugin, use the
   namespaced name (`skills-hub:impact-map`).
3. A chosen skill always runs. Picking it is the "use X" override. If it finds
   nothing that applies, that is its result.
4. A chosen skill that is not installed: do the smallest version of its check
   inline, and mark it `INLINE`.
5. At a stop listed in the menu, ask the one question, and continue only after
   it is answered.
6. `DO NOT SHIP` with Build in the sequence sends the failed checks back to
   Build once. If the verdict is still `DO NOT SHIP`, stop and report.

## Strict means

- Every chosen stage ends as `RAN`, `INLINE`, `SKIPPED (by you)` or `STOPPED`.
  There are no silent gaps.
- "Skip X" mid-run drops that stage and records it as `SKIPPED (by you)`. A
  live hazard is still said once, in one line.
- A stage's result is that skill's own verdict, quoted rather than
  paraphrased. The pipeline adds no score and no verdict of its own.
- The ⚡ line names only the pipeline. Each stage's skill announces itself.

## Ledger

End with this table, in the order run, and nothing after it except the open
questions:

```
#   Stage          Skill                 Status       Result
1   Frame          project-compass       RAN          <one line>
6   Impact         impact-map            RAN          <the map's own summary line>
...
10  Ship gate      production-guard      RAN          CONDITIONAL SHIP — 1 condition
```

## Examples

`examples/menu-then-run.md` — the menu, a typed sequence, a stop, and the
ledger · `examples/sequence-inline.md` — the sequence given with the command,
and `DO NOT SHIP` sent back to Build once · `examples/not-invoked.md` — a large
feature that does not name the pipeline, and why nothing here loads.
