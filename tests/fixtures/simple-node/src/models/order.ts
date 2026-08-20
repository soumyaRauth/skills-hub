export type OrderStatus = "pending" | "paid" | "cancelled" | "shipped";

export interface Order {
  id: string;
  customerId: string;
  status: OrderStatus;
  placedAt: Date;
  totalCents: number;
}
