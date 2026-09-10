const db = require('./db');
const { can } = require('./permissions');

const SORTABLE = ['name', 'plan', 'status', 'created_at', 'last_seen_at'];

async function list(actor, { q, plan, status, region, since, sort }) {
  const where = ['deleted_at IS NULL'];
  const args = [];
  if (q) { args.push(`%${q}%`); where.push(`email ILIKE $${args.length}`); }
  if (plan) { args.push(plan); where.push(`plan = $${args.length}`); }
  if (status) { args.push(status); where.push(`status = $${args.length}`); }
  if (region) { args.push(region); where.push(`region = $${args.length}`); }
  if (since) { args.push(since); where.push(`created_at >= $${args.length}`); }
  const order = SORTABLE.includes(sort) ? sort : 'created_at';
  return db.query(
    `SELECT * FROM customers WHERE ${where.join(' AND ')} ORDER BY ${order} DESC`,
    args
  );
}

async function bulkDeactivate(actor, ids) {
  if (!can(actor, 'bulk')) throw new Error('forbidden');
  await db.query("UPDATE customers SET status = 'inactive' WHERE id = ANY($1)", [ids]);
}

async function bulkDelete(actor, ids) {
  if (!can(actor, 'bulk')) throw new Error('forbidden');
  await db.query('DELETE FROM customers WHERE id = ANY($1)', [ids]);
}

async function reassign(actor, customerId, staffId) {
  if (!can(actor, 'reassign')) throw new Error('forbidden');
  await db.query('UPDATE customers SET owner_staff_id = $2 WHERE id = $1', [customerId, staffId]);
}

module.exports = { list, bulkDeactivate, bulkDelete, reassign, SORTABLE };
