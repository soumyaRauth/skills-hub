const db = require('../db');
const provider = require('../provider');

async function refundOrder(orderId) {
  const order = await db.one('SELECT * FROM orders WHERE id = $1', [orderId]);

  if (!order.is_paid) throw new Error('cannot refund an unpaid order');

  const payment = await db.one('SELECT * FROM payments WHERE order_id = $1', [order.id]);
  await provider.refund(payment.provider_ref, order.total_cents);

  await db.query('INSERT INTO refunds (order_id, amount_cents) VALUES ($1, $2)', [
    order.id,
    order.total_cents,
  ]);
  await db.query('UPDATE orders SET is_refunded = true WHERE id = $1', [order.id]);

  return { ok: true };
}

module.exports = { refundOrder };
