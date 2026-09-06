async function toBase64(file) {
  const buffer = await file.arrayBuffer();
  let binary = "";
  const bytes = new Uint8Array(buffer);
  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}

export async function uploadPlanFile(tenantId, file) {
  const response = await fetch(`/api/tenants/${tenantId}/plans/import`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      filename: file.name,
      contentType: file.type || "text/csv",
      contentBase64: await toBase64(file),
    }),
  });

  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error ?? "Upload failed");
  return payload;
}
