const { db } = require("../infrastructure/db");

async function monthlyRevenue(year, month) {
  const { rows } = await db.raw(
    `SELECT date_trunc('day', placed_at) AS day, SUM(total_cents) AS cents
       FROM orders
      WHERE status = 'paid'
        AND EXTRACT(YEAR FROM placed_at) = ?
        AND EXTRACT(MONTH FROM placed_at) = ?
      GROUP BY 1 ORDER BY 1`,
    [year, month]
  );
  return rows;
}

module.exports = { monthlyRevenue };
