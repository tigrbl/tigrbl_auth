import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL || "http://localhost:8101";

  return {
    plugins: [react()],
    server: {
      port: 3011,
      host: "0.0.0.0",
      proxy: {
        "/rpc": { target, changeOrigin: true },
        "/tenant": { target, changeOrigin: true },
        "/user": { target, changeOrigin: true }
      }
    }
  };
});
