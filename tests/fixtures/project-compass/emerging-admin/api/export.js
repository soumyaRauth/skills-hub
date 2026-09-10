const db = require('./db');
const { isManager } = require('./groups');

// Export bypasses permissions.can() and asks the group table instead.
async function exportCustomers(actor, filters) {
  if (actor.role !== 'admin' && !(await isManager(actor.id))) {
    throw new Error('forbidden');
  }
  const rows = await db.query('SELECT * FROM customers');
  const header = Object.keys(rows[0] || {}).join(',');
  return [header, ...rows.map((r) => Object.values(r).join(','))].join('\n');
}

module.exports = { exportCustomers };
