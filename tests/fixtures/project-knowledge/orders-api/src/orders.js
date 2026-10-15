import { enqueue } from "./queue.js";

// Orders are created "pending". Only the provider's webhook marks them paid —
// a successful charge response is not proof the money moved.
export async function createOrder(req, res) {
  const id = crypto.randomUUID();
  // db.insert("orders", { id, status: "pending" })
  await enqueue("charge", { orderId: id });
  res.writeHead(201, { "content-type": "application/json" }).end(JSON.stringify({ id, status: "pending" }));
}
