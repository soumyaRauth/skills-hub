import { useTranslation } from "react-i18next";

export function InvoiceList({ invoices, overdueCount }) {
  const { t } = useTranslation();

  return (
    <section>
      <h2>{t("invoice.title")}</h2>
      <p>{t("invoice.invoice", { count: invoices.length })}</p>
      {overdueCount > 0 && <p className="warn">{t("invoice.overdue", { count: overdueCount })}</p>}

      <ul>
        {invoices.map((invoice) => (
          <li key={invoice.id}>
            <span>{invoice.number}</span>
            <span>{"$" + invoice.amount.toFixed(2)}</span>
            <span>{new Date(invoice.issuedAt).toLocaleDateString("en-US")}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
