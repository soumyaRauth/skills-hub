import { paginate } from './pagination.js';

const records = Array.from({ length: 25 }, (_, i) => ({
  id: i + 1,
  name: `Record ${i + 1}`,
}));

export function listRecords(query = {}) {
  return paginate(records, query);
}

export function allRecords() {
  return records;
}
