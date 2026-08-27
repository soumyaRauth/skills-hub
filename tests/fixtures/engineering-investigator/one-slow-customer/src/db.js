const knex = require("knex");

module.exports = knex({
  client: "pg",
  connection: process.env.DATABASE_URL,
  pool: { min: 2, max: 20 }
});
