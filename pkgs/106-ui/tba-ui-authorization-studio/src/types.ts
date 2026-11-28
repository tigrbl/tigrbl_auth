export type PolicyLifecycle = "draft" | "active" | "deprecated" | "archived";
export type TenantRecord = { id: string; tenantId: string };
export type Permission = TenantRecord & { name: string; deprecated?: boolean; replacementId?: string };
export type Role = TenantRecord & { name: string };
export type RoleAssignment = TenantRecord & { roleId: string; subjectId: string };
export type DelegationGrant = TenantRecord & { from: string; to: string };
export type RelationshipTuple = TenantRecord & { subject: string; relation: string; object: string };
export type Policy = TenantRecord & {
  name: string;
  status: PolicyLifecycle;
  effect: "permit" | "deny";
  action: string;
  resourceType: string;
  roleId?: string;
};
export type AuthZenEvaluationRequest = {
  tenantId: string;
  subject: { id: string };
  action: { name: string };
  resource: { type: string; id: string };
};
export type Trace = {
  id: string;
  tenantId: string;
  matchedPolicies: string[];
  decision: "permit" | "deny";
  evaluatedAt: string;
};
export type Receipt = { decisionId: string; traceReference: string; decision: Trace["decision"] };
