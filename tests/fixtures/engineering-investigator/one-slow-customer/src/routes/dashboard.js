const express = require("express");
const db = require("../db");

const router = express.Router();

// Returns the full 12-month activity series for every site the tenant owns.
// The client renders three charts from it and discards the rest.
router.get("/api/dashboard", async (req, res) => {
  const tenantId = req.tenant.id;

  const sites = await db("sites").where({ tenant_id: tenantId });
  const series = await db("daily_metrics")
    .whereIn("site_id", sites.map((s) => s.id))
    .where("day", ">=", db.raw("now() - interval '12 months'"))
    .orderBy("day", "asc");

  res.json({
    sites,
    series,
    generatedAt: new Date().toISOString()
  });
});

module.exports = router;
