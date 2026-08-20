import { useState } from "react";

export function BulkActions({ selectedIds }) {
  const [error, setError] = useState(null);

  async function onDelete() {
    setError(null);
    const res = await fetch("/api/users/bulk-delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_ids: selectedIds }),
    });
    if (!res.ok) {
      setError("Something went wrong.");
    }
  }

  return (
    <div>
      <button onClick={onDelete}>Delete {selectedIds.length} users</button>
      {error && <p role="alert">{error}</p>}
    </div>
  );
}
