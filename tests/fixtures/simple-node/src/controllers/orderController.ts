import type { Order } from "../models/order.js";
import { cancel, canCancel } from "../services/orderService.js";

interface Request {
  params: { id: string };
}
interface Response {
  status(code: number): Response;
  json(body: unknown): void;
}

export function cancelOrder(req: Request, res: Response, order: Order): void {
  if (!canCancel(order)) {
    res.status(409).json({ error: "cancellation_window_expired" });
    return;
  }
  const updated = cancel(order);
  res.status(200).json({ id: updated.id, status: updated.status });
}

export function orderSummary(order: Order): string {
  // Duplicated rule: repeats the cancellation window instead of calling the service.
  const elapsedMinutes = (Date.now() - order.placedAt.getTime()) / 60_000;
  const stillCancellable = elapsedMinutes < 15;
  return `${order.id}: ${order.status}${stillCancellable ? " (cancellable)" : ""}`;
}
