/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export enum CeremonyState {
  IDLE = 'idle',
  ELIGIBILITY_LOADING = 'eligibility_loading',
  READY = 'ready',
  AWAITING_DEVICE = 'awaiting_device',
  INSERT_GUIDANCE = 'insert_guidance',
  TOUCH_GUIDANCE = 'touch_guidance',
  PROCESSING = 'processing',
  PRESENCE_ABSENT = 'presence_absent',
  UV_REQUIRED = 'uv_required',
  CANCELLED = 'cancelled',
  TIMEOUT = 'timeout',
  DEVICE_REMOVED = 'device_removed',
  TRANSPORT_UNAVAILABLE = 'transport_unavailable',
  UNSUPPORTED_ENVIRONMENT = 'unsupported_environment',
  INVALID_ASSERTION = 'invalid_assertion',
  REPLAY_DETECTED = 'replay_detected',
  POLICY_CHANGED = 'policy_changed',
  EXPIRED = 'expired',
  BLOCKED = 'blocked',
  SUCCESS = 'success',
  REQUIRES_NEXT_STEP = 'requires_next_step',
}

export type AuthenticatorType = 'passkey' | 'security_key' | 'managed_key';
export type TransportType = 'internal' | 'usb' | 'nfc' | 'ble';

export interface Authenticator {
  id: string;
  name: string;
  type: AuthenticatorType;
  transport: TransportType;
  upSupported: boolean; // User Presence
  uvSupported: boolean; // User Verification
  hardwareBacked: boolean;
  aaguid: string;
  createdAt: string;
  lastUsedAt: string | null;
  signatureCount: number;
}

export interface PresencePolicy {
  id: string;
  name: string;
  presenceRequired: boolean;
  uvRequired: boolean;
  phishingResistant: boolean;
  hardwareBacked: boolean;
  maxAuthAgeSeconds: number;
  appScope: string;
}

export interface ManagedKeyProfile {
  id: string;
  name: string;
  allowedTransports: TransportType[];
  enforceHardwareBacking: boolean;
  allowedAaguids: string[];
  requireFreshnessSeconds: number;
}

export interface CeremonyEvidence {
  id: string;
  timestamp: string;
  authenticatorId: string;
  authenticatorName: string;
  authenticatorType: AuthenticatorType;
  transport: TransportType;
  purpose: string;
  userPresent: boolean;
  userVerified: boolean;
  modality: 'touch' | 'biometric' | 'pin' | 'unknown' | 'none';
  origin: string;
  rpId: string;
  clientDataHash: string;
  signature: string;
  counter: number;
  policySatisfied: boolean;
  auditReference: string;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  event: string;
  category: 'auth' | 'enrollment' | 'policy' | 'lifecycle' | 'error';
  status: 'success' | 'failure' | 'warning' | 'info';
  details: string;
  auditReference: string;
}

export interface PreflightCheck {
  id: string;
  name: string;
  description: string;
  status: 'pass' | 'fail' | 'warning' | 'unchecked';
  value: string;
}
