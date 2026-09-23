# Example: the menu, a sequence, a stop, the ledger

**Request:** `/skills-pipeline add team invitations with roles`

The pipeline prints the menu from `references/pipeline.md` and waits. It has
not read the repository yet.

```
1. Frame · project-compass
2. Design · architecture-engineer
3. Standards · standards-compass
...
11. Investigate · engineering-investigator

Sequence? e.g. 1,6,7,10 · all · and the task, if not given yet
```

**Reply:** `1,3,6,7,10`

```
⚡ Skills Pipeline — Frame → Standards → Impact → Build → Ship gate
```

**Frame.** Project Compass finds roles checked by string comparison at seven
call sites and no roles table. It stops on the menu's condition, a business rule
the build depends on:

> Can one person hold different roles in different teams, or one role
> everywhere?

The run waits. **Reply:** *per team.*

**Standards, Impact, Build, Ship gate** then run in order. Each receives the
task plus the answer and every earlier stage's result. Impact Map and
Production Guard run as subagents, so the pipeline passes that context in
explicitly.

```
#   Stage       Skill               Status   Result
1   Frame       project-compass     RAN      roles become per-team (answered)
3   Standards   standards-compass   RAN      4 requirements: invite token expiry, single use, rate limit, audit entry
6   Impact      impact-map          RAN      7 role checks, 1 raw-SQL report, 2 fixtures
7   Build       proof-driven-dev    RAN      VERIFIED — 9/9 requirements proven
10  Ship gate   production-guard    RAN      CONDITIONAL SHIP — backfill existing members before deploy
```

Open question: none.

Each Result cell is that skill's own verdict line. The pipeline added none.
