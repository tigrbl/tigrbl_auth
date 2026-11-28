import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TBA_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL || "http://localhost:8016";

  return {
    plugins: [react()],
    resolve: {
      alias: [
        { find: "@tba/ui-primitives/styles.css", replacement: path.resolve(process.cwd(), "../../100-uix-core/tba-ui-primitives/src/styles/core.css") },
        { find: "@tba/ui-primitives", replacement: path.resolve(process.cwd(), "../../100-uix-core/tba-ui-primitives/index.ts") }
      ]
    },
    server: {
      port: 3012,
      host: "0.0.0.0",
      proxy: {
        "/rpc": { target, changeOrigin: true },
        "/user": { target, changeOrigin: true },
        "/client": { target, changeOrigin: true },
        "/clientregistration": { target, changeOrigin: true },
        "/consent": { target, changeOrigin: true },
        "/auth": { target, changeOrigin: true },
        "/keyrotationevent": { target, changeOrigin: true }
      }
    }
  };
});
