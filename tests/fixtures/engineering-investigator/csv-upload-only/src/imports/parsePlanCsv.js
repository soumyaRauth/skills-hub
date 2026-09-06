import { decodeUtf8 } from "../lib/encoding.js";

const REQUIRED = ["plan_code", "name", "monthly_price", "seats"];

/**
 * Parses an uploaded plan sheet into normalized rows.
 * Returns { rows, errors } — never throws on bad data, so the route can
 * report every problem in one response instead of the first one.
 */
export function parsePlanCsv(bytes) {
  const text = decodeUtf8(bytes);
  const lines = text.split(/\r?\n/).filter((l) => l.trim() !== "");
  if (lines.length === 0) return { rows: [], errors: ["file is empty"] };

  const header = lines[0].split(",").map((h) => h.trim().toLowerCase());
  const missing = REQUIRED.filter((c) => !header.includes(c));
  if (missing.length) {
    return { rows: [], errors: [`missing columns: ${missing.join(", ")}`] };
  }

  const rows = [];
  const errors = [];
  for (let i = 1; i < lines.length; i++) {
    const cells = lines[i].split(",").map((c) => c.trim());
    const record = Object.fromEntries(header.map((h, j) => [h, cells[j] ?? ""]));
    const row = normalizeRow(record, i + 1);
    if (row.error) errors.push(row.error);
    else rows.push(row.value);
  }
  return { rows, errors };
}

// The row shape every downstream consumer expects.
export function normalizeRow(record, lineNumber) {
  const price = Number(record.monthly_price);
  const seats = Number(record.seats);
  if (!record.plan_code) return { error: `line ${lineNumber}: plan_code is required` };
  if (!Number.isFinite(price)) return { error: `line ${lineNumber}: monthly_price is not a number` };
  if (!Number.isInteger(seats)) return { error: `line ${lineNumber}: seats is not an integer` };
  return {
    value: {
      planCode: record.plan_code,
      name: record.name,
      monthlyPrice: price,
      seats,
    },
  };
}
