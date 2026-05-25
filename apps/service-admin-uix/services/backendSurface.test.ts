import { describe, expect, it } from "vitest";
import { API_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, apiUrl, assertSurfacePath } from "./backendSurface";

describe("service admin API boundary", () => {
  it("uses exactly the service admin API base URL variable", () => {
    expect(API_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_SERVICE_ADMIN_API_BASE_URL");
  });

  it("permits service identity paths and rejects tenant/human login paths", () => {
    expect(apiUrl("/service").pathname).toBe("/service");
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
  });
});
