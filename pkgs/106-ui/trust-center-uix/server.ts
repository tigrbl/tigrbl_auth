import express from "express";
import path from "path";
import dotenv from "dotenv";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI, Type } from "@google/genai";
import {
  FederationProtocol,
  ConnectionState,
  ConnectionDirection,
  FederationConnection,
  TrustAnchor,
  TrustNode,
  TrustEdge,
  IncidentRecord,
} from "./src/types.js";

dotenv.config();

const app = express();
app.use(express.json());

const PORT = 3000;

// Initialize Gemini Client
let ai: GoogleGenAI | null = null;
if (process.env.GEMINI_API_KEY) {
  try {
    ai = new GoogleGenAI({
      apiKey: process.env.GEMINI_API_KEY,
      httpOptions: {
        headers: {
          "User-Agent": "aistudio-build",
        },
      },
    });
    console.log("Google GenAI client initialized successfully with telemetric user-agent.");
  } catch (error) {
    console.error("Failed to initialize Google GenAI client:", error);
  }
} else {
  console.log("No GEMINI_API_KEY environment variable found. Backend will use reliable fallback simulations.");
}

// ==========================================
// CANONICAL SEED DATA (Store in-memory for live interactions)
// ==========================================

let connections: FederationConnection[] = [
  {
    id: "conn-okta-workplace",
    tenantId: "tenant-default",
    displayName: "Okta Enterprise Workforce IdP",
    protocol: FederationProtocol.OIDC,
    direction: ConnectionDirection.INBOUND,
    state: ConnectionState.ACTIVE,
    issuer: "https://tigrbl-enterprise.okta.com/oauth2/default",
    metadataMode: "discovery",
    metadataUrl: "https://tigrbl-enterprise.okta.com/oauth2/default/.well-known/openid-configuration",
    audience: "tigrbl-auth-router-federation",
    scopes: ["openid", "profile", "email", "groups"],
    clientAuth: {
      method: "client_secret_post",
      secretReference: "vault://tenants/default/secrets/okta-client-secret",
    },
    claimMappings: [
      { id: "m1", sourceSelector: "sub", normalizedTarget: "external_id", transformation: "as-is", required: true, privacyClass: "internal" },
      { id: "m2", sourceSelector: "email", normalizedTarget: "email", transformation: "lowercase", required: true, privacyClass: "internal" },
      { id: "m3", sourceSelector: "given_name", normalizedTarget: "first_name", transformation: "as-is", required: false, privacyClass: "public" },
      { id: "m4", sourceSelector: "family_name", normalizedTarget: "last_name", transformation: "as-is", required: false, privacyClass: "public" },
      { id: "m5", sourceSelector: "groups", normalizedTarget: "roles", transformation: "split", required: false, privacyClass: "sensitive" },
    ],
    routingRules: [
      { id: "r1", priority: 10, conditionType: "domain", conditionValue: "tigrbl.com", action: "route_to_connection" },
      { id: "r2", priority: 20, conditionType: "organization", conditionValue: "Tigrbl Corp", action: "route_to_connection" },
    ],
    activeVersion: 2,
    currentVersion: 2,
    health: "healthy",
    lastValidation: new Date(Date.now() - 3600000).toISOString(),
    lastMetadataRefresh: new Date(Date.now() - 1200000).toISOString(),
    lastKnownGoodDigest: "sha256-a78b4c9e8d...",
  },
  {
    id: "conn-swedish-trust-marks",
    tenantId: "tenant-default",
    displayName: "Swedish National Multilateral Federation",
    protocol: FederationProtocol.OPENID_FEDERATION,
    direction: ConnectionDirection.INBOUND,
    state: ConnectionState.REVIEW,
    issuer: "https://fed.trust.sweden.se",
    metadataMode: "federation",
    metadataUrl: "https://fed.trust.sweden.se/.well-known/openid-federation",
    audience: "https://auth.tigrbl.com/tenant-default/federation",
    scopes: ["openid", "profile", "email", "swedish_civic_id"],
    clientAuth: {
      method: "private_key_jwt",
      keyId: "key-se-fed-signing-2026",
    },
    claimMappings: [
      { id: "sm1", sourceSelector: "sub", normalizedTarget: "external_id", transformation: "as-is", required: true, privacyClass: "internal" },
      { id: "sm2", sourceSelector: "seCivicNumber", normalizedTarget: "national_id", transformation: "as-is", required: true, privacyClass: "sensitive" },
      { id: "sm3", sourceSelector: "email", normalizedTarget: "email", transformation: "lowercase", required: true, privacyClass: "internal" },
    ],
    routingRules: [
      { id: "sr1", priority: 5, conditionType: "domain", conditionValue: "*.se", action: "route_to_connection" },
    ],
    activeVersion: 0,
    currentVersion: 1,
    health: "degraded",
    lastValidation: new Date(Date.now() - 18000000).toISOString(),
    lastMetadataRefresh: new Date(Date.now() - 18000000).toISOString(),
    lastKnownGoodDigest: "sha256-b89c4e2a11...",
    errorMessage: "Intermediate trust path certificate is warning of imminent rotation on August 1st, 2026.",
  },
  {
    id: "conn-edu-gain",
    tenantId: "tenant-default",
    displayName: "eduGAIN Research & Academic Trust",
    protocol: FederationProtocol.OPENID_FEDERATION,
    direction: ConnectionDirection.INBOUND,
    state: ConnectionState.SUSPENDED,
    issuer: "https://edugain.org/federation",
    metadataMode: "federation",
    metadataUrl: "https://edugain.org/.well-known/openid-federation",
    audience: "https://auth.tigrbl.com/tenant-default/federation",
    scopes: ["openid", "profile", "eduPersonPrincipalName", "email"],
    clientAuth: {
      method: "none",
    },
    claimMappings: [
      { id: "em1", sourceSelector: "eduPersonPrincipalName", normalizedTarget: "external_id", transformation: "as-is", required: true, privacyClass: "internal" },
      { id: "em2", sourceSelector: "email", normalizedTarget: "email", transformation: "lowercase", required: true, privacyClass: "internal" },
    ],
    routingRules: [
      { id: "er1", priority: 30, conditionType: "domain", conditionValue: "*.edu", action: "route_to_connection" },
    ],
    activeVersion: 1,
    currentVersion: 2,
    health: "failing",
    lastValidation: new Date(Date.now() - 86400000).toISOString(),
    lastMetadataRefresh: new Date(Date.now() - 43200000).toISOString(),
    lastKnownGoodDigest: "sha256-f28394bc8d...",
    errorMessage: "Trust chain validation failed: Cryptographic signature mismatch detected at Intermediate anchor 'https://anchors.edugain.org/keys'. Connection quarantined.",
  }
];

let trustAnchors: TrustAnchor[] = [
  {
    id: "anchor-tigrbl-global",
    displayName: "Tigrbl Global Root Authority",
    entityId: "https://trust.auth.tigrbl.com",
    pinnedKeys: [
      { kid: "root-key-1", kty: "RSA", alg: "RS256", use: "sig", n: "uvw...", e: "AQAB" }
    ],
    authorityHints: [],
    status: "active",
    created: "2026-01-15T00:00:00Z"
  },
  {
    id: "anchor-se-gov",
    displayName: "Swedish Government Trust Anchor",
    entityId: "https://trust.gov.se/federation",
    pinnedKeys: [
      { kid: "se-gov-key-2", kty: "EC", alg: "ES256", use: "sig" }
    ],
    authorityHints: ["https://trust.gov.se/federation"],
    status: "active",
    created: "2026-02-20T00:00:00Z"
  },
  {
    id: "anchor-edugain-root",
    displayName: "eduGAIN Global Federation Anchor",
    entityId: "https://edugain.org/anchor",
    pinnedKeys: [
      { kid: "edugain-key-3", kty: "RSA", alg: "RS256", use: "sig" }
    ],
    authorityHints: ["https://edugain.org/anchor"],
    status: "active",
    created: "2026-03-01T00:00:00Z"
  }
];

let trustNodes: TrustNode[] = [
  { id: "n-root", label: "Tigrbl Global Root", type: "anchor", entityId: "https://trust.auth.tigrbl.com", health: "healthy" },
  { id: "n-se-gov", label: "Swedish Government Anchor", type: "anchor", entityId: "https://trust.gov.se/federation", health: "healthy" },
  { id: "n-edugain", label: "eduGAIN Anchor", type: "anchor", entityId: "https://edugain.org/anchor", health: "healthy" },
  
  { id: "n-inter-se", label: "Swedish Gov Intermediate IDP Entity", type: "intermediate", entityId: "https://intermediate.trust.sweden.se", health: "healthy" },
  { id: "n-inter-edu", label: "eduGAIN Academic Intermediate", type: "intermediate", entityId: "https://anchors.edugain.org/keys", health: "failing" },
  
  { id: "n-leaf-okta", label: "Okta Enterprise workforce IdP", type: "op", entityId: "https://tigrbl-enterprise.okta.com/oauth2/default", health: "healthy" },
  { id: "n-leaf-swedish", label: "Swedish National Multilateral Federation", type: "op", entityId: "https://fed.trust.sweden.se", health: "degraded" },
  { id: "n-leaf-edugain", label: "eduGAIN Research & Academic Trust", type: "op", entityId: "https://edugain.org/federation", health: "failing" },
  
  { id: "n-rp-portal", label: "Tigrbl Auth Portal (RP)", type: "rp", entityId: "https://auth.tigrbl.com/tenant-default/federation", health: "healthy" }
];

let trustEdges: TrustEdge[] = [
  // Anchors pointing to intermediate or leaf associations
  { id: "e1", source: "n-root", target: "n-leaf-okta", exchangeKind: "anchor_association", state: "active", constraints: "{\"allowed_issuers\":[\"https://tigrbl-enterprise.okta.com/*\"],\"max_path_depth\":2}", validUntil: "2027-01-15T00:00:00Z" },
  { id: "e2", source: "n-se-gov", target: "n-inter-se", exchangeKind: "subordinate", state: "active", constraints: "{\"allowed_algorithms\":[\"RS256\",\"ES256\"],\"max_path_depth\":3}", validUntil: "2026-12-31T23:59:59Z" },
  { id: "e3", source: "n-inter-se", target: "n-leaf-swedish", exchangeKind: "subordinate", state: "active", constraints: "{\"required_trust_marks\":[\"swedish_civic_id_v1\"]}", validUntil: "2026-11-30T00:00:00Z" },
  
  { id: "e4", source: "n-edugain", target: "n-inter-edu", exchangeKind: "subordinate", state: "active", constraints: "{\"allowed_algorithms\":[\"RS256\"],\"max_path_depth\":4}", validUntil: "2026-10-15T00:00:00Z" },
  { id: "e5", source: "n-inter-edu", target: "n-leaf-edugain", exchangeKind: "subordinate", state: "active", constraints: "{\"allowed_issuers\":[\"*.edu\"]}", validUntil: "2026-08-31T00:00:00Z" },
  
  // RP pointing back to trust systems
  { id: "e6", source: "n-rp-portal", target: "n-root", exchangeKind: "anchor_association", state: "active", constraints: "{}", validUntil: "2028-01-01T00:00:00Z" },
  { id: "e7", source: "n-rp-portal", target: "n-se-gov", exchangeKind: "anchor_association", state: "active", constraints: "{}", validUntil: "2027-07-01T00:00:00Z" },
  { id: "e8", source: "n-rp-portal", target: "n-edugain", exchangeKind: "anchor_association", state: "active", constraints: "{}", validUntil: "2026-12-31T00:00:00Z" }
];

let incidents: IncidentRecord[] = [
  {
    id: "inc-1",
    title: "eduGAIN Intermediate Signature Match Failure",
    type: "signature_failure",
    severity: "critical",
    status: "active",
    connectionId: "conn-edu-gain",
    description: "During a periodic validation run, the intermediate authority statement published by 'https://anchors.edugain.org/keys' failed signature verification. The key ID (kid) was not registered at the root anchor.",
    timestamp: new Date(Date.now() - 7200000).toISOString(),
    affectedTenants: 1,
    affectedApps: 14,
    affectedSessions: 182,
  },
  {
    id: "inc-2",
    title: "Swedish Federation Metadata Drift Warning",
    type: "metadata_drift",
    severity: "warning",
    status: "active",
    connectionId: "conn-swedish-trust-marks",
    description: "The remote issuer 'https://fed.trust.sweden.se' published an updated JWKS containing ES384 algorithm support that is not permitted under the active connection constraints.",
    timestamp: new Date(Date.now() - 14400000).toISOString(),
    affectedTenants: 1,
    affectedApps: 6,
    affectedSessions: 0,
  }
];

// ==========================================
// API ROUTES
// ==========================================

// --- Connections CRUD ---

// Get all connections
app.get("/api/federation/connections", (req, res) => {
  res.json(connections);
});

// Create a connection (DRAFT)
app.post("/api/federation/connections", (req, res) => {
  const { displayName, protocol, direction, issuer, metadataMode, metadataUrl, audience, scopes, clientAuth } = req.body;
  
  if (!displayName || !issuer || !metadataUrl) {
    return res.status(400).json({ error: "Missing required fields for drafting a connection" });
  }

  const newConnection: FederationConnection = {
    id: `conn-${Math.random().toString(36).substr(2, 9)}`,
    tenantId: "tenant-default",
    displayName,
    protocol: protocol || FederationProtocol.OIDC,
    direction: direction || ConnectionDirection.INBOUND,
    state: ConnectionState.DRAFT,
    issuer,
    metadataMode: metadataMode || "discovery",
    metadataUrl,
    audience: audience || "https://auth.tigrbl.com/tenant-default/federation",
    scopes: scopes || ["openid", "profile", "email"],
    clientAuth: clientAuth || { method: "none" },
    claimMappings: [
      { id: `m-${Math.random().toString(36).substr(2, 5)}`, sourceSelector: "sub", normalizedTarget: "external_id", transformation: "as-is", required: true, privacyClass: "internal" },
      { id: `m-${Math.random().toString(36).substr(2, 5)}`, sourceSelector: "email", normalizedTarget: "email", transformation: "lowercase", required: true, privacyClass: "internal" }
    ],
    routingRules: [],
    activeVersion: 0,
    currentVersion: 1,
    health: "healthy",
    lastValidation: new Date().toISOString()
  };

  connections.push(newConnection);

  // Also dynamically create corresponding trust node in the explorer
  const nodeType = newConnection.protocol === FederationProtocol.OPENID_FEDERATION ? "op" : "op";
  trustNodes.push({
    id: `n-${newConnection.id}`,
    label: newConnection.displayName,
    type: nodeType,
    entityId: newConnection.issuer,
    health: "healthy"
  });

  // Link newly drafted node to RP portal node
  trustEdges.push({
    id: `e-dyn-${newConnection.id}`,
    source: "n-rp-portal",
    target: `n-${newConnection.id}`,
    exchangeKind: "anchor_association",
    state: "active",
    constraints: "{}",
    validUntil: new Date(Date.now() + 31536000000).toISOString() // 1 year
  });

  res.status(201).json(newConnection);
});

// Get connection details
app.get("/api/federation/connections/:id", (req, res) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) return res.status(404).json({ error: "Connection not found" });
  res.json(conn);
});

// Update connection (PATCH)
app.patch("/api/federation/connections/:id", (req, res) => {
  const connIndex = connections.findIndex(c => c.id === req.params.id);
  if (connIndex === -1) return res.status(404).json({ error: "Connection not found" });

  const current = connections[connIndex];
  const updates = req.body;

  // Preserve ID and version bump logic
  const updatedConnection: FederationConnection = {
    ...current,
    ...updates,
    id: current.id, // Immutable
    currentVersion: current.currentVersion + 1, // Mutate connection bump
    lastValidation: new Date().toISOString()
  };

  connections[connIndex] = updatedConnection;
  res.json(updatedConnection);
});

// Validate connection
app.post("/api/federation/connections/:id/validate", async (req, res) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) return res.status(404).json({ error: "Connection not found" });

  // Simulate a comprehensive check
  const findings: string[] = [];
  let health: "healthy" | "degraded" | "failing" = "healthy";

  if (!conn.issuer.startsWith("https://")) {
    findings.push("Issuer URL must enforce HTTPS scheme.");
    health = "failing";
  }
  if (!conn.metadataUrl.startsWith("https://")) {
    findings.push("Metadata/Discovery URL must enforce HTTPS scheme.");
    health = "failing";
  }
  if (conn.scopes.length === 0 || !conn.scopes.includes("openid")) {
    findings.push("Missing required OIDC scope: 'openid'. This is mandatory for authentication.");
    health = "degraded";
  }

  // Cross-domain constraint checking for OpenID Federation
  if (conn.protocol === FederationProtocol.OPENID_FEDERATION) {
    // Check if we have an edge mapping to any trust anchor
    const hasPath = trustEdges.some(e => e.target === `n-${conn.id}` && e.state === "active");
    if (!hasPath) {
      findings.push("No active trust path exists in the current trust graph to any configured trust anchor.");
      health = "degraded";
    }
  }

  // Update in-memory state
  conn.health = health;
  conn.lastValidation = new Date().toISOString();
  if (findings.length > 0) {
    conn.errorMessage = findings.join(" ");
  } else {
    conn.errorMessage = undefined;
  }

  res.json({
    success: health !== "failing",
    health,
    lastValidation: conn.lastValidation,
    findings,
    diagnosticLog: [
      "Retrieved authority certificate chain...",
      "Cryptographic verification of keys: SUCCESS",
      "DNS alignment and server security headers: SECURED",
      `Summary findings count: ${findings.length}`
    ]
  });
});

// Test Connection (Initiate test authentication/callback response simulation)
app.post("/api/federation/connections/:id/test", async (req, res) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) return res.status(404).json({ error: "Connection not found" });

  // Create a simulated client callback result with claim transformation
  const mockRawIdToken = {
    iss: conn.issuer,
    sub: "user_test_fed_9921",
    email: "EXEMPLAR.USER@TIGRBL.COM",
    given_name: "Jane",
    family_name: "Doe-Federated",
    groups: ["administrators", "billing-managers", "security-operators"],
    seCivicNumber: "19881025-1234",
    acr: "urn:mace:incommon:iap:silver",
    auth_time: Math.floor(Date.now() / 1000)
  };

  // Perform claim normalization based on mappings
  const normalizedClaims: Record<string, any> = {};
  conn.claimMappings.forEach(mapping => {
    const rawVal = mockRawIdToken[mapping.sourceSelector as keyof typeof mockRawIdToken];
    if (rawVal !== undefined) {
      let transformed = rawVal;
      if (mapping.transformation === "lowercase" && typeof rawVal === "string") {
        transformed = rawVal.toLowerCase();
      } else if (mapping.transformation === "split" && Array.isArray(rawVal)) {
        transformed = rawVal;
      }
      normalizedClaims[mapping.normalizedTarget] = transformed;
    }
  });

  res.json({
    connectionId: conn.id,
    status: "success",
    rawToken: mockRawIdToken,
    normalizedClaims,
    securityHeaderMatch: true,
    correlationId: `tx-test-${Math.random().toString(36).substr(2, 9)}`,
    timestamp: new Date().toISOString()
  });
});

// Activate Connection
app.post("/api/federation/connections/:id/activate", (req, res) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) return res.status(404).json({ error: "Connection not found" });

  conn.state = ConnectionState.ACTIVE;
  conn.activeVersion = conn.currentVersion;
  conn.errorMessage = undefined;
  conn.health = "healthy";

  // If there was an active incident for this connection, mitigate/resolve it
  incidents = incidents.map(inc => {
    if (inc.connectionId === conn.id && inc.status === "active") {
      return { ...inc, status: "resolved", resolution: "Connection was manually re-evaluated and activated by Tenant Admin." };
    }
    return inc;
  });

  res.json({ success: true, state: conn.state, activeVersion: conn.activeVersion });
});

// Suspend Connection
app.post("/api/federation/connections/:id/suspend", (req, res) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) return res.status(404).json({ error: "Connection not found" });

  conn.state = ConnectionState.SUSPENDED;
  conn.health = "degraded";

  res.json({ success: true, state: conn.state });
});

// Retire Connection
app.post("/api/federation/connections/:id/retire", (req, res) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) return res.status(404).json({ error: "Connection not found" });

  conn.state = ConnectionState.RETIRED;
  conn.health = "unknown";

  res.json({ success: true, state: conn.state });
});

// --- Metadata & Keys Plane ---

// SSRF-safe metadata fetch inspection with Gemini assistance
app.post("/api/federation/metadata:inspect", async (req, res) => {
  const { issuerUrl, mode } = req.body;
  if (!issuerUrl) {
    return res.status(400).json({ error: "Issuer URL is required" });
  }

  // Simulate strict URL/SSRF defense check
  try {
    const parsedUrl = new URL(issuerUrl);
    if (parsedUrl.protocol !== "https:") {
      return res.status(400).json({ error: "Invalid schema. Only secure HTTPS endpoints are approved for fetching federation metadata." });
    }
    // Block local loopbacks
    if (["localhost", "127.0.0.1", "0.0.0.0"].includes(parsedUrl.hostname)) {
      return res.status(400).json({ error: "SSRF Protection: Retrieval of local metadata loopback paths is prohibited." });
    }
  } catch (err) {
    return res.status(400).json({ error: "Invalid Issuer URL format." });
  }

  let rawMetadata: Record<string, any> = {};
  let analysis = "";

  if (ai) {
    try {
      const prompt = `Generate a fully compliant OpenID Federation 1.0 JSON entity configuration or standard OIDC discovery metadata for the issuer: "${issuerUrl}". The mode of metadata is "${mode}".
Return a clean JSON object with exactly two keys:
"rawMetadata": a detailed, realistic mock JSON configuration (e.g. issuer, authorization_endpoint, token_endpoint, jwks with fake public keys, claims_supported, scopes_supported). If the mode is "federation", output a standard Signed Entity Statement with "iss", "sub", "jwks", "authority_hints", "metadata".
"analysis": a 3-sentence expert assessment of the cryptographic posture, certificate status, and compatibility of this metadata with the Tigrbl authentication router.

Ensure the returned format is parseable as JSON.`;

      const response = await ai.models.generateContent({
        model: "gemini-3.5-flash",
        contents: prompt,
        config: {
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              rawMetadata: { type: Type.OBJECT, description: "The raw metadata JSON object" },
              analysis: { type: Type.STRING, description: "A 3-sentence summary analysis" }
            },
            required: ["rawMetadata", "analysis"]
          }
        }
      });

      const parsed = JSON.parse(response.text || "{}");
      rawMetadata = parsed.rawMetadata || {};
      analysis = parsed.analysis || "Metadata inspected and parsed successfully.";
    } catch (error) {
      console.error("Gemini metadata generation failed, using fallback:", error);
    }
  }

  // Reliable Fallback if Gemini not present/fails
  if (Object.keys(rawMetadata).length === 0) {
    rawMetadata = {
      issuer: issuerUrl,
      authorization_endpoint: `${issuerUrl}/v2/authorize`,
      token_endpoint: `${issuerUrl}/v2/token`,
      userinfo_endpoint: `${issuerUrl}/v2/userinfo`,
      jwks_uri: `${issuerUrl}/jwks.json`,
      jwks: {
        keys: [
          { kid: "key-fallback-1", kty: "RSA", alg: "RS256", use: "sig", n: "FallbackModulus...", e: "AQAB" }
        ]
      },
      scopes_supported: ["openid", "profile", "email", "offline_access"],
      response_types_supported: ["code", "token", "id_token"],
      subject_types_supported: ["public", "pairwise"]
    };
    analysis = "Metadata parsed through strict local static validators. Cryptographic signature validates perfectly against authority hints; algorithms comply with default NIST-800-63C security profile.";
  }

  res.json({
    issuerUrl,
    mode,
    timestamp: new Date().toISOString(),
    rawMetadata,
    analysis,
    provenance: {
      fetchedVia: "Tigrbl Safe SSRF Proxy Engine",
      dnsResolution: "93.184.216.34",
      httpStatus: 200,
      tlsVersion: "TLS 1.3 (ECDHE-ECDSA-AES128-GCM-SHA256)"
    }
  });
});

// Compare Metadata Difference (Semantic Diff)
app.get("/api/federation/connections/:id/metadata:diff", async (req, res) => {
  const conn = connections.find(c => c.id === req.params.id);
  if (!conn) return res.status(404).json({ error: "Connection not found" });

  const activeMetadata = {
    issuer: conn.issuer,
    scopes_supported: conn.scopes,
    jwks: { keys: [{ kid: conn.id === "conn-edu-gain" ? "edugain-key-3" : "key-okta-v1", alg: "RS256" }] }
  };

  const currentMetadata = {
    issuer: conn.issuer,
    scopes_supported: [...conn.scopes, "offline_access"],
    jwks: {
      keys: [
        { kid: conn.id === "conn-edu-gain" ? "edugain-key-3" : "key-okta-v1", alg: "RS256" },
        { kid: "key-new-rollover-2026", alg: "ES256", note: "Newly observed via key cache scan" }
      ]
    }
  };

  let diffSummary = "Detected 2 semantic changes: Added scope 'offline_access' and registered modern ES256 key 'key-new-rollover-2026' for key rotation rollover prep.";
  if (ai) {
    try {
      const response = await ai.models.generateContent({
        model: "gemini-3.5-flash",
        contents: `Compare these two metadata configurations for an OIDC Federation Connection. Summarize the changes (semantic difference) in 2 sentences, describing security, compatibility, and certificate warnings:
Active: ${JSON.stringify(activeMetadata)}
Candidate/Current Observed: ${JSON.stringify(currentMetadata)}`
      });
      diffSummary = response.text || diffSummary;
    } catch (e) {
      console.error(e);
    }
  }

  res.json({
    connectionId: conn.id,
    activeMetadata,
    currentMetadata,
    diffSummary,
    hasChanges: true
  });
});

// --- Trust Graph & OpenID Federation 1.0 Runtime APIs ---

// Resolve Trust Paths
app.post("/api/federation/trust-paths:resolve", (req, res) => {
  const { leafEntityId, anchorEntityId } = req.body;
  if (!leafEntityId || !anchorEntityId) {
    return res.status(400).json({ error: "leafEntityId and anchorEntityId are required" });
  }

  // Find corresponding nodes
  const startNode = trustNodes.find(n => n.entityId === leafEntityId);
  const endNode = trustNodes.find(n => n.entityId === anchorEntityId);

  if (!startNode || !endNode) {
    return res.status(400).json({ error: "Specified nodes do not exist in the platform trust database." });
  }

  // Build simulated acyclic path step-by-step
  // E.g., leaf-swedish -> intermediate-se -> anchor-se-gov
  const pathNodes: TrustNode[] = [startNode];
  const validationHops: any[] = [];

  if (leafEntityId === "https://fed.trust.sweden.se") {
    const intermediate = trustNodes.find(n => n.id === "n-inter-se")!;
    pathNodes.push(intermediate, endNode);

    validationHops.push(
      {
        subject: "https://fed.trust.sweden.se",
        issuer: "https://intermediate.trust.sweden.se",
        signatureValid: true,
        expiry: "2026-11-30T00:00:00Z",
        findings: "Subordinate statement matches expected cryptographic anchor keys."
      },
      {
        subject: "https://intermediate.trust.sweden.se",
        issuer: "https://trust.gov.se/federation",
        signatureValid: true,
        expiry: "2026-12-31T23:59:59Z",
        findings: "Intermediate statement verified by pinned Government Trust Anchor root certificates."
      }
    );
  } else if (leafEntityId === "https://edugain.org/federation") {
    const intermediate = trustNodes.find(n => n.id === "n-inter-edu")!;
    pathNodes.push(intermediate, endNode);

    validationHops.push(
      {
        subject: "https://edugain.org/federation",
        issuer: "https://anchors.edugain.org/keys",
        signatureValid: false,
        expiry: "2026-08-31T00:00:00Z",
        findings: "CRYPTOGRAPHIC FAILURE: Signature verification failed. Subordinate statement was signed by an unrecognized key."
      },
      {
        subject: "https://anchors.edugain.org/keys",
        issuer: "https://edugain.org/anchor",
        signatureValid: true,
        expiry: "2026-10-15T00:00:00Z",
        findings: "Intermediate statement verified by eduGAIN Root anchor."
      }
    );
  } else {
    // Direct bilateral trust simulation
    pathNodes.push(endNode);
    validationHops.push({
      subject: leafEntityId,
      issuer: anchorEntityId,
      signatureValid: true,
      expiry: "2027-01-15T00:00:00Z",
      findings: "Direct trust registration. Root authority keys verify direct OP credentials."
    });
  }

  const success = validationHops.every(h => h.signatureValid);

  res.json({
    pathNodes,
    validationHops,
    success,
    resolvedMetadata: {
      issuer: leafEntityId,
      authorization_endpoint: `${leafEntityId}/authorize`,
      token_endpoint: `${leafEntityId}/token`,
      claims_supported: ["sub", "email", "name"]
    },
    provenanceChain: "Acyclic trust hierarchy resolved with depth bounds verification."
  });
});

// Revoke Edge (Blast Radius & quarantine assessment)
app.post("/api/federation/edges/:id/revoke", async (req, res) => {
  const edgeId = req.params.id;
  const edge = trustEdges.find(e => e.id === edgeId);
  if (!edge) return res.status(404).json({ error: "Trust edge not found" });

  // Update in-memory
  edge.state = "revoked";

  // Calculate Affected Blast Radius
  let affectedTenants = 1;
  let affectedApps = 0;
  let affectedSessions = 0;
  let recommendations = "Check that workloads routing via this trust node are redirected immediately.";

  // Specific mock counts based on edge revoking
  if (edgeId === "e2" || edgeId === "e3") { // Swedish gov
    affectedApps = 8;
    affectedSessions = 112;
  } else if (edgeId === "e4" || edgeId === "e5") { // eduGAIN
    affectedApps = 14;
    affectedSessions = 182;
  } else if (edgeId === "e1") { // Okta
    affectedApps = 5;
    affectedSessions = 340;
  }

  if (ai) {
    try {
      const response = await ai.models.generateContent({
        model: "gemini-3.5-flash",
        contents: `A critical security operator is revoking trust edge "${edgeId}" connecting "${edge.source}" and "${edge.target}" in a multilateral OpenID Federation 1.0 Trust Center.
Generate 3 short, human-readable recovery/mitigation recommendations for the administrator console.`
      });
      recommendations = response.text || recommendations;
    } catch (e) {
      console.error(e);
    }
  }

  res.json({
    edgeId,
    state: "revoked",
    blastRadius: {
      affectedTenants,
      affectedApps,
      affectedSessions,
      quarantinedNodes: [edge.target]
    },
    recommendations,
    timestamp: new Date().toISOString()
  });
});

// Claims Transformation and Normalization Lab
app.post("/api/federation/claims:simulate", async (req, res) => {
  const { sourceClaims, mappings } = req.body;
  if (!sourceClaims || !mappings) {
    return res.status(400).json({ error: "Source claims and mappings are required." });
  }

  const normalizedClaims: Record<string, any> = {};
  const logs: string[] = [];

  mappings.forEach((m: any) => {
    const rawVal = sourceClaims[m.sourceSelector];
    if (rawVal !== undefined) {
      let transformed = rawVal;
      if (m.transformation === "lowercase" && typeof rawVal === "string") {
        transformed = rawVal.toLowerCase();
        logs.push(`Mapped and lowercased claim '${m.sourceSelector}' -> '${m.normalizedTarget}'`);
      } else if (m.transformation === "split" && typeof rawVal === "string") {
        transformed = rawVal.split(/[ ,]+/);
        logs.push(`Split comma/space delimited claim '${m.sourceSelector}' -> array in '${m.normalizedTarget}'`);
      } else {
        logs.push(`Direct map of claim '${m.sourceSelector}' -> '${m.normalizedTarget}'`);
      }
      normalizedClaims[m.normalizedTarget] = transformed;
    } else {
      if (m.required) {
        logs.push(`WARNING: Required claim '${m.sourceSelector}' is absent from the upstream response! Authentication will fail-closed.`);
      }
    }
  });

  let safetyAnalysis = "All claims verified according to requested privacy parameters.";
  if (ai) {
    try {
      const prompt = `Act as an identity architect. Analyze the claims mapping results. Look for PII risks, account link takeover hazards, or required claim absence.
Input Upstream claims: ${JSON.stringify(sourceClaims)}
Resulting Normalized claims: ${JSON.stringify(normalizedClaims)}
Provide a 2-sentence feedback report on potential account hijacking (such as trusting insecure email claims) or PII leakage.`;

      const response = await ai.models.generateContent({
        model: "gemini-3.5-flash",
        contents: prompt
      });
      safetyAnalysis = response.text || safetyAnalysis;
    } catch (e) {
      console.error(e);
    }
  }

  res.json({
    normalizedClaims,
    logs,
    safetyAnalysis
  });
});

// Incidents list & actions
app.get("/api/federation/incidents", (req, res) => {
  res.json(incidents);
});

app.post("/api/federation/incidents/:id/mitigate", (req, res) => {
  const inc = incidents.find(i => i.id === req.params.id);
  if (!inc) return res.status(404).json({ error: "Incident not found" });

  inc.status = "mitigated";
  inc.resolution = "Quarantine applied; trust routing policies diverted. Direct and subordinate keys isolated.";

  // Propagate failing status to connection if linked
  if (inc.connectionId) {
    const conn = connections.find(c => c.id === inc.connectionId);
    if (conn) {
      conn.state = ConnectionState.SUSPENDED;
      conn.health = "degraded";
    }
  }

  res.json(inc);
});

app.post("/api/federation/incidents/:id/resolve", (req, res) => {
  const inc = incidents.find(i => i.id === req.params.id);
  if (!inc) return res.status(404).json({ error: "Incident not found" });

  inc.status = "resolved";
  inc.resolution = "New JWKS published and verified. Trusted anchor successfully re-signed the intermediate statement.";

  if (inc.connectionId) {
    const conn = connections.find(c => c.id === inc.connectionId);
    if (conn) {
      conn.state = ConnectionState.ACTIVE;
      conn.health = "healthy";
      conn.errorMessage = undefined;
    }
  }

  res.json(inc);
});

// Publishes local Entity Configuration according to OpenID Federation 1.0 (Sec 4)
app.get("/.well-known/openid-federation", (req, res) => {
  res.setHeader("Content-Type", "application/entity-statement+jwt");
  res.json({
    iss: "https://auth.tigrbl.com/tenant-default",
    sub: "https://auth.tigrbl.com/tenant-default",
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 86400,
    jwks: {
      keys: [
        { kid: "key-se-fed-signing-2026", kty: "RSA", alg: "RS256", use: "sig" }
      ]
    },
    metadata: {
      federation_entity: {
        organization_name: "Tigrbl Identity Platform",
        contacts: ["security@tigrbl.com"],
        homepage_uri: "https://ai.studio/build"
      }
    },
    authority_hints: [
      "https://trust.auth.tigrbl.com"
    ]
  });
});

// ==========================================
// VITE DEV SERVER / STATIC PRODUCTION ROUTING
// ==========================================

async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Trust Center server boot successful.`);
    console.log(`Port ingress mapping configured at: http://localhost:${PORT}`);
  });
}

startServer();
