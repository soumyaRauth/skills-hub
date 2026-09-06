const db = require('../db');
const provider = require('../provider');
const { notifyOrderComplete } = require('../notify');

async function payOrder(orderId, card) {
  const order = await db.one('SELECT * FROM orders WHERE id = $1', [orderId]);
  if (order.is_paid) return { ok: true, alreadyPaid: true };

  const charge = await provider.charge(card, order.total_cents);

  await db.query('INSERT INTO payments (order_id, amount_cents, provider_ref) VALUES ($1,$2,$3)', [
    order.id,
    order.total_cents,
    charge.ref,
  ]);
  await db.query('UPDATE orders SET is_paid = true, paid_at = now() WHERE id = $1', [order.id]);

  await notifyOrderComplete(order.id);
  return { ok: true };
}

module.exports = { payOrder };
