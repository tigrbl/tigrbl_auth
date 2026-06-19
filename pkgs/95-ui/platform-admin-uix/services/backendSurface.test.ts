import { describe, expect, it } from "vitest";
import { API_BASE_URL, API_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, apiUrl, assertSurfacePath } from "./backendSurface";

describe("platform admin API boundary", () => {
  it("uses exactly the platform admin API base URL variable", () => {
    expect(API_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL");
    expect(API_BASE_URL).toBe("http://localhost:8015");
  });

  it("permits platform control-plane paths and rejects public login paths", () => {
    expect(apiUrl("/admin/tenant").pathname).toBe("/admin/tenant");
    expect(apiUrl("/admin/realm").pathname).toBe("/admin/realm");
    expect(apiUrl("/admin/realm/demo/tenant").pathname).toBe("/admin/realm/demo/tenant");
    expect(apiUrl("/admin/identities").pathname).toBe("/admin/identities");
    expect(apiUrl("/admin/identities?tenant_id=public").pathname).toBe("/admin/identities");
    expect(() => assertSurfacePath("/admin/identity")).toThrow(/not part/);
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
    expect(() => assertSurfacePath("/rpc")).toThrow(/not part/);
  });
});
