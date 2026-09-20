const express = require("express");
const { db } = require("../infrastructure/db");
const { placeOrder } = require("../application/placeOrder");

const router = express.Router();

router.post("/orders", async (req, res) => {
  const order = await placeOrder(req.user, req.body.items);
  res.status(201).json(order);
});

// Cancellation rule lives here as well as in domain/order.js.
router.post("/orders/:id/cancel", async (req, res) => {
  const order = await db("orders").where({ id: req.params.id }).first();
  const elapsedMinutes = (Date.now() - new Date(order.placed_at)) / 60000;

  if (order.status !== "placed" || elapsedMinutes >= 15) {
    return res.status(409).json({ error: "cannot_cancel" });
  }

  await db("orders").where({ id: order.id }).update({ status: "cancelled" });
  res.json({ ok: true });
});

module.exports = router;
