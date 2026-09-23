import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// Settings are read from the .env file in the project root (one level up), the same file the backend uses.
// During development, /api calls are forwarded to FastAPI on API_PORT.
// In production both run from one FastAPI server, so no proxy is needed.
export default defineConfig(({ mode }) => {
  const env = { ...loadEnv(mode, "..", ""), ...process.env };
  const apiTarget = env.API_PROXY_TARGET || `http://localhost:${env.API_PORT || 8000}`;
  const brandName = env.BRAND_NAME || "SafeRide Airport Taxis";

  return {
    plugins: [
      react(),
      {
        // Puts the brand name into <title> in index.html
        name: "brand-name",
        transformIndexHtml: (html) => html.replaceAll("%BRAND_NAME%", brandName),
      },
    ],
    envDir: "..",
    server: {
      port: Number(env.FRONTEND_PORT || 5173),
      strictPort: true,
      proxy: { "/api": apiTarget },
    },
  };
});
