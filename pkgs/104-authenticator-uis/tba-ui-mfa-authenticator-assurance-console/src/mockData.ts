/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { MfaFactor, MfaPolicy, UserPosture, AuditEvent, ProviderHealth } from './types';

export const INITIAL_FACTORS: MfaFactor[] = [
  {
    id: 'f-1',
    name: 'MacBook TouchID',
    type: 'passkey',
    status: 'active',
    enrolledAt: '2026-03-12T08:30:00Z',
    lastUsedAt: '2026-07-15T09:44:00Z',
    deviceName: 'MacBook Pro 16"',
    phishingResistant: true,
    factorClass: 'Inherence',
  },
  {
    id: 'f-2',
    name: 'YubiKey 5C NFC',
    type: 'security_key',
    status: 'active',
    enrolledAt: '2026-01-05T14:22:00Z',
    lastUsedAt: '2026-07-11T16:15:00Z',
    deviceName: 'YubiKey 5C',
    phishingResistant: true,
    factorClass: 'Possession',
  },
  {
    id: 'f-3',
    name: 'Microsoft Authenticator',
    type: 'totp',
    status: 'active',
    enrolledAt: '2025-08-20T10:11:00Z',
    lastUsedAt: '2026-07-15T10:20:00Z',
    deviceName: 'iPhone 15 Pro',
    phishingResistant: false,
    factorClass: 'Knowledge',
  },
  {
    id: 'f-4',
    name: 'Company Email OTP',
    type: 'email_otp',
    status: 'active',
    enrolledAt: '2025-08-20T09:00:00Z',
    lastUsedAt: '2026-07-15T08:12:00Z',
    deviceName: 'Webmail',
    phishingResistant: false,
    factorClass: 'Possession',
  },
  {
    id: 'f-5',
    name: 'Duo Mobile Push',
    type: 'push',
    status: 'active',
    enrolledAt: '2026-02-18T11:45:00Z',
    lastUsedAt: '2026-07-14T15:30:00Z',
    deviceName: 'iPhone 15 Pro',
    phishingResistant: false,
    factorClass: 'Possession',
  },
  {
    id: 'f-6',
    name: 'Emergency Offline recovery codes',
    type: 'recovery',
    status: 'active',
    enrolledAt: '2026-03-12T08:35:00Z',
    lastUsedAt: null,
    phishingResistant: false,
    factorClass: 'Knowledge',
  }
];

export const INITIAL_POLICIES: MfaPolicy[] = [
  {
    id: 'p-1',
    version: 3,
    requiredClasses: ['Possession', 'Knowledge'],
    allowGracePeriod: true,
    gracePeriodDays: 14,
    rememberDeviceDays: 30,
    lockoutThreshold: 5,
    sessionTimeoutMinutes: 15,
    enforcePhishingResistant: true,
    allowedFactorTypes: ['passkey', 'security_key', 'totp', 'push', 'email_otp'],
  },
  {
    id: 'p-2',
    version: 1,
    requiredClasses: ['Possession'],
    allowGracePeriod: true,
    gracePeriodDays: 30,
    rememberDeviceDays: 90,
    lockoutThreshold: 10,
    sessionTimeoutMinutes: 60,
    enforcePhishingResistant: false,
    allowedFactorTypes: ['passkey', 'security_key', 'totp', 'push', 'email_otp'],
  }
];

export const INITIAL_USER_POSTURES: UserPosture[] = [
  {
    id: 'u-1',
    name: 'Jane Doe',
    email: 'jane.doe@acme.com',
    enrollmentStatus: 'fully_enrolled',
    factorsCount: 4,
    factors: [
      { ...INITIAL_FACTORS[0] }, // TouchID
      { ...INITIAL_FACTORS[1] }, // YubiKey
      { ...INITIAL_FACTORS[2] }, // TOTP
      { ...INITIAL_FACTORS[5] }, // Recovery codes
    ],
    graceExpiresAt: null,
    recoveryEligible: true,
    lastMfaTime: '2026-07-15T09:44:00Z',
  },
  {
    id: 'u-2',
    name: 'John Smith',
    email: 'john.smith@acme.com',
    enrollmentStatus: 'partially_enrolled',
    factorsCount: 2,
    factors: [
      { ...INITIAL_FACTORS[2] }, // TOTP only
      { ...INITIAL_FACTORS[3] }, // Email OTP
    ],
    graceExpiresAt: null,
    recoveryEligible: true,
    lastMfaTime: '2026-07-15T08:12:00Z',
  },
  {
    id: 'u-3',
    name: 'Alice Vance',
    email: 'alice.vance@acme.com',
    enrollmentStatus: 'grace_period',
    factorsCount: 1,
    factors: [
      { ...INITIAL_FACTORS[3] }, // Email OTP only
    ],
    graceExpiresAt: '2026-07-29T10:33:00Z',
    recoveryEligible: false,
    lastMfaTime: null,
  },
  {
    id: 'u-4',
    name: 'Bob Lee',
    email: 'bob.lee@acme.com',
    enrollmentStatus: 'no_enrollment',
    factorsCount: 0,
    factors: [],
    graceExpiresAt: null,
    recoveryEligible: false,
    lastMfaTime: null,
  }
];

export const INITIAL_PROVIDER_HEALTH: ProviderHealth[] = [
  {
    name: 'FIDO2 / WebAuthn Service',
    type: 'passkey',
    status: 'operational',
    maturity: 'high',
    ceremonyModes: ['Passkey', 'Security Key', 'Platform Biometrics'],
    latencyMs: 14,
  },
  {
    name: 'TOTP Code Engine',
    type: 'totp',
    status: 'operational',
    maturity: 'high',
    ceremonyModes: ['RFC-6238 TOTP'],
    latencyMs: 4,
  },
  {
    name: 'Transactional Push Service',
    type: 'push',
    status: 'operational',
    maturity: 'medium',
    ceremonyModes: ['Push Approval Callbacks', 'Interactive Prompt'],
    latencyMs: 120,
  },
  {
    name: 'Corporate SMTP / OTP Gateway',
    type: 'email_otp',
    status: 'degraded',
    maturity: 'medium',
    ceremonyModes: ['Email Pin Delivery'],
    latencyMs: 820,
  },
  {
    name: 'Cryptographic Key Manager (HSM)',
    type: 'core',
    status: 'operational',
    maturity: 'high',
    ceremonyModes: ['Independence Evaluator', 'Token Signing'],
    latencyMs: 2,
  }
];

export const INITIAL_AUDIT_EVENTS: AuditEvent[] = [
  {
    id: 'evt-1',
    timestamp: '2026-07-15T10:20:15Z',
    eventType: 'CEREMONY_START',
    subject: 'jane.doe@acme.com',
    status: 'info',
    policyVersion: 3,
    detail: 'MFA assurance ceremony initiated for transaction "sensitive_fund_transfer"',
    ipAddress: '192.168.1.45',
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0',
  },
  {
    id: 'evt-2',
    timestamp: '2026-07-15T10:20:45Z',
    eventType: 'FACTOR_EVALUATED',
    subject: 'jane.doe@acme.com',
    status: 'success',
    factorType: 'passkey',
    factorClass: 'Inherence',
    policyVersion: 3,
    detail: 'Passkey verification succeeded (phishing-resistant, hardware-backed TouchID)',
    ipAddress: '192.168.1.45',
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0',
  },
  {
    id: 'evt-3',
    timestamp: '2026-07-15T10:21:02Z',
    eventType: 'CEREMONY_COMPLETE',
    subject: 'jane.doe@acme.com',
    status: 'success',
    policyVersion: 3,
    detail: 'MFA criteria satisfied with independent classes Inherence + Knowledge. AMR token issued.',
    ipAddress: '192.168.1.45',
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0',
  },
  {
    id: 'evt-4',
    timestamp: '2026-07-15T10:25:30Z',
    eventType: 'ENROLLMENT_STARTED',
    subject: 'alice.vance@acme.com',
    status: 'info',
    policyVersion: 3,
    detail: 'Required MFA enrollment triggered for user in grace period.',
    ipAddress: '172.56.21.90',
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) Mobile/15E148',
  }
];

export function getStoredState<T>(key: string, defaultValue: T): T {
  try {
    const item = localStorage.getItem(`mfa_console_${key}`);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error('Error reading localStorage', error);
    return defaultValue;
  }
}

export function setStoredState<T>(key: string, value: T): void {
  try {
    localStorage.setItem(`mfa_console_${key}`, JSON.stringify(value));
  } catch (error) {
    console.error('Error writing localStorage', error);
  }
}
