/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { FaceAuthenticator, TenantEvidencePolicy, TrustedProvider, AuditLogEntry, ConsentRecord } from './types';

export const INITIAL_AUTHENTICATORS: FaceAuthenticator[] = [
  {
    id: 'auth-01',
    label: 'Primary Work Laptop - Built-in IR Camera',
    status: 'active',
    verifierProfile: 'verifier-f1-secure-v2',
    createdDate: '2026-03-12T14:22:11Z',
    lastUsedDate: '2026-07-15T07:44:02Z',
    consentVersion: 'v2.1-compliance',
    consentDate: '2026-03-12T14:19:40Z',
    retentionPolicy: 'Local verifier enclave partition. Templates are purged 24 hours after deletion activation or on consent withdrawal.',
    recoveryPostured: true,
    recoveryMethod: 'Hardware Security Key (YubiKey 5C)',
    deviceProjection: 'Apple MacBook Pro (M3 Max / Secure Enclave Auth)',
  },
  {
    id: 'auth-02',
    label: 'Enterprise Mobile Secure Capture',
    status: 'replacement_required',
    verifierProfile: 'verifier-mobile-liveness-v3',
    createdDate: '2025-06-20T09:15:00Z',
    lastUsedDate: '2026-06-10T18:30:11Z',
    consentVersion: 'v1.0-legacy',
    consentDate: '2025-06-20T09:12:00Z',
    retentionPolicy: 'Encrypted verifier server enclave. Replacement required due to legacy consent framework and hardware-profile updates.',
    recoveryPostured: true,
    recoveryMethod: 'Supervised Admin Recovery',
    deviceProjection: 'Google Pixel 8 (Secure Element biometric binder)',
  }
];

export const INITIAL_PROVIDERS: TrustedProvider[] = [
  {
    id: 'prov-01',
    name: 'Okta Enterprise Federation',
    clientId: 'okta_ent_client_8819',
    endpointUrl: 'https://enterprise.okta.com/oauth2/v1/auth',
    trustProfile: 'federated_verified',
    allowedAmrMappings: ['face', 'uv'],
    lastChecked: '2026-07-15T08:30:00Z',
    status: 'healthy'
  },
  {
    id: 'prov-02',
    name: 'Microsoft Entra ID (Contoso Tenant)',
    clientId: 'entra_client_6623_prod',
    endpointUrl: 'https://login.microsoftonline.com/oauth2/v2.0',
    trustProfile: 'strict_direct',
    allowedAmrMappings: ['face'],
    lastChecked: '2026-07-15T08:45:00Z',
    status: 'healthy'
  },
  {
    id: 'prov-03',
    name: 'PingIdentity Legacy Gateway',
    clientId: 'ping_legacy_client',
    endpointUrl: 'https://ping.gateway.internal/auth',
    trustProfile: 'lax_any',
    allowedAmrMappings: ['uv'],
    lastChecked: '2026-07-15T08:50:00Z',
    status: 'degraded'
  }
];

export const INITIAL_POLICY: TenantEvidencePolicy = {
  allowFirstPartyFace: true,
  allowFederatedFace: true,
  requireLiveness: true,
  requireHardwareBacking: true,
  maxEvidenceAgeSeconds: 3600, // 1 hour
  allowedProviders: ['prov-01', 'prov-02'],
  fallbackMethods: ['passkey', 'security_key', 'recovery_code'],
  enforceMfaOnFailure: true,
  version: 4,
  lastUpdated: '2026-06-05T10:11:45Z',
  lastUpdatedBy: 'admin-operator-99@company.com'
};

export const INITIAL_AUDIT_LOGS: AuditLogEntry[] = [
  {
    id: 'log-001',
    timestamp: '2026-07-15T08:45:12Z',
    event: 'Biometric Evidence Verified',
    category: 'authentication',
    actor: 'jick.68.0@gmail.com',
    status: 'success',
    details: 'Direct first-party face verified inside approved native capture enclave. Liveness challenge signature validated.',
    amrEvidence: 'face',
    provenance: 'face_verified',
    device: 'Apple MacBook Pro (M3 Max / Secure Enclave Auth)',
    ip: '198.51.100.42'
  },
  {
    id: 'log-002',
    timestamp: '2026-07-15T08:12:30Z',
    event: 'WebAuthn Assertion Received',
    category: 'authentication',
    actor: 'jick.68.0@gmail.com',
    status: 'success',
    details: 'Browser passkey assertion ceremony completed. Modality confidence is insufficient (AMR contains only general uv). Re-routed as generic user verification.',
    amrEvidence: 'uv',
    provenance: 'user_verified_modality_unknown',
    device: 'iPhone 15 Pro (Safari browser generic WebAuthn)',
    ip: '198.51.100.42'
  },
  {
    id: 'log-003',
    timestamp: '2026-07-15T07:11:05Z',
    event: 'Federated Evidence Transformed',
    category: 'authentication',
    actor: 'jick.68.0@gmail.com',
    status: 'success',
    details: 'Upstream assertion from Microsoft Entra ID parsed. Trusted AMR face mapped to local security policy.',
    amrEvidence: 'face',
    provenance: 'upstream_face_trusted',
    device: 'Windows Desktop (Edge browser)',
    ip: '203.0.113.88'
  },
  {
    id: 'log-004',
    timestamp: '2026-07-15T06:50:18Z',
    event: 'Enrollment Preflight Blocked',
    category: 'enrollment',
    actor: 'jick.68.0@gmail.com',
    status: 'failure',
    details: 'Face capture preflight failed. Untrusted generic browser camera flow used. Enrollment blocked to prevent unsecured template collection.',
    device: 'Linux PC (Firefox browser - webcam)',
    ip: '198.51.100.99'
  },
  {
    id: 'log-005',
    timestamp: '2026-07-14T15:22:41Z',
    event: 'Biometric Consent Record Created',
    category: 'consent',
    actor: 'jick.68.0@gmail.com',
    status: 'success',
    details: 'Informed consent captured for legal version v2.1-compliance. Local processor and controller bounds explicitly approved.',
    device: 'Apple MacBook Pro (M3 Max / Secure Enclave Auth)',
    ip: '198.51.100.42'
  }
];

export const CONSENT_TEXTS = {
  version: 'v2.1-compliance',
  title: 'Biometric Privacy and Consent Notice',
  legalBasis: 'GDPR Article 9(2)(a) (Explicit Consent), CCPA/CPRA Biometric Privacy Framework',
  purpose: 'This consent authorizes the collection, encryption, and streaming of facial biometric sample feeds exclusively for presentation-attack detection (liveness analysis) and direct secure enclave match confirmation.',
  processingBoundary: 'All raw facial frames are transiently processed inside the hardware-backed native camera boundary and streamed using ephemeral TLS tunnels directly to the secure isolated verifier boundary. NO facial images, video recordings, or raw biometric templates are ever persisted, logged, or exposed in the general browser document object model (DOM), application local storage, analytics payloads, or operational error metrics.',
  retention: 'The computed mathematical template is stored securely in an isolated physical security partition. Upon revocation of this authenticator, withdrawal of consent, or failure of biometric verification retention audits, the biometric template is marked for asynchronous permanent erasure (cryptographically shredded within 24 hours) with an immutable cryptographic deletion certificate generated.',
  sharing: 'Absolutely no biometric information is ever shared with third parties, analytics companies, or cloud databases outside the strictly defined company verifier identity enclave.',
  alternatives: 'Enrollment in first-party face recognition is strictly voluntary. If you choose to decline, you may satisfy the security policy by registering alternative phishing-resistant authenticators such as a WebAuthn FIDO2 Hardware Security Key or Supervised Passwordless Authentication.'
};
