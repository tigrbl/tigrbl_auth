import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { 
  AuthenticatorEnum, 
  DisplayCategory, 
  CeremonyState, 
  CeremonyPurpose, 
  Authenticator, 
  AuthenticatorPolicy, 
  Ceremony, 
  AuthEvent 
} from "./src/types";

// Initialize in-memory database for state preservation
let authenticators: Authenticator[] = [
  {
    id: "auth-pass-1",
    name: "Primary Password",
    type: AuthenticatorEnum.PASSWORD_LOCAL,
    category: DisplayCategory.HUMAN,
    status: "active",
    created: "2026-01-10T10:00:00Z",
    properties: {
      phishingResistant: false,
      hardwareProtected: false,
      userPresent: true,
      userVerified: true,
      senderConstrained: false,
      replayResistant: false
    }
  },
  {
    id: "auth-totp-1",
    name: "Google Authenticator (Work Phone)",
    type: AuthenticatorEnum.OTP_LOCAL,
    category: DisplayCategory.HUMAN,
    status: "active",
    created: "2026-02-15T14:30:00Z",
    properties: {
      phishingResistant: false,
      hardwareProtected: false,
      userPresent: true,
      userVerified: true,
      senderConstrained: false,
      replayResistant: false
    }
  },
  {
    id: "auth-passkey-1",
    name: "MacBook Pro TouchID",
    type: AuthenticatorEnum.WEBAUTHN_LOCAL,
    category: DisplayCategory.HUMAN,
    status: "active",
    created: "2026-03-20T09:15:00Z",
    lastUsed: "2026-07-12T15:20:00Z",
    metadata: {
      platform: "Apple iCloud Keychain",
      synced: true,
      aaguid: "adce0002-35bc-c60a-2b7b-40b2fed21711"
    },
    properties: {
      phishingResistant: true,
      hardwareProtected: true,
      userPresent: true,
      userVerified: true,
      senderConstrained: false,
      replayResistant: true
    }
  },
  {
    id: "auth-securitykey-1",
    name: "YubiKey 5C NFC",
    type: AuthenticatorEnum.WEBAUTHN_LOCAL,
    category: DisplayCategory.HUMAN,
    status: "active",
    created: "2026-04-01T11:00:00Z",
    lastUsed: "2026-07-11T18:40:00Z",
    metadata: {
      platform: "Yubico Hardware",
      synced: false,
      aaguid: "cb69481e-8e17-48f1-b92c-d922df66d5b3"
    },
    properties: {
      phishingResistant: true,
      hardwareProtected: true,
      userPresent: true,
      userVerified: true,
      senderConstrained: false,
      replayResistant: true
    }
  },
  {
    id: "auth-oidc-google",
    name: "Google Workspace Account (jick.68.0@gmail.com)",
    type: AuthenticatorEnum.FEDERATED_OIDC,
    category: DisplayCategory.HUMAN,
    status: "active",
    created: "2026-01-10T10:05:00Z",
    metadata: {
      issuer: "https://accounts.google.com",
      subject: "google-sub-123456789"
    },
    properties: {
      phishingResistant: false,
      hardwareProtected: false,
      userPresent: true,
      userVerified: false,
      senderConstrained: false,
      replayResistant: false
    }
  },
  {
    id: "auth-recovery-codes",
    name: "Account Backup Recovery Codes",
    type: AuthenticatorEnum.RECOVERY_CODE_LOCAL,
    category: DisplayCategory.RECOVERY,
    status: "active",
    created: "2026-01-10T10:02:00Z",
    metadata: {
      totalCodes: 10,
      remainingCodes: 8
    },
    properties: {
      phishingResistant: false,
      hardwareProtected: false,
      userPresent: true,
      userVerified: true,
      senderConstrained: false,
      replayResistant: true
    }
  },
  {
    id: "auth-clientsecret-1",
    name: "Auth Core Sync Agent",
    type: AuthenticatorEnum.CLIENT_SECRET_LOCAL,
    category: DisplayCategory.MACHINE,
    status: "active",
    created: "2026-05-12T08:00:00Z",
    lastUsed: "2026-07-12T18:30:00Z",
    metadata: {
      clientId: "client-sync-01",
      prefix: "tgb_sec_live_..."
    },
    properties: {
      phishingResistant: false,
      hardwareProtected: false,
      userPresent: false,
      userVerified: false,
      senderConstrained: false,
      replayResistant: false
    }
  },
  {
    id: "auth-apikey-1",
    name: "Production Logging API Key",
    type: AuthenticatorEnum.API_KEY_LOCAL,
    category: DisplayCategory.MACHINE,
    status: "active",
    created: "2026-05-20T10:15:00Z",
    lastUsed: "2026-07-12T18:45:00Z",
    metadata: {
      prefix: "tgb_key_prod_a98..."
    },
    properties: {
      phishingResistant: false,
      hardwareProtected: false,
      userPresent: false,
      userVerified: false,
      senderConstrained: false,
      replayResistant: false
    }
  },
  {
    id: "auth-servicekey-1",
    name: "Spanner Ledger Connector Service Key",
    type: AuthenticatorEnum.SERVICE_KEY_LOCAL,
    category: DisplayCategory.MACHINE,
    status: "active",
    created: "2026-06-01T15:20:00Z",
    lastUsed: "2026-07-12T18:10:00Z",
    metadata: {
      prefix: "tgb_svckey_span_..."
    },
    properties: {
      phishingResistant: false,
      hardwareProtected: false,
      userPresent: false,
      userVerified: false,
      senderConstrained: false,
      replayResistant: false
    }
  },
  {
    id: "auth-mtls-1",
    name: "Enterprise Gateway mTLS Client Certificate",
    type: AuthenticatorEnum.MTLS_CLIENT_CERT,
    category: DisplayCategory.MACHINE,
    status: "active",
    created: "2026-06-15T09:00:00Z",
    metadata: {
      subject: "CN=gateway.enterprise.internal, O=Tigrbl Core, C=US",
      fingerprint: "6A:B9:4C:E3:89:12:35:FC:B6:81:42:01:DF:EE:AA:53:C9:92:DF:CC"
    },
    properties: {
      phishingResistant: true,
      hardwareProtected: true,
      userPresent: false,
      userVerified: false,
      senderConstrained: true,
      replayResistant: true
    }
  }
];

let ceremonies: Record<string, Ceremony> = {};

let policies: AuthenticatorPolicy[] = [
  {
    id: "policy-v1",
    version: 1,
    isActive: false,
    allowedMethods: [
      AuthenticatorEnum.PASSWORD_LOCAL,
      AuthenticatorEnum.OTP_LOCAL,
      AuthenticatorEnum.RECOVERY_CODE_LOCAL,
      AuthenticatorEnum.FEDERATED_OIDC
    ],
    requiredMethods: [AuthenticatorEnum.PASSWORD_LOCAL],
    prohibitedMethods: [],
    attestationPolicy: "none",
    algorithmPolicy: ["ES256", "RS256"],
    mfaGracePeriodDays: 14,
    requireHardwareProtection: false,
    updatedAt: "2026-01-01T00:00:00Z",
    updatedBy: "System Setup"
  },
  {
    id: "policy-v2",
    version: 2,
    isActive: true,
    allowedMethods: [
      AuthenticatorEnum.PASSWORD_LOCAL,
      AuthenticatorEnum.OTP_LOCAL,
      AuthenticatorEnum.WEBAUTHN_LOCAL,
      AuthenticatorEnum.RECOVERY_CODE_LOCAL,
      AuthenticatorEnum.FEDERATED_OIDC,
      AuthenticatorEnum.CLIENT_SECRET_LOCAL,
      AuthenticatorEnum.API_KEY_LOCAL,
      AuthenticatorEnum.SERVICE_KEY_LOCAL,
      AuthenticatorEnum.MTLS_CLIENT_CERT,
      AuthenticatorEnum.DPOP_PROOF,
      AuthenticatorEnum.SESSION_LOCAL,
      AuthenticatorEnum.REMOTE_INTROSPECTION
    ],
    requiredMethods: [],
    prohibitedMethods: [],
    attestationPolicy: "indirect",
    algorithmPolicy: ["ES256", "RS256", "Ed25519"],
    mfaGracePeriodDays: 7,
    requireHardwareProtection: false,
    updatedAt: "2026-05-15T12:00:00Z",
    updatedBy: "security-admin@tigrbl.internal"
  }
];

let activePolicyId = "policy-v2";

let auditEvents: AuthEvent[] = [
  {
    id: "evt-1",
    timestamp: "2026-07-12T10:00:00Z",
    eventType: "USER_LOGIN_SUCCESS",
    subjectId: "usr-jick",
    tenantId: "tenant-default",
    authenticatorType: AuthenticatorEnum.PASSWORD_LOCAL,
    authenticatorId: "auth-pass-1",
    success: true,
    ipAddress: "192.168.1.50",
    location: "Oakland, CA, USA",
    acr: "urn:tigrbl:acr:aal1",
    amr: ["password_local"],
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    details: "Standard identifier-first password authentication succeeded"
  },
  {
    id: "evt-2",
    timestamp: "2026-07-12T15:20:00Z",
    eventType: "USER_STEP_UP_SUCCESS",
    subjectId: "usr-jick",
    tenantId: "tenant-default",
    authenticatorType: AuthenticatorEnum.WEBAUTHN_LOCAL,
    authenticatorId: "auth-passkey-1",
    success: true,
    ipAddress: "192.168.1.50",
    location: "Oakland, CA, USA",
    acr: "urn:tigrbl:acr:aal3",
    amr: ["password_local", "webauthn_local"],
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    details: "MFA challenge completed via hardware-backed platform passkey"
  }
];

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Log helper
  const logEvent = (
    eventType: string,
    success: boolean,
    details: string,
    extra: Partial<AuthEvent> = {}
  ) => {
    const event: AuthEvent = {
      id: `evt-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      timestamp: new Date().toISOString(),
      eventType,
      subjectId: "usr-jick",
      tenantId: "tenant-default",
      success,
      ipAddress: "192.168.1.50",
      location: "Oakland, CA, USA",
      userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
      details,
      ...extra
    };
    auditEvents.unshift(event);
    return event;
  };

  // ==================== CATALOG ENDPOINTS ====================
  app.get("/api/catalog", (req, res) => {
    // Return display metadata, maturity, and characteristics of all providers
    res.json({
      providers: [
        {
          type: AuthenticatorEnum.PASSWORD_LOCAL,
          category: DisplayCategory.HUMAN,
          label: "Password",
          description: "Standard primary credential verified on the secure backend",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal1",
          phishingResistant: false,
          hardwareProtected: false
        },
        {
          type: AuthenticatorEnum.OTP_LOCAL,
          category: DisplayCategory.HUMAN,
          label: "Authenticator App (TOTP)",
          description: "Generates time-based one-time verification codes using an app like Google Authenticator",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal2",
          phishingResistant: false,
          hardwareProtected: false
        },
        {
          type: AuthenticatorEnum.WEBAUTHN_LOCAL,
          category: DisplayCategory.HUMAN,
          label: "WebAuthn Passkey / Security Key",
          description: "Phishing-resistant biometrics, device keys, or roaming hardware keys",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal3",
          phishingResistant: true,
          hardwareProtected: true
        },
        {
          type: AuthenticatorEnum.FEDERATED_OIDC,
          category: DisplayCategory.HUMAN,
          label: "Federated Identity (OIDC)",
          description: "Sign-in securely through trusted upstream identity providers",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal2",
          phishingResistant: false,
          hardwareProtected: false
        },
        {
          type: AuthenticatorEnum.RECOVERY_CODE_LOCAL,
          category: DisplayCategory.RECOVERY,
          label: "Backup Recovery Codes",
          description: "Highly secure, one-time use printable recovery codes",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:recovery",
          phishingResistant: false,
          hardwareProtected: false
        },
        {
          type: AuthenticatorEnum.CLIENT_SECRET_LOCAL,
          category: DisplayCategory.MACHINE,
          label: "Client Secret",
          description: "Confidential credentials issued for application server-to-server auth",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal1",
          phishingResistant: false,
          hardwareProtected: false
        },
        {
          type: AuthenticatorEnum.API_KEY_LOCAL,
          category: DisplayCategory.MACHINE,
          label: "API Key",
          description: "Scoped token keys for lightweight machine clients and webhooks",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal1",
          phishingResistant: false,
          hardwareProtected: false
        },
        {
          type: AuthenticatorEnum.SERVICE_KEY_LOCAL,
          category: DisplayCategory.MACHINE,
          label: "Service Account Key",
          description: "Cryptographic service credentials for direct tenant background actions",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal1",
          phishingResistant: false,
          hardwareProtected: false
        },
        {
          type: AuthenticatorEnum.MTLS_CLIENT_CERT,
          category: DisplayCategory.MACHINE,
          label: "mTLS Client Certificate",
          description: "Phishing-resistant client authentication bound directly at the TLS layer",
          maturity: "production",
          assuranceLevel: "urn:tigrbl:acr:aal3",
          phishingResistant: true,
          hardwareProtected: true
        }
      ]
    });
  });

  // ==================== CURRENT-SUBJECT AUTHENTICATORS ====================
  app.get("/api/authenticators", (req, res) => {
    res.json({ authenticators });
  });

  app.post("/api/authenticators/enroll/start", (req, res) => {
    const { type, name } = req.body;
    if (!type) {
      return res.status(400).json({ error: "Authenticator type is required" });
    }

    const id = `auth-${type.replace("_local", "")}-${Date.now()}`;
    
    // WebAuthn specific challenge setup
    let challengeDescriptor = "";
    let seed = "";
    if (type === AuthenticatorEnum.WEBAUTHN_LOCAL) {
      challengeDescriptor = Buffer.from(Math.random().toString()).toString("base64");
    } else if (type === AuthenticatorEnum.OTP_LOCAL) {
      // Return secret seed for QR
      seed = "HXH44YKLVPLXURK3NJ7H27BGL2KSLY6B";
    }

    const enrollmentCeremony: Ceremony = {
      id: `cer-${Date.now()}`,
      type,
      purpose: CeremonyPurpose.ENROLLMENT,
      state: CeremonyState.AWAITING_USER,
      subjectDisplayName: "jick.68.0@gmail.com",
      tenantId: "tenant-default",
      realm: "realm-main",
      challengeDescriptor,
      expiryTime: new Date(Date.now() + 5 * 60 * 1000).toISOString(),
      serverTime: new Date().toISOString(),
      attemptBudget: 3,
      attemptsRemaining: 3,
      methodSwitchEligibility: [],
      cancellationPolicy: "allowed",
      correlationId: `corr-${Date.now()}`,
      riskSafeExplanation: `Enrollment initialization for new ${type} authenticator.`,
      nextAction: type === AuthenticatorEnum.WEBAUTHN_LOCAL ? "PROMPT_WEBAUTHN_NAVIGATOR" : "VERIFY_TOTP_CODE_INPUT",
      callbackTarget: `/api/authenticators/enroll/finish`
    };

    ceremonies[enrollmentCeremony.id] = enrollmentCeremony;

    res.json({
      ceremony: enrollmentCeremony,
      seed,
      qrUrl: seed ? `otpauth://totp/Tigrbl:jick.68.0@gmail.com?secret=${seed}&issuer=Tigrbl` : undefined
    });
  });

  app.post("/api/authenticators/enroll/finish", (req, res) => {
    const { ceremonyId, response, name, type, metadata } = req.body;
    const ceremony = ceremonies[ceremonyId];

    if (!ceremony) {
      return res.status(404).json({ error: "Enrollment ceremony not found" });
    }

    if (new Date(ceremony.expiryTime) < new Date()) {
      ceremony.state = CeremonyState.EXPIRED;
      return res.status(400).json({ error: "Enrollment ceremony expired" });
    }

    // Verify code for TOTP, or credential for WebAuthn
    if (ceremony.type === AuthenticatorEnum.OTP_LOCAL) {
      if (response !== "123456") {
        ceremony.attemptsRemaining--;
        if (ceremony.attemptsRemaining <= 0) {
          ceremony.state = CeremonyState.TERMINAL_FAILURE;
          logEvent("MFA_ENROLL_FAILED", false, "TOTP Enrollment code verification failed: attempts exhausted", { authenticatorType: ceremony.type });
          return res.status(400).json({ error: "Invalid verification code. Attempts exhausted." });
        }
        logEvent("MFA_ENROLL_FAILED", false, "TOTP Enrollment code incorrect", { authenticatorType: ceremony.type });
        return res.status(400).json({ error: "Invalid verification code", attemptsRemaining: ceremony.attemptsRemaining, retryable: true });
      }
    } else if (ceremony.type === AuthenticatorEnum.WEBAUTHN_LOCAL) {
      if (!response || response.cancelled) {
        ceremony.state = CeremonyState.CANCELLED;
        logEvent("WEBAUTHN_ENROLL_CANCELLED", false, "WebAuthn ceremony was cancelled by user", { authenticatorType: ceremony.type });
        return res.status(400).json({ error: "Passkey operation cancelled by browser or user" });
      }
    }

    ceremony.state = CeremonyState.SUCCEEDED;

    // Create the authenticator
    const isWebAuthn = ceremony.type === AuthenticatorEnum.WEBAUTHN_LOCAL;
    const newAuth: Authenticator = {
      id: `auth-${ceremony.type.replace("_local", "")}-${Date.now()}`,
      name: name || `My ${ceremony.type}`,
      type: ceremony.type,
      category: ceremony.type === AuthenticatorEnum.RECOVERY_CODE_LOCAL ? DisplayCategory.RECOVERY : DisplayCategory.HUMAN,
      status: "active",
      created: new Date().toISOString(),
      metadata: isWebAuthn ? {
        platform: "Roaming Security Key",
        synced: false,
        ...metadata
      } : metadata,
      properties: isWebAuthn ? {
        phishingResistant: true,
        hardwareProtected: true,
        userPresent: true,
        userVerified: true,
        senderConstrained: false,
        replayResistant: true
      } : {
        phishingResistant: false,
        hardwareProtected: false,
        userPresent: true,
        userVerified: true,
        senderConstrained: false,
        replayResistant: false
      }
    };

    authenticators.push(newAuth);
    logEvent("AUTHENTICATOR_ENROLLED", true, `Successfully enrolled new authenticator: ${newAuth.name}`, {
      authenticatorId: newAuth.id,
      authenticatorType: newAuth.type
    });

    res.json({ success: true, authenticator: newAuth });
  });

  app.put("/api/authenticators/:id", (req, res) => {
    const { name, status } = req.body;
    const auth = authenticators.find(a => a.id === req.params.id);
    if (!auth) {
      return res.status(404).json({ error: "Authenticator not found" });
    }

    if (name) auth.name = name;
    if (status) auth.status = status;

    logEvent("AUTHENTICATOR_UPDATED", true, `Updated authenticator properties for: ${auth.name}`, {
      authenticatorId: auth.id,
      authenticatorType: auth.type
    });

    res.json({ success: true, authenticator: auth });
  });

  app.delete("/api/authenticators/:id", (req, res) => {
    const authIdx = authenticators.findIndex(a => a.id === req.params.id);
    if (authIdx === -1) {
      return res.status(404).json({ error: "Authenticator not found" });
    }

    const auth = authenticators[authIdx];

    // Safeguard: Check if it's the last human factor remaining
    const humanFactors = authenticators.filter(a => a.category === DisplayCategory.HUMAN && a.id !== req.params.id);
    const passFactors = humanFactors.filter(a => a.type === AuthenticatorEnum.PASSWORD_LOCAL || a.type === AuthenticatorEnum.WEBAUTHN_LOCAL);
    
    if (passFactors.length === 0 && auth.category === DisplayCategory.HUMAN) {
      return res.status(400).json({
        error: "Lockout prevention: Cannot delete the final authentication factor that secures your account."
      });
    }

    authenticators.splice(authIdx, 1);
    logEvent("AUTHENTICATOR_DELETED", true, `Removed authenticator factor: ${auth.name}`, {
      authenticatorId: auth.id,
      authenticatorType: auth.type
    });

    res.json({ success: true });
  });

  app.post("/api/authenticators/recovery-codes/rotate", (req, res) => {
    const auth = authenticators.find(a => a.type === AuthenticatorEnum.RECOVERY_CODE_LOCAL);
    if (!auth) {
      return res.status(404).json({ error: "No recovery codes enrolled" });
    }

    const newCodes = Array.from({ length: 8 }, () => 
      Math.floor(10000000 + Math.random() * 90000000).toString().replace(/(\d{4})(\d{4})/, "$1-$2")
    );

    auth.metadata = {
      totalCodes: 8,
      remainingCodes: 8,
      codesPreview: newCodes // Exposed ONLY during this single response
    };

    logEvent("RECOVERY_CODES_ROTATED", true, "Generated new set of 8 backup recovery codes", {
      authenticatorId: auth.id,
      authenticatorType: auth.type
    });

    res.json({ success: true, codes: newCodes });
  });

  app.post("/api/authenticators/federation/link", (req, res) => {
    const { provider, email } = req.body;
    if (!provider) {
      return res.status(400).json({ error: "Provider is required" });
    }

    const exists = authenticators.find(a => a.type === AuthenticatorEnum.FEDERATED_OIDC && a.name.includes(provider));
    if (exists) {
      return res.status(400).json({ error: `Account already federated with ${provider}` });
    }

    const newOidc: Authenticator = {
      id: `auth-oidc-${provider}-${Date.now()}`,
      name: `${provider} Account (${email || "jick.68.0@gmail.com"})`,
      type: AuthenticatorEnum.FEDERATED_OIDC,
      category: DisplayCategory.HUMAN,
      status: "active",
      created: new Date().toISOString(),
      metadata: {
        issuer: `https://${provider.toLowerCase()}.com`,
        subject: `sub-${provider.toLowerCase()}-${Date.now()}`
      },
      properties: {
        phishingResistant: false,
        hardwareProtected: false,
        userPresent: true,
        userVerified: false,
        senderConstrained: false,
        replayResistant: false
      }
    };

    authenticators.push(newOidc);
    logEvent("FEDERATION_LINKED", true, `Linked federated OIDC provider: ${provider}`, {
      authenticatorId: newOidc.id,
      authenticatorType: newOidc.type
    });

    res.json({ success: true, authenticator: newOidc });
  });

  app.post("/api/authenticators/federation/unlink", (req, res) => {
    const { provider } = req.body;
    const idx = authenticators.findIndex(a => a.type === AuthenticatorEnum.FEDERATED_OIDC && a.name.includes(provider));
    if (idx === -1) {
      return res.status(404).json({ error: `OIDC federation for ${provider} not found` });
    }

    const auth = authenticators[idx];
    authenticators.splice(idx, 1);
    logEvent("FEDERATION_UNLINKED", true, `Unlinked federated provider: ${provider}`, {
      authenticatorId: auth.id,
      authenticatorType: auth.type
    });

    res.json({ success: true });
  });

  // ==================== CEREMONIES ENDPOINTS ====================
  app.post("/api/ceremonies/start", (req, res) => {
    const { purpose, type, requiredAcr } = req.body;

    const selectedType = type || AuthenticatorEnum.PASSWORD_LOCAL;
    const ceremonyId = `cer-${Date.now()}`;
    const desc = selectedType === AuthenticatorEnum.WEBAUTHN_LOCAL 
      ? Buffer.from(Math.random().toString()).toString("base64")
      : undefined;

    let explanation = "Verify identity to access application console";
    if (purpose === CeremonyPurpose.STEP_UP) {
      explanation = "Elevated hardware security check required to modify tenant policies";
    } else if (purpose === CeremonyPurpose.RECOVERY) {
      explanation = "Verify primary recovery methods to override locked-out credentials";
    }

    // Determine eligible switch fallback options
    const switchOptions = authenticators
      .filter(a => a.category === DisplayCategory.HUMAN || a.category === DisplayCategory.RECOVERY)
      .map(a => a.type)
      .filter((v, i, self) => self.indexOf(v) === i && v !== selectedType);

    const ceremony: Ceremony = {
      id: ceremonyId,
      type: selectedType,
      purpose: purpose || CeremonyPurpose.SIGN_IN,
      state: CeremonyState.AWAITING_USER,
      subjectDisplayName: "jick.68.0@gmail.com",
      tenantId: "tenant-default",
      realm: "realm-main",
      challengeDescriptor: desc,
      expiryTime: new Date(Date.now() + 5 * 60 * 1000).toISOString(),
      serverTime: new Date().toISOString(),
      attemptBudget: 5,
      attemptsRemaining: 5,
      methodSwitchEligibility: switchOptions,
      requiredAcr: requiredAcr || (purpose === CeremonyPurpose.STEP_UP ? "urn:tigrbl:acr:aal3" : "urn:tigrbl:acr:aal1"),
      riskSafeExplanation: explanation,
      cancellationPolicy: "allowed",
      correlationId: `corr-${Date.now()}`
    };

    ceremonies[ceremonyId] = ceremony;
    logEvent("CEREMONY_STARTED", true, `Ceremony started for ${selectedType} (${ceremony.purpose})`, {
      acr: ceremony.requiredAcr
    });

    res.json({ ceremony });
  });

  app.get("/api/ceremonies/:id", (req, res) => {
    const ceremony = ceremonies[req.params.id];
    if (!ceremony) {
      return res.status(404).json({ error: "Ceremony not found" });
    }
    // Update server time on read
    ceremony.serverTime = new Date().toISOString();
    res.json({ ceremony });
  });

  app.post("/api/ceremonies/:id/switch", (req, res) => {
    const ceremony = ceremonies[req.params.id];
    const { targetType } = req.body;

    if (!ceremony) {
      return res.status(404).json({ error: "Ceremony not found" });
    }

    if (!ceremony.methodSwitchEligibility.includes(targetType)) {
      return res.status(400).json({ error: `Method switch to ${targetType} is prohibited by current policy` });
    }

    ceremony.type = targetType;
    ceremony.attemptsRemaining = 5; // Reset budget on switch
    ceremony.challengeDescriptor = targetType === AuthenticatorEnum.WEBAUTHN_LOCAL 
      ? Buffer.from(Math.random().toString()).toString("base64")
      : undefined;

    logEvent("CEREMONY_METHOD_SWITCHED", true, `Switched ceremony authentication method to ${targetType}`, {
      acr: ceremony.requiredAcr
    });

    res.json({ ceremony });
  });

  app.post("/api/ceremonies/:id/cancel", (req, res) => {
    const ceremony = ceremonies[req.params.id];
    if (!ceremony) {
      return res.status(404).json({ error: "Ceremony not found" });
    }

    ceremony.state = CeremonyState.CANCELLED;
    logEvent("CEREMONY_CANCELLED", true, "User terminated the ceremony", {
      acr: ceremony.requiredAcr
    });

    res.json({ ceremony });
  });

  app.post("/api/ceremonies/:id/finish", (req, res) => {
    const ceremony = ceremonies[req.params.id];
    const { secret, clientAssertion } = req.body;

    if (!ceremony) {
      return res.status(404).json({ error: "Ceremony not found" });
    }

    if (ceremony.state === CeremonyState.SUCCEEDED) {
      return res.json({ success: true, ceremony });
    }

    if (new Date(ceremony.expiryTime) < new Date()) {
      ceremony.state = CeremonyState.EXPIRED;
      return res.status(400).json({ error: "Ceremony session has expired" });
    }

    // Core validation based on type
    let valid = false;
    let message = "";

    if (ceremony.type === AuthenticatorEnum.PASSWORD_LOCAL) {
      if (secret === "password" || secret === "correct-password") {
        valid = true;
        ceremony.achievedAcr = "urn:tigrbl:acr:aal1";
      } else {
        message = "Incorrect password.";
      }
    } else if (ceremony.type === AuthenticatorEnum.OTP_LOCAL) {
      if (secret === "123456" || secret === "654321") {
        valid = true;
        ceremony.achievedAcr = "urn:tigrbl:acr:aal2";
      } else {
        message = "Invalid six-digit verification code.";
      }
    } else if (ceremony.type === AuthenticatorEnum.WEBAUTHN_LOCAL) {
      if (clientAssertion && !clientAssertion.error) {
        valid = true;
        ceremony.achievedAcr = "urn:tigrbl:acr:aal3";
      } else {
        message = "Passkey hardware validation failed.";
      }
    } else if (ceremony.type === AuthenticatorEnum.RECOVERY_CODE_LOCAL) {
      if (secret && secret.length >= 8) {
        valid = true;
        ceremony.achievedAcr = "urn:tigrbl:acr:recovery";
        // Decrement remaining recovery codes
        const codeAuth = authenticators.find(a => a.type === AuthenticatorEnum.RECOVERY_CODE_LOCAL);
        if (codeAuth && codeAuth.metadata) {
          codeAuth.metadata.remainingCodes = Math.max(0, codeAuth.metadata.remainingCodes - 1);
        }
      } else {
        message = "Invalid backup recovery code.";
      }
    } else if (ceremony.type === AuthenticatorEnum.FEDERATED_OIDC) {
      valid = true; // Simulating OIDC callback success
      ceremony.achievedAcr = "urn:tigrbl:acr:aal2";
    }

    if (valid) {
      ceremony.state = CeremonyState.SUCCEEDED;
      ceremony.evidence = {
        amr: [ceremony.type],
        properties: ceremony.type === AuthenticatorEnum.WEBAUTHN_LOCAL ? ["phishing_resistant", "hardware_protected"] : [],
        time: new Date().toISOString()
      };
      logEvent("CEREMONY_SUCCESS", true, `Identity successfully verified via ${ceremony.type}`, {
        acr: ceremony.achievedAcr,
        amr: [ceremony.type]
      });
      res.json({ success: true, ceremony });
    } else {
      ceremony.attemptsRemaining--;
      if (ceremony.attemptsRemaining <= 0) {
        ceremony.state = CeremonyState.TERMINAL_FAILURE;
        logEvent("CEREMONY_FAILED_LOCKOUT", false, `Authentication failed for ${ceremony.type}: budget exhausted`, {
          acr: ceremony.requiredAcr
        });
        res.status(400).json({ error: `${message} Attempts remaining: 0. Account recovery suggested.`, attemptsRemaining: 0 });
      } else {
        logEvent("CEREMONY_FAILED_ATTEMPT", false, `Incorrect credential attempt for ${ceremony.type}`, {
          acr: ceremony.requiredAcr
        });
        res.status(400).json({ error: `${message} Attempts remaining: ${ceremony.attemptsRemaining}.`, attemptsRemaining: ceremony.attemptsRemaining, retryable: true });
      }
    }
  });

  app.get("/api/ceremonies/:id/result", (req, res) => {
    const ceremony = ceremonies[req.params.id];
    if (!ceremony) {
      return res.status(404).json({ error: "Ceremony not found" });
    }
    res.json({
      ceremonyId: ceremony.id,
      state: ceremony.state,
      purpose: ceremony.purpose,
      achievedAcr: ceremony.achievedAcr,
      evidence: ceremony.evidence,
      subjectDisplayName: ceremony.subjectDisplayName
    });
  });

  // ==================== POLICY & ADMINISTRATION ====================
  app.get("/api/policies", (req, res) => {
    res.json({
      policies,
      activePolicyId
    });
  });

  app.post("/api/policies", (req, res) => {
    const { allowedMethods, requiredMethods, prohibitedMethods, attestationPolicy, algorithmPolicy, mfaGracePeriodDays, requireHardwareProtection } = req.body;
    
    const newPolicy: AuthenticatorPolicy = {
      id: `policy-v${policies.length + 1}`,
      version: policies.length + 1,
      isActive: false,
      allowedMethods: allowedMethods || [AuthenticatorEnum.PASSWORD_LOCAL],
      requiredMethods: requiredMethods || [],
      prohibitedMethods: prohibitedMethods || [],
      attestationPolicy: attestationPolicy || "none",
      algorithmPolicy: algorithmPolicy || ["ES256"],
      mfaGracePeriodDays: mfaGracePeriodDays || 7,
      requireHardwareProtection: !!requireHardwareProtection,
      updatedAt: new Date().toISOString(),
      updatedBy: "security-admin@tigrbl.internal"
    };

    policies.push(newPolicy);
    logEvent("POLICY_DRAFTED", true, `Drafted new authentication policy version: v${newPolicy.version}`);
    res.json({ success: true, policy: newPolicy });
  });

  app.post("/api/policies/activate/:id", (req, res) => {
    const policy = policies.find(p => p.id === req.params.id);
    if (!policy) {
      return res.status(404).json({ error: "Policy draft not found" });
    }

    policies.forEach(p => p.isActive = false);
    policy.isActive = true;
    activePolicyId = policy.id;

    logEvent("POLICY_ACTIVATED", true, `Activated authentication policy version: v${policy.version}`);
    res.json({ success: true, activePolicyId });
  });

  app.post("/api/policies/simulate", (req, res) => {
    const { allowedMethods, requireHardwareProtection } = req.body;

    // Simulate lockout impact for active users:
    // How many users would be locked out if we activated this policy?
    // Let's assume we have 100 registered users in the organization
    // Let's do a mock simulation:
    let affectedUsers = 0;
    const details: string[] = [];

    const hasPhishingResistant = allowedMethods.includes(AuthenticatorEnum.WEBAUTHN_LOCAL) || allowedMethods.includes(AuthenticatorEnum.MTLS_CLIENT_CERT);
    const hasPassword = allowedMethods.includes(AuthenticatorEnum.PASSWORD_LOCAL);

    if (!hasPassword && !hasPhishingResistant) {
      affectedUsers = 100;
      details.push("CRITICAL: Prohibiting both Passwords and Passkeys would lock out 100% of human users immediately.");
    } else if (requireHardwareProtection && !allowedMethods.includes(AuthenticatorEnum.WEBAUTHN_LOCAL)) {
      affectedUsers = 85;
      details.push("HIGH RISK: Requiring hardware protection without WebAuthn allowed locks out 85% of users without roaming keys.");
    } else if (!allowedMethods.includes(AuthenticatorEnum.PASSWORD_LOCAL)) {
      affectedUsers = 40;
      details.push("WARN: Disabling Password logins locks out 40% of users who have not enrolled FIDO2/WebAuthn factors.");
    } else {
      affectedUsers = 3;
      details.push("LOW RISK: Policy is highly backward-compatible. Only 3 users without compliant passwords are affected.");
    }

    res.json({
      affectedUsers,
      riskLevel: affectedUsers > 50 ? "CRITICAL" : (affectedUsers > 10 ? "HIGH" : "LOW"),
      details
    });
  });

  // ==================== IDENTITY MANAGEMENT ====================
  app.get("/api/identities/:identityId/authenticators", (req, res) => {
    // Admin projection: Redact actual secrets or code previews
    const adminProjection = authenticators.map(a => {
      const { metadata, ...rest } = a;
      return {
        ...rest,
        // Redact previews to prevent admin takeover
        metadata: metadata ? {
          ...metadata,
          codesPreview: undefined 
        } : undefined
      };
    });
    res.json({ authenticators: adminProjection });
  });

  app.post("/api/identities/:identityId/require-re-enrollment", (req, res) => {
    logEvent("ADMIN_FORCE_REENROLL", true, `Admin forced re-enrollment for identity: ${req.params.identityId}`);
    res.json({ success: true });
  });

  app.post("/api/identities/:identityId/authenticators/:id/suspend", (req, res) => {
    const auth = authenticators.find(a => a.id === req.params.id);
    if (!auth) {
      return res.status(404).json({ error: "Authenticator not found" });
    }
    auth.status = "suspended";
    logEvent("ADMIN_SUSPENDED_FACTOR", true, `Admin suspended factor: ${auth.name} for ${req.params.identityId}`, {
      authenticatorId: auth.id,
      authenticatorType: auth.type
    });
    res.json({ success: true, authenticator: auth });
  });

  app.post("/api/identities/:identityId/authenticators/:id/revoke", (req, res) => {
    const authIdx = authenticators.findIndex(a => a.id === req.params.id);
    if (authIdx === -1) {
      return res.status(404).json({ error: "Authenticator not found" });
    }
    const auth = authenticators[authIdx];
    authenticators.splice(authIdx, 1);
    logEvent("ADMIN_REVOKED_FACTOR", true, `Admin fully revoked factor: ${auth.name} for ${req.params.identityId}`, {
      authenticatorId: auth.id,
      authenticatorType: auth.type
    });
    res.json({ success: true });
  });

  app.post("/api/identities/:identityId/recovery/govern", (req, res) => {
    logEvent("ADMIN_INIT_GOVERNED_RECOVERY", true, `Admin initiated supervised/governed recovery flow for ${req.params.identityId}`);
    res.json({ 
      success: true, 
      governanceId: `gov-${Date.now()}`,
      instructions: "Temporary bypass token generated. Deliver code securely to verified physical recipient." 
    });
  });

  app.get("/api/audit-events", (req, res) => {
    res.json({ events: auditEvents });
  });

  // Vite and static asset configuration
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
    console.log(`[Tigrbl Backend] Server running on http://localhost:${PORT}`);
  });
}

startServer().catch(err => {
  console.error("Failed to start Tigrbl Server:", err);
});
