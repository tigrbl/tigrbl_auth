/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export enum AuthenticatorStatus {
  INELIGIBLE = "ineligible",
  NOT_ENROLLED = "not_enrolled",
  ENROLLMENT_PENDING = "enrollment_pending",
  ACTIVE = "active",
  SUSPENDED = "suspended",
  COMPROMISED = "compromised",
  REPLACEMENT_REQUIRED = "replacement_required",
  REVOKED = "revoked"
}

export enum CeremonyType {
  SIGN_IN = "sign_in",
  STEP_UP = "step_up",
  RECOVERY = "recovery",
  ENROLLMENT = "enrollment",
  REPLACEMENT = "replacement",
  REMOVAL = "removal"
}

export enum CeremonyStatus {
  READY = "ready",
  SUBMITTING = "submitting",
  INVALID_RESPONSE = "invalid_response",
  RATE_LIMITED = "rate_limited",
  ATTEMPTS_EXHAUSTED = "attempts_exhausted",
  EXPIRED = "expired",
  BLOCKED = "blocked",
  SUCCESS = "success",
  REQUIRES_NEXT_STEP = "requires_next_step",
  CANCELLED = "cancelled",
  PROVIDER_UNAVAILABLE = "provider_unavailable"
}

export enum AssuranceLevel {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high"
}

export interface KbaQuestion {
  id: string;
  category: string;
  text: string;
  isCustomAllowed?: boolean;
}

export interface KbaAnswerEnrollment {
  questionId: string;
  questionText: string;
  normalizedHash: string; // Simulated SHA-256 hash
}

export interface KbaUserCredential {
  status: AuthenticatorStatus;
  enrollmentDate: string | null;
  lastUsedDate: string | null;
  enrolledQuestions: KbaAnswerEnrollment[];
  failureCount: number;
  lockoutUntil: string | null;
}

export interface TenantPolicy {
  isKbaProhibited: boolean;
  minAssuranceRequired: AssuranceLevel;
  maxAttempts: number;
  lockoutDurationMinutes: number;
  sessionFreshnessSeconds: number;
  allowCustomQuestions: boolean;
  requiredQuestionCount: number;
  questionSource: string;
  fallbackFactors: string[];
}

export interface ProviderConfig {
  id: string;
  name: string;
  sourceType: "internal" | "external_credit" | "utility_records" | "identity_bureau";
  encryptionAlgorithm: string;
  keyRotationDate: string;
  healthStatus: "healthy" | "degraded" | "outage";
  regionalAvailability: string[];
}

export interface AuditEvent {
  id: string;
  timestamp: string;
  userEmail: string;
  action: string; // e.g., "challenge_attempt", "enrollment_completed", "policy_updated", "compromise_response"
  ceremonyType: CeremonyType;
  status: CeremonyStatus | "completed" | "failed";
  providerId: string;
  details: string; // Sanitized metadata without questions/answers
  ipAddress: string;
  assuranceLevel: AssuranceLevel;
}
