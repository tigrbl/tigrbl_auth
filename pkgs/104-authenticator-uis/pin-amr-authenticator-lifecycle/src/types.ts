/**
 * Types and interfaces for the PIN AMR Authenticator Lifecycle application.
 */

export type AMRMode = 'first-party' | 'device-local' | 'authenticator-pin' | 'trusted-upstream';

export type PinState =
  | 'not-enrolled'
  | 'introduction'
  | 'creation'
  | 'confirmation-mismatch'
  | 'verification-pending'
  | 'active'
  | 'invalid'
  | 'rate-limited'
  | 'attempts-exhausted'
  | 'locked'
  | 'compromised'
  | 'change-replace-pending'
  | 'suspended'
  | 'revoked'
  | 'removed'
  | 'reset-requested'
  | 'forced-reset'
  | 'recovery'
  | 'policy-changed'
  | 'success'
  | 'requires-next-step'
  // External device states
  | 'awaiting-system-device'
  | 'pin-requested-externally'
  | 'cancellation'
  | 'invalid-blocked-externally'
  | 'device-unavailable-removed'
  | 'middleware-unavailable'
  | 'timeout'
  | 'modality-unknown'
  | 'stale-untrusted-evidence';

export interface AuditEvent {
  id: string;
  timestamp: string;
  action: string;
  category: 'authentication' | 'lifecycle' | 'policy' | 'hardware' | 'admin';
  outcome: 'success' | 'failure' | 'warning' | 'info';
  details: string;
  provenance?: string;
  authenticatorClass?: string;
}

export interface FirstPartyPolicy {
  minLength: number;
  maxLength: number;
  allowAlpha: boolean;
  disallowedPatterns: string[]; // e.g. "1234", "1111", "0000"
  maxAttempts: number;
  rateLimitMinutes: number;
  lockoutThreshold: number;
  historySize: number;
}

export interface ExternalDeviceProfile {
  id: string;
  name: string;
  type: 'passkey' | 'roaming-key' | 'smart-card' | 'native-biometric';
  hasPinConfigured: boolean;
  supportsUserVerification: boolean;
  trustedUpstreamEvidence: boolean;
  requiresExternalPinPrompt: boolean;
}

export interface SimulatedServerState {
  // First-party fields
  isFirstPartyEnrolled: boolean;
  firstPartyVerifierHash: string | null; // e.g. pbkdf2-like representation
  firstPartyBackupRecoverySet: boolean;
  remainingAttempts: number;
  status: 'active' | 'suspended' | 'revoked' | 'locked' | 'compromised' | 'forced-reset';
  
  // Policy Config
  policy: FirstPartyPolicy;
  trustedExternalSources: {
    passkeyAllowed: boolean;
    securityKeyAllowed: boolean;
    smartCardAllowed: boolean;
    nativeDeviceAllowed: boolean;
    trustEvidenceProvenanceOnly: boolean;
  };
  
  // External state simulation counters
  deviceRetriesLeft: number;
  deviceLocked: boolean;
  middlewareHealthy: boolean;
  providerOutage: boolean;
}
