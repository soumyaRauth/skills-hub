#!/usr/bin/env node
// npx github:soumyaRauth/skills-hub uninstall [--project] [--dry-run]
//
// Removes the skills this repository ships, and no others. The list is read
// from skills/ at run time, so a skill added later is covered without editing
// this file. It hands the list to the Skills CLI, which skips any that are not
// installed.
import { existsSync, readdirSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const usage = "usage: npx github:soumyaRauth/skills-hub uninstall [--project] [--dry-run]";
const [cmd, ...flags] = process.argv.slice(2);
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
