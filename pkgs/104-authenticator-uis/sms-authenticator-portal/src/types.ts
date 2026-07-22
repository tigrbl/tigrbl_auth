/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type DeliveryState = 'queued' | 'delivered' | 'delayed' | 'failed' | 'unknown';

export interface Country {
  code: string;
  name: string;
  dialCode: string;
  flag: string;
  isAllowed: boolean;
  costPerSms: number;
}

export interface SmsProvider {
  id: string;
  name: string;
  status: 'active' | 'degraded' | 'offline';
  routingWeight: number; // percentage
  costPerSms: number;
  totalSent: number;
  totalFailed: number;
  avgLatencyMs: number;
}

export interface SmsLog {
  id: string;
  timestamp: string;
  recipient: string;
  maskedRecipient: string;
  code: string;
  providerId: string;
  state: DeliveryState;
  latencyMs: number;
  carrier: string;
  simSwapRisk: 'low' | 'medium' | 'high';
  isPumpingRisk: boolean;
  purpose: 'enrollment' | 'authentication' | 'step-up' | 'recovery';
}

export interface SmsPolicy {
  allowedCountries: string[]; // country codes
  maxAttempts: number;
  codeExpiryMinutes: number;
  resendDelaySeconds: number;
  smsCostLimitMonthly: number;
  minAssuranceLevel: 'low' | 'none'; // SMS is inherently lower assurance
  simChangeBlock: boolean;
  pumpingProtection: boolean;
  defaultTemplate: string;
}

export interface SmsTemplate {
  id: string;
  name: string;
  purpose: 'enrollment' | 'authentication' | 'step-up' | 'recovery';
  body: string;
}

export interface EnrolledPhone {
  id: string;
  label: string;
  countryCode: string;
  number: string;
  maskedNumber: string;
  verifiedAt: string;
  lastUsedAt: string;
  status: 'active' | 'suspended';
}

export interface AuditLog {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  category: 'enrollment' | 'authentication' | 'policy' | 'provider' | 'abuse';
  details: string;
  severity: 'info' | 'warning' | 'critical';
}

export interface SmsCeremonySession {
  id: string;
  type: 'enroll' | 'login' | 'step-up' | 'replace' | 'recovery';
  phoneNumber: string;
  countryCode: string;
  dialCode: string;
  maskedNumber: string;
  label?: string; // used for enrollment naming
  state: 'idle' | 'introduction' | 'entry' | 'send_pending' | 'otp_waiting' | 'completed' | 'failed';
  subState: 'ready' | 'queued' | 'delivered' | 'delayed' | 'failed' | 'invalid' | 'expired' | 'rate-limited' | 'blocked';
  generatedCode: string;
  attemptsCount: number;
  resendCountdown: number;
  expiryCountdown: number;
  providerId: string;
  purpose: 'enrollment' | 'authentication' | 'step-up' | 'recovery';
  simSwapRiskDetected?: boolean;
}
