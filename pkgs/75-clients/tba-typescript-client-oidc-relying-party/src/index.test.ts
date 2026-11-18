import { describe, expect, it } from "vitest";
import {
  BrowserMemorySession,
  PublicRelyingParty,
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

describe("public OIDC callbacks", () => {
  const issuer = "https://issuer.example.test";

  it.each(["success", "issuer", "audience", "extra-audience", "nonce", "expired", "signature"])(
    "consumes the transaction once and verifies the signed token (%s)",
    async (scenario) => {
      const algorithm = { name: "RSASSA-PKCS1-v1_5", modulusLength: 2048,
        publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" };
      const keys = await crypto.subtle.generateKey(algorithm, true, ["sign", "verify"]);
      const jwk = { ...await crypto.subtle.exportKey("jwk", keys.publicKey), kid: "key-1", alg: "RS256" };
      const metadata = { issuer, authorization_endpoint: issuer + "/authorize",
        token_endpoint: issuer + "/token", jwks_uri: issuer + "/jwks",
        token_endpoint_auth_methods_supported: ["none"] };
      let idToken: string;
      const forms: URLSearchParams[] = [];
      const rp = new PublicRelyingParty(config, async (input, options) => {
        expect(options?.redirect).toBe("error");
        switch (input) {
          case issuer + "/.well-known/openid-configuration": return Response.json(metadata);
          case issuer + "/jwks": return Response.json({ keys: [jwk] });
          case issuer + "/token":
            expect(options?.method).toBe("POST");
            forms.push(options?.body as URLSearchParams);
            return Response.json({ id_token: idToken, access_token: "access", token_type: "Bearer",
              sub: "untrusted-token-response-subject" });
          default: throw new Error("unexpected request");
        }
      });
      const { url, login } = await rp.beginLogin();
      expect(new URL(url).searchParams.get("code_challenge")).toBe(await pkceS256(login.codeVerifier));
      const now = Math.floor(Date.now() / 1000);
      const claims = {
        iss: scenario === "issuer" ? issuer + "/" : issuer,
        aud: scenario === "extra-audience" ? [config.clientId, "other"] : config.clientId,
        ...(scenario === "extra-audience" ? { azp: config.clientId } : {}),
        nonce: scenario === "nonce" ? "other" : login.nonce,
        exp: scenario === "expired" ? now - 1 : now + 60, iat: now, sub: "verified-subject",
      };
      if (scenario === "audience") claims.aud = "other";
      const encode = (value: object) => Buffer.from(JSON.stringify(value)).toString("base64url");
      const signingInput = encode({ alg: "RS256", kid: "key-1" }) + "." + encode(claims);
      const signature = new Uint8Array(await crypto.subtle.sign(
        algorithm.name, keys.privateKey, new TextEncoder().encode(signingInput),
      ));
      if (scenario === "signature") signature[0] ^= 1;
      idToken = signingInput + "." + Buffer.from(signature).toString("base64url");
      const stored = new Map([[login.state, login]]);
      const consume = (state: string) => {
        const transaction = stored.get(state);
        stored.delete(state);
        return transaction;
      };
      const callback = config.redirectUri + "?code=code&state=" + login.state;
      await expect(rp.completeCallback(callback, "another-browser", consume)).rejects.toThrow("state mismatch");
      await expect(rp.completeCallback(callback + "&state=duplicate", login.state, consume)).rejects.toThrow("duplicate");
      expect(forms).toHaveLength(0);
      if (scenario === "success") {
        const result = await rp.completeCallback(callback, login.state, consume);
        expect(result.identity.sub).toBe("verified-subject");
        expect(result.tokens.accessToken).toBe("access");
      } else {
        await expect(rp.completeCallback(callback, login.state, consume)).rejects.toThrow(RPError);
      }
      await expect(rp.completeCallback(callback, login.state, consume)).rejects.toThrow("active login request");
      expect(forms.map(form => Object.fromEntries(form))).toEqual([{
        grant_type: "authorization_code", client_id: config.clientId, redirect_uri: config.redirectUri,
        code: "code", code_verifier: login.codeVerifier,
      }]);
    },
  );
});

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
