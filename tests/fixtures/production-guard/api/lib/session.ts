export interface Session {
  userId: string;
  teamId: string;
  role: "admin" | "member" | "support";
}

/** Resolves the session from the request cookie. Does not check any role. */
export async function getSession(_request: Request): Promise<Session | null> {
  throw new Error("stub");
}
