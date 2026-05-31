import { describe, expect, it } from "vitest";
import { PlatformAdminClient } from "./platformAdminClient";

function jsonResponse(payload: unknown) {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "content-type": "application/json" }
  });
}

describe("platform-admin tenant CRUD workflows", () => {
  it("exposes the expected tenant and platform identity mutation methods", () => {
    const client = new PlatformAdminClient();

    for (const method of [
      "tenants",
      "tenant",
      "createTenant",
      "updateTenant",
      "enableTenant",
      "disableTenant",
      "deleteTenant",
      "identities",
      "createIdentity",
      "updateIdentity",
      "deleteIdentity"
    ] as const) {
      expect(typeof client[method]).toBe("function");
    }
  });

  it("sends tenant lifecycle mutations to platform-admin paths with credentials", async () => {
    const calls: Array<{ body?: unknown; method: string; path: string }> = [];
    const client = new PlatformAdminClient(async (input, init) => {
      calls.push({
        body: init?.body ? JSON.parse(String(init.body)) : undefined,
        method: init?.method ?? "GET",
        path: new URL(String(input)).pathname
      });
      expect(init?.credentials).toBe("include");
      return jsonResponse({ id: "tenant-1", slug: "acme", name: "Acme", email: "ops@acme.test" });
    });

    await client.createTenant({ slug: "acme", name: "Acme", email: "ops@acme.test" });
    await client.updateTenant("tenant-1", { name: "Acme Updated" });
    await client.disableTenant("tenant-1");
    await client.deleteTenant("tenant-1");

    expect(calls).toEqual([
      { body: { slug: "acme", name: "Acme", email: "ops@acme.test" }, method: "POST", path: "/admin/tenant" },
      { body: { name: "Acme Updated" }, method: "PATCH", path: "/admin/tenant/tenant-1" },
      { body: { is_active: false }, method: "PATCH", path: "/admin/tenant/tenant-1" },
      { body: undefined, method: "DELETE", path: "/admin/tenant/tenant-1" }
    ]);
  });

  it("encodes resource identifiers and surfaces structured API errors", async () => {
    const paths: string[] = [];
    const client = new PlatformAdminClient(async (input) => {
      paths.push(String(input));
      if (paths.length === 1) {
        return jsonResponse({ id: "tenant/one two", slug: "acme", name: "Acme" });
      }
      return new Response(JSON.stringify({ detail: "tenant is locked" }), {
        status: 409,
        statusText: "Conflict",
        headers: { "content-type": "application/json" }
      });
    });

    await expect(client.tenant("tenant/one two")).resolves.toMatchObject({ id: "tenant/one two" });
    await expect(client.updateTenant("tenant/one two", { name: "Blocked" })).rejects.toThrow("tenant is locked");

    expect(paths[0]).toContain("/admin/tenant/tenant%2Fone%20two");
    expect(paths[1]).toContain("/admin/tenant/tenant%2Fone%20two");
  });
});
