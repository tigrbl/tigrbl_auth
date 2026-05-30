export const PRODUCT_API = "tigrbl-auth-api-platform-admin";
export const API_BASE_URL_ENV = "VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL";
export const API_BASE_URL = (import.meta.env.VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL ?? "http://localhost:8015").replace(/\/+$/, "");
export const SURFACE_PURPOSE = "Cross-tenant control plane for tenant lifecycle and platform authority.";

export const FORBIDDEN_PATH_PREFIXES = ["/login", "/authorize", "/token", "/consent", "/register", "/userinfo"];
export const ALLOWED_PATH_PREFIXES = ["/admin/auth", "/admin/tenant", "/admin/identity", "/auditevent"];

export function assertSurfacePath(path: string): void {
  if (!path.startsWith("/")) {
    throw new Error(`API paths must be absolute: ${path}`);
  }
  const pathname = new URL(path, `${API_BASE_URL}/`).pathname;
  if (FORBIDDEN_PATH_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`))) {
    throw new Error(`Path is outside ${PRODUCT_API}: ${path}`);
  }
  if (!ALLOWED_PATH_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`))) {
    throw new Error(`Path is not part of ${PRODUCT_API}: ${path}`);
  }
}

export function apiUrl(path: string): URL {
  assertSurfacePath(path);
  return new URL(path, `${API_BASE_URL}/`);
}
