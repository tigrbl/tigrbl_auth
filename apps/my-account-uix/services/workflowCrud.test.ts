import { describe, expect, it } from "vitest";
import { MyAccountClient } from "./myAccountClient";

function jsonResponse(payload: unknown) {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "content-type": "application/json" }
  });
}

describe("my-account self-service mutation workflows", () => {
  it("exposes current-subject profile, credential, session, app, and consent methods", () => {
    const client = new MyAccountClient("http://example.test");

    for (const method of [
      "profile",
      "updateProfile",
      "changePassword",
      "sessions",
      "revokeSession",
      "authorizedApps",
      "revokeAuthorizedApp",
      "consents",
      "revokeConsent"
    ] as const) {
      expect(typeof client[method]).toBe("function");
    }
  });

  it("sends current-subject mutations only to /account paths with credentials", async () => {
    const calls: Array<{ body?: unknown; method: string; path: string }> = [];
    const client = new MyAccountClient("http://example.test", async (input, init) => {
      calls.push({
        body: init?.body ? JSON.parse(String(init.body)) : undefined,
        method: init?.method ?? "GET",
        path: new URL(String(input)).pathname
      });
      expect(init?.credentials).toBe("include");
      return jsonResponse({ status: "ok", id: "subject-1" });
    });

    await client.updateProfile({ email: "alice@example.test" });
    await client.changePassword("old-pass", "new-pass");
    await client.revokeSession("session-1");
    await client.revokeConsent("consent-1");

    expect(calls).toEqual([
      { body: { email: "alice@example.test" }, method: "PATCH", path: "/account/profile" },
      { body: { current_password: "old-pass", new_password: "new-pass" }, method: "POST", path: "/account/password/change" },
      { body: undefined, method: "DELETE", path: "/account/sessions/session-1" },
      { body: undefined, method: "DELETE", path: "/account/consents/consent-1" }
    ]);
  });
});
