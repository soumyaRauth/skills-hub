import { test } from "node:test";
import assert from "node:assert/strict";
import { createApp } from "../src/app.js";

async function withServer(fn) {
  const server = createApp().listen(0);
  await new Promise((r) => server.once("listening", r));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    await fn(base);
  } finally {
    server.close();
  }
}

test("health answers 200", () =>
  withServer(async (base) => {
    const res = await fetch(`${base}/health`);
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { ok: true });
  }));

test("a note can be created and listed", () =>
  withServer(async (base) => {
    const created = await fetch(`${base}/notes`, {
      method: "POST",
      body: JSON.stringify({ text: "ship it" }),
    });
    assert.equal(created.status, 201);
    const list = await (await fetch(`${base}/notes`)).json();
    assert.equal(list.at(-1).text, "ship it");
  }));

test("an empty note is rejected", () =>
  withServer(async (base) => {
    const res = await fetch(`${base}/notes`, { method: "POST", body: "{}" });
    assert.equal(res.status, 400);
  }));
