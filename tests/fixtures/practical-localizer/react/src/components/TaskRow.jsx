import { useTranslation } from "react-i18next";
import { markComplete } from "../api/tasks";

export function TaskRow({ task }) {
  const { t } = useTranslation();

  return (
    <li>
      <span>{task.title}</span>

      <span className={"badge badge--" + task.status}>
        {task.status === "complete" ? t("status.complete") : t("status.pending")}
      </span>

      <button onClick={() => markComplete(task.id)}>{t("actions.complete")}</button>
    </li>
  );
}
