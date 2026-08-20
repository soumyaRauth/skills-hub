/** Stub HTTP client. No timeout is configured anywhere in this fixture. */
export const httpClient = {
  async post(_url: string, _body: unknown): Promise<{ data: any }> {
    throw new Error("stub");
  },
};
