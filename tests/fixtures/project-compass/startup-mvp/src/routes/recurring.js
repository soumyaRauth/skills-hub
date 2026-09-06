const db = require('../db');

// Schedules can be created and listed. Nothing runs them yet.
async function createSchedule(req, res) {
  const row = await db.insert('recurring_schedules', { ...req.body, user_id: req.user.id });
  return res.json(row);
}

async function listSchedules(req, res) {
  return res.json(
    await db.query('SELECT * FROM recurring_schedules WHERE user_id = $1', [req.user.id]),
  );
}

module.exports = { createSchedule, listSchedules };
