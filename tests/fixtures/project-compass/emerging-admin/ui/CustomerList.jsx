import { CustomerFilters } from './CustomerFilters';
import { SavedSegments } from './SavedSegments';

const COLUMNS = ['email', 'name', 'plan', 'status', 'last_seen_at'];

export function CustomerList({ rows, filters, segments, onChange, onBulk, onExport }) {
  const [selected, setSelected] = useState([]);

  return (
    <div className="console">
      <CustomerFilters value={filters} onChange={onChange} />
      <SavedSegments segments={segments} current={filters} onSave={onChange} onApply={onChange} />
      <div className="bulk">
        <button onClick={() => onBulk('deactivate', selected)}>Deactivate</button>
        <button onClick={() => onBulk('delete', selected)}>Delete</button>
        <button onClick={onExport}>Export CSV</button>
      </div>
      <table>
        <thead>
          <tr>{COLUMNS.map((c) => <th key={c}>{c}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>{COLUMNS.map((c) => <td key={c}>{r[c]}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
