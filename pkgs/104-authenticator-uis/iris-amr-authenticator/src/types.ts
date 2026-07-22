export interface BiometricConsent {
  accepted: boolean;
  version: string;
  signedAt?: string;
  withdrawnAt?: string;
}

export type IrisEnrollmentStatus = 
  | 'unregistered'
  | 'preflight'
  | 'capturing'
  | 'analyzing'
  | 'activated'
  | 'revoked'
  | 'pending_deletion'
  | 'deleted';

export type IrisAuthStatus =
  | 'idle'
  | 'connecting'
  | 'ready'
  | 'gaze_alignment'
  | 'capturing'
  | 'processing'
  | 'success'
  | 'retry_needed'
  | 'no_match'
  | 'spoof_detected'
  | 'disconnected'
  | 'blocked';

export interface IrisEnrollmentState {
  status: IrisEnrollmentStatus;
  currentStep: number;
  samplesCollected: number;
  maxSamples: number;
  gazeAligned: boolean;
  calibrationProgress: number; // 0 to 100
  qualityScore: number; // 0 to 100
  livenessVerified: boolean;
  retryReason?: string;
}

export interface IrisAuthState {
  status: IrisAuthStatus;
  challengeNonce: string;
  purpose: string;
  progress: number; // 0 to 100
  gazeAligned: boolean;
  eyeDetected: boolean;
  livenessChecked: boolean;
  errorMessage?: string;
  attemptsLeft: number;
  acceptedEvidence?: {
    amr: 'iris';
    source: 'first-party' | 'federated' | 'external-native';
    provenance: string;
    verifiedAt: string;
    trustProfile: 'high' | 'medium' | 'untrusted';
    livenessResultClass: string;
    ceremonyPurpose: string;
    auditReference: string;
  };
}

export interface BiometricPolicy {
  allowedProviders: string[];
  maxEvidenceAgeSeconds: number;
  requireLiveness: boolean;
  applicationScope: 'all' | 'restricted' | 'step-up-only';
  fallbackMethod: 'passkey' | 'totp' | 'supervised-recovery';
  regionalRollout: {
    usEast: boolean;
    euWest: boolean;
    apSouth: boolean;
  };
  minTrustLevel: 'high' | 'medium';
}

export interface ProviderConfig {
  id: string;
  name: string;
  type: 'first-party' | 'federated' | 'external-native';
  status: 'active' | 'suspended' | 'degraded' | 'offline';
  conformanceCertified: boolean;
  retentionDays: number;
  apiEndpoint: string;
  lastHealthCheck: string;
}

export interface AuditLogRecord {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  outcome: 'success' | 'failure' | 'warning';
  evidenceType: string;
  provenance: string;
  detailsRedacted: string;
}

export interface SimulatorSettings {
  alignmentPerfect: boolean;
  gazeAligned: boolean;
  lightingOptimal: boolean;
  livenessGenuine: boolean;
  deviceConnected: boolean;
  providerOutage: boolean;
}
