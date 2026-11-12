#!/usr/bin/env node
// npx github:soumyaRauth/skills-hub uninstall [--project] [--dry-run]
// npx github:soumyaRauth/skills-hub knowledge <init|remove|mcp>  (see knowledge.mjs)
// npx github:soumyaRauth/skills-hub runway <status|install-hooks|...>
//
// uninstall removes the skills this repository ships, and no others. The list
// is read from skills/ at run time, so a skill added later is covered without
// editing this file. It hands the list to the Skills CLI, which skips any that
// are not installed.
//
// runway copies the Runway tool to ~/.claude/runway/bin/ and runs it there, so
// the hooks it installs point at a stable path rather than at npx's cache,
// which can be cleared. Each run refreshes the copy to this version.
import { chmodSync, cpSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const usage = "usage: npx github:soumyaRauth/skills-hub uninstall [--project] [--dry-run]\n       npx github:soumyaRauth/skills-hub knowledge <init|remove|mcp>\n       npx github:soumyaRauth/skills-hub runway <status|install-hooks|uninstall-hooks|backtest|calibrate|accuracy|--help>";
const [cmd, ...flags] = process.argv.slice(2);

if (cmd === "knowledge") {
  const { main } = await import("./knowledge.mjs");
  main(flags);
} else if (cmd === "runway") {
  runway();
} else {
  uninstall();
}

function runway() {
  const src = join(dirname(fileURLToPath(import.meta.url)), "..", "integrations", "claude-code", "runway");
  // The same folder the Python side calls home: CLAUDE_RUNWAY_HOME, or <Claude dir>/runway.
  const home = process.env.CLAUDE_RUNWAY_HOME || join(process.env.CLAUDE_CONFIG_DIR || join(homedir(), ".claude"), "runway");
  const bin = join(home, "bin");
  mkdirSync(bin, { recursive: true });
  for (const f of readdirSync(src)) {
    if (f === "claude-runway" || (f.endsWith(".py") && !f.startsWith("test_"))) cpSync(join(src, f), join(bin, f));
  }
  chmodSync(join(bin, "claude-runway"), 0o755);
  const python = process.platform === "win32" ? "python" : "python3";
  const run = spawnSync(python, [join(bin, "claude-runway"), ...flags], { stdio: "inherit" });
  if (run.error) {
    console.error(`runway needs Python 3 (${python} was not found on PATH).`);
    process.exit(1);
  }
  process.exit(run.status ?? 1);
}

function uninstall() {
  const unknown = flags.filter((f) => f !== "--project" && f !== "--dry-run");
  if (cmd !== "uninstall" || unknown.length) {
    console.error(unknown.length ? `unknown option: ${unknown.join(" ")}\n${usage}` : usage);
    process.exit(2);
  }

  const dir = join(dirname(fileURLToPath(import.meta.url)), "..", "skills");
  const skills = readdirSync(dir).filter((d) => existsSync(join(dir, d, "SKILL.md"))).sort();

  // Named, never --skill '*': the wildcard would remove every skill on the machine.
  const args = ["--yes", "skills", "remove", ...skills, ...(flags.includes("--project") ? [] : ["-g"]), "-y"];
  if (flags.includes("--dry-run")) {
    console.log(`npx ${args.join(" ")}`);
    process.exit(0);
  }
  // ponytail: shell only on Windows, where npx is a .cmd; the args are fixed skill names.
  const run = spawnSync("npx", args, { stdio: "inherit", shell: process.platform === "win32" });
  process.exit(run.status ?? 1);
}
