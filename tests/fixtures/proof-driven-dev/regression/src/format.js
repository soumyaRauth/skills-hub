// Shared money formatting. Used by invoices AND receipts — grep before editing.
export function formatCurrency(cents, currency = 'USD') {
  const amount = (cents / 100).toFixed(2);
  const withSeparators = amount.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  const symbol = currency === 'USD' ? '$' : '';
  return `${symbol}${withSeparators}`;
}

export function formatDate(iso) {
  return iso.slice(0, 10);
}
