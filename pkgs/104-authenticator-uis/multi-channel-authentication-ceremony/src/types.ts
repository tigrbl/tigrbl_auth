export type AuthenticatorMethod = 'sms' | 'email' | 'totp' | 'push' | 'passkey' | 'voice' | 'smartcard';

export interface Authenticator {
  id: string;
  type: AuthenticatorMethod;
  label: string;
  destination: string; // obfuscated hint
  enrolled: boolean;
  lastUsed?: string;
  independentGroup: string; // Used to evaluate if channels are truly independent
}

export type StepStatus = 'completed' | 'current' | 'waiting' | 'failed' | 'skipped';

export interface CeremonyStep {
  id: string;
  title: string;
  description: string;
  allowedMethods: AuthenticatorMethod[];
  selectedMethod: AuthenticatorMethod | null;
  status: StepStatus;
  progressText: string;
  completedAt: string | null;
  providerId: string;
}

export interface Policy {
  id: string;
  name: string;
  requiredIndependentChannels: number;
  allowedCombinations: AuthenticatorMethod[][];
  sequenceOrder: 'strict' | 'flexible';
  tokenExpirySeconds: number;
  allowFallback: boolean;
  fallbackCombination: AuthenticatorMethod[];
}

export type ProviderHealthState = 'operational' | 'degraded' | 'outage';

export interface ProviderHealth {
  id: string;
  name: string;
  type: AuthenticatorMethod;
  status: ProviderHealthState;
  latencyMs: number;
  reliability: number; // percentage
}

export interface AuditEvent {
  id: string;
  timestamp: string;
  level: 'info' | 'success' | 'warn' | 'error';
  category: 'orchestration' | 'policy' | 'provider' | 'enrollment';
  message: string;
  ceremonyId: string;
  details?: any;
}

export interface CeremonySession {
  id: string;
  subject: string;
  tenantId: string;
  ipAddress: string;
  deviceOs: string;
  location: string;
  amrEmitted: string[];
  mcaAchieved: boolean;
}
