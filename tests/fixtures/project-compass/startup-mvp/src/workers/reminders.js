const db = require('../db');
const mailer = require('../mailer');

// Written 3 weeks ago. Not wired into any scheduler.
async function sendOverdueReminders() {
  const overdue = await db.query(
    "SELECT * FROM invoices WHERE status = 'sent' AND due_at < now()",
  );
  for (const invoice of overdue) {
    await mailer.send(invoice.client_id, 'overdue', { invoice });
  }
}

module.exports = { sendOverdueReminders };
