export default function CustomerTable({ customers, onSelect }) {
  return (
    <div className="table">
      {customers.map((c) => (
        <div key={c.id} className="row" onClick={() => onSelect(c)}>
          <span>{c.name}</span>
          <span>{c.email}</span>
        </div>
      ))}
    </div>
  )
}
