const db = require('../db');

async function shipOrder(orderId, carrier, tracking) {
  const order = await db.one('SELECT * FROM orders WHERE id = $1', [orderId]);

  if (!order.is_paid) throw new Error('cannot ship an unpaid order');

  await db.query('INSERT INTO shipments (order_id, carrier, tracking) VALUES ($1,$2,$3)', [
    order.id,
    carrier,
    tracking,
  ]);
  await db.query('UPDATE orders SET is_shipped = true, shipped_at = now() WHERE id = $1', [
    order.id,
  ]);

  return { ok: true };
}

module.exports = { shipOrder };
