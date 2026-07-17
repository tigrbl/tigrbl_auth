import type { User } from "../types";
import { buildPopupCallbackHash } from "./publicUxPolicy";

export const DEFAULT_PUBLIC_HASH = "#/";
export const LOGIN_HASH = "#/login";
export const VERIFY_EMAIL_HASH = "#/verify-email";

export const publicHashPath = (hash: string): string => hash.split("?")[0] || DEFAULT_PUBLIC_HASH;

export const resolveInitialPublicHash = (
  pathname: string,
  search: string,
  hash: string,
): string => {
  if (pathname === "/callback") {
    const callbackHash = buildPopupCallbackHash(search);
    if (callbackHash) {
      return callbackHash;
    }
  }
  return hash || DEFAULT_PUBLIC_HASH;
};

export const shouldNormalizeCallbackLocation = (
  pathname: string,
  search: string,
): string | null => {
  if (pathname !== "/callback") {
    return null;
  }
  return buildPopupCallbackHash(search);
};

export interface PublicRedirectDecision {
  currentHash: string;
  isAuthenticated: boolean;
  user: User | null;
  callbackTarget: string;
  mfaPending: boolean;
}

export const resolvePublicRedirect = ({
  currentHash,
  isAuthenticated,
  user,
  callbackTarget,
  mfaPending,
}: PublicRedirectDecision): string | null => {
  if (mfaPending) {
    return null;
  }

  const path = publicHashPath(currentHash);
  if (path === "#/callback") {
    return null;
  }

  if (!currentHash || path === DEFAULT_PUBLIC_HASH || currentHash === "#") {
    return isAuthenticated ? callbackTarget : LOGIN_HASH;
  }

  if ((path === "#/login" || path === "#/register") && isAuthenticated) {
    return callbackTarget;
  }

  if (path === "#/profile" && !isAuthenticated) {
    return user && !user.isEmailVerified ? VERIFY_EMAIL_HASH : LOGIN_HASH;
  }

  return null;
};
