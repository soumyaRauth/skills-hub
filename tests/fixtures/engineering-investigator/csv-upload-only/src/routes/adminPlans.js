import { parsePlanCsv } from "../imports/parsePlanCsv.js";
import { fromBase64 } from "../lib/encoding.js";
import { replacePlans } from "../repo/plans.js";

const ALLOWED_MIME = ["text/csv", "application/vnd.ms-excel"];
const MAX_BYTES = 5 * 1024 * 1024;

export async function uploadPlans(req, res) {
  const { filename, contentType, contentBase64 } = req.body ?? {};

  if (!ALLOWED_MIME.includes(contentType)) {
    return res.status(415).json({ error: "Only CSV files can be uploaded." });
  }
  if (!String(filename).toLowerCase().endsWith(".csv")) {
    return res.status(415).json({ error: "Only CSV files can be uploaded." });
  }

  const bytes = fromBase64(contentBase64);
  if (bytes.length > MAX_BYTES) {
    return res.status(413).json({ error: "File is larger than 5 MB." });
  }

  const { rows, errors } = parsePlanCsv(bytes);
  if (errors.length) {
    return res.status(422).json({ error: "The file could not be imported.", details: errors });
  }

  await replacePlans(req.tenantId, rows);
  return res.status(200).json({ imported: rows.length });
}
