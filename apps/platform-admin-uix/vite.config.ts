import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const target = env.VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL || "http://localhost:8015";

  return {
    plugins: [react()],
    server: {
      port: 3011,
      host: "0.0.0.0",
      proxy: {
        "/admin": { target, changeOrigin: true },
        "/auditevent": { target, changeOrigin: true }
      }
    }
  };
});
