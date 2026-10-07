import { httpClient } from "../http.js";
import { setImage } from "./productRepo.js";

interface Request {
  params: { id: string };
  body: { url?: string };
  user: { id: string };
}
interface Response {
  status(code: number): Response;
  json(body: unknown): void;
}

/** New in this change: copy a product image from a URL the seller supplies. */
export async function importImage(req: Request, res: Response): Promise<void> {
  const url = req.body.url;
  if (!url) return res.status(400).json({ error: "url_required" });

  const fetched = await httpClient.get(url);
  if (fetched.status !== 200) {
    return res.status(502).json({ error: "fetch_failed", status: fetched.status, body: new TextDecoder().decode(fetched.body) });
  }
  const stored = await storeImage(fetched.body);
  await setImage(req.params.id, req.user.id, stored);
  res.status(200).json({ image_url: stored });
}

async function storeImage(_bytes: Uint8Array): Promise<string> {
  throw new Error("stub");
}
