import React from 'react';

// Saved views persist a subset of the filter state.
const PERSISTED = ['status', 'assignee'];

export function SavedViews({ onApply, current }) {
  const save = async () => {
    const filters = {};
    for (const key of PERSISTED) filters[key] = current[key];
    await fetch('/api/saved-views', { method: 'POST', body: JSON.stringify({ filters }) });
  };

  return (
    <div className="saved-views">
      <button onClick={save}>Save this view</button>
    </div>
  );
}
