# Delegation Provenance API + Authority Chain Explorer UIX Requirements Brief

**Pairing:** `tigrbl-auth-api-delegation-provenance` + `@tigrbl-auth/authority-chain-explorer-uix`  
**Additional opportunity:** Authorization/delegation/sovereignty extension 2  
**Primary buyers:** security engineering, IAM platform teams, application owners, workload and agent platform teams, auditors, and incident response  
**Status:** proposed product surface; durable delegation grants, scopes, proofs, edges, token links, authority graphs, attenuation, and runtime lineage already exist

## 1. Product Decision

Build a dedicated delegation provenance plane that records, validates, explains, and governs every chain in which one principal acts with authority originating from another principal or authority source.

The product must answer:

1. Who originally possessed or granted the authority?
2. Who is acting now, on whose behalf, and under which semantic mode?
3. What exact authority was transferred at each hop?
4. Which constraints, approvals, policies, and proofs narrowed that authority?
5. Which credentials, tokens, sessions, requests, and actions consumed the chain?
6. Is every link active, authorized, unexpired, non-cyclic, and provably no broader than its parent?
7. What descendants and active artifacts are affected by replacement, expiry, or revocation?
8. Can an auditor reconstruct the chain independently of token contents?

The API owns canonical cross-domain delegation lineage and lifecycle evidence. The UIX provides authority-chain exploration, safe grant review, descendant impact, incident response, token/action linkage, and historical reconstruction.

## 2. Product Scope

The product covers delegation involving:

- human-to-human delegated administration;
- human-to-application or service consent/authority;
- service-to-service and workload chains;
- OAuth token exchange;
- applications acting on behalf of users;
- platform, tenant, developer, and service administration;
- resource-owner or business-owner delegation;
- agent sponsorship and sub-agent delegation;
- device/fleet and operational delegation;
- entitlement, approval, and remediation workflows;
- trust-framework or organizational authority delegation;
- emergency and break-glass delegation under explicit profiles.

It must not equate all these cases. Each uses a declared delegation profile with its own subjects, authority sources, constraints, evidence, and revocation semantics.

## 3. Current Repository Reality

The repository already includes an advanced delegation foundation:

- accepted requirements for durable subject, actor, client, resource, trust-domain, token, attenuation, and proof-binding lineage;
- `DelegationGrant` with tenant, realm, delegator, delegate, delegate type, state, parent, source authority, policy version, provenance, constraints, effective/expiry/revocation, and replacement fields;
- normalized `DelegationGrantScope` records for resource type/ID, action, scope, audience, resource indicator, tenant, realm, and constraints;
- `DelegationGrantProof` with parent/delegated scope hashes, attenuation result, uncovered scopes, proof version/hash, and evaluation time;
- durable `DelegationGrantEdge` parent-child graph records;
- `DelegationGrantTokenLink` with safe token hashes, authorization trace, delegation lineage, actor/subject, exchange mode, and source/actor token hashes;
- lifecycle operations for create, activate, inspect, replace, revoke, expire, and list;
- child deactivation and chain-collapse behavior;
- authority closure, reachability, provenance, monotonicity, and least-authority diffs;
- RFC 8693 token exchange integration and token/introspection persistence;
- deterministic authorization and delegation provenance builders;
- security, unit, integration, and robustness tests for bounded chains, attenuation, stale/revoked/expired grants, policy conflicts, token persistence, and cross-tenant denial.

The missing product layer includes:

- one canonical API and UIX across administrative, OAuth, workload, agent, entitlement, and trust-framework delegation;
- first-class profile and semantic-mode definitions;
- durable human approval/acceptance and authority-source evidence;
- complete chain snapshots and point-in-time reconstruction;
- descendant invalidation/revocation convergence tracking;
- action and enforcement receipts beyond token issuance;
- privacy-aware graph search and external evidence export;
- operational scale, notification, reconciliation, and incident workflows;
- productized impersonation restrictions and disclosures.

## 4. Relationship to Existing Pairings

### Authorization Provenance

Authorization Provenance explains one decision and references the delegation lineage used by it. Delegation Provenance owns the multi-hop authority chain and its lifecycle across many decisions and artifacts.

### Authorization Decision and Policy Studio

Policy Studio defines who may delegate, which profiles/constraints apply, and how grants are evaluated. It does not own the canonical grant/provenance store or chain operations.

### Authority Attenuation

The Attenuation API proves safe narrowing and composes constraints. Delegation Provenance stores and links those proofs to grants, descendants, decisions, and actions.

### Agent Trust

Agent Trust uses delegation for sponsors, tasks, tools, budgets, and sub-agents. This API supplies the general authority chain rather than duplicating agent-only lineage.

### Token Service

Token Service consumes active grants and projects actor/subject semantics into tokens. OAuth/OIDC tokens are protocol artifacts, not the canonical delegation record.

## 5. Delegation Semantics

Every chain edge declares one semantic mode:

- **delegation:** actor remains identifiable as itself while acting on behalf of a responsible subject/authority;
- **impersonation:** actor is authorized to act as the subject within a bounded context, potentially without actor visibility to the relying party;
- **representation:** actor signs or performs a defined act for an organization/person under a legal/business role;
- **administrative delegation:** delegator transfers bounded management authority;
- **technical delegation:** workload/service receives bounded authority to call another resource;
- **approval delegation:** approver delegates a decision task, not the underlying resource authority;
- **custodial execution:** service executes an authorized operation without receiving discretionary authority;
- **emergency delegation:** exceptional, strongly governed, time-bound authority.

Delegation and impersonation must never be inferred from a missing actor. RFC 8693 distinguishes them: delegation preserves actor and subject, whereas impersonation makes the actor effectively the subject within the authorized context.

Impersonation defaults to prohibited and requires an explicit profile, rationale, approval, narrow scope/time, elevated audit, relying-party disclosure policy, and post-use review.

## 6. Canonical Principal Roles

Represent separately:

- source authority or authority issuer;
- original responsible subject/resource owner;
- delegator at the current edge;
- delegate/actor;
- requested or represented subject;
- client/application initiating protocol exchange;
- sponsor or business owner;
- approver and accepting delegate;
- resource server/PEP;
- token/credential issuer;
- policy and proof evaluator;
- revoker and incident responder.

A principal may occupy multiple roles, but the record must retain each role explicitly to expose conflicts of interest and self-delegation.

## 7. Canonical Delegation Grant

Each grant requires:

- stable grant ID, tenant, realm/trust domain, and profile;
- semantic mode;
- delegator and delegate references/types;
- responsible/original subject where distinct;
- source authority reference and point-in-time proof;
- normalized action/resource/tenant/realm/audience/scope constraints;
- typed constraints and purpose;
- policy and schema versions;
- parent grant and root lineage ID;
- created, effective, expiry, accepted, revoked, and replaced times;
- creator, approver, delegate acceptance, and rationale;
- attenuation proof and proof version;
- sender/proof-of-possession requirements;
- maximum child depth/fan-out and redelegation permission;
- lifecycle, incident, notification, and evidence references;
- region/residency and retention classification.

Source authority must be independently resolvable; a grant cannot establish its own source authority merely by asserting it.

## 8. Scope and Constraint Model

Delegated authority may be constrained by:

- tenant, realm, trust domain, organization, and environment;
- resource type and immutable resource identifier;
- action/permission and OAuth scope;
- resource indicator and audience;
- purpose/task/transaction;
- subject or beneficiary;
- time, one-time use, frequency, and concurrency;
- transaction count/value/budget;
- data classification, disclosure, retention, and region;
- network, device, workload, attestation, and authentication assurance;
- sender constraint/key/certificate;
- allowed downstream delegate types;
- chain depth, fan-out, and child lifetime;
- approval or human-interaction requirement;
- obligations and post-action receipts.

Constraints must be typed and versioned. Free-form JSON may preserve adapter fields but cannot be treated as safely attenuated until an ordering/evaluator exists.

## 9. Grant Lifecycle

Use an explicit lifecycle:

`draft -> pending_review -> pending_acceptance -> approved -> active`

Alternative and terminal states:

`rejected`, `withdrawn`, `suspended`, `expired`, `revoked`, `replaced`, `collapsed`, `invalid`, and `orphaned`.

Requirements:

- create only after current source authority resolves;
- prove attenuation before approval/activation;
- require acceptance where the delegate assumes duties, liability, or data handling;
- activate at a deterministic effective time;
- renew or replace as a new governed decision;
- expire automatically and invalidate descendant use;
- suspend temporarily without erasing history;
- revoke with reason, actor, time, scope, and propagation policy;
- prohibit mutation of active grant scope; replacement creates a successor;
- preserve historical chains after terminal states.

## 10. Chain Model

A chain is an ordered, acyclic, bounded path from root authority through one or more grants to an actor’s effective authority.

For every edge, preserve:

- parent/source grant or root authority;
- delegator and delegate;
- semantic mode;
- granted and effective scopes;
- typed constraint delta;
- attenuation proof;
- effective/expiry/status;
- policy/approval/acceptance;
- credential/token/action links;
- provenance and integrity identifiers.

The engine must detect:

- cycles and repeated principals/grants;
- disconnected or missing parents;
- tenant/realm/trust-domain changes;
- scope broadening;
- lifetime extension beyond parent;
- incompatible purpose/audience/resource;
- excessive depth/fan-out;
- stale source authority or proof;
- revoked, expired, replaced, suspended, or invalid edges;
- policy-version incompatibility;
- duplicate or conflicting paths.

## 11. Effective Authority and Multiple Sources

A delegate may receive similar authority through multiple independent paths. The product must:

- compute effective authority per source/path;
- show union only when policy explicitly permits combination;
- never combine partial constraints from different grants to manufacture authority no single permitted path provides;
- preserve source provenance for each effective scope;
- identify redundant and excess authority;
- explain whether revoking one path removes actual access;
- recalculate after source, relationship, policy, or grant change.

Least-authority diffs should compare required authority with direct, inherited, delegated, and relationship-derived authority.

## 12. Attenuation Proof Linkage

For each parent-child edge, store:

- canonical parent effective-scope hash;
- proposed child scope/constraint hash;
- typed comparison rules and evaluator version;
- proof result and uncovered/broadened dimensions;
- source policy and fact versions;
- evaluation time and expiry/freshness;
- proof hash and integrity seal;
- re-evaluation trigger.

Proof must cover action, resource, tenant, realm, audience, lifetime, purpose, budgets, data/region, redelegation, and sender constraints supported by the selected profile.

If partial-order comparison is unknown, activation fails or requires a new root authorization. “Cannot prove broader” is not evidence of attenuation.

## 13. Token and Credential Lineage

Link grants to:

- subject and actor input token hashes;
- output access/refresh token hashes;
- token family, exchange mode, audience, resource, scope, and proof binding;
- authorization trace and delegation lineage IDs;
- introspection/revocation state;
- certificate, credential lease, session, or capability artifact;
- issuer and issuance time;
- expiration/replacement/revocation.

Raw tokens, secrets, cookies, or private keys are prohibited.

RFC 8693 exchange is a protocol event and does not inherently create ongoing linkage or revocation propagation. Tigrbl’s canonical grant model must explicitly preserve and converge those relationships.

## 14. Action and Outcome Lineage

Link the chain to authorized actions:

- decision ID and PEP;
- actor and represented subject;
- resource/action/purpose/transaction digest;
- token/session/credential used;
- grant path selected;
- obligations and enforcement receipt;
- operation outcome and safe result reference;
- occurred time, region, and incident.

Distinguish authority to attempt an operation, authorization decision, enforcement, and successful business outcome.

High-risk profiles may require one-use transaction binding so a broad bearer token cannot substitute for an exact approved action.

## 15. Revocation and Chain Collapse

Revocation is a convergence workflow, not a database flag.

Required stages:

`requested -> source_grant_revoked -> descendants_identified -> artifacts_invalidated -> caches/verifiers_notified -> enforcement_confirmed -> reconciled`

Alternative states include `partial`, `failed`, `unreachable`, `exception`, and `unverified`.

The product must:

- compute descendants and affected authority before execution;
- support root, subtree, edge, scope, actor, credential, and incident-scoped revocation;
- revoke/disable descendants whose authority no longer resolves;
- invalidate refresh families, active leases, sessions, cached decisions, verifier state, and token links according to capability;
- publish status changes through Security Signals where configured;
- reconcile enforcement systems and retain failures;
- avoid claiming complete revocation until required consumers confirm or artifacts expire;
- preserve historical graph/evidence.

## 16. Replacement and Renewal

- Replacement creates a successor grant with explicit predecessor link.
- Existing descendants are not silently transferred to the successor.
- Each child must be re-evaluated against successor authority and policy.
- Overlap is bounded and visible.
- Renewal requires source authority, policy, risk, purpose, and delegate status revalidation.
- Approval and acceptance may be reused only under an explicit still-valid policy.
- Tokens/credentials must link to the exact grant version active at issuance.

## 17. Administrative Delegation

Support platform, tenant, developer, service, resource-owner, help-desk, and auditor profiles.

Requirements:

- administrative actions use stable permission vocabulary;
- resource/tenant scope is explicit;
- grant creator cannot exceed their own effective authority;
- self-grant and circular approval are prohibited by default;
- high-risk permissions require independent approval and short expiry;
- audit/provenance administration remains separated from subjects of review;
- delegated administrators cannot modify their source grant, evidence, or audit trail;
- break-glass grants are exceptional and reviewed after use.

## 18. Human, Service, Workload, and Agent Profiles

### Human delegation

- clear identity, duties, consent/acceptance, expiry, and revocation;
- accessible plain-language scope;
- substitute/absence workflows that do not transfer passwords or sessions.

### Service/workload delegation

- workload/client instance identity and attestation;
- sender-constrained, audience/resource-bound credentials;
- automatic renewal/revocation with no impossible human approval for every request;
- deployment/workflow identity binding.

### Agent delegation

- sponsor, task, tools, data, budgets, approvals, and child-agent limits;
- exact transaction receipts for high-impact operations;
- prompt/model identity is not a substitute for runtime/workload identity.

### Organization/trust-framework delegation

- legal/organizational authority, mandate, jurisdiction, role, evidence, and effective time;
- Trust Registry references rather than self-asserted authority.

## 19. API Requirements

Provide versioned endpoints for:

- `/profiles` and semantic modes;
- `/grants`, scopes, constraints, lifecycle, and versions;
- `/grants/{id}/proofs`;
- `/grants/{id}/parents`, children, ancestors, descendants, and effective authority;
- `/grants/{id}/tokens-credentials-sessions`;
- `/grants/{id}/decisions-actions-outcomes`;
- `/chains/resolve`, validate, compare, and historical reconstruction;
- `/proposals`, approvals, acceptance, and rejection;
- `/replacements` and renewals;
- `/revocations`, impact preview, execution, convergence, and reconciliation;
- `/search` with bounded tenant-safe filters;
- `/incidents/impact` and containment;
- `/evidence-bundles`, manifests, and verification;
- `/ingest` for authenticated protocol/product adapters.

API behavior:

- stable typed schemas, opaque pagination, time bounds, and field projections;
- idempotency for create/approve/accept/revoke/reconcile operations;
- optimistic concurrency and immutable active versions;
- asynchronous jobs for large descendant impact/revocation;
- no raw token, secret, private key, or arbitrary policy execution;
- no general graph traversal that can enumerate unauthorized subjects/resources;
- exact routes generated from live Tigrbl operations during implementation.

## 20. Search and Graph Safety

Delegation graphs expose sensitive relationships and organizational structure. Therefore:

- enforce tenant, realm, trust-domain, resource-owner, and purpose scopes;
- use authorized graph projections;
- mask subjects and resources according to role;
- bound depth, fan-out, result size, and time window;
- prevent count/timing leakage for hidden nodes where practical;
- require reason/purpose for protected exploration and exports;
- audit searches, graph expansion, and evidence access;
- separate public mandate facts from private operational delegation.

## 21. Evidence and Integrity

Evidence bundles include:

- root authority and verification result;
- grants, scopes, constraints, and lifecycle versions;
- approvals/acceptance and authentication context;
- parent-child edges and chain snapshot;
- attenuation proofs and evaluator versions;
- authorization decisions and safe action/outcome references;
- token/credential/session hashes and states;
- revocation/reconciliation progress;
- canonical digests, signatures/seals, redaction manifest, and retention state.

Use append-only supersession and protected checkpoints for high-assurance evidence. Export may map delegation to W3C PROV `actedOnBehalfOf`/qualified delegation, but internal typed authority semantics remain canonical.

## 22. Privacy and Retention

- Minimize personal identities, relationships, duties, reasons, actions, and resource details.
- Separate searchable pseudonymous identifiers from protected evidence.
- Never expose raw tokens or confidential claims.
- Apply role/purpose-based redaction and field-level authorization.
- Support tenant/region-specific retention, legal hold, deletion, and tombstoned integrity references.
- Preserve minimum security evidence for revoked/expired grants according to policy.
- Treat human delegation reasons and organizational relationships as potentially sensitive employment/legal data.
- Disclose when deletion prevents exact historical reconstruction.

## 23. Authority Chain Explorer UIX

### Overview

Show active and expiring grants, chain depth/fan-out, privileged/impersonation grants, stale proofs, orphaned chains, redundant/excess authority, unlinked tokens/actions, incomplete revocations, and regional/evidence posture.

### Grant inventory

Filter by delegator, delegate, profile, mode, resource/action, status, source authority, parent/root, expiry, proof state, token/action use, incident, region, and risk. Sensitive identities are masked unless authorized.

### Grant detail

Show source authority, delegator/delegate roles, semantic mode, normalized scope, constraints, policy, approval/acceptance, proof, parent/children, credentials, decisions/actions, lifecycle, revocation, and evidence.

### Chain explorer

Visualize root-to-actor paths, attenuation at each hop, status/freshness, and artifacts/actions. Every graph has accessible table and timeline alternatives. Multiple sources remain visually separate.

### Grant composer

Guide profile, parties, source authority, scope, constraints, purpose, expiry, redelegation, proof binding, approval, acceptance, and impact preview. Show source-versus-proposed diff and block unsafe broadening.

### Review and acceptance

Reviewers see exact authority, risk, descendants permitted, duration, evidence, conflicts, and obligations. Delegates see duties and data-handling responsibilities before acceptance.

### Revocation and incident center

Preview descendant grants, tokens, sessions, leases, decisions, actions, resources, and expected propagation. Show each invalidation/reconciliation stage, failures, retries, exceptions, and residual exposure.

### Historical reconstruction

Select a past time and reconstruct chain, authority, policy/proof, token/action links, and status then. Clearly distinguish historical from current validity.

### Evidence room

Provide read-only bundles, integrity verification, redactions, retention/hold, and export approval without granting graph mutation authority.

## 24. Security and Reliability

- Enforce tenant, realm, trust-domain, resource, profile, and field-level isolation.
- Separate grant creation, approval, acceptance, activation, revocation, audit, and evidence authority.
- Require step-up or workload attestation for privileged grants and high-impact operations.
- Prohibit self-approval, circular approval, and source-grant modification by delegates by default.
- Validate graph acyclicity, parent integrity, attenuation, time bounds, policy compatibility, and source freshness transactionally.
- Use durable outbox/idempotent consumers for token invalidation, signals, and reconciliation.
- Detect graph gaps, duplicate/conflicting edges, late events, clock anomalies, and partial revocation.
- Fail closed when source authority, proof, or required state is unavailable.
- Preserve decision/token service availability using bounded cached grants only within declared freshness policy.
- Protect evidence and audit tools from delegated administrators whose actions they record.
- Partition/index graph state for scale and bound all traversals.
- Meet WCAG 2.2 AA for graph, table, timeline, review, and incident workflows.

## 25. Stakeholder Requirements

### Technical marketing

Demonstrate human admin delegation, workload token exchange, agent sub-delegation, attenuation failure, multiple authority paths, and subtree revocation. Explain delegation versus impersonation and decision versus revocation convergence.

### Developer relations

Deliver grant/chain SDKs, RFC 8693 actor/subject examples, AuthZEN integration, service/workload and agent fixtures, safe graph queries, attenuation proof handling, token/action linkage, revocation webhooks/signals, and negative cases for cycles/broadening/stale parents.

### Sales and account management

Use discovery for principal types, administrative roles, on-behalf-of flows, token exchange, approval, maximum depth, expiry, revocation SLA, PEPs/resources, regions, audit, and existing delegation systems. Separate built-in lineage from adapter-dependent invalidation.

### GTM strategist

Position as accountable on-behalf-of authority for administration, APIs, workloads, agents, and regulated operations. Start with explainable grant lifecycle and token exchange, then expand into action receipts and cross-organization mandates. Do not market universal non-repudiation.

### Copywriter

Standardize `source authority`, `responsible subject`, `delegator`, `delegate/actor`, `delegation`, `impersonation`, `grant`, `scope`, `constraint`, `attenuation`, `chain`, `descendant`, `revocation requested`, and `revocation reconciled`. Avoid vague “access shared” or “fully revoked.”

## 26. Delivery Instructions

### Frontend engineer

- Generate typed clients from grant, graph, proof, token/action, and revocation schemas.
- Preserve tenant/realm/profile/historical-time/projection context throughout navigation.
- Implement bounded server-side graph queries and accessible table/timeline alternatives.
- Render server-authorized projections; client masking is not access control.
- Use asynchronous jobs for large impact/revocation operations with cancellation and partial failure.
- Require semantic diff/preview/confirmation for grant activation, replacement, impersonation, and revocation.
- Keep identifiers/reasons out of URLs, analytics, and session replay.

### UIX designer

- Make responsible subject, actor, semantic mode, source authority, scope, and current validity persistent.
- Establish visual states for active, pending, suspended, stale, expired, revoked, replaced, collapsed, orphaned, and partially reconciled.
- Show authority narrowing at each edge, not only final scope.
- Keep multiple paths separate and explain the effect of removing one.
- Design no-access, redacted, missing-parent, unknown-constraint, and incomplete-revocation states.
- Optimize grant review, incident response, and audit reconstruction separately.

### Copywriter

- Explain who acts, for whom, under what scope, until when, and with what responsibility.
- State impersonation consequences prominently.
- Distinguish broker-side status from downstream invalidation.
- Write neutral diagnostics for invalid or suspicious chains.
- Place evidence limitations beside conclusions.

## 27. Delivery Phases

### Phase 1: Unified grants and chain exploration

- reconcile existing contracts/tables/runtime into a transactional service;
- delegation profiles and semantic modes;
- grant/search/detail/chain/effective-authority APIs;
- Authority Chain Explorer inventory, detail, graph/table/timeline;
- retain existing token-exchange and attenuation evidence.

### Phase 2: Governed authoring and lifecycle

- proposal, approval, acceptance, activation, replacement, renewal, suspension, expiry, and revocation;
- Grant Composer and source-versus-child diff;
- administrative, human, and workload profiles;
- notifications, evidence bundles, and privacy projections.

### Phase 3: Action linkage and revocation convergence

- Authorization Provenance and PEP receipt linkage;
- token/session/lease/action descendant invalidation;
- Security Signals propagation and reconciliation;
- incident impact, subtree containment, and residual exposure.

### Phase 4: Agents, organizations, and ecosystem

- agent task/tool/budget profile;
- trust-framework/organizational mandates;
- GNAP adapter where a concrete use case warrants it;
- external provenance export, regional controls, scale, and certification.

## 28. Acceptance Criteria

### API/domain

- Every grant resolves a valid source authority and declared semantic mode.
- Active children are provably no broader/longer than parent authority under supported constraint types.
- Unknown constraint ordering fails closed.
- Chains are bounded, acyclic, tenant/realm-safe, and point-in-time reconstructable.
- Multiple paths preserve separate provenance and are not combined unsafely.
- Token/credential/session/action links contain no raw bearer or secret material.
- Replacement does not silently inherit descendants.
- Revocation identifies descendants and tracks downstream invalidation/reconciliation.
- Impersonation is disabled unless an explicit profile/policy authorizes it.
- Corrections and lifecycle changes preserve immutable history.

### UIX

- An authorized operator can explain root authority through the current actor.
- A reviewer can compare source and proposed authority before approval.
- Delegation and impersonation cannot be confused visually or linguistically.
- Revocation preview shows affected descendants and residual limitations.
- Historical views cannot be mistaken for current validity.
- Graphs have accessible equivalent tables/timelines.
- Core workflows meet WCAG 2.2 AA.

### Evidence/business

- Fixtures cover direct, multi-hop, multiple-source, human, workload, agent, token exchange, impersonation, expiry, replacement, cycle, broadening, stale proof, parent revoke, partial propagation, and historical reconstruction.
- Marketing claims map independently to grant lifecycle, attenuation proof, token lineage, action lineage, and revocation convergence.
- An auditor can verify a redacted chain bundle without database access.

## 29. Success Measures

- percentage of delegation-bearing decisions/tokens/actions linked to canonical grants;
- active grants with verified source authority and current attenuation proof;
- mean/p95 chain depth and fan-out by profile;
- stale, orphaned, cyclic, broadened, or conflicting chain findings;
- privileged and impersonation grant count/age;
- expiring grants renewed or closed before lapse;
- time to explain an on-behalf-of action;
- revocation request-to-descendant identification time;
- revocation request-to-artifact/enforcement reconciliation time;
- residual/unverified descendant count and age;
- redundant/excess authority removed;
- support and audit reconstruction time;
- unauthorized graph-access or privacy incidents.

## 30. Source Evidence

### Repository

- `.ssot/specs/SPEC-1092-delegation-graph-and-token-exchange-provenance-requirements.yaml`
- `.ssot/specs/SPEC-1197-delegation-provenance-contract.yaml`
- `.ssot/specs/SPEC-1206-authority-derivation-graph-contract.yaml`
- `.ssot/specs/SPEC-1208-delegation-attenuation-proof-contract.yaml`
- `.ssot/specs/SPEC-1213-delegation-grant-lifecycle-contract.yaml`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/delegation/`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/authority/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/delegation_grant/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/authority_derivation_graph/`
- `pkgs/20-providers/tigrbl-security-authorization-provenance-builder/`
- `pkgs/30-storage-runtime/tigrbl-authz-policy-authority-derivation-graph/`
- `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/token_exchange.py`
- `tests/security/test_delegation_provenance.py`
- `tests/unit/test_delegation_grant_lifecycle_contract.py`
- `tests/unit/test_delegation_attenuation_proof.py`
- `tests/unit/test_delegation_attenuation_robustness_t2.py`
- `tests/unit/test_authority_closure_monotonicity.py`
- `tests/unit/test_authorization_provenance.py`

### Standards and primary guidance

- [RFC 8693, OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693): subject/actor tokens, delegation versus impersonation, actor claims, resources, audiences, and scopes.
- [RFC 9635, GNAP](https://www.rfc-editor.org/rfc/rfc9635): grant negotiation and delegation with client-instance proof and optional resource-owner interaction; use only through an explicit adapter/profile.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/): agents, activities, responsibility, `actedOnBehalfOf`, and qualified delegation for interoperable provenance mapping.
- [NIST least privilege](https://csrc.nist.gov/glossary/term/least_privilege) and [NIST SP 800-171 Rev. 3](https://csrc.nist.gov/pubs/sp/800/171/r3/final): minimum necessary authority, privileged-function logging, audit protection, and periodic review.
- [RFC 9396, OAuth Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396): typed authorization details useful for preserving precise delegated transaction scope.
- [RFC 9449, DPoP](https://www.rfc-editor.org/rfc/rfc9449) and [RFC 8705, OAuth mTLS](https://www.rfc-editor.org/rfc/rfc8705): sender-constrained protocol artifacts that can maintain actor/client proof continuity.

## 31. Explicit Non-Claims

- A recorded chain does not prove each source-authority assertion is true unless independently verified.
- A token actor claim is not the canonical delegation grant or complete chain.
- Token exchange does not inherently propagate later revocation to output tokens.
- Delegation does not transfer accountability entirely away from the responsible subject or delegator.
- Impersonation is not equivalent to transparent delegation.
- An attenuation hash/result is not sufficient when typed constraint semantics were not evaluated.
- Revoking a database grant does not prove every token, session, cache, lease, or resource action was invalidated.
- Graph reachability alone does not authorize an action; current policy and context still apply.
- W3C PROV mapping does not make private delegation relationships public linked data.
- Existing repository lifecycle/proof/token tests do not establish complete cross-product delegation coverage or downstream revocation convergence.
