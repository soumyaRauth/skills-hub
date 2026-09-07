const { requireAuth, requireRole } = require('../../middleware/auth')
const prisma = require('../../lib/db')

module.exports = (app) => {
  app.get('/api/admin/users', requireAuth, requireRole('admin'), async (req, res) => {
    const users = await prisma.user.findMany({
      where: { organizationId: req.user.organizationId },
    })
    res.json(users)
  })

  app.post('/api/admin/users/:id/role', requireAuth, requireRole('admin'), async (req, res) => {
    const updated = await prisma.user.update({
      where: { id: req.params.id },
      data: { role: req.body.role },
    })
    res.json(updated)
  })
}
