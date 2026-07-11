# Token Service API + Token Studio UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-token-service` + `@tigrbl-auth/token-studio-uix`  
**Status:** New governed product surface over substantial existing OAuth, JOSE, storage, exchange, validation, and revocation behavior  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-token-service`  
**Protocol owners:** OAuth/OIDC protocol packages and format-specific token providers  
**Proposed UIX owner:** `pkgs/95-ui/token-studio-uix`

## 1. Product Decision

Create a governed token service and broker surface for defining token profiles, issuing and exchanging tokens through approved protocols, enforcing audience/resource/scope/delegation/sender constraints, managing token and refresh-family lifecycle, validating/introspecting status, tracing lineage, and operating revocation or compromise response.

The product must preserve strict distinctions among:

- OAuth access tokens, refresh tokens, authorization codes, device codes, and ID tokens;
- JWT and opaque access-token formats;
- sender-constrained tokens using DPoP or mTLS;
- RFC 8693 subject and actor tokens used as exchange inputs;
- SPIFFE JWT-SVIDs, CWTs, EATs, Security Event Tokens, credentials, certificates, attestations, and non-bearer receipts;
- experimental capability/authorization token families such as Macaroons, Biscuits, or PASETO.

Token Studio is an administrative policy, simulation, and operations console. It does not display usable token values, mint arbitrary production tokens from a browser, or replace the standards-defined OAuth token endpoint.

## 2. Current Repository Reality

The repository already has meaningful token-service foundations:

- runtime composition for persisted access/refresh token pairs, refresh redemption, context exchange, token listing, introspection, and revocation;
- durable `TokenRecord` containing token hash, JTI, kind/type, status, refresh family and predecessor/successor hashes, subject, tenant/client, scopes, issuer, key/version, audience, claims, issue/expiry/use/introspection/reuse/revocation state;
- refresh-token rotation and family revocation behavior with reuse detection;
- OAuth token endpoint grants including authorization code, client credentials, device flow, assertions, and related tests;
- RFC 8693 token-exchange runtime with subject/actor tokens, delegation/impersonation distinction, resource/audience selection, DPoP/mTLS sender constraint, authorization trace, delegation provenance, and persistence;
- RFC 7662 introspection and RFC 7009 revocation implementations/tests;
- RFC 9449 DPoP and RFC 8705 mTLS confirmation-binding providers;
- JOSE/JWT signing, verification, encryption, key rotation, JWKS, issuer, algorithm, and token revocation foundations;
- resource-server verification contracts and introspection clients;
- token, audit, delegation, session, client, service, resource, policy, and provenance records.

The product is still fragmented. Gaps include:

- canonical versioned token profiles and claims policy;
- one inventory and lifecycle model spanning issuance, lineage, exchange, refresh, sender constraints, status, and consumers;
- safe management API and Token Studio;
- opaque/JWT profile choice and RFC 9068 conformance evidence;
- subject/actor token-type registry and strict exchange authorization;
- token format/provider extensibility without token confusion;
- key/profile compatibility, staged rollout, simulation, impact, and rollback;
- privacy-minimized token records and operations analytics.

### Current exchange constraints

The release path publishes `/token/exchange`, whereas RFC 8693 defines token exchange as a grant using existing token-endpoint request/response constructs. It currently supports only access-token output and decodes input tokens through the local JWT coder. Before claiming a general security token service, implementation must decide standards-compatible route composition, enforce subject/actor token-type semantics, authorize every exchange, validate source issuers and audiences through explicit trust, and support only accurately advertised requested token types.

## 3. Users and Jobs

### Authorization-server/security administrator

1. define token formats, claims, lifetimes, keys, audiences/resources, scopes, grants, sender constraints, exchange rules, and refresh policy.
2. test profiles against clients and resource-server contracts.
3. stage, activate, roll back, retire, and rotate profiles/keys without invalid token confusion.
4. monitor issuance, validation, introspection, refresh, exchange, reuse, revocation, and denial posture.
5. contain a compromised client, key, refresh family, subject, issuer, or token lineage.

### API and application developer

1. know which grant, client authentication, token type, audience/resource, scope, and proof are required.
2. inspect a redacted synthetic/test token and validate expected claims.
3. exchange a token only across approved trust/resource boundaries.
4. integrate resource validation and handle expiry/revocation/retry correctly.
5. diagnose a denial without access to production token material.

### Service/workload owner

1. obtain short-lived audience-bound tokens using strong client/workload authentication.
2. use DPoP/mTLS sender constraints for high-assurance calls.
3. delegate or impersonate only under explicit policy and traceable lineage.
4. rotate credentials and revoke affected tokens rapidly.

### SOC, support, compliance, and privacy teams

1. investigate token lineage and status by hash/JTI/reference, never by broad raw token access.
2. distinguish issuance, possession, presentation, introspection, refresh, exchange, and revocation.
3. identify overbroad scopes/audiences, long lifetimes, replay/reuse, unusual exchange depth, and stale authorization.
4. preserve privacy-minimized evidence of token actions and response.

## 4. Architectural Ownership

### OAuth/OIDC protocol packages own

- authorization and token endpoint grant semantics;
- client authentication, authorization code/PKCE, refresh, device flow, assertions, resource indicators, token exchange, introspection, and revocation protocols;
- OAuth/OIDC error and metadata behavior;
- ID-token/user authentication semantics.

### Token format providers own

- JWT, opaque-reference, and later CWT encoding/validation;
- exact media/type headers, claims representation, signing/MAC/encryption, key selection, and algorithm policy;
- format-specific proof-of-possession confirmation methods;
- no assumption that all token-like objects are JWTs.

### Token Service API owns

- profile, route, client/resource assignment, claim mapping, lifecycle, simulation, lineage, query, response, metrics, and UI-facing schemas;
- orchestration across policy, JOSE, storage, OAuth, resource validation, credentials, delegation, and security signals;
- management authorization, audit, privacy, idempotency, and operational controls.

### Existing owners retain semantics

- Policy Studio owns access decisions and permission vocabulary;
- Developer/Service Admin own client/service credentials and grants;
- Resource Validation owns protected-resource token verification;
- Workload Trust owns SVIDs;
- Attestation owns EAT evidence/results;
- Security Signals owns SETs;
- storage owns token hashes/status/lineage and related durable data;
- UIX never signs, decodes as authority, or exposes bearer material.

## 5. Token Taxonomy and Naming

### OAuth artifacts

| Artifact | Intended use | UI/API guardrail |
|---|---|---|
| Access token | Authorize calls to a resource server. | Audience/resource, scope, expiry, status, and sender constraint are primary. |
| Refresh token | Obtain new access tokens under a continuing grant. | High-value credential; store hashed/opaque, rotate, detect reuse, bind to client/grant. |
| ID token | Assert authentication to an OIDC client. | Not an API access token; validate nonce/audience/issuer/auth context. |
| Authorization code | One-time authorization response artifact. | Short-lived, client/redirect/PKCE bound; never shown as reusable token. |
| Device/user code | Coordinate device authorization. | Different secrecy and polling semantics; not access tokens. |
| Subject token | RFC 8693 input representing subject. | Type, issuer, audience, validity, trust, and exchange authorization required. |
| Actor token | RFC 8693 input representing acting party. | Preserve `act`/delegation semantics and lineage. |

### Token types versus formats

`access_token` is a semantic token type. JWT, opaque reference, and CWT are representations. `Bearer` and `DPoP` describe presentation/proof behavior. The object model and copy must not use these terms interchangeably.

### Non-OAuth token-like artifacts

- Security Event Tokens communicate events and are not authorization credentials.
- EATs carry attestation evidence/results and are not generic access tokens.
- JWT-SVIDs authenticate workloads and follow SPIFFE rules.
- Signed decision receipts prove a decision/evidence record and are non-bearer.
- API/service keys are credentials, not tokens merely because they are strings.

## 6. Token Profile Requirements

Every issued token is governed by an immutable profile version defining:

- semantic type, format, protocol/grants, issuer, subject/client mapping, and intended consumers;
- allowed audiences/resources and one-versus-many target policy;
- scope/roles/entitlements/authorization-details claim source and disclosure;
- required/optional/forbidden claims and mapping/type/cardinality;
- token lifetime, not-before/skew, maximum authorization staleness, and refresh behavior;
- signing/MAC/encryption algorithms, key class/use/version, `typ`/content type, and key publication;
- bearer, DPoP, mTLS, or other explicit confirmation binding;
- opaque persistence/introspection or JWT local-validation posture;
- revocation, reuse, exchange, delegation, privacy, audit, and incident policy;
- owning tenant/environment and rollout/compatibility version.

Profiles must be immutable after activation. Changes create a new version and include compatibility/consumer impact, key publication/overlap, staged assignment, and rollback.

## 7. JWT and Opaque Access Token Requirements

### JWT access tokens

Adopt an explicit RFC 9068 profile where claimed:

- signed tokens with `typ` of `at+jwt` and no `none` algorithm;
- required issuer, subject, audience, expiry, issued-at, JTI, and client ID claims as applicable;
- resource/audience alignment and exact issuer/algorithm/key validation;
- scoped authentication/identity/authorization claims with privacy review;
- asymmetric signing recommended for distributed resource-server verification;
- dedicated access-token validation preventing ID token, SET, EAT, assertion, or arbitrary JWT confusion;
- key/version lineage and JWKS publication/retirement coordinated with token lifetime.

### Opaque access tokens

- cryptographically random, unguessable values with only digests stored;
- authoritative status/claims through RFC 7662 introspection;
- tenant/client/resource binding, expiry, revocation, and last-introspection/usage evidence;
- introspection response minimized to the authenticated resource server's needs;
- caching bounded by token expiry, status freshness policy, and security signals.

### Format selection

- JWT for efficient first-party/offline validation where short staleness is acceptable;
- opaque for centralized control, minimal external disclosure, or immediate status checks;
- hybrid deployments require explicit profile/consumer discovery and cannot guess by token shape;
- encryption is not a substitute for audience restriction or minimized claims.

## 8. Proof-of-Possession and Sender Constraints

### DPoP

- validate proof JWT type/header/key, signature, HTTP method/URI, issue time, JTI replay, nonce where required, and access-token hash;
- bind issued token using `cnf.jkt` and return correct token type;
- maintain replay/nonce stores per issuer/client/resource policy;
- prevent proof key substitution across authorization and token/presentation steps;
- show only public thumbprint/posture in UIX.

### mTLS

- authenticate client certificate and validate full chain/profile before thumbprint binding;
- bind token using `cnf.x5t#S256` under RFC 8705 semantics;
- distinguish PKI method from self-signed certificate method where supported;
- track certificate/credential rotation and overlap across still-active tokens;
- use Certificate Center for certificate validation/lifecycle.

### Policy

- high-assurance profiles may require sender constraint;
- bearer-to-bound or bound-to-bearer exchange is forbidden unless an explicit risk-reviewed rule permits it;
- exchanged tokens should preserve or strengthen proof binding, never silently downgrade it;
- proof possession does not replace client/subject authorization.

## 9. Token Exchange and Delegation

### Exchange authorization pipeline

1. authenticate the requesting client and resolve tenant/issuer/profile;
2. validate grant type and exact subject/actor/requested token-type URIs;
3. validate subject and actor token using the provider/trust policy for their declared types;
4. validate source issuer, audience, purpose, status, sender constraint, and exchange eligibility;
5. resolve subject and actor without cross-tenant or identifier fallback;
6. evaluate impersonation versus delegation and the actor/subject relationship;
7. authorize target resource/audience, scopes, requested type, lifetime, and proof binding;
8. enforce monotonic attenuation unless a specifically authorized privilege transformation exists;
9. issue a new token with `act`/lineage and minimal claims;
10. persist only hash/status/provenance and audit the decision/result.

### Exchange constraints

- one effective target by default; multiple resources require an explicit profile;
- output lifetime cannot exceed source authorization/credential/policy limits;
- output scopes/permissions cannot exceed the allowed intersection of source authority, actor/delegation grant, client grant, and target policy;
- cap exchange depth and detect cycles/repeated lineage;
- validate each source token according to its native type rather than decoding every input as local JWT;
- never accept arbitrary external tokens because their signature is valid;
- revocation/compromise of source token, actor, delegation grant, credential, or trust edge must identify descendants.

### Route composition

Prefer RFC 8693 grant handling at the canonical token endpoint. A compatibility `/token/exchange` route may remain only if metadata/docs clearly describe it and behavior is identical, tested, and not the sole standards claim.

## 10. Refresh Token and Session Continuity

- Store refresh tokens only as strong digests/reference state; raw values are returned once to the client.
- Bind family to tenant, client, subject/grant/session, authorized resources/scopes, credential/proof posture, and profile.
- Rotate on every successful redemption where configured; mark parent consumed and link successor atomically.
- Reuse of a consumed token revokes the family and emits audit/security signal according to policy.
- Use idempotency/concurrency control to distinguish legitimate retry from malicious replay where possible.
- Re-evaluate client status, credential, grant, session, subject, authorization freshness, and proof before issuance.
- Enforce absolute and inactivity lifetimes; rotation must not extend beyond allowed grant/session horizon.
- Public clients receive stronger rotation/binding rules and no client-secret assumptions.
- Revocation can target one token, family, session, client, subject, tenant, key, grant, or lineage with impact preview.

## 11. Introspection, Validation, and Revocation

### Introspection

- authenticate/authorize callers and restrict each resource server to relevant tokens/claims;
- return `active=false` without existence details for unknown, expired, revoked, wrong-audience, wrong-tenant, or unauthorized tokens;
- only return claims required for validation/authorization;
- update operational metrics without creating write amplification that threatens availability;
- define cache and maximum authorization-status staleness.

### Local validation

- exact issuer, `typ`, algorithm, key use/version, signature, time, audience/resource, subject/client, scopes, status/freshness, and proof checks;
- deterministic policy reason codes and no untrusted `kid` network fetch;
- stale JWKS/key handling, rotation overlap, and fail-closed behavior;
- optional introspection fallback only under explicit profile and circuit-breaker policy.

### Revocation

- RFC 7009 endpoint behavior must avoid token-existence disclosure and be idempotent;
- revocation record includes actor/client, tenant, target hash/reference, scope, reason, time, descendants, and outcome;
- JWT revocation needs short lifetime, revocation store/security signals, or resource-server freshness strategy;
- bulk/emergency revocation must be bounded, approved, observable, and reversible only by new issuance, not reactivation of compromised tokens.

## 12. Management API Requirements

Use `/admin/token-service` for management. Standards endpoints remain on public/protocol surfaces.

### Profiles and assignments

- CRUD/version lifecycle for token profiles, claim schemas/mappings, issuer/key policy, proof policy, refresh policy, and exchange policy;
- assignment to tenant, environment, client/app/service, grant, resource server, and route;
- validate, lint, simulate, submit, approve, activate, stage, rollback, supersede, and retire actions;
- compatibility matrix between token profile and resource-server verifier contract.

### Token metadata and lineage

- tenant-safe search by opaque record ID, hash prefix where safe, JTI, subject/client/resource, kind/profile/status, family, session, delegation grant, exchange lineage, key/version, and time;
- no broad raw token search or display;
- detail returns safe claims metadata, status, lineage, bindings, decisions, evidence, and events;
- impact query for client/credential/key/profile/grant/policy/trust changes;
- revoke token/family/session/client/subject/lineage with preview and approval thresholds.

### Simulation and tooling

- build synthetic issuance/exchange/refresh requests from fixtures;
- show selected profile, normalized claims, audience/resources, scopes, proof, lifetime, signing key, persistence, and validation contract;
- before/after token semantic diff across profile versions;
- resource-server validation simulation with safe failure trace;
- never accept a production token into a general browser decoder; privileged incident ingestion must be separate, consented, memory-limited, and audited.

## 13. Novel Token and Token-Service Opportunities

### Near-term standards extension: CWT/ACE

CBOR Web Tokens (RFC 8392) and CWT proof-of-possession semantics (RFC 8747) can serve constrained IoT/edge environments. This requires:

- CBOR/COSE-native encoding, signing/MAC/encryption, content formats, claim-key mapping, and deterministic tests;
- ACE-OAuth profile selection, resource-server/client context, transport binding, and revocation/status behavior;
- no JWT-to-CWT byte translation shortcut;
- UI rendering through normalized semantic claims while preserving format/profile details.

This is the strongest novel standards-based token opportunity because it horizontally supports industrial, telecom, automotive, healthcare-device, building, and edge verticals.

### Capability and attenuable tokens

Macaroons and Biscuits offer delegation/attenuation models worth research for edge, agents, offline services, and delegated workflows. Before productization:

- define issuer/verifier trust, caveat/fact/rule semantics, revocation, discharge/third-party behavior, lineage, and policy integration;
- prove monotonic attenuation and bounded evaluation;
- prevent token amplification, confused deputy, ambient authority, and policy-language injection;
- choose one ecosystem based on interoperability/customer demand rather than exposing generic "custom token" plugins.

### PASETO and proprietary formats

PASETO may reduce some JWT algorithm-footgun classes but is not an OAuth interoperability default. Treat it as a profile-specific research option, not a replacement for standards-required JWT access tokens. Proprietary formats need a clear advantage, maintained specification, independent libraries, cryptographic review, and explicit consumer negotiation.

### Non-bearer receipts

Signed decision, delegation, issuance, validation, revocation, and audit receipts can provide tamper-evident proof without granting access. They should be modeled as receipts/evidence artifacts with audience/purpose and retention, not accepted in `Authorization: Bearer`.

## 14. Canonical Data Requirements

### Token profile/version

- profile/version ID, semantic type, format, issuer, tenant/environment, lifecycle, and compatibility;
- grants/client auth, subject/client mapping, resources/audiences, scopes/claims, lifetime, refresh, exchange, and proof policies;
- signing/MAC/encryption/key/JWKS policy and verifier contract;
- owner, approvals, rollout, predecessor, fixtures, and evidence.

### Token record

- token digest and optional JTI/CTI, kind/type/format/profile, issuer/key/version, issued/expiry/not-before, and status;
- tenant, subject, actor, client, session/grant, resources/audience, scopes, authorization decision/version, and confirmation binding;
- refresh family/parent/successor or exchange parent/descendant lineage;
- last use/introspection, reuse/replay, revocation, and privacy-safe claims digest/selected metadata;
- avoid storing the complete sensitive claims set by default when it is derivable or unnecessary.

### Exchange lineage edge

- child token, subject/actor source tokens, declared/validated types, source issuers, delegation/impersonation mode, client, target, attenuation diff, proof transition, decision/provenance, time, and status;
- hashes/references only, not raw source token values;
- acyclic bounded graph and descendant impact indexes.

### Validation/usage event

- token reference, tenant, resource/consumer, operation, outcome/reason, proof posture, policy/verifier version, time, and correlation;
- sampling/aggregation strategy for volume and privacy;
- raw request headers/tokens prohibited.

## 15. Token Studio UIX

### Overview

- issuance, refresh, exchange, introspection, validation, and revocation volume/outcomes;
- active/expired/revoked/reused families, sender-constrained coverage, profile/key posture, and resource compatibility;
- high-risk findings for long lifetimes, broad audiences/scopes, bearer high-value tokens, weak algorithms, stale authorization, deep exchange, reuse/replay, and unknown consumers;
- no headline "active tokens" metric without explaining observability limits for self-contained tokens.

### Profile studio

- guided builder for semantic type, format, grants, subjects, audiences/resources, scopes/claims, lifetime, proof, keys, refresh, exchange, introspection, and revocation;
- claims schema with source, type, cardinality, privacy, mutability, and disclosure;
- compatibility view against clients and resource servers;
- synthetic preview with header/claims shown using non-sensitive values;
- lint, threat findings, semantic diff, simulation, approval, staged rollout, rollback, and retirement.

### Token and lineage explorer

- table by safe token reference/hash prefix, type, profile, subject/client, resource, status, issue/expiry, proof, and lineage;
- detail with claim categories, not reusable token string;
- refresh family and exchange lineage as accessible tree/table plus optional graph;
- source authority, actor, delegation grant, attenuation, proof transitions, validation, and revocation timeline;
- blast-radius mode for credential/key/profile/grant/policy/source compromise.

### Simulation lab

- preset OAuth grant/exchange/refresh scenarios and synthetic actors/resources;
- output selection, claims provenance, policy decision, key, proof binding, persistence, and verifier outcome;
- negative simulations for wrong audience, scope, issuer, key, proof, stale auth, replay, reuse, revoked source, and excessive delegation;
- code/curl snippets use dedicated test issuer and clearly labeled non-production tokens.

### Incident operations

- locate by hash/JTI/reference/correlation without token paste where possible;
- revoke one, family, session, client, subject, lineage, key, or profile cohort with impact/approval;
- show propagation to introspection/resource validators/security signals and remaining self-contained-token risk window;
- verify containment and issue replacement only through normal authorized flows;
- redacted incident evidence bundle.

## 16. Security, Privacy, and Reliability

- Never log, index, export, analytics-capture, URL-encode, or display raw access/refresh/subject/actor tokens.
- Hash opaque tokens with domain separation and sufficient secret/pepper strategy where appropriate; do not use token hashes as public lookup oracles.
- Enforce JWT/JOSE type, algorithm, key use, issuer, audience, time, and confusion defenses.
- Treat refresh, subject, and actor tokens as credentials with stronger handling than ordinary metadata.
- Require TLS and hardened client authentication for token/introspection/revocation/exchange endpoints.
- Prevent scope/audience/resource escalation, actor substitution, tenant crossing, exchange cycles, proof downgrade, and refresh-family races.
- Use atomic persistence for issue/rotate/revoke/lineage/audit and transactional outbox for security events.
- Rate-limit by tenant/client/grant/credential/source/target and protect expensive crypto/introspection/exchange paths.
- Define clock, key/JWKS outage, database/cache outage, partial persistence, and regional failover behavior.
- Bound claim size/count, audience/resources/scopes, exchange depth, family size, token lifetime, and introspection response.
- Minimize identity/authorization claims to intended resource; pairwise subjects and opaque tokens can reduce correlation.
- Audit privileged metadata reads, simulations using historical fixtures, bulk revocation, and incident exports.

## 17. Stakeholder Requirements

### Technical marketing

- demonstrate audience-bound JWT/opaque profiles, DPoP/mTLS protection, refresh reuse containment, and attenuated token exchange using synthetic identities;
- explain token service versus credential vault, authorization engine, workload identity, attestation, and security signals;
- prepare use cases for API access, B2B delegation, microservices, multi-cloud brokering, agents, edge/IoT, and regulated data APIs;
- label novel token families as research/preview until interoperable and certified.

### Developer relations

- publish grant, JWT access token, opaque/introspection, DPoP, mTLS, refresh rotation, revocation, and RFC 8693 quickstarts;
- provide deterministic positive/negative fixtures and a safe local issuer/resource server;
- document profile discovery, claims, audiences/resources, scopes, keys/JWKS, proof, errors, retry, lifetime, and clock handling;
- provide CWT/ACE and attenuable-token research examples only under explicit experimental labels.

### Sales and account management

- use a discovery worksheet covering clients/subjects, grants, resources, scopes, formats, lifetimes, sender constraints, refresh, exchange, source issuers, keys, validation, revocation, scale, region, and compliance;
- provide a readiness report separating issuance, brokering, validation, lifecycle, operations, and novel profiles;
- define RACI for issuer, keys, client credentials, grants, resource servers, exchange trust, revocation, and incidents;
- avoid claims of universal token translation or immediate JWT revocation.

### GTM strategist

- package Token Profiles, High-Assurance Sender Constraints, Token Exchange/Broker, Lifecycle Operations, and Edge/IoT Tokens separately;
- pair with Policy Studio, Developer/Service Admin, Resource Validation, Workload Trust, and Security Signals;
- lead with governed OAuth access/refresh/exchange operations before novel formats;
- meter issuance/exchange/introspection volume, managed clients/resources, advanced profiles, or governance tier without discouraging revocation/validation.

### Copywriter

- distinguish semantic type, format, presentation type, credential, proof, claims, profile, issuer, audience/resource, scope, grant, refresh family, and lineage;
- never call ID tokens access tokens or decoded claims "verified" without signature/policy checks;
- say "revocation recorded" separately from "all resource servers have enforced revocation";
- make proof binding, attenuation, expiry, stale authorization, and privacy clear;
- never invite users to paste production tokens into ordinary UI fields.

## 18. Delivery Instructions

### Frontend engineer

- generate typed management/simulation clients; standards token endpoints are not browser admin APIs;
- enforce schemas that omit raw token values and add automated tests preventing tokens in analytics/logs/URLs/storage;
- render server-returned claims provenance, lineage, proof, decisions, status, and reason codes;
- support large inventories with safe pagination/aggregation, background revocation/impact jobs, partial failure, stale version, and approval state;
- make synthetic/test context unmistakable and prevent production issuer credentials in simulation;
- instrument profile rollout and token operation outcomes using opaque references and safe categories.

### UIX designer

- separate token type, representation, status, proof posture, and authorization state;
- design lifecycle/timeline rather than a raw decoder-first experience;
- cover empty, draft, issuing, active, expiring, expired, rotating, refreshed, reuse detected, exchanged, introspection unavailable, revoked, propagation pending, and contained states;
- provide accessible tree/table alternatives to lineage graphs;
- require preview/approval for key/profile rollout, proof downgrade, scope expansion, bulk revocation, and source trust changes;
- meet WCAG 2.2 AA with keyboard operation, non-color status, accessible diffs/charts/timelines, focus management, and reduced motion.

### Copywriter

- create token taxonomy, profile, grant, proof, validation, refresh, exchange, revocation, reason-code, confirmation, incident, and recovery catalogs;
- write separate developer, security operator, support, and auditor language;
- make raw-token non-display policy and safe lookup methods clear;
- explain propagation and self-contained-token limitations during incidents;
- calibrate standards, format, and interoperability claims to evidence.

## 19. Delivery Phases

### Phase 1: Canonical governed token profiles

- profile/version, claim schema, assignment, safe token record, validation event, and lineage contracts;
- RFC 9068 JWT profile and opaque/introspection profile;
- Token Studio profile/simulation/posture views;
- raw token exposure review across APIs, logs, storage, tests, and UIX.

### Phase 2: Lifecycle and sender constraints

- refresh-family operations/reuse UI, DPoP/mTLS posture, revocation impact/propagation, key/profile rollout, and resource compatibility;
- production-safe token explorer and incident workflow;
- security-signals integration.

### Phase 3: Token exchange broker

- RFC 8693 at canonical token endpoint, strict type/provider registry, external issuer trust, actor/delegation policy, attenuation, bounded lineage, descendant revocation, and interoperability fixtures;
- compatibility handling for `/token/exchange`.

### Phase 4: Novel profiles

- CWT/COSE and selected ACE-OAuth profile for constrained systems;
- controlled research/pilots for capability/attenuable tokens and signed non-bearer receipts;
- vertical packs for IoT, industrial, telecom, automotive, healthcare devices, agents, and offline/edge systems.

## 20. Acceptance Criteria

### API/runtime

- Every issued token maps to an active immutable profile, authorized grant/client/subject/resource, key version, decision, and safe record.
- JWT access tokens meet the claimed RFC 9068 profile and cannot be confused with ID/SET/EAT/assertion JWTs.
- Opaque tokens introspect with least-disclosure and no existence oracle.
- Refresh rotation is atomic and reuse revokes the intended family with evidence/security signal.
- Exchange validates native input types/trust, actor/subject semantics, attenuation, target, lifetime, proof, and lineage.
- Revocation impact can find families and exchange descendants without raw tokens.
- Raw token values never appear in management reads, UIX, logs, metrics, URLs, exports, or analytics.

### UIX

- An administrator can create, simulate, review, stage, activate, and roll back a token profile.
- Developers can understand expected token semantics using synthetic examples.
- Operators can trace safe token lineage and proof posture without bearer material.
- Incident response shows requested action, affected lineage, propagation, residual risk window, and verified outcome.
- Token taxonomy prevents semantic type/format/presentation confusion.

### Evidence/business

- DevRel can run deterministic positive/adversarial JWT, opaque, refresh, proof, exchange, introspection, and revocation fixtures.
- Technical marketing can demonstrate broker and reuse-containment scenarios with test-only tokens.
- Sales can provide readiness/RACI without production token access.
- RFC/profile/novel-format/interoperability claims link to versioned certified evidence.

## 21. Success Measures

- issuance/refresh/exchange/introspection/validation/revocation success by safe reason;
- token lifetime, scope, audience, bearer versus sender-constrained, and profile distribution;
- refresh reuse and DPoP replay detection/containment;
- exchange depth, attenuation violations prevented, and descendant impact coverage;
- profile/resource compatibility and rollout failure rate;
- revocation request-to-enforcement/verification latency;
- stale authorization/JWKS/introspection incidents;
- raw-token leakage incidents and sensitive claim reduction;
- developer integration and incident resolution time.

Guardrails include token confusion, privilege escalation, cross-tenant exchange, proof downgrade, refresh race/reuse acceptance, revocation gaps, key rollover outage, privacy over-disclosure, and overstated translation/interoperability.

## 22. Source Evidence

### Repository

- `pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/token_service.py`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/token_record/`
- `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/token_exchange.py`
- `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/introspection.py`
- `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/revocation.py`
- `pkgs/50-protocols/tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/standards/`
- `pkgs/20-providers/tigrbl-security-proof-dpop/`
- `pkgs/20-providers/tigrbl-security-dpop-cnf-binding-validator/`
- `pkgs/20-providers/tigrbl-security-mtls-cnf-binding-validator/`
- `pkgs/20-providers/tigrbl-security-token-introspection-client/`
- JOSE, credentials, resource validation, delegation, authorization provenance, audit, and key-rotation packages;
- RFC 7009/7662/8693/8705/9449 and refresh/token persistence tests.

### Standards and primary sources

- [RFC 9068: JWT Profile for OAuth 2.0 Access Tokens](https://www.rfc-editor.org/rfc/rfc9068)
- [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707)
- [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 8705: OAuth 2.0 Mutual-TLS and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7662: OAuth 2.0 Token Introspection](https://www.rfc-editor.org/rfc/rfc7662)
- [RFC 7009: OAuth 2.0 Token Revocation](https://www.rfc-editor.org/rfc/rfc7009)
- [RFC 8392: CBOR Web Token](https://www.rfc-editor.org/rfc/rfc8392)
- [RFC 8747: Proof-of-Possession Key Semantics for CWTs](https://www.rfc-editor.org/rfc/rfc8747)
- [RFC 9200: Authentication and Authorization for Constrained Environments](https://www.rfc-editor.org/rfc/rfc9200)

## 23. Explicit Non-Claims

This brief does not claim that the current repository:

- exposes a unified governed token-service product or Token Studio;
- fully conforms to RFC 9068 JWT access-token profile;
- implements general RFC 8693 input/output token-type translation or external security token brokering;
- supports opaque and JWT access-token profiles through one certified policy surface;
- implements CWT/COSE, ACE-OAuth, Macaroons, Biscuits, or PASETO;
- provides immediate universal revocation of self-contained JWTs;
- safely exposes production token values for debugging;
- can treat SVIDs, EATs, SETs, ID tokens, credentials, or receipts as interchangeable access tokens.

Those claims require profile contracts, strict type/format validation, policy and lineage enforcement, privacy-safe operations, adversarial/interoperability tests, resource-server evidence, incident exercises, and release certification.
