const nodemailer = require("nodemailer");

const transport = nodemailer.createTransport(process.env.SMTP_URL);

async function sendOrderEmail(to, orderId) {
  return transport.sendMail({
    from: process.env.MAIL_FROM || "orders@example.com",
    to,
    subject: `Order ${orderId}`,
    text: `Your order ${orderId} has been received.`,
  });
}

module.exports = { sendOrderEmail };
