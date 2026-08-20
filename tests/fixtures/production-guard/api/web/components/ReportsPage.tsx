"use client";

import { useSession } from "../../lib/useSession";

export function ReportsPage() {
  const session = useSession();

  // Non-admins never see the report link or the export button.
  if (session.role !== "admin") {
    return <p>You do not have access to reports.</p>;
  }

  return (
    <section>
      <h1>Revenue</h1>
      <a href="/api/reports">Download revenue report</a>
    </section>
  );
}
