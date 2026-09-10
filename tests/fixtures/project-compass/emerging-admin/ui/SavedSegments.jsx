// saved_segments only has columns for plan and status, so the rest is dropped.
const PERSISTED = ['plan', 'status'];

export function SavedSegments({ segments, current, onSave, onApply }) {
  const save = (name) =>
    onSave({ name, ...Object.fromEntries(PERSISTED.map((f) => [f, current[f]])) });

  return (
    <aside>
      <button onClick={() => save(prompt('Name this segment'))}>Save current view</button>
      <ul>
        {segments.map((s) => (
          <li key={s.id}>
            <button onClick={() => onApply(s)}>{s.name}</button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
