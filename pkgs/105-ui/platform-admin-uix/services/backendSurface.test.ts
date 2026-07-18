import { describe, expect, it } from "vitest";
import { BACKEND_APP_BASE_URL, BACKEND_APP_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, backendAppUrl, assertSurfacePath } from "./backendSurface";

describe("platform admin API boundary", () => {
  it("uses exactly the platform admin backend-app base URL variable", () => {
    expect(BACKEND_APP_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_PLATFORM_ADMIN_BACKEND_APP_BASE_URL");
    expect(BACKEND_APP_BASE_URL).toBe("http://localhost:8015");
  });

  it("permits platform control-plane paths and rejects public login paths", () => {
    expect(backendAppUrl("/admin/tenant").pathname).toBe("/admin/tenant");
    expect(backendAppUrl("/admin/realm").pathname).toBe("/admin/realm");
    expect(backendAppUrl("/admin/realm/demo/tenant").pathname).toBe("/admin/realm/demo/tenant");
    expect(backendAppUrl("/admin/identities").pathname).toBe("/admin/identities");
    expect(backendAppUrl("/admin/identities?tenant_id=public").pathname).toBe("/admin/identities");
    expect(() => assertSurfacePath("/admin/identity")).toThrow(/not part/);
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
    expect(() => assertSurfacePath("/rpc")).toThrow(/not part/);
  });
});
