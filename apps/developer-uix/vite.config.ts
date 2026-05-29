import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL || "http://localhost:8017";

  return {
    plugins: [react()],
    resolve: {
      alias: [
        { find: "@tigrbl-auth/uix-core/styles.css", replacement: path.resolve(process.cwd(), "../../packages/uix-core/src/styles/core.css") },
        { find: "@tigrbl-auth/uix-core", replacement: path.resolve(process.cwd(), "../../packages/uix-core/index.ts") }
      ]
    },
    server: {
      port: 3013,
      host: "0.0.0.0",
      proxy: {
        "/register": { target, changeOrigin: true },
        "/rpc": { target, changeOrigin: true },
        "/client": { target, changeOrigin: true },
        "/clientregistration": { target, changeOrigin: true },
        "/.well-known": { target, changeOrigin: true }
      }
    }
  };
});
