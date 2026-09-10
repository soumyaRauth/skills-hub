export function GroupAdmin({ groups, staff, onAdd, onToggleManage }) {
  return (
    <section>
      <h2>Staff groups</h2>
      {groups.map((g) => (
        <div key={g.id}>
          <label>
            <input
              type="checkbox"
              checked={g.can_manage}
              onChange={() => onToggleManage(g)}
            />
            {g.name} can manage the console
          </label>
          <select onChange={(e) => onAdd(g.id, e.target.value)}>
            {staff.map((s) => <option key={s.id} value={s.id}>{s.email}</option>)}
          </select>
        </div>
      ))}
    </section>
  );
}
