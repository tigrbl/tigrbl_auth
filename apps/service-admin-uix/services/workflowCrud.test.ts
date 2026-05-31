import { describe, expect, it } from "vitest";
import { ServiceAdminClient } from "./serviceAdminClient";

function jsonResponse(payload: unknown) {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "content-type": "application/json" }
  });
}

describe("service-admin workload CRUD workflows", () => {
  it("exposes service, service-key, API-key, token, and validation workflow methods", () => {
    const client = new ServiceAdminClient();

    for (const method of [
      "services",
      "createService",
      "updateService",
      "deleteService",
      "serviceKeys",
      "createServiceKey",
      "revokeServiceKey",
      "apiKeys",
      "createApiKey",
      "updateApiKey",
      "revokeApiKey",
      "tokenRecords",
      "resourceMetadata",
      "introspect"
    ] as const) {
      expect(typeof client[method]).toBe("function");
    }
  });

  it("sends service and credential mutations to service-admin paths with credentials", async () => {
    const calls: Array<{ body?: unknown; method: string; path: string }> = [];
    const client = new ServiceAdminClient(async (input, init) => {
      calls.push({
        body: init?.body ? JSON.parse(String(init.body)) : undefined,
        method: init?.method ?? "GET",
        path: new URL(String(input)).pathname
      });
      expect(init?.credentials).toBe("include");
      return jsonResponse({ id: "service-1", name: "orders" });
    });

    await client.createService({ name: "orders", subject: "svc:orders" });
    await client.createServiceKey({ service_id: "service-1", kid: "kid-1" });
    await client.createApiKey({ service_id: "service-1", name: "deploy", scopes: ["orders:read"] });
    await client.revokeApiKey("api-key-1");

    expect(calls).toEqual([
      { body: { name: "orders", subject: "svc:orders" }, method: "POST", path: "/service" },
      { body: { service_id: "service-1", kid: "kid-1" }, method: "POST", path: "/servicekey" },
      { body: { service_id: "service-1", name: "deploy", scopes: ["orders:read"] }, method: "POST", path: "/apikey" },
      { body: undefined, method: "DELETE", path: "/apikey/api-key-1" }
    ]);
  });
});
