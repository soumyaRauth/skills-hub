import { findOrders, findCustomer } from './db.js';

// Builds the paid-orders report. findCustomersByIds() exists in db.js and is
// unused here.
export function buildOrderReport() {
  const orders = findOrders({ status: 'paid' });

  const rows = orders.map((order) => {
    const customer = findCustomer(order.customerId);
    return {
      orderId: order.id,
      customer: customer.name,
      tier: customer.tier,
      totalCents: order.totalCents,
    };
  });

  return {
    rows,
    orderCount: rows.length,
    totalCents: rows.reduce((sum, row) => sum + row.totalCents, 0),
  };
}
