import { describe, expect, it } from "vitest";
import { DeveloperClient } from "./developerClient";

function jsonResponse(payload: unknown) {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "content-type": "application/json" }
  });
}

describe("developer client CRUD workflows", () => {
  it("exposes application and client-registration workflow methods", () => {
    const client = new DeveloperClient();

    for (const method of [
      "applications",
      "application",
      "updateApplication",
      "deleteApplication",
      "clientRegistrations",
      "clientRegistration",
      "updateClientRegistration",
      "deleteClientRegistration",
      "registerClient",
      "discovery"
    ] as const) {
      expect(typeof client[method]).toBe("function");
    }
  });

  it("sends client registration mutations to developer-api paths with credentials", async () => {
    const calls: Array<{ body?: unknown; method: string; path: string }> = [];
    const client = new DeveloperClient(async (input, init) => {
      calls.push({
        body: init?.body ? JSON.parse(String(init.body)) : undefined,
        method: init?.method ?? "GET",
        path: new URL(String(input)).pathname
      });
      expect(init?.credentials).toBe("include");
      return jsonResponse({ id: "client-1", client_id: "client-1", client_name: "Portal" });
    });

    await client.registerClient({ client_name: "Portal", redirect_uris: ["https://app.example.test/callback"] });
    await client.updateClientRegistration("reg-1", { client_name: "Portal v2" });
    await client.deleteClientRegistration("reg-1");

    expect(calls).toEqual([
      { body: { client_name: "Portal", redirect_uris: ["https://app.example.test/callback"] }, method: "POST", path: "/register" },
      { body: { client_name: "Portal v2" }, method: "PATCH", path: "/clientregistration/reg-1" },
      { body: undefined, method: "DELETE", path: "/clientregistration/reg-1" }
    ]);
  });
});
