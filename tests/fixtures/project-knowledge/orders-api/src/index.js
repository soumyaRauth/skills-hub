import http from "node:http";
import { createOrder } from "./orders.js";
import { handleWebhook } from "./payments/webhooks.js";

http.createServer(async (req, res) => {
  if (req.method === "POST" && req.url === "/orders") return createOrder(req, res);
  if (req.method === "POST" && req.url === "/webhooks/payments") return handleWebhook(req, res);
  res.writeHead(404).end();
}).listen(3000);
