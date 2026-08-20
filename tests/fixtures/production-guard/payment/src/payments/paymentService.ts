import { db } from "../db.js";
import { provider } from "./provider.js";

export interface PayResult {
  paymentId: string;
  status: "succeeded" | "failed";
}

/**
 * Charges the saved card for an invoice and marks the invoice paid.
 */
export async function payInvoice(
  invoiceId: string,
  userId: string,
): Promise<PayResult> {
  const invoice = await db.invoices.find(invoiceId);
  if (!invoice) throw new Error("invoice_not_found");
  if (invoice.userId !== userId) throw new Error("forbidden");

  return db.transaction(async (tx) => {
    const charge = await provider.charge({
      amount: invoice.amountCents,
      currency: invoice.currency,
      customerId: invoice.customerId,
    });

    const payment = await tx.payments.create({
      invoiceId,
      providerChargeId: charge.id,
      amountCents: invoice.amountCents,
      status: "succeeded",
    });

    await tx.invoices.update(invoiceId, { status: "paid", paidAt: new Date() });

    return { paymentId: payment.id, status: "succeeded" };
  });
}
