# Workload Trust and SPIFFE API + Workload Trust Center UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-workload-trust` + `@tigrbl-auth/workload-trust-center-uix`  
**Status:** New product surface; workload/machine records, credentials, trust domains, graphs, token exchange, mTLS, and governance foundations exist  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-workload-trust`  
**Proposed protocol/provider owner:** `pkgs/50-protocols/tigrbl-workload-spiffe` and SPIFFE-compatible providers  
**Proposed UIX owner:** `pkgs/95-ui/workload-trust-center-uix`

## 1. Product Decision

Create a dedicated workload identity and trust product surface for discovering runtime workloads, attesting their execution context, assigning stable workload identities, issuing short-lived credentials, distributing trust bundles, governing cross-domain trust, and proving workload-to-workload authentication.

The product must separate:

- **Workload identity control plane:** trust domains, selectors, registration entries, ownership, policy, federation, posture, lifecycle, and evidence.
- **Local workload plane:** a SPIFFE-compatible Workload API or adapter used by a local workload to obtain and rotate authorized X.509-SVIDs, JWT-SVIDs, and bundles.
- **Trust validation plane:** peer SVID, bundle, audience, issuer/trust-domain, revocation/expiry, and policy validation.
- **Operations experience:** inventory, attestation health, registration policy, SVID/bundle posture, federation, access impact, incident response, and migration.

SPIFFE is a standards family; SPIRE is one implementation. Tigrbl should initially interoperate with or govern a SPIFFE/SPIRE deployment rather than claim to replace a production SPIRE server/agent. A native implementation is a later decision requiring a substantially larger attestation, CA, streaming API, plugin, and operations scope.

## 2. Current Repository Reality

The repository already contains:

- durable `WorkloadIdentity` with principal, workload subject, tenant/realm, trust domain, namespace, service account, cloud identity, image digest, status, and metadata;
- durable `MachineIdentity` with principal, machine subject, tenant/realm, hardware ID, attestation type, trust anchor, status, and metadata;
- service, client, service-key, API-key, mTLS-certificate, token, revocation, audit, and key records;
- workload, service, machine, client, and tenant principal concepts;
- tenant and realm trust-domain authority objects for issuer, JWKS, subject namespace, protected resource, accepted issuers, and verification scope;
- trust-domain/edge/path graph behavior and cross-cloud workload mapping;
- OAuth client credentials, RFC 8693 token exchange, JWT assertion, mTLS, DPoP, and resource validation;
- mTLS confirmation-claim validation for `x5t#S256`;
- machine-identity governance tests requiring non-human type, owner, rotating credential, tenant, and allowed audience;
- key attestation evidence and release attestation records;
- planned tests for workload principal, workload attestation, trust domain, tenant binding, and resource-server rejection.

Important limitations remain:

- no SPIFFE ID/SVID/Workload API contracts or endpoints were found;
- no node/workload attestor plugin model, selector evaluation, registration entry lifecycle, bundle store, or SVID issuance service exists;
- `MtlsBindingValidator.verify_certificate()` currently returns valid without certificate-chain, identity, lifetime, key-usage, or revocation verification, so it is not an X.509-SVID validator;
- durable workload/machine records do not by themselves prove runtime attestation or current credential possession;
- the M2M product lane is broader than workload trust and should remain integrated but not conflated.

## 3. Users and Jobs

### Platform and workload identity administrator

1. define trust domains and map environments, clusters, namespaces, accounts, regions, and tenants.
2. register attested selectors to authorized SPIFFE IDs and credential profiles.
3. monitor node/workload attestation, SVID issuance, rotation, bundle health, and stale registrations.
4. federate selected trust domains and understand exactly which workloads gain authentication reachability.
5. suspend a workload, registration, attestor, bundle source, or federation edge during an incident.

### Service owner and developer

1. obtain workload identity without shipping a long-lived bootstrap secret in the application.
2. use X.509-SVIDs for mutual TLS or JWT-SVIDs for audience-bound authentication where appropriate.
3. see the workload's identity, expiry, trust domain, and authorized destinations without exposing private keys.
4. test peer validation and diagnose selector/attestation/registration mismatches.
5. migrate from static service secrets with overlap and rollback.

### Security architect and reviewer

1. inspect the chain from node attestation through selector match, registration, SVID, trust bundle, peer validation, and authorization.
2. enforce trust-domain separation, least privilege, short lifetime, approved algorithms, and audience boundaries.
3. detect wildcard selectors, orphan identities, excessive federation, stale bundles, long-lived credentials, and unmanaged workloads.
4. prove that a workload identity was issued under a specific policy and evidence set.

### Sales, solutions, and account teams

1. assess deployment environment, orchestration, existing SPIRE/service mesh, trust boundaries, migration, and compliance needs.
2. demonstrate identity rotation and cross-domain authentication without exposing customer infrastructure data.
3. distinguish Tigrbl-native capability, SPIFFE compatibility, and tested SPIRE interoperability accurately.

## 4. Architectural Ownership

### SPIFFE protocol/provider layer owns

- SPIFFE ID parsing and canonical validation;
- X.509-SVID and JWT-SVID issuance/validation profiles;
- Workload API gRPC/protobuf behavior and local endpoint semantics where implemented;
- X.509 and JWT bundle formats, streaming updates, and validation;
- SPIFFE federation bundle endpoint profiles;
- adapters to SPIRE or other conforming implementations.

### Workload Trust API owns

- tenant/platform trust-domain and workload identity lifecycle;
- registration entries, selectors, attestor configuration, ownership, policy, and approval;
- provider/agent/server inventory and health;
- federation relationship governance and impact analysis;
- normalized SVID/bundle posture and issuance/validation evidence;
- migration, incident, reporting, and UI-facing schemas.

### Existing owners retain semantics

- principal packages own workload/service/machine identity concepts;
- credential/certificate/JOSE packages own cryptographic material and verification primitives;
- storage owns durable workload, machine, key, certificate, graph, audit, and new SPIFFE records;
- OAuth owns client credentials/token exchange, not SVID issuance;
- resource validation owns access-token validation, not general peer SVID validation;
- authorization decides what an authenticated workload may do;
- attestation pairing will own generalized evidence evaluation when delivered;
- UIX never handles private keys or performs trust validation.

## 5. Identity and Credential Model

### Service, workload, machine, and client

- **Service principal:** durable logical service/product identity and ownership.
- **Workload principal:** a running or deployable software identity tied to environment/runtime selectors.
- **Machine/node principal:** compute substrate that may attest and host workloads.
- **OAuth client:** protocol client authorized for grants and token operations.
- **SPIFFE ID:** URI identifier within a SPIFFE trust domain, normally assigned to a workload.

These may be linked but are not interchangeable. One service can have many workloads; one workload deployment can produce many instances; a node can host many workloads; an OAuth client can represent a service or integration; and a SPIFFE ID identifies the authorized workload identity, not a database row or certificate serial number.

### Credential types

- **X.509-SVID:** short-lived X.509 identity document with a SPIFFE ID, intended for mTLS and preferred where direct channel authentication is possible.
- **JWT-SVID:** short-lived, audience-bound signed token for workload authentication where X.509/mTLS is impractical; treat replay risk explicitly.
- **Trust bundle:** public verification material for one trust domain; X.509 and JWT use-specific content must not be mixed carelessly.
- **OAuth access token:** authorization artifact issued through OAuth; not an SVID.
- **mTLS-bound access token:** OAuth token sender-constrained to a certificate; not automatically a SPIFFE credential.

Private keys should remain local/non-exportable wherever the provider permits. The UI and management API expose fingerprints, public metadata, lifetime, and status only.

## 6. Trust Domain and SPIFFE ID Requirements

### Trust domain

- globally unambiguous configured name and owning tenant/platform scope;
- environment/security-boundary purpose, operator, provider, status, and lifecycle;
- issuance profiles, algorithms, SVID lifetimes, bundle rotation, and key custody;
- authorized attestors, selector namespaces, SPIFFE ID templates, and registration policy;
- federation allowlist and prohibited relationships;
- mapping to existing tenant/realm trust-domain authority without forcing OAuth issuer and SPIFFE trust domain to be identical.

### SPIFFE ID

- canonical URI of the form `spiffe://trust-domain/path` following the SPIFFE specification;
- immutable trust-domain component and validated path normalization;
- stable semantic workload identity, not instance hostname/IP, pod UID, certificate serial, or mutable display name;
- link to canonical workload/service principal and registration entry;
- no user/person identities in the initial workload profile;
- uniqueness and reassignment policy preventing recycled identity confusion.

### Suggested path templates

Examples for design/testing, not mandated defaults:

- `spiffe://prod.example.com/ns/payments/sa/api`;
- `spiffe://corp.example.com/service/billing/environment/prod`;
- `spiffe://edge.example.com/site/chi/device-class/gateway/workload/agent`.

Templates must be deterministic, bounded, reviewable, and protected from selector-value path injection.

## 7. Workload API and Runtime Requirements

Where Tigrbl serves or proxies a SPIFFE Workload API, it must use the official protobuf/gRPC contract and local Workload Endpoint semantics. It must not invent a REST substitute and call it SPIFFE-compatible.

### X.509-SVID profile

- fetch authorized X.509-SVID(s), private-key handle/material according to endpoint guarantees, and trust bundles;
- stream complete updates on rotation and authorization change;
- issue short-lived certificates with required SPIFFE identity and profile constraints;
- validate certificate chain to the correct trust-domain bundle, time, signature, SAN/SPIFFE ID, key usage, path constraints, and profile rules;
- support overlapping bundle/key rotation without accepting removed trust indefinitely;
- ensure the workload only receives identities authorized for its locally attested process.

### JWT-SVID profile

- fetch one or more SVIDs for explicit audience(s), optionally constrained to an authorized SPIFFE ID;
- stream JWT bundles keyed by trust domain;
- validate signature against the subject trust-domain bundle, audience, time, subject/SPIFFE ID, algorithm, and required claims;
- reject arbitrary issuer/bundle fallback and access-token assumptions;
- use short lifetime and prefer X.509-SVID where architecture permits.

### Local endpoint security

- identify the calling process through provider/platform-specific out-of-band mechanisms;
- restrict endpoint filesystem/socket permissions and namespace exposure;
- do not require a shipped application secret merely to call the Workload API;
- bind selector evidence to the current process/container/node and prevent confused-deputy identity retrieval;
- close/revoke authorization promptly when selectors, registration, node trust, or workload status changes.

## 8. Management API Requirements

Use UI-facing REST resources under `/admin/workload-trust`; the local SPIFFE Workload API remains gRPC/protobuf.

### Trust domains and providers

| Method | Proposed route | Purpose |
|---|---|---|
| `GET/POST` | `/admin/workload-trust/domains` | List or draft trust domains. |
| `GET/PATCH` | `/admin/workload-trust/domains/{domain_id}` | Inspect or version configuration. |
| `POST` | `/admin/workload-trust/domains/{domain_id}:validate` | Validate names, authority, profiles, templates, and provider readiness. |
| `POST` | `/admin/workload-trust/domains/{domain_id}:activate` | Activate after review and evidence. |
| `GET` | `/admin/workload-trust/providers` | Inventory SPIRE/native/adaptor endpoints and health. |
| `POST` | `/admin/workload-trust/providers/{provider_id}:verify` | Run bounded interoperability/health checks. |

### Workloads and registrations

- list/detail workload/machine/service identities and their linkages;
- CRUD/versioned registration entries mapping selectors to SPIFFE IDs, parent IDs, DNS names, profiles, lifetimes, and metadata;
- validate/simulate selector matches against synthetic or approved observed workloads;
- submit, approve, activate, suspend, revoke, retire, and restore where safe;
- batch import with dry run, bounded size, partial result manifest, and no silent wildcard expansion;
- detect unmatched workloads, ambiguous matches, multiple identities, or selectors matching unexpected tenants/environments.

### SVID, bundles, and validation

- SVID posture views by identity/provider/type/status/expiry, never private key reads;
- issuance and rotation history with serial/JTI/fingerprint/digest, policy, and evidence;
- bundle versions, keys/certificates, activation/retirement, propagation, and consumer acknowledgement;
- peer validation test accepting only controlled test material and returning hop-by-hop reason codes;
- bundle diff, expiry, stale-consumer, and rollback analysis.

### Federation

- draft federation relationship with foreign trust domain, bundle endpoint, profile, expected endpoint identity, owner, scope, and validity;
- fetch/validate candidate bundle under hardened network policy;
- approve, activate, pause, reverify, rotate bootstrap trust, revoke, and retire;
- graph/path and blast-radius query showing workloads, services, environments, and policies affected;
- no transitive trust assumption unless explicitly defined and verified.

## 9. Canonical Data Requirements

### Workload registration entry

- stable ID, tenant/platform, trust domain, provider, lifecycle/version, owner, and justification;
- SPIFFE ID or governed template;
- parent identity where the provider uses delegation;
- typed selectors with source/attestor namespace and normalized value;
- DNS names, SVID profiles/lifetimes, allowed audiences, and workload metadata;
- created/approved/activated times, evidence, last match, match count, and last issuance;
- constraint preventing ambiguous or cross-tenant selector matches.

### Attested workload observation

- observation ID, provider/node/agent, time window, selectors, process/deployment references, and image digest;
- mapped machine/workload/service principals and tenant/environment;
- attestation method/result/confidence, evidence digest/reference, and expiry;
- registration candidates/matches and reason codes;
- privacy classification and retention policy.

This record describes observed evidence, not permanent truth. General evidence formats and verifier policy should align with the later Attestation API pairing.

### SVID issuance record

- workload/SPIFFE ID, registration, provider, SVID type, fingerprint or JTI, issuer/trust domain, audience for JWT, issued/expiry, status, and rotation lineage;
- public certificate/claim metadata permitted by policy and payload digest;
- key handle/provider reference but never exportable private key value;
- policy/profile versions and attestation observation/evidence link;
- revoke/supersede reason and audit/provenance.

### Trust bundle version

- trust domain, bundle type/use, version/digest, source, keys/certificates, valid window, status, and signer/verification evidence;
- propagation targets, acknowledgements, last fetch, last success, and stale consumers;
- predecessor/successor and emergency rollback/retirement state.

### Federation relationship

- local/foreign domains, direction, endpoint/profile, expected endpoint identity, bootstrap trust, lifecycle, and validity;
- allowed workloads/services/namespaces/audiences or linked policy;
- bundle state, last validation, health, owner, approval, and incident contacts;
- impact and provenance references.

## 10. Attestation, Registration, and Issuance Semantics

1. establish node/agent trust through an approved attestor and current evidence;
2. identify the local calling workload/process without trusting self-asserted selectors;
3. normalize selectors with typed namespaces and source provenance;
4. resolve tenant, environment, trust domain, and canonical workload linkage;
5. match only active registrations using deterministic exact semantics;
6. reject ambiguous, cross-tenant, expired, suspended, or excessive selector matches;
7. authorize requested SPIFFE ID, SVID profile, audience, and lifetime;
8. generate or reference a workload-local key and issue the short-lived SVID;
9. record issuance evidence and stream the complete authorized identity/bundle set;
10. rotate before expiry and remove identities/bundles promptly after loss of authorization;
11. require peer authorization separately after successful authentication.

Possession of a valid SVID authenticates a SPIFFE identity. It does not by itself authorize database access, tenant administration, API scopes, or cross-domain operations.

## 11. Federation and Cross-Cloud Trust Semantics

- Federation exchanges verification bundles between administratively distinct trust domains.
- A foreign bundle must be bootstrapped through an explicitly approved endpoint/profile and verified identity.
- Bundle possession permits cryptographic validation; policy still governs which foreign SPIFFE IDs may communicate.
- Local and foreign trust domains remain separate namespaces; do not translate identities by string replacement.
- Federation is directional in governance even if both parties configure reciprocal relationships.
- Limit foreign identities by domain, path/prefix only where safe, service, namespace, environment, audience, and resource policy.
- Bundle changes require validation, bounded overlap, consumer propagation, and stale-bundle detection.
- Revoking a federation edge must calculate active connection/session/token consequences and stop new trust promptly.
- Existing trust-graph reachability is useful for visualization and policy input, but graph reachability alone is not cryptographic validation.

## 12. Workload Trust Center UIX

### Overview

- registered, observed, attested, active, unmatched, ambiguous, dormant, and suspended workloads;
- SVID issuance/rotation/expiry, bundle freshness, provider/agent health, and federation status;
- priority findings for wildcard selectors, orphan owners, stale agents, failed rotations, long lifetimes, unexpected audiences, and excessive federation;
- environment/trust-domain posture and migration progress away from long-lived secrets.

### Workload inventory

- accessible table grouped by service, environment, tenant, trust domain, cluster/namespace, and owner;
- identity detail showing canonical principal, SPIFFE ID, selectors, registration, current credential posture, last attestation, last issuance, and allowed peers/resources;
- instance observations separated from logical workload identity;
- filters for status, provider, attestor, SVID type, expiry, owner, image digest, and risk finding;
- safe deep links to Service Admin, Certificate Center, Attestation Center, Policy Studio, and Security Signals.

### Registration policy studio

- typed selector builder with source namespace and exact match semantics;
- SPIFFE ID template preview and path validation;
- synthetic/approved observation simulation showing all matches and conflicts;
- warnings for wildcards, high-cardinality selectors, mutable labels, cross-environment overlap, and privileged identity;
- SVID profile, lifetime, audience, DNS name, owner, and approval settings;
- version diff, impact, staged activation, rollback, and change justification.

### SVID and bundle posture

- active/expiring/replaced/invalid issuance metadata without private keys;
- rotation timeline, fingerprint/JTI, provider, profile, lifetime, and issuance reason;
- bundle contents summarized by safe public metadata, use, version, propagation, and consumer acknowledgement;
- semantic bundle diff and overlap/retirement window;
- validation lab for controlled sample SVID/peer identities with explicit reason codes.

### Trust-domain and federation explorer

- domain cards plus accessible graph/table view;
- local/foreign domains, provider, bundle endpoint/profile, relationship direction, constraints, and health;
- path/peer query answering "Can workload A authenticate workload B, and under which bundle/policy?";
- blast-radius mode for domain, registration, attestor, bundle, key, provider, or edge changes;
- graph never implies authorization merely from a visible line.

### Migration and incident modes

- migration planner from client secrets, service keys, static certificates, or cloud credentials to workload identity;
- overlap, validation, traffic observation, cutover, rollback, and old-credential retirement checklist;
- emergency suspend registration/workload/provider/federation, rotate bundle/key, and deny new issuance;
- show effect on running SVIDs, new connections, active sessions/tokens, and recovery;
- redacted incident bundle with policy/evidence digests and timestamps.

## 13. Security, Reliability, and Privacy

- Keep private keys workload-local or in approved non-exportable key providers; never return them through management APIs/UIX.
- Protect Workload Endpoint socket/pipe permissions and prevent container/namespace escape or neighboring-process access.
- Make attestation evidence fresh, nonce/challenge bound where applicable, replay-resistant, and tied to the current node/process.
- Treat selectors as security inputs: type them, normalize them, bound them, and reject ambiguous matches.
- Require short SVID lifetimes and continuous streaming rotation; test clock skew and disconnected rotation behavior.
- Validate X.509-SVID chains and profiles fully; the current permissive certificate verifier must not be reused as proof.
- Validate JWT-SVID audience explicitly and avoid bearer replay; prefer X.509-SVID for direct workload authentication.
- Separate SPIFFE bundles by trust domain and usage; never fall back to a global JWKS/CA pool.
- Protect bundle endpoints against SSRF, downgrade, stale response, redirect abuse, and bootstrap substitution.
- Enforce tenant/environment/trust-domain isolation in records, selectors, issuance, bundles, validation, search, exports, and metrics.
- Use transactional issuance evidence/outbox, durable rotation state, backpressure, and fail-safe recovery.
- Define CA/provider outage, expired SVID, stale bundle, compromised attestor, and clock failure behavior.
- Audit all registration, attestor, trust-domain, bundle, federation, and emergency mutations.
- Minimize runtime metadata; process args, environment variables, labels, node IDs, and image details may be sensitive.

## 14. Stakeholder Requirements

### Technical marketing

- demonstrate secretless bootstrap, short-lived identity rotation, mTLS peer identity, and controlled cross-domain authentication;
- explain service versus workload versus instance versus SPIFFE ID in plain language;
- show integration with existing SPIRE/service mesh before positioning native infrastructure replacement;
- prepare stories for Kubernetes, VMs, bare metal, multi-cloud, edge/IoT gateways, CI/CD runners, service mesh, data platforms, and agentic workloads.

### Developer relations

- publish Workload API client examples for X.509-SVID and JWT-SVID, peer validation, bundle updates, and reconnection;
- provide local SPIRE-compatible test environments and deterministic selector/registration fixtures;
- document trust-domain design, SPIFFE ID conventions, audience rules, rotation, error handling, and authorization separation;
- include negative tests for wrong bundle/domain/audience, expired SVID, ambiguous selector, unauthorized identity, stale bundle, and socket misuse.

### Sales and account management

- use an assessment for platforms, clusters/accounts, environments, existing SPIRE/mesh/PKI, service count, attestors, trust boundaries, federation, compliance, and migration;
- produce a readiness and gap report separating workload inventory, attestation, issuance, validation, policy, and operations;
- define RACI for trust domain, CA/key custody, attestors, registration policy, provider operation, application integration, federation, and incident response;
- avoid promising "zero secrets" where bootstrap, CA, cloud, or provider credentials still exist operationally.

### GTM strategist

- package Workload Identity Governance, SPIFFE Integration, Cross-Cloud Federation, and High-Assurance Workload Trust as distinct offers;
- lead with short-lived workload identity and secret reduction, then federation and policy depth;
- pair with M2M/service admin, certificate lifecycle, attestation, resource validation, authorization, and security signals;
- meter by managed workload, trust domain, provider/cluster, issuance volume, federation edge, or governance tier without charging for security rotation failures.

### Copywriter

- distinguish service, workload, instance, machine/node, client, SPIFFE ID, SVID, certificate, token, and bundle;
- say "authenticated as" rather than "authorized" after SVID validation;
- say "observed" or "attested under policy" rather than "trusted" without scope/time;
- explain expiry, rotation, bundle, selector mismatch, ambiguity, and federation effects precisely;
- never describe private keys as viewable or downloadable from the console.

## 15. Delivery Instructions

### Frontend engineer

- generate typed management clients; do not call the local Workload API from the browser;
- ensure private key fields do not exist in UI schemas, logs, analytics, state persistence, or exports;
- render server-returned selector matches, validation results, trust paths, reason codes, and impact rather than recomputing policy;
- support large inventories with accessible pagination/virtualization and background health/rotation jobs;
- implement version/ETag conflict handling, approval waits, partial failures, stale posture, and incident kill-switch state;
- instrument onboarding, attestation, issuance, rotation, validation, federation, and migration milestones using opaque identifiers.

### UIX designer

- visually separate logical workload, observed instance, registration, SVID, and trust bundle;
- distinguish identity lifecycle, attestation state, credential posture, provider health, and authorization;
- design progressive disclosure from fleet posture to evidence and certificate/token detail;
- cover empty, discovering, unmatched, ambiguous, attestation failed, registered, issuing, rotating, expiring, stale bundle, provider unavailable, suspended, and recovery states;
- provide accessible tables/trees for every graph and relationship workflow;
- meet WCAG 2.2 AA with keyboard flows, non-color status, clear focus, reduced motion, and announced streaming updates.

### Copywriter

- create terminology, lifecycle, attestation, selector, issuance, validation, federation, reason-code, confirmation, and recovery catalogs;
- explain why a workload did or did not receive an identity without disclosing sensitive selectors;
- include affected identities, new versus existing connections, reversibility, and recovery in dangerous-action copy;
- use evidence-calibrated SPIFFE/SPIRE compatibility language;
- write migration guidance that identifies when old credentials can be safely retired.

## 16. Delivery Phases

### Phase 1: Inventory and SPIFFE interoperability

- canonical SPIFFE ID, trust-domain, registration, bundle, and SVID posture contracts;
- SPIRE/provider adapter and read-only inventory/health;
- workload/service/machine linkage, selector observation, and UIX inventory;
- correct X.509/JWT-SVID validation providers and fixtures.

### Phase 2: Governed registration and consumption

- registration lifecycle, selector simulation, approval, import, drift, and incident suspension;
- Workload API client/sidecar integration guidance and SDK examples;
- bundle streaming/rotation posture and peer validation lab;
- migration planner from long-lived credentials.

### Phase 3: Issuance/control-plane depth

- decide between managed external provider, embedded provider, or native implementation;
- if native: node/workload attestors, CA/key custody, official Workload API, SVID issuance/rotation, plugins, scale, and recovery certification;
- security signals and policy response integration.

### Phase 4: Federation and vertical profiles

- SPIFFE federation bundle endpoint profiles and cross-cloud governance;
- multi-region, edge/IoT, CI/CD, data platform, service mesh, confidential-compute, and agent workload packs;
- deeper attestation and certificate lifecycle integration.

## 17. Acceptance Criteria

### API/runtime

- SPIFFE IDs are canonical, tenant/trust-domain safe, and linked to workload principals.
- A registration maps trusted selectors deterministically to only authorized identities and profiles.
- X.509-SVID validation checks the correct bundle/domain, chain, time, SAN identity, key usage, and profile.
- JWT-SVID validation checks the correct trust-domain JWT bundle, signature, subject, audience, and time.
- Bundle rotation propagates with bounded overlap and rejects removed trust after policy expiry.
- Federation does not create transitive or cross-tenant trust implicitly.
- Private keys never cross the workload/provider boundary into management reads or UIX.

### UIX

- An operator can trace workload observation to attestation, registration, SVID issuance, bundle, and peer validation.
- Ambiguous or dangerous selector rules cannot activate without explicit remediation/approval.
- Operators can find expiring/failed credentials and stale bundles before service interruption.
- Federation views explain authentication reachability and separate it from authorization.
- Incident actions disclose blast radius, effect on issued SVIDs/connections, and recovery.

### Evidence/business

- DevRel can run deterministic positive and negative SPIFFE/SPIRE interoperability fixtures.
- Technical marketing can demonstrate rotation and cross-domain authentication without secrets or customer data.
- Sales can produce a readiness/migration report and RACI.
- SPIFFE compatibility or SPIRE interoperability claims link to pinned-version tests and certified evidence.

## 18. Success Measures

- managed versus discovered workload coverage;
- unmatched, ambiguous, orphaned, dormant, and suspended workload rate;
- attestation and registration match success by safe category;
- SVID issuance/rotation success and expiry incidents;
- median credential lifetime and percentage migrated from long-lived secrets;
- stale bundle/provider/agent age and propagation latency;
- peer validation failures by domain/audience/expiry/profile reason;
- federation edge count, scope, and excessive-trust findings;
- workload onboarding and incident containment time;
- unauthorized issuance or private-key exposure incidents.

Guardrails include selector overmatch, cross-tenant issuance, false attestation, stale-bundle acceptance, JWT replay, federation expansion, identity recycling, key exposure, and overstated conformance.

## 19. Source Evidence

### Repository

- `docs/m2m-workload-identity-focus.md`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/workload_identity/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/machine_identity/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/credential_mtls_certificate/`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/authority/trust_domains.py`
- `pkgs/30-storage-runtime/tigrbl-identity-admin-trust-federation-graph/`
- `pkgs/20-providers/tigrbl-security-certificate-mtls/`
- `pkgs/20-providers/tigrbl-security-mtls-cnf-binding-validator/`
- OAuth token-exchange, client-credentials, resource-validation, JOSE, credential, and audit packages;
- `tests/security/test_machine_identity_governance.py` and workload/trust-domain planned tests.

### Standards and primary sources

- [SPIFFE Overview](https://spiffe.io/docs/latest/spiffe-about/overview/)
- [SPIFFE Concepts](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)
- [SPIFFE Identity and Verifiable Identity Document specification](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md)
- [X.509-SVID specification](https://github.com/spiffe/spiffe/blob/main/standards/X509-SVID.md)
- [JWT-SVID specification](https://github.com/spiffe/spiffe/blob/main/standards/JWT-SVID.md)
- [SPIFFE Workload API specification](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Workload_API.md)
- [SPIFFE Federation specification](https://spiffe.io/docs/latest/spiffe-specs/spiffe_federation/)
- [SPIRE project documentation](https://spiffe.io/docs/latest/spire-about/)
- [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)

## 20. Explicit Non-Claims

This brief does not claim that the current repository:

- implements SPIFFE IDs, X.509-SVIDs, JWT-SVIDs, or the SPIFFE Workload API;
- is a SPIRE replacement or production workload identity issuer;
- performs node or workload attestation;
- fully validates X.509 certificates/SVIDs through the current permissive certificate provider;
- exposes or consumes SPIFFE federation bundles;
- has proven cross-cloud workload trust or service-mesh interoperability;
- makes workload authorization automatic after successful authentication.

Those claims require official protocol contracts, full cryptographic/profile validation, attestor and selector security, workload-local key guarantees, streaming rotation, federation hardening, interoperability evidence, operations proof, and release certification.
