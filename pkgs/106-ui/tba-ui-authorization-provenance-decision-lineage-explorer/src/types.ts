export const EvaluationOutcome = { PERMIT: "permit", DENY: "deny" } as const;
export type EvaluationOutcome = typeof EvaluationOutcome[keyof typeof EvaluationOutcome];
export const ReplayMode = {
  EXACT_HISTORICAL: "exact_historical", CURRENT_ENGINE: "current_engine",
  CURRENT_STATE: "current_state", COUNTERFACTUAL: "counterfactual",
} as const;
export type ReplayMode = typeof ReplayMode[keyof typeof ReplayMode];
export const AuthorityType = { DIRECT_ASSIGNMENT: "direct_assignment", DELEGATION_GRANT: "delegation_grant" } as const;
type AuthorityType = typeof AuthorityType[keyof typeof AuthorityType];
export type Step = { ruleName: string; outcome: EvaluationOutcome; reason: string };
type Fact = {
  id: string; type: string; schemaVersion: string; associatedWith: string; key: string;
  rawValue: string; isRedacted: boolean; sourceSystem: string; resolver: string;
  version: string; observedAt: string; effectiveAt: string; confidence: number;
  cacheStatus: string; digest: string;
};
export type DecisionTrace = {
  id: string; decisionKey: string; tenantId: string; environment: string; region: string;
  correlationId: string; requestId: string; sessionId: string; transactionId?: string;
  timestamp: string; durationMs: number; expiryDeadline: string;
  subject: { id: string; type: string; roles: string[] };
  resource: { id: string; type: string; attributes: Record<string, string> };
  action: string; context: Record<string, string>; effect: EvaluationOutcome; safeReason: string;
  obligations: { name: string; status: string; receiptId: string }[];
  policyLineage: { bundleId: string; bundleVersion: string; bundleHash: string; engineVersion: string;
    applicableRules: string[]; combiningAlgorithm: string; hasConflicts: boolean };
  facts: Fact[]; steps: Step[];
  authorityPaths: { id: string; type: AuthorityType; source: string; target: string; via?: string;
    isVerified: boolean; freshnessSeconds: number; confidence: number }[];
  outcomeLink?: { pepId: string; pepVersion: string; enforcementStatus: string;
    enforcedAt: string; receiptSignature: string; tokenId?: string };
  integritySeal: string; isLegalHold: boolean; retentionExpiresAt: string; supersededByDecisionId?: string;
};
export type ReplayJob = {
  id: string; mode: ReplayMode; targetDecisionId: string; timestamp: string; runBy: string;
  status: "completed"; substitutions: Record<string, string>; policyBundleVersionUsed: string;
  expectedCostSecs: number; purpose: string;
  result: { isReproducible: boolean; originalOutcome: EvaluationOutcome; replayedOutcome: EvaluationOutcome;
    durationMs: number; differences: string[]; missingEvidence: string[] };
};
export type ComparisonReport = {
  sourceDecisionId: string; targetDecisionId: string; effectChanged: boolean;
  sourceEffect: EvaluationOutcome; targetEffect: EvaluationOutcome; changedAuthorityPaths: string[];
  changedRules: string[]; changedFacts: string[]; addedObligations: string[];
  removedObligations: string[]; warnings: string[];
};
