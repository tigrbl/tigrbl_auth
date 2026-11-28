import { readFileSync } from "node:fs";
import {
  authorizationOptions,
  resolveEndSessionEndpoint,
  validateLogoutReturn,
  type LoginIntent,
} from "./index.js";
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

describe("@tbauth/client-oidc-relying-party", () => {
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
    expect(nodeVersionMatrix()).toEqual(["@tbauth/client-oidc-relying-party@node22", "@tbauth/client-oidc-relying-party@node24", "@tbauth/client-oidc-relying-party@node26"]);
    expect(npmProvenanceManifest()).toMatchObject({
      package: "@tbauth/client-oidc-relying-party",
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

const sessionVectors = JSON.parse(readFileSync(
  new URL("../../../../tests/fixtures/oidc-rp-session-vectors.json", import.meta.url),
  "utf-8",
)) as {
  intents: { intent: LoginIntent; acrValues?: string; expected?: Record<string, string>; error?: boolean }[];
  discovery: { endpoint?: string; expected?: string; error?: boolean; metadataIssuer?: string }[];
  logout: { url: string; registered?: string; accepted: boolean }[];
};

for (const vector of sessionVectors.intents) {
  it(`uses shared authorization intent vector ${JSON.stringify(vector)}`, () => {
    const resolve = () => authorizationOptions(vector.intent, vector.acrValues);
    if (vector.error) expect(resolve).toThrow();
    else expect(resolve()).toEqual(vector.expected);
  });
}

for (const vector of sessionVectors.logout) {
  it(`uses shared logout return vector ${vector.url}`, () => {
    expect(validateLogoutReturn(
      vector.url, vector.registered ?? "https://rp.example/out", "browser",
    )).toBe(vector.accepted);
  });
}


for (const vector of sessionVectors.discovery) {
  it(`uses shared issuer end-session discovery vector ${JSON.stringify(vector)}`, () => {
    const issuer = "https://authority.example";
    const discover = () => resolveEndSessionEndpoint({
      issuer: vector.metadataIssuer ?? issuer,
      authorization_endpoint: issuer + "/authorize",
      token_endpoint: issuer + "/token",
      jwks_uri: issuer + "/jwks",
      end_session_endpoint: vector.endpoint,
    }, issuer);
    if (vector.error) expect(discover).toThrow();
    else expect(discover()).toBe(vector.expected);
  });
}
