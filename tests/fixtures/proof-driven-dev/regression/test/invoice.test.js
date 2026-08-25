import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderInvoice } from '../src/invoice.js';

test('renders an invoice with a total', () => {
  const output = renderInvoice({
    number: 'INV-001',
    issuedAt: '2026-03-01T00:00:00.000Z',
    lineItems: [
      { description: 'Seat license', amountCents: 100000 },
      { description: 'Support', amountCents: 23450 },
    ],
  });

  assert.match(output, /INVOICE INV-001/);
  assert.match(output, /Total {3}\$1,234\.50/);
});
