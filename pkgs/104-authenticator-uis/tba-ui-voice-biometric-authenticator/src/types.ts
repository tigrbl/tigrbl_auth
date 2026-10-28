export type VoiceBiometricStatus = 'unenrolled' | 'enrolled' | 'suspended' | 'revoked' | 'deleted';

export type LivenessClass = 'unknown' | 'live' | 'synthetic' | 'replay' | 'excessive_noise' | 'no_speech';

export type DeletionStatus = 'none' | 'pending' | 'completed' | 'failed';

export interface VoiceSample {
  id: string;
  phrase: string;
  durationSeconds: number;
  noiseDb: number;
  timestamp: string;
  qualityScore: number; // 0-100
}

export interface VoiceProfile {
  id: string;
  status: VoiceBiometricStatus;
  consentSigned: boolean;
  consentVersion: string;
  consentSignedAt?: string;
  createdTime?: string;
  lastUsedTime?: string;
  modelId: string;
  region: string;
  samples: VoiceSample[];
  deletionStatus: DeletionStatus;
  deletionTxHash?: string;
  deletionRequestTime?: string;
}

export interface PolicyConfig {
  minConfidence: number; // e.g. 85
  strictnessLevel: 'low' | 'medium' | 'high';
  allowedLanguages: string[];
  fallbackFactor: 'password' | 'totp' | 'fido_passkey' | 'security_questions';
  retentionDays: number;
  strictLiveness: boolean;
  noiseThresholdDb: number; // Max allowed ambient noise e.g. -45dB
}

export interface VerifierConfig {
  providerName: string;
  endpointUrl: string;
  region: 'us-east1' | 'europe-west1' | 'asia-east1';
  activeModel: string;
  healthStatus: 'healthy' | 'degraded' | 'offline';
  failBehavior: 'fail_safe' | 'fail_open';
}

export interface AuditLog {
  id: string;
  timestamp: string;
  action: string;
  status: 'success' | 'failure' | 'warning' | 'info';
  details: string;
  amrToken?: string;
  ipAddress: string;
}

export interface DiagnosticsSummary {
  totalAttempts: number;
  successCount: number;
  failureCount: number;
  spoofAttempts: {
    replay: number;
    synthetic: number;
  };
  noiseFailures: number;
  noSpeechFailures: number;
  averageResponseTimeMs: number;
}
