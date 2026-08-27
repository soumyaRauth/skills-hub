const { Pool } = require("pg");

const pool = new Pool({ max: 10 });

async function query(sql, params) {
  const started = Date.now();
  const result = await pool.query(sql, params);
  return { rows: result.rows, ms: Date.now() - started };
}

module.exports = { query };
