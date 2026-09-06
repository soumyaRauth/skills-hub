const db = require('../db');
const { assertTransition } = require('./state');

async function approveAdjustment(adjustmentId, approver) {
  const adj = await db.one('SELECT * FROM adjustments WHERE id = $1', [adjustmentId]);
  assertTransition(adj.state, 'approved');

  if (approver.role !== 'manager') throw new Error('forbidden');

  await db.query(
    "UPDATE adjustments SET state = 'approved', approved_by = $1, approved_at = now() WHERE id = $2",
    [approver.id, adj.id],
  );
  return { ok: true };
}

module.exports = { approveAdjustment };
