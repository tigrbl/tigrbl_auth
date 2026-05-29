import { describe, expect, it } from "vitest";
import { API_BASE_URL, API_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, apiUrl, assertSurfacePath } from "./backendSurface";

describe("developer API boundary", () => {
  it("uses exactly the developer API base URL variable", () => {
    expect(API_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL");
    expect(API_BASE_URL).toBe("http://localhost:8017");
  });

  it("permits client registration paths and rejects tenant/service operations", () => {
    expect(apiUrl("/register").pathname).toBe("/register");
    expect(apiUrl("/.well-known/openid-configuration").pathname).toBe("/.well-known/openid-configuration");
    expect(() => assertSurfacePath("/admin/tenant")).toThrow(/not part/);
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
  });
});
