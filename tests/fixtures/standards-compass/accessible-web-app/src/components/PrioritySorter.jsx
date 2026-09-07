// Clinicians reorder their waiting list by dragging rows.
export default function PrioritySorter({ patients, onReorder }) {
  return (
    <ul className="sorter">
      {patients.map((p, index) => (
        <li
          key={p.id}
          draggable
          onDragStart={(e) => e.dataTransfer.setData('text/plain', String(index))}
          onDrop={(e) => onReorder(Number(e.dataTransfer.getData('text/plain')), index)}
          onDragOver={(e) => e.preventDefault()}
        >
          {p.name}
        </li>
      ))}
    </ul>
  )
}
