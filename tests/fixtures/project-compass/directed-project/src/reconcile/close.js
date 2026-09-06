const db = require('../db');

async function closePeriod(reconciliationId) {
  const rec = await db.one('SELECT * FROM reconciliations WHERE id = $1', [reconciliationId]);
  if (rec.closed_at) return { ok: true, alreadyClosed: true };

  await db.query('UPDATE reconciliations SET closed_at = now() WHERE id = $1', [rec.id]);
  return { ok: true, variance: rec.counted_total - rec.system_total };
}

module.exports = { closePeriod };
