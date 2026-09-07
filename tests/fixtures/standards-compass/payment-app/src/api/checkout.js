const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY)
const { requireAuth } = require('../middleware/auth')

module.exports = (app) => {
  app.post('/api/checkout', requireAuth, async (req, res) => {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      customer_email: req.user.email,
      line_items: [{ price: req.body.priceId, quantity: 1 }],
      success_url: process.env.APP_URL + '/billing/done',
      cancel_url: process.env.APP_URL + '/billing',
    })
    res.json({ url: session.url })
  })
}
