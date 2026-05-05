import type { User } from "../types";

export const PUBLIC_SESSION_STORAGE_KEY = "tigrbl_auth_user";
export const PUBLIC_SESSION_COOKIE_NAME = "tigrbl_auth_public_session";
export const PUBLIC_SESSION_COOKIE_VALUE = "present";

type StorageLike = Pick<Storage, "getItem" | "setItem" | "removeItem">;
type DocumentLike = Pick<Document, "cookie">;

export interface PublicSessionState {
  isAuthenticated: boolean;
  user: User | null;
}

export interface PublicSessionCookieOptions {
  maxAgeSeconds?: number;
  path?: string;
  sameSite?: "Lax" | "Strict" | "None";
  secure?: boolean;
}

export const parseStoredPublicUser = (raw: string | null): User | null => {
  if (!raw) {
    return null;
  }

  try {
    const parsed = JSON.parse(raw) as Partial<User>;
    if (!parsed || typeof parsed !== "object") {
      return null;
    }
    if (typeof parsed.id !== "string" || typeof parsed.email !== "string" || typeof parsed.name !== "string") {
      return null;
    }
    return {
      id: parsed.id,
      email: parsed.email,
      name: parsed.name,
      picture: typeof parsed.picture === "string" ? parsed.picture : undefined,
      provider: "generic",
      isEmailVerified: parsed.isEmailVerified === true,
      mfaEnabled: parsed.mfaEnabled === true,
    };
  } catch {
    return null;
  }
};

export const resolvePublicSessionState = (raw: string | null): PublicSessionState => {
  const user = parseStoredPublicUser(raw);
  return {
    user,
    isAuthenticated: user?.isEmailVerified === true,
  };
};

export const persistPublicUser = (
  storage: StorageLike | null | undefined,
  user: User,
): void => {
  storage?.setItem(PUBLIC_SESSION_STORAGE_KEY, JSON.stringify(user));
};

export const clearPersistedPublicUser = (
  storage: StorageLike | null | undefined,
): void => {
  storage?.removeItem(PUBLIC_SESSION_STORAGE_KEY);
};

export const serializePublicSessionCookie = (
  options: PublicSessionCookieOptions = {},
): string => {
  const {
    maxAgeSeconds = 3600,
    path = "/",
    sameSite = "Lax",
    secure = false,
  } = options;
  const parts = [
    `${PUBLIC_SESSION_COOKIE_NAME}=${PUBLIC_SESSION_COOKIE_VALUE}`,
    `Path=${path}`,
    `Max-Age=${maxAgeSeconds}`,
    `SameSite=${sameSite}`,
  ];
  if (secure) {
    parts.push("Secure");
  }
  return parts.join("; ");
};

export const isSecureContextForPublicSession = (origin: string): boolean => {
  try {
    return new URL(origin).protocol === "https:";
  } catch {
    return false;
  }
};

export const writePublicSessionCookie = (
  documentLike: DocumentLike | null | undefined,
  origin: string,
): void => {
  if (!documentLike) {
    return;
  }
  documentLike.cookie = serializePublicSessionCookie({
    secure: isSecureContextForPublicSession(origin),
  });
};

export const clearPublicSessionCookie = (
  documentLike: DocumentLike | null | undefined,
  origin: string,
): void => {
  if (!documentLike) {
    return;
  }
  documentLike.cookie = serializePublicSessionCookie({
    maxAgeSeconds: 0,
    secure: isSecureContextForPublicSession(origin),
  });
};

