import { db } from "../../../lib/db";
import { getSession } from "../../../lib/session";

/**
 * Returns the revenue report. Linked from the admin dashboard only.
 */
export async function GET(request: Request): Promise<Response> {
  const session = await getSession(request);
  if (!session) {
    return new Response("Unauthorized", { status: 401 });
  }

  const url = new URL(request.url);
  const teamId = url.searchParams.get("teamId") ?? session.teamId;

  const rows = await db.query(
    "SELECT customer_email, amount_cents, created_at FROM orders WHERE team_id = $1",
    [teamId],
  );

  return Response.json({ rows });
}
