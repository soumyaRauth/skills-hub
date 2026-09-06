import React from 'react';

export function Reconcile({ rec, adj }) {
  const variance = rec.counted_total - rec.system_total;

  return (
    <div className="reconcile">
      <h1>{rec.period}</h1>
      <p>Counted: {rec.counted_total}</p>
      <p>System: {rec.system_total}</p>
      <p className={variance === 0 ? 'ok' : 'warn'}>Variance: {variance}</p>

      <button onClick={() => fetch(`/api/reconciliations/${rec.id}/export`)}>Export</button>

      <ul>
        {adj.map((a) => (
          <li key={a.id}>
            {a.sku} {a.delta > 0 ? '+' : ''}
            {a.delta}
          </li>
        ))}
      </ul>
    </div>
  );
}
