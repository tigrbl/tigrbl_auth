import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";

// Interfaces to represent Service Admin domain objects
export interface ServiceIdentity {
  id: string;
  name: string;
  subject: string;
  tenant: string;
  realm: string;
  owner: string; // Team or contact, e.g. "billing-team"
  purpose: string;
  environment: "Production" | "Staging" | "Development";
  state: "Active" | "Suspended";
  createdAt: string;
  updatedAt: string;
  lastActive: string | null;
}

export interface CredentialServiceKey {
  id: string;
  serviceId: string;
  algorithm: "RS256" | "ES256" | "EdDSA";
  state: "Active" | "Suspended" | "Retired" | "Revoked" | "Expired";
  createdAt: string;
  activatedAt: string | null;
  expiresAt: string;
  lastUsedAt: string | null;
  publicFingerprint: string;
  rotationRelationship: string; // e.g. "Initial key" or "Rotated from key_..."
  secretMaterial?: string; // Revealed ONCE
}

export interface CredentialApiKey {
  id: string;
  serviceId: string;
  owner: string;
  purpose: string;
  scopes: string[];
  environment: "Production" | "Staging" | "Development";
  state: "Active" | "Revoked" | "Expired";
  expiresAt: string;
  createdAt: string;
  lastUsedAt: string | null;
  keyPrefix: string;
  networkConstraints?: string;
  secretMaterial?: string; // Revealed ONCE
}

export interface TokenRecord {
  id: string;
  serviceId: string | null;
  subject: string;
  issuer: string;
  audience: string;
  scopes: string[];
  issuedAt: string;
  expiresAt: string;
  state: "Active" | "Expired" | "Revoked" | "Stale";
  validationOutcome: "Allowed" | "Denied";
  validationReason: string;
}

export interface AuditEvent {
  id: string;
  serviceId: string | null;
  actor: string;
  action: string;
  target: string;
  permissionDelta: string | null;
  outcome: "Success" | "Failure";
  timestamp: string;
  correlationId: string;
  details: string;
}

export interface RotationEvent {
  id: string;
  serviceId: string;
  oldKeyId: string;
  newKeyId: string;
  actor: string;
  reason: string;
  status: "Requested" | "Generated" | "Staged" | "Activated" | "Propagated" | "Retiring" | "Completed" | "Failed";
  timestamp: string;
  failureReason: string | null;
  retryCount: number;
  correlationId: string;
}

// Global In-Memory Database (Fully Resettable)
let services: ServiceIdentity[] = [];
let serviceKeys: CredentialServiceKey[] = [];
let apiKeys: CredentialApiKey[] = [];
let tokenRecords: TokenRecord[] = [];
let auditEvents: AuditEvent[] = [];
let rotationEvents: RotationEvent[] = [];

// Helper to seed high-fidelity fixtures
function seedDatabase() {
  const now = new Date();
  
  services = [
    {
      id: "svc-pay-prod",
      name: "payment-gateway-prod",
      subject: "spn:realm-us:tenant-alpha:svc:payment-gateway",
      tenant: "tenant-alpha",
      realm: "realm-us",
      owner: "billing-platform-team",
      purpose: "Core stripe card processing and invoice settlement",
      environment: "Production",
      state: "Active",
      createdAt: "2026-01-15T08:00:00Z",
      updatedAt: "2026-07-10T12:00:00Z",
      lastActive: "2026-07-12T17:15:00Z"
    },
    {
      id: "svc-user-sync",
      name: "user-profile-sync",
      subject: "spn:realm-eu:tenant-alpha:svc:user-profile-sync",
      tenant: "tenant-alpha",
      realm: "realm-eu",
      owner: "identity-team",
      purpose: "Synchronize user details and permission shards across datacenters",
      environment: "Production",
      state: "Active",
      createdAt: "2026-03-10T09:30:00Z",
      updatedAt: "2026-03-10T09:30:00Z",
      lastActive: "2026-07-12T17:01:00Z"
    },
    {
      id: "svc-legacy-rep",
      name: "legacy-reporting-svc",
      subject: "spn:realm-us:tenant-beta:svc:legacy-reporting",
      tenant: "tenant-beta",
      realm: "realm-us",
      owner: "analytics-team",
      purpose: "Legacy database reporter scheduling script",
      environment: "Staging",
      state: "Suspended", // Suspended service with Active Keys! (Dashboard alert)
      createdAt: "2025-05-12T14:00:00Z",
      updatedAt: "2026-07-11T12:00:00Z",
      lastActive: "2026-07-11T12:00:00Z"
    },
    {
      id: "svc-abandoned",
      name: "abandoned-alert-svc",
      subject: "spn:realm-us:tenant-alpha:svc:abandoned-alert",
      tenant: "tenant-alpha",
      realm: "realm-us",
      owner: "", // Missing Owner! (Dashboard alert)
      purpose: "Temporary forwarding tool that was never decomissioned",
      environment: "Development",
      state: "Active",
      createdAt: "2026-02-18T11:00:00Z",
      updatedAt: "2026-02-18T11:00:00Z",
      lastActive: "2026-04-12T11:00:00Z" // Stale active credential/identity
    },
    {
      id: "svc-compliance",
      name: "compliance-audit-prod",
      subject: "spn:realm-us:tenant-omega:svc:compliance-audit",
      tenant: "tenant-omega",
      realm: "realm-us",
      owner: "security-team",
      purpose: "Log validation metadata and compliance rotation audits",
      environment: "Production",
      state: "Active",
      createdAt: "2026-04-01T09:00:00Z",
      updatedAt: "2026-07-11T14:30:00Z",
      lastActive: "2026-07-12T17:00:00Z"
    }
  ];

  serviceKeys = [
    {
      id: "key-pay-active",
      serviceId: "svc-pay-prod",
      algorithm: "RS256",
      state: "Active",
      createdAt: "2026-06-01T00:00:00Z",
      activatedAt: "2026-06-01T00:05:00Z",
      expiresAt: "2026-12-01T00:00:00Z",
      lastUsedAt: "2026-07-12T17:15:00Z",
      publicFingerprint: "sha256:d8:e2:fb:24:99:a4:bf:cf:11:ea:23:44:8a:bc:ef:90",
      rotationRelationship: "Rotated from key-pay-old"
    },
    {
      id: "key-sync-expiring", // Expiring very soon!
      serviceId: "svc-user-sync",
      algorithm: "ES256",
      state: "Active",
      createdAt: "2026-01-12T10:00:00Z",
      activatedAt: "2026-01-12T10:05:00Z",
      expiresAt: "2026-07-14T17:22:00Z", // Within 48 hours
      lastUsedAt: "2026-07-12T16:45:00Z",
      publicFingerprint: "sha256:a4:23:cd:9f:ef:bc:01:9a:77:88:99:bb:aa:cc:11:ee",
      rotationRelationship: "Initial key"
    },
    {
      id: "key-legacy-active", // Active key on suspended service alert!
      serviceId: "svc-legacy-rep",
      algorithm: "RS256",
      state: "Active",
      createdAt: "2025-05-12T14:05:00Z",
      activatedAt: "2025-05-12T14:10:00Z",
      expiresAt: "2027-05-12T14:00:00Z",
      lastUsedAt: "2026-07-11T12:00:00Z",
      publicFingerprint: "sha256:ff:88:9a:bc:23:45:67:89:11:22:33:44:55:66:77:88",
      rotationRelationship: "Initial key"
    },
    {
      id: "key-abandoned-active", // Orphaned key with missing owner
      serviceId: "svc-abandoned",
      algorithm: "EdDSA",
      state: "Active",
      createdAt: "2026-02-18T11:05:00Z",
      activatedAt: "2026-02-18T11:10:00Z",
      expiresAt: "2028-02-18T11:00:00Z",
      lastUsedAt: "2026-04-12T11:00:00Z",
      publicFingerprint: "sha256:bb:22:cc:dd:ee:ff:11:22:33:44:55:66:77:88:99:aa",
      rotationRelationship: "Initial key"
    },
    {
      id: "key-compliance-failed",
      serviceId: "svc-compliance",
      algorithm: "RS256",
      state: "Retired", // Failed rotation backup
      createdAt: "2026-04-01T09:05:00Z",
      activatedAt: "2026-04-01T09:10:00Z",
      expiresAt: "2026-10-01T09:00:00Z",
      lastUsedAt: "2026-07-12T17:00:00Z",
      publicFingerprint: "sha256:77:88:99:aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66",
      rotationRelationship: "Retiring to key-compliance-new"
    }
  ];

  apiKeys = [
    {
      id: "apikey-pay-active",
      serviceId: "svc-pay-prod",
      owner: "billing-platform-team",
      purpose: "Stripe secure charge dispatch and processing",
      scopes: ["charge:create", "charge:read", "refund:create"],
      environment: "Production",
      state: "Active",
      expiresAt: "2027-01-01T00:00:00Z",
      createdAt: "2026-06-01T00:00:00Z",
      lastUsedAt: "2026-07-12T17:10:00Z",
      keyPrefix: "tg_live_chrg_ab12",
      networkConstraints: "10.240.0.0/16, 192.168.1.0/24"
    },
    {
      id: "apikey-sync-broad", // Overbroad scope wildcard alert!
      serviceId: "svc-user-sync",
      owner: "identity-team",
      purpose: "Broad system query access to identity directory",
      scopes: ["*"], // Wildcard!
      environment: "Production",
      state: "Active",
      expiresAt: "2026-09-01T00:00:00Z",
      createdAt: "2026-03-10T10:00:00Z",
      lastUsedAt: "2026-07-12T17:01:00Z",
      keyPrefix: "tg_live_id_wild_99ef"
    }
  ];

  tokenRecords = [
    {
      id: "tok_01j2f5a_f",
      serviceId: "svc-pay-prod",
      subject: "spn:realm-us:tenant-alpha:svc:payment-gateway",
      issuer: "https://auth.tigrbl.net/oauth/v2/tenant-alpha",
      audience: "https://api.tigrbl.net/payments",
      scopes: ["charge:create", "charge:read"],
      issuedAt: "2026-07-12T17:10:00Z",
      expiresAt: "2026-07-12T18:10:00Z",
      state: "Active",
      validationOutcome: "Allowed",
      validationReason: "Token verified via JWKS, signatures match, claims within boundaries"
    },
    {
      id: "tok_01j2f5b_f",
      serviceId: "svc-user-sync",
      subject: "spn:realm-eu:tenant-alpha:svc:user-profile-sync",
      issuer: "https://auth.tigrbl.net/oauth/v2/tenant-alpha",
      audience: "https://api.tigrbl.net/users",
      scopes: ["*"],
      issuedAt: "2026-07-12T16:00:00Z",
      expiresAt: "2026-07-12T17:00:00Z",
      state: "Expired",
      validationOutcome: "Denied",
      validationReason: "Token expired at 17:00:00Z (current evaluation time: 17:22:50Z)"
    },
    {
      id: "tok_01j2f5c_f",
      serviceId: "svc-legacy-rep",
      subject: "spn:realm-us:tenant-beta:svc:legacy-reporting",
      issuer: "https://auth.tigrbl.net/oauth/v2/tenant-beta",
      audience: "https://api.tigrbl.net/reports",
      scopes: ["reports:read"],
      issuedAt: "2026-07-11T11:00:00Z",
      expiresAt: "2026-07-11T12:00:00Z",
      state: "Revoked",
      validationOutcome: "Denied",
      validationReason: "Associated service principal identity 'svc-legacy-rep' is Suspended"
    }
  ];

  auditEvents = [
    {
      id: "aud_01j2f_1",
      serviceId: "svc-pay-prod",
      actor: "platform-lead@tigrbl.com",
      action: "service.update",
      target: "svc-pay-prod",
      permissionDelta: null,
      outcome: "Success",
      timestamp: "2026-07-10T12:00:00Z",
      correlationId: "tx_01j2f_ab",
      details: "Updated description and team mapping metadata for payment-gateway-prod"
    },
    {
      id: "aud_01j2f_2",
      serviceId: "svc-compliance",
      actor: "operator-compliance@tigrbl.com",
      action: "key.rotate",
      target: "key-compliance-failed",
      permissionDelta: null,
      outcome: "Failure",
      timestamp: "2026-07-11T14:30:00Z",
      correlationId: "tx_01j2f5i",
      details: "Failed to rotate key for compliance-audit-prod. Propagation timeout on regional hosts."
    },
    {
      id: "aud_01j2f_3",
      serviceId: "svc-pay-prod",
      actor: "system-automation@tigrbl.com",
      action: "key.rotate",
      target: "key-pay-active",
      permissionDelta: null,
      outcome: "Success",
      timestamp: "2026-06-01T00:05:00Z",
      correlationId: "tx_01j2f5j",
      details: "Completed automated rotation cycle. Issued key-pay-active and retired old credential."
    },
    {
      id: "aud_01j2f_4",
      serviceId: "svc-user-sync",
      actor: "identity-lead@tigrbl.com",
      action: "apikey.create",
      target: "apikey-sync-broad",
      permissionDelta: "+ *",
      outcome: "Success",
      timestamp: "2026-03-10T10:00:00Z",
      correlationId: "tx_01j2f_cd",
      details: "Created API key apikey-sync-broad with broad scope permission wildcard"
    },
    {
      id: "aud_01j2f_5",
      serviceId: "svc-legacy-rep",
      actor: "sec-admin@tigrbl.com",
      action: "service.suspend",
      target: "svc-legacy-rep",
      permissionDelta: null,
      outcome: "Success",
      timestamp: "2026-07-11T12:00:00Z",
      correlationId: "tx_01j2f_ef",
      details: "Suspended workload identity legacy-reporting-svc due to inactivity and security policy"
    }
  ];

  rotationEvents = [
    {
      id: "rot_01j2f_fail",
      serviceId: "svc-compliance",
      oldKeyId: "key-compliance-failed",
      newKeyId: "key-compliance-pending",
      actor: "operator-compliance@tigrbl.com",
      reason: "Scheduled quarterly credential rotation",
      status: "Failed",
      timestamp: "2026-07-11T14:30:00Z",
      failureReason: "Key propagation timed out on region-us-west cluster. Edge sync failed.",
      retryCount: 3,
      correlationId: "tx_01j2f5i"
    },
    {
      id: "rot_01j2f_ok",
      serviceId: "svc-pay-prod",
      oldKeyId: "key-pay-old",
      newKeyId: "key-pay-active",
      actor: "system-automation@tigrbl.com",
      reason: "Automated 30-day rotation compliance",
      status: "Completed",
      timestamp: "2026-06-01T00:05:00Z",
      failureReason: null,
      retryCount: 0,
      correlationId: "tx_01j2f5j"
    }
  ];
}

// Initialize seed
seedDatabase();

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API base route log
  app.use((req, res, next) => {
    // Basic request logger for audit context
    next();
  });

  // -----------------------------------------------------------------
  // SYSTEM SEED RESET ENDPOINT
  // -----------------------------------------------------------------
  app.post("/api/reset", (req, res) => {
    seedDatabase();
    // Add audit log for reset
    auditEvents.unshift({
      id: "aud_reset_" + Date.now(),
      serviceId: null,
      actor: "operator@tigrbl.com",
      action: "system.reset",
      target: "database",
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_reset_" + Math.random().toString(36).substr(2, 9),
      details: "System database and seeded fixtures reinitialized to defaults."
    });
    res.json({ message: "Database reset to initial high-fidelity seeded state." });
  });

  // -----------------------------------------------------------------
  // PROVIDER METADATA ENDPOINTS
  // -----------------------------------------------------------------
  app.get("/api/metadata/provider", (req, res) => {
    const { scope, tenant, realm } = req.query;
    res.json({
      issuer: `https://auth.tigrbl.net/oauth/v2/${tenant || "global"}${realm ? `/${realm}` : ""}`,
      jwks_uri: `https://auth.tigrbl.net/oauth/v2/${tenant || "global"}/jwks`,
      token_endpoint: `https://auth.tigrbl.net/oauth/v2/${tenant || "global"}/token`,
      introspection_endpoint: `https://auth.tigrbl.net/oauth/v2/${tenant || "global"}/introspect`,
      revocation_endpoint: `https://auth.tigrbl.net/oauth/v2/${tenant || "global"}/revoke`,
      supported_algorithms: ["RS256", "ES256", "EdDSA"],
      scopes_supported: ["*", "charge:create", "charge:read", "refund:create", "reports:read", "identity:query"],
      grant_types_supported: ["client_credentials"]
    });
  });

  app.get("/api/metadata/jwks", (req, res) => {
    res.json({
      keys: [
        {
          kty: "RSA",
          use: "sig",
          alg: "RS256",
          kid: "key-pay-active",
          n: "u1W_A3zYq0Y7YpD8...",
          e: "AQAB"
        },
        {
          kty: "EC",
          use: "sig",
          alg: "ES256",
          crv: "P-256",
          kid: "key-sync-expiring",
          x: "f83OJ3D2xF...",
          y: "x_daS31ldD..."
        }
      ]
    });
  });

  // -----------------------------------------------------------------
  // SERVICE IDENTITIES (WORKLOADS) ENDPOINTS
  // -----------------------------------------------------------------
  app.get("/api/services", (req, res) => {
    res.json(services);
  });

  app.get("/api/services/:id", (req, res) => {
    const service = services.find(s => s.id === req.params.id);
    if (!service) {
      return res.status(404).json({ error: "Service identity not found" });
    }
    res.json(service);
  });

  app.post("/api/services", (req, res) => {
    const { name, tenant, realm, owner, purpose, environment } = req.body;
    
    if (!name || !tenant || !realm || !purpose || !environment) {
      return res.status(400).json({ error: "Missing required service parameters" });
    }

    const cleanName = name.toLowerCase().replace(/[^a-z0-9-]/g, "-");
    const id = `svc-${cleanName}-${Math.random().toString(36).substring(2, 6)}`;
    const subject = `spn:${realm}:${tenant}:svc:${cleanName}`;

    // Validate if name already exists
    if (services.some(s => s.name === name)) {
      return res.status(400).json({ error: `Service identity with name '${name}' already exists.` });
    }

    const newService: ServiceIdentity = {
      id,
      name,
      subject,
      tenant,
      realm,
      owner: owner || "",
      purpose,
      environment,
      state: "Active",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      lastActive: null
    };

    services.push(newService);

    // Audit log
    auditEvents.unshift({
      id: "aud_svc_" + Date.now(),
      serviceId: id,
      actor: "operator@tigrbl.com",
      action: "service.create",
      target: id,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_svc_" + Math.random().toString(36).substring(2, 8),
      details: `Created service workload identity ${name} (${subject})`
    });

    res.status(201).json(newService);
  });

  app.put("/api/services/:id", (req, res) => {
    const serviceIndex = services.findIndex(s => s.id === req.params.id);
    if (serviceIndex === -1) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const service = services[serviceIndex];
    const { owner, purpose, environment } = req.body;

    const originalOwner = service.owner;
    const originalPurpose = service.purpose;

    services[serviceIndex] = {
      ...service,
      owner: owner !== undefined ? owner : service.owner,
      purpose: purpose !== undefined ? purpose : service.purpose,
      environment: environment !== undefined ? environment : service.environment,
      updatedAt: new Date().toISOString()
    };

    // Audit log
    auditEvents.unshift({
      id: "aud_svc_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "service.update",
      target: service.id,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_svc_" + Math.random().toString(36).substring(2, 8),
      details: `Updated service metadata. Owner: '${originalOwner}'->'${owner}', Purpose: '${originalPurpose}'->'${purpose}'`
    });

    res.json(services[serviceIndex]);
  });

  app.post("/api/services/:id/suspend", (req, res) => {
    const serviceIndex = services.findIndex(s => s.id === req.params.id);
    if (serviceIndex === -1) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const service = services[serviceIndex];
    services[serviceIndex].state = "Suspended";
    services[serviceIndex].updatedAt = new Date().toISOString();

    // Audit log
    auditEvents.unshift({
      id: "aud_svc_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "service.suspend",
      target: service.id,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_svc_" + Math.random().toString(36).substring(2, 8),
      details: `Suspended service workload. Associated keys and API keys will fail authentication checks.`
    });

    res.json(services[serviceIndex]);
  });

  app.post("/api/services/:id/activate", (req, res) => {
    const serviceIndex = services.findIndex(s => s.id === req.params.id);
    if (serviceIndex === -1) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const service = services[serviceIndex];
    services[serviceIndex].state = "Active";
    services[serviceIndex].updatedAt = new Date().toISOString();

    // Audit log
    auditEvents.unshift({
      id: "aud_svc_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "service.activate",
      target: service.id,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_svc_" + Math.random().toString(36).substring(2, 8),
      details: `Activated service workload and restored key/credential operations.`
    });

    res.json(services[serviceIndex]);
  });

  app.delete("/api/services/:id", (req, res) => {
    const service = services.find(s => s.id === req.params.id);
    if (!service) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    // Check if active credentials exist
    const activeKeys = serviceKeys.filter(k => k.serviceId === service.id && k.state === "Active");
    const activeApiKeys = apiKeys.filter(k => k.serviceId === service.id && k.state === "Active");

    if (activeKeys.length > 0 || activeApiKeys.length > 0) {
      return res.status(400).json({
        error: `Cannot delete service identity with active credentials remaining. Please revoke all active service keys (${activeKeys.length}) and API keys (${activeApiKeys.length}) first.`,
        activeKeysCount: activeKeys.length,
        activeApiKeysCount: activeApiKeys.length
      });
    }

    // Filter out all associated credentials (even inactive/revoked ones)
    serviceKeys = serviceKeys.filter(k => k.serviceId !== service.id);
    apiKeys = apiKeys.filter(k => k.serviceId !== service.id);
    services = services.filter(s => s.id !== service.id);

    // Audit log
    auditEvents.unshift({
      id: "aud_svc_" + Date.now(),
      serviceId: null,
      actor: "operator@tigrbl.com",
      action: "service.delete",
      target: service.id,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_svc_" + Math.random().toString(36).substring(2, 8),
      details: `Deleted service identity '${service.name}' and purged historic metadata.`
    });

    res.json({ message: "Service successfully deleted and associated metadata purged." });
  });

  // -----------------------------------------------------------------
  // CREDENTIAL SERVICE KEYS ENDPOINTS
  // -----------------------------------------------------------------
  app.get("/api/services/:id/keys", (req, res) => {
    const keys = serviceKeys.filter(k => k.serviceId === req.params.id);
    res.json(keys);
  });

  app.post("/api/services/:id/keys", (req, res) => {
    const service = services.find(s => s.id === req.params.id);
    if (!service) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const { algorithm, expiryDays } = req.body;
    if (!algorithm || !["RS256", "ES256", "EdDSA"].includes(algorithm)) {
      return res.status(400).json({ error: "Invalid cryptographic algorithm choice." });
    }

    const days = expiryDays ? parseInt(expiryDays) : 180;
    const expiresAt = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString();
    const keyId = `key_${Math.random().toString(36).substring(2, 10)}`;
    
    // Generate private key mock
    const secretMaterial = `-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDgW\n[REVEALED_ONCE_DO_NOT_PERSIST_OR_RE_DISPLAY]\n${Buffer.from(keyId).toString("base64")}\n-----END PRIVATE KEY-----`;

    const newKey: CredentialServiceKey = {
      id: keyId,
      serviceId: service.id,
      algorithm,
      state: "Active",
      createdAt: new Date().toISOString(),
      activatedAt: new Date().toISOString(),
      expiresAt,
      lastUsedAt: null,
      publicFingerprint: `sha256:${Array.from({ length: 8 }, () => Math.random().toString(16).substring(2, 4)).join(":")}`,
      rotationRelationship: "Initial key",
      secretMaterial // Returned ONCE
    };

    // Store in global database WITHOUT secret material for security compliance
    const keyToStore = { ...newKey };
    delete keyToStore.secretMaterial;
    serviceKeys.push(keyToStore);

    // Audit log
    auditEvents.unshift({
      id: "aud_key_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "key.create",
      target: keyId,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_key_" + Math.random().toString(36).substring(2, 8),
      details: `Generated new ${algorithm} service key. Security material revealed once.`
    });

    // Return the full object with the secret material
    res.status(201).json(newKey);
  });

  app.post("/api/services/:id/keys/:keyId/rotate", (req, res) => {
    const service = services.find(s => s.id === req.params.id);
    if (!service) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const originalKeyIndex = serviceKeys.findIndex(k => k.id === req.params.keyId && k.serviceId === service.id);
    if (originalKeyIndex === -1) {
      return res.status(404).json({ error: "Source key to rotate not found" });
    }

    const originalKey = serviceKeys[originalKeyIndex];

    // Create new rotated key
    const nextKeyId = `key_${Math.random().toString(36).substring(2, 10)}`;
    const expiresAt = new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString();
    const secretMaterial = `-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDgW_ROTATED\n[REVEALED_ONCE_DO_NOT_PERSIST]\n${Buffer.from(nextKeyId).toString("base64")}\n-----END PRIVATE KEY-----`;

    const newKey: CredentialServiceKey = {
      id: nextKeyId,
      serviceId: service.id,
      algorithm: originalKey.algorithm,
      state: "Active",
      createdAt: new Date().toISOString(),
      activatedAt: new Date().toISOString(),
      expiresAt,
      lastUsedAt: null,
      publicFingerprint: `sha256:${Array.from({ length: 8 }, () => Math.random().toString(16).substring(2, 4)).join(":")}`,
      rotationRelationship: `Rotated from ${originalKey.id}`,
      secretMaterial
    };

    // Store new key
    const keyToStore = { ...newKey };
    delete keyToStore.secretMaterial;
    serviceKeys.push(keyToStore);

    // Update old key relationship & state
    serviceKeys[originalKeyIndex].state = "Retired";
    serviceKeys[originalKeyIndex].rotationRelationship = `Rotated to ${nextKeyId}`;

    // Track Rotation Event
    const rotId = `rot_${Math.random().toString(36).substring(2, 8)}`;
    const corrId = `tx_rot_${Math.random().toString(36).substring(2, 8)}`;
    
    rotationEvents.unshift({
      id: rotId,
      serviceId: service.id,
      oldKeyId: originalKey.id,
      newKeyId: nextKeyId,
      actor: "operator@tigrbl.com",
      reason: "Operator initiated zero-downtime rotation",
      status: "Completed",
      timestamp: new Date().toISOString(),
      failureReason: null,
      retryCount: 0,
      correlationId: corrId
    });

    // Audit Log
    auditEvents.unshift({
      id: "aud_rot_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "key.rotate",
      target: nextKeyId,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: corrId,
      details: `Rotated key ${originalKey.id} -> ${nextKeyId}. Retiring old key.`
    });

    res.status(200).json(newKey);
  });

  app.post("/api/services/:id/keys/:keyId/revoke", (req, res) => {
    const service = services.find(s => s.id === req.params.id);
    if (!service) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const keyIndex = serviceKeys.findIndex(k => k.id === req.params.keyId && k.serviceId === service.id);
    if (keyIndex === -1) {
      return res.status(404).json({ error: "Service key not found" });
    }

    const key = serviceKeys[keyIndex];
    serviceKeys[keyIndex].state = "Revoked";

    // Audit log
    auditEvents.unshift({
      id: "aud_key_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "key.revoke",
      target: key.id,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_key_" + Math.random().toString(36).substring(2, 8),
      details: `Revoked service key ${key.id}. This key can no longer validate tokens.`
    });

    res.json(serviceKeys[keyIndex]);
  });

  // -----------------------------------------------------------------
  // CREDENTIAL API KEYS ENDPOINTS
  // -----------------------------------------------------------------
  app.get("/api/services/:id/apikeys", (req, res) => {
    const keys = apiKeys.filter(k => k.serviceId === req.params.id);
    res.json(keys);
  });

  app.post("/api/services/:id/apikeys", (req, res) => {
    const service = services.find(s => s.id === req.params.id);
    if (!service) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const { purpose, scopes, expiryDays, networkConstraints } = req.body;
    if (!purpose || !scopes || !Array.isArray(scopes) || scopes.length === 0) {
      return res.status(400).json({ error: "Invalid purpose or missing structured permissions/scopes" });
    }

    const days = expiryDays ? parseInt(expiryDays) : 365;
    const expiresAt = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString();
    const keyId = `apikey_${Math.random().toString(36).substring(2, 10)}`;
    
    const keyMaterial = `tg_live_${Math.random().toString(36).substring(2, 10)}${Math.random().toString(36).substring(2, 10)}`;
    const keyPrefix = keyMaterial.substring(0, 12);

    const newApiKey: CredentialApiKey = {
      id: keyId,
      serviceId: service.id,
      owner: service.owner || "platform-operations",
      purpose,
      scopes,
      environment: service.environment,
      state: "Active",
      expiresAt,
      createdAt: new Date().toISOString(),
      lastUsedAt: null,
      keyPrefix,
      networkConstraints,
      secretMaterial: keyMaterial // Returned ONCE
    };

    const storeApiKey = { ...newApiKey };
    delete storeApiKey.secretMaterial;
    apiKeys.push(storeApiKey);

    // Audit log
    auditEvents.unshift({
      id: "aud_api_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "apikey.create",
      target: keyId,
      permissionDelta: `+ ${scopes.join(", ")}`,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_api_" + Math.random().toString(36).substring(2, 8),
      details: `Created scoped API key ${keyPrefix}... Permissions: [${scopes.join(", ")}]`
    });

    res.status(201).json(newApiKey);
  });

  app.post("/api/services/:id/apikeys/:keyId/revoke", (req, res) => {
    const service = services.find(s => s.id === req.params.id);
    if (!service) {
      return res.status(404).json({ error: "Service identity not found" });
    }

    const apiKeyIndex = apiKeys.findIndex(k => k.id === req.params.keyId && k.serviceId === service.id);
    if (apiKeyIndex === -1) {
      return res.status(404).json({ error: "API key not found" });
    }

    const apiKey = apiKeys[apiKeyIndex];
    apiKeys[apiKeyIndex].state = "Revoked";

    // Audit log
    auditEvents.unshift({
      id: "aud_api_" + Date.now(),
      serviceId: service.id,
      actor: "operator@tigrbl.com",
      action: "apikey.revoke",
      target: apiKey.id,
      permissionDelta: null,
      outcome: "Success",
      timestamp: new Date().toISOString(),
      correlationId: "tx_api_" + Math.random().toString(36).substring(2, 8),
      details: `Revoked API key ${apiKey.keyPrefix}... Integration failure is expected.`
    });

    res.json(apiKeys[apiKeyIndex]);
  });

  // -----------------------------------------------------------------
  // TOKEN RECORDS AND VALIDATION TOOLS
  // -----------------------------------------------------------------
  app.get("/api/tokens", (req, res) => {
    res.json(tokenRecords);
  });

  // Dedicated validation endpoint with trace tree
  app.post("/api/tokens/validate", (req, res) => {
    const { token, clientIp } = req.body;
    
    if (!token || token.trim() === "") {
      return res.status(400).json({ error: "Token or credential input is empty" });
    }

    const traceId = `trace_${Math.random().toString(36).substring(2, 8)}`;
    const correlationId = `tx_val_${Math.random().toString(36).substring(2, 8)}`;

    const isApiKey = token.startsWith("tg_live_");
    
    // Evaluation state
    const traceSteps: { step: string; status: "Passed" | "Failed" | "Skipped"; detail: string }[] = [];
    let outcome: "Allowed" | "Denied" = "Denied";
    let matchedService: ServiceIdentity | null = null;
    let finalReason = "Unknown token format";
    let scopes: string[] = [];
    let subject = "Unresolved Principal";

    if (isApiKey) {
      traceSteps.push({
        step: "Token Type Detection",
        status: "Passed",
        detail: "Detected TigrBl static API Key material."
      });

      const matchedKey = apiKeys.find(k => token.startsWith(k.keyPrefix));
      if (!matchedKey) {
        traceSteps.push({
          step: "Material Match",
          status: "Failed",
          detail: "Credential fingerprint not found in service registry."
        });
        finalReason = "API Key not found or invalid fingerprint.";
      } else {
        traceSteps.push({
          step: "Material Match",
          status: "Passed",
          detail: `Matched Key ID ${matchedKey.id} (prefix ${matchedKey.keyPrefix}).`
        });

        matchedService = services.find(s => s.id === matchedKey.serviceId) || null;
        if (!matchedService) {
          traceSteps.push({
            step: "Owner Service Active Check",
            status: "Failed",
            detail: "Workload owner identity record was deleted."
          });
          finalReason = "Orphaned key without active workload.";
        } else if (matchedService.state === "Suspended") {
          traceSteps.push({
            step: "Owner Service Active Check",
            status: "Failed",
            detail: `Workload identity '${matchedService.name}' is SUSPENDED.`
          });
          finalReason = "Associated service principal identity is Suspended.";
        } else {
          traceSteps.push({
            step: "Owner Service Active Check",
            status: "Passed",
            detail: `Workload identity '${matchedService.name}' is Active.`
          });

          // Check expiry
          const isExpired = new Date(matchedKey.expiresAt) < new Date();
          if (isExpired) {
            traceSteps.push({
              step: "Temporal Constraint Check",
              status: "Failed",
              detail: `API Key expired on ${new Date(matchedKey.expiresAt).toLocaleString()}`
            });
            finalReason = "Credential expired.";
          } else {
            traceSteps.push({
              step: "Temporal Constraint Check",
              status: "Passed",
              detail: `Key expires on ${new Date(matchedKey.expiresAt).toLocaleString()}`
            });

            // Network Constraint Check
            let networkPassed = true;
            if (matchedKey.networkConstraints) {
              const allowedIps = matchedKey.networkConstraints.split(",").map(i => i.trim());
              if (clientIp && !allowedIps.some(ip => clientIp.includes(ip) || ip === "0.0.0.0/0")) {
                networkPassed = false;
                traceSteps.push({
                  step: "Sender Constraint Check",
                  status: "Failed",
                  detail: `Client IP ${clientIp} does not match allowed CIDRs: [${matchedKey.networkConstraints}]`
                });
                finalReason = "Sender constraint mismatch.";
              } else {
                traceSteps.push({
                  step: "Sender Constraint Check",
                  status: "Passed",
                  detail: `Client IP ${clientIp || "127.0.0.1"} matches authorized subnet constraints.`
                });
              }
            } else {
              traceSteps.push({
                step: "Sender Constraint Check",
                status: "Skipped",
                detail: "No network restrictions configured on API Key."
              });
            }

            if (networkPassed) {
              outcome = "Allowed";
              scopes = matchedKey.scopes;
              subject = matchedService.subject;
              finalReason = "Static API Key authorization authorized successfully.";
              
              // Update last used
              matchedKey.lastUsedAt = new Date().toISOString();
              matchedService.lastActive = new Date().toISOString();
            }
          }
        }
      }
    } else {
      // Decode JWT mock
      traceSteps.push({
        step: "Token Type Detection",
        status: "Passed",
        detail: "Detected JSON Web Token (JWT) OAuth credential."
      });

      // Simple parse simulation of custom string "jwt_<valid|expired|revoked|bad_sig|wrong_aud>_..."
      const lower = token.toLowerCase();
      if (lower.includes("jwt_valid")) {
        matchedService = services.find(s => s.id === "svc-pay-prod") || services[0];
        traceSteps.push({
          step: "Cryptographic Signature Validation",
          status: "Passed",
          detail: "Signature verified against JWKS keys successfully."
        }, {
          step: "Claim Context Resolution",
          status: "Passed",
          detail: `Issuer matches metadata. Subject: ${matchedService?.subject}`
        }, {
          step: "Temporal Validity Verification",
          status: "Passed",
          detail: "Token time check complete (iat < now < exp)."
        }, {
          step: "Audience Boundary Check",
          status: "Passed",
          detail: "Audience boundaries verified successfully."
        });

        outcome = "Allowed";
        scopes = ["charge:create", "charge:read"];
        subject = matchedService?.subject || "spn:realm-us:tenant-alpha:svc:payment-gateway";
        finalReason = "Token validated successfully via tenant JWKS.";
        
        if (matchedService) {
          matchedService.lastActive = new Date().toISOString();
        }
      } else if (lower.includes("jwt_expired")) {
        traceSteps.push({
          step: "Cryptographic Signature Validation",
          status: "Passed",
          detail: "Signature verified successfully."
        }, {
          step: "Temporal Validity Verification",
          status: "Failed",
          detail: "Token expiration time (exp) occurred in the past."
        });
        finalReason = "Evaluation failed: Temporal validity verification failed (expired).";
      } else if (lower.includes("jwt_revoked")) {
        traceSteps.push({
          step: "Cryptographic Signature Validation",
          status: "Passed",
          detail: "Signature verified successfully."
        }, {
          step: "Introspection Resolve",
          status: "Failed",
          detail: "Provider revocation listing matched this token signature ID."
        });
        finalReason = "Evaluation failed: Credential previously revoked.";
      } else if (lower.includes("jwt_bad_sig")) {
        traceSteps.push({
          step: "Cryptographic Signature Validation",
          status: "Failed",
          detail: "No signature certificate in JWKS matched payload header hash."
        });
        finalReason = "Evaluation failed: Invalid signature.";
      } else if (lower.includes("jwt_wrong_aud")) {
        traceSteps.push({
          step: "Cryptographic Signature Validation",
          status: "Passed",
          detail: "Signature verified successfully."
        }, {
          step: "Audience Boundary Check",
          status: "Failed",
          detail: "Token audience claims mismatched available resource server scopes."
        });
        finalReason = "Evaluation failed: Audience mismatch.";
      } else {
        // Fallback guess parsing
        traceSteps.push({
          step: "Cryptographic Signature Validation",
          status: "Failed",
          detail: "Custom token payload hash could not be parsed."
        });
        finalReason = "Evaluation failed: Unknown token structure or corrupt cryptographic material.";
      }
    }

    // Capture Token Record
    const newRecord: TokenRecord = {
      id: "tok_" + Math.random().toString(36).substring(2, 10),
      serviceId: matchedService ? matchedService.id : null,
      subject,
      issuer: "https://auth.tigrbl.net/oauth/v2/tenant-alpha",
      audience: "https://api.tigrbl.net/resources",
      scopes,
      issuedAt: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
      expiresAt: new Date(Date.now() + 55 * 60 * 1000).toISOString(),
      state: outcome === "Allowed" ? "Active" : "Revoked",
      validationOutcome: outcome,
      validationReason: finalReason
    };
    tokenRecords.unshift(newRecord);

    // Audit Event
    auditEvents.unshift({
      id: "aud_val_" + Date.now(),
      serviceId: matchedService ? matchedService.id : null,
      actor: "resource-enforcer-gateway",
      action: "token.validate",
      target: isApiKey ? "apikey" : "oauth_token",
      permissionDelta: null,
      outcome: outcome === "Allowed" ? "Success" : "Failure",
      timestamp: new Date().toISOString(),
      correlationId,
      details: `Workload Introspection: ${outcome}. Reason: ${finalReason}`
    });

    res.json({
      traceId,
      correlationId,
      outcome,
      reasonCode: outcome === "Allowed" ? "SUCCESS_AUTHORIZED" : "FAILED_CONSTRAINT_VIOLATION",
      reasonDetails: finalReason,
      subject,
      resolvedService: matchedService,
      scopes,
      traceSteps
    });
  });

  // -----------------------------------------------------------------
  // AUDIT EVENTS ENDPOINTS
  // -----------------------------------------------------------------
  app.get("/api/audit", (req, res) => {
    const { serviceId, action } = req.query;
    let filtered = [...auditEvents];
    if (serviceId) {
      filtered = filtered.filter(e => e.serviceId === serviceId);
    }
    if (action) {
      filtered = filtered.filter(e => e.action === action);
    }
    res.json(filtered);
  });

  // -----------------------------------------------------------------
  // ROTATION EVENTS ENDPOINTS
  // -----------------------------------------------------------------
  app.get("/api/rotation", (req, res) => {
    res.json(rotationEvents);
  });

  // Vite development integration
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
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer().catch(err => {
  console.error("Failed to start server", err);
});
