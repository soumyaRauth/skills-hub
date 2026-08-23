import { useTranslation } from "react-i18next";
import { useState } from "react";
import { cancelSubscription } from "../api/billing";

export function SubscriptionPanel({ subscription }) {
  const { t } = useTranslation();
  const [confirming, setConfirming] = useState(false);

  return (
    <section>
      <h2>{t("billing.planTitle")}</h2>

      <button onClick={() => setConfirming(true)}>
        {t("billing.cancelSubscription")}
      </button>

      {confirming && (
        <div role="dialog" aria-label={t("billing.confirmTitle")}>
          <h3>{t("billing.confirmTitle")}</h3>
          <p>{t("billing.confirmBody", { endDate: subscription.endsAt })}</p>

          <button onClick={() => cancelSubscription(subscription.id)}>
            {t("billing.cancelSubscription")}
          </button>

          <button onClick={() => setConfirming(false)}>
            {t("common.cancel")}
          </button>
        </div>
      )}
    </section>
  );
}
