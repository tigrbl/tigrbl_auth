import { describe, expect, it } from "vitest";

import {
  LOGIN_HASH,
  publicHashPath,
  resolveInitialPublicHash,
  resolvePublicRedirect,
  shouldNormalizeCallbackLocation,
  VERIFY_EMAIL_HASH,
} from "./publicRouting";

describe("publicRouting", () => {
  const callbackTarget = "#/profile";

  it("T0 exposes the governed public route constants and path parser", () => {
    expect(LOGIN_HASH).toBe("#/login");
    expect(VERIFY_EMAIL_HASH).toBe("#/verify-email");
    expect(publicHashPath("#/callback?code=abc&state=xyz")).toBe("#/callback");
  });

  it("T1 makes callback URLs the initial boot route before default redirects", () => {
    expect(
      resolveInitialPublicHash(
        "/callback",
        "?code=code-1&state=state-1",
        "",
      ),
    ).toBe("#/callback?code=code-1&state=state-1");

    expect(
      shouldNormalizeCallbackLocation("/callback", "?code=code-1&state=state-1"),
    ).toBe("#/callback?code=code-1&state=state-1");
  });

  it("T1 ignores non-callback startup URLs when resolving initial hash", () => {
    expect(resolveInitialPublicHash("/", "", "")).toBe("#/");
    expect(resolveInitialPublicHash("/", "", "#/profile")).toBe("#/profile");
    expect(shouldNormalizeCallbackLocation("/", "?code=code-1&state=state-1")).toBeNull();
  });

  it("T2 never redirects an active callback route to login", () => {
    expect(
      resolvePublicRedirect({
        currentHash: "#/callback?code=code-1&state=state-1",
        isAuthenticated: false,
        user: null,
        callbackTarget,
        mfaPending: false,
      }),
    ).toBeNull();
  });

  it("T2 moves default, authenticated login, and protected profile decisions out of render", () => {
    expect(
      resolvePublicRedirect({
        currentHash: "#/",
        isAuthenticated: false,
        user: null,
        callbackTarget,
        mfaPending: false,
      }),
    ).toBe("#/login");

    expect(
      resolvePublicRedirect({
        currentHash: "#/login",
        isAuthenticated: true,
        user: {
          id: "user-1",
          email: "user@example.com",
          name: "User One",
          provider: "generic",
          isEmailVerified: true,
          mfaEnabled: false,
        },
        callbackTarget,
        mfaPending: false,
      }),
    ).toBe("#/profile");

    expect(
      resolvePublicRedirect({
        currentHash: "#/profile",
        isAuthenticated: false,
        user: {
          id: "user-1",
          email: "user@example.com",
          name: "User One",
          provider: "generic",
          isEmailVerified: false,
          mfaEnabled: false,
        },
        callbackTarget,
        mfaPending: false,
      }),
    ).toBe("#/verify-email");
  });
});
