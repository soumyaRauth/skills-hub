# Setup: hook, MCP server, and the team flow

## Contents

- One command per repository
- The Stop hook
- The MCP server
- A new developer's first day
- Removing it
- Later: a shared knowledge hub

## One command per repository

From the repository root:

```bash
npx -y github:soumyaRauth/skills-hub knowledge init      # --dry-run shows the plan first
```

It writes, all as project files meant to be committed:

| File | Why |
| --- | --- |
| `.claude/skills/project-knowledge/` | the skill, so every clone has it without installing anything (`--no-skill` skips it if you installed the skill globally) |
| `.claude/hooks/knowledge-check.sh` + a `Stop` entry in `.claude/settings.json` | keeps the knowledge current |
| `.mcp.json` entry `project-knowledge` | serves the knowledge to any MCP client |
| `.agents/knowledge/` | where the knowledge lives |
| one line in `.gitignore` | the hook's per-commit marker |
| one pointer line in `CLAUDE.md` / `AGENTS.md` | so agents know the knowledge exists |

Re-running it updates the copied skill and hook and adds nothing twice.

## The Stop hook

Runs when Claude Code finishes a reply. It is bash, git and grep, so it costs
no tokens when it does nothing, which is almost always. When the knowledge is
`LEARN_EVERY` (default 5) or more commits behind `HEAD`, or has never been
learned, it blocks the stop once and asks Claude to run this skill. It then
records `HEAD` in `.agents/knowledge/.learn-nagged`, so it asks at most once per
commit, and it never blocks a stop that a hook already continued.

It does nothing in a repository without `.agents/knowledge/`, so it is also safe
to register globally in `~/.claude/settings.json`.

It runs only inside a Claude Code session, at the end of a reply. Nothing runs
in the background.

## The MCP server

`.mcp.json` starts `npx -y github:soumyaRauth/skills-hub knowledge mcp`, a
dependency-free stdio server that reads `.agents/knowledge/` from the
repository it is started in. Claude Code asks each developer once to approve a
project's MCP servers.

| Tool | Returns |
| --- | --- |
| `knowledge_onboard` | architecture and gotchas in full, the five newest decisions, and how far behind `HEAD` the knowledge is |
| `knowledge_search` | the sections that mention every word of a query |
| `knowledge_read` | one doc in full |
| `knowledge_status` | the docs, the cursor, commits behind `HEAD` |

It also offers an `onboard` prompt, which Claude Code shows as the slash command
`/mcp__project-knowledge__onboard`.

The server only reads. Writing stays with the skill, so knowledge is always
produced from the code and the history by the same rules.

Any MCP client can use it: Cursor, VS Code, Codex and others take the same
command in their own MCP config.

## A new developer's first day

1. Clone. Open Claude Code. Approve the `project-knowledge` MCP server.
2. Type `/mcp__project-knowledge__onboard`, or just ask "how does this codebase
   work?"
3. Work. When their commits push the knowledge past the threshold, the hook
   asks Claude to update it, and the updated docs go in with their next commit.

## Removing it

```bash
npx -y github:soumyaRauth/skills-hub knowledge remove    # --dry-run first if you like
```

Removes the copied skill, the hook and both registrations. It leaves
`.agents/knowledge/` and the pointer line: those are the project's.

## Later: a shared knowledge hub

The knowledge is plain files with a fixed layout. A hosted hub that stores
knowledge per project would accept these files (pushed from CI or by the
developer), and serve the same four tools over MCP's HTTP transport. The
format is the contract: the hub stores and serves it, and nothing in a project
ever has to call the hub to work.
