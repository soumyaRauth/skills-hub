const { Worker } = require("bullmq");
const { connection } = require("./connection");
const { sendOrderEmail } = require("../mailer");

new Worker(
  "emails",
  async (job) => {
    await sendOrderEmail(job.data.to, job.data.orderId);
  },
  { connection, concurrency: 5 }
);
