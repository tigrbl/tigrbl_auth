import { beforeEach, describe, expect, it, vi } from "vitest";

import {
  buildTigrblAuthOidcConfig,
  getDiscoveryUrl,
  getDiscoveredLogoutUrl,
  hasEndpoint,
  loadTigrblAuthDiscovery,
  postDiscoveredJson,
  safeProblemMessage,
} from "./tigrblAuthDiscovery";

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

describe("tigrblAuthDiscovery", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    vi.stubGlobal("sessionStorage", createStorage());
  });

  it("loads OIDC discovery from the configured public base URL", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        authorization_endpoint: "http://localhost:3000/authorize",
        token_endpoint: "http://localhost:3000/token",
      }),
    }));

    const discovery = await loadTigrblAuthDiscovery();

    expect(getDiscoveryUrl()).toBe("http://localhost:3000/.well-known/openid-configuration");
    expect(discovery.issuer).toBe("https://authn.example.com");
    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:3000/.well-known/openid-configuration",
      { credentials: "include", headers: { Accept: "application/json" } },
    );
  });

  it("builds a generic OIDC config from discovery metadata", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        authorization_endpoint: "http://localhost:3000/authorize",
        token_endpoint: "http://localhost:3000/token",
        userinfo_endpoint: "http://localhost:3000/userinfo",
      }),
    }));

    const config = await buildTigrblAuthOidcConfig("public-uix");

    expect(config.clientId).toBe("public-uix");
    expect(config.authority).toBe("https://authn.example.com");
    expect(config.loginEndpoint).toBe("http://localhost:3000/login");
    expect(config.authorizationEndpoint).toBe("http://localhost:3000/authorize");
    expect(config.tokenEndpoint).toBe("http://localhost:3000/token");
    expect(config.redirectUri).toBe("http://localhost:3000/#/callback");
  });

  it("gates UI actions by discovered endpoint availability", () => {
    expect(hasEndpoint({ issuer: "https://authn.example.com", registration_endpoint: "/register" }, "registration_endpoint")).toBe(true);
    expect(hasEndpoint({ issuer: "https://authn.example.com" }, "registration_endpoint")).toBe(false);
  });

  it("posts UI actions only when the endpoint is discovered", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          issuer: "https://authn.example.com",
          registration_endpoint: "http://localhost:3000/register",
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ id: "user-1" }),
      });
    vi.stubGlobal("fetch", fetchMock);

    await expect(postDiscoveredJson("registration_endpoint", "registration", { email: "user@example.com" })).resolves.toEqual({ id: "user-1" });

    expect(fetchMock).toHaveBeenLastCalledWith(
      "http://localhost:3000/register",
      expect.objectContaining({
        method: "POST",
        credentials: "include",
        headers: expect.objectContaining({
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRF-Token": expect.any(String),
          "X-Requested-With": "XMLHttpRequest",
        }),
      }),
    );
  });

  it("blocks unavailable public actions with a safe message", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ issuer: "https://authn.example.com" }),
    }));

    await expect(postDiscoveredJson("registration_endpoint", "registration", {})).rejects.toThrow(
      "registration is not available from the discovered tigrbl_auth endpoints.",
    );
  });

  it("redacts unsafe problem details before display", () => {
    expect(safeProblemMessage("Bearer abc.def.ghi failed at https://authn.example.com/token")).toBe(
      "Bearer [redacted-token] failed at [redacted-url]",
    );
  });

  it("reuses a session CSRF token for discovered public POST actions", async () => {
    const storage = createStorage();
    vi.stubGlobal("sessionStorage", storage);
    storage.setItem("tigrbl_auth_public_csrf", "csrf-fixed");

    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          issuer: "https://authn.example.com",
          registration_endpoint: "http://localhost:3000/register",
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ id: "user-1" }),
      });
    vi.stubGlobal("fetch", fetchMock);

    await postDiscoveredJson("registration_endpoint", "registration", { email: "user@example.com" });

    expect(fetchMock).toHaveBeenLastCalledWith(
      "http://localhost:3000/register",
      expect.objectContaining({
        headers: expect.objectContaining({
          "X-CSRF-Token": "csrf-fixed",
        }),
      }),
    );
  });

  it("rejects cross-origin discovered browser POST targets", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        registration_endpoint: "https://admin.example.com/register",
      }),
    }));

    await expect(postDiscoveredJson("registration_endpoint", "registration", {})).rejects.toThrow(
      "registration is not available from the discovered tigrbl_auth endpoints.",
    );
  });

  it("builds a discovered logout URL when end-session is available", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        end_session_endpoint: "http://localhost:3000/logout",
      }),
    }));

    await expect(getDiscoveredLogoutUrl()).resolves.toBe(
      "http://localhost:3000/logout?post_logout_redirect_uri=http%3A%2F%2Flocalhost%3A3000%2F%23%2Flogin",
    );
  });

  it("rejects discovered logout endpoints outside the governed public origin", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        end_session_endpoint: "https://admin.example.com/logout",
      }),
    }));

    await expect(getDiscoveredLogoutUrl()).resolves.toBeNull();
  });
});
