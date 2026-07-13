# Federation and Trust API + Trust Center UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-federation-trust` + `@tigrbl-auth/trust-center-uix`  
**Status:** New product surface; relevant contracts, providers, graphs, discovery, JOSE, storage, and tenant authority foundations exist  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-federation-trust`  
**Proposed UIX owner:** `pkgs/95-ui/trust-center-uix`

## 1. Product Decision

Create a dedicated federation management and trust-resolution product surface for connecting external identity providers, relying parties, authorization servers, protected resources, workloads, and multilateral trust networks.

The pairing must expose two separated planes:

- **Runtime trust plane:** discovery, entity-statement publication/fetching, trust-chain resolution, metadata derivation, upstream login initiation/callback support, key refresh, and trust-status checks used by protocol runtimes.
- **Management plane:** connection configuration, trust-anchor governance, metadata review, claim transformation, routing, testing, approval, rollout, revocation, and incident response used by Trust Center.

The API must compose existing OIDC federation contracts, upstream `IdentityProvider` and `FederatedSession` models, JOSE/JWKS facilities, issuer discovery, tenant trust-domain authority, trust graph, and provenance capabilities. It must not embed federation policy independently in OAuth/OIDC routes, tenant screens, or browser code.

Trust Center is a policy and operations console. It never handles an end user's upstream password, exposes client secrets after creation, or becomes a required hop in an authentication transaction.

## 2. Why This Pairing Is Needed

The repository already contains meaningful foundations:

- `FederationEntityStatementRequest`, `FederationEntityStatementResult`, and `OidcFederationPort`;
- a `StaticOidcFederationProvider` capability advertising `entity_statement` support;
- upstream `IdentityProvider` contracts with issuer, discovery URL, audience, claims mapping, scopes, logout capability, key-set version, and enabled state;
- `FederatedSession` contracts with provider, tenant, issuer, audience, normalized claims, and binding time;
- durable trust federation graph, node, and edge tables;
- trust-domain and trust-edge evaluation, bounded path resolution, edge revocation, constraints, and cross-cloud workload mapping;
- OAuth/OIDC discovery and tenant-scoped issuer/JWKS authority;
- JOSE signing, verification, algorithm policy, key rotation, and JWKS cache packages;
- issuer-confusion, runtime-issuer-alignment, trust-graph-integrity, tenant-discovery, and metadata tests;
- a deprecated federation registry whose replacement requirements can be recovered without restoring its package boundary.

The missing product layer is a canonical lifecycle and operator experience. Today, these primitives do not collectively provide safe partner onboarding, metadata diffing, trust-chain inspection, staged activation, routing, health monitoring, or emergency containment.

This is also a timely standards opportunity. OpenID Federation 1.0 became a Final Specification in February 2026 and defines signed entity statements, trust anchors, intermediates, trust chains, metadata policy, trust marks, and automatic registration. Tigrbl's existing entity-statement port and trust graph are a strong starting point, but must not be marketed as conformance until a full implementation and test profile exist.

## 3. Users and Jobs

### Tenant identity administrator

1. Connect an enterprise or social OIDC identity provider without editing server configuration.
2. Import and validate metadata, map claims, select scopes, and test login safely.
3. Route users by organization, email domain, tenant, application, or explicit choice.
4. Stage, activate, suspend, rotate, and remove a connection without creating an authentication outage.
5. Diagnose failed callbacks, issuer changes, key rotation, and logout behavior.

### Platform and security operator

1. Define trust anchors, allowed issuers, algorithms, endpoints, redirect constraints, and chain depth.
2. Resolve and inspect every statement and signature in a trust chain.
3. Compare published metadata with last-known-good state and approve material changes.
4. Detect expired statements, stale keys, invalid signatures, unreachable endpoints, loops, ambiguity, and excessive trust.
5. Quarantine a provider, anchor, edge, key, or chain and understand affected tenants and applications.

### Application developer

1. Select an approved connection or use tenant discovery/routing.
2. obtain stable callback, logout, issuer, and connection identifiers.
3. Test a connection with non-production credentials and inspect normalized claims.
4. receive actionable errors that do not reveal secrets or internal trust topology.

### Partner or federation operator

1. Exchange metadata and keys through a standards-based mechanism.
2. Register and maintain subordinate or peer relationships.
3. publish entity statements, trust marks, contacts, and policy metadata.
4. coordinate rollover, incident containment, and decommissioning.

### Support, sales, and account teams

1. Confirm supported federation profiles without making unverified conformance claims.
2. demonstrate connection health and configuration readiness with redacted evidence.
3. explain which party owns metadata, domains, keys, routing, and incident actions.

## 4. Architectural Boundary

### Runtime trust plane owns

- retrieving and validating discovery metadata and entity statements;
- resolving trust chains against tenant-approved anchors;
- applying federation metadata policy in deterministic order;
- returning derived, normalized, provenance-linked metadata;
- selecting only enabled and eligible connections;
- initiating upstream protocol flow through the owning OAuth/OIDC/RP runtime;
- validating callback issuer, audience, state, nonce, code binding, and keys;
- normalizing approved claims and creating a federated-session result;
- cache lifetime, refresh, last-known-good behavior, and fail-closed rules.

### Management plane owns

- provider, entity, anchor, intermediate, edge, trust-mark, routing, and mapping configuration;
- draft, review, approval, rollout, rollback, suspension, and retirement lifecycle;
- metadata import, comparison, pinning, refresh policy, and test fixtures;
- trust-chain simulation, impact analysis, evidence, and incident controls;
- tenant-scoped access control and separation of duties.

### Existing packages retain ownership

- identity and federation contracts remain in `tigrbl-identity-contracts`;
- cryptographic implementation remains in JOSE/security provider packages;
- protocol flow remains in OAuth, OIDC, and RP packages;
- durable graph and identity records remain in storage;
- tenant issuer truth remains in the tenant trust-domain authority object;
- cross-cutting policy decisions remain in the authorization decision service;
- API composition and projection belong in the proposed API package;
- presentation, local interaction state, and accessible visualization belong in UIX.

The deprecated federation registry is evidence of prior intent, not an implementation owner. New behavior must use current contracts and package boundaries.

## 5. Product Scope and Profiles

### Initial profiles

- bilateral upstream OIDC identity-provider connections;
- outbound OIDC relying-party and authorization-server trust registration;
- manual metadata plus OIDC Discovery and RFC 8414 metadata ingestion;
- tenant-specific connection assignment and home-realm discovery;
- claim normalization and subject-linking preview;
- key rotation monitoring and logout capability declaration;
- trust graph and direct-trust controls.

### OpenID Federation profile

- `/.well-known/openid-federation` entity configuration;
- signed entity-statement publication and retrieval;
- authority hints, subordinate statements, trust anchors, and intermediates;
- trust-chain construction, validation, selection, and expiry;
- federation metadata policy application and resolved metadata;
- trust marks and status where enabled;
- explicit and automatic registration only after profile-specific threat modeling;
- entity types for federation entity, OP, RP, authorization server, OAuth client, and protected resource.

### Later interoperable profiles

- SAML 2.0 IdP/SP metadata and assertion flows through a separately owned protocol provider;
- WS-Federation only if a validated customer segment justifies legacy enterprise support;
- education/research federation bundles and national trust frameworks;
- government and regulated-industry trust marks;
- cross-cloud workload federation, expanded by the Workload Trust pairing;
- security-event linkage to the future Security Signals pairing.

SAML support must not be represented by mapping SAML fields onto OIDC contracts. It needs protocol-native contracts, signing/encryption controls, metadata validation, binding selection, assertion replay defense, and conformance tests.

## 6. API Requirements

Use tenant-scoped, resource-oriented JSON management routes and standards-defined public endpoints. Exact Tigrbl operations and schemas should be derived from live package APIs during implementation.

### Connection lifecycle

| Method | Proposed route | Purpose |
|---|---|---|
| `GET` | `/admin/federation/connections` | List connections with profile, state, health, and assignment summary. |
| `POST` | `/admin/federation/connections` | Create a draft connection without activating it. |
| `GET` | `/admin/federation/connections/{connection_id}` | Return configuration, version, health, and safe provenance. |
| `PATCH` | `/admin/federation/connections/{connection_id}` | Update a draft or create a new mutable version. |
| `POST` | `/admin/federation/connections/{connection_id}:validate` | Validate syntax, metadata, keys, endpoints, mappings, and policy. |
| `POST` | `/admin/federation/connections/{connection_id}:test` | Run a bounded test and return a redacted report. |
| `POST` | `/admin/federation/connections/{connection_id}:submit` | Submit a version for approval. |
| `POST` | `/admin/federation/connections/{connection_id}:activate` | Activate an approved version with rollout controls. |
| `POST` | `/admin/federation/connections/{connection_id}:suspend` | Stop new use while preserving evidence and recovery. |
| `POST` | `/admin/federation/connections/{connection_id}:retire` | Retire a connection after impact and session review. |

### Metadata and keys

| Method | Proposed route | Purpose |
|---|---|---|
| `POST` | `/admin/federation/metadata:inspect` | Fetch or accept metadata and return parsed, untrusted findings. |
| `GET` | `/admin/federation/connections/{connection_id}/metadata` | Return effective and source metadata with provenance. |
| `POST` | `/admin/federation/connections/{connection_id}/metadata:refresh` | Refresh under SSRF-safe fetch policy. |
| `GET` | `/admin/federation/connections/{connection_id}/metadata:diff` | Compare candidate, active, and last-known-good metadata. |
| `GET` | `/admin/federation/connections/{connection_id}/keys` | Show public key identifiers, algorithms, status, and observed dates. |
| `POST` | `/admin/federation/connections/{connection_id}/keys:acknowledge` | Approve a policy-requiring key or algorithm change. |

### Trust graph and OpenID Federation

| Method | Proposed route | Purpose |
|---|---|---|
| `GET` | `/.well-known/openid-federation` | Publish the current entity configuration when enabled. |
| `GET` | `/federation/fetch` | Return an authorized subordinate statement per the standard profile. |
| `GET` | `/federation/list` | List subordinate entities only where policy permits. |
| `GET` | `/federation/resolve` | Resolve a trust chain only where a trusted resolver role is enabled. |
| `GET/POST` | `/federation/registration` | Support explicit registration after profile hardening. |
| `GET` | `/admin/federation/entities` | List entities, roles, anchors, marks, state, and health. |
| `POST` | `/admin/federation/trust-anchors` | Add a draft anchor through an out-of-band verification workflow. |
| `POST` | `/admin/federation/trust-paths:resolve` | Build and validate candidate paths with bounded depth. |
| `POST` | `/admin/federation/trust-paths:simulate` | Apply candidate metadata policy without runtime activation. |
| `POST` | `/admin/federation/edges/{edge_id}:revoke` | Revoke a relationship and calculate blast radius. |

### Routing, mapping, and operations

- CRUD/version operations for routing rules and tenant/application assignments;
- deterministic route simulation for a synthetic identifier and context;
- mapping preview from source claims to normalized claims;
- collision analysis for subject aliases and account linking;
- connection health, incidents, validation runs, and audit timeline;
- export/import of redacted configuration bundles with signed manifests;
- impact query showing applications, tenants, sessions, and trust paths affected by a change.

### API invariants

- Every mutable object has tenant, version, lifecycle state, creator, timestamps, and immutable audit linkage.
- Reads are tenant-filtered before object lookup; cross-tenant identifiers do not disclose existence.
- Activation uses optimistic concurrency and idempotency keys.
- Remote content is always classified as untrusted until fully validated.
- Runtime responses expose stable reason codes; internal exceptions, secrets, and full topology do not cross public boundaries.
- Published metadata is derived from the same authority/configuration object used by runtime verification.

## 7. Canonical Data Model

### Federation connection

- stable connection ID, tenant ID, display name, protocol/profile, direction, and lifecycle state;
- issuer/entity identifier and metadata source mode;
- discovery/metadata URL, expected audience, scopes, response modes, and logout capability;
- client authentication method and secret reference, never secret value;
- mapping version, routing assignments, trust-policy reference, and active version;
- health, last successful validation, last metadata refresh, and last-known-good digest.

### Federation entity and statement

- entity ID, entity types/roles, authority hints, endpoints, contacts, and organization metadata;
- compact signed statement stored under sensitive evidence controls;
- parsed header/claims, issuer, subject, issued/expiry times, key ID, algorithm, digest, source, and validation status;
- metadata by entity type, applied metadata policy, derived metadata, trust marks, and warnings.

### Trust anchor, domain, node, and edge

- anchor identity and pinned key material/digest established out of band;
- trust domain name, permitted issuers/clouds, jurisdiction/profile tags, and owner;
- directed source/target edge, exchange kind, constraints, validity window, status, and revocation evidence;
- maximum chain depth, allowed algorithms, required trust marks, permitted entity types, and metadata constraints.

### Claim mapping and subject link

- source claim selector, normalized target, transformation, required flag, validation, and privacy classification;
- pairwise/persistent subject policy, alias namespace, collision behavior, link approval mode, and unlink consequences;
- sample source and normalized result must be ephemeral or explicitly retained under evidence policy.

### Validation and rollout record

- configuration version/digest, environment, profile, tests, findings, timestamps, and actor;
- candidate/active/last-known-good comparison;
- approval, rollout percentage or assignment scope, observation window, rollback pointer, and outcome.

## 8. Trust and Evaluation Semantics

The implementation must define deterministic, testable semantics:

1. resolve tenant and requested federation profile;
2. identify eligible, enabled connection or entity without trusting user-supplied issuer labels;
3. retrieve content through a hardened fetcher with strict scheme, DNS/IP, redirect, size, time, and content limits;
4. validate statement type, syntax, issuer/subject relationships, time bounds, algorithms, key ID, and signatures;
5. build only acyclic, bounded candidate paths to locally configured trust anchors;
6. validate each path independently and reject ambiguous or policy-ineligible paths;
7. apply metadata policy in specified order and record every transformation;
8. validate resulting endpoints, key material, entity type, trust marks, and profile constraints;
9. select a path using explicit tenant policy, never incidental discovery order;
10. cache the validated result no longer than its shortest applicable expiry;
11. return derived metadata plus safe provenance and stable reason codes;
12. fail closed when no valid path exists, unless a narrowly defined last-known-good policy is active.

Direct bilateral trust and multilateral federation are separate trust modes. Enabling one must not silently enable the other. A graph path indicates configured reachability, not proof by itself; cryptographic and policy validation remain mandatory.

## 9. Trust Center UIX

### Overview

- federation readiness, active/draft/suspended connections, expiring statements/keys, failing checks, and recent changes;
- trust-path health and affected tenant/application counts;
- prioritized actions such as metadata drift, key rollover, invalid signatures, expiring anchors, and broken logout;
- protocol/profile badges that distinguish implemented, preview, and planned support.

### Connection wizard

1. choose direction and protocol/profile;
2. enter issuer/entity identifier or metadata source;
3. inspect untrusted fetched metadata before adoption;
4. configure secret references and authentication method;
5. map and classify claims;
6. set subject-linking and routing policy;
7. run configuration and interactive tests;
8. review security findings and affected surfaces;
9. submit, approve, and schedule activation.

The wizard must support save-and-resume, immutable version comparison, and a safe manual path when discovery is unavailable. A successful network fetch must never be presented as successful trust validation.

### Trust graph explorer

- accessible graph plus equivalent table/tree representation;
- nodes for anchors, intermediates, leaf entities, providers, RPs, authorization servers, resources, and trust domains;
- directed edges with exchange kind, constraints, state, validity, and provenance;
- path selection showing statement-by-statement signature and policy results;
- filters for tenant, profile, role, anchor, jurisdiction, status, mark, algorithm, and expiry;
- blast-radius mode for anchor, edge, key, metadata, or policy changes;
- no graph-only critical interaction; keyboard and screen-reader users receive full parity.

### Metadata and chain inspector

- source, fetched, parsed, effective, and last-known-good views;
- semantic diff rather than raw JSON-only comparison;
- signed statement header/claims, signature result, key source, time validity, and digest;
- metadata-policy transformation sequence with before/after values;
- exact failing hop and remediation guidance;
- raw payload access restricted, redacted, and audited.

### Mapping and routing lab

- side-by-side source and normalized claims with sensitive values masked by default;
- transformation validation, required-claim checks, and subject-collision warnings;
- home-realm routing builder with explicit priority and fallback;
- synthetic simulations for tenant, application, domain, and connection context;
- explanation of selected connection and rejected alternatives.

### Operations and incident mode

- health timeline for discovery, statements, keys, callbacks, and logout;
- refresh/revalidate controls with status and correlation IDs;
- suspend, quarantine, revoke edge, rollback, and restore-last-known-good actions;
- forced impact review and typed confirmation for destructive containment;
- incident bundle export containing redacted configuration, evidence digests, reason codes, and timestamps.

## 10. Security, Privacy, and Reliability

- Harden all remote metadata retrieval against SSRF, DNS rebinding, redirect abuse, oversized content, decompression bombs, slow responses, and unsafe schemes.
- Pin tenant-approved trust anchors out of band; discovery cannot create its own root of trust.
- Enforce explicit algorithm allowlists and reject `none`, confusion-prone JWT types, missing required `typ`, unknown critical headers, and unsafe key use.
- Separate signing keys, TLS server identity, client credentials, and anchor keys conceptually and operationally.
- Protect client secrets with write-only secret references, rotation, least privilege, and no UI echo.
- Prevent issuer mix-up, audience confusion, callback substitution, open redirects, login CSRF, nonce replay, assertion replay, and account-link takeover.
- Require explicit, reviewed mapping for privileged or identity-binding claims; do not infer authorization roles from arbitrary upstream claims.
- Treat email as an attribute, not globally unique proof of account ownership.
- Record metadata and graph provenance without retaining unnecessary personal claims.
- Define fail-closed behavior, bounded last-known-good use, cache expiry, refresh jitter, circuit breaking, and recovery objectives.
- Make suspension fast and reversible; make anchor/key deletion rare, reviewed, and delayed.
- Audit reads of raw statements, mappings with sample claims, secret metadata, and incident exports.

## 11. Stakeholder Requirements

### Technical marketing

- demo a partner connection from metadata import through validated login and claim normalization;
- visualize bilateral versus multilateral trust and show why signed chains reduce manual pairwise setup;
- use only evidence-backed standards labels: OpenID Federation support must be marked planned, preview, or conformant according to tested status;
- prepare narratives for B2B SSO, SaaS enterprise connection, research/education networks, regulated ecosystems, cross-cloud trust, and public-sector federation.

### Developer relations

- publish quickstarts for upstream OIDC, tenant routing, entity-statement publication, chain validation, key rollover, and failure handling;
- provide local fixtures for healthy, expired, invalid-signature, rotated-key, ambiguous-chain, and metadata-drift cases;
- document stable reason codes, webhook/event integration, SDK types, and test-environment limitations;
- provide recipes for common IdPs without implying vendor certification unless tested.

### Sales and account management

- receive a discovery worksheet covering protocol, direction, issuer/entity IDs, domains, claims, subject policy, logout, keys, routing, SLA, and compliance;
- use a support matrix that distinguishes configuration support, protocol support, and certified interoperability;
- produce a tenant-scoped readiness report and ownership/RACI summary;
- estimate migration and rollout risk from provider count, metadata quality, claim inconsistency, and account-linking rules.

### GTM strategist

- package the surface as Enterprise Connections, Federation Network, and Trust Operations tiers;
- prioritize B2B SaaS enterprise SSO first, then multilateral regulated/research networks and cross-cloud trust;
- meter on active connections, federation entities, tenants, validation volume, or premium governance features, not end-user login failure volume;
- treat SAML, OpenID Federation, trust marks, and managed partner onboarding as distinct value modules.

### Copywriter

- distinguish connection, provider, issuer, entity, trust anchor, trust path, and trust domain;
- use "validated" only for completed cryptographic and policy checks, not successful retrieval;
- say "suspend new sign-ins" rather than ambiguous "disable" when sessions remain active;
- make blast radius, reversibility, session effect, and recovery steps explicit in confirmations;
- never describe federation as automatically trusting any discovered provider.

## 12. Delivery Instructions

### Frontend engineer

- generate typed clients from canonical API schemas and preserve version/ETag/idempotency behavior;
- isolate secret-entry components and prevent values from entering logs, analytics, URLs, local storage, or error telemetry;
- render graph, table, and statement views from the same normalized model;
- use server-returned validation/reason codes rather than reimplementing trust decisions;
- support long-running validation with resumable status, cancellation, correlation IDs, and stale-state detection;
- add route-level authorization, tenant context, unsaved-change protection, and safe deep links;
- instrument wizard completion, validation failure category, time to activation, rollback, and recovery without collecting claim values.

### UIX designer

- make trust state, lifecycle state, health, and conformance status visually distinct;
- design progressive disclosure from executive health to statement-level cryptographic detail;
- provide semantic diffs and path narratives alongside raw technical views;
- design empty, loading, partial, stale, unreachable, invalid, ambiguous, expired, suspended, and rollback states;
- require review summaries for changes to anchors, algorithms, subject linking, routing, claim mappings, and active metadata;
- ensure WCAG 2.2 AA behavior, keyboard graph navigation alternatives, focus management, contrast, reduced motion, and non-color status cues.

### Copywriter

- create terminology, status, reason-code, remediation, confirmation, and notification catalogs;
- write separate language for tenant admins, security operators, developers, and partner operators;
- label remote content as "untrusted" until validated;
- provide concise explanations for each chain hop, policy transformation, rejected path, and metadata change;
- include safe recovery copy for key rollover, provider outage, issuer change, broken routing, and emergency suspension.

## 13. Delivery Phases

### Phase 1: Bilateral OIDC connections

- canonical provider/connection lifecycle and durable versions;
- metadata import, validation, diff, key monitoring, claim mapping, routing, and test flow;
- tenant assignment, activation, suspension, rollback, health, and audit;
- migration path from deprecated federation-registry concepts.

### Phase 2: Trust operations

- durable graph management and constrained path evaluation;
- anchor governance, blast-radius analysis, incident mode, and last-known-good policy;
- subject-linking safeguards, richer routing, logout validation, and partner evidence bundles.

### Phase 3: OpenID Federation 1.0

- complete entity configuration, fetch/list/resolve, subordinate statement, metadata policy, trust mark, and registration profiles;
- cryptographic chain validation and interoperability fixtures;
- conformance evidence before public "OpenID Federation 1.0 support" claims.

### Phase 4: Additional protocols and networks

- protocol-native SAML package and management adapter if prioritized;
- education, government, healthcare, finance, telecom, and supply-chain trust-framework profiles;
- integration with Security Signals and Workload Trust surfaces.

## 14. Acceptance Criteria

### API

- A tenant admin can draft, validate, test, approve, activate, suspend, roll back, and retire an OIDC connection without direct database/config edits.
- Metadata refresh detects semantic changes and cannot silently activate a policy-sensitive change.
- Issuer, audience, callback, algorithm, key, state, nonce, and tenant checks fail closed with stable reason codes.
- Trust path resolution is deterministic, bounded, cycle-safe, tenant-scoped, provenance-linked, and independently signature validated.
- Anchor and edge changes provide impact analysis and require appropriate approval.
- Secrets and personal claim samples are absent from standard reads, logs, telemetry, and exports.

### UIX

- A first-time admin can configure and test a typical OIDC connection using documented inputs.
- The UI clearly distinguishes fetched, parsed, validated, approved, active, degraded, suspended, and retired states.
- Operators can locate a failing chain hop or metadata field and identify the recommended recovery action.
- Every graph task has an accessible non-graph equivalent.
- Destructive or high-blast-radius operations disclose effect on new logins, existing sessions, tenants, applications, and recovery.

### Business and evidence

- Technical marketing can run a repeatable redacted demo with proof of validation and rollback.
- Sales can produce an accurate readiness report without privileged raw data.
- DevRel has tested quickstarts and negative fixtures.
- Standards and interoperability claims map to versioned tests/evidence, not package names or roadmap intent.

## 15. Success Measures

- median time from metadata receipt to first validated test;
- connection activation success rate and rollback rate;
- percentage of metadata/key changes detected before runtime failure;
- mean time to diagnose and contain a federation incident;
- authentication failures by safe reason-code category;
- stale, expiring, ambiguous, or excessive trust paths;
- percentage of connections using reviewed mappings, bounded routing, and last-known-good policy;
- support cases per active connection and partner onboarding cycle time.

Guardrails include account-link collisions, cross-tenant disclosure, unreviewed trust expansion, expired-chain use, secret exposure, false-positive health, and standards-claim accuracy.

## 16. Source Evidence

### Repository evidence

- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/federation/`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/oidc/federation.py`
- `pkgs/20-providers/tigrbl-security-oidc-federation-provider/`
- `pkgs/30-storage-runtime/tigrbl-identity-admin-trust-federation-graph/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/trust_federation_graph/`
- `pkgs/20-providers/tigrbl-identity-jose/`
- `pkgs/20-providers/tigrbl-security-token-jwks-cache/`
- `docs/compliance/tenant_trust_domain_authority_phase3.md`
- `docs/oidc-party-vendor-support-matrix.md`
- `docs/iam-ciam-pam-focus.md`
- issuer, discovery, JWKS rotation, runtime alignment, and trust-graph tests under `tests/`.

### External standards and primary sources

- [OpenID Federation 1.0 Final Specification](https://openid.net/specs/openid-federation-1_0.html)
- [OpenID Federation 1.0 final approval announcement](https://openid.net/openid-federation-1-0-final-specification-approved/)
- [OAuth 2.0 Authorization Server Metadata (RFC 8414)](https://www.rfc-editor.org/rfc/rfc8414)
- [OAuth 2.0 Dynamic Client Registration Protocol (RFC 7591)](https://www.rfc-editor.org/rfc/rfc7591)
- [OpenID Connect Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html)
- [OpenID Connect Dynamic Client Registration 1.0](https://openid.net/specs/openid-connect-registration-1_0.html)
- [NIST SP 800-63C: Federation and Assertions](https://pages.nist.gov/800-63-4/sp800-63c.html)
- [OASIS SAML V2.0 Standard](https://docs.oasis-open.org/security/saml/v2.0/)

## 17. Explicit Non-Claims

This brief does not claim that the current repository:

- fully implements or conforms to OpenID Federation 1.0;
- provides production SAML federation;
- safely supports dynamic or automatic registration;
- has a complete persistent upstream federation lifecycle;
- has certified interoperability with named vendors or national trust frameworks;
- can infer account identity or authorization safely from email or arbitrary upstream claims.

Those statements require implemented runtime behavior, negative tests, interoperability evidence, operational hardening, and release certification.
