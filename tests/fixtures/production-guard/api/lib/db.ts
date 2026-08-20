/** Stub persistence layer. The fixture is read, not run. */
export const db = {
  async query(_sql: string, _params: unknown[]): Promise<any[]> {
    throw new Error("stub");
  },
};
