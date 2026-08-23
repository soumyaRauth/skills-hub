import { useTranslations } from "next-intl";

export function SideNav() {
  const t = useTranslations("nav");

  return (
    <nav className="w-40">
      <a href="/dashboard" className="block truncate whitespace-nowrap">{t("dashboard")}</a>
      <a href="/team" className="block truncate whitespace-nowrap">{t("team")}</a>
      <a href="/files" className="block truncate whitespace-nowrap">{t("files")}</a>
      <a href="/settings" className="block truncate whitespace-nowrap">{t("accountSettings")}</a>
    </nav>
  );
}
