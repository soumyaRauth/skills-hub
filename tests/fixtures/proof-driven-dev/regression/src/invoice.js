import { formatCurrency, formatDate } from './format.js';

export function renderInvoice(invoice) {
  const lines = invoice.lineItems.map(
    (item) => `${item.description}  ${formatCurrency(item.amountCents)}`,
  );
  const total = invoice.lineItems.reduce((sum, item) => sum + item.amountCents, 0);

  return [
    `INVOICE ${invoice.number}`,
    `Issued ${formatDate(invoice.issuedAt)}`,
    ...lines,
    `Total   ${formatCurrency(total)}`,
  ].join('\n');
}
