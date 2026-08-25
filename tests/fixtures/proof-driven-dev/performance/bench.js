import { buildOrderReport } from './src/report.js';
import { stats, resetStats } from './src/db.js';

resetStats();
const started = process.hrtime.bigint();
const report = buildOrderReport();
const elapsedMs = Number(process.hrtime.bigint() - started) / 1e6;

console.log(`rows:      ${report.orderCount}`);
console.log(`total:     ${report.totalCents}`);
console.log(`queries:   ${stats.queries}`);
console.log(`elapsed:   ${elapsedMs.toFixed(2)}ms   (local wall clock — not a production number)`);
