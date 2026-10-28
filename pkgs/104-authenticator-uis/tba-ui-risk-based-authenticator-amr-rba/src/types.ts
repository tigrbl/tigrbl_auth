export type RiskDecision = 'continue' | 'step-up' | 'review' | 'deny' | 'recover';

export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export type SignalStatus = 'safe' | 'suspicious' | 'compromised' | 'unavailable';

export interface RiskSignal {
  id: string;
  name: string;
  category: 'network' | 'device' | 'behavior' | 'location' | 'reputation';
  status: SignalStatus;
  value: string;
  source: string;
  freshness: string; // e.g., "12s ago"
  confidence: number; // 0-100
  privacyClass: 'restricted' | 'redacted' | 'internal';
}

export interface AuthMethod {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: 'knowledge' | 'possession' | 'inherence';
  enabled: boolean;
  ceremonySteps: string[];
}

export interface PolicyRule {
  id: string;
  name: string;
  riskLevel: RiskLevel;
  conditions: {
    field: string;
    operator: 'equals' | 'not_equals' | 'contains' | 'greater_than' | 'less_than' | 'one_of';
    value: string;
  }[];
  outcome: RiskDecision;
  eligibleMethods: string[]; // AuthMethod IDs allowed
  fallbackMethod: string; // AuthMethod ID
  freshnessThreshold: number; // in seconds
  missingSignalBehavior: 'fail-closed' | 'fail-open' | 'step-up';
  enabled: boolean;
}

export interface SimulationScenario {
  id: string;
  name: string;
  description: string;
  icon: string;
  signals: Partial<Record<string, { status: SignalStatus; value: string; confidence: number }>>;
  forcedDecision?: RiskDecision;
}

export interface ProviderHealth {
  id: string;
  name: string;
  type: 'first-party' | 'third-party';
  status: 'active' | 'degraded' | 'suspended' | 'outage';
  latency: number; // ms
  errorRate: number; // %
  freshness: string; // e.g. "99.9%"
  lastChecked: string;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  trackingId: string;
  subject: string;
  action: string;
  policyVersion: string;
  signalClasses: string[];
  decision: RiskDecision;
  achievedMethods: string[];
  redactedEvidence: string;
  freshnessMet: boolean;
  tenantId: string;
}

export interface ActiveSession {
  id: string;
  device: string;
  location: string;
  ipAddress: string;
  startTime: string;
  lastActive: string;
  riskLevel: RiskLevel;
  signalsVerified: string[];
  amr: string[];
}
