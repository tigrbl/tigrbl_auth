import { describe, expect, it } from "vitest";
import { API_BASE_URL, API_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, apiUrl, assertSurfacePath } from "./backendSurface";

describe("tenant admin API boundary", () => {
  it("uses exactly the tenant admin API base URL variable", () => {
    expect(API_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_TENANT_ADMIN_API_BASE_URL");
    expect(API_BASE_URL).toBe("http://localhost:8016");
  });

  it("permits tenant-scoped paths and rejects platform tenant lifecycle paths", () => {
    expect(apiUrl("/user").pathname).toBe("/user");
    expect(apiUrl("/rpc").pathname).toBe("/rpc");
    expect(apiUrl("/admin/auth/login").pathname).toBe("/admin/auth/login");
    expect(() => assertSurfacePath("/auth/admin/login")).toThrow(/not part/);
    expect(() => assertSurfacePath("/admin/tenant")).toThrow(/not part/);
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
  });
});
