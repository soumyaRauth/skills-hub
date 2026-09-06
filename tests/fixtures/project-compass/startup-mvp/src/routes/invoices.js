const db = require('../db');
const { requireUser } = require('../auth');

async function createInvoice(req, res) {
  const invoice = await db.insert('invoices', { ...req.body, user_id: req.user.id });
  return res.json(invoice);
}

async function sendInvoice(req, res) {
  const invoice = await db.one('SELECT * FROM invoices WHERE id = $1', [req.params.id]);
  await require('../mailer').send(invoice.client_id, 'invoice', { invoice });
  await db.query("UPDATE invoices SET status = 'sent', sent_at = now() WHERE id = $1", [invoice.id]);
  return res.json({ ok: true });
}

async function recordPayment(req, res) {
  const invoice = await db.one('SELECT * FROM invoices WHERE id = $1', [req.params.id]);
  const paid = invoice.paid_cents + req.body.amount_cents;

  // TODO: what is this if they only paid part of it?
  await db.query("UPDATE invoices SET paid_cents = $1, status = 'paid' WHERE id = $2", [
    paid,
    invoice.id,
  ]);
  return res.json({ ok: true });
}

module.exports = { createInvoice, sendInvoice, recordPayment, requireUser };
