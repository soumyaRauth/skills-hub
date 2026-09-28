import { createServer } from "node:http";

const notes = [];

export function createApp() {
  return createServer((req, res) => {
    if (req.method === "GET" && req.url === "/health") {
      return send(res, 200, { ok: true });
    }
    if (req.method === "GET" && req.url === "/notes") {
      return send(res, 200, notes);
    }
    if (req.method === "POST" && req.url === "/notes") {
      let body = "";
      req.on("data", (chunk) => (body += chunk));
      req.on("end", () => {
        const text = safeText(body);
        if (!text) return send(res, 400, { error: "text is required" });
        const note = { id: notes.length + 1, text };
        notes.push(note);
        send(res, 201, note);
      });
      return;
    }
    send(res, 404, { error: "not found" });
  });
}

function safeText(body) {
  try {
    const text = JSON.parse(body).text;
    return typeof text === "string" && text.trim() ? text.trim() : null;
  } catch {
    return null;
  }
}

function send(res, status, data) {
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(data));
}
