import { beforeEach, describe, expect, it, vi } from "vitest";

import { GenericAdapter } from "./GenericAdapter";

const createStorage = () => {
  const values = new Map<string, string>();
  return {
    getItem: vi.fn((key: string) => values.get(key) ?? null),
    setItem: vi.fn((key: string, value: string) => {
      values.set(key, value);
    }),
    removeItem: vi.fn((key: string) => {
      values.delete(key);
    }),
  };
};

describe("GenericAdapter", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("exchanges the authorization code without persisting bearer tokens", async () => {
    const localStorage = createStorage();
    localStorage.setItem("oidc_session_GenericAdapter", JSON.stringify({
      state: "state-1",
      verifier: "verifier-1",
      timestamp: Date.now(),
    }));

    vi.stubGlobal("localStorage", localStorage);
    vi.stubGlobal("window", {
      location: {
        search: "?code=code-1&state=state-1",
        hash: "#/callback?code=code-1&state=state-1",
      },
    });

    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ access_token: "access-token-1" }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          sub: "user-1",
          email: "user@example.com",
          name: "User One",
          email_verified: true,
        }),
      });
    vi.stubGlobal("fetch", fetchMock);

    const adapter = new GenericAdapter({
      clientId: "public-uix",
      redirectUri: "http://localhost:3000/#/callback",
      scope: "openid profile email",
      authority: "http://localhost:3000",
      tokenEndpoint: "http://localhost:3000/token",
      userinfoEndpoint: "http://localhost:3000/userinfo",
    });

    const user = await adapter.handleCallback();

    expect(user.email).toBe("user@example.com");
    expect(fetchMock).toHaveBeenNthCalledWith(
      2,
      "http://localhost:3000/userinfo",
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer access-token-1",
        }),
      }),
    );
    expect(localStorage.removeItem).toHaveBeenCalledWith("oidc_session_GenericAdapter");
    expect(localStorage.setItem).toHaveBeenCalledTimes(1);
  });

  it("fails closed when the callback state does not match the saved session", async () => {
    const localStorage = createStorage();
    localStorage.setItem("oidc_session_GenericAdapter", JSON.stringify({
      state: "expected-state",
      verifier: "verifier-1",
      timestamp: Date.now(),
    }));

    vi.stubGlobal("localStorage", localStorage);
    vi.stubGlobal("window", {
      location: {
        search: "?code=code-1&state=wrong-state",
        hash: "#/callback?code=code-1&state=wrong-state",
      },
    });

    const adapter = new GenericAdapter({
      clientId: "public-uix",
      redirectUri: "http://localhost:3000/#/callback",
      scope: "openid profile email",
      authority: "http://localhost:3000",
      tokenEndpoint: "http://localhost:3000/token",
    });

    await expect(adapter.handleCallback()).rejects.toThrow(
      "Identity verification failed: State mismatch or missing code.",
    );
  });

  it("fails visibly when discovery did not provide a userinfo endpoint", async () => {
    const localStorage = createStorage();
    localStorage.setItem("oidc_session_GenericAdapter", JSON.stringify({
      state: "state-1",
      verifier: "verifier-1",
      timestamp: Date.now(),
    }));

    vi.stubGlobal("localStorage", localStorage);
    vi.stubGlobal("window", {
      location: {
        search: "?code=code-1&state=state-1",
        hash: "#/callback?code=code-1&state=state-1",
      },
    });

    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ access_token: "access-token-1" }),
    }));

    const adapter = new GenericAdapter({
      clientId: "public-uix",
      redirectUri: "http://localhost:3000/#/callback",
      scope: "openid profile email",
      authority: "http://localhost:3000",
      tokenEndpoint: "http://localhost:3000/token",
    });

    await expect(adapter.handleCallback()).rejects.toThrow(
      "OIDC discovery did not provide a UserInfo endpoint.",
    );
  });

  it("fails visibly when userinfo rejects the access token", async () => {
    const localStorage = createStorage();
    localStorage.setItem("oidc_session_GenericAdapter", JSON.stringify({
      state: "state-1",
      verifier: "verifier-1",
      timestamp: Date.now(),
    }));

    vi.stubGlobal("localStorage", localStorage);
    vi.stubGlobal("window", {
      location: {
        search: "?code=code-1&state=state-1",
        hash: "#/callback?code=code-1&state=state-1",
      },
    });

    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ access_token: "access-token-1" }),
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ detail: "invalid access token" }),
      }));

    const adapter = new GenericAdapter({
      clientId: "public-uix",
      redirectUri: "http://localhost:3000/#/callback",
      scope: "openid profile email",
      authority: "http://localhost:3000",
      tokenEndpoint: "http://localhost:3000/token",
      userinfoEndpoint: "http://localhost:3000/userinfo",
    });

    await expect(adapter.handleCallback()).rejects.toThrow("invalid access token");
  });

  it("fails visibly when the requested email claim is missing", async () => {
    const localStorage = createStorage();
    localStorage.setItem("oidc_session_GenericAdapter", JSON.stringify({
      state: "state-1",
      verifier: "verifier-1",
      timestamp: Date.now(),
    }));

    vi.stubGlobal("localStorage", localStorage);
    vi.stubGlobal("window", {
      location: {
        search: "?code=code-1&state=state-1",
        hash: "#/callback?code=code-1&state=state-1",
      },
    });

    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ access_token: "access-token-1" }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ sub: "user-1", name: "User One" }),
      }));

    const adapter = new GenericAdapter({
      clientId: "public-uix",
      redirectUri: "http://localhost:3000/#/callback",
      scope: "openid profile email",
      authority: "http://localhost:3000",
      tokenEndpoint: "http://localhost:3000/token",
      userinfoEndpoint: "http://localhost:3000/userinfo",
    });

    await expect(adapter.handleCallback()).rejects.toThrow(
      "UserInfo response did not include the requested email claim.",
    );
  });
});
