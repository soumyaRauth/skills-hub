import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildOrderReport } from '../src/report.js';

test('reports only paid orders', () => {
  const report = buildOrderReport();
  assert.equal(report.orderCount, 445);
});

test('rows carry the customer name and tier', () => {
  const [first] = buildOrderReport().rows;
  assert.equal(typeof first.customer, 'string');
  assert.ok(['gold', 'standard'].includes(first.tier));
});

test('total matches the sum of the rows', () => {
  const report = buildOrderReport();
  const sum = report.rows.reduce((acc, row) => acc + row.totalCents, 0);
  assert.equal(report.totalCents, sum);
});
