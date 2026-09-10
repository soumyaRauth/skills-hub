const FIELDS = ['plan', 'status', 'region', 'since', 'q'];

export function CustomerFilters({ value, onChange }) {
  return (
    <form className="filters">
      {FIELDS.map((f) => (
        <input
          key={f}
          name={f}
          value={value[f] || ''}
          placeholder={f}
          onChange={(e) => onChange({ ...value, [f]: e.target.value })}
        />
      ))}
    </form>
  );
}
