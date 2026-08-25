import { test } from 'node:test';
import assert from 'node:assert/strict';
import { listInvoices } from '../src/api.js';

const session = { userId: 1, organizationId: 10 };

test('lists the signed-in user’s invoices', () => {
  const response = listInvoices(session);
  assert.equal(response.status, 200);
  assert.deepEqual(response.body.invoices.map((i) => i.id), ['inv_100', 'inv_101']);
});

test('rejects an unauthenticated request', () => {
  assert.equal(listInvoices(null).status, 401);
});
