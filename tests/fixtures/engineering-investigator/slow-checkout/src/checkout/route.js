const express = require("express");
const db = require("../db");
const { serializeCart } = require("./cartSerializer");

const router = express.Router();

router.post("/checkout", async (req, res) => {
  const cart = await loadCart(req.body.cartId);
  const totals = await calculateTotals(cart);
  const payload = await serializeCart(cart);

  res.json({ cart: payload, totals });
});

async function loadCart(cartId) {
  const cart = await db.query("SELECT * FROM carts WHERE id = $1", [cartId]);
  const items = await db.query("SELECT * FROM cart_items WHERE cart_id = $1", [cartId]);
  return { ...cart.rows[0], items: items.rows };
}

async function calculateTotals(cart) {
  const tax = await db.query("SELECT rate FROM tax_rates WHERE region = $1", [cart.region]);
  const shipping = await db.query("SELECT * FROM shipping_rates WHERE zone = $1", [cart.zone]);
  return { tax: tax.rows[0], shipping: shipping.rows[0] };
}

module.exports = router;
