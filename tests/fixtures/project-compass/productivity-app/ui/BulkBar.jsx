import React from 'react';

export function BulkBar({ ids, onDone }) {
  const apply = async (patch) => {
    await fetch('/api/tasks/bulk', { method: 'POST', body: JSON.stringify({ ids, patch }) });
    onDone();
  };

  return (
    <div className="bulk-bar">
      <span>{ids.length} selected</span>
      <button onClick={() => apply({ status: 'done' })}>Mark done</button>
      <button onClick={() => apply({ assignee_id: null })}>Unassign</button>
      <button onClick={() => apply({ priority: 'high' })}>Raise priority</button>
    </div>
  );
}
