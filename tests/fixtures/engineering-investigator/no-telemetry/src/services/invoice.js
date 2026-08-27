const Stripe = require("stripe");
const prisma = require("../prisma");

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

async function finalizeInvoice(invoiceId) {
  const invoice = await prisma.invoice.findUnique({ where: { id: invoiceId } });

  const paymentIntent = await stripe.paymentIntents.create({
    amount: invoice.totalCents,
    currency: invoice.currency,
    customer: invoice.stripeCustomerId,
    metadata: { invoice_id: invoice.id }
  });

  return prisma.invoice.update({
    where: { id: invoice.id },
    data: { status: "finalized", stripePaymentIntentId: paymentIntent.id }
  });
}

module.exports = { finalizeInvoice };
