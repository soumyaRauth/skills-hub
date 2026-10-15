#!/usr/bin/env node
// Project Knowledge MCP server: serves a repository's .agents/knowledge/ to any
// MCP client, so a developer who just cloned the repo can ask how it works.
//
//   npx -y github:soumyaRauth/skills-hub knowledge mcp [--root <dir>]
//
// stdio, newline-delimited JSON-RPC, no dependencies. It only reads: the
// knowledge files are written by the project-knowledge skill and committed.
// ponytail: local files only. A hosted knowledge hub would serve these same
// tool names over HTTP; the markdown format is the contract, not this process.
import { existsSync, readFileSync, readdirSync, realpathSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join, resolve } from "node:path";
import { createInterface } from "node:readline";
import { pathToFileURL } from "node:url";

const VERSION = "1.0.0";

export function findRoot(start) {
  const git = spawnSync("git", ["rev-parse", "--show-toplevel"], { cwd: start, encoding: "utf8" });
  return git.status === 0 ? git.stdout.trim() : resolve(start);
}

const docsDir = (root) => join(root, ".agents", "knowledge");

export function listDocs(root) {
  const dir = docsDir(root);
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => f.endsWith(".md")).sort();
}

function readDoc(root, name) {
  const file = name.endsWith(".md") ? name : `${name}.md`;
  // Names come from the client: only files that listDocs returns are readable.
  if (!listDocs(root).includes(file)) return null;
  return readFileSync(join(docsDir(root), file), "utf8");
}

// Splits a doc on "## " headings; the text before the first one is its intro.
function sections(text) {
  const out = [];
  for (const part of text.split(/^(?=## )/m)) if (part.trim()) out.push(part.trim());
  return out;
}

export function status(root) {
  const docs = listDocs(root);
  if (!docs.length) {
    const note = existsSync(docsDir(root))
      ? "Set up, but nothing learned yet. Ask the agent to learn the codebase (the project-knowledge skill)."
      : "No .agents/knowledge/ here. Run `npx -y github:soumyaRauth/skills-hub knowledge init`, then ask the agent to learn the codebase.";
    return { initialized: false, root, docs, note };
  }
  let state = {};
  try { state = JSON.parse(readFileSync(join(docsDir(root), ".learn-state.json"), "utf8")); } catch {}
  const last = state.last_learned_commit;
  let behind = null;
  if (last) {
    const n = spawnSync("git", ["rev-list", "--count", `${last}..HEAD`], { cwd: root, encoding: "utf8" });
    if (n.status === 0) behind = Number(n.stdout.trim());
  }
  return { initialized: true, root, docs, last_learned_commit: last ?? null, updated_at: state.updated_at ?? null, commits_behind_head: behind };
}

function statusLine(s) {
  if (!s.initialized) return s.note;
  const age = s.commits_behind_head == null ? "freshness unknown" : `${s.commits_behind_head} commit(s) behind HEAD`;
  return `Knowledge last learned at ${s.last_learned_commit?.slice(0, 9) ?? "?"} (${s.updated_at ?? "unknown date"}), ${age}. Treat anything newer than that as unverified.`;
}

export function search(root, query, limit = 8) {
  const terms = String(query).toLowerCase().split(/\s+/).filter(Boolean);
  if (!terms.length) return [];
  const hits = [];
  for (const doc of listDocs(root)) {
    for (const sec of sections(readDoc(root, doc))) {
      const low = sec.toLowerCase();
      const score = terms.reduce((n, t) => n + (low.split(t).length - 1), 0);
      // Every term must appear, so a two-word query narrows instead of widening.
      if (terms.every((t) => low.includes(t))) hits.push({ doc, score, text: sec });
    }
  }
  return hits.sort((a, b) => b.score - a.score).slice(0, limit);
}

// The briefing a new developer starts from: architecture and gotchas in full
// (the skill keeps both short), the newest decisions, and how fresh it all is.
export function onboard(root) {
  const s = status(root);
  if (!s.initialized) return s.note;
  const parts = [statusLine(s)];
  for (const doc of ["architecture.md", "gotchas.md"]) {
    const text = readDoc(root, doc);
    if (text) parts.push(text.trim());
  }
  const decisions = readDoc(root, "decisions.md");
  if (decisions) {
    const entries = sections(decisions).filter((x) => x.startsWith("## "));
    parts.push(`# Recent decisions (${Math.min(5, entries.length)} of ${entries.length}; read decisions.md for the rest)\n\n${entries.slice(-5).join("\n\n")}`);
  }
  const others = s.docs.filter((d) => !["architecture.md", "gotchas.md", "decisions.md"].includes(d));
  if (others.length) parts.push(`Other knowledge docs: ${others.join(", ")} (knowledge_read).`);
  return parts.join("\n\n---\n\n");
}

const TOOLS = [
  { name: "knowledge_onboard", description: "Start here in an unfamiliar repository: architecture, gotchas, the newest decisions, and how current the knowledge is.", inputSchema: { type: "object", properties: {} } },
  { name: "knowledge_search", description: "Find the knowledge sections (architecture, decisions, gotchas) that mention every word of a query. Use before reading code to learn how something works or why it was built that way.", inputSchema: { type: "object", properties: { query: { type: "string" }, limit: { type: "number" } }, required: ["query"] } },
  { name: "knowledge_read", description: "Read one knowledge doc in full, by name (for example decisions or gotchas.md).", inputSchema: { type: "object", properties: { doc: { type: "string" } }, required: ["doc"] } },
  { name: "knowledge_status", description: "Which knowledge docs exist and how many commits they are behind HEAD.", inputSchema: { type: "object", properties: {} } },
];

const PROMPTS = [
  { name: "onboard", description: "Walk a new developer through this codebase from its recorded knowledge." },
];

export function callTool(root, name, args = {}) {
  switch (name) {
    case "knowledge_onboard": return onboard(root);
    case "knowledge_status": return JSON.stringify(status(root), null, 2);
    case "knowledge_read": {
      const text = readDoc(root, String(args.doc ?? ""));
      if (text == null) throw new Error(`no knowledge doc "${args.doc}"; have: ${listDocs(root).join(", ") || "none"}`);
      return text;
    }
    case "knowledge_search": {
      const hits = search(root, args.query ?? "", Number(args.limit) || 8);
      if (!hits.length) return `Nothing in the knowledge docs mentions all of: ${args.query}. Read the code, and record what you learn with the project-knowledge skill.`;
      return hits.map((h) => `[${h.doc}]\n${h.text}`).join("\n\n---\n\n");
    }
    default: throw new Error(`unknown tool: ${name}`);
  }
}

function handle(root, msg) {
  const { id, method, params = {} } = msg;
  switch (method) {
    case "initialize":
      return { protocolVersion: params.protocolVersion ?? "2025-06-18", capabilities: { tools: {}, prompts: {} }, serverInfo: { name: "project-knowledge", version: VERSION } };
    case "ping": return {};
    case "tools/list": return { tools: TOOLS };
    case "prompts/list": return { prompts: PROMPTS };
    case "prompts/get":
      if (params.name !== "onboard") throw Object.assign(new Error(`unknown prompt: ${params.name}`), { code: -32602 });
      return { messages: [{ role: "user", content: { type: "text", text: "I'm new to this repository. Call knowledge_onboard, then explain how the codebase fits together, how to run it, and the gotchas most likely to bite me first. Say how current the knowledge is, and check anything that matters against the code before relying on it." } }] };
    case "tools/call":
      try {
        return { content: [{ type: "text", text: callTool(root, params.name, params.arguments) }] };
      } catch (e) {
        return { content: [{ type: "text", text: e.message }], isError: true };
      }
    default:
      if (id === undefined) return undefined; // a notification: nothing to answer
      throw Object.assign(new Error(`method not found: ${method}`), { code: -32601 });
  }
}

export function serve(root, input = process.stdin, output = process.stdout) {
  const send = (o) => output.write(JSON.stringify(o) + "\n");
  createInterface({ input }).on("line", (line) => {
    if (!line.trim()) return;
    let msg;
    try { msg = JSON.parse(line); } catch { return send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "parse error" } }); }
    try {
      const result = handle(root, msg);
      if (msg.id !== undefined && result !== undefined) send({ jsonrpc: "2.0", id: msg.id, result });
    } catch (e) {
      if (msg.id !== undefined) send({ jsonrpc: "2.0", id: msg.id, error: { code: e.code ?? -32603, message: e.message } });
    }
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  const i = process.argv.indexOf("--root");
  serve(findRoot(i > 0 ? process.argv[i + 1] : process.cwd()));
}
