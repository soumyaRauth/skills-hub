const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY)
const db = require('../db/client')

async function refund(chargeId, amountCents) {
  const result = await stripe.refunds.create({
    charge: chargeId,
    amount: amountCents,
  })
  await db.payment.update({
    where: { stripeChargeId: chargeId },
    data: { status: 'refunded' },
  })
  return result
}

module.exports = { refund }
