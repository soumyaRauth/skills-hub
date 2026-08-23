import { useTranslation } from "react-i18next";
import { tr } from "../legacy/translations";

export function SystemStatus({ status }) {
  const { t } = useTranslation();

  return (
    <div className="status">
      {status.serverDown && <p className="error">{tr("server_error")}</p>}
      {status.cacheCleared && <p>{t("system.cacheCleared")}</p>}

      <button style={{ width: 120, whiteSpace: "nowrap", overflow: "hidden" }}>
        {t("system.downloadReport")}
      </button>

      <button style={{ width: 120, whiteSpace: "nowrap", overflow: "hidden" }}>
        {tr("upload")}
      </button>

      <p>{t("system.apiKey")}</p>
    </div>
  );
}
