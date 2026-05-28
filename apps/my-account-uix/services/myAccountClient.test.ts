import { describe, expect, it } from "vitest";
import { MyAccountClient } from "./myAccountClient";

describe("MyAccountClient", () => {
  it("calls the current-subject profile endpoint with credentials", async () => {
    const requests: RequestInfo[] = [];
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
