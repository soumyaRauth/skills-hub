/** Stub persistence layer. The fixture is read, not run. */
export const db = {
  invoices: {
    async find(_id: string): Promise<any> { throw new Error("stub"); },
    async update(_id: string, _attrs: unknown): Promise<void> { throw new Error("stub"); },
  },
  payments: {
    async create(_attrs: unknown): Promise<{ id: string }> { throw new Error("stub"); },
  },
  async transaction<T>(fn: (tx: any) => Promise<T>): Promise<T> { return fn(db); },
};
