import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TIGRBL_AUTH_SERVICE_ADMIN_API_BASE_URL || "http://localhost:8018";

  return {
    plugins: [react()],
    resolve: {
      alias: [
        { find: "@tigrbl-auth/uix-core/styles.css", replacement: path.resolve(process.cwd(), "../../100-uix-core/uix-core/src/styles/core.css") },
        { find: "@tigrbl-auth/uix-core", replacement: path.resolve(process.cwd(), "../../100-uix-core/uix-core/index.ts") }
      ]
    },
    server: {
      port: 3014,
      host: "0.0.0.0",
      proxy: {
        "/rpc": { target, changeOrigin: true },
        "/service": { target, changeOrigin: true },
        "/servicekey": { target, changeOrigin: true },
        "/apikey": { target, changeOrigin: true },
        "/tokenrecord": { target, changeOrigin: true },
        "/.well-known": { target, changeOrigin: true },
        "/introspect": { target, changeOrigin: true }
      }
    }
  };
});
