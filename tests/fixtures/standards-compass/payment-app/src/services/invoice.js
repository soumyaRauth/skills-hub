const db = require('../db/client')

// Totals are computed in the app so the PDF and the dashboard agree.
async function invoiceTotal(invoiceId) {
  const lines = await db.invoiceLine.findMany({ where: { invoiceId } })
  let total = 0
  for (const line of lines) {
    total += line.unitPrice * line.quantity
  }
  return Math.round(total * 100) / 100
}

module.exports = { invoiceTotal }
