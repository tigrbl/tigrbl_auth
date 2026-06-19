/// <reference types="vitest" />
import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: "@tigrbl-auth/uix-core/styles.css", replacement: path.resolve(process.cwd(), "../../90-uix-core/uix-core/src/styles/core.css") },
      { find: "@tigrbl-auth/uix-core", replacement: path.resolve(process.cwd(), "../../90-uix-core/uix-core/index.ts") }
    ]
  },
  server: {
    host: "0.0.0.0",
    port: 3020,
    proxy: {
      "/api/public": {
        target: "http://localhost:8013",
        changeOrigin: true,
        rewrite: (requestPath) => requestPath.replace(/^\/api\/public/, "")
      },
      "/api/resource-validation": {
        target: "http://localhost:8014",
        changeOrigin: true,
        rewrite: (requestPath) => requestPath.replace(/^\/api\/resource-validation/, "")
      },
      "/api/platform-admin": {
        target: "http://localhost:8015",
        changeOrigin: true,
        rewrite: (requestPath) => requestPath.replace(/^\/api\/platform-admin/, "")
      },
      "/api/tenant-admin": {
        target: "http://localhost:8016",
        changeOrigin: true,
        rewrite: (requestPath) => requestPath.replace(/^\/api\/tenant-admin/, "")
      },
      "/api/developer": {
        target: "http://localhost:8017",
        changeOrigin: true,
        rewrite: (requestPath) => requestPath.replace(/^\/api\/developer/, "")
      },
      "/api/service-admin": {
        target: "http://localhost:8018",
        changeOrigin: true,
        rewrite: (requestPath) => requestPath.replace(/^\/api\/service-admin/, "")
      },
      "/api/my-account": {
        target: "http://localhost:8019",
        changeOrigin: true,
        rewrite: (requestPath) => requestPath.replace(/^\/api\/my-account/, "")
      }
    }
  },
  test: {
    environment: "node"
  }
});
