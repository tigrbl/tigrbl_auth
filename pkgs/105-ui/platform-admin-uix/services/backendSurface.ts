export const BACKEND_APP = "tigrbl-auth-backend-app-platform-admin";
export const BACKEND_APP_BASE_URL_ENV = "VITE_TIGRBL_AUTH_PLATFORM_ADMIN_BACKEND_APP_BASE_URL";
export const BACKEND_APP_BASE_URL = (import.meta.env.VITE_TIGRBL_AUTH_PLATFORM_ADMIN_BACKEND_APP_BASE_URL ?? "http://localhost:8015").replace(/\/+$/, "");
export const SURFACE_PURPOSE = "Cross-tenant control plane for tenant lifecycle and platform authority.";

export const FORBIDDEN_PATH_PREFIXES = ["/login", "/authorize", "/token", "/consent", "/register", "/userinfo"];
export const ALLOWED_PATH_PREFIXES = ["/admin/auth", "/admin/realm", "/admin/tenant", "/admin/identities", "/auditevent"];

export function assertSurfacePath(path: string): void {
  if (!path.startsWith("/")) {
    throw new Error(`Transport paths must be absolute: ${path}`);
  }
  const pathname = new URL(path, `${BACKEND_APP_BASE_URL}/`).pathname;
  if (FORBIDDEN_PATH_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`))) {
    throw new Error(`Path is outside ${BACKEND_APP}: ${path}`);
  }
  if (!ALLOWED_PATH_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`))) {
    throw new Error(`Path is not part of ${BACKEND_APP}: ${path}`);
  }
}

export function backendAppUrl(path: string): URL {
  assertSurfacePath(path);
  return new URL(path, `${BACKEND_APP_BASE_URL}/`);
}
