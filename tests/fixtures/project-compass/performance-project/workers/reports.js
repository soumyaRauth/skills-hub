const db = require('../src/db');

async function buildMonthlyReport(org, month) {
  const rows = await db.query(
    `SELECT a.id, a.created_at, a.amount_cents, w.name AS warehouse, p.sku, u.email
       FROM adjustments a
       JOIN warehouses w ON w.id = a.warehouse_id
       JOIN products   p ON p.id = a.product_id
       JOIN users      u ON u.id = a.created_by
       JOIN organizations o ON o.id = a.organization_id
      WHERE a.organization_id = $1
        AND a.created_at >= $2
        AND a.created_at <  ($2::date + interval '1 month')`,
    [org, month],
  );

  return {
    month,
    count: rows.length,
    total_cents: rows.reduce((sum, r) => sum + r.amount_cents, 0),
    rows,
  };
}

module.exports = { buildMonthlyReport };
