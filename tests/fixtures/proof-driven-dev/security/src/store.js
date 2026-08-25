export const users = [
  { id: 1, email: 'ada@example.com', organizationId: 10 },
  { id: 2, email: 'grace@example.com', organizationId: 10 },
  { id: 3, email: 'lin@example.com', organizationId: 20 },
];

export const invoices = [
  { id: 'inv_100', userId: 1, organizationId: 10, amountCents: 5000, status: 'paid' },
  { id: 'inv_101', userId: 1, organizationId: 10, amountCents: 7500, status: 'open' },
  { id: 'inv_200', userId: 2, organizationId: 10, amountCents: 1200, status: 'paid' },
  { id: 'inv_300', userId: 3, organizationId: 20, amountCents: 9900, status: 'paid' },
];

// No authorization here by design — the data layer is dumb, the API layer
// decides who may see what.
export function findInvoice(id) {
  return invoices.find((invoice) => invoice.id === id) ?? null;
}

export function findInvoicesByUser(userId) {
  return invoices.filter((invoice) => invoice.userId === userId);
}
