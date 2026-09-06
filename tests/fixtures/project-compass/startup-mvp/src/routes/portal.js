const db = require('../db');

// Client-facing view of an invoice. No session — the portal key is the auth.
async function viewInvoice(req, res) {
  const invoice = await db.one('SELECT * FROM invoices WHERE id = $1', [req.params.id]);
  return res.json(invoice);
}

async function listClientInvoices(req, res) {
  const client = await db.one('SELECT * FROM clients WHERE portal_key = $1', [req.params.key]);
  return res.json(await db.query('SELECT * FROM invoices WHERE client_id = $1', [client.id]));
}

module.exports = { viewInvoice, listClientInvoices };
