// node mcp/project-knowledge/test.mjs — the MCP server over real stdio, the
// knowledge init/remove round trip, and the Stop hook, in a throwaway repo.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HUB = join(dirname(fileURLToPath(import.meta.url)), "../..");
const repo = mkdtempSync(join(tmpdir(), "pk-test-"));
const git = (...a) => spawnSync("git", ["-C", repo, ...a], { encoding: "utf8" });
const commit = (msg) => { writeFileSync(join(repo, "f.txt"), msg); git("add", "-A"); git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", msg); };

try {
  git("init", "-q");
  commit("first");
  writeFileSync(join(repo, "CLAUDE.md"), "# Repo\n");
  mkdirSync(join(repo, ".claude"));
  writeFileSync(join(repo, ".claude/settings.json"), JSON.stringify({ hooks: { Stop: [{ hooks: [{ type: "command", command: "other.sh" }] }] } }));

  // init: idempotent, keeps the existing hook, writes every piece.
  const cli = (...a) => spawnSync("node", [join(HUB, "scripts/skills-hub.mjs"), "knowledge", ...a], { cwd: repo, encoding: "utf8" });
  assert.equal(cli("init").status, 0);
  assert.match(cli("init").stdout, /nothing to do/, "second init must change nothing");
  const settings = JSON.parse(readFileSync(join(repo, ".claude/settings.json"), "utf8"));
  assert.equal(settings.hooks.Stop.length, 2);
  assert.equal(settings.hooks.Stop[0].hooks[0].command, "other.sh");
  assert.ok(existsSync(join(repo, ".claude/skills/project-knowledge/SKILL.md")));
  assert.deepEqual(JSON.parse(readFileSync(join(repo, ".mcp.json"), "utf8")).mcpServers["project-knowledge"].args.slice(-2), ["knowledge", "mcp"]);
  assert.match(readFileSync(join(repo, "CLAUDE.md"), "utf8"), /\.agents\/knowledge/);
  assert.match(readFileSync(join(repo, ".gitignore"), "utf8"), /\.learn-nagged/);

  // Stop hook: first run asks once per HEAD; quiet under the threshold.
  const hook = (input = "{}") => spawnSync("bash", [join(repo, ".claude/hooks/knowledge-check.sh")], { cwd: repo, input, encoding: "utf8" }).stdout;
  assert.match(hook(), /never been learned/);
  assert.equal(hook(), "", "fires at most once per HEAD");
  const kdir = join(repo, ".agents/knowledge");
  writeFileSync(join(kdir, ".learn-state.json"), JSON.stringify({ last_learned_commit: git("rev-parse", "HEAD").stdout.trim(), updated_at: "2026-01-01" }));
  for (let i = 0; i < 5; i++) commit(`c${i}`);
  assert.equal(hook('{"stop_hook_active": true}'), "", "never blocks twice in a row");
  assert.match(hook(), /5 commits behind/);

  // MCP server over stdio.
  writeFileSync(join(kdir, "architecture.md"), "# Architecture\n\n## Run it\npnpm dev\n\n## Queue\nJobs go through QUEUE_URL.\n");
  writeFileSync(join(kdir, "gotchas.md"), "# Gotchas\n\n## Webhook marks orders paid\nNot the charge.\n");
  writeFileSync(join(kdir, "decisions.md"), "# Decisions\n\n## 2026-01-01 — Queue over cron\nWhy: overlaps.\n");
  const reqs = [
    { jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-06-18" } },
    { jsonrpc: "2.0", method: "notifications/initialized" },
    { jsonrpc: "2.0", id: 2, method: "tools/list" },
    { jsonrpc: "2.0", id: 3, method: "tools/call", params: { name: "knowledge_search", arguments: { query: "queue url" } } },
    { jsonrpc: "2.0", id: 4, method: "tools/call", params: { name: "knowledge_onboard", arguments: {} } },
    { jsonrpc: "2.0", id: 5, method: "tools/call", params: { name: "knowledge_read", arguments: { doc: "../../etc/passwd" } } },
    { jsonrpc: "2.0", id: 6, method: "tools/call", params: { name: "knowledge_status", arguments: {} } },
    { jsonrpc: "2.0", id: 7, method: "prompts/get", params: { name: "onboard" } },
    { jsonrpc: "2.0", id: 8, method: "nope" },
  ];
  const srv = spawnSync("node", [join(HUB, "scripts/skills-hub.mjs"), "knowledge", "mcp"], { cwd: repo, input: reqs.map((r) => JSON.stringify(r)).join("\n") + "\n", encoding: "utf8" });
  const res = Object.fromEntries(srv.stdout.trim().split("\n").map((l) => JSON.parse(l)).map((r) => [r.id, r]));
  assert.equal(Object.keys(res).length, 8, "a notification gets no answer");
  assert.equal(res[1].result.serverInfo.name, "project-knowledge");
  assert.equal(res[2].result.tools.length, 4);
  assert.match(res[3].result.content[0].text, /## Queue/);
  assert.doesNotMatch(res[3].result.content[0].text, /Run it/, "a section must contain every term");
  assert.match(res[4].result.content[0].text, /5 commit\(s\) behind HEAD[\s\S]*Webhook marks[\s\S]*Queue over cron/);
  assert.equal(res[5].result.isError, true, "only listed docs are readable");
  assert.equal(JSON.parse(res[6].result.content[0].text).commits_behind_head, 5);
  assert.match(res[7].result.messages[0].content.text, /knowledge_onboard/);
  assert.equal(res[8].error.code, -32601);

  // remove: takes back what init added, keeps the knowledge and the other hook.
  assert.equal(cli("remove").status, 0);
  const after = JSON.parse(readFileSync(join(repo, ".claude/settings.json"), "utf8"));
  assert.deepEqual(after.hooks.Stop, [{ hooks: [{ type: "command", command: "other.sh" }] }]);
  assert.ok(!existsSync(join(repo, ".mcp.json")));
  assert.ok(!existsSync(join(repo, ".claude/skills/project-knowledge")));
  assert.ok(existsSync(join(kdir, "architecture.md")));
  console.log("project-knowledge: all checks passed");
} finally {
  rmSync(repo, { recursive: true, force: true });
}
