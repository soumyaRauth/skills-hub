const express = require("express");
const prisma = require("../prisma");

const router = express.Router();

router.get("/api/customers", async (req, res) => {
  const customers = await prisma.customer.findMany({
    where: { organizationId: req.user.organizationId },
    include: { sites: true, contacts: true }
  });

  res.json({ customers });
});

module.exports = router;
