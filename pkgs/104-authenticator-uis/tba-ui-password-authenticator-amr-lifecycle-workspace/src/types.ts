/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type AuthScreenId =
  | "identifier-first"
  | "password-entry"
  | "step-up"
  | "create-password"
  | "requirements-explanation"
  | "change-password"
  | "forced-change"
  | "forgot-password"
  | "reset-link-received"
  | "reset-completion"
  | "invalid-reset"
  | "compromised-response"
  | "password-detail"
  | "disable-remove"
  | "evidence-detail"
  | "policy-editor"
  | "user-posture"
  | "security-events"
  | "native-password";

export interface PasswordPolicy {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecial: boolean;
  blocklist: string[];
  blockBreachedSecrets: boolean;
  maxAttempts: number;
  rateLimitWindowsMs: number;
  forceResetIntervalDays: number;
}

export interface UserAccount {
  email: string;
  fullName: string;
  passwordHash: string; // simulated
  passwordCreatedDate: string;
  passwordChangedDate: string;
  passwordLastUsedDate: string;
  isPasswordRequired: boolean;
  hasMfaEnabled: boolean;
  hasWebAuthnEnabled: boolean;
  failedAttempts: number;
  isLocked: boolean;
  lockoutTime?: string;
  isCompromised: boolean;
  isExpired: boolean;
  needsForcedChange: boolean;
  accountStatus: "active" | "suspended" | "disabled";
}

export interface SecurityEvent {
  id: string;
  timestamp: string;
  eventType:
    | "sign_in_success"
    | "sign_in_failure"
    | "lockout"
    | "password_change"
    | "password_compromise_detected"
    | "forced_change_triggered"
    | "forced_change_completed"
    | "forgot_password_request"
    | "reset_link_validated"
    | "reset_completed"
    | "password_disabled"
    | "admin_action"
    | "policy_updated";
  severity: "info" | "warning" | "critical";
  description: string;
  ipAddress: string;
  userAgent: string;
  redactedDetails?: string;
}

export interface SessionEvidence {
  token: string;
  amr: string[]; // e.g. ["pwd"], ["pwd", "mfa"], ["hw"]
  subject: string;
  authenticatedAt: string;
  freshnessSeconds: number;
  purpose: string;
  assuranceLevel: "AAL1" | "AAL2" | "AAL3";
  isStepUpVerified: boolean;
}

export interface BreachedSecretMatch {
  passwordText: string;
  occurrenceCount: number;
  recommendation: string;
}
