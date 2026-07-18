export const BACKEND_APP = "tigrbl-auth-backend-app-developer";
export const BACKEND_APP_BASE_URL_ENV = "VITE_TIGRBL_AUTH_DEVELOPER_BACKEND_APP_BASE_URL";
export const BACKEND_APP_BASE_URL = (import.meta.env.VITE_TIGRBL_AUTH_DEVELOPER_BACKEND_APP_BASE_URL ?? "http://localhost:8017").replace(/\/+$/, "");
export const SURFACE_PURPOSE = "Developer control plane for app registration and client metadata.";

export const FORBIDDEN_PATH_PREFIXES = ["/login", "/authorize", "/token", "/tenant", "/service", "/apikey", "/servicekey"];
export const ALLOWED_PATH_PREFIXES = ["/register", "/register/", "/rpc", "/client", "/clientregistration", "/.well-known"];

export function assertSurfacePath(path: string): void {
  if (!path.startsWith("/")) {
    throw new Error(`Transport paths must be absolute: ${path}`);
  }
  if (FORBIDDEN_PATH_PREFIXES.some((prefix) => path === prefix || path.startsWith(`${prefix}/`))) {
    throw new Error(`Path is outside ${BACKEND_APP}: ${path}`);
  }
  if (!ALLOWED_PATH_PREFIXES.some((prefix) => path === prefix || path.startsWith(`${prefix}/`))) {
    throw new Error(`Path is not part of ${BACKEND_APP}: ${path}`);
  }
}

export function backendAppUrl(path: string): URL {
  assertSurfacePath(path);
  return new URL(path, `${BACKEND_APP_BASE_URL}/`);
}
