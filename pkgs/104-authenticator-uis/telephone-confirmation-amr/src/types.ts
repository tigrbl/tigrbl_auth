/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface PhoneAuthenticator {
  id: string;
  label: string;
  rawNumber: string;
  maskedNumber: string;
  countryCode: string;
  verifiedAt: string;
  createdAt: string;
  lastUsedAt?: string;
  status: 'active' | 'suspended' | 'replacement_pending';
}

export type CallState =
  | 'idle'
  | 'queued'
  | 'ringing'
  | 'connected'
  | 'ivr_active'
  | 'awaiting_code'
  | 'completed'
  | 'busy'
  | 'no_answer'
  | 'voicemail'
  | 'rejected'
  | 'failed'
  | 'expired'
  | 'rate_limited'
  | 'blocked';

export interface CallContext {
  id: string;
  type: 'enrollment' | 'login' | 'step_up';
  destination: string;
  maskedDestination: string;
  verificationCode: string; // The code the user hears or needs to enter
  ivrMode: 'code_read' | 'approval_press'; // 'code_read': IVR reads code, user enters on web; 'approval_press': IVR asks to press 1 to approve on phone
  timer: number;
  maxTimer: number;
  transactionPurpose: string;
  status: CallState;
  provider: string;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  eventType: string; // 'ENROLLMENT_START' | 'IVR_APPROVED' | 'OTP_MATCHED' | 'RATE_LIMIT_EXCEEDED' | 'PROVIDER_FAILOVER' etc.
  details: string;
  status: 'success' | 'failure' | 'warning' | 'info';
  ipAddress: string;
  maskedNumber?: string;
}

export interface TelephonePolicy {
  allowedRegions: string[]; // ['US', 'CA', 'GB', 'FR', 'DE', 'AU']
  quietHoursStart: string; // '22:00'
  quietHoursEnd: string; // '07:00'
  maxAttempts: number; // e.g., 3
  callDurationSeconds: number; // e.g., 60
  lockoutDurationMinutes: number; // e.g., 15
  requireApprovalMode: 'any' | 'ivr_keypad' | 'web_otp_only' | 'both';
  enableVoicemailDetection: boolean;
  allowReducedAssuranceRecovery: boolean;
}

export interface ProviderConfig {
  activeProvider: string; // 'twillo_telecom' | 'infobip_voice' | 'custom_sip'
  callerIdName: string;
  callerIdNumber: string;
  language: string; // 'en-US' | 'es-ES' | 'fr-FR' | 'de-DE'
  voiceType: 'male' | 'female' | 'neural_assistant';
  retryFailoverEnabled: boolean;
  callbackUrl: string;
  fallbackProvider: string;
}

export interface CallStats {
  totalCalls: number;
  completed: number;
  abandoned: number;
  busyNoAnswer: number;
  voicemailBlocked: number;
  fraudAlerts: number;
  estimatedCost: number;
}
