const db = require("../db");

async function serializeCart(cart) {
  const items = [];

  for (const item of cart.items) {
    const wrap = await db.query(
      "SELECT * FROM gift_wrap_options WHERE product_id = $1",
      [item.productId]
    );

    items.push({
      productId: item.productId,
      name: item.name,
      quantity: item.quantity,
      unitPrice: item.unitPrice,
      giftWrapOptions: wrap.rows.map((w) => ({ id: w.id, label: w.label, price: w.price }))
    });
  }

  return { id: cart.id, items, subtotal: cart.subtotal, currency: cart.currency };
}

module.exports = { serializeCart };
