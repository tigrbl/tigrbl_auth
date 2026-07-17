# Certificate Lifecycle API + Certificate Center UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-router-certificates` + `@tigrbl-auth/certificate-center-uix`<br>
**Status:** New product surface; certificate DTOs/bases, mTLS credentials, key lifecycle, rotation policy, storage, and JOSE foundations exist<br>
**Prepared:** July 11, 2026<br>
**Proposed router owner:** `pkgs/80-routers/tigrbl-auth-router-certificates`<br>
**Proposed protocol/provider owners:** certificate domain providers plus optional ACME/EST adapters<br>
**Proposed UIX owner:** `pkgs/105-ui/certificate-center-uix`

## 1. Product Decision

Create a governed certificate lifecycle product surface for inventorying, requesting, issuing/importing, deploying, renewing, rotating, validating, revoking, replacing, and retiring X.509 certificates and their trust chains.

The product must support distinct certificate programs rather than one generic "certificate" bucket:

- internal service and mTLS certificates;
- OAuth mTLS client-authentication and certificate-bound token credentials;
- workload/SPIFFE certificates through the Workload Trust product;
- TLS server certificates from public or private CAs;
- device/machine certificates;
- intermediate/root trust anchors under stricter authority controls;
- later code-signing, S/MIME, document-signing, or other profiles only through profile-native requirements.

The API is a management/orchestration plane. Private-key generation and custody should remain in approved KMS/HSM/agent/workload environments wherever possible. Certificate Center must never become a browser-based private-key vault.

## 2. Current Repository Reality

The repository already provides:

- `CertificateRequest` covering CSR/certificate operation, subject, key reference, CSR, issuer, issuer certificate, serial, validity, SAN, extensions, signature algorithm, format, policy, and options;
- `CertificateVerifyRequest` covering certificate, roots, intermediates, validation time, revocation flag, policy, and options;
- `CertificateServiceDomainBase` methods for CSR creation, issuance, verification, and parsing;
- provider-neutral key creation/import/rotation/destruction/discovery/export contracts;
- durable mTLS credential binding with principal, thumbprint, subject DN, DNS/URI/IP/email SANs, status, and metadata;
- key rotation policies with profile, key class/use, algorithm, cadence, maximum age, overlap, retirement, approval, publication, and versioning;
- durable key rotation events;
- mTLS credential/proof-binding contracts and RFC 8705-related tests;
- key attestation, JOSE, trust-domain, resource-validation, audit, service/workload identity, and authorization foundations;
- a Platform Admin Key Rotation page that correctly labels its action as planned.

Critical gaps:

- no complete certificate inventory, authority/profile, order, deployment, renewal, revocation, validation, or trust-store lifecycle;
- no ACME or EST implementation was found; `examples/acme_notes_cli` is an example product name, not ACME protocol support;
- no OCSP/CRL production integration, certificate transparency monitoring, or replacement-chain model;
- no durable issuer/account/order/challenge/deployment/consumer records;
- no Certificate Center UIX;
- `MtlsBindingValidator.verify_certificate()` currently returns `valid=True` without path, signature, time, name, usage, policy, or revocation validation.

The current provider is sufficient only for confirmation-thumbprint comparison. It must not be marketed or reused as a general X.509 validator until replaced/composed with a real path-validation implementation.

## 3. Users and Jobs

### PKI and security administrator

1. define certificate authorities, accounts, issuance profiles, trust stores, renewal policy, and approval requirements.
2. see every managed certificate, owner, identity, consumer, key posture, chain, expiry, replacement, and deployment state.
3. detect invalid chains, forbidden algorithms/extensions, stale trust, failed renewal, and unmanaged certificates.
4. revoke/replace compromised certificates and verify deployment/recovery.
5. preserve an evidence chain for issuance, approval, deployment, validation, renewal, revocation, and destruction.

### Service/workload owner

1. request the correct profile without manually constructing unsafe CSR fields.
2. generate or reference a non-exportable key in the intended environment.
3. receive and deploy a certificate with automated renewal and health checks.
4. understand which service instances/clients depend on it.
5. migrate or rotate without outage and retire the predecessor safely.

### Platform/SRE operator

1. monitor expiry, renewal windows, deployment coverage, handshake/validation failures, and trust-bundle propagation.
2. retry recoverable orders and diagnose validation challenges/provider failures.
3. roll out replacement certificates gradually and verify consumers before revoking old material.
4. respond to CA compromise, mass revocation, algorithm deprecation, or trust-anchor changes.

### Compliance, sales, and account teams

1. distinguish internal/private PKI from publicly trusted TLS requirements.
2. report certificate posture and policy compliance without revealing private key or sensitive subject data.
3. identify ownership between customer, Tigrbl, CA, cloud/KMS, and deployment operator.
4. avoid implying public-trust, CA/B Forum compliance, hardware protection, or automated renewal without evidence.

## 4. Architectural Ownership

### Certificate domain owns

- X.509 CSR/certificate parsing, encoding, signing request, issuance, and full validation contracts;
- certificate profiles, extension constraints, chain/path building, identity/name checks, and reason codes;
- lifecycle semantics for request/order, issue/import, deploy, renew/rekey/replace, revoke, expire, and retire;
- issuer/provider adapters for internal CA, ACME, EST, cloud CA, or external enterprise CA;
- OCSP/CRL and trust-store integration contracts.

### Certificate API owns

- tenant/platform resource composition and authorization;
- authorities, accounts, profiles, orders, certificates, deployments, consumers, trust stores, renewal jobs, incidents, reports, and UI-facing schemas;
- provider selection, secret references, idempotency, workflow, audit, metrics, and evidence;
- safe actions and lifecycle projection across providers.

### Existing owners retain semantics

- key providers/KMS/HSM own private keys and cryptographic operations;
- authenticator lifecycle owns human/client mTLS authenticator binding;
- OAuth owns mTLS client authentication and certificate-bound access tokens;
- Workload Trust owns SPIFFE X.509-SVID semantics and Workload API;
- Attestation owns generalized evidence for keys/devices/workloads;
- storage owns durable state;
- authorization governs who may request, approve, issue, deploy, revoke, or reveal metadata;
- UIX never parses as the authority or handles private keys.

## 5. Certificate Program and Profile Model

Every certificate belongs to an explicit, versioned profile. A profile defines:

- purpose: TLS server, TLS client/mTLS, workload, device, CA, code signing, email, document, or custom governed profile;
- public versus private trust model;
- allowed issuers/authorities and key providers;
- subject/SAN templates and required/forbidden identity fields;
- key type, size/curve, signature algorithm, exportability, and attestation requirements;
- basic constraints, key usage, extended key usage, certificate policies, name constraints, and critical extension rules;
- validity maximum, renewal window, overlap, retirement, revocation, and replacement behavior;
- CT, OCSP, CRL, AIA, CAA, ACME, EST, and audit requirements where applicable;
- owner, environment, tenant, approval, deployment, and validation policy.

Profiles must not let requesters override protected fields. Public TLS profiles must track the current applicable CA/Browser Forum requirements and issuer policy as mutable external compliance inputs, not hard-coded assumptions.

## 6. Core Lifecycle Semantics

### Request and CSR

1. resolve tenant, owner, identity, purpose, provider, and profile;
2. authorize request and subject/SAN scope;
3. generate/reuse a key only under profile policy and approved provider;
4. create or ingest CSR and validate signature, public key, subject, SAN, requested extensions, and policy;
5. store CSR digest/public metadata and key handle, never unnecessary private material;
6. create an idempotent order with approval state and provider correlation.

### Issuance/import

1. complete provider-specific authorization/challenges;
2. receive the issued leaf and chain;
3. validate chain, identity/name, key match, validity, extensions, usage, policy, and issuer;
4. record serial, fingerprints, SPKI digest, authority key identifier, subject key identifier, SCT/CT data where applicable, and provenance;
5. link predecessor/successor and set deployment state;
6. never mark certificate active merely because a CA returned bytes.

### Deployment

- distribute certificate/chain to explicit consumers through provider-native secret stores, agents, workload APIs, ingress controllers, load balancers, or application integrations;
- keep private key in the original approved key boundary;
- track desired versus observed certificate fingerprint/version for every consumer;
- validate configuration and handshake/peer behavior after deployment;
- require a minimum healthy coverage or explicit exception before predecessor retirement.

### Renewal, rekey, and replacement

- distinguish renewal (new cert, same key where allowed), rekey (new key), and modification (identity/profile changes);
- default toward new keys according to profile/risk;
- support ACME Renewal Information (ARI, RFC 9773) suggested windows when the provider advertises it;
- choose jittered renewal time within valid policy/provider window and apply retry/backoff;
- retain bounded overlap, verify deployment, then retire/revoke predecessor;
- link replacement lineage and prevent conflicting concurrent replacements.

### Revocation and destruction

- accept reason, evidence, urgency, affected scope, and replacement strategy;
- revoke at issuer when supported and publish/observe OCSP/CRL state;
- stop new deployments and remove trust/binding where required;
- rotate/rekey and verify replacement before or alongside revocation according to incident severity;
- destroy private keys only through provider lifecycle and retention/legal policy;
- preserve public certificate and immutable evidence as allowed.

## 7. Validation Requirements

Validation must produce a structured result, not only a Boolean. At minimum:

- parse DER/PEM safely with input size/count limits;
- build an allowed path to an explicitly configured trust anchor using supplied/intermediate stores;
- verify every signature and issuer/subject linkage;
- evaluate not-before/not-after with explicit clock/skew;
- enforce basic constraints, path length, key usage, extended key usage, critical extensions, name constraints, and policy constraints;
- verify hostname/DNS/IP/URI/email or principal identity according to the selected profile, not generic CN fallback;
- enforce key/signature algorithm and strength policy;
- check revocation through configured OCSP/CRL policy with defined soft/hard fail behavior;
- validate CT/SCT requirements for public TLS where applicable;
- distinguish expired, not-yet-valid, untrusted root, missing intermediate, signature failure, name mismatch, revoked, unknown revocation, weak algorithm/key, invalid use, forbidden extension, and policy failure;
- include safe path/provenance metadata without revealing private or excessive certificate content.

Thumbprint equality for `cnf.x5t#S256` is a sender-binding check only. It must run after or alongside authentic certificate and TLS validation, not replace it.

## 8. Management API Requirements

Use resource-oriented routes under `/admin/certificates`. Provider-native protocols remain in their owning adapter/frontdoor.

### Authorities, accounts, and profiles

- `GET/POST /admin/certificates/authorities` and versioned authority lifecycle;
- account enrollment/rotation/deactivation using secret references and external account binding where required;
- `GET/POST /admin/certificates/profiles` with validate, simulate, submit, approve, activate, supersede, and retire actions;
- trust anchor/intermediate inventory and constrained trust-store assignment;
- provider capability discovery that advertises only supported order, renewal, revocation, ARI, OCSP, CRL, CT, key, and challenge features.

### Orders and certificates

| Method | Proposed route | Purpose |
|---|---|---|
| `GET/POST` | `/admin/certificates/orders` | List or create governed certificate orders. |
| `GET` | `/admin/certificates/orders/{order_id}` | Show request, validation, approval, provider, and issuance state. |
| `POST` | `/admin/certificates/orders/{order_id}:validate` | Validate CSR/request/profile before provider action. |
| `POST` | `/admin/certificates/orders/{order_id}:approve` | Approve where separation of duties requires it. |
| `POST` | `/admin/certificates/orders/{order_id}:issue` | Start/resume idempotent provider issuance. |
| `GET` | `/admin/certificates` | Search inventory with posture and ownership. |
| `GET` | `/admin/certificates/{certificate_id}` | Return public metadata, lineage, deployment, validation, and evidence. |
| `POST` | `/admin/certificates/{certificate_id}:validate` | Validate under a named profile/trust-store/time. |
| `POST` | `/admin/certificates/{certificate_id}:renew` | Create a linked replacement order. |
| `POST` | `/admin/certificates/{certificate_id}:rekey` | Replace certificate and key. |
| `POST` | `/admin/certificates/{certificate_id}:revoke` | Execute governed issuer/domain revocation. |
| `POST` | `/admin/certificates/{certificate_id}:retire` | End use after replacement/impact checks. |

### Deployments and consumers

- inventory certificate consumers and desired/observed versions;
- create staged deployment plans with target selector, batch size, health gates, observation window, rollback, and predecessor behavior;
- deploy, pause, resume, rollback, verify, and close actions;
- handshake/configuration validation through authorized probes;
- drift, stale consumer, failed reload, and unreported consumer detection;
- dependency/blast-radius query by certificate, key, issuer, root, intermediate, profile, algorithm, SAN, owner, service, environment, and tenant.

### Renewal and revocation operations

- renewal schedule and job inventory, including ARI window/source where available;
- retry/dead-letter with idempotency and provider rate-limit awareness;
- expiring/expired/failed renewal and mass-renewal views;
- OCSP/CRL/CT monitoring records and issuer status;
- emergency mass replacement/revocation workflow with approval threshold and kill switch.

## 9. ACME and EST Requirements

### ACME client adapter

If implemented, support RFC 8555 primitives through a dedicated adapter:

- directory discovery, nonce, account, key rollover, order, authorization, challenge, finalize, certificate retrieval, and revocation;
- HTTP-01, DNS-01, TLS-ALPN-01, or device-attest challenges only where explicitly implemented and securely delegated;
- JWS request protection, nonce replay handling, problem documents, retries, and rate limits;
- External Account Binding where required;
- ACME ARI renewal windows and replacement identifiers per RFC 9773;
- provider-specific capability profiles without forking core lifecycle semantics.

Challenge plugins are high authority. DNS plugins especially require narrowly scoped credentials and must not expose zone-wide secrets to the API/UI.

### ACME server

A Tigrbl-operated ACME server is out of the initial scope. It would require account/order/authorization/challenge/finalize/revocation semantics, CA policy, validation agents, abuse prevention, nonces, problem responses, scale, and conformance. Do not imply server support from an ACME client adapter.

### EST

EST (RFC 7030) may be added for enterprise/device enrollment. It needs native server/client authentication, CA certificates, CSR attributes, enrollment/reenrollment, server-key generation decisions, and profile tests. It must not be represented as ACME with renamed routes.

## 10. Canonical Data Requirements

### Certificate authority/provider

- authority/provider ID, tenant/platform scope, type, trust model, endpoint, capability profile, lifecycle, owner, and contacts;
- root/intermediate public metadata, chain, policy/CPS links, allowed profiles, and jurisdictions;
- secret/key/account references, never raw values;
- health, last verification, rate-limit, ARI, OCSP, CRL, CT, and incident posture.

### Certificate order

- order ID, tenant, profile/version, requester, owner, subject/SAN request, CSR digest, key handle/public-key digest, provider, and idempotency key;
- draft/validation/approval/provider/challenge/finalization/issuance/failure/cancel state;
- provider correlation URLs/IDs, challenge references, retry schedule, errors, and timestamps;
- predecessor/replacement relationship and issuance evidence.

### Managed certificate

- certificate ID, tenant, owner, purpose/profile, principal/service/workload/device binding, provider/authority, and lifecycle;
- serial, leaf/chain fingerprints, SPKI digest, SKI/AKI, subject, SANs, issuer, validity, algorithms, usages, policies, and public extensions;
- CT/OCSP/CRL metadata where relevant;
- key handle/provider and attestation reference, never private key;
- predecessor/successor, renewal window, revocation/expiry/retirement, and evidence links.

### Deployment and consumer

- consumer ID/type, tenant/environment/region, owner, integration provider, and target reference;
- desired/observed certificate/key/chain versions and last observation;
- deployment batch, status, health checks, reload/restart requirements, rollback, and failure reason;
- no storage of cloud/service credentials outside secret references.

### Trust store/version

- trust-store ID, scope, intended usages, active version, roots/intermediates, source, digest, validity, and owner;
- consumer assignments and propagation status;
- additions/removals, overlap, approval, rollback, and provenance;
- explicit prohibition against indiscriminate global trust-store fallback.

## 11. Certificate Center UIX

### Overview

- total/managed/unmanaged certificates, expiring windows, renewal failures, revoked/invalid certificates, stale deployments, and weak-policy findings;
- CA/provider, trust-store, key custody, and deployment health;
- upcoming renewal load with ARI windows where present;
- critical actions for compromised material, mass expiry, algorithm deprecation, stale root, and broken revocation status.

### Inventory

- accessible table by certificate, purpose/profile, owner, principal/service, issuer, environment, SAN, key posture, expiry, renewal, deployment, and status;
- detail page with safe parsed metadata, chain, validation, lifecycle/lineage, key reference, deployments, consumers, and evidence;
- separate raw PEM/download permission from ordinary metadata view;
- filters for unmanaged, duplicate key, shared key, long validity, weak algorithm, invalid use, missing owner, unknown consumer, and stale observation.

### Request wizard

1. select certificate program/profile and owner;
2. select/generate approved key provider and attestation policy;
3. enter identity/SAN inputs allowed by the profile;
4. create/upload CSR and validate it;
5. choose issuer/provider/account and deployment targets;
6. preview certificate fields, renewal, overlap, revocation, and impact;
7. satisfy approval/challenge steps;
8. issue, validate, deploy, and verify;
9. schedule renewal and predecessor retirement.

### Chain and validation inspector

- leaf-to-anchor chain view plus accessible ordered table;
- per-certificate signature, time, constraints, usage, name, algorithm, policy, and revocation result;
- tested identity/hostname/audience/purpose and selected trust store/profile;
- alternative/missing path explanation without suggesting unsafe root import;
- stable reason codes and remediation.

### Renewal and deployment operations

- renewal calendar/queue with policy and ARI suggested windows;
- replacement lineage and old/new semantic diff;
- deployment rollout showing desired/observed fingerprint and health per consumer;
- pause, retry, rollback, verify, retire predecessor, and revoke actions;
- mass-event workspace grouping affected certificates by common issuer/key/profile/consumer.

### Trust and incident center

- CA/account/trust-store inventory and versions;
- root/intermediate change impact before activation/removal;
- compromised key/certificate/issuer workflow with containment, rekey, replace, deploy, revoke, verify, and close stages;
- incident evidence bundle with public metadata/digests and redacted operational context;
- no private key reveal or browser upload except explicitly governed import workflows.

## 12. Security, Reliability, and Privacy

- Keep private keys non-exportable where possible and represent them through opaque provider handles.
- Require explicit authority for key export/import; never show private material in UI, logs, analytics, errors, URLs, or support exports.
- Validate CSRs before signing and reject requester control over serial, issuer, CA bit, critical extensions, policy OIDs, usage, or unauthorized SANs.
- Use cryptographically strong unique serials according to issuer/profile requirements.
- Protect CA/root/intermediate keys with stronger separation, HSM/KMS, quorum, offline controls, and ceremony evidence appropriate to authority level.
- Enforce separation of duties for CA/profile/trust-store changes, high-value issuance, key export, and mass revocation.
- Harden ACME/EST/provider fetches against SSRF, redirect/downgrade, credential leakage, DNS manipulation, replay, and rate abuse.
- Scope DNS/API challenge credentials narrowly and isolate plugins.
- Use full validation and explicit trust stores; never trust based only on parsed fields or thumbprint presence.
- Define OCSP/CRL hard/soft-fail by profile and surface unknown status distinctly.
- Make renewal idempotent, jittered, rate-aware, observable, and resilient to clock/provider/network failures.
- Track deployment truth; successful issuance is not successful rotation.
- Encrypt sensitive subject/SAN and infrastructure metadata according to classification and tenant.
- Test backups, restore, provider migration, CA rollover, trust-store rollback, mass expiry, and compromised-key recovery.

## 13. Stakeholder Requirements

### Technical marketing

- demonstrate request-to-deployment, automated renewal, chain validation, and zero-outage rekey with non-sensitive sample infrastructure;
- distinguish certificate automation from becoming a public CA;
- prepare stories for API mTLS, internal PKI, public TLS operations, device identity, private cloud, service mesh, edge, and regulated certificate governance;
- use evidence-backed labels for ACME, EST, HSM, CT, OCSP, public trust, and SPIFFE.

### Developer relations

- publish CSR, ACME-client, internal-CA, mTLS binding, renewal, deployment, and validation quickstarts;
- provide deterministic chains and negative fixtures for expiry, wrong name, missing intermediate, untrusted root, revoked, weak algorithm, invalid use, malformed extension, and key mismatch;
- document provider capability differences, reason codes, renewal/backoff, ARI, trust stores, and safe secret handling;
- supply local test CA/ACME environments clearly marked non-production.

### Sales and account management

- use a certificate discovery worksheet for use cases, trust model, current CA/PKI, certificate count, lifetime, domains/SANs, key custody, deployments, renewal, revocation, compliance, and ownership;
- provide a readiness/posture report separating inventory, issuance, key custody, deployment, validation, renewal, and incident response;
- define RACI across customer, Tigrbl, CA, DNS/cloud provider, application owner, and security operator;
- never promise public trust or compliance merely because certificate automation exists.

### GTM strategist

- package Certificate Inventory, Automated Lifecycle, Private PKI Orchestration, Public TLS Operations, and Advanced Trust Governance separately;
- pair with Workload Trust, Attestation, Authenticator Center, Service Admin, Resource Validation, and Security Signals;
- prioritize mTLS/internal service and public TLS inventory/renewal before operating a native CA;
- meter managed certificates, authorities/accounts, deployments, renewal operations, trust stores, or governance tier without penalizing security rotation.

### Copywriter

- distinguish key, CSR, certificate, chain, root, intermediate, trust store, issuer/CA, profile, order, deployment, renewal, rekey, replacement, revocation, expiry, and retirement;
- say "issued" separately from "deployed" and "validated";
- avoid "secure" or "trusted" without naming validation profile, time, identity, and trust anchor;
- explain OCSP/CRL unknown versus good and revoked;
- make private-key custody, impact, overlap, reversibility, and recovery explicit.

## 14. Delivery Instructions

### Frontend engineer

- generate typed clients and rely on server parsing/validation/reason codes;
- ensure private-key fields are absent from normal schemas and scrub upload/import state after completion;
- render certificate/chain metadata safely without HTML interpretation or uncontrolled huge extension values;
- support large inventories, background validation/renewal/deployment jobs, partial results, stale versions, and idempotent actions;
- implement reveal/download permissions separately with audit acknowledgement;
- instrument issuance, renewal, deployment, validation, revocation, and recovery milestones using opaque IDs and safe categories.

### UIX designer

- separate certificate lifecycle, validation, renewal, deployment, revocation, and key posture visually;
- use progressive disclosure from portfolio risk to ASN.1/extension-level detail;
- design empty, discovering, requested, pending approval/challenge, issued-not-deployed, deploying, active, renewal scheduled/running/failed, expiring, expired, invalid, revoked, and recovered states;
- provide accessible ordered chain tables and relationship alternatives to diagrams;
- require previews for trust-anchor removal, key export, rekey, revocation, mass replacement, and predecessor retirement;
- meet WCAG 2.2 AA with keyboard operation, focus management, non-color status, accessible timelines/charts, and reduced motion.

### Copywriter

- create terminology, profile, order, challenge, validation, renewal, deployment, revocation, incident, reason-code, confirmation, and notification catalogs;
- explain failures with the tested identity/profile/trust-store context;
- make provider versus customer versus Tigrbl ownership explicit;
- distinguish retryable provider/network failures from policy or certificate-invalid failures;
- write safe mass-expiry, compromised-key, CA outage, failed deployment, and rollback guidance.

## 15. Delivery Phases

### Phase 1: Inventory and real validation

- canonical certificate, profile, authority, trust store, consumer/deployment, lineage, and evidence records;
- full X.509 parsing/path/name/use/policy/time validation provider and negative fixtures;
- import/discovery inventory and Certificate Center read/posture experience;
- replace or constrain the permissive certificate verifier.

### Phase 2: Internal issuance and deployment

- CSR/order/approval lifecycle, internal/external CA adapter, KMS/HSM key references, staged deployment, renewal/rekey, revocation, and audit;
- mTLS certificate/principal bindings and resource-validation integration;
- operational dashboards and incident workflow.

### Phase 3: ACME automation

- RFC 8555 ACME client adapter with selected challenges, secure plugins, EAB, key rollover, revocation, and provider profiles;
- RFC 9773 ARI renewal scheduling/replacement lineage;
- public TLS/CT/CAA/CA-policy checks where applicable and evidence-backed interoperability.

### Phase 4: Additional profiles

- EST/device enrollment, deeper OCSP/CRL services, private PKI orchestration, SPIFFE integration, and vertical profiles;
- code signing/S/MIME/document profiles only with separate standards and custody requirements;
- native CA or ACME server only after an explicit product/security decision.

## 16. Acceptance Criteria

### API/runtime

- A certificate validates only when chain, signature, time, identity/name, usage, extensions, algorithm, trust store, profile, and configured revocation requirements pass.
- CSR/order issuance cannot request unauthorized SANs, CA capability, usages, extensions, lifetime, or algorithms.
- Every managed certificate has owner, purpose/profile, key reference, issuer, lineage, consumers/deployments, renewal, and evidence.
- Renewal/rekey creates an idempotent linked replacement and does not retire the predecessor before deployment health gates.
- Revocation records issuer outcome and downstream containment/validation state.
- Private keys are never returned through management reads/UIX.

### UIX

- Operators can find certificates expiring or failing renewal/deployment before outage.
- Validation results show the exact failing chain element/check and safe remediation.
- Issued-but-not-deployed and deployed-but-not-observed states are unmistakable.
- Trust-store and revocation changes disclose blast radius and rollback/recovery.
- Critical workflows are accessible without relying on graphs, hover, color, or raw PEM.

### Evidence/business

- DevRel can run positive/negative path-validation and renewal fixtures.
- Technical marketing can demonstrate deterministic issue-deploy-renew-revoke behavior without production keys.
- Sales can provide a readiness report/RACI without sensitive key or infrastructure disclosure.
- ACME, EST, public-trust, HSM, CT, OCSP, and interoperability claims link to versioned tests and release evidence.

## 17. Success Measures

- inventory coverage and unmanaged certificate count;
- certificates missing owner, profile, key custody, deployment, or renewal;
- expiry incidents and days of advance detection;
- renewal/rekey success, retry, and completion before policy deadline;
- issued-to-deployed and deployed-to-verified latency;
- stale/failed consumer deployment rate;
- validation failures by safe reason category;
- revocation/replacement/containment SLA;
- weak/shared/exportable key and algorithm-policy findings;
- trust-store propagation and stale-consumer time;
- unauthorized issuance or private-key exposure incidents.

Guardrails include false-valid verification, SAN/usage escalation, key leakage, trust-anchor overreach, failed renewal outage, incomplete deployment, stale revocation, accidental mass revocation, and overstated public-trust/compliance claims.

## 18. Source Evidence

### Repository

- `pkgs/02-contracts/tigrbl-security-trust-contracts/src/tigrbl_security_trust_contracts/types.py`
- `pkgs/05-bases/tigrbl-security-trust-domain-bases/src/tigrbl_security_trust_domain_bases/bases.py`
- `pkgs/20-providers/tigrbl-security-certificate-mtls/`
- `pkgs/20-providers/tigrbl-security-mtls-cnf-binding-validator/`
- `pkgs/20-providers/tigrbl-authenticator-mtls-client-cert/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/credential_mtls_certificate/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/key_rotation_policy/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/key_rotation_event/`
- key provider/lifecycle, JOSE, attestation, trust-domain, audit, service/workload, OAuth mTLS, and resource-validation packages;
- `pkgs/105-ui/platform-admin-uix/pages/KeyRotationPage.tsx`;
- mTLS, key-rotation, and certificate-credential tests.

### Standards and primary sources

- [RFC 5280: Internet X.509 PKI Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280)
- [RFC 6125: Service Identity in TLS](https://www.rfc-editor.org/rfc/rfc6125)
- [RFC 8555: Automatic Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555)
- [RFC 9773: ACME Renewal Information](https://www.rfc-editor.org/rfc/rfc9773)
- [RFC 7030: Enrollment over Secure Transport](https://www.rfc-editor.org/rfc/rfc7030)
- [RFC 6960: Online Certificate Status Protocol](https://www.rfc-editor.org/rfc/rfc6960)
- [RFC 9162: Certificate Transparency Version 2.0](https://www.rfc-editor.org/rfc/rfc9162)
- [RFC 8705: OAuth Mutual-TLS and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [CA/Browser Forum TLS Server Certificate Baseline Requirements](https://cabforum.org/working-groups/server/baseline-requirements/requirements/)

## 19. Explicit Non-Claims

This brief does not claim that the current repository:

- performs complete X.509 path, identity, usage, policy, or revocation validation;
- implements ACME, ACME Renewal Information, EST, OCSP, CRL, or Certificate Transparency operations;
- operates a certificate authority or ACME server;
- issues publicly trusted TLS certificates or meets CA/Browser Forum requirements;
- integrates with HSM/KMS/private CA/public CA products in a certified profile;
- has automated certificate deployment, renewal, replacement, or mass-revocation recovery;
- can use the current always-valid certificate provider for production trust decisions.

Those claims require full validation and lifecycle implementations, provider integrations, adversarial and interoperability tests, key-custody assurance, deployment truth, incident exercises, compliance evidence, and release certification.
