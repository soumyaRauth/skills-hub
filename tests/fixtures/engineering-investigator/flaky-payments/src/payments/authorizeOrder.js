const { authorize } = require("./providerClient");
const logger = require("../logger");

async function authorizeOrder(order) {
  const idempotencyKey = `order-${order.id}-auth`;

  try {
    const result = await authorize({
      orderId: order.id,
      amountCents: order.totalCents,
      currency: order.currency,
      token: order.paymentToken,
      idempotencyKey
    });

    await order.markAuthorized(result.authorization_id);
    return { ok: true };
  } catch (err) {
    logger.warn("payment_authorize_failed", {
      order_id: order.id,
      provider_status: err.providerStatus,
      provider_request_id: err.providerRequestId,
      error: err.message
    });

    await order.markFailed(err.message);
    return { ok: false, error: err.message };
  }
}

module.exports = { authorizeOrder };
