import type { OidcConfig, OidcDiscoveryMetadata } from "../types";
import {
  buildBrowserJsonRequestInit,
  getOrCreateCsrfToken,
  resolveTrustedPublicEndpoint,
} from "./publicUxPolicy";

const trimTrailingSlash = (value: string): string => value.replace(/\/+$/, "");
const MAX_SAFE_ERROR_LENGTH = 180;

export const getPublicBaseUrl = (): string => {
  const configured = import.meta.env.VITE_TIGRBL_AUTH_PUBLIC_BASE_URL;
  const fallbackOrigin = typeof window === "undefined" ? "http://localhost:3000" : window.location.origin;
  return trimTrailingSlash(configured && configured.trim() ? configured : fallbackOrigin);
};

export const getDiscoveryUrl = (): string => {
  return `${getPublicBaseUrl()}/.well-known/openid-configuration`;
};

export async function loadTigrblAuthDiscovery(): Promise<OidcDiscoveryMetadata> {
  const response = await fetch(getDiscoveryUrl(), {
    credentials: "include",
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error(`OIDC discovery failed with HTTP ${response.status}`);
  }
  return response.json() as Promise<OidcDiscoveryMetadata>;
}

export async function buildTigrblAuthOidcConfig(clientId: string): Promise<OidcConfig> {
  const metadata = await loadTigrblAuthDiscovery();
  const publicBaseUrl = getPublicBaseUrl();
  const authorizationEndpoint = resolveTrustedPublicEndpoint(
    requireDiscoveredEndpoint(metadata, "authorization_endpoint", "login"),
    "login",
    publicBaseUrl,
  );
  const tokenEndpoint = resolveTrustedPublicEndpoint(
    requireDiscoveredEndpoint(metadata, "token_endpoint", "callback"),
    "callback",
    publicBaseUrl,
  );
  return {
    clientId,
    authority: trimTrailingSlash(metadata.issuer || publicBaseUrl),
    authorizationEndpoint,
    tokenEndpoint,
    userinfoEndpoint: metadata.userinfo_endpoint
      ? resolveTrustedPublicEndpoint(metadata.userinfo_endpoint, "userinfo", publicBaseUrl)
      : undefined,
    endSessionEndpoint: metadata.end_session_endpoint
      ? resolveTrustedPublicEndpoint(metadata.end_session_endpoint, "logout", publicBaseUrl)
      : undefined,
    redirectUri: `${typeof window === "undefined" ? "http://localhost:3000" : window.location.origin}/#/callback`,
    scope: "openid profile email",
  };
}

export function hasEndpoint(
  discovery: OidcDiscoveryMetadata | null,
  key: keyof OidcDiscoveryMetadata,
): boolean {
  return Boolean(discovery?.[key]);
}

export function safeProblemMessage(error: unknown): string {
  const raw = error instanceof Error ? error.message : String(error || "Request failed.");
  const singleLine = raw.replace(/\s+/g, " ").trim();
  const redacted = singleLine
    .replace(/https?:\/\/\S+/gi, "[redacted-url]")
    .replace(/\b[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g, "[redacted-token]")
    .replace(/Bearer\s+\S+/gi, "Bearer [redacted-token]");
  return redacted.slice(0, MAX_SAFE_ERROR_LENGTH) || "Request failed.";
}

export function requireDiscoveredEndpoint(
  discovery: OidcDiscoveryMetadata,
  key: keyof OidcDiscoveryMetadata,
  action: string,
): string {
  const endpoint = discovery[key];
  if (typeof endpoint === "string" && endpoint.trim()) {
    return endpoint;
  }
  throw new Error(`${action} is not available from the discovered tigrbl_auth endpoints.`);
}

async function readProblem(response: Response): Promise<string> {
  try {
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json") || contentType.includes("application/problem+json")) {
      const body = await response.json();
      return safeProblemMessage(body.title || body.detail || body.error_description || body.error || `HTTP ${response.status}`);
    }
  } catch {
    // Fall through to the generic status message.
  }
  return `HTTP ${response.status}`;
}

export async function postDiscoveredJson<T = unknown>(
  key: keyof OidcDiscoveryMetadata,
  action: string,
  body: unknown,
): Promise<T | null> {
  try {
    const discovery = await loadTigrblAuthDiscovery();
    const endpoint = resolveTrustedPublicEndpoint(
      requireDiscoveredEndpoint(discovery, key, action),
      action,
      getPublicBaseUrl(),
    );
    const response = await fetch(
      endpoint,
      buildBrowserJsonRequestInit(body, getOrCreateCsrfToken()),
    );
    if (!response.ok) {
      throw new Error(await readProblem(response));
    }
    if (response.status === 204) {
      return null;
    }
    return response.json() as Promise<T>;
  } catch (error) {
    throw new Error(safeProblemMessage(error));
  }
}

export async function getDiscoveredLogoutUrl(): Promise<string | null> {
  try {
    const discovery = await loadTigrblAuthDiscovery();
    if (!hasEndpoint(discovery, "end_session_endpoint")) {
      return null;
    }
    const endpoint = resolveTrustedPublicEndpoint(
      requireDiscoveredEndpoint(discovery, "end_session_endpoint", "logout"),
      "logout",
      getPublicBaseUrl(),
    );
    const redirect = `${typeof window === "undefined" ? "http://localhost:3000" : window.location.origin}/#/login`;
    const url = new URL(endpoint, getPublicBaseUrl());
    url.searchParams.set("post_logout_redirect_uri", redirect);
    return url.toString();
  } catch {
    return null;
  }
}
