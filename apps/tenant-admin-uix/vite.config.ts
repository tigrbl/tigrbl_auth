import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL || "http://localhost:8102";

  return {
    plugins: [react()],
    server: {
      port: 3012,
      host: "0.0.0.0",
      proxy: {
        "/rpc": { target, changeOrigin: true },
        "/user": { target, changeOrigin: true },
        "/client": { target, changeOrigin: true }
      }
    }
  };
});
