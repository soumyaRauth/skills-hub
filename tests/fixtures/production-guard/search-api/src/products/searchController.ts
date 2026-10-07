import { searchProducts, findProduct } from "./productRepo.js";

interface Request {
  query: Record<string, string | undefined>;
  params: Record<string, string>;
}
interface Response {
  status(code: number): Response;
  json(body: unknown): void;
}

export async function search(req: Request, res: Response): Promise<void> {
  const q = req.query.q ?? "";
  const sort = req.query.sort ?? "name";
  const dir = req.query.dir === "desc" ? "DESC" : "ASC";
  const results = await searchProducts(q, sort, dir);
  res.status(200).json({ query: q, results });
}

export async function show(req: Request, res: Response): Promise<void> {
  const product = await findProduct(req.params.id);
  if (!product) return res.status(404).json({ error: "not_found" });
  res.status(200).json(product);
}
