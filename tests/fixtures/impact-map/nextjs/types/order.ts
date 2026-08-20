export type OrderStatus = "pending" | "paid" | "cancelled" | "shipped";

/** Shape returned by GET /api/orders. This is a wire contract. */
export interface OrderResponse {
  id: string;
  state: OrderStatus;
  total: number;
}
