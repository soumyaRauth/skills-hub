const db = require('../db');

async function cancelOrder(orderId, reason) {
  const order = await db.one('SELECT * FROM orders WHERE id = $1', [orderId]);

  if (order.is_cancelled) return { ok: true, alreadyCancelled: true };

  await db.query('UPDATE orders SET is_cancelled = true, cancelled_at = now() WHERE id = $1', [
    order.id,
  ]);

  return { ok: true, reason };
}

module.exports = { cancelOrder };
