# Project Knowledge

### Every new developer rebuilds how the codebase works. This writes it down once, and keeps it true.

Project Knowledge is an [Agent Skill](https://code.claude.com/docs/en/skills)
that builds a small, committed knowledge base in `.agents/knowledge/`
(architecture, a dated decision log, gotchas) and updates it incrementally: each
run reads only what changed since the last one.

```bash
npx skills add soumyaRauth/skills-hub --skill project-knowledge
```

For a whole team, set the repository up once instead. This adds the skill, a
Stop hook that keeps the knowledge current, and an MCP server that serves it,
all as files you commit:

```bash
npx -y github:soumyaRauth/skills-hub knowledge init
```

Then ask your agent to *learn this codebase*. After that, a developer who clones
the repository approves the MCP server once and asks, or types
`/mcp__project-knowledge__onboard` in Claude Code.

## What it does

| | |
| --- | --- |
| **Incremental** | Commit messages first, then `git diff --stat`, then full diffs only for paths that change structure or contracts. Cost follows the diff, not the codebase |
| **Automatic** | The Stop hook asks for a run every few commits (`LEARN_EVERY`, default 5). It costs no tokens until it fires, and fires once per commit at most |
| **Shared** | Everything is committed, the cursor included, so every clone shares one view |
| **Portable** | Plain markdown. The MCP server works with any MCP client; the files work with none |
| **Safe** | Never records a secret value, only that a variable exists and what it controls |

## What it will not do

- Start a full scan of a repository nobody asked about. The hook does nothing
  where `.agents/knowledge/` is absent.
- Commit. It says which files changed, and you commit them with your work.
- Invent a reason. A decision the history does not explain is recorded as an
  open question.

## Learn more

- [SKILL.md](SKILL.md) — the full method
- [references/knowledge-format.md](references/knowledge-format.md) — the files and their entries
- [references/incremental-learning.md](references/incremental-learning.md) — first run and later runs
- [references/setup.md](references/setup.md) — `knowledge init`, the hook, the MCP server, removing it
- Examples: [first run](examples/first-run.md) · [incremental run](examples/incremental-run.md) · [onboarding](examples/onboarding.md)
