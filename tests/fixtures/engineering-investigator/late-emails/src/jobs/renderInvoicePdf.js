const { chromium } = require("playwright");
const { renderTemplate } = require("../templates");

// Renders a PDF invoice by loading the invoice HTML in a headless browser.
async function renderInvoicePdf({ invoiceId }) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const html = await renderTemplate("invoice", { invoiceId });
  await page.setContent(html, { waitUntil: "networkidle" });

  const pdf = await page.pdf({ format: "A4", printBackground: true });
  await browser.close();

  return { bytes: pdf.length };
}

module.exports = { renderInvoicePdf };
