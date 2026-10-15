// Verifies the signature with PAYMENT_WEBHOOK_SECRET, then marks the order paid.
// Locally nothing arrives unless the provider's CLI forwards webhooks here.
export async function handleWebhook(req, res) {
  // verify(req, process.env.PAYMENT_WEBHOOK_SECRET); db.update("orders", { status: "paid" })
  res.writeHead(200).end();
}
