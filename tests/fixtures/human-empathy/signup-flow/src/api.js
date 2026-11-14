export async function createAccount(form) {
  const res = await fetch("/api/accounts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form),
  });
  if (!res.ok) {
    // 409 = email already registered, 422 = server-side validation, 5xx = outage
    throw new Error("Something went wrong. Please try again.");
  }
  return res.json();
}
