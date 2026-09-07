const db = require('../../db/client')

module.exports = (app) => {
  app.post('/api/webhooks/stripe', async (req, res) => {
    const event = req.body

    if (event.type === 'checkout.session.completed') {
      await db.subscription.update({
        where: { stripeCustomerId: event.data.object.customer },
        data: { status: 'active', currentPeriodEnd: event.data.object.expires_at },
      })
    }

    if (event.type === 'invoice.payment_failed') {
      await db.subscription.update({
        where: { stripeCustomerId: event.data.object.customer },
        data: { status: 'past_due' },
      })
    }

    res.json({ received: true })
  })
}
