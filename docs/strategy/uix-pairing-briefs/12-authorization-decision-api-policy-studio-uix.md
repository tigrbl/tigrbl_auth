# Authorization Decision API + Policy Studio UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-authorization` + `@tigrbl-auth/policy-studio-uix`  
**Status:** New product surface; substantial engine, contract, graph, and storage foundations exist  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-authorization`  
**Proposed UIX owner:** `pkgs/95-ui/policy-studio-uix`

## 1. Product Decision

Create a dedicated authorization product surface with two rigorously separated planes:

- **Decision plane:** a low-latency, fail-closed Policy Decision Point (PDP) API used by Policy Enforcement Points (PEPs), aligned with the OpenID AuthZEN Authorization API.
- **Management plane:** policy, role, permission, delegation, relationship, version, simulation, rollout, and audit operations used by Policy Studio.

The API must compose the repository’s existing policy contracts, decision engine, rules, evaluators, combiners, obligations, attribute mapping, authority graph, delegation lifecycle, relationship graph, and provenance builders. It must not duplicate policy decisions inside OAuth, OIDC, principal, resource-server, or UIX code.

Policy Studio is an administrative instrument, not a replacement for application authorization checks. Production services call the decision plane directly; they never depend on a browser UI.

## 2. Why This Pairing Is Needed

The repository already has:

- `PolicyRequest`, policy decisions, targets, combining contracts, and policy versions;
- concrete RBAC, ABAC, permission/policy, and delegation rules;
- default condition/rule evaluators and policy combiner;
- obligation/advice handlers;
- attribute mapping and selectors;
- a policy decision engine capability;
- authority nodes, edges, scopes, closure, reachability proof, monotonicity checks, and least-authority diffs;
- delegation grant, scope, proof, edge, token-link, lifecycle, expiry, revocation, and audit storage;
- relationship definitions/tuples and an advanced relationship graph;
- deterministic authorization and delegation provenance builders;
- durable role and policy-version tables;
- UIX policy simulation/RBAC/ABAC tests in the legacy admin boundary.

The gaps are a canonical network API, durable product-level lifecycle for all policy objects, persisted/redacted decision evidence, formal resource/action vocabulary, tenant-safe management surfaces, relationship storage/productization, and controlled deployment.

## 3. Users and Jobs

### Application and resource-server developer

1. Submit a normalized subject/resource/action/context request.
2. Receive an unambiguous permit/deny result with safe obligations and correlation.
3. Batch-evaluate multiple requests where supported.
4. Integrate without depending on the PDP’s internal policy language.
5. Troubleshoot denial safely in non-production or authorized support contexts.

### Policy administrator

1. Define roles, permissions, policies, attributes, relationships, and delegation rules.
2. Test policy changes against fixtures and historical-safe scenarios.
3. Understand before/after access impact and least-authority differences.
4. Submit for review, publish, stage, activate, roll back, and retire versions.
5. Audit who changed authority and why.

### Security reviewer

1. Inspect default-deny behavior, tenant isolation, combining semantics, delegation attenuation, relationship reachability, and obligations.
2. Find excess, missing, stale, orphaned, or conflicting authority.
3. Review redacted decision traces and policy coverage.
4. Validate policy/runtime compatibility and rollout evidence.

### Resource or business owner

1. Understand who can perform which action on owned resources and why.
2. Approve or reject delegated access and time-bound grants.
3. Review expiring/stale authority and access-impact summaries.

## 4. Architectural Boundary

### Decision plane owns

- request normalization;
- tenant/resource boundary resolution;
- subject, resource, action, and context evaluation;
- credential/authentication context as input facts;
- role/permission/attribute/delegation/relationship evaluation;
- combining and default-deny semantics;
- obligations/advice generation;
- deterministic decision trace/provenance;
- correlation, policy version, and decision receipt metadata.

### Management plane owns

- permission/action/resource catalogs;
- role and assignment lifecycle;
- policy definitions and versions;
- attribute source mappings;
- delegation grants and revocation;
- relationship definitions and tuples;
- test fixtures, simulations, approvals, releases, rollouts, and rollback;
- redacted decision/audit query.

### Other packages retain ownership

- credentials/authenticators determine verified identity and authentication context;
- principals own principal facts, not permission decisions;
- OAuth/OIDC own protocol issuance and claims projection, not policy semantics;
- resource servers enforce returned decisions and obligations;
- storage owns durable records, not policy meaning;
- product admin APIs own domain-specific mutation authority and may delegate evaluation to this API.

## 5. Proposed API Contract

### AuthZEN-aligned decision routes

- `POST /access/v1/evaluation`
- `POST /access/v1/evaluations` for bounded batch/boxcar evaluation
- subject/resource/action search routes only after their authorization and enumeration risks are defined

Minimum request:

- tenant/trust-domain context;
- subject type and stable reference;
- resource type and stable reference;
- action name;
- normalized context attributes;
- credential/session assurance references where relevant;
- correlation and purpose metadata.

Minimum response:

- decision: permit or deny;
- policy set/version;
- safe reason category;
- obligations/advice;
- decision/correlation ID;
- expiry/cache constraints;
- optional authorized trace reference;
- evaluation timestamp.

Indeterminate/internal errors must resolve to deny at the enforcement contract unless a narrowly specified domain policy says otherwise.

### Management routes

- `/admin/authorization/catalogs/*`
- `/admin/authorization/roles/*`
- `/admin/authorization/assignments/*`
- `/admin/authorization/policies/*`
- `/admin/authorization/policy-versions/*`
- `/admin/authorization/delegations/*`
- `/admin/authorization/relationships/definitions/*`
- `/admin/authorization/relationships/tuples/*`
- `/admin/authorization/attributes/sources/*`
- `/admin/authorization/simulations/*`
- `/admin/authorization/releases/*`
- `/admin/authorization/decisions/*`
- `/admin/authorization/audit/*`

Exact routes must be generated from live Tigrbl operations. This brief defines product ownership, not hand-written framework routes.

### Prohibited behavior

- no token issuance, credential verification, or user authentication;
- no generic arbitrary-code policy execution;
- no cross-tenant subject/resource search;
- no policy mutation through the decision endpoint;
- no raw confidential context, personal data, secrets, tokens, or full resource bodies in traces;
- no browser-side “authoritative” simulation disconnected from the runtime engine;
- no permit result produced from missing policy data, unknown combining semantics, or partial graph state.

## 6. Canonical Domain Model

### Permission catalog

Every permission/action needs:

- canonical ID/name;
- resource type;
- action verb;
- owning product/domain;
- risk/sensitivity class;
- required context schema;
- deprecation/replacement;
- version and provenance.

Avoid wildcard permissions as user-facing defaults. When wildcards exist, expand their effective impact during review.

### Role and assignment

- Role groups permissions; it does not encode every contextual condition.
- Assignment binds subject/group/service to role within tenant/resource scope and effective time.
- Show direct, inherited, delegated, relationship-derived, and platform/system authority separately.

### Policy and version

- immutable versioned source/structured representation;
- lifecycle: draft, review, approved, staged, active, superseded, retired, rejected;
- target resources/actions/tenants;
- combining semantics and priority;
- effective window;
- author/reviewer and rationale;
- compatibility/schema version;
- tests, simulation results, and release evidence.

### Delegation grant

- delegator and delegate;
- tenant/resource/action scopes;
- constraints and purpose;
- valid-from/expiry;
- proof and approval;
- parent/derived grant chain;
- token link where applicable;
- active/revoked/expired/collapsed lifecycle;
- monotonic attenuation proof and audit.

A delegate cannot grant authority they do not possess, and derived delegation cannot broaden scope or time.

### Relationship model

- typed relationship definition;
- allowed subject/resource types;
- tuple with tenant, subject, relation, resource, caveats, and effective window;
- provenance, writer authority, and version;
- cycle/depth/fanout constraints;
- deletion and referential integrity.

### Decision trace

Trace contains safe evaluation facts:

- decision/correlation ID;
- normalized type-level subject/resource/action references;
- tenant and policy version;
- evaluated policy kinds;
- matched/failed rules and safe reason codes;
- delegation/relationship provenance references;
- obligations/advice;
- duration/cache status.

Raw secrets, tokens, personal attributes, resource content, and sensitive relationship values must be redacted or referenced by opaque IDs.

### Decision receipt

Optionally issue a signed, non-bearer receipt containing:

- decision ID;
- policy version/hash;
- hashed/opaque subject and resource references;
- action;
- decision and obligations digest;
- issued/expiry time;
- correlation ID.

It proves what the PDP decided under a specific policy snapshot. It does not grant access, replace enforcement, or reveal the underlying policy/context.

## 7. Evaluation Semantics

Required order:

1. Validate request shape, supported types, and tenant context.
2. Resolve canonical subject, resource, action, and context schemas.
3. Enforce tenant/resource isolation invariants.
4. Resolve credential/session assurance facts as inputs.
5. Check direct permissions and role assignments.
6. Check delegation authority, attenuation, expiry, and revocation.
7. Check attributes and contextual conditions.
8. Check relationship graph and caveats where applicable.
9. Apply explicit deny/default-deny and combining semantics.
10. Derive obligations/advice.
11. Produce redacted trace, provenance, decision, and cache constraints.

The implementation must formally specify deny precedence. Current authority tests note that deny precedence is not active until deny semantics exist; the product must not imply otherwise.

## 8. Required Policy Studio Experience

### Overview

- Active policy release/version, recent changes, evaluation health, denied/error rates, expiring delegations, unused roles, coverage, and required reviews.
- Avoid a generic “authorization health score.”

### Catalogs

- Browse resource types, actions, permissions, attributes, context schemas, obligations, and owners.
- Show usage, versions, deprecations, and broken references.
- Require governed registration rather than free-form strings in production policy.

### Role and assignment administration

- Create/version roles and assign them within explicit tenant/resource/time scope.
- Preview effective permissions, inheritance, excess authority, and self-impact.
- Protect platform/system roles and privilege escalation.

### Policy editor

- Prefer structured builders over unrestricted code for baseline policy types.
- Support RBAC, ABAC, permission/policy, delegation, and relationship blocks with exact semantics.
- Validate continuously against schemas and supported operators.
- Provide raw/spec view for experts without allowing unsupported constructs.

### Delegation center

- Create, review, approve, revoke, expire, and inspect delegation chains.
- Show delegator authority, requested/effective scopes, attenuation proof, parent/child grants, and affected tokens/resources.
- Warn on circular, stale, overbroad, non-expiring, or orphaned grants.

### Relationship explorer

- Visualize a bounded subgraph around one subject/resource, with list/table fallback.
- Create definitions/tuples only through authorized typed forms.
- Show reachability path, caveats, cycles, depth, and provenance.
- Never load or expose an entire sensitive graph by default.

### Simulation lab

- Run the production decision engine in side-effect-free simulation mode against draft or active versions.
- Support deterministic fixtures, safe historical replays, mutation tests, batch matrices, and expected outcomes.
- Compare current versus proposed: new permits, new denies, unchanged, errors, obligations changed, least-authority excess/missing.
- Never send notifications, mutate grants, consume one-time values, or execute external obligations.

### Change review and release

- Show semantic diff, impacted resources/actions/tenants, simulation evidence, approvers, rollout plan, rollback, and expiry.
- Support staged/shadow/canary rollout where runtime architecture permits.
- Require dual control for platform-wide or high-risk authorization changes.

### Decision explorer

- Search by correlation/decision ID and approved metadata, not arbitrary personal attributes.
- Show redacted trace, policy version, safe reason, obligations, provenance, and timing.
- Apply strict retention, access, export, and purpose controls.

## 9. Security and Reliability Requirements

- Default deny on missing, stale, invalid, incompatible, or unavailable policy state.
- Server-side tenant, resource, and management authority for every operation.
- Policy management plane must not share credentials/permissions with the runtime decision plane by default.
- Sign/version/cache policy bundles; reject partial or rollback-incompatible state.
- Bound evaluation time, graph depth/fanout, batch size, attribute resolution, and response size.
- Prevent injection through policy source, selectors, attribute names, expressions, and obligation parameters.
- Attribute resolvers need allowlists, timeouts, caching, provenance, and fail-closed semantics.
- Simulation is side-effect free and clearly labeled.
- Decision caches must bind policy version, tenant, subject/resource/action/context digest, and expiry.
- Logs/traces exclude secrets, tokens, raw PII, full resource bodies, and sensitive graph data.
- High-risk policy changes require recent strong authentication, review, reason, audit, and rollback readiness.

## 10. Team Requirements

### Technical marketing

- Provide stable screenshots for decision trace, policy simulation, least-authority diff, delegation chain, and staged rollout.
- Demonstrate explainable allow/deny without exposing customer policy or data.
- Use AuthZEN compatibility only after interoperability tests prove the exact supported surface.
- Avoid “fine-grained,” “real-time,” “zero trust,” or universal ReBAC claims without scoped evidence.

### Developer relations

- Provide tested PDP integration examples for Python, Tigrbl resource servers, gateways, and a generic HTTP PEP.
- Document request normalization, default deny, obligations, caching, correlation, failure modes, and migration from in-app checks.
- Supply policy-as-data fixtures, simulation examples, and negative tests.
- Explain what belongs in credentials, principals, policy, resource servers, and application enforcement.

### Sales and account management

- Provide scenarios for role-based access, context denial, delegated access, relationship access, policy change simulation, and rollback.
- Include “what this proves / what it does not prove” for scale, language support, external PDP compatibility, and audit.
- Make tenant, policy version, fixture status, profile, and release maturity visible.
- Avoid promising a complete IGA/PAM product from a PDP surface alone.

### GTM strategy

- Position the pairing around composable and explainable authorization decisions.
- Track privacy-safe policy workflow stages, simulation categories, decision result categories, docs/evidence engagement, and handoff.
- Never emit subject/resource/tenant IDs, attributes, policy source, graph tuples, obligations, or raw traces.
- Use one taxonomy for permission, role, assignment, policy, delegation, relationship, decision, obligation, and provenance.

### Copywriter

- Distinguish authentication from authorization and role from permission/policy.
- Explain direct, inherited, delegated, relationship-derived, and contextual authority.
- Write safe decision reasons that help without disclosing policy bypass information.
- Avoid “access granted” in Policy Studio simulation; use “simulation would permit under policy version X.”

## 11. Frontend Engineering Instructions

1. Implement the AuthZEN-compatible decision contract over the existing canonical policy engine rather than a parallel evaluator.
2. Separate decision and management deployments, credentials, route groups, rate limits, and telemetry.
3. Generate typed clients/schemas and keep resource/action/context catalogs authoritative.
4. Build policy/version/delegation/relationship workflows as explicit lifecycle state machines.
5. Execute simulation server-side through the production engine with obligations disabled or sandboxed.
6. Compute semantic/least-authority diffs and impact summaries from canonical graph/policy data.
7. Redact trace data through typed policies before it reaches UIX or logs.
8. Add property-based and negative tests for tenant isolation, monotonic delegation, default deny, combining, cycles, stale versions, injection, cache keys, and unavailable attribute sources.
9. Add load/latency budgets and failover tests for the decision plane separately from UIX tests.
10. Integrate product APIs/resource servers as PEPs without moving their domain mutation ownership into Policy Studio.

## 12. UIX Designer Instructions

- Use a dense technical console with persistent tenant, environment, active policy release, and draft context.
- Design policy workflows around catalogs, structured rules, simulation, review, rollout, and rollback.
- Visualize only bounded delegation/relationship subgraphs and always provide accessible list/table alternatives.
- Distinguish active, draft, staged, shadow, superseded, retired, invalid, stale, and incompatible without color alone.
- Make current versus proposed decision differences immediately legible.
- Provide empty catalog, first policy, large matrix, partial attribute source, cycle, conflict, denied simulation, rollout failure, rollback, and stale trace states.
- Validate keyboard editing, focus, announcements, high zoom, reduced motion, dense tables, graphs, and WCAG 2.2 AA.

## 13. Copy Deliverables

Produce:

- catalog, role, assignment, policy, delegation, relationship, and obligation terminology;
- structured editor labels/help/validation;
- simulation, current-versus-proposed, least-authority, and decision-reason copy;
- review, approval, stage, activate, shadow, rollback, retire, and expiry language;
- trace redaction/retention, unauthorized, stale, conflict, unavailable-source, default-deny, and support copy;
- developer integration and failure-mode explanations.

## 14. Delivery Phases

### Phase 0: Contracts and semantics

- Finalize canonical resource/action/permission/context catalogs.
- Define explicit deny and combining semantics.
- Complete policy/relationship storage and trace redaction contracts.
- Threat-model PDP, PAP, graph, delegation, attributes, simulation, and caches.

### Phase 1: Decision plane

- AuthZEN evaluation endpoint.
- Default-deny, correlation, obligations, policy versions, caching rules, and latency proof.
- Tigrbl resource-server/PEP integration.

### Phase 2: Policy Studio baseline

- Catalogs, roles, permissions, assignments, policy versions, structured RBAC/ABAC/permission editing.
- Deterministic simulation, diff, review, activate, and rollback.

### Phase 3: Delegation and relationships

- Delegation lifecycle/attenuation UI.
- Relationship definitions/tuples and bounded graph explorer.
- ReBAC evaluation and provenance.

### Phase 4: Operations and interoperability

- Decision explorer, redacted persistence, staged/shadow rollout, coverage, external AuthZEN interoperability, and signed decision receipts.

## 15. Acceptance Criteria

- One canonical decision engine produces API, simulation, trace, and enforcement outcomes.
- Decision and management planes have separate credentials, authority, routes, and reliability budgets.
- Default deny applies to missing/invalid/stale/incompatible state and runtime errors.
- Tenant isolation precedes all other evaluation and is proven across search, graph, cache, trace, and batch behavior.
- Roles, attributes, permissions, delegation, relationships, scopes, and context compose under documented combining/deny semantics.
- Delegation is monotonic, time/scope bounded, revocable, and provenance-preserving.
- Simulation is side-effect free and compares current/proposed outcomes accurately.
- Policy lifecycle requires versioning, review, impact evidence, rollout, rollback, and audit.
- Traces and receipts are redacted, non-bearer, retention-controlled, and correlation-safe.
- AuthZEN contract, security, graph, isolation, latency, accessibility, responsive visual, and end-to-end tests pass.

## 16. Source Evidence

- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/policy/`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/authority/`
- `pkgs/05-bases/tigrbl-authz-policy-bases/`
- `pkgs/10-concrete/tigrbl-authz-policy-rules-concrete/`
- `pkgs/10-concrete/tigrbl-authz-policy-evaluators-default/`
- `pkgs/10-concrete/tigrbl-authz-policy-combiner-default/`
- `pkgs/10-concrete/tigrbl-authz-policy-obligations-concrete/`
- `pkgs/10-concrete/tigrbl-authz-policy-attributes-mapping/`
- `pkgs/20-providers/tigrbl-security-authorization-provenance-builder/`
- `pkgs/40-capabilities/tigrbl-authz-policy/`
- `pkgs/40-capabilities/tigrbl-authz-policy-decision-engine/`
- `pkgs/40-capabilities/tigrbl-authz-policy-authority-derivation-graph/`
- `pkgs/40-capabilities/tigrbl-identity-admin-relationship-graph/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/`
- `docs/authorization-models-focus.md`
- Policy, delegation, authority, graph, simulation, provenance, UIX, isolation, and monotonicity tests/SSOT records
- OpenID AuthZEN Authorization API 1.0 specification
