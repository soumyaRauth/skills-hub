const { requireAuth } = require('../../middleware/auth')
const { refund } = require('../../services/refund')

module.exports = (app) => {
  app.post('/api/admin/refunds', requireAuth, async (req, res) => {
    const result = await refund(req.body.chargeId, req.body.amountCents)
    res.json(result)
  })
}
