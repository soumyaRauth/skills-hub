/** Stub persistence layer. The fixture is read, not run. */
export const db = {
  async query<T = any>(_sql: string, _params: unknown[] = []): Promise<T[]> {
    throw new Error("stub");
  },
};
