/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { PasswordPolicy, UserAccount, SecurityEvent, SessionEvidence, BreachedSecretMatch } from "./types";

// Standard simulated password policy
export const DEFAULT_POLICY: PasswordPolicy = {
  minLength: 12,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecial: true,
  blocklist: ["password123", "qwerty123456", "admin12345", "welcome123"],
  blockBreachedSecrets: true,
  maxAttempts: 5,
  rateLimitWindowsMs: 60000, // 1 minute
  forceResetIntervalDays: 90,
};

// Default user account for simulation
export const DEFAULT_USER: UserAccount = {
  email: "user@enterprise.com",
  fullName: "Alex Rivera",
  passwordHash: "SecureP@ss1234", // Plaintxt representation for local simulation simplicity
  passwordCreatedDate: "2026-04-15T09:00:00-07:00",
  passwordChangedDate: "2026-04-15T09:00:00-07:00",
  passwordLastUsedDate: "2026-07-14T18:22:11-07:00",
  isPasswordRequired: true,
  hasMfaEnabled: true,
  hasWebAuthnEnabled: false,
  failedAttempts: 0,
  isLocked: false,
  isCompromised: false,
  isExpired: false,
  needsForcedChange: false,
  accountStatus: "active",
};

// Pre-populated security events audit logs
export const DEFAULT_EVENTS: SecurityEvent[] = [
  {
    id: "evt-001",
    timestamp: "2026-07-15T10:15:30-07:00",
    eventType: "sign_in_success",
    severity: "info",
    description: "Successful login using AMR 'pwd'",
    ipAddress: "192.168.1.45",
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0",
    redactedDetails: "Assurance Level: AAL1, factor: password",
  },
  {
    id: "evt-002",
    timestamp: "2026-07-15T08:12:11-07:00",
    eventType: "password_compromise_detected",
    severity: "critical",
    description: "Password matching active breached-secret telemetry detected on separate external audit",
    ipAddress: "System",
    userAgent: "Breach-Watch Monitor v4.1",
    redactedDetails: "Database matching SHA-1 suffix blocklist check triggered",
  },
  {
    id: "evt-003",
    timestamp: "2026-07-14T22:45:00-07:00",
    eventType: "sign_in_failure",
    severity: "warning",
    description: "Failed password credential attempt",
    ipAddress: "203.0.113.12",
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    redactedDetails: "Redacted credentials mismatch, failure threshold: 1/5",
  },
  {
    id: "evt-004",
    timestamp: "2026-07-14T14:30:12-07:00",
    eventType: "policy_updated",
    severity: "info",
    description: "Password policy modified by tenant administrator",
    ipAddress: "10.0.2.11",
    userAgent: "AdminPortal/v2.4.0",
    redactedDetails: "Minimum length changed from 10 to 12. Breached check enabled.",
  },
];

// Helper to evaluate password requirements
export interface PolicyEvaluation {
  passed: boolean;
  lengthOk: boolean;
  upperOk: boolean;
  lowerOk: boolean;
  numberOk: boolean;
  specialOk: boolean;
  notInBlocklist: boolean;
  notBreached: boolean;
  similarityOk: boolean;
}

export function evaluatePassword(password: string, policy: PasswordPolicy, userEmail?: string): PolicyEvaluation {
  const lengthOk = password.length >= policy.minLength;
  const upperOk = !policy.requireUppercase || /[A-Z]/.test(password);
  const lowerOk = !policy.requireLowercase || /[a-z]/.test(password);
  const numberOk = !policy.requireNumbers || /[0-9]/.test(password);
  const specialOk = !policy.requireSpecial || /[^A-Za-z0-9]/.test(password);
  
  // Custom quick similarity check (not same as email)
  const similarityOk = !userEmail || !password.toLowerCase().includes(userEmail.split("@")[0].toLowerCase());
  
  // Blocklist check
  const notInBlocklist = !policy.blocklist.some(b => password.toLowerCase().includes(b.toLowerCase()));
  
  // Simulated breached-secret service (common simple bad passwords in breach lists)
  const commonBreachedText = ["12345678", "password", "qwerty", "letmein", "sunshine", "iloveyou", "admin", "welcome"];
  const notBreached = !policy.blockBreachedSecrets || !commonBreachedText.some(b => password.toLowerCase().includes(b));

  const passed = lengthOk && upperOk && lowerOk && numberOk && specialOk && similarityOk && notInBlocklist && notBreached;

  return {
    passed,
    lengthOk,
    upperOk,
    lowerOk,
    numberOk,
    specialOk,
    notInBlocklist,
    notBreached,
    similarityOk
  };
}

// Breached secret database representation (P2 diagnostics detail)
export const BREACHED_DATABASE_SAMPLE: BreachedSecretMatch[] = [
  { passwordText: "password123", occurrenceCount: 4210982, recommendation: "Extremely common credential. Immediate revocation required." },
  { passwordText: "welcome123", occurrenceCount: 890122, recommendation: "Common default bootstrap password. Blocked from system entry." },
  { passwordText: "12345678", occurrenceCount: 15309481, recommendation: "Top globally breached credential. Critical threat rating." },
  { passwordText: "letmein1", occurrenceCount: 204910, recommendation: "Common dictionary entry. Blocked by entropy checks." }
];
