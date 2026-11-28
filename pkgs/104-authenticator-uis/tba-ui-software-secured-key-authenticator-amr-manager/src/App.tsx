import React, { useState } from 'react';
import {
  Shield,
  Key,
  Plus,
  Play,
  Lock,
  Unlock,
  AlertOctagon,
  AlertTriangle,
  Cpu,
  Info,
  CheckCircle,
  XCircle,
  Settings,
  HeartPulse,
  History,
  Code,
  Fingerprint
} from 'lucide-react';

import {
  KeyProfile,
  KeyProfileType,
  StorageClassification,
  SoftwareKeyCredential,
  KeyOriginPolicy,
  ProviderHealth,
  AuditEvent,
  ProofChallenge,
  ProofAssertion
} from './types';

// Import Custom Modular Components
import KeyBackingBadge from './components/KeyBackingBadge';
import SoftwareKeyPrivacyNotice from './components/SoftwareKeyPrivacyNotice';
import PublicKeySummary from './components/PublicKeySummary';
import KeyStorePicker, { KEYSTORE_OPTIONS } from './components/KeyStorePicker';
import KeyDependencyImpact from './components/KeyDependencyImpact';
import KeyRotationTimeline from './components/KeyRotationTimeline';
import OneTimeSecretReveal from './components/OneTimeSecretReveal';
import JwksEditor from './components/JwksEditor';
import PolicyImpactPreview from './components/PolicyImpactPreview';
import ValidationWorkbench from './components/ValidationWorkbench';
import ProviderHealthMonitor from './components/ProviderHealthMonitor';
import CliTooling from './components/CliTooling';
import CeremonyShell from './components/CeremonyShell';
import AuditDiagnostics from './components/AuditDiagnostics';

// Static Profiles List
const KEY_PROFILES: KeyProfile[] = [
  {
    id: 'passkey',
    name: 'FIDO Passkey (Software Profile)',
    description: 'User-present software-secured authenticator bound to WebAuthn browser client.',
    algorithms: ['ES256', 'EdDSA'],
    recommendedStore: 'macOS Keychain (CryptoKit)',
    intendedUse: 'User Authentication / SSO Session'
  },
  {
    id: 'dpop',
    name: 'Demonstration of Proof-of-Possession (DPoP)',
    description: 'Cryptographically binds OAuth 2.0 access and refresh tokens to local software-secured keys.',
    algorithms: ['ES256', 'RS256'],
    recommendedStore: 'macOS Keychain (CryptoKit)',
    intendedUse: 'OAuth API Token Sender Constraint'
  },
  {
    id: 'private_key_jwt',
    name: 'Private Key JWT Client Assertions',
    description: 'Automated software key assertions for system OIDC client authentication without client secrets.',
    algorithms: ['RS256', 'ES256'],
    recommendedStore: 'Linux Secret Service (systemd-creds)',
    intendedUse: 'Machine-to-Machine Client Authentication'
  },
  {
    id: 'signing',
    name: 'Cryptographic Payload Signer',
    description: 'Signs message bodies, database records, and critical operations metadata locally.',
    algorithms: ['EdDSA', 'ES256', 'RS256'],
    recommendedStore: 'Windows CNG',
    intendedUse: 'Integrity Check / Transaction Signatures'
  },
  {
    id: 'workload',
    name: 'Workload Identity Credential',
    description: 'Verifiable credentials for daemon processes running on dynamic container environments.',
    algorithms: ['ES256', 'EdDSA'],
    recommendedStore: 'CLI Secure Keyring (OpenSSL Engine)',
    intendedUse: 'Service-to-Service Workload Identity'
  }
];

// Initial active credentials list (Realistic Mock Data)
const INITIAL_CREDENTIALS: SoftwareKeyCredential[] = [
  {
    id: 'swk-dpop-99812',
    name: 'DPoP Gateway Assertor',
    profile: 'dpop',
    algorithm: 'ES256',
    keyStoreProvider: 'macOS Keychain (CryptoKit)',
    storageClass: 'software_secured',
    hasVerifiedEvidence: true,
    evidenceProvenance: 'OS Keystore Metadata Statement (v2)',
    publicKeyJwk: JSON.stringify({
      kty: "EC",
      use: "sig",
      alg: "ES256",
      crv: "P-256",
      x: "g8T_R3p1s-K4m89aL_oWp1t7vE",
      y: "y8Wp2q1m7_t5r9pK4o8v1t2e5",
      kid: "swk-dpop-99812"
    }, null, 2),
    fingerprint: 'SHA256:d8f1e5c2b0a99812f87a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e',
    status: 'active',
    backupPosture: 'blocked',
    exportPosture: 'blocked',
    createdAt: '2026-05-10T14:32:00Z',
    lastUsedAt: '2026-07-15T10:44:00Z',
    appScope: 'api.secured-keys.internal',
    dependencies: ['Internal-API-Gateway', 'OAuth-Token-Service']
  },
  {
    id: 'swk-pkjwt-44102',
    name: 'OIDC Client Authenticator',
    profile: 'private_key_jwt',
    algorithm: 'RS256',
    keyStoreProvider: 'Linux Secret Service',
    storageClass: 'software_secured',
    hasVerifiedEvidence: true,
    evidenceProvenance: 'Kernel LUKS Keyring Attestation',
    publicKeyJwk: JSON.stringify({
      kty: "RSA",
      use: "sig",
      alg: "RS256",
      n: "v9w-N2p5s-t1r7m8K4oO8w2t1e7q5m8_oWp1t",
      e: "AQAB",
      kid: "swk-pkjwt-44102"
    }, null, 2),
    fingerprint: 'SHA256:88fa22cb99eef1102ffaa771122bb33cc44dd55ee66ff778899aa00bb11cc22',
    status: 'active',
    backupPosture: 'permitted',
    exportPosture: 'blocked',
    createdAt: '2026-06-18T09:12:00Z',
    lastUsedAt: '2026-07-15T08:22:00Z',
    appScope: 'identity.auth-service.org',
    dependencies: ['Okta-Federator', 'IAM-Sync-Daemon']
  },
  {
    id: 'swk-unverified-7761',
    name: 'Legacy Dev Session Signer',
    profile: 'signing',
    algorithm: 'EdDSA',
    keyStoreProvider: 'Browser Session Keyring (IndexedDB)',
    storageClass: 'unknown',
    hasVerifiedEvidence: false,
    evidenceProvenance: 'None (Self-Asserted browser container)',
    publicKeyJwk: JSON.stringify({
      kty: "OKP",
      use: "sig",
      alg: "EdDSA",
      crv: "Ed25519",
      x: "a9_f2V1r8t4p9_k5m8_v1t2e",
      kid: "swk-unverified-7761"
    }, null, 2),
    fingerprint: 'SHA256:77a11bb22cc33dd44ee55ff66aa77bb88cc99dd00ee11ff22aa33bb44ee55ff',
    status: 'active',
    backupPosture: 'unverified',
    exportPosture: 'permitted',
    createdAt: '2026-07-01T11:00:00Z',
    lastUsedAt: '2026-07-14T23:55:00Z',
    appScope: 'development.localhost',
    dependencies: ['Local-Dev-Gateway']
  }
];

// Initial Health status
const INITIAL_PROVIDERS: ProviderHealth[] = [
  {
    id: 'macos_keychain',
    name: 'macOS Keychain Driver (CryptoKit)',
    type: 'native',
    status: 'healthy',
    latencyMs: 12,
    lastChecked: '2026-07-15T10:50:00-07:00',
    version: '2.4.1'
  },
  {
    id: 'windows_cng',
    name: 'Windows CNG Driver (NCrypt)',
    type: 'native',
    status: 'healthy',
    latencyMs: 18,
    lastChecked: '2026-07-15T10:50:00-07:00',
    version: '4.0.0'
  },
  {
    id: 'linux_systemd',
    name: 'Linux Secret Service (systemd-creds)',
    type: 'native',
    status: 'healthy',
    latencyMs: 8,
    lastChecked: '2026-07-15T10:50:00-07:00',
    version: '252.4'
  },
  {
    id: 'jwt_validator',
    name: 'JWT Signature Validator Service',
    type: 'validator',
    status: 'healthy',
    latencyMs: 44,
    lastChecked: '2026-07-15T10:50:00-07:00',
    version: '1.8.2'
  }
];

// Initial Policy settings
const INITIAL_POLICY: KeyOriginPolicy = {
  allowedStores: ['macos_keychain', 'windows_cng', 'linux_systemd', 'openssl_cli'],
  allowedAlgorithms: ['ES256', 'EdDSA', 'RS256'],
  backupPolicy: 'block',
  exportPolicy: 'block',
  requireEnclaveClassification: false,
  minKeyLength: 256,
  appScopeDefault: 'api.secured-keys.internal'
};

// Initial audit logs
const INITIAL_AUDIT_LOGS: AuditEvent[] = [
  {
    id: 'evt-1',
    timestamp: '2026-07-15T08:00:00Z',
    eventType: 'policy_change',
    actor: 'admin@secured-keys.org',
    profile: 'signing',
    storageClass: 'software_secured',
    evidenceVerified: true,
    details: 'Key origin policy updated to block unverified browser key storage for production scopes.',
    hash: '0x8f2c3d1e4a5b6c7d8e9f'
  },
  {
    id: 'evt-2',
    timestamp: '2026-07-15T09:12:00Z',
    eventType: 'registration',
    actor: 'iam-agent-prod-01',
    profile: 'private_key_jwt',
    storageClass: 'software_secured',
    evidenceVerified: true,
    details: 'Registered new Linux systemd-creds client key "OIDC Client Authenticator" with verified kernel attestation.',
    hash: '0x3c4d5e6f7a8b9c0d1e2f'
  },
  {
    id: 'evt-3',
    timestamp: '2026-07-15T10:44:00Z',
    eventType: 'verification',
    actor: 'billing-applet-user',
    profile: 'dpop',
    storageClass: 'software_secured',
    evidenceVerified: true,
    details: 'Signature verification passed on /api/v1/payments endpoint. Bound client token verified.',
    hash: '0x1a2b3c4d5e6f7a8b9c0d'
  }
];

export default function App() {
  // Navigation
  const [workspace, setWorkspace] = useState<'p0_auth' | 'p1_enroll' | 'p2_policy' | 'cli_emulator'>('p0_auth');

  // Application Data States
  const [credentials, setCredentials] = useState<SoftwareKeyCredential[]>(INITIAL_CREDENTIALS);
  const [policy, setPolicy] = useState<KeyOriginPolicy>(INITIAL_POLICY);
  const [providers, setProviders] = useState<ProviderHealth[]>(INITIAL_PROVIDERS);
  const [auditLogs, setAuditLogs] = useState<AuditEvent[]>(INITIAL_AUDIT_LOGS);

  // Detail View State
  const [selectedCredentialId, setSelectedCredentialId] = useState<string>(INITIAL_CREDENTIALS[0].id);
  const activeCredential = credentials.find((c) => c.id === selectedCredentialId) || credentials[0];

  // Failure simulation configurations
  const [simulateLockedKeystore, setSimulateLockedKeystore] = useState(false);
  const [simulateStaleProof, setSimulateStaleProof] = useState(false);
  const [simulateReplayAttack, setSimulateReplayAttack] = useState(false);
  const [simulateWrongAlgorithm, setSimulateWrongAlgorithm] = useState(false);

  // Enrollment Wizard state
  const [enrollStep, setEnrollStep] = useState(0);
  const [enrollProfile, setEnrollProfile] = useState<KeyProfileType>('dpop');
  const [enrollKeystore, setEnrollKeystore] = useState('macos_keychain');
  const [enrollKeyName, setEnrollKeyName] = useState('Billing Token Signer');
  const [enrollAlgorithm, setEnrollAlgorithm] = useState('ES256');
  const [enrollAppScope, setEnrollAppScope] = useState('api.billing-system.internal');
  const [isSimulatingEnrollAuth, setIsSimulatingEnrollAuth] = useState(false);
  const [enrollError, setEnrollError] = useState<string | null>(null);
  const [oneTimeSecret, setOneTimeSecret] = useState<string | null>(null);

  // Runtime Proof Ceremony state
  const [proofStep, setProofStep] = useState(0); // 0: Select, 1: Challenge, 2: Sign, 3: Result
  const [proofChallenge, setProofChallenge] = useState<ProofChallenge | null>(null);
  const [proofAssertion, setProofAssertion] = useState<ProofAssertion | null>(null);
  const [isSimulatingProofAuth, setIsSimulatingProofAuth] = useState(false);
  const [proofError, setProofError] = useState<string | null>(null);

  // Key Rotation simulation state
  const [rotationStage, setRotationStage] = useState<number>(0); 

  // Handlers for registering public custom keys from JWKS Editor
  const handleAddJwkToRegistry = (jwk: any) => {
    const kid = jwk.kid || `swk-${Math.floor(Math.random() * 90000)}`;
    const newCredential: SoftwareKeyCredential = {
      id: kid,
      name: `Deregistered JWK - ${kid}`,
      profile: 'signing',
      algorithm: jwk.alg || 'RS256',
      keyStoreProvider: 'CLI Secure Keyring (OpenSSL Engine)',
      storageClass: 'software_secured',
      hasVerifiedEvidence: true,
      evidenceProvenance: 'JWKS Upload Verification Attestation',
      publicKeyJwk: JSON.stringify(jwk, null, 2),
      fingerprint: 'SHA256:custom-jwk-upload-material-fingerprint-digest-abc',
      status: 'active',
      backupPosture: 'unverified',
      exportPosture: 'permitted',
      createdAt: new Date().toISOString(),
      lastUsedAt: new Date().toISOString(),
      appScope: 'unbounded.scope',
      dependencies: ['External-Client-Workload']
    };

    setCredentials([newCredential, ...credentials]);
    addAuditEvent('registration', 'system-gateway', 'signing', 'software_secured', true, `Imported custom JWK ${kid} into server JWKS registry.`);
  };

  const handleRemoveJwkFromRegistry = (kid: string) => {
    setCredentials(credentials.filter((c) => c.id !== kid));
    addAuditEvent('compromise', 'admin-console', 'signing', 'unknown', false, `Deregistered key ${kid} from server JWKS registry.`);
  };

  // Helper to add audit logs
  const addAuditEvent = (
    eventType: string,
    actor: string,
    profile: string,
    storageClass: StorageClassification,
    evidenceVerified: boolean,
    details: string
  ) => {
    const newEvent: AuditEvent = {
      id: `evt-${Date.now()}`,
      timestamp: new Date().toISOString(),
      eventType,
      actor,
      profile,
      storageClass,
      evidenceVerified,
      details,
      hash: `0x${Math.random().toString(16).substring(2, 12)}${Math.random().toString(16).substring(2, 12)}`
    };
    setAuditLogs((prev) => [newEvent, ...prev]);
  };

  // Provider health toggler
  const handleToggleProviderHealth = (id: string) => {
    setProviders((prev) =>
      prev.map((p) => {
        if (p.id === id) {
          const nextStatusMap: Record<'healthy' | 'degraded' | 'unavailable', 'healthy' | 'degraded' | 'unavailable'> = {
            healthy: 'degraded',
            degraded: 'unavailable',
            unavailable: 'healthy'
          };
          const nextStatus = nextStatusMap[p.status];
          const nextLatency = nextStatus === 'healthy' ? 12 : nextStatus === 'degraded' ? 152 : 999;

          addAuditEvent(
            'policy_change',
            'health-sensor-daemon',
            'workload',
            'software_secured',
            true,
            `Keystore provider health for "${p.name}" changed to ${nextStatus.toUpperCase()} (Latency: ${nextLatency}ms)`
          );

          return {
            ...p,
            status: nextStatus,
            latencyMs: nextLatency,
            lastChecked: new Date().toISOString()
          };
        }
        return p;
      })
    );
  };

  const handleRefreshHealthAll = () => {
    setProviders((prev) =>
      prev.map((p) => ({
        ...p,
        latencyMs: p.status === 'healthy' ? Math.floor(Math.random() * 20 + 5) : p.status === 'degraded' ? Math.floor(Math.random() * 100 + 120) : 999,
        lastChecked: new Date().toISOString()
      }))
    );
  };

  // Compromise / Revocation logic
  const handleCompromiseKey = (id: string) => {
    setCredentials((prev) =>
      prev.map((c) => {
        if (c.id === id) {
          addAuditEvent(
            'compromise',
            'security-officer',
            c.profile,
            c.storageClass,
            c.hasVerifiedEvidence,
            `CRITICAL: Marked key "${c.name}" (${c.id}) as COMPROMISED. Dependent apps locked down immediately.`
          );
          return { ...c, status: 'compromised' };
        }
        return c;
      })
    );
  };

  const handleRevokeKey = (id: string) => {
    setCredentials((prev) =>
      prev.map((c) => {
        if (c.id === id) {
          addAuditEvent(
            'compromise',
            'security-officer',
            c.profile,
            c.storageClass,
            c.hasVerifiedEvidence,
            `REVOCATION: Key "${c.name}" (${c.id}) is explicitly revoked and retired.`
          );
          return { ...c, status: 'revoked' };
        }
        return c;
      })
    );
  };

  // Rotation Actions
  const handleRotationAdvance = () => {
    if (rotationStage === 0) {
      setRotationStage(1);
      addAuditEvent('rotation', 'ops-manager', 'dpop', 'software_secured', true, 'Initiated overlapping rotation sequence for gateway DPoP key. Phase 1: Overlap Key generated.');
    } else if (rotationStage === 1) {
      setRotationStage(2);
      addAuditEvent('rotation', 'ops-manager', 'dpop', 'software_secured', true, 'Phase 2: Completed server challenge-response ownership proof for replacement gateway key.');
    } else if (rotationStage === 2) {
      setRotationStage(3);
      addAuditEvent('rotation', 'ops-manager', 'dpop', 'software_secured', true, 'Phase 3: Commenced traffic verification. Routing 10% of signature telemetry to new key.');
    } else if (rotationStage === 3) {
      setRotationStage(4);
      setCredentials((prev) =>
        prev.map((c) => {
          if (c.id === 'swk-dpop-99812') {
            return {
              ...c,
              name: 'DPoP Gateway Assertor (Retired)',
              status: 'revoked',
              lastUsedAt: new Date().toISOString()
            };
          }
          return c;
        })
      );
      const newRotatedKey: SoftwareKeyCredential = {
        id: 'swk-dpop-v2-active',
        name: 'DPoP Gateway Assertor v2',
        profile: 'dpop',
        algorithm: 'ES256',
        keyStoreProvider: 'macOS Keychain (CryptoKit)',
        storageClass: 'software_secured',
        hasVerifiedEvidence: true,
        evidenceProvenance: 'OS Keystore Metadata Statement (v2)',
        publicKeyJwk: JSON.stringify({
          kty: "EC",
          use: "sig",
          alg: "ES256",
          crv: "P-256",
          x: "k3D_R4q8s_F1m99oP_vQt3v9e",
          y: "a2Sp9q1b7_z5r1pK5o8w2t3e9",
          kid: "swk-dpop-v2-active"
        }, null, 2),
        fingerprint: 'SHA256:abcd-rotated-fingerprint-for-evidence-provenance-es256',
        status: 'active',
        backupPosture: 'blocked',
        exportPosture: 'blocked',
        createdAt: new Date().toISOString(),
        lastUsedAt: new Date().toISOString(),
        appScope: 'api.secured-keys.internal',
        dependencies: ['Internal-API-Gateway', 'OAuth-Token-Service']
      };
      setCredentials((prev) => [newRotatedKey, ...prev]);
      setSelectedCredentialId(newRotatedKey.id);

      addAuditEvent('rotation', 'ops-manager', 'dpop', 'software_secured', true, 'Phase 4: Explicit retirement complete. Original DPoP key retired, v2 replacement fully active.');
    }
  };

  const handleRotationReset = () => {
    setRotationStage(0);
    setCredentials((prev) => {
      const filtered = prev.filter((c) => c.id !== 'swk-dpop-v2-active');
      return filtered.map((c) => {
        if (c.id === 'swk-dpop-99812') {
          return {
            ...c,
            name: 'DPoP Gateway Assertor',
            status: 'active'
          };
        }
        return c;
      });
    });
    setSelectedCredentialId('swk-dpop-99812');
  };

  // ENROLLMENT WIZARD ACTIONS
  const handleEnrollStepAdvance = () => {
    setEnrollError(null);

    if (enrollStep === 0) {
      setEnrollStep(1);
    } else if (enrollStep === 1) {
      setEnrollStep(2);
    } else if (enrollStep === 2) {
      setEnrollStep(3);
    } else if (enrollStep === 3) {
      setIsSimulatingEnrollAuth(true);
    } else if (enrollStep === 4) {
      const keyId = `swk-${enrollProfile}-${Math.floor(Math.random() * 90000 + 10000)}`;
      const selectedKeystoreObj = KEYSTORE_OPTIONS.find((k) => k.id === enrollKeystore);

      const isStoreSecured = selectedKeystoreObj?.isSoftwareSecured || false;
      const verifiedEvidence = isStoreSecured && enrollKeystore !== 'unverified_browser';

      const newKey: SoftwareKeyCredential = {
        id: keyId,
        name: enrollKeyName,
        profile: enrollProfile,
        algorithm: enrollAlgorithm,
        keyStoreProvider: selectedKeystoreObj?.name || 'Unknown Keystore',
        storageClass: isStoreSecured ? 'software_secured' : 'unknown',
        hasVerifiedEvidence: verifiedEvidence,
        evidenceProvenance: selectedKeystoreObj?.evidenceModel || 'Self-Asserted Key Attestation',
        publicKeyJwk: JSON.stringify({
          kty: enrollAlgorithm === 'RS256' ? 'RSA' : 'EC',
          use: 'sig',
          alg: enrollAlgorithm,
          kid: keyId,
          ...(enrollAlgorithm === 'ES256' ? { crv: 'P-256', x: 'g8T_R3p1s-K4m89aL_oWp1t7vE', y: 'y8Wp2q1m7_t5r9pK4o8v1t2e5' } : {})
        }, null, 2),
        fingerprint: `SHA256:${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`,
        status: 'active',
        backupPosture: enrollKeystore === 'macos_keychain' ? 'blocked' : 'permitted',
        exportPosture: enrollKeystore === 'openssl_cli' ? 'permitted' : 'blocked',
        createdAt: new Date().toISOString(),
        lastUsedAt: new Date().toISOString(),
        appScope: enrollAppScope,
        dependencies: ['Dynamic-Gateway-Integration']
      };

      setCredentials((prev) => [newKey, ...prev]);
      setSelectedCredentialId(keyId);

      const code = `RECOVERY-${Math.floor(Math.random() * 900000 + 100000)}-${enrollProfile.toUpperCase()}`;
      setOneTimeSecret(code);

      addAuditEvent(
        'registration',
        'operator-web',
        enrollProfile,
        newKey.storageClass,
        newKey.hasVerifiedEvidence,
        `Enrolled new software key "${newKey.name}" via ${newKey.keyStoreProvider}. Evidence verification classification: ${newKey.hasVerifiedEvidence ? 'swk verified' : 'backing unverified'}.`
      );

      setEnrollStep(5);
    }
  };

  const handleEnrollAuthSuccess = () => {
    setIsSimulatingEnrollAuth(false);
    setEnrollStep(4);
  };

  const handleEnrollAuthFail = () => {
    setIsSimulatingEnrollAuth(false);
    setEnrollError('Native OS keystore authorization denied by user. Private key generation aborted.');
  };

  const handleResetEnrollment = () => {
    setEnrollStep(0);
    setEnrollError(null);
    setOneTimeSecret(null);
  };

  // RUNTIME PROOF CEREMONY ACTIONS
  const handleStartProofCeremony = () => {
    setProofError(null);
    setProofStep(0);

    const activeProviderObj = providers.find((p) =>
      (activeCredential.keyStoreProvider.includes('macOS') && p.id === 'macos_keychain') ||
      (activeCredential.keyStoreProvider.includes('Windows') && p.id === 'windows_cng') ||
      (activeCredential.keyStoreProvider.includes('Linux') && p.id === 'linux_systemd') ||
      (activeCredential.keyStoreProvider.includes('Browser') && p.id === 'jwt_validator')
    );

    if (activeProviderObj && activeProviderObj.status === 'unavailable') {
      setProofError(`Outage detected: Keystore provider ${activeProviderObj.name} is currently offline. Verification aborted.`);
      return;
    }

    const challenge: ProofChallenge = {
      purpose: 'API access token confirmation step-up',
      endpoint: `https://${activeCredential.appScope}/v1/transfer`,
      nonce: `nonce-${Math.floor(Math.random() * 900000 + 100000)}`,
      audience: `https://${activeCredential.appScope}`,
      timestamp: new Date().toISOString(),
      algorithm: activeCredential.algorithm
    };

    setProofChallenge(challenge);
    setProofStep(1);
    addAuditEvent('verification', 'server-gateway', activeCredential.profile, activeCredential.storageClass, activeCredential.hasVerifiedEvidence, `Issued bound challenge nonce ${challenge.nonce} for ${activeCredential.id}`);
  };

  const handleTriggerProofSign = () => {
    setProofError(null);
    setIsSimulatingProofAuth(true);
  };

  const handleProofAuthSuccess = () => {
    setIsSimulatingProofAuth(false);

    if (!proofChallenge) return;

    if (simulateLockedKeystore) {
      setProofError('Keystore locked or unavailable. Please unlock your local native OS vault and try again.');
      addAuditEvent('error', 'client-agent', activeCredential.profile, activeCredential.storageClass, activeCredential.hasVerifiedEvidence, `Signature generation failed: Keystore locked.`);
      return;
    }

    if (simulateWrongAlgorithm) {
      setProofError('Unsupported algorithm signature binding. Client signed with an unapproved cryptographic key type.');
      addAuditEvent('error', 'server-gateway', activeCredential.profile, activeCredential.storageClass, activeCredential.hasVerifiedEvidence, `Signature verification failed: Algorithm mismatch.`);
      return;
    }

    const assertion: ProofAssertion = {
      signature: `SIG_ECDSA_${Math.random().toString(36).substring(2, 15)}_${Math.random().toString(36).substring(2, 15)}`,
      nonce: simulateReplayAttack ? 'previously-processed-replay-nonce-88712' : proofChallenge.nonce,
      audience: proofChallenge.audience,
      algorithm: proofChallenge.algorithm,
      timestamp: simulateStaleProof ? '2026-07-15T01:00:00Z' : new Date().toISOString(),
      evidenceToken: `EVID_JWT_SWK_${Math.random().toString(36).substring(4, 12)}`,
      status: 'valid'
    };

    setProofAssertion(assertion);
    setProofStep(2);
  };

  const handleProofAuthFail = () => {
    setIsSimulatingProofAuth(false);
    setProofError('Authorization denied. Operating system keystore signature request was declined by the user.');
    addAuditEvent('error', 'client-agent', activeCredential.profile, activeCredential.storageClass, activeCredential.hasVerifiedEvidence, `Signature generation denied by user.`);
  };

  const handleSubmitProofAssertion = () => {
    if (!proofAssertion || !proofChallenge) return;

    setProofStep(3);

    let finalStatus: ProofAssertion['status'] = 'valid';

    if (simulateReplayAttack) {
      finalStatus = 'replay_rejected';
    } else if (simulateStaleProof) {
      finalStatus = 'stale';
    }

    const updatedAssertion = {
      ...proofAssertion,
      status: finalStatus
    };

    setProofAssertion(updatedAssertion);

    const isSuccess = finalStatus === 'valid';
    const amrVerified = isSuccess && activeCredential.storageClass === 'software_secured' && activeCredential.hasVerifiedEvidence;

    addAuditEvent(
      isSuccess ? 'verification' : 'error',
      'server-gateway',
      activeCredential.profile,
      activeCredential.storageClass,
      amrVerified,
      isSuccess
        ? `Cryptographic proof assertion verified successfully for endpoint ${proofChallenge.endpoint}. Bound AMR: swk.`
        : `Cryptographic proof assertion rejected. Failure reason: ${finalStatus.toUpperCase()}`
    );

    if (isSuccess) {
      setCredentials((prev) =>
        prev.map((c) => {
          if (c.id === activeCredential.id) {
            return {
              ...c,
              lastUsedAt: new Date().toISOString()
            };
          }
          return c;
        })
      );
    }
  };

  const handleResetProofCeremony = () => {
    setProofStep(0);
    setProofChallenge(null);
    setProofAssertion(null);
    setProofError(null);
  };

  return (
    <div id="app-root" className="min-h-screen bg-slate-900 text-slate-100 font-sans antialiased flex flex-col">
      {/* Background ambient glow */}
      <div className="absolute top-0 left-0 right-0 h-[500px] bg-gradient-to-b from-indigo-950/40 via-slate-900/0 to-transparent pointer-events-none z-0" />

      {/* Top Bar Header */}
      <header className="relative z-10 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-600 text-white rounded-xl shadow-lg ring-4 ring-indigo-500/10">
              <Key className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-bold text-slate-100 tracking-tight leading-none">Software-Secured Key AMR Workspace</h1>
                <span className="px-2 py-0.5 rounded-full text-[9px] font-bold bg-indigo-950 text-indigo-400 border border-indigo-900 uppercase">
                  swk Core v1.2
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">Evidence-driven cryptographic origin protection and step-up ceremonies</p>
            </div>
          </div>

          <div className="flex items-center gap-3.5 bg-slate-950/60 rounded-xl px-4 py-2 border border-slate-800 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span className="text-slate-400 font-medium">Tenant Guard:</span>
              <span className="text-emerald-400 font-bold uppercase tracking-wider font-mono">ACTIVE</span>
            </div>
            <div className="w-px h-4 bg-slate-800" />
            <div className="text-slate-400">
              Assurance Model: <span className="text-indigo-400 font-semibold uppercase font-mono text-[10px]">swk-attested</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col lg:flex-row gap-6">
        {/* Navigation Sidebar & Credentials Tree */}
        <section className="w-full lg:w-[320px] shrink-0 space-y-6">
          <div className="bg-slate-950/40 border border-slate-800 rounded-2xl p-4 space-y-2.5">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block px-1">
              Workspace Scope
            </span>

            <nav className="space-y-1">
              <button
                onClick={() => setWorkspace('p0_auth')}
                id="nav-p0"
                className={`w-full flex items-center justify-between p-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  workspace === 'p0_auth'
                    ? 'bg-indigo-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Lock className="w-4 h-4 shrink-0" />
                  <span>P0 - Runtime Proofs</span>
                </div>
                <span className={`px-1.5 py-0.5 rounded text-[9px] font-extrabold ${workspace === 'p0_auth' ? 'bg-indigo-750 text-white' : 'bg-slate-800 text-slate-400'}`}>
                  PRIORITY
                </span>
              </button>

              <button
                onClick={() => setWorkspace('p1_enroll')}
                id="nav-p1"
                className={`w-full flex items-center justify-between p-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  workspace === 'p1_enroll'
                    ? 'bg-indigo-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Plus className="w-4 h-4 shrink-0" />
                  <span>P1 - Enrollment & Lifecycles</span>
                </div>
              </button>

              <button
                onClick={() => setWorkspace('p2_policy')}
                id="nav-p2"
                className={`w-full flex items-center justify-between p-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  workspace === 'p2_policy'
                    ? 'bg-indigo-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Settings className="w-4 h-4 shrink-0" />
                  <span>P2 - Governance & Ops</span>
                </div>
              </button>

              <button
                onClick={() => setWorkspace('cli_emulator')}
                id="nav-cli"
                className={`w-full flex items-center justify-between p-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  workspace === 'cli_emulator'
                    ? 'bg-indigo-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Code className="w-4 h-4 shrink-0" />
                  <span>CLI & SDK Sandbox</span>
                </div>
              </button>
            </nav>
          </div>

          <div className="bg-slate-950/40 border border-slate-800 rounded-2xl p-4 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                Active Software Keys ({credentials.length})
              </span>
              <button
                onClick={() => {
                  setWorkspace('p1_enroll');
                  setEnrollStep(0);
                }}
                className="text-[10px] text-indigo-400 hover:text-indigo-300 font-bold flex items-center gap-0.5 p-1 transition-colors"
              >
                <Plus className="w-3.5 h-3.5" /> Enrolled
              </button>
            </div>

            <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-1">
              {credentials.map((cred) => {
                const isSelected = cred.id === selectedCredentialId;
                const isCompromised = cred.status === 'compromised';
                const isRevoked = cred.status === 'revoked';

                return (
                  <button
                    key={cred.id}
                    id={`cred-card-item-${cred.id}`}
                    onClick={() => setSelectedCredentialId(cred.id)}
                    className={`w-full text-left p-3 rounded-xl border transition-all relative ${
                      isSelected
                        ? 'bg-indigo-950/45 border-indigo-500/80 ring-1 ring-indigo-500/20'
                        : 'bg-slate-900/60 border-slate-800/80 hover:border-slate-700 hover:bg-slate-800/30'
                    }`}
                  >
                    <span className={`absolute top-3.5 right-3 w-1.5 h-1.5 rounded-full ${
                      isCompromised ? 'bg-rose-500 animate-ping' : isRevoked ? 'bg-slate-500' : 'bg-emerald-500'
                    }`} />

                    <div className="space-y-1.5">
                      <div className="pr-4">
                        <span className={`font-bold text-xs truncate block ${
                          isCompromised ? 'text-rose-400 line-through' : isRevoked ? 'text-slate-400 line-through' : 'text-slate-200'
                        }`}>
                          {cred.name}
                        </span>
                        <span className="text-[10px] text-slate-400 block font-mono mt-0.5">
                          id: {cred.id}
                        </span>
                      </div>

                      <div className="flex items-center gap-1">
                        <KeyBackingBadge
                          storageClass={cred.storageClass}
                          hasVerifiedEvidence={cred.hasVerifiedEvidence}
                          className="scale-90 origin-left py-0 px-1.5 font-bold"
                        />
                        {isCompromised && (
                          <span className="bg-rose-950/80 text-rose-400 text-[8px] font-extrabold uppercase px-1 rounded border border-rose-900">
                            Compromised
                          </span>
                        )}
                        {isRevoked && (
                          <span className="bg-slate-800 text-slate-400 text-[8px] font-extrabold uppercase px-1 rounded border border-slate-700">
                            Revoked
                          </span>
                        )}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </section>

        {/* Center Content Viewport */}
        <section className="flex-1 space-y-6">
          {workspace === 'p0_auth' && (
            <div className="space-y-6">
              <div className="bg-indigo-950/30 border border-indigo-900/50 p-4.5 rounded-2xl flex items-start gap-3.5 text-xs">
                <div className="p-2 bg-indigo-600/15 text-indigo-400 rounded-lg shrink-0">
                  <Fingerprint className="w-5 h-5" />
                </div>
                <div className="space-y-1">
                  <h4 className="font-bold text-slate-200">Runtime Client Signature Proof Ceremony (P0)</h4>
                  <p className="text-slate-400 leading-relaxed">
                    Test how server gateways verify evidence-based client signatures in real time. Choose an active key from the sidebar inventory, request a bound challenge nonce, sign, and submit. Use simulation toggles to test various cryptographic failure pathways.
                  </p>
                </div>
              </div>

              <CeremonyShell
                title="Audience-Bound Signature & Proof Ceremony"
                subtitle="Challenge-response authentication enforcing software-key possession evidence"
                steps={['Challenge Request', 'OS Keystore Authorize', 'Verify Signature Assertion', 'Evidence Established']}
                currentStep={proofStep}
                isSimulatingNativeAuth={isSimulatingProofAuth}
                onSimulateAuthSuccess={handleProofAuthSuccess}
                onSimulateAuthFail={handleProofAuthFail}
              >
                <div className="space-y-5 text-slate-800">
                  {proofStep === 0 && (
                    <div className="space-y-4">
                      <div className="p-4.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block">Selected Credential Summary</span>
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-bold text-slate-800">{activeCredential.name}</span>
                          <KeyBackingBadge
                            storageClass={activeCredential.storageClass}
                            hasVerifiedEvidence={activeCredential.hasVerifiedEvidence}
                          />
                        </div>
                        <div className="text-xs text-slate-500 font-mono space-y-1 pt-1.5 border-t border-slate-200/60">
                          <div>Provider : {activeCredential.keyStoreProvider}</div>
                          <div>Algorithm: {activeCredential.algorithm}</div>
                          <div>Scope    : {activeCredential.appScope}</div>
                        </div>
                      </div>

                      {activeCredential.status === 'compromised' && (
                        <div className="bg-rose-50 border border-rose-200 text-rose-800 p-3 rounded-lg flex gap-2 text-xs">
                          <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                          <span>This key is flagged as <strong>COMPROMISED</strong>. Server validators will refuse to issue challenges for compromised keys. Please choose another key or run recovery.</span>
                        </div>
                      )}

                      {activeCredential.status === 'revoked' && (
                        <div className="bg-slate-100 border border-slate-200 text-slate-700 p-3 rounded-lg flex gap-2 text-xs">
                          <AlertTriangle className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                          <span>This key is marked <strong>REVOKED</strong>. Active authentications cannot be initiated.</span>
                        </div>
                      )}

                      {proofError && (
                        <div id="proof-error-banner" className="bg-rose-50 border border-rose-200 text-rose-800 p-3 rounded-lg flex gap-2 text-xs">
                          <XCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                          <span>{proofError}</span>
                        </div>
                      )}

                      <div className="flex justify-end pt-2">
                        <button
                          type="button"
                          id="btn-trigger-proof-start"
                          onClick={handleStartProofCeremony}
                          disabled={activeCredential.status !== 'active'}
                          className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-colors flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
                        >
                          <Play className="w-4 h-4" />
                          Request Server bound challenge Nonce
                        </button>
                      </div>
                    </div>
                  )}

                  {proofStep === 1 && proofChallenge && (
                    <div className="space-y-4">
                      <div className="space-y-1">
                        <h4 className="font-bold text-slate-800 text-sm">Step 1: Challenge Nonce Received</h4>
                        <p className="text-xs text-slate-500">
                          The server issued an audience-bound, cryptographically signed payload challenge.
                        </p>
                      </div>

                      <pre className="p-3.5 bg-slate-900 text-slate-200 rounded-xl font-mono text-xs leading-relaxed border border-slate-800 overflow-x-auto">
                        {JSON.stringify(proofChallenge, null, 2)}
                      </pre>

                      {proofError && (
                        <div className="bg-rose-50 border border-rose-200 text-rose-800 p-3 rounded-lg flex gap-2 text-xs">
                          <XCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                          <span>{proofError}</span>
                        </div>
                      )}

                      <div className="bg-slate-50 border border-slate-200 p-3.5 rounded-xl space-y-2.5">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Inject Cryptographic Failure / Anomaly</span>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                          <label className="flex items-center gap-1.5 p-2 bg-white border border-slate-200 rounded-lg text-xs cursor-pointer select-none">
                            <input
                              type="checkbox"
                              checked={simulateLockedKeystore}
                              onChange={(e) => setSimulateLockedKeystore(e.target.checked)}
                              className="accent-indigo-600"
                            />
                            <span>Lock Keystore</span>
                          </label>
                          <label className="flex items-center gap-1.5 p-2 bg-white border border-slate-200 rounded-lg text-xs cursor-pointer select-none">
                            <input
                              type="checkbox"
                              checked={simulateStaleProof}
                              onChange={(e) => setSimulateStaleProof(e.target.checked)}
                              className="accent-indigo-600"
                            />
                            <span>Stale (Expired)</span>
                          </label>
                          <label className="flex items-center gap-1.5 p-2 bg-white border border-slate-200 rounded-lg text-xs cursor-pointer select-none">
                            <input
                              type="checkbox"
                              checked={simulateReplayAttack}
                              onChange={(e) => setSimulateReplayAttack(e.target.checked)}
                              className="accent-indigo-600"
                            />
                            <span>Replay Attack</span>
                          </label>
                          <label className="flex items-center gap-1.5 p-2 bg-white border border-slate-200 rounded-lg text-xs cursor-pointer select-none">
                            <input
                              type="checkbox"
                              checked={simulateWrongAlgorithm}
                              onChange={(e) => setSimulateWrongAlgorithm(e.target.checked)}
                              className="accent-indigo-600"
                            />
                            <span>Alg Mismatch</span>
                          </label>
                        </div>
                      </div>

                      <div className="flex gap-2.5 justify-between pt-2">
                        <button
                          type="button"
                          onClick={handleResetProofCeremony}
                          className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Cancel
                        </button>
                        <button
                          type="button"
                          id="btn-sign-proof"
                          onClick={handleTriggerProofSign}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-xl text-xs transition-colors flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
                        >
                          Authorize & Sign Signature Assertion
                        </button>
                      </div>
                    </div>
                  )}

                  {proofStep === 2 && proofAssertion && (
                    <div className="space-y-4">
                      <div className="space-y-1">
                        <h4 className="font-bold text-slate-800 text-sm">Step 2: Sign-off Complete</h4>
                        <p className="text-xs text-slate-500">
                          Your local OS Keystore successfully authorized access and generated the audience-bound assertion.
                        </p>
                      </div>

                      <pre className="p-3.5 bg-slate-900 text-slate-200 rounded-xl font-mono text-xs leading-relaxed border border-slate-800 overflow-x-auto">
                        {JSON.stringify(proofAssertion, null, 2)}
                      </pre>

                      <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-800 flex gap-2">
                        <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                        <span>The private key is bound locally and was not exported. Only the dynamic cryptographic assertion is submitted to the server gateway.</span>
                      </div>

                      <div className="flex gap-2.5 justify-end pt-2">
                        <button
                          type="button"
                          id="btn-submit-assertion-to-server"
                          onClick={handleSubmitProofAssertion}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-colors flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
                        >
                          Submit Cryptographic Assertion
                        </button>
                      </div>
                    </div>
                  )}

                  {proofStep === 3 && proofAssertion && (
                    <div className="space-y-4">
                      <div className="space-y-1">
                        <h4 className="font-bold text-slate-800 text-sm">Step 3: Server Verification Response</h4>
                        <p className="text-xs text-slate-500 font-medium">
                          Gateway processed and authenticated the signature bounds.
                        </p>
                      </div>

                      {proofAssertion.status === 'valid' ? (
                        <div className="space-y-3">
                          <div id="proof-success-banner" className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 space-y-2 text-xs">
                            <div className="flex items-center gap-2 font-bold text-emerald-900 text-sm">
                              <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
                              Cryptographic Evidence Verified!
                            </div>
                            <p className="leading-relaxed">
                              Server attestation check successfully validated signature bindings and classified the originating environment as <strong>Verified Software</strong>.
                            </p>
                            <div className="flex items-center gap-2 pt-2 border-t border-emerald-200/60 font-semibold">
                              <span>AMR Claim Assigned:</span>
                              <KeyBackingBadge
                                storageClass={activeCredential.storageClass}
                                hasVerifiedEvidence={activeCredential.hasVerifiedEvidence}
                              />
                            </div>
                          </div>

                          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1.5 font-mono">
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block font-sans mb-1">AMR EVIDENCE DETAIL</span>
                            <div>Provenance Classification: {activeCredential.evidenceProvenance}</div>
                            <div>Storage Boundary: isolated {activeCredential.storageClass} storage</div>
                            <div>Telemetry Freshness check: SUCCESS (42ms)</div>
                            <div>Replay analysis check: UNIQUE (Nonce unique)</div>
                            <div>Assurance verified timestamp: {new Date().toISOString()}</div>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-3">
                          <div id="proof-failure-banner" className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 space-y-2.5 text-xs">
                            <div className="flex items-center gap-2 font-bold text-rose-900 text-sm">
                              <XCircle className="w-5 h-5 text-rose-600 shrink-0" />
                              Authentication Proof Rejected!
                            </div>
                            <p className="leading-relaxed">
                              {proofAssertion.status === 'replay_rejected' && 'The server rejected this assertion because the challenge nonce has already been utilized. This is typical of a cryptographic replay attack.'}
                              {proofAssertion.status === 'stale' && 'The cryptographic bound assertion expired or has a stale timestamp block.'}
                            </p>

                            <div className="bg-white border border-rose-100 rounded-lg p-3 text-[11px] leading-relaxed text-rose-900 space-y-1.5 font-sans">
                              <strong className="font-bold text-rose-950 uppercase tracking-wide block mb-1">Recommended Recovery Path:</strong>
                              <p>Since this authentication assertion has failed strict compliance, the gateway advises executing the following safeguards:</p>
                              <ul className="list-disc pl-4 space-y-0.5">
                                <li>Initiate a newly-generated key enrollment to replace old bindings</li>
                                <li>Revoke and audit credentials for exfiltration signs</li>
                                <li>Use fallback Human Multi-Factor Recovery pathways</li>
                              </ul>
                            </div>
                          </div>

                          <div className="flex gap-2.5 justify-end">
                            <button
                              type="button"
                              onClick={() => {
                                setWorkspace('p1_enroll');
                                setEnrollStep(0);
                              }}
                              className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                            >
                              Reprovision New Key
                            </button>
                          </div>
                        </div>
                      )}

                      <div className="flex justify-end pt-2 border-t border-slate-100">
                        <button
                          type="button"
                          onClick={handleResetProofCeremony}
                          className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Complete and Dismiss
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </CeremonyShell>
            </div>
          )}

          {workspace === 'p1_enroll' && (
            <div className="space-y-6">
              <CeremonyShell
                title="First-Party Software-Key Enrollment Ceremony"
                subtitle="Ceremonial creation, local binding, possession proof and gateway activation"
                steps={['Profile Chooser', 'Storage Boundary Notice', 'Keystore Picker', 'Approved Creation', 'JWK Attestation', 'Credential Activated']}
                currentStep={enrollStep}
                isSimulatingNativeAuth={isSimulatingEnrollAuth}
                onSimulateAuthSuccess={handleEnrollAuthSuccess}
                onSimulateAuthFail={handleEnrollAuthFail}
              >
                <div className="space-y-5 text-slate-800">
                  {enrollStep === 0 && (
                    <div className="space-y-4">
                      <div className="space-y-1">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Choose Intended Key Profile</label>
                        <p className="text-xs text-slate-500 leading-relaxed">
                          Software-secured keys require dedicated profiles to align cryptographic algorithms with intended gateway use.
                        </p>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                        {KEY_PROFILES.map((profile) => (
                          <button
                            key={profile.id}
                            id={`btn-profile-opt-${profile.id}`}
                            type="button"
                            onClick={() => setEnrollProfile(profile.id)}
                            className={`p-4 rounded-xl border text-left transition-all ${
                              enrollProfile === profile.id
                                ? 'bg-indigo-50/80 border-indigo-500 ring-2 ring-indigo-500/10'
                                : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                            }`}
                          >
                            <span className="font-bold text-sm text-slate-800 block">{profile.name}</span>
                            <p className="text-xs text-slate-500 mt-1.5 leading-relaxed">{profile.description}</p>
                            <div className="text-[10px] text-indigo-700 font-mono mt-2 flex items-center justify-between font-semibold">
                              <span>Recommended Store: {profile.recommendedStore}</span>
                              <span className="bg-indigo-100 px-1.5 py-0.5 rounded">
                                {profile.algorithms.join('/')}
                              </span>
                            </div>
                          </button>
                        ))}
                      </div>

                      <div className="flex justify-end pt-2">
                        <button
                          type="button"
                          id="btn-enroll-profile-next"
                          onClick={handleEnrollStepAdvance}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Advance to Boundary Notice
                        </button>
                      </div>
                    </div>
                  )}

                  {enrollStep === 1 && (
                    <div className="space-y-4">
                      <div className="space-y-1">
                        <h4 className="font-bold text-slate-800 text-sm">Review Cryptographic Boundaries & Backup Postures</h4>
                        <p className="text-xs text-slate-500">
                          Confirm how software-isolated credentials differ from HSMs and hardware modules.
                        </p>
                      </div>

                      <SoftwareKeyPrivacyNotice
                        backupPolicy={policy.backupPolicy}
                        exportPolicy={policy.exportPolicy}
                      />

                      <div className="flex gap-2 justify-between pt-2">
                        <button
                          type="button"
                          onClick={() => setEnrollStep(0)}
                          className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Back
                        </button>
                        <button
                          type="button"
                          id="btn-enroll-privacy-next"
                          onClick={handleEnrollStepAdvance}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Accept and Pick Keystore
                        </button>
                      </div>
                    </div>
                  )}

                  {enrollStep === 2 && (
                    <div className="space-y-4">
                      <KeyStorePicker
                        selectedId={enrollKeystore}
                        onChange={(id) => setEnrollKeystore(id)}
                      />

                      <div className="flex gap-2 justify-between pt-2">
                        <button
                          type="button"
                          onClick={() => setEnrollStep(1)}
                          className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Back
                        </button>
                        <button
                          type="button"
                          id="btn-enroll-keystore-next"
                          onClick={handleEnrollStepAdvance}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Continue to Creation Details
                        </button>
                      </div>
                    </div>
                  )}

                  {enrollStep === 3 && (
                    <div className="space-y-4">
                      <div className="space-y-1">
                        <h4 className="font-bold text-slate-800 text-sm">Step 3: Key Pair Configuration Details</h4>
                        <p className="text-xs text-slate-500">
                          Configure metadata aliases and scopes for the local keystore generation call.
                        </p>
                      </div>

                      {enrollError && (
                        <div className="bg-rose-50 border border-rose-200 text-rose-800 p-3 rounded-lg flex gap-2 text-xs">
                          <XCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                          <span>{enrollError}</span>
                        </div>
                      )}

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-1.5">
                          <label className="text-xs font-semibold text-slate-600 block">Friendly Credential Name</label>
                          <input
                            id="input-enroll-name"
                            type="text"
                            value={enrollKeyName}
                            onChange={(e) => setEnrollKeyName(e.target.value)}
                            className="w-full text-xs border border-slate-200 rounded-lg p-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500"
                            placeholder="e.g. My Secure Token"
                          />
                        </div>

                        <div className="space-y-1.5">
                          <label className="text-xs font-semibold text-slate-600 block">Cryptographic Algorithm</label>
                          <select
                            id="select-enroll-algorithm"
                            value={enrollAlgorithm}
                            onChange={(e) => setEnrollAlgorithm(e.target.value)}
                            className="w-full text-xs border border-slate-200 rounded-lg p-2.5 bg-white outline-none focus:ring-2 focus:ring-indigo-500"
                          >
                            <option value="ES256">ECDSA ES256 (NIST P-256)</option>
                            <option value="EdDSA">EdDSA (Ed25519 - Modern)</option>
                            <option value="RS256">RSA RS256 (2048-bit Signature)</option>
                          </select>
                        </div>

                        <div className="space-y-1.5 md:col-span-2">
                          <label className="text-xs font-semibold text-slate-600 block">Scope Application URL/Bound</label>
                          <input
                            id="input-enroll-scope"
                            type="text"
                            value={enrollAppScope}
                            onChange={(e) => setEnrollAppScope(e.target.value)}
                            className="w-full text-xs border border-slate-200 rounded-lg p-2.5 bg-white font-mono outline-none focus:ring-2 focus:ring-indigo-500"
                            placeholder="e.g. api.domain.org"
                          />
                        </div>
                      </div>

                      <div className="flex gap-2 justify-between pt-2">
                        <button
                          type="button"
                          onClick={() => setEnrollStep(2)}
                          className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Back
                        </button>
                        <button
                          type="button"
                          id="btn-enroll-generate"
                          onClick={handleEnrollStepAdvance}
                          className="bg-slate-900 hover:bg-slate-800 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-colors flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
                        >
                          <Cpu className="w-4 h-4 text-indigo-400" />
                          Generate Key Material in OS Keystore
                        </button>
                      </div>
                    </div>
                  )}

                  {enrollStep === 4 && (
                    <div className="space-y-4">
                      <div className="space-y-1">
                        <h4 className="font-bold text-slate-800 text-sm">Step 4: Register Public Material & Prove Possession</h4>
                        <p className="text-xs text-slate-500">
                          The private key stays isolated on your OS. We must send the public key JWK and sign a server-issued proof challenge to earn the verified classification.
                        </p>
                      </div>

                      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5 text-xs">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block">Local Key Material (JWK Export Blocked)</span>
                        <div>Algorithm : <strong className="font-semibold text-slate-800">{enrollAlgorithm}</strong></div>
                        <div>Keystore  : <strong className="font-semibold text-indigo-700">{enrollKeystore}</strong></div>
                        <div className="font-mono text-slate-500 text-[10px] pt-1 border-t border-slate-200 mt-1">
                          Generated Public Key: {"{"} kty: "{enrollAlgorithm === 'RS256' ? 'RSA' : 'EC'}", alg: "{enrollAlgorithm}" ... {"}"}
                        </div>
                      </div>

                      <div className="bg-emerald-50 border border-emerald-150 text-emerald-800 rounded-lg p-3 text-xs leading-relaxed">
                        The gateway issued an authorization challenge challenge nonce. Completing this step registers the key on the server JWKS set and derivation filters verify attestation properties.
                      </div>

                      <div className="flex gap-2 justify-between pt-2">
                        <button
                          type="button"
                          onClick={() => setEnrollStep(3)}
                          className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Back
                        </button>
                        <button
                          type="button"
                          id="btn-enroll-prove-possession"
                          onClick={handleEnrollStepAdvance}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 px-4 rounded-xl text-xs transition-colors flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
                        >
                          <CheckCircle className="w-4 h-4" />
                          Submit Public Registration & Possession Proof
                        </button>
                      </div>
                    </div>
                  )}

                  {enrollStep === 5 && (
                    <div className="space-y-4 animate-in fade-in duration-300">
                      <div className="p-5 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 space-y-3 text-xs">
                        <div className="flex items-center gap-2 font-bold text-emerald-950 text-sm">
                          <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
                          Enrollment Ceremony Successful!
                        </div>
                        <p className="leading-relaxed">
                          Your key <strong>{enrollKeyName}</strong> was successfully generated and registered. Server-side attestation parsed your OS metadata statement and derived the following protection classification:
                        </p>

                        <div className="flex items-center gap-2 pt-2 border-t border-emerald-200/60 font-semibold text-emerald-950">
                          <span>Verified Backing:</span>
                          {enrollKeystore === 'unverified_browser' ? (
                            <span className="inline-flex items-center gap-1 bg-amber-100 text-amber-800 px-2 py-0.5 rounded text-[10px] font-bold border border-amber-200">
                              Backing not verified
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold border border-emerald-200">
                              Verified swk AMR Status
                            </span>
                          )}
                        </div>
                      </div>

                      {oneTimeSecret && (
                        <OneTimeSecretReveal
                          secret={oneTimeSecret}
                          label="Software-Key Backup Attestation Recovery Token"
                        />
                      )}

                      <div className="flex justify-end pt-2 border-t border-slate-100">
                        <button
                          type="button"
                          id="btn-enroll-complete-dismiss"
                          onClick={handleResetEnrollment}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer"
                        >
                          Finish & View Key Details
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </CeremonyShell>

              {/* Detail view of selected key with Rotation/Compromise controls */}
              <div className="bg-slate-950/40 border border-slate-800 rounded-2xl p-5 space-y-5">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                  <div className="space-y-0.5">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block">Selected Credential Inventory Report</span>
                    <h4 className="font-bold text-slate-100 text-sm">{activeCredential.name}</h4>
                  </div>
                  <div className="flex items-center gap-2">
                    <KeyBackingBadge
                      storageClass={activeCredential.storageClass}
                      hasVerifiedEvidence={activeCredential.hasVerifiedEvidence}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-5 text-xs">
                  <div className="space-y-3.5">
                    <div className="space-y-1.5">
                      <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wide block">Properties</span>
                      <div className="bg-slate-900/60 rounded-xl p-3 border border-slate-800/80 space-y-2.5 font-mono text-[11px] text-slate-300">
                        <div className="flex justify-between">
                          <span className="text-slate-500">Credential ID:</span>
                          <span className="font-semibold text-slate-100">{activeCredential.id}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Key Type Profile:</span>
                          <span className="font-semibold text-slate-100 uppercase">{activeCredential.profile}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Algorithm:</span>
                          <span className="font-semibold text-indigo-400">{activeCredential.algorithm}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Keystore Provider:</span>
                          <span className="font-semibold text-slate-100">{activeCredential.keyStoreProvider}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Backup Posture:</span>
                          <span className={`font-semibold uppercase ${activeCredential.backupPosture === 'blocked' ? 'text-emerald-400' : 'text-amber-400'}`}>{activeCredential.backupPosture}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Export Posture:</span>
                          <span className={`font-semibold uppercase ${activeCredential.exportPosture === 'blocked' ? 'text-emerald-400' : 'text-amber-400'}`}>{activeCredential.exportPosture}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">App Scope:</span>
                          <span className="font-semibold text-slate-100">{activeCredential.appScope}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Created:</span>
                          <span className="font-semibold text-slate-100">{new Date(activeCredential.createdAt).toLocaleDateString()}</span>
                        </div>
                      </div>
                    </div>

                    <PublicKeySummary
                      publicKeyJwk={activeCredential.publicKeyJwk}
                      fingerprint={activeCredential.fingerprint}
                      algorithm={activeCredential.algorithm}
                    />
                  </div>

                  <div className="space-y-4">
                    <KeyDependencyImpact
                      dependencies={activeCredential.dependencies}
                      status={activeCredential.status}
                      keyName={activeCredential.name}
                    />

                    {activeCredential.profile === 'dpop' && (
                      <KeyRotationTimeline
                        currentStage={rotationStage}
                        onAdvance={handleRotationAdvance}
                        onReset={handleRotationReset}
                        replacingKeyName="DPoP Gateway Assertor v2"
                        originalKeyName="DPoP Gateway Assertor"
                      />
                    )}

                    <div id="danger-zone-credentials" className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-3.5">
                      <div className="flex items-center gap-1.5 border-b border-slate-800 pb-2 text-rose-400 font-bold">
                        <AlertOctagon className="w-4 h-4" />
                        <span>Danger Zone Operations</span>
                      </div>
                      <p className="text-[11px] text-slate-400 leading-relaxed">
                        Operations on private credentials are irreversible. Marking a key as compromised will immediately drop gateway routes.
                      </p>

                      <div className="flex flex-col sm:flex-row gap-2 pt-1">
                        <button
                          type="button"
                          id="btn-compromise-key-action"
                          onClick={() => handleCompromiseKey(activeCredential.id)}
                          disabled={activeCredential.status === 'compromised'}
                          className="flex-1 text-center bg-rose-950/40 hover:bg-rose-950/80 border border-rose-900 text-rose-400 py-2 px-3 rounded-lg font-semibold transition-colors cursor-pointer disabled:opacity-40"
                        >
                          Mark Compromised
                        </button>
                        <button
                          type="button"
                          id="btn-revoke-key-action"
                          onClick={() => handleRevokeKey(activeCredential.id)}
                          disabled={activeCredential.status === 'revoked'}
                          className="flex-1 text-center bg-slate-800 hover:bg-slate-750 border border-slate-700 text-slate-300 py-2 px-3 rounded-lg font-semibold transition-colors cursor-pointer disabled:opacity-40"
                        >
                          Explicit Revoke
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {workspace === 'p2_policy' && (
            <div className="space-y-6">
              <div className="bg-slate-950/40 border border-slate-800 rounded-2xl p-5 space-y-4">
                <div className="border-b border-slate-800 pb-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Settings className="w-5 h-5 text-indigo-400" />
                    <h3 className="font-bold text-slate-100 text-sm">Key-Origin Policy & Governance</h3>
                  </div>
                  <span className="text-[10px] font-mono bg-indigo-950 text-indigo-400 border border-indigo-900 px-2 py-0.5 rounded">
                    Global Scope Policy Enforced
                  </span>
                </div>

                <p className="text-xs text-slate-400 leading-relaxed">
                  Configure verification parameters required of software isolated keys to claim verified <code className="bg-slate-900 px-1 py-0.5 rounded text-xs text-indigo-400 font-mono">swk</code> AMR status.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
                  <div className="space-y-4">
                    <div className="space-y-1.5">
                      <span className="text-xs font-semibold text-slate-300 block">Accepted Software Keystore Providers</span>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        {[
                          { id: 'macos_keychain', label: 'macOS Keychain' },
                          { id: 'windows_cng', label: 'Windows CNG' },
                          { id: 'linux_systemd', label: 'Linux systemd' },
                          { id: 'openssl_cli', label: 'CLI OpenSSL' },
                          { id: 'unverified_browser', label: 'Browser IndexedDB' }
                        ].map((storeOpt) => {
                          const isAllowed = policy.allowedStores.includes(storeOpt.id);
                          return (
                            <button
                              key={storeOpt.id}
                              id={`checkbox-policy-store-${storeOpt.id}`}
                              type="button"
                              onClick={() => {
                                const nextStores = isAllowed
                                  ? policy.allowedStores.filter((id) => id !== storeOpt.id)
                                  : [...policy.allowedStores, storeOpt.id];
                                setPolicy({ ...policy, allowedStores: nextStores });
                                addAuditEvent('policy_change', 'admin-console', 'system', 'software_secured', true, `Allowed keystores modified. Checked: ${storeOpt.id} = ${!isAllowed}`);
                              }}
                              className={`p-2 rounded-lg border text-left transition-colors cursor-pointer font-medium ${
                                isAllowed
                                  ? 'bg-indigo-950/30 border-indigo-500/60 text-indigo-300'
                                  : 'bg-slate-900/60 border-slate-800 text-slate-500 hover:text-slate-400'
                              }`}
                            >
                              {storeOpt.label} {isAllowed ? '✓' : '✗'}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    <div className="space-y-1.5">
                      <span className="text-xs font-semibold text-slate-300 block">Permitted Signature Algorithms</span>
                      <div className="flex gap-2">
                        {['ES256', 'EdDSA', 'RS256'].map((alg) => {
                          const isAllowed = policy.allowedAlgorithms.includes(alg);
                          return (
                            <button
                              key={alg}
                              id={`checkbox-policy-alg-${alg}`}
                              type="button"
                              onClick={() => {
                                const nextAlgs = isAllowed
                                  ? policy.allowedAlgorithms.filter((id) => id !== alg)
                                  : [...policy.allowedAlgorithms, alg];
                                setPolicy({ ...policy, allowedAlgorithms: nextAlgs });
                                addAuditEvent('policy_change', 'admin-console', 'system', 'software_secured', true, `Permitted signature algorithms updated: ${alg} = ${!isAllowed}`);
                              }}
                              className={`px-3 py-1.5 rounded-lg border text-xs font-mono transition-colors cursor-pointer font-bold ${
                                isAllowed
                                  ? 'bg-indigo-950/30 border-indigo-500/60 text-indigo-300'
                                  : 'bg-slate-900/60 border-slate-800 text-slate-500 hover:text-slate-400'
                              }`}
                            >
                              {alg} {isAllowed ? '✓' : '✗'}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3 pt-1">
                      <div className="space-y-1.5">
                        <label className="text-xs font-semibold text-slate-300 block">Backup Storage Policy</label>
                        <select
                          id="select-policy-backup"
                          value={policy.backupPolicy}
                          onChange={(e) => {
                            const val = e.target.value as any;
                            setPolicy({ ...policy, backupPolicy: val });
                            addAuditEvent('policy_change', 'admin-console', 'system', 'software_secured', true, `Backup policy modified to ${val.toUpperCase()}`);
                          }}
                          className="w-full text-xs border border-slate-800 bg-slate-900 rounded-lg p-2 bg-slate-900 text-slate-200 outline-none focus:ring-1 focus:ring-indigo-500"
                        >
                          <option value="allow">Permitted</option>
                          <option value="block">Blocked</option>
                          <option value="strict_evidence">Strict Evidence Required</option>
                        </select>
                      </div>

                      <div className="space-y-1.5">
                        <label className="text-xs font-semibold text-slate-300 block">Export Policy Extraction</label>
                        <select
                          id="select-policy-export"
                          value={policy.exportPolicy}
                          onChange={(e) => {
                            const val = e.target.value as any;
                            setPolicy({ ...policy, exportPolicy: val });
                            addAuditEvent('policy_change', 'admin-console', 'system', 'software_secured', true, `Export extraction policy modified to ${val.toUpperCase()}`);
                          }}
                          className="w-full text-xs border border-slate-800 bg-slate-900 rounded-lg p-2 bg-slate-900 text-slate-200 outline-none focus:ring-1 focus:ring-indigo-500"
                        >
                          <option value="allow">Permitted</option>
                          <option value="block">Blocked</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <PolicyImpactPreview
                    policy={policy}
                    activeCredentials={credentials}
                  />
                </div>
              </div>

              <ValidationWorkbench
                activeKeys={credentials.filter((c) => c.status === 'active')}
              />

              <JwksEditor
                initialKeys={credentials.map((c) => {
                  try {
                    return JSON.parse(c.publicKeyJwk);
                  } catch {
                    return { kid: c.id, alg: c.algorithm, kty: 'RSA' };
                  }
                })}
                onAddKey={handleAddJwkToRegistry}
                onRemoveKey={handleRemoveJwkFromRegistry}
              />

              <ProviderHealthMonitor
                providers={providers}
                onToggleStatus={handleToggleProviderHealth}
                onRefreshAll={handleRefreshHealthAll}
              />

              <AuditDiagnostics
                events={auditLogs}
                onClearLogs={() => {
                  setAuditLogs([]);
                  addAuditEvent('compromise', 'admin-console', 'system', 'unknown', false, 'Cryptographic diagnostics audit log manually cleared.');
                }}
              />
            </div>
          )}

          {workspace === 'cli_emulator' && (
            <CliTooling />
          )}
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 py-5 shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div>
            © 2026 Software-Secured Key AMR Workspace. All rights reserved.
          </div>
          <div className="flex gap-4">
            <a href="#privacy" className="hover:text-slate-300">Portability Boundaries</a>
            <a href="#compliance" className="hover:text-slate-300">swk AMR attestation metadata</a>
            <a href="#help" className="hover:text-slate-300">Validator workbench</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
