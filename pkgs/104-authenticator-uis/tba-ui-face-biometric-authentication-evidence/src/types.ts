/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// --- Biometric Authenticators & Lifecycle Types ---
export type AuthenticatorStatus = 'active' | 'suspended' | 'replacement_required' | 'revoked' | 'compromised';

export interface FaceAuthenticator {
  id: string;
  label: string;
  status: AuthenticatorStatus;
  verifierProfile: string;
  createdDate: string;
  lastUsedDate: string;
  consentVersion: string;
  consentDate: string;
  retentionPolicy: string;
  deletionJobId?: string;
  deletionStatus?: DeletionJobStatus;
  deletionLogs?: string[];
  recoveryPostured: boolean;
  recoveryMethod: string;
  deviceProjection: string;
}

export type DeletionJobStatus = 'none' | 'pending' | 'completed' | 'failed' | 'manual_review';

export interface ConsentRecord {
  version: string;
  consentDate: string;
  status: 'accepted' | 'declined' | 'withdrawn';
  controllerRole: string;
  processorRole: string;
  retentionMonths: number;
  sharingBoundary: string;
  auditReference: string;
}

// --- Ceremony / Transaction State ---
export type CeremonyState =
  | 'initializing'
  | 'ready'
  | 'awaiting_os_prompt'
  | 'submitting'
  | 'retryable_failure'
  | 'biometric_unavailable'
  | 'consent_required'
  | 'consent_declined'
  | 'permission_denied'
  | 'preflight_incompatible'
  | 'capturing'
  | 'liveness_passed'
  | 'liveness_failed'
  | 'no_match'
  | 'suspected_spoofing'
  | 'attempts_exhausted'
  | 'completed_success'
  | 'completed_multi_factor_required'
  | 'cancelled'
  | 'timeout'
  | 'untrusted_evidence';

export interface CeremonyContext {
  id: string;
  state: CeremonyState;
  purpose: 'enrollment' | 'login' | 'step_up' | 'replacement';
  challenge: string;
  timestamp: string;
  expiresAt: string;
  attempts: number;
  maxAttempts: number;
  allowedRecovery: boolean;
  selectedMethod?: string;
}

// --- Evidence Provenance & Provenance Mapping ---
export type EvidenceProvenance =
  | 'face_verified'                     // Direct first-party verified native capture
  | 'user_verified_modality_unknown'    // Generic WebAuthn User Verification
  | 'upstream_face_trusted'            // Trusted IDP federated face evidence
  | 'upstream_face_untrusted'          // Federated face evidence that fails policy or has unrecognized AMR
  | 'face_evidence_stale';             // Enrolled face evidence that exceeded lifetime

export interface BiometricEvidence {
  amr: 'face' | 'uv' | 'unknown';
  provenance: EvidenceProvenance;
  issuer: string;
  verificationTime: string;
  freshnessSeconds: number;
  confidenceRating: 'high_attested' | 'medium_reported' | 'low_unknown';
  isHardwareBacked: boolean;
  isLivenessProtected: boolean;
  auditReference: string;
  redactedRawClaims: Record<string, string>;
}

// --- Audit & Analytics Log Entry ---
export interface AuditLogEntry {
  id: string;
  timestamp: string;
  event: string;
  category: 'enrollment' | 'authentication' | 'lifecycle' | 'policy' | 'consent';
  actor: string;
  status: 'success' | 'failure' | 'warning' | 'info';
  details: string;
  amrEvidence?: string;
  provenance?: EvidenceProvenance;
  device?: string;
  ip?: string;
}

// --- Admin Policy & Trusted Provider Models ---
export interface TrustedProvider {
  id: string;
  name: string;
  clientId: string;
  endpointUrl: string;
  trustProfile: 'strict_direct' | 'federated_verified' | 'lax_any';
  allowedAmrMappings: string[];
  lastChecked: string;
  status: 'healthy' | 'degraded' | 'outage';
}

export interface TenantEvidencePolicy {
  allowFirstPartyFace: boolean;
  allowFederatedFace: boolean;
  requireLiveness: boolean;
  requireHardwareBacking: boolean;
  maxEvidenceAgeSeconds: number;
  allowedProviders: string[];
  fallbackMethods: string[];
  enforceMfaOnFailure: boolean;
  version: number;
  lastUpdated: string;
  lastUpdatedBy: string;
}
