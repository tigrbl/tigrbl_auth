export type BrowserStoragePolicy = "memory" | "sessionStorage" | "localStorage";

export interface RPConfiguration {
  issuer: string;
  clientId: string;
  redirectUri: string;
  scopes?: readonly string[];
  clientSecret?: string;
  postLogoutRedirectUri?: string;
}

export interface LoginRequest {
  state: string;
  nonce: string;
  codeVerifier: string;
  codeChallenge: string;
  redirectUri: string;
  scope: readonly string[];
}

export interface CallbackResult {
  code: string;
  state: string;
  iss?: string;
}

export interface TokenSet {
  accessToken: string;
  idToken?: string;
  refreshToken?: string;
  expiresIn?: number;
}

export interface IdTokenClaims {
  iss: string;
  sub: string;
  aud: string | readonly string[];
  exp: number;
  nonce?: string;
}

export interface DiscoveryMetadata {
  issuer: string;
  authorization_endpoint: string;
  token_endpoint: string;
  jwks_uri: string;
  userinfo_endpoint?: string;
  end_session_endpoint?: string;
}

export class RPError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "RPError";
  }
}

const DEFAULT_SCOPES = ["openid"] as const;

function requireValue(value: string | undefined, name: string): string {
  if (!value) {
    throw new RPError(`${name} is required`);
  }
  return value;
}

function randomBase64Url(byteLength = 32): string {
  const bytes = new Uint8Array(byteLength);
  globalThis.crypto.getRandomValues(bytes);
  return base64Url(bytes);
}

function base64Url(bytes: Uint8Array): string {
  const binary = Array.from(bytes, (byte) => String.fromCharCode(byte)).join("");
  const encoded = typeof btoa === "function" ? btoa(binary) : Buffer.from(bytes).toString("base64");
  return encoded.replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/u, "");
}

function normalizeIssuer(issuer: string): string {
  return issuer.replace(/\/+$/u, "");
}

export async function pkceS256(verifier: string): Promise<string> {
  if (!verifier) {
    throw new RPError("PKCE verifier is required");
  }
  const data = new TextEncoder().encode(verifier);
  const digest = await globalThis.crypto.subtle.digest("SHA-256", data);
  return base64Url(new Uint8Array(digest));
}

export function assertBrowserSafeConfig(config: RPConfiguration): void {
  if (config.clientSecret) {
    throw new RPError("browser RP configuration must not include a client secret");
  }
}

export function validateBrowserStoragePolicy(policy: BrowserStoragePolicy): BrowserStoragePolicy {
  if (policy === "localStorage") {
    throw new RPError("browser RP tokens must not be persisted in localStorage");
  }
  return policy;
}

export async function createLoginRequest(config: RPConfiguration): Promise<LoginRequest> {
  assertBrowserSafeConfig(config);
  const codeVerifier = randomBase64Url(48);
  const scope = [...new Set(config.scopes ?? DEFAULT_SCOPES)].sort();
  return {
    state: randomBase64Url(24),
    nonce: randomBase64Url(24),
    codeVerifier,
    codeChallenge: await pkceS256(codeVerifier),
    redirectUri: requireValue(config.redirectUri, "redirectUri"),
    scope,
  };
}

export async function buildAuthorizationUrl(
  config: RPConfiguration,
  authorizationEndpoint: string,
  login?: LoginRequest,
): Promise<string> {
  const request = login ?? (await createLoginRequest(config));
  const params = new URLSearchParams({
    response_type: "code",
    client_id: requireValue(config.clientId, "clientId"),
    redirect_uri: request.redirectUri,
    scope: request.scope.join(" "),
    state: request.state,
    nonce: request.nonce,
    code_challenge: request.codeChallenge,
    code_challenge_method: "S256",
  });
  return `${authorizationEndpoint}?${params.toString()}`;
}

export function parseCallback(url: string): CallbackResult {
  const parsed = new URL(url);
  const error = parsed.searchParams.get("error");
  if (error) {
    throw new RPError(error);
  }
  const code = parsed.searchParams.get("code");
  const state = parsed.searchParams.get("state");
  if (!code || !state) {
    throw new RPError("callback requires code and state");
  }
  const iss = parsed.searchParams.get("iss") ?? undefined;
  return { code, state, iss };
}

export function validateCallbackState(callback: CallbackResult, expectedState: string): CallbackResult {
  if (callback.state !== expectedState) {
    throw new RPError("callback state mismatch");
  }
  return callback;
}

export function validateDiscoveryMetadata(metadata: DiscoveryMetadata, issuer: string): DiscoveryMetadata {
  if (normalizeIssuer(metadata.issuer) !== normalizeIssuer(issuer)) {
    throw new RPError("issuer metadata mismatch");
  }
  for (const key of ["authorization_endpoint", "token_endpoint", "jwks_uri"] as const) {
    if (!metadata[key]) {
      throw new RPError(`issuer metadata missing required endpoint: ${key}`);
    }
  }
  return metadata;
}

export function validateIdTokenClaims(
  claims: IdTokenClaims,
  config: RPConfiguration,
  expectedNonce: string,
  nowSeconds = Math.floor(Date.now() / 1000),
): IdTokenClaims {
  if (normalizeIssuer(claims.iss) !== normalizeIssuer(config.issuer)) {
    throw new RPError("ID token issuer mismatch");
  }
  const audiences = Array.isArray(claims.aud) ? claims.aud : [claims.aud];
  if (!audiences.includes(config.clientId)) {
    throw new RPError("ID token audience mismatch");
  }
  if (claims.nonce !== expectedNonce) {
    throw new RPError("ID token nonce mismatch");
  }
  if (claims.exp <= nowSeconds) {
    throw new RPError("ID token expired");
  }
  return claims;
}

export function buildLogoutUrl(config: RPConfiguration, endSessionEndpoint: string, idTokenHint: string, state?: string): string {
  const params = new URLSearchParams({
    client_id: config.clientId,
    id_token_hint: idTokenHint,
  });
  if (config.postLogoutRedirectUri) {
    params.set("post_logout_redirect_uri", config.postLogoutRedirectUri);
  }
  if (state) {
    params.set("state", state);
  }
  return `${endSessionEndpoint}?${params.toString()}`;
}

export class BrowserMemorySession {
  #tokens: TokenSet | null = null;
  readonly policy: BrowserStoragePolicy;

  constructor(policy: BrowserStoragePolicy = "memory") {
    this.policy = validateBrowserStoragePolicy(policy);
  }

  set(tokens: TokenSet): void {
    this.#tokens = { ...tokens };
  }

  get(): TokenSet | null {
    return this.#tokens ? { ...this.#tokens } : null;
  }

  clear(): void {
    this.#tokens = null;
  }
}

export function nodeVersionMatrix(packageName = "@tigrbl-auth/rp", versions = ["22", "24", "26"]): readonly string[] {
  return versions.map((version) => `${packageName}@node${version}`);
}

export function npmProvenanceManifest(): Readonly<Record<string, string | boolean>> {
  return {
    package: "@tigrbl-auth/rp",
    workflow: "monorepo-npm-package-release.yml",
    provenance: true,
    publishConfigAccess: "public",
  };
}

export function sharedVectorManifest(): Readonly<Record<string, string>> {
  return {
    pkceVerifier: "testkit-vector-verifier",
    pkceS256: "h3HB4s6R4f5U5EQGbR3B5YPPvheB5qvVs5HrLBv7R0M",
    callbackRequiredParams: "code,state",
  };
}
