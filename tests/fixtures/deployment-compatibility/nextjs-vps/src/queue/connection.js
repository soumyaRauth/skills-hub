const IORedis = require("ioredis");
const { Queue } = require("bullmq");

// Opened at module load: every process that requires this file needs Redis
// before it can serve anything.
const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null,
});

const queue = new Queue("emails", { connection });

module.exports = { connection, queue };
