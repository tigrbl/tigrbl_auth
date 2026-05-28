import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL || "http://localhost:8017";

  return {
    plugins: [react()],
    server: {
      port: 3013,
      host: "0.0.0.0",
      proxy: {
        "/register": { target, changeOrigin: true },
        "/rpc": { target, changeOrigin: true },
        "/.well-known": { target, changeOrigin: true }
      }
    }
  };
});
