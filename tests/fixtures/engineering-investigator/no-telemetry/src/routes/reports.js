const express = require("express");
const prisma = require("../prisma");

const router = express.Router();

router.get("/api/reports/activity", async (req, res) => {
  const events = await prisma.activityEvent.findMany({
    where: { organizationId: req.user.organizationId },
    include: { user: true, job: true },
    orderBy: { createdAt: "desc" }
  });

  res.json({ events: events.map(serialize) });
});

function serialize(event) {
  return {
    id: event.id,
    type: event.type,
    at: event.createdAt,
    user: event.user ? { id: event.user.id, name: event.user.name } : null,
    job: event.job ? { id: event.job.id, reference: event.job.reference } : null
  };
}

module.exports = router;
