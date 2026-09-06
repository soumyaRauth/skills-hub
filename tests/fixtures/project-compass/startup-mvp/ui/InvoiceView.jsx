import React from 'react';

export function InvoiceView({ invoice }) {
  const outstanding = invoice.total_cents - invoice.paid_cents;

  return (
    <div className="invoice">
      <h1>Invoice {invoice.number}</h1>
      <p>Status: {invoice.status}</p>
      <p>Total: {invoice.total_cents}</p>
      {outstanding > 0 && <p className="warn">Outstanding: {outstanding}</p>}

      <button onClick={() => {}}>Download PDF</button>
      <button onClick={() => window.print()}>Print</button>
    </div>
  );
}
