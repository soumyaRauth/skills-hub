const db = require('../db');

// Monthly revenue: completed orders only.
async function monthlyRevenue(month) {
  const rows = await db.query(
    `SELECT SUM(total_cents) AS cents
       FROM orders
      WHERE is_paid = true
        AND is_shipped = true
        AND is_refunded = false
        AND date_trunc('month', created_at) = $1`,
    [month],
  );
  return rows[0].cents || 0;
}

module.exports = { monthlyRevenue };
