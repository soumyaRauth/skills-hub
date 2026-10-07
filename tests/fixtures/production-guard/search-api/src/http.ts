/** Stub HTTP client. Follows redirects; nothing restricts the destination. */
export const httpClient = {
  async get(_url: string): Promise<{ status: number; body: Uint8Array }> {
    throw new Error("stub");
  },
};
