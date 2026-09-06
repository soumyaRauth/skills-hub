import { useState } from "react";
import { uploadPlanFile } from "./api.js";

export function PlanUpload({ tenantId }) {
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  async function onChange(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".csv")) {
      setError("Please choose a CSV file.");
      return;
    }

    setError(null);
    try {
      setResult(await uploadPlanFile(tenantId, file));
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="plan-upload">
      <label htmlFor="plan-file">Import plans</label>
      <input id="plan-file" type="file" accept=".csv,text/csv" onChange={onChange} />
      <p className="hint">Upload a CSV file with the columns plan_code, name, monthly_price, seats.</p>
      {error && <p className="error">{error}</p>}
      {result && <p className="ok">Imported {result.imported} plans.</p>}
    </div>
  );
}
