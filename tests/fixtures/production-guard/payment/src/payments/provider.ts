import { httpClient } from "../http.js";

/** Thin wrapper around the payment provider's HTTP API. */
export const provider = {
  async charge(params: {
    amount: number;
    currency: string;
    customerId: string;
  }): Promise<{ id: string }> {
    const res = await httpClient.post("https://api.payments.example/charges", params);
    return { id: res.data.id };
  },
};
