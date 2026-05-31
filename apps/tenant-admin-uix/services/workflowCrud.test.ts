import { describe, expect, it } from "vitest";
import { TenantAdminClient } from "./tenantAdminClient";

function jsonResponse(payload: unknown) {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "content-type": "application/json" }
  });
}

describe("tenant-admin identity CRUD workflows", () => {
  it("exposes tenant-scoped identity, client, consent, and key-rotation mutation methods", () => {
    const client = new TenantAdminClient();

    for (const method of [
      "identities",
      "createIdentity",
      "updateIdentity",
      "lockIdentity",
      "unlockIdentity",
      "deleteIdentity",
      "clients",
      "createClient",
      "updateClient",
      "deleteClient",
      "consents",
      "revokeConsent",
      "keyEvents",
      "triggerKeyRotation"
    ] as const) {
      expect(typeof client[method]).toBe("function");
    }
  });

  it("sends tenant identity lifecycle mutations to tenant-admin paths with credentials", async () => {
    const calls: Array<{ body?: unknown; method: string; path: string }> = [];
    const client = new TenantAdminClient(async (input, init) => {
      calls.push({
        body: init?.body ? JSON.parse(String(init.body)) : undefined,
        method: init?.method ?? "GET",
        path: new URL(String(input)).pathname
      });
      expect(init?.credentials).toBe("include");
      return jsonResponse({ id: "user-1", username: "alice", email: "alice@example.test" });
    });

    await client.createIdentity({ username: "alice", email: "alice@example.test", password: "Start123!" });
    await client.lockIdentity("user-1");
    await client.unlockIdentity("user-1");
    await client.deleteIdentity("user-1");

    expect(calls).toEqual([
      { body: { username: "alice", email: "alice@example.test", password: "Start123!" }, method: "POST", path: "/user" },
      { body: { is_active: false }, method: "PATCH", path: "/user/user-1" },
      { body: { is_active: true }, method: "PATCH", path: "/user/user-1" },
      { body: undefined, method: "DELETE", path: "/user/user-1" }
    ]);
  });
});
