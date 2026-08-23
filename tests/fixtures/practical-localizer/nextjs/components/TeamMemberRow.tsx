"use client";

import { useTranslations } from "next-intl";
import { removeMember } from "@/lib/team";

export function TeamMemberRow({ member, teamId }: { member: Member; teamId: string }) {
  const t = useTranslations();

  return (
    <li className="row">
      <span>{member.name}</span>
      <button
        className="btn-secondary"
        onClick={() => removeMember(teamId, member.id)}
        aria-label={t("common.remove")}
      >
        {t("common.remove")}
      </button>
    </li>
  );
}
