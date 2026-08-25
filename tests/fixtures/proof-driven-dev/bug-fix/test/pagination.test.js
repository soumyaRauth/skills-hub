import { test } from 'node:test';
import assert from 'node:assert/strict';
import { paginate } from '../src/pagination.js';

// Every existing test uses a count that is an exact multiple of perPage.
const twenty = Array.from({ length: 20 }, (_, i) => i + 1);

test('returns the first page by default', () => {
  const result = paginate(twenty);
  assert.equal(result.page, 1);
  assert.equal(result.items.length, 10);
  assert.equal(result.items[0], 1);
});

test('returns the second page', () => {
  const result = paginate(twenty, { page: 2 });
  assert.equal(result.items[0], 11);
  assert.equal(result.items.at(-1), 20);
});

test('reports the total item count', () => {
  assert.equal(paginate(twenty).totalItems, 20);
});

test('reports the total page count', () => {
  assert.equal(paginate(twenty).totalPages, 2);
});

test('respects a custom page size', () => {
  const result = paginate(twenty, { perPage: 5 });
  assert.equal(result.items.length, 5);
  assert.equal(result.totalPages, 4);
});
