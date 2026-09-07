const crypto = require('crypto')
const prisma = require('../lib/db')
const log = require('../lib/log')

module.exports = (app) => {
  app.post('/api/auth/reset-request', async (req, res) => {
    const user = await prisma.user.findUnique({ where: { email: req.body.email } })
    if (!user) {
      return res.status(404).json({ error: 'no account with that email' })
    }
    const token = crypto.randomBytes(16).toString('hex')
    await prisma.passwordReset.create({ data: { userId: user.id, token } })
    log.info(`password reset requested for ${user.email}, token ${token}`)
    res.json({ ok: true })
  })

  app.post('/api/auth/reset', async (req, res) => {
    const reset = await prisma.passwordReset.findFirst({ where: { token: req.body.token } })
    if (!reset) return res.status(400).json({ error: 'invalid token' })
    const hash = crypto.createHash('md5').update(req.body.password).digest('hex')
    await prisma.user.update({ where: { id: reset.userId }, data: { passwordHash: hash } })
    res.json({ ok: true })
  })
}
