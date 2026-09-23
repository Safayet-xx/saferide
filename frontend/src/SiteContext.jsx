import { createContext, useContext, useEffect, useState } from "react";

// Loads all site content once from /api/site and shares it with every page.
const SiteContext = createContext(null);

export function SiteProvider({ children }) {
  const [site, setSite] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/site")
      .then((res) => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then(setSite)
      .catch(() => setError("Site content couldn't load. Make sure the FastAPI server is running."));
  }, []);

  if (error) return <p className="status">{error}</p>;
  if (!site) return <p className="status">Loading…</p>;

  return <SiteContext.Provider value={site}>{children}</SiteContext.Provider>;
}

export const useSite = () => useContext(SiteContext);

export const telLink = (phone) => `tel:${phone.replace(/\s/g, "")}`;
