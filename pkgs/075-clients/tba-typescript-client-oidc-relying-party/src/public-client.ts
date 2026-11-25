import {
  buildAuthorizationUrl,
  createLoginRequest,
  parseCallback,
  RPError,
  validateCallbackState,
  validateIdTokenClaims,
  type DiscoveryMetadata,
  type IdTokenClaims,
  type LoginIntent,
  type LoginRequest,
  type RPConfiguration,
} from "./index.js";

type JsonObject = Record<string, unknown>;

export interface VerifiedCallback {
  identity: IdTokenClaims;
  tokens: {
    accessToken: string;
    idToken: string;
    refreshToken?: string;
  };
}

function isObject(value: unknown): value is JsonObject {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isText(value: unknown): value is string {
  return typeof value === "string" && value.length > 0;
}

function httpsUrl(value: unknown, name: string): URL {
  if (isText(value) && /^https:\/\//u.test(value) && !/[\s\u0000-\u001f\\#]/u.test(value)) {
    try {
      const url = new URL(value);
      if (url.hostname && !url.username && !url.password) return url;
    } catch {
      // Emit one error without including the URL.
    }
  }
  throw new RPError(`invalid ${name} URL`);
}

function callbackAtRegisteredUri(callbackUrl: string, redirectUri: string): URL {
  const actual = httpsUrl(callbackUrl, "callback");
  const expected = httpsUrl(redirectUri, "redirect URI");
  const reserved = ["code", "state", "iss", "error", "error_description", "error_uri"];
  if (actual.origin !== expected.origin || actual.pathname !== expected.pathname) {
    throw new RPError("callback URL does not match the registered redirect URI");
  }
  for (const key of new Set(expected.searchParams.keys())) {
    const fixed = expected.searchParams.getAll(key);
    const received = actual.searchParams.getAll(key);
    if (reserved.includes(key) || fixed.length !== received.length || fixed.some((value, i) => value !== received[i])) {
      throw new RPError("callback URL does not match the registered redirect URI");
    }
  }
  if (reserved.some(key => actual.searchParams.getAll(key).length > 1)) {
    throw new RPError("callback contains duplicate protocol parameters");
  }
  return actual;
}

function decodeSegment(value: string): Uint8Array<ArrayBuffer> {
  if (!/^[A-Za-z0-9_-]+$/u.test(value)) throw new RPError("invalid ID token encoding");
  const decoded = atob(value.replaceAll("-", "+").replaceAll("_", "/"));
  const canonical = btoa(decoded).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/u, "");
  if (canonical !== value) throw new RPError("invalid ID token encoding");
  return Uint8Array.from(decoded, char => char.charCodeAt(0));
}

function decodeObject(part: string): JsonObject {
  const value: unknown = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(decodeSegment(part)));
  if (!isObject(value)) throw new RPError("invalid ID token JSON object");
  return value;
}

async function signedClaims(token: string, jwks: JsonObject): Promise<JsonObject> {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) throw new RPError("expected compact JWS");
    const [protectedHeader, payload, signature] = parts;
    const header = decodeObject(protectedHeader);
    if (header.alg !== "RS256" || !isText(header.kid) || "crit" in header || "b64" in header) {
      throw new RPError("unexpected ID token algorithm or headers");
    }
    if (!Array.isArray(jwks.keys)) throw new RPError("invalid JWKS");
    const keys = jwks.keys.filter((key): key is JsonObject => isObject(key) && key.kid === header.kid);
    const [key] = keys;
    if (keys.length !== 1 || key.kty !== "RSA" || (key.alg !== undefined && key.alg !== "RS256")
      || (key.use !== undefined && key.use !== "sig")
      || (key.key_ops !== undefined && (!Array.isArray(key.key_ops) || !key.key_ops.includes("verify")))
      || ["d", "p", "q", "dp", "dq", "qi", "oth", "k"].some(part => part in key)) {
      throw new RPError("invalid ID token signing key");
    }
    const algorithm = { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" };
    const publicKey = await crypto.subtle.importKey("jwk", key, algorithm, false, ["verify"]);
    const { modulusLength } = publicKey.algorithm as RsaKeyAlgorithm;
    if (modulusLength < 2048 || !await crypto.subtle.verify(
      algorithm.name, publicKey, decodeSegment(signature), new TextEncoder().encode(`${protectedHeader}.${payload}`),
    )) {
      throw new RPError("ID token signature did not verify");
    }
    return decodeObject(payload);
  } catch {
    throw new RPError("ID token signature or structure is invalid");
  }
}

function verifyClaims(claims: JsonObject, config: RPConfiguration, nonce: string): IdTokenClaims {
  const now = Math.floor(Date.now() / 1000);
  if (claims.iss !== config.issuer) throw new RPError("ID token issuer mismatch");
  const audiences = Array.isArray(claims.aud) ? claims.aud : [claims.aud];
  if (audiences.length !== 1 || audiences[0] !== config.clientId) throw new RPError("ID token audience mismatch");
  if ("azp" in claims && claims.azp !== config.clientId) {
    throw new RPError("ID token authorized party mismatch");
  }
  if (!isText(claims.sub) || typeof claims.exp !== "number" || !Number.isFinite(claims.exp)
    || typeof claims.iat !== "number" || !Number.isFinite(claims.iat)
    || ("nbf" in claims && (typeof claims.nbf !== "number" || !Number.isFinite(claims.nbf)))) {
    throw new RPError("invalid ID token claims");
  }
  if (claims.iat > now || (typeof claims.nbf === "number" && claims.nbf > now)) {
    throw new RPError("ID token is not active yet");
  }
  return validateIdTokenClaims(claims as unknown as IdTokenClaims, config, nonce, now);
}

/** A public OIDC client. Keep login transactions in the app's browser-bound session. */
export class PublicRelyingParty {
  readonly #config: RPConfiguration;
  readonly #fetch: typeof fetch;

  constructor(config: RPConfiguration, fetcher: typeof fetch = globalThis.fetch) {
    const issuer = httpsUrl(config.issuer, "issuer");
    if (config.issuer.includes("?") || issuer.username || !config.clientId || config.clientSecret != null
      || !(config.scopes ?? ["openid"]).includes("openid")) {
      throw new RPError("invalid public OIDC client configuration");
    }
    httpsUrl(config.redirectUri, "redirect URI");
    this.#config = { ...config, issuer: config.issuer.replace(/\/+$/u, ""), scopes: [...(config.scopes ?? ["openid"])] };
    this.#fetch = fetcher;
  }

  async #request(url: string, form?: URLSearchParams): Promise<JsonObject> {
    const response = await this.#fetch(url, {
      redirect: "error", credentials: "omit", cache: "no-store",
      headers: { accept: "application/json" },
      ...(form ? { method: "POST", body: form } : {}),
    });
    if (!response.ok) throw new RPError(form ? "token exchange was rejected" : "issuer metadata or keys unavailable");
    const data: unknown = await response.json();
    if (!isObject(data)) throw new RPError("invalid JSON response from issuer");
    return data;
  }

  async #discover(): Promise<DiscoveryMetadata> {
    const { issuer } = this.#config;
    const data = await this.#request(`${issuer}/.well-known/openid-configuration`);
    if (data.issuer !== issuer) throw new RPError("issuer metadata mismatch");
    for (const [name, supported] of [
      ["code_challenge_methods_supported", "S256"],
      ["token_endpoint_auth_methods_supported", "none"],
      ["id_token_signing_alg_values_supported", "RS256"],
    ]) {
      const values = data[name];
      if (values != null && (!Array.isArray(values) || !values.includes(supported))) {
        throw new RPError(`issuer does not support ${supported} in ${name}`);
      }
    }
    httpsUrl(data.authorization_endpoint, "authorization endpoint");
    httpsUrl(data.token_endpoint, "token endpoint");
    httpsUrl(data.jwks_uri, "JWKS endpoint");
    return data as unknown as DiscoveryMetadata;
  }

  async beginLogin(
    intent: LoginIntent = "ordinary", acrValues?: string,
  ): Promise<{ url: string; login: LoginRequest }> {
    const metadata = await this.#discover();
    const login = await createLoginRequest(this.#config);
    return {
      url: await buildAuthorizationUrl(this.#config, metadata.authorization_endpoint, login, intent, acrValues),
      login,
    };
  }

  /**
   * expectedState comes from the app's browser session. consumeLogin atomically
   * removes an unexpired transaction scoped to this issuer and client.
   */
  async completeCallback(
    callbackUrl: string,
    expectedState: string,
    consumeLogin: (state: string) => LoginRequest | undefined | Promise<LoginRequest | undefined>,
    expectedSubject?: string,
  ): Promise<VerifiedCallback> {
    const url = callbackAtRegisteredUri(callbackUrl, this.#config.redirectUri);
    if (url.searchParams.has("error")) throw new RPError("authorization was not completed");
    const callback = validateCallbackState(parseCallback(url.href), expectedState);
    if (callback.iss !== undefined && callback.iss !== this.#config.issuer) {
      throw new RPError("callback issuer mismatch");
    }
    const login = await consumeLogin(callback.state);
    if (!login || login.state !== callback.state || login.redirectUri !== this.#config.redirectUri
      || !isText(login.nonce) || !/^[A-Za-z0-9._~-]{43,128}$/u.test(login.codeVerifier)) {
      throw new RPError("callback does not match an active login request");
    }
    const metadata = await this.#discover();
    const data = await this.#request(metadata.token_endpoint, new URLSearchParams({
      grant_type: "authorization_code",
      client_id: this.#config.clientId,
      redirect_uri: login.redirectUri,
      code: callback.code,
      code_verifier: login.codeVerifier,
    }));
    if (data.error) throw new RPError("token exchange was rejected");
    if (!isText(data.access_token) || !isText(data.id_token) || !isText(data.token_type)
      || data.token_type.toLowerCase() !== "bearer"
      || ("refresh_token" in data && !isText(data.refresh_token))) {
      throw new RPError("token response is missing valid OIDC tokens");
    }
    const jwks = await this.#request(metadata.jwks_uri);
    const identity = verifyClaims(await signedClaims(data.id_token, jwks), this.#config, login.nonce);
    if (expectedSubject !== undefined && identity.sub !== expectedSubject) {
      throw new RPError("callback subject does not match the expected account");
    }
    return {
      identity,
      tokens: {
        accessToken: data.access_token,
        idToken: data.id_token,
        ...(isText(data.refresh_token) ? { refreshToken: data.refresh_token } : {}),
      },
    };
  }
}
