/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type FactorClass = 'Knowledge' | 'Possession' | 'Inherence';

export type FactorType = 'totp' | 'passkey' | 'security_key' | 'push' | 'email_otp' | 'recovery';

export interface MfaFactor {
  id: string;
  name: string;
  type: FactorType;
  status: 'active' | 'suspended' | 'replacement_required';
  enrolledAt: string;
  lastUsedAt: string | null;
  deviceName?: string;
  phishingResistant: boolean;
  factorClass: FactorClass;
}

export interface MfaPolicy {
  id: string;
  version: number;
  requiredClasses: FactorClass[];
  allowGracePeriod: boolean;
  gracePeriodDays: number;
  rememberDeviceDays: number;
  lockoutThreshold: number;
  sessionTimeoutMinutes: number;
  enforcePhishingResistant: boolean;
  allowedFactorTypes: FactorType[];
}

export type CeremonyStatus =
  | 'intro'
  | 'chooser'
  | 'challenge'
  | 'external_wait'
  | 'success'
  | 'failed_blocked'
  | 'recovery'
  | 'enrollment_required';

export interface MfaCeremony {
  id: string;
  status: CeremonyStatus;
  purpose: string; // e.g. "Sensitive transaction authorization", "Regular sign-in"
  requiredClasses: FactorClass[];
  achievedClasses: FactorClass[];
  eligibleFactors: MfaFactor[];
  currentFactor?: MfaFactor;
  attemptsRemaining: number;
  expiresInSeconds: number;
  allowMethodSwitch: boolean;
  recoveryMode: boolean;
  reducedAssurance: boolean;
  amr: string[];
  auditReference: string;
}

export interface AuditEvent {
  id: string;
  timestamp: string;
  eventType: string;
  subject: string;
  status: 'success' | 'failure' | 'warning' | 'info';
  factorType?: FactorType;
  factorClass?: FactorClass;
  policyVersion?: number;
  detail: string;
  ipAddress: string;
  userAgent: string;
}

export interface UserPosture {
  id: string;
  name: string;
  email: string;
  enrollmentStatus: 'fully_enrolled' | 'partially_enrolled' | 'no_enrollment' | 'grace_period';
  factorsCount: number;
  factors: MfaFactor[];
  graceExpiresAt: string | null;
  recoveryEligible: boolean;
  lastMfaTime: string | null;
}

export interface ProviderHealth {
  name: string;
  type: FactorType | 'core';
  status: 'operational' | 'degraded' | 'outage';
  maturity: 'high' | 'medium' | 'low';
  ceremonyModes: string[];
  latencyMs: number;
}
