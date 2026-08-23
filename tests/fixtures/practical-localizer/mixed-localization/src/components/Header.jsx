import { useTranslation } from "react-i18next";
import { tr } from "../legacy/translations";

export function Header({ user }) {
  const { t } = useTranslation();

  return (
    <header>
      <span className="brand">{t("brand")}</span>

      <nav>
        <a href="/tickets">{t("nav.tickets")}</a>
        <a href="/reports">{t("nav.reports")}</a>
        <a href="/settings">{tr("settings")}</a>
      </nav>

      {user ? (
        <button onClick={() => signOut()}>{tr("logout")}</button>
      ) : (
        <a href="/login">{t("auth.signIn")}</a>
      )}

      <span className="beta-badge">Beta — feedback welcome</span>
      <a href="/help">Help</a>
    </header>
  );
}
