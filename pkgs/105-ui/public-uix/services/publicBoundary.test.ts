import { describe, expect, it } from "vitest";

import {
  publicUixBoundaryIntegrity,
  publicUixBoundaryManifest,
} from "./publicBoundary";
import {
  buildBrowserJsonRequestInit,
  parseConsentViewModel,
  resolveTrustedPublicEndpoint,
  safePublicHashPaths,
  sanitizePublicHashTarget,
} from "./publicUxPolicy";
import {
  resolvePublicSessionState,
  serializePublicSessionCookie,
} from "./publicSession";

const BOUNDARY_FEATURE_IDS = new Set([
  "feat:uix-public-shell",
  "feat:uix-public-auth-session",
  "feat:uix-public-login-view",
  "feat:uix-public-logout-view",
  "feat:uix-public-registration-view",
  "feat:uix-public-recovery-view",
  "feat:uix-public-session-continuity",
  "feat:uix-public-openapi-contract-consumption",
  "feat:uix-public-browser-token-handling",
  "feat:uix-public-problem-details-rendering",
  "feat:uix-public-safe-error-disclosure",
  "feat:uix-public-consent-view",
  "feat:uix-public-cookie-session-model",
  "feat:uix-public-csrf-protection",
  "feat:uix-public-origin-and-redirect-constraints",
]);

describe("phase2 public UIX browser security boundary", () => {
  it("T0 inventories all public UIX flow, session, contract, and browser security features", () => {
    const manifest = publicUixBoundaryManifest();

    expect(new Set(Object.keys(manifest))).toEqual(BOUNDARY_FEATURE_IDS);
    expect(manifest["feat:uix-public-login-view"].route).toBe("#/login");
    expect(manifest["feat:uix-public-consent-view"].route).toBe("#/consent");
    expect(manifest["feat:uix-public-cookie-session-model"].category).toBe("session");
    expect(safePublicHashPaths()).toEqual(expect.arrayContaining([
      "#/callback",
      "#/consent",
      "#/forgot-password",
      "#/login",
      "#/profile",
      "#/register",
      "#/reset-password",
    ]));
  });

  it("T1 composes browser-session, CSRF, consent, endpoint, and redirect behavior", () => {
    const state = resolvePublicSessionState(JSON.stringify({
      id: "user-1",
      email: "user@example.test",
      name: "User One",
      isEmailVerified: true,
      mfaEnabled: true,
    }));
    const request = buildBrowserJsonRequestInit({ email: "user@example.test" }, "csrf-fixed");
    const consent = parseConsentViewModel(
      "#/consent?client_name=Portal&scope=openid%20email&continue=%23%2Fprofile&cancel=%23%2Flogin",
    );
    const registrationEndpoint = resolveTrustedPublicEndpoint(
      "/register",
      "registration",
      "https://public.example.test",
    );

    expect(state.isAuthenticated).toBe(true);
    expect(request.credentials).toBe("include");
    expect(request.headers).toMatchObject({
      "X-CSRF-Token": "csrf-fixed",
      "X-Requested-With": "XMLHttpRequest",
    });
    expect(consent.approveTarget).toBe("#/profile");
    expect(consent.cancelTarget).toBe("#/login");
    expect(registrationEndpoint).toBe("https://public.example.test/register");
    expect(serializePublicSessionCookie({ secure: true })).toContain("SameSite=Lax; Secure");
  });

  it("T2 rejects unsafe browser tokens, origins, redirects, endpoints, and malformed sessions", () => {
    const integrity = publicUixBoundaryIntegrity();

    expect(integrity.passed).toBe(true);
    expect(integrity.unsafeTokenFeatureIds).toEqual([]);
    expect(integrity.unsafeErrorFeatureIds).toEqual([]);
    expect(integrity.unconstrainedRedirectFeatureIds).toEqual([]);
    expect(resolvePublicSessionState("{bad json").isAuthenticated).toBe(false);
    expect(sanitizePublicHashTarget("https://evil.example.test/#/profile", "#/login")).toBe("#/login");
    expect(sanitizePublicHashTarget("#/admin", "#/login")).toBe("#/login");
    expect(() =>
      resolveTrustedPublicEndpoint("https://admin.example.test/rpc", "token", "https://public.example.test"),
    ).toThrow("token is not available from the discovered tigrbl_auth endpoints.");
    expect(() =>
      resolveTrustedPublicEndpoint("/rpc/discover", "token", "https://public.example.test"),
    ).toThrow("token is not available from the discovered tigrbl_auth endpoints.");
  });
});
