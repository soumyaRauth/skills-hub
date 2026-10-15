// npx github:soumyaRauth/skills-hub knowledge <init|remove|mcp>
//
// init    sets a repository up so its knowledge stays current and reaches every
//         developer who clones it: the project-knowledge skill, the Stop hook
//         that keeps it fresh, and the MCP server, all as committed project
//         files. Safe to re-run; it updates the copies and adds nothing twice.
// remove  takes those back out. The knowledge docs stay: they are the project's.
// mcp     runs the MCP server (what .mcp.json starts; not run by hand).
import { chmodSync, cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { findRoot, serve } from "../mcp/project-knowledge/server.mjs";

const HUB = join(dirname(fileURLToPath(import.meta.url)), "..");
const HOOK_CMD = '"$CLAUDE_PROJECT_DIR"/.claude/hooks/knowledge-check.sh';
const MCP = { command: "npx", args: ["-y", "github:soumyaRauth/skills-hub", "knowledge", "mcp"] };
const POINTER = "Architecture, decisions and gotchas: `.agents/knowledge/` (read on demand, or through the project-knowledge MCP server; kept current by the `project-knowledge` skill).";
const NAGGED = ".agents/knowledge/.learn-nagged";

const readJson = (f) => (existsSync(f) ? JSON.parse(readFileSync(f, "utf8")) : {});
const writeJson = (f, o) => { mkdirSync(dirname(f), { recursive: true }); writeFileSync(f, JSON.stringify(o, null, 2) + "\n"); };
// True when every file under src exists under dst with the same bytes.
function same(src, dst) {
  if (!statSync(src).isDirectory()) return existsSync(dst) && readFileSync(src).equals(readFileSync(dst));
  return readdirSync(src, { recursive: true }).every((f) => statSync(join(src, f)).isDirectory() || same(join(src, f), join(dst, f)));
}
const isOurs = (h) => String(h?.command ?? "").includes("knowledge-check.sh");

export function init(root, { dryRun = false, skill = true } = {}) {
  const done = [];
  const step = (msg, fn) => { done.push(msg); if (!dryRun) fn(); };

  const skillSrc = join(HUB, "skills/project-knowledge");
  if (skill && !same(skillSrc, join(root, ".claude/skills/project-knowledge"))) {
    step("copy skill      .claude/skills/project-knowledge/", () =>
      cpSync(skillSrc, join(root, ".claude/skills/project-knowledge"), { recursive: true }));
  }
  const hookSrc = join(HUB, "integrations/claude-code/knowledge-check.sh");
  const hookDst = join(root, ".claude/hooks/knowledge-check.sh");
  if (!same(hookSrc, hookDst)) {
    step("copy Stop hook  .claude/hooks/knowledge-check.sh", () => {
      mkdirSync(dirname(hookDst), { recursive: true });
      cpSync(hookSrc, hookDst);
      chmodSync(hookDst, 0o755);
    });
  }

  // /learn: a manual trigger, so nobody has to remember the skill's name.
  const cmdSrc = join(HUB, "integrations/claude-code/learn.md");
  const cmdDst = join(root, ".claude/commands/learn.md");
  if (!same(cmdSrc, cmdDst)) {
    step("add command     .claude/commands/learn.md (/learn)", () => {
      mkdirSync(dirname(cmdDst), { recursive: true });
      cpSync(cmdSrc, cmdDst);
    });
  }

  const settingsFile = join(root, ".claude/settings.json");
  const settings = readJson(settingsFile);
  const stop = settings.hooks?.Stop ?? [];
  if (!stop.some((g) => (g.hooks ?? []).some(isOurs))) {
    step("register hook   .claude/settings.json (hooks.Stop)", () => {
      settings.hooks = { ...settings.hooks, Stop: [...stop, { hooks: [{ type: "command", command: HOOK_CMD }] }] };
      writeJson(settingsFile, settings);
    });
  }

  const mcpFile = join(root, ".mcp.json");
  const mcp = readJson(mcpFile);
  if (JSON.stringify(mcp.mcpServers?.["project-knowledge"]) !== JSON.stringify(MCP)) {
    step("register MCP    .mcp.json (project-knowledge)", () => {
      mcp.mcpServers = { ...mcp.mcpServers, "project-knowledge": MCP };
      writeJson(mcpFile, mcp);
    });
  }

  if (!existsSync(join(root, ".agents/knowledge"))) {
    step("create          .agents/knowledge/", () => mkdirSync(join(root, ".agents/knowledge"), { recursive: true }));
  }

  const gi = join(root, ".gitignore");
  const giText = existsSync(gi) ? readFileSync(gi, "utf8") : "";
  if (!giText.split("\n").includes(NAGGED)) {
    step(`ignore          ${NAGGED}`, () =>
      writeFileSync(gi, giText + (giText && !giText.endsWith("\n") ? "\n" : "") + `\n# Stop hook's once-per-commit marker; the knowledge cursor itself is committed.\n${NAGGED}\n`));
  }

  // Claude Code reads CLAUDE.md; Codex and others read AGENTS.md. Point each
  // that exists at the knowledge, and create CLAUDE.md when neither does.
  const memories = ["CLAUDE.md", "AGENTS.md"].filter((f) => existsSync(join(root, f)));
  for (const f of memories.length ? memories : ["CLAUDE.md"]) {
    const file = join(root, f);
    const text = existsSync(file) ? readFileSync(file, "utf8") : "";
    if (text.includes(".agents/knowledge")) continue;
    step(`point           ${f} at .agents/knowledge/`, () =>
      writeFileSync(file, text + (text && !text.endsWith("\n") ? "\n" : "") + (text ? "\n" : "") + POINTER + "\n"));
  }
  return done;
}

export function remove(root, { dryRun = false } = {}) {
  const done = [];
  const step = (msg, fn) => { done.push(msg); if (!dryRun) fn(); };
  for (const p of [".claude/skills/project-knowledge", ".claude/hooks/knowledge-check.sh", ".claude/commands/learn.md"]) {
    if (existsSync(join(root, p))) step(`delete          ${p}`, () => rmSync(join(root, p), { recursive: true }));
  }
  const settingsFile = join(root, ".claude/settings.json");
  const settings = readJson(settingsFile);
  const stop = settings.hooks?.Stop;
  if (stop?.some((g) => (g.hooks ?? []).some(isOurs))) {
    step("unregister hook .claude/settings.json", () => {
      const kept = stop.map((g) => ({ ...g, hooks: (g.hooks ?? []).filter((h) => !isOurs(h)) })).filter((g) => g.hooks.length);
      if (kept.length) settings.hooks.Stop = kept; else delete settings.hooks.Stop;
      writeJson(settingsFile, settings);
    });
  }
  const mcpFile = join(root, ".mcp.json");
  const mcp = readJson(mcpFile);
  if (mcp.mcpServers?.["project-knowledge"]) {
    step("unregister MCP  .mcp.json", () => {
      delete mcp.mcpServers["project-knowledge"];
      if (Object.keys(mcp.mcpServers).length || Object.keys(mcp).length > 1) writeJson(mcpFile, mcp); else rmSync(mcpFile);
    });
  }
  return done;
}

export function main(args) {
  const [sub, ...flags] = args;
  const usage = "usage: npx github:soumyaRauth/skills-hub knowledge <init [--no-skill] | remove | mcp [--root <dir>]> [--dry-run]";
  const i = flags.indexOf("--root");
  const root = findRoot(i >= 0 ? flags[i + 1] : process.cwd());
  if (sub === "mcp") return serve(root);
  if (sub !== "init" && sub !== "remove") {
    console.error(usage);
    process.exit(2);
  }
  const dryRun = flags.includes("--dry-run");
  const done = sub === "init" ? init(root, { dryRun, skill: !flags.includes("--no-skill") }) : remove(root, { dryRun });
  const where = relative(process.cwd(), root) || ".";
  console.log(done.length ? done.map((d) => `${dryRun ? "would " : ""}${d}`).join("\n") : `nothing to do in ${where}`);
  if (sub === "init" && !dryRun && done.length) {
    console.log("\nCommit these files so every developer who clones the repo gets them.\nNext: in Claude Code, ask \"learn this codebase\" (or just finish a reply: the Stop hook asks for the first run).");
  }
  if (sub === "remove" && !dryRun) console.log("Left in place: .agents/knowledge/ and the pointer line in CLAUDE.md/AGENTS.md (they are the project's).");
}
