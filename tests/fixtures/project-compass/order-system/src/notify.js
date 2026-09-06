const db = require('./db');
const mailer = require('./mailer');

// "Your order is complete" — sent once payment lands.
async function notifyOrderComplete(orderId) {
  const order = await db.one('SELECT * FROM orders WHERE id = $1', [orderId]);
  if (!order.is_paid) return;

  await mailer.send(order.customer_id, 'order-complete', {
    orderId: order.id,
    total: order.total_cents,
  });
}

module.exports = { notifyOrderComplete };
