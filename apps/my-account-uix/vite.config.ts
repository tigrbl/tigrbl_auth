import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TIGRBL_AUTH_MY_ACCOUNT_API_BASE_URL || "http://localhost:8019";

  return {
    plugins: [react()],
    server: {
      port: 3019,
      host: "0.0.0.0",
      proxy: {
        "/account": { target, changeOrigin: true },
        "/.well-known": { target, changeOrigin: true },
        "/tenants": { target, changeOrigin: true }
      }
    },
    test: {
      environment: "node"
    }
  };
});
