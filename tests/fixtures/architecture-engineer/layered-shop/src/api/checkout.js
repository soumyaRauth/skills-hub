const express = require("express");
const { db } = require("../infrastructure/db");

const router = express.Router();

router.post("/checkout/quote", async (req, res) => {
  const customer = await db("customers").where({ id: req.user.id }).first();
  const subtotal = req.body.items.reduce((s, i) => s + i.priceCents * i.qty, 0);

  let total = subtotal;
  if (customer.tier === "gold") total = Math.round(subtotal * 0.9);
  else if (customer.tier === "silver") total = Math.round(subtotal * 0.95);

  res.json({ subtotalCents: subtotal, totalCents: total });
});

module.exports = router;
