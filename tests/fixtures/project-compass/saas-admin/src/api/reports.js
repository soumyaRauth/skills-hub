const db = require('../db');

// Weekly digest: ticket subjects and volumes per organization.
async function ticketDigest(req, res) {
  const { user } = req;

  if (user.role !== 'admin' && user.role !== 'manager') {
    return res.status(403).json({ error: 'forbidden' });
  }

  const rows = await db.query(
    `SELECT t.subject, t.status, t.created_at
       FROM tickets t
      WHERE t.organization_id = $1
      ORDER BY t.created_at DESC`,
    [user.organization_id],
  );

  return res.json({ organization: user.organization_id, tickets: rows });
}

module.exports = { ticketDigest };
