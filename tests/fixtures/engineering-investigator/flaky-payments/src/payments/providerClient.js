const { request } = require("undici");

const BASE_URL = process.env.PAYMENTS_BASE_URL;
const TIMEOUT_MS = 30000;

async function authorize({ orderId, amountCents, currency, token, idempotencyKey }) {
  const response = await request(`${BASE_URL}/v2/authorizations`, {
    method: "POST",
    headersTimeout: TIMEOUT_MS,
    bodyTimeout: TIMEOUT_MS,
    headers: {
      authorization: `Bearer ${process.env.PAYMENTS_API_KEY}`,
      "idempotency-key": idempotencyKey,
      "content-type": "application/json"
    },
    body: JSON.stringify({ order_id: orderId, amount: amountCents, currency, token })
  });

  const body = await response.body.json();

  if (response.statusCode >= 400) {
    const error = new Error(body.message || "authorization failed");
    error.providerStatus = response.statusCode;
    error.providerRequestId = body.request_id;
    throw error;
  }

  return body;
}

module.exports = { authorize };
