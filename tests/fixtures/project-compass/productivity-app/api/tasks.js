const db = require('./db');

const BULK_FIELDS = ['status', 'assignee_id', 'priority'];

async function bulkUpdate(req, res) {
  const { ids, patch } = req.body;
  const fields = Object.keys(patch).filter((f) => BULK_FIELDS.includes(f));
  if (fields.length === 0) return res.status(400).json({ error: 'nothing to update' });

  for (const id of ids) {
    for (const f of fields) {
      await db.query(`UPDATE tasks SET ${f} = $1 WHERE id = $2`, [patch[f], id]);
    }
  }
  return res.json({ updated: ids.length });
}

module.exports = { bulkUpdate };
