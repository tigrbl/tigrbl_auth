import { describe, expect, it } from "vitest";
import { PlatformAdminClient } from "./platformAdminClient";
import { assertSurfacePath } from "./backendSurface";

describe("PlatformAdminClient", () => {
  it("calls platform-admin routes with browser credentials", async () => {
    const calls: string[] = [];
    const client = new PlatformAdminClient(async (input, init) => {
      calls.push(String(input));
      expect(init?.credentials).toBe("include");
      return new Response(JSON.stringify([{ id: "t1", slug: "alpha", name: "Alpha", email: "alpha@example.test" }]), {
        status: 200,
        headers: { "content-type": "application/json" }
      });
    });

    const tenants = await client.tenants();

    expect(tenants[0].slug).toBe("alpha");
    expect(calls[0]).toContain("/admin/tenant");
  });

  it("rejects public login and token routes through the surface guard", () => {
    const client = new PlatformAdminClient();

    expect(() => client.baseUrl()).not.toThrow();
    expect(() => assertSurfacePath("/login")).toThrow(/outside/);
    expect(() => assertSurfacePath("/token")).toThrow(/outside/);
    expect(() => assertSurfacePath("/rpc")).toThrow(/not part/);
  });
});
