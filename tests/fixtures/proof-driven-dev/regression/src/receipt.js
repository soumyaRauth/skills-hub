import { formatCurrency, formatDate } from './format.js';

// The customer-facing email receipt. Its wording and formatting are asserted
// character-for-character by the existing suite.
export function renderReceipt(payment) {
  return [
    `Thanks for your payment of ${formatCurrency(payment.amountCents)}.`,
    `Paid ${formatDate(payment.paidAt)} with card ending ${payment.last4}.`,
  ].join('\n');
}
