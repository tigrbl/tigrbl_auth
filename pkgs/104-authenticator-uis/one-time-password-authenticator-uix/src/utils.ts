/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { OtpAlgorithm, FactorStatus, AuthenticatorProfile, AuditLog, TenantPolicy } from "./types";

// A simple, deterministic custom hashing function that maps a string to a 32-bit positive integer
export function customHash(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
}

// Generates a mock Base32 secret string (20 chars)
export function generateBase32Secret(): string {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
  let result = "";
  for (let i = 0; i < 16; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

// Pure client-side TOTP-like generator
export function generateTOTP(
  secret: string,
  timeSkewSeconds: number = 0,
  period: number = 30,
  digits: number = 6
): string {
  const epoch = Math.floor((Date.now() / 1000) + timeSkewSeconds);
  const counter = Math.floor(epoch / period);
  const hashInput = `${secret}-${counter}`;
  const h = customHash(hashInput);
  const code = h % Math.pow(10, digits);
  return code.toString().padStart(digits, "0");
}

// Verifies a client-side TOTP with support for skew, replay store, and custom parameters
export function verifyTOTP(
  inputCode: string,
  secret: string,
  timeSkewSeconds: number = 0,
  period: number = 30,
  digits: number = 6,
  driftWindow: number = 1, // number of intervals allowed backward/forward
  replayStore: Set<string> = new Set()
): { 
  success: boolean; 
  driftSteps?: number; 
  error?: "expired" | "replay" | "invalid" | "rate_limited" 
} {
  // Validate basic format
  if (!inputCode || inputCode.length !== digits || !/^\d+$/.test(inputCode)) {
    return { success: false, error: "invalid" };
  }

  // Check if code has been replayed
  if (replayStore.has(inputCode)) {
    return { success: false, error: "replay" };
  }

  const epoch = Math.floor((Date.now() / 1000) + timeSkewSeconds);
  const currentCounter = Math.floor(epoch / period);

  // Search within drift windows
  for (let d = -driftWindow; d <= driftWindow; d++) {
    const counter = currentCounter + d;
    const hashInput = `${secret}-${counter}`;
    const h = customHash(hashInput);
    const expectedCode = (h % Math.pow(10, digits)).toString().padStart(digits, "0");
    if (expectedCode === inputCode) {
      return { success: true, driftSteps: d };
    }
  }

  return { success: false, error: "invalid" };
}

// Pre-seeded recovery codes
export function generateRecoveryCodes(): string[] {
  const codes: string[] = [];
  for (let i = 0; i < 8; i++) {
    const segment1 = Math.floor(1000 + Math.random() * 9000).toString();
    const segment2 = Math.floor(1000 + Math.random() * 9000).toString();
    codes.push(`${segment1}-${segment2}`);
  }
  return codes;
}

// Helper to format timestamps gracefully
export function formatTime(isoString: string): string {
  try {
    const d = new Date(isoString);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch (e) {
    return isoString;
  }
}

// Default initial data for simulation state
export const DEFAULT_POLICY: TenantPolicy = {
  allowedAlgorithms: [OtpAlgorithm.SHA1, OtpAlgorithm.SHA256],
  allowedDigits: [6, 8],
  allowedPeriods: [30, 60],
  attemptsLimit: 5,
  rateLimitWindow: 60,
  replayStoreExpiry: 300,
  driftWindowGrace: 1,
  stepUpTimeout: 120,
  forceMfa: true,
  allowFallback: true,
};

export const INITIAL_AUTHENTICATORS: AuthenticatorProfile[] = [
  {
    id: "auth-totp-1",
    label: "Work iPhone 15",
    type: "totp",
    status: FactorStatus.ACTIVE,
    secret: "N7JZ2K3XNBPV9Y7A",
    digits: 6,
    period: 30,
    algorithm: OtpAlgorithm.SHA1,
    created: new Date(Date.now() - 30 * 24 * 3600 * 1000).toISOString(),
    lastUsed: new Date(Date.now() - 2 * 3600 * 1000).toISOString(),
  },
  {
    id: "auth-sms-1",
    label: "SMS Backup Line",
    type: "sms",
    status: FactorStatus.ACTIVE,
    secret: "SMS_SECRET_PLACEHOLDER",
    digits: 6,
    period: 60,
    algorithm: OtpAlgorithm.SHA1,
    created: new Date(Date.now() - 45 * 24 * 3600 * 1000).toISOString(),
    lastUsed: new Date(Date.now() - 10 * 24 * 3600 * 1000).toISOString(),
    deliveryTarget: "+1 (555) 019-2834",
  },
  {
    id: "auth-email-1",
    label: "Corporate Email Factor",
    type: "email",
    status: FactorStatus.ACTIVE,
    secret: "EMAIL_SECRET_PLACEHOLDER",
    digits: 6,
    period: 60,
    algorithm: OtpAlgorithm.SHA1,
    created: new Date(Date.now() - 60 * 24 * 3600 * 1000).toISOString(),
    lastUsed: new Date(Date.now() - 15 * 24 * 3600 * 1000).toISOString(),
    deliveryTarget: "j.austin@enterprise.com",
  }
];

export const INITIAL_AUDIT_LOGS: AuditLog[] = [
  {
    id: "log-1",
    timestamp: new Date(Date.now() - 2.5 * 3600 * 1000).toISOString(),
    eventType: "AUTH_SUCCESS",
    actor: "j.austin@enterprise.com",
    details: "MFA challenge verified successfully via Work iPhone 15 (TOTP)",
    status: "success",
    ipAddress: "192.168.1.45",
    requestId: "req-9a8b7c6d",
  },
  {
    id: "log-2",
    timestamp: new Date(Date.now() - 2.5 * 3600 * 1000).toISOString(),
    eventType: "DRIFT_CORRECTED",
    actor: "j.austin@enterprise.com",
    details: "TOTP skew corrected by +1 period on Work iPhone 15",
    status: "info",
    ipAddress: "192.168.1.45",
    requestId: "req-9a8b7c6d",
  },
  {
    id: "log-3",
    timestamp: new Date(Date.now() - 5 * 3600 * 1000).toISOString(),
    eventType: "POLICY_UPDATE",
    actor: "admin@enterprise.com",
    details: "Tenant policy updated: enforced minimum digits size to 6",
    status: "warning",
    ipAddress: "10.0.1.12",
    requestId: "req-0f1e2d3c",
  }
];
