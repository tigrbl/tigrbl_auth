import { randomUUID } from "node:crypto";
import type { AuthZenEvaluationRequest, Policy, Receipt, Role, RoleAssignment, Trace } from "./types";

export function generateId(prefix: string) {
  return prefix + randomUUID();
}

// Local policy simulator. A permit requires a matching active rule in the
// request's tenant. The simulator does not establish the caller's identity.
export class AuthorizationEngine {
  constructor(private state: { policies: Policy[]; roles: Role[]; assignments: RoleAssignment[] }) {}

  evaluate(request: AuthZenEvaluationRequest, policies = this.state.policies) {
    const valid = [request?.tenantId, request?.subject?.id, request?.action?.name,
      request?.resource?.type, request?.resource?.id]
      .every(value => typeof value === "string" && value.trim() !== "");
    const roles = new Set(valid ? this.state.assignments
      .filter(item => item.tenantId === request.tenantId && item.subjectId === request.subject.id)
      .map(item => item.roleId) : []);
    const matches = valid ? policies.filter(policy =>
      policy.tenantId === request.tenantId && policy.status === "active" &&
      policy.action === request.action.name && policy.resourceType === request.resource.type &&
      (!policy.roleId || (roles.has(policy.roleId) && this.state.roles.some(role =>
        role.id === policy.roleId && role.tenantId === request.tenantId)))
    ) : [];
    const decision = matches.some(policy => policy.effect === "permit") &&
      matches.every(policy => policy.effect === "permit") ? "permit" : "deny";
    const evaluatedAt = new Date().toISOString();
    const trace: Trace = {
      id: generateId("trace_"), tenantId: valid ? request.tenantId : "",
      matchedPolicies: matches.map(policy => policy.id), decision, evaluatedAt,
    };
    const receipt: Receipt = { decisionId: generateId("decision_"), traceReference: trace.id, decision };
    const safeReason = !valid ? "The evaluation request is incomplete." : decision === "permit"
      ? "A matching active policy permits this action." : "No applicable permit or a matching deny.";
    return { trace, receipt, response: {
      ...receipt, safeReason, policySetVersion: "local-demo-v1",
      obligations: [], advice: [], expirySeconds: 0, evaluatedAt,
    } };
  }
}
