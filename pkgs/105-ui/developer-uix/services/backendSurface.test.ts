import { describe, expect, it } from "vitest";
import { BACKEND_APP_BASE_URL, BACKEND_APP_BASE_URL_ENV, FORBIDDEN_PATH_PREFIXES, backendAppUrl, assertSurfacePath } from "./backendSurface";

describe("developer API boundary", () => {
  it("uses exactly the developer backend-app base URL variable", () => {
    expect(BACKEND_APP_BASE_URL_ENV).toBe("VITE_TIGRBL_AUTH_DEVELOPER_BACKEND_APP_BASE_URL");
    expect(BACKEND_APP_BASE_URL).toBe("http://localhost:8017");
  });

  it("permits client registration paths and rejects tenant/service operations", () => {
    expect(backendAppUrl("/register").pathname).toBe("/register");
    expect(backendAppUrl("/.well-known/openid-configuration").pathname).toBe("/.well-known/openid-configuration");
    expect(() => assertSurfacePath("/admin/tenant")).toThrow(/not part/);
    for (const path of FORBIDDEN_PATH_PREFIXES) {
      expect(() => assertSurfacePath(path)).toThrow(/outside/);
    }
  });
});
