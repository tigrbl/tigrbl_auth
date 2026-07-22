export type DecisionEffect = 'permit' | 'deny' | 'indeterminate' | 'challenge';

export interface TraceFact {
  id: string;
  type: string;
  source: string;
  version: string;
  freshness: 'fresh' | 'stale' | 'missing' | 'unverified';
  observedAt: string;
  value: any;
}

export interface TraceStep {
  id: string;
  ruleId: string;
  evaluator: string;
  outcome: 'matched' | 'not_matched' | 'failed' | 'skipped' | 'short_circuited';
  durationMs: number;
}

export interface Obligation {
  id: string;
  type: string;
  status: 'fulfilled' | 'pending' | 'failed' | 'unmatched';
  description: string;
}

export interface EnforcementReceipt {
  id: string;
  pepId: string;
  status: 'enforced' | 'failed' | 'mismatch' | 'unknown';
  timestamp: string;
}

export interface DecisionRecord {
  id: string;
  decisionKey: string;
  timestamp: string;
  tenant: string;
  subject: {
    id: string;
    type: string;
    name: string;
    delegatedFrom?: string;
  };
  resource: {
    id: string;
    type: string;
    name: string;
  };
  action: string;
  effect: DecisionEffect;
  policyVersion: string;
  engineVersion: string;
  facts: TraceFact[];
  steps: TraceStep[];
  obligations: Obligation[];
  enforcement: EnforcementReceipt | null;
  replayable: boolean;
  reason: string;
  integritySeal: 'valid' | 'invalid' | 'missing';
}
