# Provisioning and Directory API + Directory and SCIM Center UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-provisioning` + `@tigrbl-auth/directory-scim-center-uix`  
**Protocol frontdoor:** tenant-scoped SCIM 2.0 under `/tenants/{tenant_slug}/scim/v2`  
**Status:** New product surface; contracts, helper behavior, durable projections, principals, memberships, and audit foundations exist  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-provisioning`  
**Proposed protocol owner:** `pkgs/50-protocols/tigrbl-identity-scim`  
**Proposed UIX owner:** `pkgs/95-ui/directory-scim-center-uix`

## 1. Product Decision

Create a dedicated inbound provisioning and directory product surface that receives identity lifecycle changes from enterprise identity providers, HR/IGA systems, and approved automation, reconciles those changes with canonical Tigrbl principals and memberships, and gives administrators safe operational control.

The pairing has three boundaries:

- **SCIM protocol plane:** RFC 7643/7644 resources, discovery, filtering, PATCH, errors, pagination, ETags, and optional bulk behavior.
- **Provisioning control plane:** source connections, credentials, attribute mappings, ownership, reconciliation, dry runs, activation, quarantine, retry, audit, and reporting.
- **Directory experience:** people, groups, memberships, source-of-truth status, conflicts, lifecycle events, and access-impact views.

SCIM is not login, OIDC federation, generic tenant CRUD, or an authorization server. The SCIM API consumes a tenant-bound credential and mutates identity state according to approved provisioning policy. It must never issue access tokens or bypass canonical principal, tenant, membership, credential, session, and audit lifecycles.

## 2. Current Repository Reality

The repository already provides useful foundations:

- SCIM governance contracts for schema, user, group, and patch operation;
- an in-memory `ScimProvisioningPlane` supporting schema registration, user/group provisioning, limited patching, tenant snapshots, and negative tests;
- durable `ScimSchemaRecord`, `ScimUserRecord`, `ScimGroupRecord`, and append-only `ScimPatchEvent` tables;
- canonical user, tenant, tenant-membership, subject-alias, role, entitlement, session, credential, and audit storage;
- `PrincipalDirectory` behavior for principal status, memberships, aliases, tenant listing, and alias collision rejection;
- resource-validation capabilities suitable for authenticating a SCIM client;
- governance work for entitlements and access reviews;
- a tenant-admin Groups and Roles page showing visible assignments;
- SSOT planning and repository research in `docs/scim-v2-focus.md` and the vendor coverage matrix.

These are not a deployable SCIM service provider. No `/scim/v2` frontdoor, RFC-complete schemas, filter grammar, PATCH evaluator, list response, SCIM error mapper, ETag behavior, connection lifecycle, reconciliation engine, or operator UIX was found.

The May 2026 SCIM focus document predates the durable SCIM tables now present. Those tables improve readiness, but they are currently projections with global uniqueness and JSON members/attributes; implementation must decide how they reconcile with canonical principals and normalized membership edges before production use.

## 3. Users and Jobs

### Tenant directory administrator

1. Connect an enterprise provisioning source and generate a least-privilege credential.
2. map source attributes and groups into tenant identities, memberships, roles, or entitlements.
3. test create, update, deactivate, reactivate, group push, and membership removal.
4. monitor sync health, conflicts, quarantined changes, retries, and deprovisioning impact.
5. rotate credentials, suspend a source, and export redacted support evidence.

### Identity governance and security team

1. define which source owns each attribute, lifecycle state, group, and entitlement.
2. prevent one source from overwriting protected or locally governed values.
3. review joiner, mover, leaver, orphan, dormant, and privileged-access consequences.
4. prove who changed an identity, through which source, with which payload digest and result.
5. enforce separation of duties for mapping, activation, privileged group push, and bulk deprovisioning.

### Enterprise integration engineer

1. discover accurately advertised SCIM capabilities and schemas.
2. execute standard user/group create, lookup, update, patch, deactivate, and membership flows.
3. receive RFC-shaped errors, stable IDs, pagination, ETags, and correlation identifiers.
4. test safely using vendor-compatible fixtures and understand unsupported behavior.

### Help desk and account manager

1. find an identity by safe identifiers and see source/sync status.
2. explain why a person was created, changed, suspended, or omitted.
3. retry a recoverable operation or escalate with a redacted evidence bundle.
4. avoid making identity or access mutations outside assigned authority.

## 4. Architectural Ownership

### SCIM protocol package owns

- RFC resource and discovery schemas;
- filter parsing/evaluation, attribute projection, pagination, sorting, and PATCH semantics;
- SCIM error types and HTTP mapping;
- version/ETag and conditional request rules;
- bulk request/response semantics if later enabled;
- protocol conformance fixtures independent of a specific UI or database.

### Provisioning API owns

- tenant resolution and SCIM resource-server composition;
- source connection, credential, mapping, ownership, lifecycle, and reconciliation operations;
- translation between SCIM resources and canonical identity commands;
- product-safe route exposure, scopes, rate limits, idempotency, audit, and observability;
- UI-facing management schemas and reports.

### Existing owners retain semantics

- principals and aliases remain owned by identity principal contracts/capabilities;
- durable users, memberships, groups/projections, events, and credentials remain in storage;
- authorization decisions remain in the authorization service;
- token/service-key verification remains in resource validation/security providers;
- entitlement and access review semantics remain in governance packages;
- UIX owns presentation and interaction, not protocol or reconciliation rules.

SCIM projection rows must not become a parallel identity database. Each provisioned resource needs an explicit mapping to a canonical principal/group/membership or a documented quarantine state.

## 5. Product Scope

### Baseline SCIM 2.0 service-provider surface

- `ServiceProviderConfig`, `ResourceTypes`, and `Schemas` discovery;
- core User and Group resources;
- Enterprise User extension after canonical attribute mapping is ready;
- create, read, list/search, replace, PATCH, deactivate/delete semantics;
- group membership push;
- filter subset needed for major provisioning clients, then expanded toward RFC coverage;
- pagination, attribute projection, sorting where advertised, and ETags;
- SCIM Error responses with correct status and `scimType`;
- tenant-bound bearer token or service credential authentication.

### Provisioning management

- source connection and credential lifecycle;
- attribute, status, group, and entitlement mappings;
- source ownership and precedence policy;
- dry-run validation and vendor test sequences;
- reconciliation, drift detection, retry, quarantine, replay-safe recovery, and reporting;
- staged rollout, suspension, rotation, retirement, and historical evidence.

### Directory experience

- tenant people and non-human identities where authorized;
- groups, memberships, aliases, status, source, last sync, and access impact;
- lifecycle and conflict queues;
- bulk review/actions with high-blast-radius safeguards;
- export only through governed, redacted, tenant-scoped workflows.

### Explicitly later

- outbound provisioning connectors where Tigrbl acts as SCIM client;
- HR-driven orchestration across multiple downstream applications;
- generic LDAP/Active Directory synchronization agents;
- cross-tenant directory aggregation;
- custom schema marketplace;
- SCIM Bulk until single-resource semantics and containment are proven.

## 6. SCIM API Requirements

The tenant-scoped route is preferred for local and hosted deployments because enterprise systems configure one base URL per tenant/application:

`/tenants/{tenant_slug}/scim/v2`

Host-based routing may be added later, but it must resolve through the same tenant authority and must not alter protocol semantics.

### Discovery

| Method | Route | Requirement |
|---|---|---|
| `GET` | `/ServiceProviderConfig` | Advertise only implemented PATCH, bulk, filter, sort, ETag, password, and auth behavior. |
| `GET` | `/ResourceTypes` | Publish supported resource types and endpoints. |
| `GET` | `/ResourceTypes/{id}` | Return one resource-type definition or SCIM error. |
| `GET` | `/Schemas` | Return supported schemas and extensions. |
| `GET` | `/Schemas/{uri}` | Return exact attribute metadata by schema URI. |

### Users

| Method | Route | Requirement |
|---|---|---|
| `GET` | `/Users` | Filtered, paginated, projected list response. |
| `POST` | `/Users` | Idempotent-by-policy create with stable SCIM ID and canonical mapping. |
| `GET` | `/Users/{id}` | Tenant-safe read with `meta` and ETag. |
| `PUT` | `/Users/{id}` | Full replacement honoring mutability and required attributes. |
| `PATCH` | `/Users/{id}` | RFC PATCH operation evaluation including `add`, `replace`, and `remove`. |
| `DELETE` | `/Users/{id}` | Default to governed deactivation/tombstone behavior, not silent hard deletion. |
| `POST` | `/Users/.search` | Structured search where enabled. |

### Groups

Provide equivalent list/create/read/replace/PATCH/delete/search routes for `/Groups`. Group PATCH must correctly address members by value filters, reject cross-tenant membership, preserve idempotency, and return the resulting representation or specified no-content behavior consistently.

### General protocol behavior

- Use SCIM media type `application/scim+json` where required.
- Support `schemas`, `id`, `externalId`, and `meta` consistently.
- Interpret `startIndex` as one-based and return `totalResults`, `itemsPerPage`, and `Resources` correctly.
- Implement `attributes` and `excludedAttributes` without leaking protected fields.
- Apply schema `mutability`, `returned`, `uniqueness`, `required`, `caseExact`, canonical values, and multi-value rules.
- Use weak or strong ETags consistently and honor `If-Match` where enabled.
- Return SCIM Error resources for invalid filter, invalid path, uniqueness, mutability, version conflict, payload size, and unsupported behavior.
- Never advertise filter operators, sorting, PATCH, ETag, or Bulk beyond tested support.

### Initial filter profile

At minimum support interoperable lookup patterns commonly used by provisioning clients:

- `userName eq "..."`;
- `externalId eq "..."`;
- `id eq "..."`;
- group `displayName eq "..."`;
- member selection such as `members[value eq "..."]` where required for PATCH;
- logical `and` for bounded indexed equality expressions.

The parser must reject unsupported grammar safely instead of approximating meaning. Broader comparison, presence, substring, nesting, and logical operators can be added with conformance tests and query-cost controls.

## 7. Management API Requirements

### Connection lifecycle

- `GET/POST /admin/provisioning/connections`;
- `GET/PATCH /admin/provisioning/connections/{connection_id}`;
- actions for validate, test, submit, approve, activate, suspend, rotate credential, and retire;
- write-only credential issuance with one-time display and hashed/indirect storage;
- connection-specific base URL, scopes, allowed networks or mTLS/DPoP policy where configured;
- active/draft version separation and rollback.

### Mapping and ownership

- versioned mappings for SCIM paths to canonical attributes;
- normalization, required/default values, enum mapping, and safe transformations;
- per-attribute source authority: source-owned, local-owned, fill-if-empty, immutable, or review-required;
- status mapping for `active`, suspended, staged, deleted, and source-missing states;
- group-to-role/entitlement mapping as an explicit governed rule, never implicit string matching;
- subject alias/link behavior with collision quarantine.

### Reconciliation and operations

- connection inventory and last-sync cursor where relevant;
- dry-run diff for a candidate resource or test batch;
- drift scan between source projection and canonical identity state;
- operation timeline with payload digest, target, source client, result, reason code, latency, retry count, and correlation;
- retry only when operation semantics and idempotency allow it;
- dead-letter/quarantine queue for conflicts and policy failures;
- replay from immutable input evidence only with authorization and duplicate protection;
- impact analysis before source suspension, mapping activation, group remap, or bulk deactivation.

## 8. Canonical Data Requirements

### Provisioning connection

- connection ID, tenant ID, name, source/vendor profile, lifecycle state, and version;
- SCIM base URL and credential reference/fingerprint;
- granted scopes, network/proof constraints, rate policy, and expiry;
- mapping and ownership policy versions;
- active time, last request, last success, error rate, and health;
- creator, approvers, change justification, and audit linkage.

### External resource link

- tenant, connection, SCIM resource type, stable SCIM ID, `externalId`, and canonical object ID;
- source version/ETag, canonical version, last payload digest, and last reconciliation time;
- state: linked, pending, quarantined, conflict, inactive, tombstoned, or detached;
- uniqueness constraints scoped by tenant and connection rather than accidental global uniqueness.

### User projection

- RFC core attributes including name, display name, user name, active state, emails, phone numbers, addresses, locale/timezone, title, and profile URL where supported;
- enterprise extension attributes such as employee number, cost center, organization, division, department, and manager only after privacy and canonical mapping decisions;
- schemas, external ID, metadata, source, and redacted extension payload.

### Group and membership

- canonical group ID plus source link, display name, type, owner, lifecycle, and mapping status;
- normalized membership edge with group, member principal/group, source, validity, status, and provenance;
- no unbounded JSON-members array as the only production relationship representation;
- nested groups only after cycle, depth, expansion, authorization, and vendor behavior are defined.

### Provisioning event

- immutable event ID, tenant, connection/client, request ID, operation, resource, result, reason, and timestamps;
- input/output digests and safe change summary;
- mapping/policy/version references;
- retry/replay lineage and correlated canonical lifecycle events;
- sensitive raw payload retention disabled by default or placed under explicit evidence retention controls.

## 9. Reconciliation and Lifecycle Semantics

### Create/link decision

1. authenticate and tenant-bind the provisioning client;
2. validate media type, size, schema, mutability, and uniqueness;
3. locate an existing external link by tenant, connection, resource type, and SCIM ID/external ID;
4. evaluate configured safe linking identifiers without trusting email as universal identity proof;
5. quarantine ambiguity or collision rather than merging accounts;
6. apply versioned mapping and source-ownership rules;
7. authorize the resulting canonical changes;
8. commit canonical identity, external link, membership, and audit changes atomically;
9. return the SCIM representation and version derived from committed state.

### Update precedence

- A source may update only fields it owns or fields governed as fill-if-empty.
- Local changes to source-owned fields should either be prohibited or surfaced as drift, not silently oscillate.
- Two sources must not overwrite the same authoritative attribute without an explicit precedence/conflict policy.
- Privileged role/entitlement mapping requires reviewable policy and cannot be created merely because a group name matches.

### Deprovisioning

`DELETE` or `active=false` must follow a defined lifecycle:

1. mark source link inactive and create immutable evidence;
2. disable new authentication/authorization as policy requires;
3. remove or expire source-owned memberships and entitlements;
4. revoke or constrain sessions, credentials, grants, and tokens according to risk policy;
5. preserve legal/audit records and controlled recovery window;
6. hard-delete personal data only through retention/privacy workflow.

The UI and API must explain the distinction between deactivate, suspend, unlink, tombstone, and permanently erase.

## 10. Directory and SCIM Center UIX

### Overview

- active connections, identities/groups managed, operations, failures, quarantines, drift, and expiring credentials;
- joiner/mover/leaver counts and privileged changes;
- action cards prioritized by blast radius and recoverability;
- clear protocol-support and test status without implied vendor certification.

### Connection setup wizard

1. name source and select generic/vendor test profile;
2. create credential and show it once with storage warning;
3. display tenant-specific base URL and scopes;
4. configure schema/attribute and status mapping;
5. configure group, role, and entitlement rules;
6. select source ownership and conflict policy;
7. run protocol and lifecycle test sequence;
8. review expected changes, security findings, and rollback;
9. submit/approve/activate.

### Directory explorer

- people, groups, memberships, services/workloads where authorized, and source links;
- search by permitted identifiers with safe highlighting;
- status, source, canonical ID, external ID, last sync, version, and conflict indicators;
- identity detail with attributes grouped by authority/source and a lifecycle timeline;
- access-impact summary linking roles, entitlements, sessions, and applications without duplicating Policy Studio;
- visible distinction between canonical fields and source projections.

### Mapping studio

- source schema tree and canonical destination model;
- transformation preview using synthetic/redacted fixtures;
- mutability, required, privacy, uniqueness, and authority badges;
- before/after semantic diff and validation findings;
- group-to-access mappings separated into a higher-risk review panel;
- version comparison, draft, approval, activation, rollback, and change justification.

### Sync activity and quarantine

- operation list by time, connection, resource, method, result, reason, and latency;
- human-readable PATCH change summaries plus restricted raw payload access;
- filters for retryable, policy denied, conflict, invalid schema, uniqueness, rate limit, and server failure;
- quarantine resolution paths: link, create separate, correct mapping, reject, or request source correction;
- retry/replay controls showing idempotency and expected effects.

### Group and membership management

- source-managed versus local groups and locked/owned fields;
- membership delta preview and nested-group warnings;
- high-impact change review showing users, access grants, sessions, and applications affected;
- bulk selection with limits, background jobs, downloadable safe result manifest, and partial-failure handling;
- accessible tables as the primary interaction; relationship visualization may supplement them.

## 11. Security, Privacy, and Reliability

- Require tenant-bound, least-privilege service credentials with expiry, rotation, revocation, last-used evidence, and optional proof/network restrictions.
- Enforce resource scopes separately for read, write, groups, schema discovery, reconciliation, and privileged mapping.
- Rate limit by tenant, connection, credential, operation cost, and failed authentication; return protocol-compatible responses.
- Bound filter complexity, result size, PATCH operations, member counts, attribute depth, extension payloads, and bulk size.
- Prevent mass assignment by using schema allowlists and mutability/ownership enforcement.
- Reject cross-tenant IDs, group members, external links, and references without existence disclosure.
- Use transactions/outbox patterns so identity mutation and audit/event emission cannot diverge silently.
- Redact secrets and sensitive attribute values in logs, traces, metrics, errors, notifications, and support exports.
- Protect against CSV/formula injection and data exfiltration in exports.
- Define deduplication/idempotency for network retry and concurrent requests.
- Use optimistic concurrency to prevent stale overwrites.
- Treat deprovisioning and group push as security-sensitive; measure and alert on delay/backlog.
- Test rollback, partial dependency outage, queue replay, migration, backup/restore, and tenant deletion.

## 12. Stakeholder Requirements

### Technical marketing

- demonstrate a complete create-update-group-deactivate sequence from a realistic enterprise source fixture;
- show product honesty through `ServiceProviderConfig` and evidence-backed capability badges;
- frame the value as automated joiner/mover/leaver lifecycle, reduced manual errors, fast deprovisioning, and auditable group access;
- prepare vertical stories for B2B SaaS, healthcare workforce, education, finance, government, contractor access, and multi-location operations.

### Developer relations

- provide RFC-shaped curl examples, SDK types, Postman/Bruno collection, and local test server/fixtures;
- document pagination, supported filters, PATCH paths, ETags, errors, limits, retry, and deactivation semantics;
- publish vendor-neutral and tested vendor-profile guides;
- include negative fixtures for duplicate userName/externalId, cross-tenant member, stale ETag, invalid filter/path, collision, oversized group, and retry.

### Sales and account management

- use an integration worksheet covering source, tenant, user/group counts, attributes, ownership, deactivation SLA, group push, credential policy, networking, and testing;
- receive a compatibility/readiness report that distinguishes protocol capability from tested vendor interoperability;
- explain customer-versus-Tigrbl ownership for mappings, source data, conflict resolution, retries, and deprovisioning;
- estimate onboarding effort from schema customization, source count, group complexity, identity matching, and lifecycle policy.

### GTM strategist

- package Enterprise Provisioning, Group Push, Directory Governance, and Advanced Reconciliation as clear modules;
- prioritize inbound SCIM for B2B/workforce customers before outbound connector orchestration;
- meter by active connection, managed identity, operation volume, or governance tier while avoiding pricing that discourages deprovisioning;
- pair provisioning with enterprise federation, authorization, audit, and access review offerings.

### Copywriter

- distinguish sync, provision, link, reconcile, deactivate, suspend, unlink, delete, and erase;
- never call a retrieved or accepted record "verified identity";
- say which system owns a field and why editing may be unavailable;
- make group-to-access effects and deprovisioning consequences explicit;
- provide actionable protocol error and recovery text without exposing protected data.

## 13. Delivery Instructions

### Frontend engineer

- generate typed management clients from canonical schemas; do not use the SCIM protocol endpoints as the browser admin API;
- never persist connection secrets or raw sample attributes in URLs, local storage, analytics, or client logs;
- implement server-driven field metadata, reason codes, permissions, lifecycle transitions, and impact summaries;
- support virtualized accessible tables, bounded selection, background-job status, partial failure, stale ETag, and optimistic updates only where safe;
- preserve tenant context and route authorization across deep links;
- instrument setup completion, validation failures, sync delay, quarantine age, retry outcome, and deprovisioning latency without identity attribute values.

### UIX designer

- make canonical versus source-projected state and source ownership immediately legible;
- design lifecycle status separately from connection health and last operation result;
- provide progressive disclosure from business impact to protocol detail;
- design zero, first sync, healthy, delayed, rate-limited, partial, drifting, conflicting, quarantined, suspended, credential-expired, and recovery states;
- require preview and approval for mapping activation, privileged group mapping, mass membership removal, and deprovisioning;
- meet WCAG 2.2 AA with keyboard operation, focus recovery, non-color status, clear table semantics, and accessible diff announcements.

### Copywriter

- create status, ownership, error, remediation, confirmation, notification, and empty-state catalogs;
- write short explanations for SCIM concepts alongside protocol names;
- include scope, reversibility, affected identities/access, and recovery in dangerous-action copy;
- distinguish customer-correctable payload errors from service incidents and policy denials;
- avoid promising real-time behavior unless measured SLAs support it.

## 14. Delivery Phases

### Phase 1: Canonical SCIM core

- protocol package, models, discovery, errors, User/Group resources, basic filter, pagination, projection, and ETag;
- external link and normalized membership storage/reconciliation;
- authenticated tenant-scoped frontdoor and audit;
- scripted create, lookup, update, deactivate, group create, add member, and remove member fixtures.

### Phase 2: Connection and operations UIX

- connection lifecycle, one-time credential, mappings, source ownership, setup testing, health, activity, quarantine, retry, and evidence export;
- directory explorer and source/canonical comparisons;
- migration or reconciliation strategy for existing SCIM projection rows.

### Phase 3: Governance depth

- Enterprise User extension, advanced filters/PATCH paths, group-to-entitlement policy, access-impact analysis, access reviews, deprovisioning orchestration, staged rollout, and stronger proof binding;
- validated vendor interoperability profiles.

### Phase 4: Scale and ecosystem

- optional Bulk with strict containment;
- outbound provisioning/connector framework if market demand is proven;
- HRIS/IGA source packs, asynchronous reconciliation, richer reporting, and multi-source mastering.

## 15. Acceptance Criteria

### Protocol and API

- Discovery endpoints advertise exactly the implemented capabilities and schema.
- A standards-shaped client can create, query, update, deactivate, reactivate, group, and ungroup a user with stable IDs and correct responses.
- Duplicate, conflicting, cross-tenant, invalid-filter, invalid-path, stale-version, and unauthorized operations fail closed with SCIM errors.
- Every SCIM resource maps to canonical state or an explicit quarantine; no silent parallel identity exists.
- Group membership is normalized, tenant-safe, transactional, and provenance-linked.
- Credential rotation does not require changing the SCIM base URL or losing history.

### UIX

- An administrator can configure and pass a baseline lifecycle test without server config edits.
- Attribute/source ownership and the effect of each mapping are understandable before activation.
- Quarantined records show reason, safe evidence, permitted resolutions, and predicted result.
- Bulk and deprovisioning actions disclose blast radius, access/session impact, recoverability, and progress.
- All critical tasks work without a relationship graph, drag-and-drop, hover, or color alone.

### Evidence and business

- DevRel can run repeatable positive and negative interoperability fixtures.
- Sales can generate a redacted readiness report without exposing identities or secrets.
- Technical marketing can demonstrate lifecycle automation with deterministic sample data.
- Any SCIM or vendor compatibility claim links to versioned endpoint tests and release evidence.

## 16. Success Measures

- median connection setup time and test-pass rate;
- provisioning operation success and retry rates by safe reason category;
- p50/p95 joiner, mover, and leaver propagation latency;
- deprovisioning SLA attainment;
- mapping conflict, identity collision, quarantine, and stale-record rates;
- orphaned identity and source-link counts;
- privileged membership changes reviewed before activation;
- support cases per connection and mean time to resolution;
- percentage of active connections with current credentials, tested mappings, and recent health checks.

Guardrails include cross-tenant mutation, accidental account merge, unauthorized access grant, delayed deprovisioning, silent data loss, source oscillation, secret exposure, and overclaimed conformance.

## 17. Source Evidence

### Repository

- `docs/scim-v2-focus.md`
- `docs/scim-v2-vendor-coverage-matrix.md`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/governance/scim/`
- `pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/governance_extension.py`
- `pkgs/40-capabilities/tigrbl-identity-principals/src/tigrbl_identity_principals/directory.py`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/scim_schema/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/scim_user/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/scim_group/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/scim_patch_event/`
- canonical user, tenant-membership, subject-alias, entitlement, session, credential, and audit tables;
- `tests/unit/test_provisioning_governance_ecosystem_boundary.py` and SCIM/governance/storage tests.

### Standards

- [RFC 7643: System for Cross-domain Identity Management - Core Schema](https://www.rfc-editor.org/rfc/rfc7643)
- [RFC 7644: System for Cross-domain Identity Management - Protocol](https://www.rfc-editor.org/rfc/rfc7644)
- [IANA SCIM Schema URIs](https://www.iana.org/assignments/scim/scim.xhtml)
- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)

## 18. Explicit Non-Claims

This brief does not claim that the current repository:

- exposes a production SCIM 2.0 service-provider API;
- conforms fully to RFC 7643 or RFC 7644;
- supports a complete SCIM filter or PATCH grammar;
- interoperates with any named vendor in a certified production profile;
- has resolved canonical group, membership, multi-source ownership, or deprovisioning semantics;
- supports outbound provisioning, LDAP synchronization, or SCIM Bulk;
- can safely grant roles or entitlements based only on incoming group names.

Those claims require implemented protocol behavior, canonical reconciliation, negative and scale testing, interoperability evidence, security review, operational proof, and release certification.
