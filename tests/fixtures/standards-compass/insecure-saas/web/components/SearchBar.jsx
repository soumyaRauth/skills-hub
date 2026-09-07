import { useState } from 'react'

export default function SearchBar({ onSearch }) {
  const [q, setQ] = useState('')
  return (
    <div className="search">
      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search" />
      <div className="btn" onClick={() => onSearch(q)}>Go</div>
    </div>
  )
}
