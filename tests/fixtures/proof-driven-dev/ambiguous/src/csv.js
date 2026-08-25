// Minimal CSV reader used by the existing settings importer. Header row
// required; no quoted-field support, which is a known limitation.
export function parseCsv(text) {
  const [header, ...rows] = text.trim().split('\n');
  const columns = header.split(',').map((c) => c.trim());

  return rows.map((row) => {
    const cells = row.split(',').map((c) => c.trim());
    return Object.fromEntries(columns.map((column, i) => [column, cells[i] ?? '']));
  });
}
