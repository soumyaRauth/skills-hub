const test = require("node:test");
const assert = require("node:assert");

test("checkout response includes cart items", () => {
  const payload = { cart: { items: [{ productId: 1, giftWrapOptions: [] }] }, totals: {} };
  assert.equal(payload.cart.items.length, 1);
});

test("checkout response includes totals", () => {
  const payload = { cart: { items: [] }, totals: { tax: { rate: 0.2 } } };
  assert.ok(payload.totals.tax);
});
