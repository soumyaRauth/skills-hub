import { useTranslation } from "react-i18next";

export function BillingPanel({ subscription }) {
  const { t } = useTranslation();

  const amount = "$" + subscription.amountCents / 100;
  const renews = new Date(subscription.renewsAt).toLocaleDateString("en-US");

  return (
    <section>
      <p>{t("billing.total", { amount })}</p>
      <p>{t("billing.renewsOn", { date: renews })}</p>
      <p>{subscription.seats.toLocaleString("en-US")} seats</p>
    </section>
  );
}
