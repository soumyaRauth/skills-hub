const db = require('../db');

// System total for a period counts approved adjustments only.
async function systemTotal(warehouseId, period) {
  const rows = await db.query(
    `SELECT COALESCE(SUM(delta), 0) AS total
       FROM adjustments
      WHERE warehouse_id = $1
        AND state = 'approved'
        AND date_trunc('month', approved_at) = $2`,
    [warehouseId, period],
  );
  return Number(rows[0].total);
}

async function openPeriod(warehouseId, period, countedTotal) {
  const system = await systemTotal(warehouseId, period);
  return db.insert('reconciliations', {
    warehouse_id: warehouseId,
    period,
    counted_total: countedTotal,
    system_total: system,
  });
}

module.exports = { systemTotal, openPeriod };
