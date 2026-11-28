import type { DelegationGrant, Permission, Policy, PolicyLifecycle, Receipt, RelationshipTuple, Role, RoleAssignment, TenantRecord, Trace } from "./types";

const tenantId = "demo";
const state = {
  permissions: [{ id: "document-read", tenantId, name: "Read document" }] as Permission[],
  roles: [{ id: "reader", tenantId, name: "Document reader" }] as Role[],
  assignments: [{ id: "alice-reader", tenantId, roleId: "reader", subjectId: "alice" }] as RoleAssignment[],
  policies: [{ id: "permit-document-read", tenantId, name: "Permit document readers", status: "active",
    effect: "permit", action: "read", resourceType: "document", roleId: "reader" }] as Policy[],
  delegations: [] as DelegationGrant[],
  relationshipTuples: [] as RelationshipTuple[],
  traces: [] as Trace[],
  receipts: [] as Receipt[],
  audit: [] as { operation: string; actorId: string; rationale?: string; timestamp: string }[],
};

function audit(operation: string, actorId: string, rationale?: string) {
  state.audit.unshift({ operation, actorId, rationale, timestamp: new Date().toISOString() });
}

function insert<T extends TenantRecord>(rows: T[], item: T) {
  if (!item.id || !item.tenantId || rows.some(row => row.id === item.id && row.tenantId === item.tenantId)) {
    throw new Error("A unique ID and tenant are required.");
  }
  rows.push(item);
}

function replace<T extends TenantRecord>(rows: T[], item: T) {
  const index = rows.findIndex(row => row.id === item.id && row.tenantId === item.tenantId);
  if (index === -1) throw new Error("Record not found in tenant.");
  rows[index] = item;
}

function remove<T extends TenantRecord>(rows: T[], id: string, tenant: string) {
  const index = rows.findIndex(row => row.id === id && row.tenantId === tenant);
  if (index === -1) throw new Error("Record not found in tenant.");
  rows.splice(index, 1);
}

export const dbInstance = {
  get: () => state,
  logDecisionResult(trace: Trace, receipt: Receipt) {
    state.traces.unshift(trace);
    state.receipts.unshift(receipt);
  },
  registerPermission(item: Permission, actor: string, why: string) {
    insert(state.permissions, item); audit("register permission", actor, why);
  },
  deprecatePermission(id: string, replacementId: string | undefined, actor: string, why: string) {
    const matches = state.permissions.filter(item => item.id === id);
    if (matches.length !== 1) throw new Error("Permission ID is missing or ambiguous.");
    Object.assign(matches[0], { deprecated: true, replacementId }); audit("deprecate permission", actor, why);
  },
  createRole(item: Role, actor: string, why: string) {
    insert(state.roles, item); audit("create role", actor, why);
  },
  updateRole(item: Role, actor: string, why: string) {
    replace(state.roles, item); audit("update role", actor, why);
  },
  deleteRole(id: string, tenant: string, actor: string, why: string) {
    remove(state.roles, id, tenant); audit("delete role", actor, why);
  },
  createAssignment(item: RoleAssignment, actor: string, why: string) {
    insert(state.assignments, item); audit("assign role", actor, why);
  },
  revokeAssignment(id: string, tenant: string, actor: string, why: string) {
    remove(state.assignments, id, tenant); audit("revoke assignment", actor, why);
  },
  createPolicy(item: Policy, actor: string, why: string) {
    insert(state.policies, item); audit("create policy", actor, why);
  },
  updatePolicy(item: Policy, actor: string, why: string) {
    replace(state.policies, item); audit("update policy", actor, why);
  },
  changePolicyLifecycle(id: string, status: PolicyLifecycle, tenant: string, actor: string, why: string) {
    if (!["draft", "active", "deprecated", "archived"].includes(status)) throw new Error("Invalid policy status.");
    const policy = state.policies.find(item => item.id === id && item.tenantId === tenant);
    if (!policy) throw new Error("Policy not found in tenant.");
    policy.status = status; audit("change policy status", actor, why);
  },
  createDelegation(item: DelegationGrant, actor: string, why: string) {
    insert(state.delegations, item); audit("create delegation", actor, why);
  },
  revokeDelegation(id: string, tenant: string, actor: string, why: string) {
    remove(state.delegations, id, tenant); audit("revoke delegation", actor, why);
  },
  createRelationshipTuple(item: RelationshipTuple, actor: string) {
    insert(state.relationshipTuples, item); audit("create relationship", actor);
  },
  deleteRelationshipTuple(id: string, tenant: string, actor: string) {
    remove(state.relationshipTuples, id, tenant); audit("delete relationship", actor);
  },
};
