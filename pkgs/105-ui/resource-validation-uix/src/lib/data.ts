export type TabId = 'overview' | 'metadata' | 'jwks' | 'config' | 'validation';

export interface JWK {
  kid: string;
  kty: string;
  alg: string;
  use: string;
  n?: string;
  e?: string;
}

export const API_BASE = "https://api.auth.tigrbl.local";

export const MOCK_METADATA = {
  issuer: "https://auth.example.com",
  authorization_endpoint: "https://auth.example.com/oauth2/v1/authorize",
  token_endpoint: "https://auth.example.com/oauth2/v1/token",
  jwks_uri: "https://auth.example.com/.well-known/jwks.json",
  scopes_supported: ["openid", "profile", "email", "api:read", "api:write", "admin:access"],
  response_types_supported: ["code", "token", "id_token"],
  grant_types_supported: ["authorization_code", "client_credentials"],
  introspection_endpoint: "https://auth.example.com/oauth2/v1/introspect",
  revocation_endpoint: "https://auth.example.com/oauth2/v1/revoke",
};

export const MOCK_JWKS = {
  keys: [
    {
      kty: "RSA",
      use: "sig",
      kid: "key-1-active",
      alg: "RS256",
      n: "vwxyz123...",
      e: "AQAB"
    },
    {
      kty: "RSA",
      use: "sig",
      kid: "key-2-rollover",
      alg: "RS256",
      n: "abcde456...",
      e: "AQAB"
    }
  ]
};

export const FIXTURES = [
  { id: 'valid', name: 'Valid Token', description: 'A properly signed, unexpired token with correct audience.' },
  { id: 'expired', name: 'Expired Token', description: 'A token that has passed its exp time.' },
  { id: 'wrong-issuer', name: 'Wrong Issuer', description: 'A token issued by an unknown authority.' },
  { id: 'wrong-audience', name: 'Wrong Audience', description: 'A token intended for a different resource server.' },
  { id: 'missing-scope', name: 'Missing Scope', description: 'A token lacking required api:read scope.' },
  { id: 'invalid-sig', name: 'Invalid Signature', description: 'A token modified after signing or signed with an unknown key.' },
  { id: 'revoked', name: 'Revoked (Introspection)', description: 'Token signature is valid but introspection returns active: false.' },
  { id: 'malformed', name: 'Malformed Token', description: 'Not a valid JWT structure.' },
];
