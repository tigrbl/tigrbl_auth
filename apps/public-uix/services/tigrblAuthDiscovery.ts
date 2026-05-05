import type { OidcConfig, OidcDiscoveryMetadata } from "../types";

const trimTrailingSlash = (value: string): string => value.replace(/\/+$/, "");

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
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error(`OIDC discovery failed with HTTP ${response.status}`);
  }
  return response.json() as Promise<OidcDiscoveryMetadata>;
}

export async function buildTigrblAuthOidcConfig(clientId: string): Promise<OidcConfig> {
  const metadata = await loadTigrblAuthDiscovery();
  return {
    clientId,
    authority: trimTrailingSlash(metadata.issuer || getPublicBaseUrl()),
    authorizationEndpoint: metadata.authorization_endpoint,
    tokenEndpoint: metadata.token_endpoint,
    userinfoEndpoint: metadata.userinfo_endpoint,
    endSessionEndpoint: metadata.end_session_endpoint,
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
