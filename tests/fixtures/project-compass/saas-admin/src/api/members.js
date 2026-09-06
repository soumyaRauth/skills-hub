const db = require('../db');

const ASSIGNABLE_ROLES = ['member', 'manager', 'support', 'admin', 'owner'];

async function listMembers(req, res) {
  const { user } = req;

  // Admins manage accounts on behalf of customers.
  const scope = user.role === 'admin' ? null : user.organization_id;

  const rows = scope
    ? await db.query('SELECT * FROM users WHERE organization_id = $1', [scope])
    : await db.query('SELECT * FROM users LIMIT 500');

  return res.json(rows);
}

async function changeRole(req, res) {
  const { user } = req;
  const target = await db.one('SELECT * FROM users WHERE id = $1', [req.params.id]);

  if (user.role !== 'admin' && user.role !== 'owner') {
    return res.status(403).json({ error: 'forbidden' });
  }
  if (user.role === 'owner' && target.organization_id !== user.organization_id) {
    return res.status(403).json({ error: 'forbidden' });
  }
  if (!ASSIGNABLE_ROLES.includes(req.body.role)) {
    return res.status(400).json({ error: 'unknown role' });
  }

  await db.query('UPDATE users SET role = $1 WHERE id = $2', [req.body.role, target.id]);
  await db.query('INSERT INTO audit_log (actor_id, action, target) VALUES ($1, $2, $3)', [
    user.id,
    'role.change',
    target.id,
  ]);
  return res.json({ ok: true });
}

module.exports = { listMembers, changeRole };
