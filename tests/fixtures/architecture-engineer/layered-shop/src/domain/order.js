const { db } = require("../infrastructure/db");

const CANCELLATION_WINDOW_MINUTES = 15;

class Order {
  constructor(row) {
    this.id = row.id;
    this.status = row.status;
    this.placedAt = new Date(row.placed_at);
    this.totalCents = row.total_cents;
  }

  canCancel(now = new Date()) {
    const elapsed = (now - this.placedAt) / 60000;
    return this.status === "placed" && elapsed < CANCELLATION_WINDOW_MINUTES;
  }

  static async find(id) {
    const row = await db("orders").where({ id }).first();
    return row ? new Order(row) : null;
  }

  async save() {
    await db("orders").where({ id: this.id }).update({ status: this.status });
  }
}

module.exports = { Order, CANCELLATION_WINDOW_MINUTES };
