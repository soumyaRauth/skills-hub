const sgMail = require("@sendgrid/mail");
const { renderTemplate } = require("../templates");

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendOrderEmail({ orderId, email, locale }) {
  const html = await renderTemplate("order-confirmation", { orderId, locale });

  const [response] = await sgMail.send({
    to: email,
    from: process.env.MAIL_FROM,
    subject: `Your order ${orderId}`,
    html
  });

  return { messageId: response.headers["x-message-id"] };
}

module.exports = { sendOrderEmail };
