export const PRODUCT_API = "tigrbl-auth-api-tenant-admin";
export const API_BASE_URL_ENV = "VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL";
export const API_BASE_URL = (import.meta.env.VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL ?? "http://localhost:8016").replace(/\/+$/, "");
export const SURFACE_PURPOSE = "Tenant-scoped control plane for users, admins, JWKS, and local policy.";

export const FORBIDDEN_PATH_PREFIXES = ["/login", "/authorize", "/token", "/register", "/tenant"];
export const ALLOWED_PATH_PREFIXES = ["/rpc", "/user", "/client", "/clientregistration", "/consent", "/auth/admin", "/keyrotationevent"];

export function assertSurfacePath(path: string): void {
  if (!path.startsWith("/")) {
    throw new Error(`API paths must be absolute: ${path}`);
  }
  if (FORBIDDEN_PATH_PREFIXES.some((prefix) => path === prefix || path.startsWith(`${prefix}/`))) {
    throw new Error(`Path is outside ${PRODUCT_API}: ${path}`);
  }
  if (!ALLOWED_PATH_PREFIXES.some((prefix) => path === prefix || path.startsWith(`${prefix}/`))) {
    throw new Error(`Path is not part of ${PRODUCT_API}: ${path}`);
  }
}

export function apiUrl(path: string): URL {
  assertSurfacePath(path);
  return new URL(path, `${API_BASE_URL}/`);
}
