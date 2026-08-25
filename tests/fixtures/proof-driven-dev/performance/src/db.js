// A fake datastore with a query counter. Query count is the deterministic
// measurement in this fixture — wall-clock time on a laptop is not.

const customers = new Map();
const orders = [];
export const stats = { queries: 0 };

for (let i = 1; i <= 200; i++) {
  customers.set(i, { id: i, name: `Customer ${i}`, tier: i % 5 === 0 ? 'gold' : 'standard' });
}
for (let i = 1; i <= 500; i++) {
  orders.push({ id: i, customerId: (i % 200) + 1, totalCents: 1000 + i * 7, status: i % 9 === 0 ? 'refunded' : 'paid' });
}

export function resetStats() {
  stats.queries = 0;
}

export function findOrders({ status } = {}) {
  stats.queries++;
  return orders.filter((o) => !status || o.status === status).map((o) => ({ ...o }));
}

export function findCustomer(id) {
  stats.queries++;
  return { ...customers.get(id) };
}

export function findCustomersByIds(ids) {
  stats.queries++;
  return ids.map((id) => ({ ...customers.get(id) })).filter(Boolean);
}
