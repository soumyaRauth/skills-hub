import { db } from "../db.js";
import { sendReceipt } from "./receipts.js";

interface WebhookRequest {
  body: {
    id: string;
    type: string;
    data: { object: { id: string; metadata: { invoiceId: string } } };
  };
  headers: Record<string, string | undefined>;
}
interface Response {
  status(code: number): Response;
  json(body: unknown): void;
}

export async function handle(req: WebhookRequest, res: Response): Promise<void> {
  const event = req.body;

  if (event.type === "payment_intent.succeeded") {
    const invoiceId = event.data.object.metadata.invoiceId;
    await db.invoices.update(invoiceId, { status: "paid", paidAt: new Date() });
    await sendReceipt(invoiceId);
  }

  res.status(200).json({ received: true });
}
