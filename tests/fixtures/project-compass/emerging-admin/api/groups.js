const db = require('./db');

// A staff group with can_manage lets its members do anything on the console.
async function isManager(staffId) {
  const rows = await db.query(
    `SELECT g.can_manage FROM staff_groups g
       JOIN staff_group_members m ON m.group_id = g.id
      WHERE m.staff_id = $1`,
    [staffId]
  );
  return rows.some((r) => r.can_manage);
}

async function addToGroup(actor, staffId, groupId) {
  if (!(await isManager(actor.id)) && actor.role !== 'admin') {
    throw new Error('forbidden');
  }
  await db.query(
    'INSERT INTO staff_group_members (group_id, staff_id) VALUES ($1, $2)',
    [groupId, staffId]
  );
}

module.exports = { isManager, addToGroup };
