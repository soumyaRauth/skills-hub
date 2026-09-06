import React, { useState } from 'react';
import { TaskFilters } from './TaskFilters';
import { SavedViews } from './SavedViews';
import { BulkBar } from './BulkBar';

export function TaskList({ tasks }) {
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState({ field: 'due_at', dir: 'asc' });
  const [filters, setFilters] = useState({});
  const [selected, setSelected] = useState([]);

  const visible = tasks
    .filter((t) => t.title.toLowerCase().includes(query.toLowerCase()))
    .filter((t) => (filters.status ? t.status === filters.status : true))
    .filter((t) => (filters.assignee ? t.assignee_id === filters.assignee : true))
    .filter((t) => (filters.priority ? t.priority === filters.priority : true))
    .filter((t) => (filters.label ? (t.labels || []).includes(filters.label) : true))
    .sort((a, b) => (a[sort.field] > b[sort.field] ? 1 : -1) * (sort.dir === 'asc' ? 1 : -1));

  return (
    <div className="task-list">
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search tasks" />
      <SavedViews onApply={setFilters} current={filters} />
      <TaskFilters value={filters} onChange={setFilters} />
      {selected.length > 0 && <BulkBar ids={selected} onDone={() => setSelected([])} />}

      <table>
        <thead>
          <tr>
            {['title', 'assignee_id', 'status', 'priority', 'due_at'].map((f) => (
              <th key={f} onClick={() => setSort({ field: f, dir: sort.dir === 'asc' ? 'desc' : 'asc' })}>
                {f}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {visible.map((t) => (
            <tr key={t.id}>
              <td>
                <input
                  type="checkbox"
                  checked={selected.includes(t.id)}
                  onChange={(e) =>
                    setSelected(e.target.checked ? [...selected, t.id] : selected.filter((i) => i !== t.id))
                  }
                />
                {t.title}
              </td>
              <td>{t.assignee_id}</td>
              <td>{t.status}</td>
              <td>{t.priority}</td>
              <td>{t.due_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
