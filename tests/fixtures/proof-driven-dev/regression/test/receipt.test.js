import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderReceipt } from '../src/receipt.js';

test('renders a receipt', () => {
  const output = renderReceipt({
    amountCents: 123450,
    paidAt: '2026-03-04T10:00:00.000Z',
    last4: '4242',
  });

  assert.equal(
    output,
    'Thanks for your payment of $1,234.50.\nPaid 2026-03-04 with card ending 4242.',
  );
});

test('renders a small payment', () => {
  const output = renderReceipt({
    amountCents: 500,
    paidAt: '2026-03-04T10:00:00.000Z',
    last4: '1111',
  });

  assert.match(output, /payment of \$5\.00\./);
});
