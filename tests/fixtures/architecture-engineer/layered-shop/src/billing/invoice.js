const { db } = require("../infrastructure/db");

async function settleInvoice(orderId, paymentRef) {
  await db("invoices").insert({
    order_id: orderId,
    payment_ref: paymentRef,
    settled_at: new Date(),
  });

  await db("orders").where({ id: orderId }).update({ status: "paid" });
}

module.exports = { settleInvoice };
