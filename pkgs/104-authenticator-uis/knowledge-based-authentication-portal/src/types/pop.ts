/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type PoPProfile = 'dpop' | 'mtls' | 'private_key_jwt' | 'workload_key';

export interface PoPKey {
  id: string;
  label: string;
  profile: PoPProfile;
  algorithm: string;
  publicKeyJwk?: {
    kty: string;
    use?: string;
    alg?: string;
    kid?: string;
    crv?: string;
    x?: string;
    y?: string;
    n?: string;
    e?: string;
  };
  certificatePem?: string;
  subjectAlternativeName?: string;
  extendedKeyUsage?: string;
  thumbprint: string; // JKT or x5t#S256
  status: 'draft' | 'validation_pending' | 'active' | 'overlap' | 'retiring' | 'expired' | 'suspended' | 'compromised' | 'revoked';
  createdAt: string;
  expiresAt: string;
  lastUsedAt?: string;
  dependentServices: string[];
  associatedClientToken?: string;
}

export interface PoPPolicy {
  allowedProfiles: PoPProfile[];
  allowedAlgorithms: string[];
  nonceRequired: boolean;
  nonceLifespanSec: number;
  replayPreventionWindowSec: number;
  strictAudienceCheck: boolean;
  requireHardwareBound: boolean;
}

export interface SyntheticRequest {
  method: string;
  url: string;
  headers: Record<string, string>;
  body?: string;
}

export interface ValidationOutcome {
  isValid: boolean;
  errorClass?: 
    | 'malformed' 
    | 'signature' 
    | 'binding_mismatch' 
    | 'nonce_required' 
    | 'nonce_stale' 
    | 'freshness_expired' 
    | 'replay_detected' 
    | 'certificate_invalid' 
    | 'algorithm_rejected' 
    | 'policy_violation' 
    | 'provider_unavailable' 
    | 'rate_limited';
  errorDetails?: string;
  evidence?: {
    popEmitted: boolean;
    verifier: string;
    profile: PoPProfile;
    proofTime: string;
    freshnessMs: number;
    keyBindingId: string;
    replayResult: 'clean' | 'replayed';
    policyVersion: string;
    auditReference: string;
  };
}

export interface ValidatorHealth {
  activeNoncesCount: number;
  storedReplayJtisCount: number;
  validationSuccessRate: number; // 0-100
  recentErrorsCount: Record<string, number>;
  averageLatencyMs: number;
  status: 'healthy' | 'degraded' | 'unavailable';
}

export interface AuditLogEntry {
  id: string;
  timestamp: string;
  action: string;
  actor: string;
  profile: PoPProfile;
  status: 'success' | 'failure';
  details: string;
  keyId?: string;
  auditReference: string;
}
