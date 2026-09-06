import React from 'react';

const FIELDS = ['status', 'assignee', 'priority', 'label'];

export function TaskFilters({ value, onChange }) {
  return (
    <div className="filters">
      {FIELDS.map((f) => (
        <select key={f} value={value[f] || ''} onChange={(e) => onChange({ ...value, [f]: e.target.value })}>
          <option value="">Any {f}</option>
        </select>
      ))}
    </div>
  );
}
