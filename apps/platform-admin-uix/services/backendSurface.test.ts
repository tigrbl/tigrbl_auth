import { describe, expect, it } from "vitest";
import { API_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, apiUrl, assertSurfacePath } from "./backendSurface";

describe("platform admin API boundary", () => {
  it("uses exactly the platform admin API base URL variable", () => {
    expect(API_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_BASE_URL");
  });

  it("permits platform control-plane paths and rejects public login paths", () => {
    expect(apiUrl("/rpc").pathname).toBe("/rpc");
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
  });
});
