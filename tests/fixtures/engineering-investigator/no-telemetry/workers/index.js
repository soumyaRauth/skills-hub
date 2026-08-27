const { Worker } = require("bullmq");
const { finalizeInvoice } = require("../src/services/invoice");

const connection = { url: process.env.REDIS_URL };

new Worker(
  "default",
  async (job) => {
    if (job.name === "finalize-invoice") return finalizeInvoice(job.data.invoiceId);
    throw new Error(`unknown job ${job.name}`);
  },
  { connection, concurrency: 4 }
);
