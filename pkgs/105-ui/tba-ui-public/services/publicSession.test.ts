import { describe, expect, it, vi } from "vitest";

import {
  clearPersistedPublicUser,
  clearPublicSessionCookie,
  isSecureContextForPublicSession,
  parseStoredPublicUser,
  persistPublicUser,
  PUBLIC_SESSION_COOKIE_NAME,
  resolvePublicSessionState,
  serializePublicSessionCookie,
  writePublicSessionCookie,
} from "./publicSession";

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

describe("publicSession", () => {
  it("parses a stored verified user into an authenticated session", () => {
    const state = resolvePublicSessionState(JSON.stringify({
      id: "user-1",
      email: "user@example.com",
      name: "User One",
      isEmailVerified: true,
      mfaEnabled: false,
    }));

    expect(state.user?.email).toBe("user@example.com");
    expect(state.isAuthenticated).toBe(true);
  });

  it("fails closed for malformed stored user data", () => {
    expect(parseStoredPublicUser("{bad json")).toBeNull();
    expect(resolvePublicSessionState(JSON.stringify({ id: "user-1" })).isAuthenticated).toBe(false);
  });

  it("persists and clears public user state through the configured storage", () => {
    const storage = createStorage();
    const user = {
      id: "user-1",
      email: "user@example.com",
      name: "User One",
      provider: "generic" as const,
      isEmailVerified: true,
      mfaEnabled: false,
    };

    persistPublicUser(storage, user);
    expect(storage.setItem).toHaveBeenCalledOnce();

    clearPersistedPublicUser(storage);
    expect(storage.removeItem).toHaveBeenCalledOnce();
  });

  it("serializes a safe browser session cookie model", () => {
    expect(
      serializePublicSessionCookie({ secure: true, maxAgeSeconds: 900 }),
    ).toBe(
      `${PUBLIC_SESSION_COOKIE_NAME}=present; Path=/; Max-Age=900; SameSite=Lax; Secure`,
    );
  });

  it("writes and clears the public session cookie marker", () => {
    const documentLike = { cookie: "" };

    writePublicSessionCookie(documentLike, "https://public.example.com");
    expect(documentLike.cookie).toContain(`${PUBLIC_SESSION_COOKIE_NAME}=present`);
    expect(documentLike.cookie).toContain("Secure");

    clearPublicSessionCookie(documentLike, "http://localhost:3000");
    expect(documentLike.cookie).toContain("Max-Age=0");
    expect(documentLike.cookie).not.toContain("Secure");
  });

  it("treats only HTTPS origins as secure cookie contexts", () => {
    expect(isSecureContextForPublicSession("https://public.example.com")).toBe(true);
    expect(isSecureContextForPublicSession("http://localhost:3000")).toBe(false);
  });
});

