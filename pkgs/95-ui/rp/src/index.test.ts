import { describe, expect, it } from "vitest";
import {
  BrowserMemorySession,
  RPError,
  assertBrowserSafeConfig,
  buildAuthorizationUrl,
  buildLogoutUrl,
  createLoginRequest,
  nodeVersionMatrix,
  npmProvenanceManifest,
  parseCallback,
  pkceS256,
  sharedVectorManifest,
  validateBrowserStoragePolicy,
  validateCallbackState,
  validateDiscoveryMetadata,
  validateIdTokenClaims,
} from "./index";

const config = {
  issuer: "https://issuer.example.test/",
  clientId: "browser-rp",
  redirectUri: "https://app.example.test/callback",
  postLogoutRedirectUri: "https://app.example.test/logout",
  scopes: ["openid", "profile"],
};

describe("@tigrbl-auth/rp", () => {
  it("builds browser-safe authorization URLs with PKCE", async () => {
    const login = await createLoginRequest(config);
    const url = await buildAuthorizationUrl(config, "https://issuer.example.test/authorize", login);
    const parsed = new URL(url);

    expect(parsed.searchParams.get("response_type")).toBe("code");
    expect(parsed.searchParams.get("client_id")).toBe("browser-rp");
    expect(parsed.searchParams.get("redirect_uri")).toBe(config.redirectUri);
    expect(parsed.searchParams.get("code_challenge_method")).toBe("S256");
    expect(parsed.searchParams.get("code_challenge")).toBe(await pkceS256(login.codeVerifier));
  });

  it("parses callbacks, validates state, discovery, ID token claims, logout, and memory session", () => {
    const callback = parseCallback("https://app.example.test/callback?code=abc&state=state-1&iss=https://issuer.example.test");
    const session = new BrowserMemorySession("memory");
    session.set({ accessToken: "at", idToken: "id" });

    expect(validateCallbackState(callback, "state-1").code).toBe("abc");
    expect(
      validateDiscoveryMetadata(
        {
          issuer: "https://issuer.example.test",
          authorization_endpoint: "https://issuer.example.test/authorize",
          token_endpoint: "https://issuer.example.test/token",
          jwks_uri: "https://issuer.example.test/jwks.json",
        },
        config.issuer,
      ).token_endpoint,
    ).toContain("/token");
    expect(
      validateIdTokenClaims(
        { iss: "https://issuer.example.test", sub: "user:123", aud: ["browser-rp"], exp: 9999999999, nonce: "nonce" },
        config,
        "nonce",
      ).sub,
    ).toBe("user:123");
    expect(buildLogoutUrl(config, "https://issuer.example.test/logout", "id", "bye")).toContain("post_logout_redirect_uri=");
    expect(session.get()?.accessToken).toBe("at");
    session.clear();
    expect(session.get()).toBeNull();
  });

  it("exposes node matrix and npm provenance manifests", () => {
    expect(nodeVersionMatrix()).toEqual(["@tigrbl-auth/rp@node22", "@tigrbl-auth/rp@node24", "@tigrbl-auth/rp@node26"]);
    expect(npmProvenanceManifest()).toMatchObject({
      package: "@tigrbl-auth/rp",
      workflow: "monorepo-npm-package-release.yml",
      provenance: true,
    });
    expect(sharedVectorManifest().callbackRequiredParams).toBe("code,state");
  });

  it("rejects unsafe browser and validation inputs", async () => {
    expect(() => assertBrowserSafeConfig({ ...config, clientSecret: "secret" })).toThrow(RPError);
    expect(() => validateBrowserStoragePolicy("localStorage")).toThrow(/localStorage/u);
    expect(() => parseCallback("https://app.example.test/callback?error=access_denied")).toThrow(/access_denied/u);
    expect(() => validateCallbackState({ code: "abc", state: "bad" }, "state-1")).toThrow(/state/u);
    expect(() =>
      validateDiscoveryMetadata(
        {
          issuer: "https://issuer.example.test",
          authorization_endpoint: "",
          token_endpoint: "https://issuer.example.test/token",
          jwks_uri: "https://issuer.example.test/jwks.json",
        },
        config.issuer,
      ),
    ).toThrow(/authorization_endpoint/u);
    expect(() =>
      validateIdTokenClaims(
        { iss: "https://issuer.example.test", sub: "user:123", aud: ["other"], exp: 9999999999, nonce: "nonce" },
        config,
        "nonce",
      ),
    ).toThrow(/audience/u);
  });
});
