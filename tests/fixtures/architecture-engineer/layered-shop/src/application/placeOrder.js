const { db } = require("../infrastructure/db");
const { applyDiscount } = require("../domain/pricing");
const { publish } = require("../events/publisher");

async function placeOrder(customer, items) {
  const subtotal = items.reduce((sum, i) => sum + i.priceCents * i.qty, 0);
  const total = applyDiscount(subtotal, customer);

  const [row] = await db("orders")
    .insert({
      customer_id: customer.id,
      status: "placed",
      total_cents: total,
      placed_at: new Date(),
    })
    .returning("*");

  await publish("order.placed", { orderId: row.id, totalCents: total });
  return row;
}

module.exports = { placeOrder };
