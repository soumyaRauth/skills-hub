import test from "node:test";
import assert from "node:assert/strict";
import type { Order } from "../src/models/order.js";
import { canCancel, cancel } from "../src/services/orderService.js";

const orderPlacedMinutesAgo = (minutes: number): Order => ({
  id: "ord_1",
  customerId: "cus_1",
  status: "pending",
  placedAt: new Date(Date.now() - minutes * 60_000),
  totalCents: 2500,
});

test("allows cancellation inside the window", () => {
  assert.equal(canCancel(orderPlacedMinutesAgo(5)), true);
});

test("rejects cancellation after the window", () => {
  assert.equal(canCancel(orderPlacedMinutesAgo(16)), false);
});

test("cancel sets the cancelled status", () => {
  assert.equal(cancel(orderPlacedMinutesAgo(1)).status, "cancelled");
});
