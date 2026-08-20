import { payInvoice } from "./paymentService.js";

interface Request {
  params: { invoiceId: string };
  user: { id: string };
  headers: Record<string, string | undefined>;
}
interface Response {
  status(code: number): Response;
  json(body: unknown): void;
}

export async function pay(req: Request, res: Response): Promise<void> {
  try {
    const result = await payInvoice(req.params.invoiceId, req.user.id);
    res.status(200).json(result);
  } catch (err) {
    res.status(500).json({ error: "payment_failed" });
  }
}
