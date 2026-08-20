import type { OrderResponse } from "../../types/order";
import { OrderStatusBadge } from "./OrderStatusBadge";

async function getOrders(): Promise<OrderResponse[]> {
  const res = await fetch("http://localhost:3000/api/orders", {
    cache: "no-store",
  });
  return res.json();
}

export default async function OrdersPage() {
  const orders = await getOrders();
  return (
    <ul>
      {orders.map((order) => (
        <li key={order.id}>
          {order.id} — <OrderStatusBadge order={order} /> — ${order.total}
        </li>
      ))}
    </ul>
  );
}
