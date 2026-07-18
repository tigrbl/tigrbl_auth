export const BACKEND_APP = "tigrbl-auth-backend-app-tenant-admin";
export const BACKEND_APP_BASE_URL_ENV = "VITE_TIGRBL_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL";
export const BACKEND_APP_BASE_URL = (import.meta.env.VITE_TIGRBL_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL ?? "http://localhost:8016").replace(/\/+$/, "");
export const SURFACE_PURPOSE = "Tenant-scoped control plane for users, admins, JWKS, and local policy.";

export const FORBIDDEN_PATH_PREFIXES = ["/login", "/authorize", "/token", "/register", "/tenant"];
export const ALLOWED_PATH_PREFIXES = ["/rpc", "/user", "/client", "/clientregistration", "/consent", "/admin/auth", "/keyrotationevent"];

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
