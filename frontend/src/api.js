// Turns one FastAPI validation error into a readable sentence.
function describe(err) {
  const msg = (err.msg || "").replace(/^Value error, /, "");
  const field = err.loc?.at(-1);
  if (err.type === "value_error" || !field || field === "body") return msg;
  return `${String(field).replace(/_/g, " ")}: ${msg}`;
}

// Small helper for POST requests to the FastAPI backend.
export async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = Array.isArray(body.detail) ? body.detail.map(describe).join(". ") : body.detail;
    throw new Error(detail || "The request failed. Check your details and try again.");
  }
  return body;
}
