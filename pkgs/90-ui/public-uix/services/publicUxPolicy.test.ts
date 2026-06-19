import { describe, expect, it, vi } from "vitest";

import {
  buildBrowserJsonRequestInit,
  buildPopupCallbackHash,
  getOrCreateCsrfToken,
  isTrustedBrowserOrigin,
  parseConsentViewModel,
  resolveTrustedPublicEndpoint,
  sanitizePublicHashTarget,
} from "./publicUxPolicy";

const createStorage = () => {
  const values = new Map<string, string>();
  return {
    getItem: vi.fn((key: string) => values.get(key) ?? null),
    setItem: vi.fn((key: string, value: string) => {
      values.set(key, value);
    }),
  };
};

describe("publicUxPolicy", () => {
  it("sanitizes redirects to governed public hash routes", () => {
    expect(sanitizePublicHashTarget("#/profile?tab=security", "#/login")).toBe("#/profile?tab=security");
    expect(sanitizePublicHashTarget("https://evil.example.com/#/profile", "#/login")).toBe("#/login");
    expect(sanitizePublicHashTarget("#/admin", "#/login")).toBe("#/login");
  });

  it("trusts same-origin browser messages and rejects foreign origins", () => {
    expect(isTrustedBrowserOrigin("https://public.example.com", "https://public.example.com")).toBe(true);
    expect(isTrustedBrowserOrigin("https://admin.example.com", "https://public.example.com")).toBe(false);
  });

  it("rejects control-plane and cross-origin discovered endpoints", () => {
    expect(
      resolveTrustedPublicEndpoint("/register", "registration", "https://public.example.com"),
    ).toBe("https://public.example.com/register");

    expect(() =>
      resolveTrustedPublicEndpoint("https://admin.example.com/register", "registration", "https://public.example.com"),
    ).toThrow("registration is not available from the discovered tigrbl_auth endpoints.");

    expect(() =>
      resolveTrustedPublicEndpoint("/rpc/discover", "registration", "https://public.example.com"),
    ).toThrow("registration is not available from the discovered tigrbl_auth endpoints.");
  });

  it("creates browser POST request options with CSRF and cookie credentials", () => {
    const init = buildBrowserJsonRequestInit({ email: "user@example.com" }, "csrf-fixed");

    expect(init.credentials).toBe("include");
    expect(init.headers).toEqual({
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRF-Token": "csrf-fixed",
      "X-Requested-With": "XMLHttpRequest",
    });
    expect(init.body).toBe(JSON.stringify({ email: "user@example.com" }));
  });

  it("reuses an existing CSRF token before generating a new one", () => {
    const storage = createStorage();
    storage.setItem("tigrbl_auth_public_csrf", "csrf-existing");

    expect(getOrCreateCsrfToken(storage)).toBe("csrf-existing");

    const emptyStorage = createStorage();
    const created = getOrCreateCsrfToken(emptyStorage);
    expect(created).toBeTruthy();
    expect(emptyStorage.setItem).toHaveBeenCalledOnce();
  });

  it("derives a safe consent model and popup callback hash", () => {
    const consent = parseConsentViewModel(
      "#/consent?client_name=Portal&scope=openid%20email&continue=%23%2Fprofile&cancel=%23%2Flogin",
      "#/profile",
      "#/login",
    );

    expect(consent.clientName).toBe("Portal");
    expect(consent.scopes).toEqual(["openid", "email"]);
    expect(consent.approveTarget).toBe("#/profile");
    expect(consent.cancelTarget).toBe("#/login");
    expect(buildPopupCallbackHash("?code=abc&state=xyz")).toBe("#/callback?code=abc&state=xyz");
  });
});

