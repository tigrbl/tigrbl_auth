import { describe, expect, it } from "vitest";
import { MyAccountClient } from "./myAccountClient";

describe("MyAccountClient", () => {
  it("uses global fetch without detaching the browser binding", async () => {
    const originalFetch = globalThis.fetch;
    const calls: Array<RequestInfo | URL> = [];
    globalThis.fetch = async (input, init) => {
      calls.push(input);
      expect(init?.credentials).toBe("include");
      return new Response(JSON.stringify({ id: "u1", tenant_id: "t1", username: "alice", email: "a@example.test", is_active: true, must_change_password: false, roles: [] }), {
        status: 200,
        headers: { "content-type": "application/json" }
      });
    };

    try {
      const client = new MyAccountClient("http://example.test");
      await client.profile();
    } finally {
      globalThis.fetch = originalFetch;
    }

    expect(calls).toEqual(["http://example.test/account/profile"]);
  });

  it("calls the current-subject profile endpoint with credentials", async () => {
    const requests: Array<RequestInfo | URL> = [];
    const client = new MyAccountClient("http://example.test", async (input, init) => {
      requests.push(input);
      expect(init?.credentials).toBe("include");
      return new Response(JSON.stringify({ id: "u1", tenant_id: "t1", username: "alice", email: "a@example.test", is_active: true, must_change_password: false, roles: [] }), {
        status: 200,
        headers: { "content-type": "application/json" }
      });
    });

    const profile = await client.profile();

    expect(profile.username).toBe("alice");
    expect(requests).toEqual(["http://example.test/account/profile"]);
  });
});
