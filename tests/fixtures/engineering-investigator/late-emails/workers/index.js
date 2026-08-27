const { Worker } = require("bullmq");
const { sendOrderEmail } = require("../src/jobs/sendOrderEmail");
const { renderInvoicePdf } = require("../src/jobs/renderInvoicePdf");

const connection = { url: process.env.REDIS_URL };

const worker = new Worker(
  "default",
  async (job) => {
    switch (job.name) {
      case "send-order-email":
        return sendOrderEmail(job.data);
      case "render-invoice-pdf":
        return renderInvoicePdf(job.data);
      default:
        throw new Error(`unknown job ${job.name}`);
    }
  },
  {
    connection,
    concurrency: 6,
    settings: {
      backoffStrategies: {}
    }
  }
);

module.exports = { worker };
