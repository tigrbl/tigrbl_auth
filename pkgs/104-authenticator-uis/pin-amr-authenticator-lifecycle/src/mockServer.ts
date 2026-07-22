import { SimulatedServerState, AuditEvent, FirstPartyPolicy, PinState } from './types';

// Let's create a class or a helper system that can hold state and can be instantiated or managed
// Since we want standard React updates, we can either use functions that take a state and return an updated state + result,
// or a mock-server reducer/handler. A pure functional approach where we pass state and actions is extremely clean for React,
// but let's provide a set of pure helper functions to simulate the server logic.
// This enforces the boundary: client code calls these functions, and they handle everything under the hood.

export const DEFAULT_POLICY: FirstPartyPolicy = {
  minLength: 6,
  maxLength: 12,
  allowAlpha: false,
  disallowedPatterns: ['123456', '654321', '111111', '000000', '123123'],
  maxAttempts: 3,
  rateLimitMinutes: 15,
  lockoutThreshold: 3,
  historySize: 3,
};

export const INITIAL_SERVER_STATE: SimulatedServerState = {
  isFirstPartyEnrolled: false,
  firstPartyVerifierHash: null,
  firstPartyBackupRecoverySet: false,
  remainingAttempts: 3,
  status: 'active',
  policy: DEFAULT_POLICY,
  trustedExternalSources: {
    passkeyAllowed: true,
    securityKeyAllowed: true,
    smartCardAllowed: true,
    nativeDeviceAllowed: true,
    trustEvidenceProvenanceOnly: true,
  },
  deviceRetriesLeft: 3,
  deviceLocked: false,
  middlewareHealthy: true,
  providerOutage: false,
};

/**
 * Super lightweight verifier hash function simulator.
 * In production this would be argon2, scrypt, or PBKDF2.
 * We hash with a custom simulated prefix.
 */
export function hashPin(pin: string): string {
  // Simple deterministic pseudo-hash
  let hash = 0;
  for (let i = 0; i < pin.length; i++) {
    const char = pin.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return `sha256-v1-tigrbl-pbkdf2:${hash.toString(16)}`;
}

/**
 * Check if PIN has disallowed patterns
 */
export function checkDisallowedPatterns(pin: string, policy: FirstPartyPolicy): string | null {
  if (pin.length < policy.minLength) {
    return `PIN is too short. Minimum length is ${policy.minLength} characters.`;
  }
  if (pin.length > policy.maxLength) {
    return `PIN is too long. Maximum length is ${policy.maxLength} characters.`;
  }
  if (!policy.allowAlpha && !/^\d+$/.test(pin)) {
    return 'PIN must contain only numbers.';
  }
  
  // Check sequential or repetitive digits
  if (policy.disallowedPatterns.includes(pin)) {
    return 'This PIN pattern is too common or easily guessed (e.g., sequential or identical numbers).';
  }
  
  // Custom checks: simple sequential run detection
  if (/^(012345|123456|234567|345678|456789|567890)$/.test(pin.substring(0, 6))) {
    return 'Sequential ascending numbers are blocked.';
  }
  if (/^(987654|876543|765432|654321|543210)$/.test(pin.substring(0, 6))) {
    return 'Sequential descending numbers are blocked.';
  }
  if (/^(\d)\1{5,}$/.test(pin)) {
    return 'Identical repeating numbers are blocked.';
  }

  return null;
}

/**
 * Server-side audit logging helper
 */
export function createAuditLog(
  action: string,
  category: AuditEvent['category'],
  outcome: AuditEvent['outcome'],
  details: string,
  provenance?: string,
  authenticatorClass?: string
): AuditEvent {
  const dateStr = new Date().toISOString();
  const id = `audit-${Math.floor(Math.random() * 1000000)}`;
  return {
    id,
    timestamp: dateStr,
    action,
    category,
    outcome,
    details,
    provenance,
    authenticatorClass,
  };
}
