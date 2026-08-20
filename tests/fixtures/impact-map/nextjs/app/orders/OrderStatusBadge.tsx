"use client";

import type { OrderResponse } from "../../types/order";

const LABELS: Record<string, string> = {
  pending: "Awaiting payment",
  paid: "Paid",
  cancelled: "Cancelled",
  shipped: "Shipped",
};

export function OrderStatusBadge({ order }: { order: OrderResponse }) {
  switch (order.state) {
    case "cancelled":
      return <span className="badge badge--muted">{LABELS[order.state]}</span>;
    case "shipped":
      return <span className="badge badge--success">{LABELS[order.state]}</span>;
    default:
      return <span className="badge">{LABELS[order.state]}</span>;
  }
}
