const { Queue } = require("bullmq");

const queue = new Queue("default", {
  connection: { url: process.env.REDIS_URL },
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: "fixed", delay: 1800000 },
    removeOnComplete: 1000
  }
});

module.exports = { queue };
