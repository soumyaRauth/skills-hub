const db = require('../src/db');
const { buildMonthlyReport } = require('./reports');

const jobs = new Map();

async function enqueueReport(org, month) {
  const id = `${org}:${month}:${Date.now()}`;
  jobs.set(id, buildMonthlyReport(org, month));
  return { id };
}

async function getReportResult(id) {
  return jobs.get(id);
}

module.exports = { enqueueReport, getReportResult, db };
