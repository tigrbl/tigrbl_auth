# Authorization Models Focus

Research date: 2026-05-28

Scope: this note frames RBAC, ABAC, delegated/delegation-based access control, PBAC, ReBAC, scope-based authorization, tenant isolation, and contextual policy for `tigrbl_auth`.

The main distinction: these are not competing features where one replaces the others. Mature identity systems compose them. Roles provide coarse authority, attributes and context constrain decisions, permissions/scopes name allowed operations, delegation explains who granted authority, relationships answer graph-shaped access, and policy ties the decision together with auditable reasons.

## Vocabulary

| Model | Meaning in `tigrbl_auth` | Primary use |
| --- | --- | --- |
| RBAC | Role-based access control: subject has role, role grants permissions or authority. | Tenant admin, platform admin, service owner, developer, group-like access. |
| ABAC | Attribute-based access control: subject/resource/context attributes must match policy. | Region, tenant, environment, risk posture, MFA state, device trust, app type. |
| DeBAC / delegated access | Delegation-based access control: authority is allowed only because an allowed delegator granted it to a delegate. | Tenant owner delegates tenant admin; service owner delegates rotation; platform admin grants tenant authority. |
| PBAC | In this repo, closest executable shape is permission-based / policy-based access control through `PermissionPolicy`; product docs should call out which meaning is intended. | Action names such as `tenant.update`, `service.rotate`, `client.read`. |
| ReBAC | Relationship-based access control: access follows graph relationships between subject and resource. | User is member of group, group is viewer of document, service owns resource. |
| Scope-based auth | OAuth/OIDC scope and audience enforcement. | API access tokens, resource-server validation, client grants, consent. |
| Tenant isolation | Tenant boundary is a mandatory authorization dimension, not just metadata. | Every admin, token, key, client, service, and user operation. |
| Contextual / risk policy | Decision uses runtime facts such as MFA, IP, device, time, anomaly, session assurance. | Step-up, deny risky actions, high-assurance admin operations. |

## Current `tigrbl_auth` State

| Area | Current state | Evidence | Interpretation |
| --- | --- | --- | --- |
| Policy package boundary | `tigrbl-authz-policy` explicitly owns authorization decisions and prevents policy logic from leaking into OAuth, OIDC, admin, server, and principals code. | [ADR-1099](../.ssot/adr/ADR-1099-policy-is-an-explicit-package-boundary.yaml), [`tigrbl-authz-policy` README](../pkgs/30-capabilities/tigrbl-authz-policy/README.md) | This is the right architectural center for RBAC/ABAC/PBAC/delegation decisions. |
| Executable RBAC/ABAC/PBAC/delegation | Unit coverage exercises `RolePolicy`, `AttributePolicy`, `PermissionPolicy`, `DelegationPolicy`, `AdminPolicy`, `PolicyRequest`, `PolicyDecisionEngine`, and decision traces. | [`test_jose_policy_boundary.py`](../tests/unit/test_jose_policy_boundary.py) | These are implemented primitives with tests, but still need product-level admin/API surfaces and storage contracts. |
| Decision trace | Policy engine records trace IDs, matched policies, evaluated kinds, and denial reasons. | [`test_jose_policy_boundary.py`](../tests/unit/test_jose_policy_boundary.py) | Strong foundation for explainable authorization and audit. |
| ReBAC / graph authorization | Phase 4 tests include `RelationshipGraph`, relationship definitions, tuples, and graph-based access decisions. | [`test_phase4_advanced_identity_boundary.py`](../tests/unit/test_phase4_advanced_identity_boundary.py) | ReBAC exists as advanced identity behavior, not yet a canonical product/storage/API surface. |
| Policy language / versioning | Phase 4 tests publish policy versions and reject unsafe policy source. | [`test_phase4_advanced_identity_boundary.py`](../tests/unit/test_phase4_advanced_identity_boundary.py) | There is a policy-language direction, but it needs formal spec, parser/runtime boundaries, and admin lifecycle. |
| Resource-server authorization | Resource servers are distinct from clients/apps and policy owns scope, permission, tenant, proof-binding, and resource authorization decisions. | [ADR-1108](../.ssot/adr/ADR-1108-resource-servers-are-distinct-from-clients-and-apps.yaml) | Scope and permission models must be tied to resource-server objects, not free-floating strings. |
| Principal authority | Principals model roles, tenant memberships, service principals, workload principals, developers, admins, owners, and superusers. | [Principal Interaction Matrices](architecture/PRINCIPAL_INTERACTION_MATRICES.md), [`models.py`](../pkgs/10-domain/tigrbl-identity-principals/src/tigrbl_identity_principals/models.py) | Authorization needs principal facts but should not be embedded inside principal models. |

## Model Composition

| Question | Best model | Example |
| --- | --- | --- |
| Who is this actor in this tenant? | RBAC + tenant membership | `tenant-admin` in `tenant-a`. |
| What exact operation is being requested? | PBAC / permission policy | `tenant.update`, `client.rotate_secret`, `service.key.revoke`. |
| Is the operation inside the right boundary? | Tenant isolation | Subject, resource, credential, token, and policy all belong to `tenant-a`. |
| Did someone delegate this authority? | Delegation / DeBAC | Tenant owner delegated `client.manage` to a developer. |
| Does context permit the action now? | ABAC / contextual policy | MFA is true, device is trusted, region is allowed, environment is prod. |
| Does the subject relate to the resource? | ReBAC | User is member of group that is viewer of resource. |
| Can this API token call this protected API? | Scope/resource authorization | Token has audience `api://billing` and scope `invoice.read`. |
| Why was this allowed or denied? | Decision trace / audit | Trace lists evaluated policies, matched policies, denial reason, correlation ID. |

## Product Boundary

| Layer | Owns | Does not own |
| --- | --- | --- |
| `tigrbl-authz-policy` | Policy request/decision contracts, RBAC, ABAC, PBAC, delegation, tenant isolation, scope/permission decisions, decision traces. | Credential verification, token signing, route mounting, DB sessions. |
| `tigrbl-identity-principals` | Principal facts: user, admin, owner, service, workload, client, tenant membership, roles as facts. | Final authorization decisions. |
| `tigrbl-authn-credentials` | Credential facts and proof posture: password, API key, service key, client secret, MFA/passkey status. | Whether a credential grants permission to perform an action. |
| `tigrbl-auth-protocol-oauth` | OAuth scopes, resource indicators, consent inputs, token issuance hooks. | Tenant/admin authorization policy itself. |
| `tigrbl-authz-resource-server` | Downstream enforcement of audience, scope, token validity, proof binding, and policy hooks. | Issuing tokens or managing policy definitions. |
| `tigrbl-identity-storage` | Canonical policy, role, permission, grant, relationship, assignment, audit, and version tables. | Policy semantics. |
| Admin frontdoors | Product-scoped policy configuration and assignment under platform, tenant, developer, or service authority. | Low-level policy evaluation internals. |

## Authorization Object Model

| Object | Needed fields / semantics | Priority |
| --- | --- | --- |
| Role | `id`, `tenant_id`, `name`, `description`, `status`, assignable scope, managed-by surface. | P0 |
| Permission | `id`, `tenant_id`, `name`, `resource_type`, `action`, risk tier, description. | P0 |
| RolePermission | role-to-permission binding with tenant/app/resource scoping and audit. | P0 |
| PrincipalRoleAssignment | principal-to-role binding with tenant, resource/app scope, expiry, delegated-by, audit. | P0 |
| Policy | policy metadata, kind, target surface/resource, status, owner, version pointer. | P0 |
| PolicyVersion | immutable source/compiled representation, hash, created-by, effective window, status. | P0 |
| AttributeRule | required subject/resource/context attributes and comparison operators. | P1 |
| DelegationGrant | delegator, delegate, tenant/resource scope, actions, expiry, constraints, revocation. | P0 |
| RelationshipDefinition | resource type, relation name, allowed subject types, constraints. | P1 |
| RelationshipTuple | tenant, resource, relation, subject, caveats/context, effective window. | P1 |
| ResourceServerGrant | client/service/principal to resource-server audience/scope/permission grant. | P0 for M2M/resource server. |
| AuthorizationDecisionLog | request facts, decision, reason, trace, matched policy IDs, redacted context, correlation ID. | P0 |

## Capability Matrix

| Capability | Current / target in `tigrbl_auth` | Priority |
| --- | --- | --- |
| RBAC evaluation | Executable primitive exists. Needs canonical storage and admin assignment surface. | P0 |
| ABAC evaluation | Executable primitive exists for required attributes. Needs richer operators, resource attributes, and context normalization. | P1 |
| Permission/PBAC evaluation | Executable primitive exists. Needs canonical permission catalog and resource/action naming. | P0 |
| Delegation / DeBAC | Executable primitive exists. Needs delegation grant lifecycle, expiry, revocation, and UI/API management. | P0 |
| Tenant isolation policy | Architecture is clear. Needs explicit invariant tests across all frontdoors and storage-backed resources. | P0 |
| Scope/resource authorization | Strong architecture direction. Needs resource-server, scope, permission, and grant objects tied together. | P0 |
| ReBAC | Advanced test behavior exists. Needs canonical relationship definitions, tuples, storage, API, and resource-server integration. | P1 |
| Policy language | Advanced test behavior exists. Needs accepted grammar, parser, safe evaluator, versioning, linting, and audit. | P1 |
| Decision trace | Executable primitive exists. Needs persistence, redaction, correlation IDs, and admin/operator views. | P0 |
| Policy provenance | Package includes provenance helpers. Needs formal proof-chain use for policy releases and changes. | P1 |
| Break-glass / emergency access | Underframed. Needs explicit policy and audit posture. | P1 |
| Deny overrides | Underframed. Needs rule precedence and fail-closed conflict handling. | P1 |

## Recommended Evaluation Shape

The policy engine should evaluate requests as a structured decision, not as scattered helper calls:

| Stage | Behavior |
| --- | --- |
| Normalize request | Convert caller/resource/action/context into `PolicyRequest` with tenant, principal, credential, scopes, resource, action, and correlation ID. |
| Enforce tenant boundary | Fail closed if subject/resource/token/policy tenant boundaries do not align. |
| Check delegation/admin authority | If request uses delegated/admin authority, verify grant, scope, expiry, and revocation. |
| Check permission/scope | Verify requested action is covered by permission or token scope for the target resource. |
| Check role assignments | Verify roles only after tenant/resource scope is known. |
| Check attributes/context | Verify contextual requirements such as MFA, environment, region, device, risk, and assurance. |
| Check relationships | If resource access is graph-shaped, evaluate relationship tuples and caveats. |
| Produce trace | Return allow/deny, reason, matched policies, evaluated kinds, redacted context, and trace ID. |

## Minimum Viable Authorization Slice

| Slice | Deliverable | Tests |
| --- | --- | --- |
| Permission catalog | Canonical permission names for tenant, client, app, service, key, user, resource-server, and policy operations. | Static naming tests and deny unknown permission tests. |
| Role and assignment storage | Storage tables and admin routes for roles, role-permission bindings, and principal-role assignments. | Storage/facade identity tests, CRUD tests, tenant-boundary tests. |
| Delegation grants | Delegation lifecycle with expiry, revocation, allowed actions, resource scope, and audit. | Positive/negative delegation tests, expired/revoked denial. |
| Policy decision API | Internal API for all frontdoors to ask policy for allow/deny with trace. | Unit tests plus frontdoor integration checks. |
| Resource-server grants | Resource server, scopes, permissions, and client/service grants for M2M/protected APIs. | Token issuance and resource validation tests. |
| Decision logs | Persist redacted authorization decisions for audit and support. | Audit shape, redaction, correlation, and retention tests. |
| ReBAC pilot | Relationship definitions and tuples for one resource family. | Graph allow/deny and tenant isolation tests. |

## Recommended Defaults

| Decision | Recommendation | Reason |
| --- | --- | --- |
| Default deny | Deny unless a specific policy grants access. | Avoids accidental authority from partial data. |
| Tenant first | Tenant boundary checks happen before role/permission matching. | Prevents cross-tenant role reuse. |
| Roles are coarse | Roles group permissions; they should not directly encode every context condition. | Keeps RBAC understandable. |
| Permissions are named actions | Use stable action strings such as `client.secret.rotate`. | Makes audit and API docs legible. |
| Delegation expires | Delegation grants should have optional but strongly encouraged expiry. | Limits stale authority. |
| Context is normalized | MFA, device, region, environment, risk, and assurance should use canonical keys. | Prevents policy drift across frontdoors. |
| Trace every decision | Every allow/deny should have a trace ID and reason. | Required for admin support and certification evidence. |
| Policy code is constrained | Any policy language must be parsed/evaluated by a safe evaluator, not arbitrary code. | Current tests already reject unsafe source. |

## Proposed SSOT Follow-Up

| Entity type | Proposed work | Purpose |
| --- | --- | --- |
| ADR update | Add a status note to ADR-1099 clarifying composed authorization: RBAC + ABAC + PBAC + delegation + ReBAC + scopes + tenant isolation. | Prevent future work from picking only one authorization model. |
| SPEC create/update | Create an `authorization-model-composition-contract` or expand an existing policy spec. | Define normative object model, evaluation order, and trace requirements. |
| SPEC link | Link resource-server, M2M, platform-admin, tenant-admin, developer, and service-admin specs to the authorization contract. | Make every frontdoor consume the same policy engine. |
| Feature | `feat:authorization-permission-catalog` | Canonical permission naming and validation. |
| Feature | `feat:authorization-role-assignment-lifecycle` | RBAC storage and admin lifecycle. |
| Feature | `feat:authorization-delegation-grants` | Delegation/DeBAC lifecycle. |
| Feature | `feat:authorization-decision-api-and-traces` | Shared internal decision contract and audit trail. |
| Feature | `feat:authorization-resource-server-grants` | Scope/permission/resource-server grant model. |
| Feature | `feat:authorization-rebac-pilot` | Relationship definitions/tuples for graph-shaped access. |
| Test | `tst:authorization-tenant-boundary-fail-closed` | Cross-tenant deny proof. |
| Test | `tst:authorization-rbac-abac-pbac-delegation-composition` | Composed decision proof. |
| Test | `tst:authorization-decision-trace-redaction` | Trace and audit safety proof. |
| Test | `tst:authorization-resource-server-grant-enforcement` | Resource/API authorization proof. |

## Key Takeaway

`tigrbl_auth` should not choose RBAC versus ABAC versus PBAC versus delegation versus ReBAC. The right product stance is a composable authorization decision system:

```text
principal facts + credential facts + tenant boundary + roles + permissions
+ delegation + scopes + resource relationships + context
= audited policy decision
```

The repo already has the first executable policy primitives. The next maturity step is canonical storage, shared decision APIs, frontdoor integration, and productized admin UI/API lifecycle.
