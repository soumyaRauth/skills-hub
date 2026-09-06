import React from 'react';

const isPaid = (inv) => inv.status === 'paid';

export function Dashboard({ invoices }) {
  const outstanding = invoices.filter((i) => !isPaid(i));
  const total = outstanding.reduce((sum, i) => sum + i.total_cents, 0);

  return (
    <div>
      <h2>Outstanding: {total}</h2>
      <ul>
        {outstanding.map((i) => (
          <li key={i.id}>
            {i.number} — {i.total_cents}
          </li>
        ))}
      </ul>
    </div>
  );
}
