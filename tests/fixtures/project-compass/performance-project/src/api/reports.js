const cache = require('../../lib/cache');
const { withRetry } = require('../../lib/retry');
const { enqueueReport, getReportResult } = require('../../workers/queue');

async function monthlyReport(req, res) {
  const key = `report:${req.query.org}:${req.query.month}`;

  const cached = cache.get(key);
  if (cached) return res.json(cached);

  const job = await withRetry(() => enqueueReport(req.query.org, req.query.month));
  const result = await getReportResult(job.id);

  cache.set(key, result);
  return res.json(result);
}

module.exports = { monthlyReport };
