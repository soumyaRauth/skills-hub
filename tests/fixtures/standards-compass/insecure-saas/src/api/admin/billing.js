const { requireAuth } = require('../../middleware/auth')
const prisma = require('../../lib/db')

module.exports = (app) => {
  app.get('/api/admin/billing/:orgId', requireAuth, async (req, res) => {
    const invoices = await prisma.invoice.findMany({
      where: { organizationId: req.params.orgId },
    })
    res.json(invoices)
  })
}
