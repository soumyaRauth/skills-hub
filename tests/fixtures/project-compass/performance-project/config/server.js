module.exports = {
  port: process.env.PORT || 3000,

  // Raised from 30s — report generation was hitting the limit.
  requestTimeoutMs: 120000,

  db: {
    connectionString: process.env.DATABASE_URL,
    max: 20,
  },
};
