import { format } from "date-fns";
import { useTranslations } from "next-intl";

export function OrderSummary({ order }: { order: Order }) {
  const t = useTranslations("checkout");

  const amount = "$" + order.totalCents / 100;
  const due = format(new Date(order.dueAt), "MM/dd/yyyy");

  return (
    <section>
      <p>{t("total", { amount })}</p>
      <p>{t("dueDate", { date: due })}</p>
      <p>{order.itemCount + " items"}</p>
      <button>{t("placeOrder")}</button>
    </section>
  );
}
