import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TBA_AUTH_MY_ACCOUNT_BACKEND_APP_BASE_URL || "http://localhost:8019";

  return {
    plugins: [react()],
    resolve: {
      alias: [
        { find: "@tba/ui-primitives/styles.css", replacement: path.resolve(process.cwd(), "../../100-uix-core/tba-ui-primitives/src/styles/core.css") },
        { find: "@tba/ui-primitives", replacement: path.resolve(process.cwd(), "../../100-uix-core/tba-ui-primitives/index.ts") }
      ]
    },
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
