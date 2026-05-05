import { beforeEach, describe, expect, it, vi } from "vitest";

import {
  buildTigrblAuthOidcConfig,
  getDiscoveryUrl,
  hasEndpoint,
  loadTigrblAuthDiscovery,
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
});
