/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { TelephonePolicy, ProviderConfig, PhoneAuthenticator, CallStats, AuditLog } from './types';

export const COUNTRIES = [
  { code: 'US', name: 'United States', prefix: '+1', pattern: ' (###) ###-####' },
  { code: 'CA', name: 'Canada', prefix: '+1', pattern: ' (###) ###-####' },
  { code: 'GB', name: 'United Kingdom', prefix: '+44', pattern: ' #### ######' },
  { code: 'FR', name: 'France', prefix: '+33', pattern: ' # ## ## ## ##' },
  { code: 'DE', name: 'Germany', prefix: '+49', pattern: ' #### #######' },
  { code: 'AU', name: 'Australia', prefix: '+61', pattern: ' ### ### ###' },
  { code: 'JP', name: 'Japan', prefix: '+81', pattern: ' ##-####-####' },
  { code: 'IN', name: 'India', prefix: '+91', pattern: ' #####-#####' },
  { code: 'BR', name: 'Brazil', prefix: '+55', pattern: ' (##) #####-####' },
];

export const INITIAL_POLICIES: TelephonePolicy = {
  allowedRegions: ['US', 'CA', 'GB', 'FR', 'DE', 'AU'],
  quietHoursStart: '22:00',
  quietHoursEnd: '07:00',
  maxAttempts: 3,
  callDurationSeconds: 60,
  lockoutDurationMinutes: 15,
  requireApprovalMode: 'both', // Requires IVR keypad press 1, then entering code on web/app
  enableVoicemailDetection: true,
  allowReducedAssuranceRecovery: true,
};

export const INITIAL_PROVIDERS: ProviderConfig = {
  activeProvider: 'twilio_telecom',
  callerIdName: 'Acme Auth Gate',
  callerIdNumber: '+1 (888) 555-0199',
  language: 'en-US',
  voiceType: 'neural_assistant',
  retryFailoverEnabled: true,
  callbackUrl: 'https://api.acme-identity.com/v1/telephony/callback',
  fallbackProvider: 'infobip_voice',
};

export const INITIAL_AUTHENTICATORS: PhoneAuthenticator[] = [
  {
    id: 'auth-1',
    label: 'Primary Personal Mobile',
    rawNumber: '+15550198812',
    maskedNumber: '+1 (555) •••-•812',
    countryCode: 'US',
    verifiedAt: '2026-05-12T14:32:00Z',
    createdAt: '2026-05-12T14:30:00Z',
    lastUsedAt: '2026-07-14T09:22:15Z',
    status: 'active',
  },
  {
    id: 'auth-2',
    label: 'Work Office Landline (Fallback)',
    rawNumber: '+447700900077',
    maskedNumber: '+44 •••• ••0077',
    countryCode: 'GB',
    verifiedAt: '2026-06-20T10:11:00Z',
    createdAt: '2026-06-20T10:05:00Z',
    lastUsedAt: '2026-07-01T15:44:02Z',
    status: 'active',
  },
];

export const INITIAL_STATS: CallStats = {
  totalCalls: 1248,
  completed: 1042,
  abandoned: 98,
  busyNoAnswer: 62,
  voicemailBlocked: 34,
  fraudAlerts: 12,
  estimatedCost: 24.96, // $0.02 per call avg
};

export const INITIAL_AUDIT_LOGS: AuditLog[] = [
  {
    id: 'log-1',
    timestamp: '2026-07-15T10:12:00-07:00',
    eventType: 'TEL_CHALLENGE_SUCCESS',
    details: 'MFA call verified for user admin@acme.com via +1 (555) •••-•812. Provider: twilio_telecom.',
    status: 'success',
    ipAddress: '198.51.100.42',
    maskedNumber: '+1 (555) •••-•812',
  },
  {
    id: 'log-2',
    timestamp: '2026-07-15T09:44:12-07:00',
    eventType: 'TEL_RATE_LIMIT_TRIGGERED',
    details: 'Max call attempts exceeded for country prefix +91. Temporary cooldown applied.',
    status: 'warning',
    ipAddress: '203.0.113.88',
  },
  {
    id: 'log-3',
    timestamp: '2026-07-15T08:15:33-07:00',
    eventType: 'TEL_VOICEMAIL_DETECTED',
    details: 'Incoming call dropped: Voicemail tone detected via carrier signaling. Call marked as failed.',
    status: 'failure',
    ipAddress: '198.51.100.12',
    maskedNumber: '+1 (555) •••-•812',
  },
  {
    id: 'log-4',
    timestamp: '2026-07-14T16:22:00-07:00',
    eventType: 'TEL_ENROLLMENT_COMPLETE',
    details: 'New telephone authenticator added and active: "Work Office Landline (Fallback)"',
    status: 'success',
    ipAddress: '12.44.156.3',
    maskedNumber: '+44 •••• ••0077',
  },
  {
    id: 'log-5',
    timestamp: '2026-07-14T11:02:44-07:00',
    eventType: 'TEL_PROVIDER_FAILOVER',
    details: 'Twilio gateway reported high latency. Temporarily routing GB traffic to infobip_voice.',
    status: 'warning',
    ipAddress: 'system-scheduler',
  },
];

export function maskPhoneNumber(raw: string, countryCode: string): string {
  if (!raw) return '';
  const country = COUNTRIES.find(c => c.code === countryCode) || COUNTRIES[0];
  const digitsOnly = raw.replace(/\D/g, '');
  const prefix = country.prefix;
  const mainPart = digitsOnly.startsWith(prefix.replace('+', '')) 
    ? digitsOnly.slice(prefix.replace('+', '').length) 
    : digitsOnly;

  if (mainPart.length <= 4) {
    return `${prefix} ••••`;
  }
  
  // Keep first and last 2 digits
  const maskedLength = mainPart.length - 4;
  const maskedMiddle = '•'.repeat(maskedLength > 0 ? maskedLength : 4);
  const formattedMask = `${mainPart.slice(0, 2)}${maskedMiddle}${mainPart.slice(-2)}`;
  return `${prefix} ${formattedMask}`;
}

export function formatPhoneNumber(digits: string, countryCode: string): string {
  const country = COUNTRIES.find(c => c.code === countryCode) || COUNTRIES[0];
  const prefix = country.prefix;
  let cleanDigits = digits.replace(/\D/g, '');
  
  if (cleanDigits.startsWith(prefix.replace('+', ''))) {
    cleanDigits = cleanDigits.slice(prefix.replace('+', '').length);
  }

  // Format using country pattern
  let formatted = prefix;
  let patternIdx = 0;
  let digitIdx = 0;
  const pattern = country.pattern;

  while (patternIdx < pattern.length && digitIdx < cleanDigits.length) {
    const char = pattern[patternIdx];
    if (char === '#') {
      formatted += cleanDigits[digitIdx];
      digitIdx++;
    } else {
      formatted += char;
    }
    patternIdx++;
  }

  // Append remaining digits if any
  if (digitIdx < cleanDigits.length) {
    formatted += ' ' + cleanDigits.slice(digitIdx);
  }

  return formatted;
}
