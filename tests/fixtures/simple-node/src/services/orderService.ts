import type { Order } from "../models/order.js";

/** Minutes after placement during which a customer may cancel. */
export const CANCELLATION_WINDOW_MINUTES = 15;

export function canCancel(order: Order, now: Date = new Date()): boolean {
  if (order.status !== "pending" && order.status !== "paid") {
    return false;
  }
  const elapsedMinutes = (now.getTime() - order.placedAt.getTime()) / 60_000;
  return elapsedMinutes < CANCELLATION_WINDOW_MINUTES;
}

export function cancel(order: Order, now: Date = new Date()): Order {
  if (!canCancel(order, now)) {
    throw new Error("Order can no longer be cancelled");
  }
  return { ...order, status: "cancelled" };
}
