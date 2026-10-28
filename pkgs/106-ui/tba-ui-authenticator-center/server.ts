import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import {
  Authenticator,
  Ceremony,
  TenantPolicy,
  AuditLog,
  AuthenticatorKind,
  AuthenticatorState,
  IdentityProfile,
  AuthenticationContext,
  AuthenticatorProperties
} from "./src/types";

const app = express();
app.use(express.json());
const PORT = 3000;

// ==========================================
// IN-MEMORY DATABASE & SEED DATA
// ==========================================

const IDENTITIES: IdentityProfile[] = [
  {
    id: "user-alice",
    email: "alice.smith@example.com",
    name: "Alice Smith",
    avatarUrl: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=120",
    role: "user"
  },
  {
    id: "user-bob",
    email: "bob.miller@example.com",
    name: "Bob Miller",
    avatarUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=120",
    role: "user"
  },
  {
    id: "user-charlie",
    email: "charlie.davis@example.com",
    name: "Charlie Davis",
    avatarUrl: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=120",
    role: "user"
  },
  {
    id: "user-admin",
    email: "admin.security@example.com",
    name: "Admin Operator",
    avatarUrl: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=120",
    role: "admin"
  }
];

// Helper to get properties for authenticator types
function getPropertiesForKind(kind: AuthenticatorKind, overrides?: Partial<AuthenticatorProperties>): AuthenticatorProperties {
  const base: AuthenticatorProperties = {
    userPresent: false,
    userVerified: false,
    phishingResistant: false,
    verifierNameBound: false,
    replayResistant: false,
    senderConstrained: false,
    hardwareBacked: false,
    synced: false,
    discoverable: false,
    attested: false
  };

  switch (kind) {
    case "password":
      base.userVerified = true;
      break;
    case "totp":
    case "hotp":
      base.userPresent = true;
      base.userVerified = false;
      base.replayResistant = true;
      break;
    case "recovery_code":
      base.userVerified = true;
      break;
    case "webauthn":
      base.userPresent = true;
      base.userVerified = true;
      base.phishingResistant = true;
      base.verifierNameBound = true;
      base.replayResistant = true;
      base.hardwareBacked = true;
      base.discoverable = true;
      base.attested = true;
      break;
    case "federated_oidc":
      base.userPresent = true;
      base.userVerified = true;
      base.verifierNameBound = true;
      base.synced = true;
      break;
    case "mtls":
      base.userPresent = true;
      base.phishingResistant = true;
      base.senderConstrained = true;
      base.hardwareBacked = true;
      break;
    case "dpop":
      base.phishingResistant = true;
      base.replayResistant = true;
      base.senderConstrained = true;
      break;
  }

  return { ...base, ...overrides };
}

// Initial Authenticators
let authenticators: Authenticator[] = [
  // Alice Smith (Highly secure, multi-factor, compliant)
  {
    id: "auth-alice-pwd",
    principalId: "user-alice",
    tenantId: "tenant-acme",
    kind: "password",
    displayName: "Corporate LDAP Password",
    state: "active",
    enrolledAt: "2026-01-10T10:00:00Z",
    lastVerifiedAt: "2026-07-10T09:00:00Z",
    lastUsedAt: "2026-07-11T21:00:00Z",
    expiresAt: "2026-10-10T10:00:00Z",
    suspendedAt: null,
    revokedAt: null,
    amr: ["pwd"],
    properties: getPropertiesForKind("password"),
    attestationSummary: "Corporate IDP Password Provider",
    recoveryEligibility: false,
    version: 1
  },
  {
    id: "auth-alice-totp",
    principalId: "user-alice",
    tenantId: "tenant-acme",
    kind: "totp",
    displayName: "Work Authenticator (Google Auth)",
    state: "active",
    enrolledAt: "2026-01-10T10:15:00Z",
    lastVerifiedAt: "2026-07-10T09:01:00Z",
    lastUsedAt: "2026-07-11T21:00:30Z",
    expiresAt: null,
    suspendedAt: null,
    revokedAt: null,
    amr: ["otp"],
    properties: getPropertiesForKind("totp"),
    attestationSummary: "Standard Software TOTP (SHA-1, 6 digits)",
    recoveryEligibility: true,
    version: 1,
    details: { otpDigits: 6, otpPeriod: 30 }
  },
  {
    id: "auth-alice-passkey",
    principalId: "user-alice",
    tenantId: "tenant-acme",
    kind: "webauthn",
    displayName: "Yubikey 5C Nano (Hardware Key)",
    state: "active",
    enrolledAt: "2026-03-15T14:30:00Z",
    lastVerifiedAt: "2026-07-11T12:00:00Z",
    lastUsedAt: "2026-07-11T12:00:00Z",
    expiresAt: null,
    suspendedAt: null,
    revokedAt: null,
    amr: ["hw", "user_presence", "user_verification", "passkey"],
    properties: getPropertiesForKind("webauthn", { hardwareBacked: true, synced: false }),
    attestationSummary: "Yubico YubiKey 5 Series (AAGUID: 12345678-abcd-ef01-2345-6789abcdef01)",
    recoveryEligibility: true,
    version: 1,
    details: {
      credentialId: "key-yubikey-alice-001",
      rpId: "ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
      origin: "https://ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
      aaguid: "12345678-abcd-ef01-2345-6789abcdef01",
      counter: 124,
      algorithm: "ES256",
      backupState: "not_backed_up"
    }
  },
  {
    id: "auth-alice-recovery",
    principalId: "user-alice",
    tenantId: "tenant-acme",
    kind: "recovery_code",
    displayName: "Emergency Recovery Codes",
    state: "active",
    enrolledAt: "2026-01-10T10:16:00Z",
    lastVerifiedAt: null,
    lastUsedAt: null,
    expiresAt: null,
    suspendedAt: null,
    revokedAt: null,
    amr: ["recovery_code"],
    properties: getPropertiesForKind("recovery_code"),
    attestationSummary: "Server-side cryptographically signed recovery blocks",
    recoveryEligibility: true,
    version: 1,
    details: { remainingCount: 8, totalCount: 10 }
  },
  {
    id: "auth-alice-oidc",
    principalId: "user-alice",
    tenantId: "tenant-acme",
    kind: "federated_oidc",
    displayName: "Alice Personal Google Account",
    state: "active",
    enrolledAt: "2026-02-20T08:00:00Z",
    lastVerifiedAt: "2026-07-01T10:00:00Z",
    lastUsedAt: "2026-07-01T10:00:00Z",
    expiresAt: null,
    suspendedAt: null,
    revokedAt: null,
    amr: ["federated"],
    properties: getPropertiesForKind("federated_oidc"),
    attestationSummary: "Google OIDC Provider link",
    recoveryEligibility: false,
    version: 1,
    details: { provider: "Google", pairwiseId: "g-alice-12345" }
  },

  // Bob Miller (Suspended / compromised device case)
  {
    id: "auth-bob-pwd",
    principalId: "user-bob",
    tenantId: "tenant-acme",
    kind: "password",
    displayName: "Bob Corporate LDAP Password",
    state: "active",
    enrolledAt: "2026-01-12T11:00:00Z",
    lastVerifiedAt: "2026-07-09T08:00:00Z",
    lastUsedAt: "2026-07-11T15:00:00Z",
    expiresAt: "2026-10-12T11:00:00Z",
    suspendedAt: null,
    revokedAt: null,
    amr: ["pwd"],
    properties: getPropertiesForKind("password"),
    attestationSummary: "Corporate IDP Password Provider",
    recoveryEligibility: false,
    version: 1
  },
  {
    id: "auth-bob-passkey-stolen",
    principalId: "user-bob",
    tenantId: "tenant-acme",
    kind: "webauthn",
    displayName: "Stolen Work Macbook TouchID",
    state: "suspended",
    enrolledAt: "2026-01-12T11:20:00Z",
    lastVerifiedAt: "2026-07-01T12:00:00Z",
    lastUsedAt: "2026-07-01T12:00:00Z",
    expiresAt: null,
    suspendedAt: "2026-07-11T16:00:00Z",
    revokedAt: null,
    amr: ["hw", "user_presence", "user_verification", "passkey"],
    properties: getPropertiesForKind("webauthn", { hardwareBacked: true, synced: false }),
    attestationSummary: "Apple TouchID Secure Enclave (AAGUID: apple-touch-id-mock-aaguid)",
    recoveryEligibility: false,
    version: 1,
    details: {
      credentialId: "key-touchid-bob-999",
      rpId: "ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
      origin: "https://ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
      aaguid: "apple-touch-id-mock-aaguid",
      counter: 45,
      algorithm: "ES256",
      backupState: "not_backed_up"
    }
  },
  {
    id: "auth-bob-recovery",
    principalId: "user-bob",
    tenantId: "tenant-acme",
    kind: "recovery_code",
    displayName: "Emergency Recovery Codes",
    state: "active",
    enrolledAt: "2026-01-12T11:21:00Z",
    lastVerifiedAt: null,
    lastUsedAt: "2026-07-11T15:05:00Z",
    expiresAt: null,
    suspendedAt: null,
    revokedAt: null,
    amr: ["recovery_code"],
    properties: getPropertiesForKind("recovery_code"),
    attestationSummary: "Server-side cryptographically signed recovery blocks",
    recoveryEligibility: true,
    version: 1,
    details: { remainingCount: 2, totalCount: 10 }
  },

  // Charlie Davis (Insecure, password only, gap warnings)
  {
    id: "auth-charlie-pwd",
    principalId: "user-charlie",
    tenantId: "tenant-acme",
    kind: "password",
    displayName: "Charlie Weak Password",
    state: "active",
    enrolledAt: "2026-05-01T09:00:00Z",
    lastVerifiedAt: "2026-07-10T11:00:00Z",
    lastUsedAt: "2026-07-11T18:00:00Z",
    expiresAt: "2026-08-01T09:00:00Z",
    suspendedAt: null,
    revokedAt: null,
    amr: ["pwd"],
    properties: getPropertiesForKind("password"),
    attestationSummary: "Corporate IDP Password Provider",
    recoveryEligibility: false,
    version: 1
  }
];

// Active Tenant Policies with versioning support
let activePolicy: TenantPolicy = {
  tenantId: "tenant-acme",
  allowedKinds: ["password", "totp", "webauthn", "recovery_code", "federated_oidc", "mtls", "dpop"],
  requiredKinds: ["password", "totp"], // Shows a gap if TOTP or WebAuthn isn't active
  prohibitedKinds: ["hotp"],
  stepUpEligibleKinds: ["webauthn", "mtls"],
  gracePeriodDays: 14,
  attestationPolicy: "indirect",
  allowedAlgorithms: ["ES256", "RS256", "EdDSA"],
  updatedBy: "user-admin",
  updatedAt: "2026-06-01T12:00:00Z",
  version: 3
};

let policyHistory: TenantPolicy[] = [
  {
    tenantId: "tenant-acme",
    allowedKinds: ["password", "totp", "recovery_code"],
    requiredKinds: ["password"],
    prohibitedKinds: ["federated_oidc"],
    stepUpEligibleKinds: ["totp"],
    gracePeriodDays: 30,
    attestationPolicy: "none",
    allowedAlgorithms: ["RS256"],
    updatedBy: "user-admin",
    updatedAt: "2026-01-01T09:00:00Z",
    version: 1
  },
  {
    tenantId: "tenant-acme",
    allowedKinds: ["password", "totp", "recovery_code", "webauthn"],
    requiredKinds: ["password"],
    prohibitedKinds: [],
    stepUpEligibleKinds: ["totp", "webauthn"],
    gracePeriodDays: 30,
    attestationPolicy: "none",
    allowedAlgorithms: ["RS256", "ES256"],
    updatedBy: "user-admin",
    updatedAt: "2026-03-01T10:00:00Z",
    version: 2
  }
];

// Seed Audit Logs
let auditLogs: AuditLog[] = [
  {
    id: "audit-1",
    timestamp: "2026-07-11T16:00:00Z",
    subjectId: "user-bob",
    tenantId: "tenant-acme",
    action: "suspend",
    authenticatorId: "auth-bob-passkey-stolen",
    operatorId: "user-admin",
    status: "success",
    reasonCode: "DEVICE_COMPROMISED",
    correlationId: "corr-bob-suspend-991",
    details: "Help-desk administrator suspended Bob Miller's Work Macbook TouchID passkey. Reason: Reported lost or stolen."
  },
  {
    id: "audit-2",
    timestamp: "2026-07-11T15:05:00Z",
    subjectId: "user-bob",
    tenantId: "tenant-acme",
    action: "verify_finish",
    authenticatorId: "auth-bob-recovery",
    operatorId: "user-bob",
    status: "success",
    correlationId: "corr-bob-rec-022",
    details: "Bob Miller successfully verified with Emergency Recovery Code. Remaining codes count: 2."
  },
  {
    id: "audit-3",
    timestamp: "2026-07-10T12:00:00Z",
    subjectId: "user-alice",
    tenantId: "tenant-acme",
    action: "verify_finish",
    authenticatorId: "auth-alice-passkey",
    operatorId: "user-alice",
    status: "success",
    correlationId: "corr-alice-webauthn-774",
    details: "Alice Smith authenticated successfully with WebAuthn Passkey (Yubikey 5C Nano). Properties: Phishing Resistant, Hardware Backed."
  }
];

let ceremonies: Ceremony[] = [];

// Helper to log audit events
function logAudit(
  subjectId: string,
  action: string,
  status: 'success' | 'failure',
  details: string,
  operatorId: string,
  authenticatorId?: string,
  reasonCode?: string
) {
  const newLog: AuditLog = {
    id: "audit-" + Date.now() + "-" + Math.random().toString(36).substring(2, 6),
    timestamp: new Date().toISOString(),
    subjectId,
    tenantId: "tenant-acme",
    action,
    authenticatorId,
    operatorId,
    status,
    reasonCode,
    correlationId: "corr-" + Math.random().toString(36).substring(2, 8),
    details
  };
  auditLogs.unshift(newLog);
  return newLog;
}

// Active current subject context evaluator
function getAuthenticationContextForSubject(subjectId: string): AuthenticationContext {
  const activeAuths = authenticators.filter(a => a.principalId === subjectId && a.state === "active");
  const achievedAmr: string[] = [];
  const achievedProperties: Partial<AuthenticatorProperties> = {};
  const contributing: AuthenticationContext['contributingAuthenticators'] = [];

  activeAuths.forEach(a => {
    achievedAmr.push(...a.amr);
    contributing.push({
      id: a.id,
      kind: a.kind,
      displayName: a.displayName,
      properties: a.properties
    });

    // Merge properties
    Object.keys(a.properties).forEach((k) => {
      const propKey = k as keyof AuthenticatorProperties;
      if (a.properties[propKey]) {
        achievedProperties[propKey] = true;
      }
    });
  });

  // Calculate Achieved AAL (Authenticator Assurance Level)
  // AAL1: password or federated_oidc
  // AAL2: Multi-factor (e.g. password + TOTP or WebAuthn/passkey)
  // AAL3: Hardware-backed, phishing-resistant, cryptographically bound MFA
  let achievedAal: AuthenticationContext['achievedAal'] = "NONE";
  const hasPassword = activeAuths.some(a => a.kind === "password");
  const hasMfa = activeAuths.some(a => a.kind === "totp" || a.kind === "webauthn" || a.kind === "recovery_code");
  const hasPhishingResistant = activeAuths.some(a => a.properties.phishingResistant && a.state === "active");
  const hasHardware = activeAuths.some(a => a.properties.hardwareBacked && a.state === "active");

  if (activeAuths.length > 0) {
    achievedAal = "AAL1";
    if (hasPassword && hasMfa) {
      achievedAal = "AAL2";
    }
    if (hasMfa && hasPhishingResistant && hasHardware) {
      achievedAal = "AAL3";
    }
  }

  // Set default required AAL based on tenant policy
  let requiredAal: AuthenticationContext['requiredAal'] = "AAL2";

  return {
    requiredAal,
    achievedAal,
    requiredAcr: ["urn:mace:incommon:iap:silver", "nih-backup-level-2"],
    achievedAmr: Array.from(new Set(achievedAmr)),
    achievedProperties,
    sessionExpiresAt: new Date(Date.now() + 86400000).toISOString(),
    evaluatedAt: new Date().toISOString(),
    contributingAuthenticators: contributing
  };
}


// ==========================================
// REST API ROUTES
// ==========================================

// Identities endpoint (to let user switch personas in the dashboard)
app.get("/api/identities", (req, res) => {
  res.json(IDENTITIES);
});

// Current-subject authenticators overview
app.get("/api/account/authenticators", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const userAuths = authenticators.filter(a => a.principalId === principalId);
  res.json(userAuths);
});

// Provider Catalog endpoint
app.get("/api/account/authenticators/catalog", (req, res) => {
  // Returns descriptive metadata for enrollment eligibility
  res.json([
    {
      kind: "password",
      title: "Corporate Password",
      description: "Secure, high-entropy character sequence checked against active compromise databases.",
      properties: getPropertiesForKind("password"),
      compatibility: "All modern platforms and clients."
    },
    {
      kind: "totp",
      title: "TOTP Software Token",
      description: "Generates secure 6-digit verification codes using RFC 6238 time-based tokens.",
      properties: getPropertiesForKind("totp"),
      compatibility: "Works with Google Authenticator, Microsoft Authenticator, 1Password, etc."
    },
    {
      kind: "webauthn",
      title: "FIDO2 Passkey / Security Key",
      description: "Strongest cryptographic factor using hardware keys or biometric platform authenticators.",
      properties: getPropertiesForKind("webauthn"),
      compatibility: "phishing-resistant. Supported in Chrome, Safari, Edge, Firefox, iOS, macOS, Windows, Android."
    },
    {
      kind: "federated_oidc",
      title: "Federated OIDC Login",
      description: "Secure cross-domain identity binding matching enterprise and public OIDC registries.",
      properties: getPropertiesForKind("federated_oidc"),
      compatibility: "Google, Microsoft Azure AD, Okta accounts."
    },
    {
      kind: "mtls",
      title: "mTLS Client Certificate",
      description: "Device-bound X.509 client certificate for corporate-managed endpoints.",
      properties: getPropertiesForKind("mtls"),
      compatibility: "Requires enterprise device enrollment and MDM certificate deployment."
    },
    {
      kind: "dpop",
      title: "DPoP Proof-of-Possession",
      description: "Sender-constrained cryptographic binding to OAuth bearer tokens.",
      properties: getPropertiesForKind("dpop"),
      compatibility: "Developer/client-focused application binding."
    }
  ]);
});

// GET Authentication Context (ACR / AMR evaluation)
app.get("/api/account/authentication-context", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  res.json(getAuthenticationContextForSubject(principalId));
});

// POST Enroll Start
app.post("/api/account/authenticators/:kind/enroll/start", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const { kind } = req.params;

  // Verify kind is allowed in active policy
  if (!activePolicy.allowedKinds.includes(kind as AuthenticatorKind)) {
    return res.status(400).json({
      error: "POLICY_VIOLATION",
      message: `Enrollment of authenticator kind '${kind}' is prohibited by tenant administrator policy.`
    });
  }

  const identity = IDENTITIES.find(id => id.id === principalId);
  const challenge = Math.random().toString(36).substring(2, 10).toUpperCase();
  const id = "ceremony-" + Math.random().toString(36).substring(2, 8);

  const ceremony: Ceremony = {
    id,
    kind: kind as AuthenticatorKind,
    operation: "enroll",
    subjectId: principalId,
    tenantId: "tenant-acme",
    challenge,
    expiresAt: new Date(Date.now() + 300000).toISOString(), // 5 min
    origin: "https://ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
    rpId: "ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
    userVerification: "preferred",
    requiredPresence: true
  };

  // Add QR secret if TOTP
  if (kind === "totp") {
    ceremony.otpSecret = "JBSWY3DPEHPK3PXP"; // Base32 test secret
  }

  // Pre-generate recovery codes if enrolling recovery code
  if (kind === "recovery_code") {
    ceremony.recoveryCodes = Array.from({ length: 10 }, () =>
      Math.floor(10000000 + Math.random() * 90000000).toString().replace(/(\d{4})(\d{4})/, "$1-$2")
    );
  }

  ceremonies.push(ceremony);

  logAudit(
    principalId,
    "enroll_start",
    "success",
    `Initiated enrollment ceremony for kind '${kind}'. Challenge: ${challenge}`,
    principalId
  );

  res.json(ceremony);
});

// POST Enroll Finish
app.post("/api/account/authenticators/:kind/enroll/finish", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const { kind } = req.params;
  const { ceremonyId, response, displayName } = req.body;

  const idx = ceremonies.findIndex(c => c.id === ceremonyId && c.subjectId === principalId);
  if (idx === -1) {
    logAudit(principalId, "enroll_finish", "failure", `Failed enrollment finish: Ceremony not found or expired`, principalId);
    return res.status(404).json({ error: "CEREMONY_NOT_FOUND", message: "Enrollment transaction was not found or expired." });
  }

  const ceremony = ceremonies[idx];
  ceremonies.splice(idx, 1); // Consume the ceremony

  // Simple validation for mock purposes
  if (kind === "totp" && (!response || response.verificationCode !== "123456")) {
    // Let's accept code 123456 for success
    logAudit(principalId, "enroll_finish", "failure", `Failed TOTP enrollment verification code mismatch`, principalId);
    return res.status(400).json({ error: "INVALID_VERIFICATION_CODE", message: "The code entered was incorrect. Try code '123456' for simulation." });
  }

  if (kind === "webauthn" && (!displayName || displayName.trim() === "")) {
    return res.status(400).json({ error: "MISSING_NAME", message: "Please specify a friendly display name for your security key." });
  }

  const newAuthId = "auth-" + Math.random().toString(36).substring(2, 8);

  const customProperties = getPropertiesForKind(kind as AuthenticatorKind, {
    synced: kind === "webauthn" ? (response?.synced || false) : undefined,
    hardwareBacked: kind === "webauthn" ? (response?.hardwareBacked || true) : undefined
  });

  // Calculate AMR codes
  let amr: string[] = [];
  if (kind === "password") amr = ["pwd"];
  else if (kind === "totp") amr = ["otp"];
  else if (kind === "webauthn") amr = ["hw", "user_presence", "user_verification", "passkey"];
  else if (kind === "recovery_code") amr = ["recovery_code"];
  else if (kind === "federated_oidc") amr = ["federated"];
  else amr = [kind];

  let details: any = {};
  if (kind === "totp") {
    details = { otpDigits: 6, otpPeriod: 30 };
  } else if (kind === "webauthn") {
    details = {
      credentialId: "key-" + Math.random().toString(36).substring(2, 10),
      rpId: ceremony.rpId,
      origin: ceremony.origin,
      aaguid: "b8908594-abc3-46bc-92bb-3a6d95328901",
      counter: 1,
      algorithm: "ES256",
      backupState: customProperties.synced ? "backed_up" : "not_backed_up"
    };
  } else if (kind === "recovery_code") {
    details = { remainingCount: 10, totalCount: 10 };
  } else if (kind === "federated_oidc") {
    details = { provider: response?.provider || "Google", pairwiseId: "g-" + Math.random().toString(36).substring(2, 8) };
  } else if (kind === "mtls") {
    details = { fingerprint: "SHA256: 4C:92:4B:C7:E2:EA:79:F3:CC:BA:45:90:3A:D8:1E:EE:AA:51:71:B0" };
  }

  const newAuth: Authenticator = {
    id: newAuthId,
    principalId,
    tenantId: "tenant-acme",
    kind: kind as AuthenticatorKind,
    displayName: displayName || `${kind.toUpperCase()} Authenticator`,
    state: "active",
    enrolledAt: new Date().toISOString(),
    lastVerifiedAt: new Date().toISOString(),
    lastUsedAt: new Date().toISOString(),
    expiresAt: kind === "password" ? new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString() : null,
    suspendedAt: null,
    revokedAt: null,
    amr,
    properties: customProperties,
    attestationSummary: kind === "webauthn" ? "WebAuthn Verified Key Credential Proof" : `${kind.toUpperCase()} Credential provider`,
    recoveryEligibility: ["totp", "webauthn", "recovery_code"].includes(kind),
    version: 1,
    details
  };

  // Check if we are enrolling recovery code, make sure old ones are replaced
  if (kind === "recovery_code") {
    // Revoke any older recovery_code records
    authenticators = authenticators.map(a => {
      if (a.principalId === principalId && a.kind === "recovery_code" && a.id !== newAuthId) {
        return { ...a, state: "revoked", revokedAt: new Date().toISOString() };
      }
      return a;
    });
  }

  // Handle explicit replacement if replaceAuthId is present on the ceremony
  if (ceremony.replaceAuthId) {
    authenticators = authenticators.map(a => {
      if (a.id === ceremony.replaceAuthId && a.principalId === principalId) {
        return { ...a, state: "revoked", revokedAt: new Date().toISOString() };
      }
      return a;
    });
  }

  authenticators.push(newAuth);

  let auditMsg = `Enrolled new ${kind} authenticator: '${newAuth.displayName}'. AMR: ${amr.join(",")}`;
  if (ceremony.replaceAuthId) {
    const oldAuth = authenticators.find(a => a.id === ceremony.replaceAuthId);
    auditMsg = `Replaced authenticator '${oldAuth?.displayName || ceremony.replaceAuthId}' with new ${kind} authenticator: '${newAuth.displayName}'.`;
  }

  logAudit(
    principalId,
    ceremony.replaceAuthId ? "replace_finish" : "enroll_finish",
    "success",
    auditMsg,
    principalId,
    newAuthId
  );

  res.json({ status: "success", authenticator: newAuth });
});

// PATCH Update Display Name
app.patch("/api/account/authenticators/:id", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const { id } = req.params;
  const { displayName } = req.body;

  const auth = authenticators.find(a => a.id === id && a.principalId === principalId);
  if (!auth) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator not found." });
  }

  if (!displayName || displayName.trim() === "") {
    return res.status(400).json({ error: "INVALID_NAME", message: "DisplayName is required." });
  }

  const oldName = auth.displayName;
  auth.displayName = displayName;
  auth.version += 1;

  logAudit(
    principalId,
    "rename",
    "success",
    `Renamed authenticator from '${oldName}' to '${displayName}'`,
    principalId,
    auth.id
  );

  res.json(auth);
});

// POST Verify Start (for step-up ceremonies)
app.post("/api/account/authenticators/:id/verify/start", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const { id } = req.params;

  const auth = authenticators.find(a => a.id === id && a.principalId === principalId);
  if (!auth) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator not found." });
  }

  if (auth.state !== "active") {
    return res.status(400).json({ error: "AUTHENTICATOR_INACTIVE", message: "Cannot verify with a non-active authenticator." });
  }

  const challenge = Math.random().toString(36).substring(2, 10).toUpperCase();
  const cid = "ceremony-" + Math.random().toString(36).substring(2, 8);

  const ceremony: Ceremony = {
    id: cid,
    kind: auth.kind,
    operation: "verify",
    subjectId: principalId,
    tenantId: "tenant-acme",
    challenge,
    expiresAt: new Date(Date.now() + 120000).toISOString(), // 2 mins
    origin: "https://ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
    rpId: "ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
    userVerification: "required",
    requiredPresence: true
  };

  ceremonies.push(ceremony);

  logAudit(
    principalId,
    "verify_start",
    "success",
    `Initiated verification ceremony for authenticator ID ${auth.id} (${auth.displayName})`,
    principalId,
    auth.id
  );

  res.json({ ceremony, authenticator: auth });
});

// POST Verify Finish (for step-up ceremonies)
app.post("/api/account/authenticators/:id/verify/finish", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const { id } = req.params;
  const { ceremonyId, code } = req.body;

  const auth = authenticators.find(a => a.id === id && a.principalId === principalId);
  if (!auth) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator not found." });
  }

  const cidIdx = ceremonies.findIndex(c => c.id === ceremonyId && c.subjectId === principalId);
  if (cidIdx === -1) {
    return res.status(404).json({ error: "CEREMONY_NOT_FOUND", message: "Verification ceremony was not found or has expired." });
  }

  const ceremony = ceremonies[cidIdx];
  ceremonies.splice(cidIdx, 1); // consume it

  // Validate OTP
  if (auth.kind === "totp" && code !== "123456") {
    logAudit(principalId, "verify_finish", "failure", `Failed Verification: OTP code verification mismatch`, principalId, auth.id);
    return res.status(400).json({ error: "INVALID_CODE", message: "Invalid verification code. For simulation, use code '123456'." });
  }

  // Validate Recovery Code
  if (auth.kind === "recovery_code") {
    if (!code || code.trim().length === 0) {
      return res.status(400).json({ error: "INVALID_CODE", message: "Please supply a recovery code." });
    }
    const remCount = auth.details?.remainingCount || 0;
    if (remCount <= 0) {
      logAudit(principalId, "verify_finish", "failure", "Exhausted recovery codes used", principalId, auth.id);
      return res.status(400).json({ error: "CODES_EXHAUSTED", message: "All emergency recovery codes have been used. Please rotate/generate a new set." });
    }
    auth.details = { ...auth.details, remainingCount: remCount - 1 };
  }

  auth.lastVerifiedAt = new Date().toISOString();
  auth.lastUsedAt = new Date().toISOString();

  logAudit(
    principalId,
    "verify_finish",
    "success",
    `Successfully verified identity using authenticator ID ${auth.id} (${auth.displayName})`,
    principalId,
    auth.id
  );

  res.json({ status: "success", authenticator: auth });
});

// POST Replace Start
app.post("/api/account/authenticators/:id/replace/start", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const { id } = req.params;
  const { newKind } = req.body;

  const oldAuth = authenticators.find(a => a.id === id && a.principalId === principalId);
  if (!oldAuth) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator to replace not found." });
  }

  const kindToEnroll = newKind || oldAuth.kind;

  // Verify kind is allowed in active policy
  if (!activePolicy.allowedKinds.includes(kindToEnroll as AuthenticatorKind)) {
    return res.status(400).json({
      error: "POLICY_VIOLATION",
      message: `Enrollment of authenticator kind '${kindToEnroll}' is prohibited by tenant administrator policy.`
    });
  }

  const challenge = Math.random().toString(36).substring(2, 10).toUpperCase();
  const cid = "ceremony-" + Math.random().toString(36).substring(2, 8);

  const ceremony: Ceremony = {
    id: cid,
    kind: kindToEnroll as AuthenticatorKind,
    operation: "replace",
    subjectId: principalId,
    tenantId: "tenant-acme",
    challenge,
    expiresAt: new Date(Date.now() + 300000).toISOString(), // 5 min
    origin: "https://ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
    rpId: "ais-dev-sh5wh4h25fixnhqgs5gkns.run.app",
    userVerification: "preferred",
    requiredPresence: true,
    replaceAuthId: id
  };

  // Add QR secret if TOTP
  if (kindToEnroll === "totp") {
    ceremony.otpSecret = "JBSWY3DPEHPK3PXP"; // Base32 test secret
  }

  // Pre-generate recovery codes if enrolling recovery code
  if (kindToEnroll === "recovery_code") {
    ceremony.recoveryCodes = Array.from({ length: 10 }, () =>
      Math.floor(10000000 + Math.random() * 90000000).toString().replace(/(\d{4})(\d{4})/, "$1-$2")
    );
  }

  ceremonies.push(ceremony);

  logAudit(
    principalId,
    "replace_start",
    "success",
    `Initiated replacement ceremony for authenticator '${oldAuth.displayName}' with new kind '${kindToEnroll}'.`,
    principalId,
    oldAuth.id
  );

  res.json(ceremony);
});

// DELETE Revoke/Delete Authenticator
app.delete("/api/account/authenticators/:id", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";
  const { id } = req.params;

  const authIdx = authenticators.findIndex(a => a.id === id && a.principalId === principalId);
  if (authIdx === -1) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator not found." });
  }

  const auth = authenticators[authIdx];

  // Self-lockout protection
  const activeRemainingAuths = authenticators.filter(
    a => a.principalId === principalId && a.id !== id && a.state === "active"
  );

  const hasPasswordLeft = activeRemainingAuths.some(a => a.kind === "password");

  if (activeRemainingAuths.length === 0) {
    return res.status(400).json({
      error: "SELF_LOCKOUT_PREVENTION",
      message: "Prohibited action: Deleting this authenticator would leave your account with no active authentication factor, resulting in immediate lockout."
    });
  }

  // Soft delete / Revoke state instead of raw database splice to retain metadata/audit
  auth.state = "revoked";
  auth.revokedAt = new Date().toISOString();

  logAudit(
    principalId,
    "revoke",
    "success",
    `User voluntarily revoked/deleted authenticator '${auth.displayName}' (${auth.kind})`,
    principalId,
    auth.id
  );

  res.json({ status: "success", authenticator: auth });
});

// POST Rotate Recovery Codes
app.post("/api/account/recovery-codes/rotate", (req, res) => {
  const principalId = (req.headers["x-principal-id"] as string) || "user-alice";

  // Revoke any active recovery codes
  authenticators = authenticators.map(a => {
    if (a.principalId === principalId && a.kind === "recovery_code" && a.state === "active") {
      return { ...a, state: "revoked", revokedAt: new Date().toISOString() };
    }
    return a;
  });

  // Generate 10 new recovery codes
  const codes = Array.from({ length: 10 }, () =>
    Math.floor(10000000 + Math.random() * 90000000).toString().replace(/(\d{4})(\d{4})/, "$1-$2")
  );

  const newAuthId = "auth-rec-" + Date.now().toString(36);
  const newAuth: Authenticator = {
    id: newAuthId,
    principalId,
    tenantId: "tenant-acme",
    kind: "recovery_code",
    displayName: "Emergency Recovery Codes",
    state: "active",
    enrolledAt: new Date().toISOString(),
    lastVerifiedAt: null,
    lastUsedAt: null,
    expiresAt: null,
    suspendedAt: null,
    revokedAt: null,
    amr: ["recovery_code"],
    properties: getPropertiesForKind("recovery_code"),
    attestationSummary: "Server-side cryptographically signed recovery blocks",
    recoveryEligibility: true,
    version: 1,
    details: { remainingCount: 10, totalCount: 10 }
  };

  authenticators.push(newAuth);

  logAudit(
    principalId,
    "rotate_recovery_codes",
    "success",
    `Rotated emergency recovery codes. 10 fresh tokens issued.`,
    principalId,
    newAuthId
  );

  res.json({
    status: "success",
    authenticator: newAuth,
    recoveryCodes: codes
  });
});


// ==========================================
// TENANT ADMIN / HELP DESK ROUTES
// ==========================================

// GET policy
app.get("/api/admin/authenticators/policy", (req, res) => {
  res.json({
    current: activePolicy,
    history: policyHistory
  });
});

// PATCH policy
app.patch("/api/admin/authenticators/policy", (req, res) => {
  const { allowedKinds, requiredKinds, prohibitedKinds, stepUpEligibleKinds, gracePeriodDays, attestationPolicy, allowedAlgorithms } = req.body;

  // Audit lock-out risk in simulation
  // Prohibiting password or having no allowed MFA kinds is highly risky.
  let warningMessage = "";
  if (prohibitedKinds && prohibitedKinds.includes("password")) {
    warningMessage = "CRITICAL RISK: Prohibiting corporate passwords without pre-configured, enforced federated logins could lock out all corporate users.";
  }

  // Push old active policy into history
  policyHistory.unshift({ ...activePolicy });

  // Update current active policy
  activePolicy = {
    ...activePolicy,
    allowedKinds: allowedKinds || activePolicy.allowedKinds,
    requiredKinds: requiredKinds || activePolicy.requiredKinds,
    prohibitedKinds: prohibitedKinds || activePolicy.prohibitedKinds,
    stepUpEligibleKinds: stepUpEligibleKinds || activePolicy.stepUpEligibleKinds,
    gracePeriodDays: gracePeriodDays !== undefined ? Number(gracePeriodDays) : activePolicy.gracePeriodDays,
    attestationPolicy: attestationPolicy || activePolicy.attestationPolicy,
    allowedAlgorithms: allowedAlgorithms || activePolicy.allowedAlgorithms,
    updatedBy: "user-admin",
    updatedAt: new Date().toISOString(),
    version: activePolicy.version + 1
  };

  logAudit(
    "all",
    "policy_patch",
    "success",
    `Admin updated tenant authenticator policy. Enrolled new policy version ${activePolicy.version}. ${warningMessage}`,
    "user-admin"
  );

  res.json({
    status: "success",
    policy: activePolicy,
    warning: warningMessage || null
  });
});

// POST policy rollback
app.post("/api/admin/authenticators/policy/rollback", (req, res) => {
  const { version } = req.body;
  const histIdx = policyHistory.findIndex(h => h.version === Number(version));
  if (histIdx === -1) {
    return res.status(404).json({ error: "POLICY_NOT_FOUND", message: `Version ${version} was not found in the historical log.` });
  }

  const rollbackTarget = policyHistory[histIdx];
  // Remove rolled-back policy and older ones from future history as we re-commit
  policyHistory.splice(0, histIdx + 1);

  policyHistory.unshift({ ...activePolicy });

  activePolicy = {
    ...rollbackTarget,
    updatedBy: "user-admin",
    updatedAt: new Date().toISOString(),
    version: activePolicy.version + 1 // New version count keeps counting up
  };

  logAudit(
    "all",
    "policy_rollback",
    "success",
    `Admin rolled back tenant authenticator policy to target configuration from version ${version}.`,
    "user-admin"
  );

  res.json({
    status: "success",
    policy: activePolicy
  });
});

// GET authenticators for specific identity (tenant admin view)
app.get("/api/admin/identities/:identity_id/authenticators", (req, res) => {
  const { identity_id } = req.params;
  const userAuths = authenticators.filter(a => a.principalId === identity_id);
  res.json(userAuths);
});

// POST Suspend an Authenticator (Administrative help-desk action)
app.post("/api/admin/identities/:identity_id/authenticators/:id/suspend", (req, res) => {
  const { identity_id, id } = req.params;
  const { reason, ticket } = req.body;

  const auth = authenticators.find(a => a.id === id && a.principalId === identity_id);
  if (!auth) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator not found." });
  }

  auth.state = "suspended";
  auth.suspendedAt = new Date().toISOString();
  auth.version += 1;

  logAudit(
    identity_id,
    "suspend",
    "success",
    `Help-desk Administrator suspended authenticator '${auth.displayName}'. Reason: ${reason || "None specified"}. Case ID: ${ticket || "N/A"}.`,
    "user-admin",
    auth.id,
    "ADMIN_SUSPENSION"
  );

  res.json({ status: "success", authenticator: auth });
});

// POST Activate/Unsuspend an Authenticator
app.post("/api/admin/identities/:identity_id/authenticators/:id/activate", (req, res) => {
  const { identity_id, id } = req.params;

  const auth = authenticators.find(a => a.id === id && a.principalId === identity_id);
  if (!auth) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator not found." });
  }

  auth.state = "active";
  auth.suspendedAt = null;
  auth.version += 1;

  logAudit(
    identity_id,
    "unsuspend",
    "success",
    `Help-desk Administrator restored suspended authenticator '${auth.displayName}' back to active state.`,
    "user-admin",
    auth.id
  );

  res.json({ status: "success", authenticator: auth });
});

// POST Force/Require Re-enrollment of an Authenticator (Help-desk action)
app.post("/api/admin/identities/:identity_id/authenticators/:id/require-reenrollment", (req, res) => {
  const { identity_id, id } = req.params;

  const auth = authenticators.find(a => a.id === id && a.principalId === identity_id);
  if (!auth) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Authenticator not found." });
  }

  auth.state = "pending"; // Triggers re-enrollment required
  auth.version += 1;

  logAudit(
    identity_id,
    "require-reenrollment",
    "success",
    `Help-desk Administrator marked authenticator '${auth.displayName}' as requiring active re-enrollment.`,
    "user-admin",
    auth.id,
    "RE_ENROLL_REQUIRED"
  );

  res.json({ status: "success", authenticator: auth });
});

// POST Initiate approved recovery for a user (starts temporary authorization / resets state)
app.post("/api/admin/identities/:identity_id/recovery/start", (req, res) => {
  const { identity_id } = req.params;
  const { reason, caseReference } = req.body;

  const identity = IDENTITIES.find(i => i.id === identity_id);
  if (!identity) {
    return res.status(404).json({ error: "NOT_FOUND", message: "Identity profile not found." });
  }

  // Simulation of supervised temporary access key issuance
  const temporaryBypassCode = Math.floor(100000 + Math.random() * 900000).toString();

  logAudit(
    identity_id,
    "admin_recovery_start",
    "success",
    `Supervised help-desk recovery initiated for '${identity.name}'. Issue approved recovery bypass code. Ticket Ref: ${caseReference || "N/A"}`,
    "user-admin",
    undefined,
    "HELP_DESK_RECOVERY_ISSUED"
  );

  res.json({
    status: "success",
    bypassCode: temporaryBypassCode,
    expiresAt: new Date(Date.now() + 15 * 60 * 1000).toISOString() // 15 min expiration
  });
});

// GET Audit logs
app.get("/api/admin/authenticators/audit", (req, res) => {
  res.json(auditLogs);
});


// ==========================================
// VITE DEV SERVER / PRODUCTION ENTRY
// ==========================================

async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa"
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
    console.log(`Server running on port ${PORT} in ${process.env.NODE_ENV || 'development'} mode`);
  });
}

startServer();
