// Small helper for POST requests to the FastAPI backend.
export async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = Array.isArray(body.detail)
      ? body.detail.map((d) => `${d.loc?.at(-1)}: ${d.msg}`).join(", ")
      : body.detail;
    throw new Error(detail || "The request failed. Check your details and try again.");
  }
  return body;
}
