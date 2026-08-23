import { useTranslation } from "react-i18next";
import { tr } from "../legacy/translations";
import { deleteTicket, removeTag } from "../api/tickets";

export function TicketList({ tickets, openCount }) {
  const { t } = useTranslation();

  return (
    <section>
      <h1>{t("tickets.title")}</h1>

      <p>{openCount + " " + t("tickets.openCount")}</p>

      <ul>
        {tickets.map((ticket) => (
          <li key={ticket.id}>
            <span>{ticket.subject}</span>
            <span>{t("tickets.assignedTo", { agent: ticket.agentName })}</span>

            <button onClick={() => removeTag(ticket.id)}>{t("tickets.removeTag")}</button>
            <button onClick={() => deleteTicket(ticket.id)}>{tr("delete")}</button>
          </li>
        ))}
      </ul>

      <button className="cta">{t("tickets.getStarted")}</button>
    </section>
  );
}
