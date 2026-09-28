import pg from "pg";

export const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });

export async function listBooks(userId) {
  const { rows } = await pool.query(
    "SELECT id, title, author, read_at FROM books WHERE user_id = $1 ORDER BY id",
    [userId],
  );
  return rows;
}

export async function addBook(userId, title, author) {
  const { rows } = await pool.query(
    "INSERT INTO books (user_id, title, author) VALUES ($1, $2, $3) RETURNING id",
    [userId, title, author],
  );
  return rows[0];
}
