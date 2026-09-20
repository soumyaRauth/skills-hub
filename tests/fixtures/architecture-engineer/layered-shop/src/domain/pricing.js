function applyDiscount(totalCents, customer) {
  if (customer.tier === "gold") return Math.round(totalCents * 0.9);
  if (customer.tier === "silver") return Math.round(totalCents * 0.95);
  return totalCents;
}

module.exports = { applyDiscount };
