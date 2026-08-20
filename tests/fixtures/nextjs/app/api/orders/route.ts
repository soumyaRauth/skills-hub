import type { OrderResponse } from "../../../types/order";

const orders = [
  { id: "ord_1", status: "pending" as const, totalCents: 2500 },
  { id: "ord_2", status: "shipped" as const, totalCents: 9900 },
];

export async function GET(): Promise<Response> {
  const body: OrderResponse[] = orders.map((o) => ({
    id: o.id,
    state: o.status,
    total: o.totalCents / 100,
  }));
  return Response.json(body);
}
