const db = require('../db');

async function getInvoices(req, res) {
  const { user } = req;

  // Billing is owner-only.
  if (user.role !== 'owner') {
    return res.status(403).json({ error: 'forbidden' });
  }

  return res.json(
    await db.query('SELECT * FROM invoices WHERE organization_id = $1', [user.organization_id]),
  );
}

async function approveRefund(req, res) {
  const { user } = req;

  const allowed =
    user.role === 'owner' ||
    (user.role === 'manager' && req.body.amount_cents <= 5000) ||
    user.role === 'admin';

  if (!allowed) return res.status(403).json({ error: 'forbidden' });

  await db.query(
    'INSERT INTO refunds (organization_id, amount_cents, approved_by) VALUES ($1, $2, $3)',
    [req.body.organization_id, req.body.amount_cents, user.id],
  );
  return res.json({ ok: true });
}

module.exports = { getInvoices, approveRefund };
