import { describe, expect, it } from "vitest";
import { BACKEND_APP_BASE_URL, BACKEND_APP_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, backendAppUrl, assertSurfacePath } from "./backendSurface";

describe("service admin API boundary", () => {
  it("uses exactly the service admin backend-app base URL variable", () => {
    expect(BACKEND_APP_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_SERVICE_ADMIN_BACKEND_APP_BASE_URL");
    expect(BACKEND_APP_BASE_URL).toBe("http://localhost:8018");
  });

  it("permits service identity paths and rejects tenant/human login paths", () => {
    expect(backendAppUrl("/service").pathname).toBe("/service");
    expect(backendAppUrl("/introspect").pathname).toBe("/introspect");
    expect(() => assertSurfacePath("/admin/tenant")).toThrow(/not part/);
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
  });
});
