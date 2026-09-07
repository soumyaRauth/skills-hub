const { requireAuth } = require('../../middleware/auth')
const prisma = require('../../lib/db')

module.exports = (app) => {
  app.get('/api/admin/exports/customers', requireAuth, async (req, res) => {
    const customers = await prisma.customer.findMany()
    const csv = customers
      .map((c) => [c.id, c.name, c.email, c.phone, c.address].join(','))
      .join('\n')
    res.type('text/csv').send(csv)
  })
}
