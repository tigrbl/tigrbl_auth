import { describe, expect, it } from "vitest";
import { assertSurfacePath, createSurfaceUrl } from "./surfaceBoundary";

const boundary = {
  backendApp: "example-backend",
  allowedPathPrefixes: ["/account", "/.well-known"],
  forbiddenPathPrefixes: ["/admin", "/tenant"]
};

describe("surface boundary", () => {
  it("permits configured paths", () => {
    expect(createSurfaceUrl("http://localhost:8000", "/account/profile", boundary).href).toBe("http://localhost:8000/account/profile");
  });

  it("rejects forbidden and unknown paths", () => {
    expect(() => assertSurfacePath("/admin/tenant", boundary)).toThrow(/outside/);
    expect(() => assertSurfacePath("/client", boundary)).toThrow(/not part/);
    expect(() => assertSurfacePath("relative", boundary)).toThrow(/absolute/);
  });
});
