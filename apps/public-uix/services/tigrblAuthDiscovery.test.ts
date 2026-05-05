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

describe("tigrblAuthDiscovery", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("loads OIDC discovery from the configured public base URL", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        authorization_endpoint: "https://authn.example.com/authorize",
        token_endpoint: "https://authn.example.com/token",
      }),
    }));

    const discovery = await loadTigrblAuthDiscovery();

    expect(getDiscoveryUrl()).toBe("http://localhost:3000/.well-known/openid-configuration");
    expect(discovery.issuer).toBe("https://authn.example.com");
    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:3000/.well-known/openid-configuration",
      { headers: { Accept: "application/json" } },
    );
  });

  it("builds a generic OIDC config from discovery metadata", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        authorization_endpoint: "https://authn.example.com/authorize",
        token_endpoint: "https://authn.example.com/token",
        userinfo_endpoint: "https://authn.example.com/userinfo",
      }),
    }));

    const config = await buildTigrblAuthOidcConfig("public-uix");

    expect(config.clientId).toBe("public-uix");
    expect(config.authority).toBe("https://authn.example.com");
    expect(config.authorizationEndpoint).toBe("https://authn.example.com/authorize");
    expect(config.tokenEndpoint).toBe("https://authn.example.com/token");
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
          registration_endpoint: "https://authn.example.com/register",
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
      "https://authn.example.com/register",
      expect.objectContaining({ method: "POST" }),
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

  it("builds a discovered logout URL when end-session is available", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        issuer: "https://authn.example.com",
        end_session_endpoint: "https://authn.example.com/logout",
      }),
    }));

    await expect(getDiscoveredLogoutUrl()).resolves.toBe(
      "https://authn.example.com/logout?post_logout_redirect_uri=http%3A%2F%2Flocalhost%3A3000%2F%23%2Flogin",
    );
  });
});
