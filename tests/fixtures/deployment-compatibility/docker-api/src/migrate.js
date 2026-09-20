const { pool } = require("./db");

async function main() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS invoices (
      id TEXT PRIMARY KEY,
      amount_cents INTEGER NOT NULL,
      currency TEXT NOT NULL DEFAULT 'USD'
    )
  `);
  await pool.query("ALTER TABLE invoices ADD COLUMN IF NOT EXISTS issued_at TIMESTAMPTZ");
  await pool.end();
}

main();
