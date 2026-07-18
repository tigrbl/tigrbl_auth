import { describe, expect, it } from "vitest";
import { BACKEND_APP_BASE_URL, BACKEND_APP_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, backendAppUrl, assertSurfacePath } from "./backendSurface";

describe("tenant admin API boundary", () => {
  it("uses exactly the tenant admin backend-app base URL variable", () => {
    expect(BACKEND_APP_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL");
    expect(BACKEND_APP_BASE_URL).toBe("http://localhost:8016");
  });

  it("permits tenant-scoped paths and rejects platform tenant lifecycle paths", () => {
    expect(backendAppUrl("/user").pathname).toBe("/user");
    expect(backendAppUrl("/rpc").pathname).toBe("/rpc");
    expect(backendAppUrl("/admin/auth/login").pathname).toBe("/admin/auth/login");
    expect(() => assertSurfacePath("/auth/admin/login")).toThrow(/not part/);
    expect(() => assertSurfacePath("/admin/tenant")).toThrow(/not part/);
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
  });
});
