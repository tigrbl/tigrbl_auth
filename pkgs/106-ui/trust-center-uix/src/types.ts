export enum FederationProtocol {
  OIDC = "OIDC",
  OPENID_FEDERATION = "OPENID_FEDERATION",
  SAML = "SAML",
}

export enum ConnectionState {
  DRAFT = "DRAFT",
  REVIEW = "REVIEW",
  APPROVED = "APPROVED",
  ACTIVE = "ACTIVE",
  SUSPENDED = "SUSPENDED",
  RETIRED = "RETIRED",
}

export enum ConnectionDirection {
  INBOUND = "INBOUND", // External IdP to Tigrbl
  OUTBOUND = "OUTBOUND", // Tigrbl RP to External AS/RP
}

export interface ClientAuthentication {
  method: "client_secret_post" | "client_secret_basic" | "private_key_jwt" | "none";
  secretReference?: string; // write-only reference
  keyId?: string;
}

export interface ClaimMapping {
  id: string;
  sourceSelector: string;
  normalizedTarget: string;
  transformation: string; // e.g. "lowercase", "split", "as-is", "none"
  required: boolean;
  privacyClass: "public" | "internal" | "sensitive";
}

export interface RoutingRule {
  id: string;
  priority: number;
  conditionType: "domain" | "organization" | "app_id" | "always";
  conditionValue: string;
  action: "route_to_connection" | "prompt_choice" | "deny";
}

export interface FederationConnection {
  id: string;
  tenantId: string;
  displayName: string;
  protocol: FederationProtocol;
  direction: ConnectionDirection;
  state: ConnectionState;
  issuer: string; // Entity Identifier
  metadataMode: "manual" | "discovery" | "federation";
  metadataUrl: string;
  audience: string;
  scopes: string[];
  clientAuth: ClientAuthentication;
  claimMappings: ClaimMapping[];
  routingRules: RoutingRule[];
  activeVersion: number;
  currentVersion: number;
  health: "healthy" | "degraded" | "failing" | "unknown";
  lastValidation?: string;
  lastMetadataRefresh?: string;
  lastKnownGoodDigest?: string;
  errorMessage?: string;
}

export interface TrustAnchor {
  id: string;
  displayName: string;
  entityId: string;
  pinnedKeys: Array<{
    kid: string;
    kty: string;
    alg: string;
    use: string;
    n?: string;
    e?: string;
  }>;
  authorityHints: string[];
  status: "active" | "revoked";
  created: string;
}

export interface TrustNode {
  id: string;
  label: string;
  type: "anchor" | "intermediate" | "leaf" | "op" | "rp";
  entityId: string;
  health: "healthy" | "degraded" | "failing";
}

export interface TrustEdge {
  id: string;
  source: string; // Node ID
  target: string; // Node ID
  exchangeKind: "subordinate" | "peer" | "anchor_association";
  state: "active" | "revoked";
  constraints: string; // JSON or text constraints
  validUntil: string;
}

export interface IncidentRecord {
  id: string;
  title: string;
  type: "signature_failure" | "expired_statement" | "issuer_mismatch" | "metadata_drift" | "broken_logout";
  severity: "critical" | "warning" | "info";
  status: "active" | "mitigated" | "resolved";
  connectionId?: string;
  description: string;
  timestamp: string;
  affectedTenants: number;
  affectedApps: number;
  affectedSessions: number;
  resolution?: string;
}

export interface EntityStatement {
  iss: string;
  sub: string;
  iat: number;
  exp: number;
  jwks: {
    keys: Array<{
      kid: string;
      kty: string;
      alg: string;
      use: string;
    }>;
  };
  metadata?: {
    openid_provider?: Record<string, any>;
    openid_relying_party?: Record<string, any>;
    federation_entity?: Record<string, any>;
  };
  authority_hints?: string[];
  trust_marks?: Array<{ id: string; value: string }>;
}
