# Additional API + UIX Opportunity Map

**Status:** Product-surface research and prioritization  
**Prepared:** July 11, 2026  
**Scope:** Missing horizontal API/UIX pairings, emerging token and credential services, authenticators, proof-of-possession, certificates, attestation, and vertical opportunities

## 1. Executive Recommendation

The current seven product APIs cover the basic identity-provider/control-plane topology well, but important capabilities remain embedded as packages, partial pages, generic admin resources, or SSOT features without a dedicated product surface.

The next portfolio should prioritize reusable control planes rather than adding more CRUD consoles. The strongest additions are:

1. Authenticator Lifecycle API + UIX
2. Authorization Decision API + Policy Studio
3. Federation and Trust API + UIX
4. Provisioning/Directory API + UIX
5. Security Signals API + UIX
6. Workload Trust/SPIFFE API + UIX
7. Certificate Lifecycle API + UIX
8. Attestation API + UIX
9. Token Service API + Token Studio
10. Digital Credential Issuer, Wallet, and Verifier pairings

These surfaces reuse code already present for WebAuthn, DPoP, mTLS, authenticators, policy, delegation, trust graphs, resource validation, certificate domains, and attestation. They also open healthcare, finance, government, education, industrial/IoT, telecom, supply-chain, cloud-native, and agentic-software markets.

## 2. Research Baseline

### Codebase assets already available

The repository already contains meaningful foundations:

- authenticators for password, OTP, recovery code, WebAuthn, API key, client secret, service key, session, remote introspection, federated OIDC, mTLS client certificates, and DPoP proofs;
- policy decision, evaluator, rule, obligation, attribute mapping, authority graph, relationship graph, delegation grant, and provenance packages;
- DPoP, mTLS, JWKS cache, introspection, token exchange, device authorization, JWT access-token profile, CWT-adjacent CBOR/COSE-friendly foundations, and GNAP profile tracking;
- federation registry and trust-federation graph packages;
- certificate, CSR, attestation, trust-domain, and proof-confirmation base contracts;
- planned or partial SSOT features for authentication context, credential-use decisions, workload attestation, trust domains, device/workload principals, and service credential management.

The gap is therefore often productization and lifecycle ownership, not a total absence of primitives.

### Industry movement

- W3C Verifiable Credentials Data Model 2.0 became a Recommendation in May 2025.
- OpenID4VP 1.0 and OpenID4VCI 1.0 became Final Specifications in 2025; a high-assurance interoperability profile followed in December 2025.
- OpenID Federation 1.0 became Final in February 2026.
- Shared Signals Framework, CAEP, and RISC became OpenID Final Specifications in September 2025.
- AuthZEN Authorization API 1.0 provides a standard PDP/PEP decision boundary.
- GNAP is now RFC 9635, with resource-server connections in RFC 9767.
- SPIFFE’s stable Workload API defines X.509-SVID and JWT-SVID profiles and federated trust bundles.
- RATS and EAT provide standard attestation architecture and token formats.
- ACME, EST, SCIM, SET, DPoP, mTLS, CWT, and ACE-OAuth remain practical standards foundations.

## 3. Priority Framework

| Priority | Meaning |
|---|---|
| P0 | Strong horizontal need, close to current code, clear buyer/user, and high portfolio leverage. |
| P1 | High-value expansion requiring meaningful new runtime/storage/product work. |
| P2 | Strategic vertical or emerging bet; incubate behind profiles and interoperability evidence. |
| Research | Do not productize until trust/security/interoperability questions are resolved. |

## 4. P0 Pairings

### 1. Authenticator Lifecycle API + Authenticator Center UIX

**Proposed packages:** `tigrbl-auth-api-authenticators` + `@tigrbl-auth/authenticator-center-uix`

**Why it is missing:** WebAuthn, OTP, recovery code, federated OIDC, mTLS, password, session, and proof authenticators exist as packages, but no dedicated surface owns enrollment, binding, step-up eligibility, recovery, replacement, assurance, or revocation.

**API scope:** authenticator catalog; enroll/verify/activate/suspend/revoke; passkey registration; OTP enrollment; recovery-code lifecycle; federated connection binding; authentication context; device binding; attestation metadata; policy eligibility.

**UIX scope:** My Account mode for personal methods and Tenant Admin mode for policy/help-desk workflows, delivered from one boundary-aware application or two façades over one API.

**Novel credential opportunities:** device-bound versus synced passkeys, hardware-backed passkeys, recovery credentials, delegated recovery contacts, ephemeral step-up authenticators, transaction-bound WebAuthn assertions.

**Primary verticals:** all; especially finance, healthcare, government, workforce, consumer CIAM.

**Guardrail:** authenticator registration is not proof of a claimed assurance level until attestation, policy, and achieved authentication context support it.

### 2. Authorization Decision API + Policy Studio UIX

**Proposed packages:** `tigrbl-auth-api-authorization` + `@tigrbl-auth/policy-studio-uix`

**Why it is missing:** policy and graph machinery is deep, but policy administration remains scattered or legacy-simulated. A standard PDP surface would make the authorization layer productizable.

**API scope:** AuthZEN-compatible evaluation; batch evaluation; subject/resource/action search; decision reasons; obligations; policy versions; simulation; change review; RBAC/ABAC/ReBAC/PBAC/delegation composition; provenance.

**UIX scope:** policy authoring, test fixtures, before/after diff, simulation, decision trace, shadow mode, rollout, rollback, coverage, and audit.

**Novel token opportunity:** issue short-lived decision receipts containing decision ID, policy version, subject/resource hashes, obligations, and expiry. These are audit receipts—not bearer access tokens.

**Primary verticals:** SaaS platforms, fintech, healthcare, government, data platforms, AI/agent systems.

**Guardrail:** do not invent a new policy language first; productize the decision boundary and current rule/graph model, then add language adapters.

### 3. Federation and Trust API + Federation Console UIX

**Proposed packages:** `tigrbl-auth-api-federation` + `@tigrbl-auth/federation-uix`

**Why it is missing:** federation registry and trust graphs exist, while the tracked OpenID Federation feature remains absent/future and no UI owns trust-anchor lifecycle.

**API scope:** OpenID Federation entities, entity statements, trust anchors, trust chains, metadata policy, federation registration, OIDC/SAML bridge metadata where separately supported, issuer allowlists, key rollover, trust marks, discovery.

**UIX scope:** trust graph, entity onboarding, chain resolution, policy application, metadata diff, key/statement expiry, incident isolation, and interoperability diagnostics.

**Novel credential opportunity:** signed trust marks and scoped federation membership credentials, always standards/profile-backed.

**Primary verticals:** research/education, government, healthcare networks, financial ecosystems, multi-company marketplaces.

**Guardrail:** graph connectivity is not transitive trust; display the exact path, policy, anchor, and expiry used.

### 4. Provisioning API + Directory Sync UIX

**Proposed packages:** `tigrbl-auth-api-provisioning` + `@tigrbl-auth/provisioning-uix`

**Why it is missing:** SCIM is recorded as implemented in SSOT, but there is no dedicated SCIM service-provider/client surface, mapping studio, synchronization monitor, or reconciliation UIX.

**API scope:** SCIM Users/Groups, schemas, resource types, service-provider config, bulk, filters, cursor pagination, inbound/outbound connectors, mapping, dry run, reconciliation, quarantine, deprovision.

**UIX scope:** connector onboarding, attribute mapping, preview, sync jobs, drift, conflict resolution, failed records, deprovision impact, and audit.

**Novel credential opportunity:** provisioning assertions and signed sync receipts for inter-organization accountability; not authentication credentials.

**Primary verticals:** workforce IAM, B2B SaaS, education, healthcare, public sector.

**Guardrail:** SCIM transport success is not identity proof; preserve source authority, mapping provenance, and tenant isolation.

### 5. Security Signals API + Continuous Access UIX

**Proposed packages:** `tigrbl-auth-api-security-signals` + `@tigrbl-auth/security-signals-uix`

**Why it is missing:** security event token and anomaly foundations exist, but no product surface owns SET/SSF/CAEP/RISC transmitter/receiver configuration or continuous-access outcomes.

**API scope:** SET issuance/verification; SSF streams; CAEP and RISC events; transmitter/receiver registration; delivery modes; replay/dedupe; subject resolution; stream status; policy reactions; session/token attenuation.

**UIX scope:** event catalog, peer/stream onboarding, delivery health, safe event viewer, correlation, replay quarantine, policy mapping, affected sessions/apps/workloads, and incident timeline.

**Novel token opportunities:** security event tokens, session-risk update tokens, credential-compromise events, workload posture-change events, and privacy-minimized incident receipts.

**Primary verticals:** all enterprises; especially regulated finance, government, healthcare, large SaaS ecosystems.

**Guardrail:** an event is an issuer’s statement, not automatically a fact. Require trust, replay protection, schema/profile validation, and policy review.

## 5. P1 Pairings

### 6. Workload Trust API + Workload Identity UIX

**Proposed packages:** `tigrbl-auth-api-workload-trust` + `@tigrbl-auth/workload-trust-uix`

**Why separate from Service Admin:** Service Admin manages service records and long-lived credentials. Workload Trust should own runtime-attested, short-lived identities and trust domains.

**API scope:** SPIFFE-compatible workload registration/selector mapping; trust domains; X.509-SVID/JWT-SVID metadata and validation adapters; bundle federation; workload attestation; rotation status; cloud/Kubernetes identity exchange.

**UIX scope:** workload inventory, selector/attestation mapping, trust-domain graph, SVID/bundle posture, federation, issuance health, and denied-attestation diagnostics. Private keys remain agent-local.

**Novel credential opportunities:** X.509-SVID, JWT-SVID, workload identity tokens, cloud identity exchange receipts, short-lived deployment credentials.

**Primary verticals:** Kubernetes, service mesh, hybrid/multi-cloud, industrial edge, telecom, data/ML platforms.

### 7. Certificate Lifecycle API + Certificate Operations UIX

**Proposed packages:** `tigrbl-auth-api-certificates` + `@tigrbl-auth/certificate-ops-uix`

**Why it is missing:** certificate/CSR and mTLS abstractions exist, but certificate enrollment, issuance, renewal, chain, revocation, inventory, and policy lack a product owner.

**API scope:** CSR creation/validation; ACME client/server adapters; EST enrollment; internal CA adapter; issuance profiles; renewal; revocation; OCSP/CRL metadata; chain/path validation; mTLS client mappings; certificate transparency where applicable.

**UIX scope:** certificate inventory, expiry/renewal, CSR review, domain/workload/client mappings, chain viewer, trust stores, revocation, automation health, and incident response.

**Novel certificate opportunities:** short-lived workload certs, delegated credentials, device/manufacturing certs, document-signing certs, mTLS OAuth client certs, code-signing identity records.

**Primary verticals:** cloud, IoT, industrial, telecom, payments, healthcare networks, enterprise PKI.

**Guardrail:** never generate/export private keys in a general browser UI; integrate HSM/KMS/agent custody.

### 8. Attestation API + Attestation Studio UIX

**Proposed packages:** `tigrbl-auth-api-attestation` + `@tigrbl-auth/attestation-uix`

**Why it is missing:** attestation provider bases, evidence contracts, key-attestation resources, and planned workload-attestation models exist without an appraisal product surface.

**API scope:** RATS roles; EAT intake/verification; endorsements/reference values; appraisal policy; attestation results; nonce/challenge; key/device/workload attestation; TPM, secure enclave, Android/iOS, WebAuthn, and cloud-provider adapters.

**UIX scope:** evidence source onboarding, appraisal policy, reference values, evidence/result timeline, claim redaction, device/workload posture, failures, freshness, and decision integration.

**Novel proof opportunities:** EAT, key attestation tokens, platform/workload posture credentials, enclave measurements, build/provenance attestations.

**Primary verticals:** government, defense, finance, healthcare devices, confidential computing, industrial/IoT, software supply chain.

**Guardrail:** attestation proves claims about a measured environment under a trust model; it does not prove the application is benign.

### 9. Token Service API + Token Studio UIX

**Proposed packages:** `tigrbl-auth-api-token-service` + `@tigrbl-auth/token-studio-uix`

**Why it is missing:** token issuance, exchange, introspection, revocation, DPoP, mTLS, device flow, resource indicators, and GNAP exist across protocol/runtime packages, but no dedicated operator surface owns token profiles and exchange policy.

**API scope:** token profile catalog; issuance policy; RFC 8693 exchange; audience/resource transformation; delegation/actor chains; DPoP/mTLS binding; JWT/opaque selection; CWT/COSE for constrained profiles; GNAP grants; introspection/revocation; key/profile compatibility; token receipts.

**UIX scope:** profile authoring, exchange graph, claim mapping, lifetime/binding policy, negative tests, sanitized token trace, compatibility matrix, and rollout/shadow analysis.

**Standards-backed token families:** JWT access tokens, opaque reference tokens, DPoP-bound tokens, mTLS-bound tokens, CWT/COSE tokens, JWT-SVID, GNAP access tokens, SETs, EATs, SD-JWT VC, and mdoc presentations.

**Novel token profiles worth exploring:**

- purpose-bound token: one resource/action/purpose with short expiry;
- transaction-bound token: bound to amount/payee/order/request digest;
- attenuated delegation token: actor chain plus monotonic scope reduction;
- workload-posture-bound token: usable only with current attestation result;
- step-up token: records achieved ACR/AMR and transaction context;
- privacy-minimized pairwise token: pairwise subject and minimal claims;
- one-shot capability token: nonce/replay-store-backed single use;
- offline edge token: CWT/COSE, strict audience, tiny lifetime, constrained verification;
- decision receipt: non-bearer proof of a policy decision;
- consent receipt: non-bearer record of what was authorized and when.

These should be profiles over reviewed JOSE/COSE/OAuth/GNAP primitives—not a new home-grown signature format.

**Primary verticals:** finance/payments, healthcare data exchange, AI agents, IoT/edge, supply chain, cross-cloud delegation.

### 10. Credential Issuer API + Issuer Studio UIX

**Proposed packages:** `tigrbl-auth-api-credential-issuer` + `@tigrbl-auth/credential-issuer-uix`

**API scope:** OpenID4VCI; credential offers; authorization/pre-authorized flows; deferred/batch issuance; credential configurations; schema/status; key binding; SD-JWT VC, W3C VC, and mdoc profiles.

**UIX scope:** credential type/schema design, issuance policy, eligibility, offers/QR, batch/deferred jobs, status/revocation, privacy/correlation review, and interoperability tests.

**Horizontal credentials:** employee/contractor status, professional license, training/certification, age-over threshold, account ownership, organization membership, device/workload compliance, delegated authority.

### 11. Credential Wallet API + Wallet UIX/SDK

**Proposed packages:** `tigrbl-auth-api-wallet` + `@tigrbl-auth/wallet-uix` and wallet SDK

**API scope:** credential storage/custody abstraction; OpenID4VCI client; OpenID4VP response; holder binding; presentation consent; backup/recovery; multi-device; status refresh.

**UIX scope:** receive, inspect, organize, present, selectively disclose, revoke/delete local copies, manage keys/devices, and understand verifier requests.

**Guardrail:** decide early whether Tigrbl operates a custodial wallet, provides embeddable wallet components, or only supplies issuer/verifier SDKs. Custody changes the threat, privacy, and regulatory model substantially.

### 12. Credential Verifier API + Verification Console UIX

**Proposed packages:** `tigrbl-auth-api-credential-verifier` + `@tigrbl-auth/credential-verifier-uix`

**API scope:** OpenID4VP requests/responses; DCQL/presentation requirements; trust lists; issuer/schema/status verification; SD-JWT VC selective disclosure; mdoc; W3C VC; holder binding; transaction data; policy decisions.

**UIX scope:** request builder, QR/cross-device flow, disclosed-claim preview, verification stages, trust/policy result, privacy minimization, safe evidence, and negative fixtures.

**Primary verticals:** government ID, education, professional licensing, hiring, healthcare eligibility, travel, age assurance, financial onboarding.

## 6. P2 and Niche Pairings

### 13. Device and IoT Identity API + Fleet Trust UIX

Combine device principals, ACE-OAuth, CWT/COSE, manufacturing certificates, secure boot/attestation, lifecycle, ownership transfer, firmware posture, and constrained-resource policy.

Best verticals: industrial IoT, medical devices, automotive, smart buildings, utilities, retail edge.

### 14. Agent Identity and Delegation API + Agent Trust UIX

Treat AI/software agents as workload principals with human/service sponsors, purpose, tools/resources, budgets, time limits, delegation chains, DPoP/mTLS keys, attestation, and revocation.

Use GNAP, OAuth token exchange, RAR, resource indicators, short-lived PoP tokens, and decision receipts. Do not create “AI agent JWT” as an unaudited new format.

Best verticals: enterprise automation, financial operations, developer agents, customer-service agents, healthcare administration.

### 15. Entitlement Governance API + Access Review UIX

Own access packages, entitlement catalog, assignments, certification campaigns, separation of duties, expiry, approvals, orphan detection, and revocation proof. Reuse policy, delegation, relationships, and audit.

Best verticals: regulated enterprises, finance, healthcare, government, B2B SaaS.

### 16. Secrets Lease/Broker API + Credential Broker UIX

Broker short-lived database, cloud, SSH, API, and third-party credentials from authenticated/attested identities. UIX owns lease policy, request/approval, expiry, rotation, revocation, and audit—not secret display as a default.

Best verticals: DevOps, platform engineering, data infrastructure, CI/CD.

### 17. Trust Registry API + Trust Registry UIX

Own issuers, schemas, trust anchors, certificate roots, credential types, status mechanisms, federation membership, approved algorithms, and jurisdiction/vertical profiles.

Best verticals: government ecosystems, healthcare exchanges, education consortia, supply chain, open finance.

### 18. Communications Identity API + Certificate/Attestation UIX

Profile certificates and signed identity assertions for telecom/email/document channels: STIR/SHAKEN, BIMI/VMC, S/MIME, document signatures, webhook signing identities.

Best verticals: telecom, regulated communications, customer support, legal/document workflows.

### 19. Supply-Chain Identity API + Provenance UIX

Bind builders, artifacts, deployments, workloads, SBOM/provenance attestations, signing identities, and policy decisions. Integrate Sigstore/in-toto/SLSA adapters rather than inventing a parallel provenance ecosystem.

Best verticals: software vendors, regulated DevSecOps, AI model supply chain, industrial firmware.

## 7. Vertical Packaging Without Forking the Core

Use profiles, schemas, policy packs, connector packs, and scenario packs over horizontal APIs:

| Vertical | Horizontal pairings to compose |
|---|---|
| Finance/open banking | Authenticator, Authorization, Federation, Signals, Token Service, Credential Verifier, Certificates |
| Healthcare | Federation, Provisioning, Authorization, Credentials, Signals, Certificates, Attestation |
| Government/eID | Authenticators, Federation, Credential Issuer/Wallet/Verifier, Trust Registry, Attestation |
| Education/research | Federation, Provisioning, Credential Issuer/Verifier, Trust Registry |
| Cloud-native/SaaS | Workload Trust, Token Service, Authorization, Signals, Certificate Ops, Secrets Broker |
| IoT/industrial | Device/Fleet Trust, Attestation, Certificates, CWT Token Service, Authorization |
| Telecom | Workload Trust, Certificates, Signals, Communications Identity, Token Service |
| AI agents | Agent Identity, Authorization, Token Service, Attestation, Workload Trust, Signals |
| Supply chain | Attestation, Certificates, Trust Registry, Provenance, Workload Trust |

Avoid separate vertical forks of the identity runtime. Vertical packages should constrain and compose the same canonical objects and operations.

## 8. Recommended Delivery Sequence

### Wave 1: Productize existing depth

1. Authenticator Lifecycle
2. Authorization Decision/Policy Studio
3. Provisioning/SCIM
4. Security Signals
5. Federation/Trust

### Wave 2: Workload and cryptographic trust

6. Workload Trust/SPIFFE
7. Certificate Lifecycle
8. Attestation
9. Token Service

### Wave 3: Digital credentials and vertical packs

10. Credential Issuer
11. Credential Verifier
12. Wallet decision/SDK
13. Device/IoT, Agent, Trust Registry, and vertical profiles

## 9. Opportunity Scoring

| Pairing | Code reuse | Market breadth | Differentiation | Delivery risk | Priority |
|---|---:|---:|---:|---:|---|
| Authenticator Lifecycle | High | High | Medium | Medium | P0 |
| Authorization + Policy Studio | High | High | High | Medium | P0 |
| Provisioning/SCIM | Medium | High | Medium | Medium | P0 |
| Security Signals | Medium | High | High | Medium | P0 |
| Federation/Trust | High | Medium-High | High | Medium | P0 |
| Workload Trust/SPIFFE | Medium-High | High | High | High | P1 |
| Certificate Lifecycle | Medium | High | Medium-High | High | P1 |
| Attestation | Medium | Medium-High | High | High | P1 |
| Token Service | High | High | High | High | P1 |
| Credential Issuer/Verifier | Medium | High | High | High | P1 |
| Wallet | Low-Medium | High | High | Very high | P1/Research |
| Device/IoT | Medium | Medium | High | High | P2 |
| Agent Identity | High | Emerging | High | High | P2 |
| Secrets Broker | Medium | High | Medium | Very high | P2 |

## 10. Product Guardrails

- Do not invent cryptographic token formats when a profile over JWT/JWS, CWT/COSE, SD-JWT, mdoc, SET, EAT, SVID, GNAP, or X.509 suffices.
- Separate bearer tokens, proof-of-possession tokens, credentials, attestations, certificates, security events, and non-bearer receipts in the object model and UI language.
- Every token/credential needs explicit issuer, subject/holder, audience/verifier, purpose, lifetime, key binding, replay model, status/revocation, privacy properties, and trust policy.
- Browser UIX must not custody private keys or long-lived secrets by default.
- New surfaces need independent API boundaries; do not recreate Legacy Admin as a universal trust console.
- Every novel profile starts experimental, with negative tests, threat model, interoperability fixtures, and prohibited marketing claims.
- Add vertical value through profiles and connectors, not duplicated core runtime implementations.

## 11. Recommended Next Briefs

Create these one at a time next:

1. Authenticator Lifecycle API + UIX brief
2. Authorization Decision API + Policy Studio brief
3. Federation and Trust API + UIX brief
4. Provisioning/SCIM API + UIX brief
5. Security Signals API + UIX brief
6. Workload Trust/SPIFFE API + UIX brief
7. Certificate Lifecycle API + UIX brief
8. Attestation API + UIX brief
9. Token Service API + Token Studio brief
10. Digital Credential Issuer/Wallet/Verifier briefs

## 12. Source Notes

Repository research covered package manifests, authenticator and security packages, trust-domain/certificate/attestation bases, authorization and delegation packages, protocol/resource-server surfaces, docs, tests, and SSOT feature inventories.

Industry research used primary standards sources from W3C, IETF/RFC Editor, OpenID Foundation, and SPIFFE, including VC Data Model 2.0, OpenID4VCI/VP, OpenID Federation, AuthZEN, Shared Signals/CAEP/RISC, GNAP, SCIM, SET, DPoP, mTLS, CWT/ACE, RATS/EAT, ACME, and SPIFFE Workload API/SVID specifications. Standards and drafts must be rechecked at implementation time.
