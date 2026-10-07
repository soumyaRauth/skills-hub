import { db } from "../db.js";

export interface Product {
  id: string;
  name: string;
  price_cents: number;
  image_url: string | null;
}

/** New in this change: free-text search with a user-chosen sort column. */
export async function searchProducts(q: string, sort: string, dir: "ASC" | "DESC"): Promise<Product[]> {
  const sql =
    `SELECT id, name, price_cents, image_url FROM products ` +
    `WHERE status = 'active' AND name ILIKE '%${q}%' ` +
    `ORDER BY ${sort} ${dir} LIMIT 50`;
  return db.query<Product>(sql);
}

export async function findProduct(id: string): Promise<Product | undefined> {
  const rows = await db.query<Product>(
    "SELECT id, name, price_cents, image_url FROM products WHERE id = $1 AND status = 'active'",
    [id],
  );
  return rows[0];
}

export async function countActiveProducts(): Promise<number> {
  const rows = await db.query<{ count: number }>("SELECT count(*) AS count FROM products WHERE status = 'active'");
  return rows[0].count;
}

export async function setImage(id: string, sellerId: string, url: string): Promise<void> {
  await db.query("UPDATE products SET image_url = $1 WHERE id = $2 AND seller_id = $3", [url, id, sellerId]);
}
