/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export enum OtpAlgorithm {
  SHA1 = "SHA-1",
  SHA256 = "SHA-256",
  SHA512 = "SHA-512",
}

export enum FactorStatus {
  NOT_ENROLLED = "Not Enrolled",
  ENROLLMENT_PENDING = "Enrollment Pending",
  SECRET_REVEALED = "Secret Revealed",
  VERIFICATION_PENDING = "Verification Pending",
  ACTIVE = "Active",
  SUSPENDED = "Suspended",
  REVOKED = "Revoked",
  COMPROMISED = "Compromised",
}

export interface AuthenticatorProfile {
  id: string;
  label: string;
  type: "totp" | "sms" | "email";
  status: FactorStatus;
  secret: string; // Base32 secret (hidden after enrollment)
  digits: number;
  period: number; // in seconds
  algorithm: OtpAlgorithm;
  created: string;
  lastUsed?: string;
  deliveryTarget?: string; // e.g. "+1 (555) 019-2834" or "user@example.com"
}

export interface TenantPolicy {
  allowedAlgorithms: OtpAlgorithm[];
  allowedDigits: number[]; // e.g. [6, 8]
  allowedPeriods: number[]; // e.g. [30, 60]
  attemptsLimit: number; // e.g. 3 attempts before temporary lock, 5 before full lockout
  rateLimitWindow: number; // in seconds, e.g. 60
  replayStoreExpiry: number; // in seconds, e.g. 300
  driftWindowGrace: number; // number of steps allowed backward/forward (e.g. 1 means skew of -1 to +1 period is fine)
  stepUpTimeout: number; // seconds a step-up verification remains valid
  forceMfa: boolean;
  allowFallback: boolean;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  eventType: 
    | "ENROLL_INIT" 
    | "ENROLL_VERIFY_SUCCESS" 
    | "ENROLL_VERIFY_FAIL" 
    | "AUTH_SUCCESS" 
    | "AUTH_FAIL" 
    | "STEP_UP_SUCCESS"
    | "REPLAY_REJECT" 
    | "DRIFT_CORRECTED" 
    | "LOCKOUT_TRIGGERED" 
    | "FACTOR_REVOKED" 
    | "FACTOR_SUSPENDED" 
    | "POLICY_UPDATE" 
    | "ADMIN_RESET";
  actor: string;
  details: string;
  status: "success" | "warning" | "error" | "info";
  ipAddress: string;
  requestId: string;
}

export interface SecurityPosture {
  failedAttemptsCount: number;
  isLockedOut: boolean;
  lockoutExpiresAt?: string;
  lastSuccessfulAuth?: string;
  recentVerificationType?: "totp" | "sms" | "email" | null;
  activeStepUpChallenge?: {
    id: string;
    purpose: string;
    amount?: string;
    expiresAt: string;
  } | null;
}

export interface SimulationState {
  currentTimeSkewSeconds: number; // skew to simulate clock-drift
  simulateReplayAttack: boolean;
  simulateStorageFailure: boolean;
  simulateNoRecoveryCode: boolean;
  lastGeneratedOtpFromSimulation?: string;
}
