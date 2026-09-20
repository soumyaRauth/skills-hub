const express = require("express");
const { pool } = require("./db");

const app = express();

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.get("/invoices", async (req, res) => {
  const { rows } = await pool.query("SELECT id, amount_cents FROM invoices LIMIT 50");
  res.json(rows);
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`billing-api on ${port}`));
