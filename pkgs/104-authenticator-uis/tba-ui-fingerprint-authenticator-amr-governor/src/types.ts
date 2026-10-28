export type CeremonyState = 
  | 'idle'
  | 'initializing'
  | 'ready'
  | 'prompt'
  | 'submitting'
  | 'success'
  | 'error';

export type CeremonyType = 
  | 'passkey_login' 
  | 'federated_login' 
  | 'step_up' 
  | 'native_handoff';

export type BiometricErrorType =
  | 'sensor_unavailable'
  | 'lockout'
  | 'cancelled'
  | 'timeout'
  | 'unsupported_environment';

export interface ProviderProfile {
  id: string;
  name: string;
  issuerUrl: string;
  status: 'online' | 'degraded' | 'outage';
  mappingRule: string; // Describes the transformation pattern
  claimsSupported: string[];
  freshnessLimitSeconds: number;
}

export interface PolicyConfig {
  requireFingerprint: boolean;
  allowedIssuers: string[];
  maxAgeSeconds: number;
  fallbackMethod: 'pin' | 'security_key' | 'mfa_redirect' | 'fail_closed';
  rolloutPercentage: number;
}

export interface AuditEvent {
  id: string;
  timestamp: string;
  type: string;
  status: 'approved' | 'blocked' | 'fallback';
  username: string;
  detectedAmrs: string[];
  sourceProvider: string;
  userVerificationFlag: boolean;
  freshnessSeconds: number;
  policySatisfied: boolean;
  auditReference: string;
  description: string;
  normalizedEvidence: {
    hasFpt: boolean;
    isTrusted: boolean;
    evidenceProvenance: string;
    directVsTransformed: 'direct' | 'transformed' | 'none';
  };
  redactedProvenance: {
    deviceClass: string;
    authChannel: string;
    browserVersion: string;
    rawClaimsRedacted: boolean;
  };
}
