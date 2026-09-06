const db = require('../db');

async function listTickets(req, res) {
  const { user } = req;

  // Support staff work across accounts, so they see everything.
  if (user.role === 'support') {
    return res.json(await db.query('SELECT * FROM tickets ORDER BY created_at DESC LIMIT 200'));
  }

  const rows = await db.query(
    'SELECT * FROM tickets WHERE organization_id = $1 ORDER BY created_at DESC LIMIT 200',
    [user.organization_id],
  );
  return res.json(rows);
}

async function closeTicket(req, res) {
  const { user } = req;
  const ticket = await db.one('SELECT * FROM tickets WHERE id = $1', [req.params.id]);

  const ownsIt = ticket.author_id === user.id;
  const sameOrg = ticket.organization_id === user.organization_id;

  if (!ownsIt && !(sameOrg && (user.role === 'manager' || user.role === 'admin'))) {
    return res.status(403).json({ error: 'forbidden' });
  }

  await db.query("UPDATE tickets SET status = 'closed' WHERE id = $1", [req.params.id]);
  return res.json({ ok: true });
}

module.exports = { listTickets, closeTicket };
