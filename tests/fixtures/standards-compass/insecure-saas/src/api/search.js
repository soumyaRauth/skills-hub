const prisma = require('../lib/db')
const { requireAuth } = require('../middleware/auth')

module.exports = (app) => {
  app.get('/api/search', requireAuth, async (req, res) => {
    const rows = await prisma.$queryRawUnsafe(
      `SELECT id, name, email FROM customers WHERE name LIKE '%${req.query.q}%'`
    )
    res.json(rows)
  })
}
