# Credential Issuer API + Issuer Studio UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-router-credential-issuer` + `@tigrbl-auth/credential-issuer-uix`<br>
**Status:** New product surface; OAuth/OIDC, JOSE, credentials, policy, attestation, status, storage, and issuer foundations are reusable, but digital credential issuance is absent<br>
**Prepared:** July 11, 2026<br>
**Proposed router owner:** `pkgs/80-routers/tigrbl-auth-router-credential-issuer`<br>
**Proposed protocol owner:** `pkgs/50-protocols/tigrbl-openid4vci`<br>
**Proposed UIX owner:** `pkgs/105-ui/credential-issuer-uix`

## 1. Product Decision

Create a standards-based digital credential issuer that defines governed credential configurations, evaluates subject eligibility and claims, creates wallet-consumable offers, authorizes issuance, verifies holder/key binding, issues credentials in selected interoperable formats, manages deferred/batch jobs and status, and provides privacy-safe operational evidence.

The initial protocol target is the OpenID for Verifiable Credential Issuance (OpenID4VCI) 1.0 Final Specification, approved in September 2025.

The product must keep these boundaries distinct:

- **Credential Issuer:** asserts claims and issues digital credentials.
- **Authorization Server:** authenticates/authorizes the issuance flow and issues OAuth access tokens.
- **Wallet:** receives, stores, and later presents credentials; it is a separate pairing.
- **Verifier:** validates presentations and applies reliance policy; it is a separate pairing.
- **Source systems:** supply authoritative claim/eligibility data but do not become issuers automatically.
- **Trust registry/framework:** tells participants which issuers/configurations are acceptable for a purpose; it is not implied by signature validity.

Digital credentials must use a separate namespace and object model from the repository's authentication `Credential` model. Passwords, passkeys, API keys, service keys, client secrets, DPoP keys, mTLS certificates, MFA factors, and recovery codes are credentials used to authenticate or prove control. Holder-presentable digital credentials assert claims. Their lifecycle, privacy, custody, status, and protocols are materially different.

## 2. Current Repository Reality

Reusable foundations include:

- OAuth/OIDC authorization, token, PKCE, PAR/JAR/RAR-adjacent, device, client authentication, metadata, and resource-server behavior;
- JOSE/JWT signing, key lifecycle, JWKS, DPoP, mTLS, encryption, canonicalization, and algorithm policy;
- tenant/realm issuer authority and discovery;
- principal, identity, membership, federation, provisioning, entitlement, policy, consent-adjacent, audit, and provenance data;
- token profiles, exchange, introspection, and revocation foundations;
- key attestation contracts and proposed Attestation Center;
- credential lifecycle vocabulary for authentication credentials;
- storage, runtime profiles, admin APIs, UIX core, and release/conformance evidence patterns.

No repository evidence was found for:

- OpenID4VCI issuer metadata, credential offers, nonce endpoint, credential endpoint, deferred credential endpoint, notification endpoint, or batch issuance;
- digital credential configuration/schema/version records;
- credential dataset assembly, eligibility, holder/key-binding policy, issued credential registry, status list, or wallet notification;
- SD-JWT VC, W3C VC 2.0, or ISO mdoc issuer implementations;
- digital-credential issuer UIX or interoperability fixtures.

The existing generic credential APIs must not be expanded with a new enum value and treated as sufficient. A new digital-credential domain is required.

## 3. Users and Jobs

### Credential program administrator

1. define a credential type/configuration, claims, source mappings, format, proof/binding, validity, status, and branding.
2. define eligibility, authorization, consent/notice, manual approval, and issuance policy.
3. test offers and wallet issuance flows before activation.
4. stage, publish, supersede, suspend, and retire versions safely.
5. monitor issuance, deferral, notification, failure, status, and privacy posture.

### Claims/data owner

1. declare authoritative claim sources and transformation rules.
2. approve which claims may be issued, for which purpose, to which subjects, and for how long.
3. understand how source changes affect already-issued credentials.
4. minimize correlation, sensitive claims, and unnecessary retention.

### Wallet/integration developer

1. discover issuer metadata and supported credential configurations/formats/proofs.
2. process credential offers using authorization-code or pre-authorized-code flow.
3. obtain nonce, prove key possession, request credential/batch, poll deferred issuance, and send notifications.
4. receive standards-shaped errors and deterministic test fixtures.
5. avoid issuer-specific undocumented claims or endpoints.

### Subject/customer support

1. understand what credential is offered, by whom, why, what claims it contains, and when it expires.
2. resolve eligibility, identity matching, expired offer, failed proof, deferred/manual review, or status questions.
3. reissue or replace a credential without disclosing wallet private keys or presentation history.

### Compliance, privacy, and fraud teams

1. prove claim provenance, issuer authority, policy, approval, format, key, status, and issuance time.
2. detect bulk abuse, replay, offer theft, code interception, identity mismatch, duplicate issuance, weak holder binding, and suspicious source changes.
3. enforce retention, consent/notice, regional, legal basis, and status privacy policy.

## 4. Architectural Ownership

### OpenID4VCI protocol package owns

- issuer/authorization-server metadata schemas and discovery;
- credential offer, nonce, credential, batch, deferred, and notification protocol behavior;
- authorization-code and pre-authorized-code flow extensions;
- proof request/validation and protocol error contracts;
- exact final-specification parameter, endpoint, media type, and capability semantics.

### Credential-format providers own

- SD-JWT VC, W3C VC/Data Integrity/JWT-secured, mdoc, or other profile-native encoding/signing/status rules;
- type metadata/schema resolution and validation;
- holder/key binding and selective-disclosure construction where applicable;
- format-specific test vectors and no lossy cross-format assumptions.

### Credential Issuer API owns

- credential program/configuration/schema/claim/policy/source lifecycle;
- eligibility, dataset assembly, approvals, issuance orchestration, status, replacement, evidence, privacy, and operations;
- wallet/client registration and assignment rules not owned by the generic authorization server;
- UI-facing management schemas and reports.

### Existing owners retain semantics

- OAuth/OIDC packages remain the authorization server;
- JOSE/key providers own signing and key custody;
- Attestation Center owns key attestation appraisal;
- Provisioning/Directory and domain systems own source identity/claim truth;
- Policy Studio owns reusable decisions;
- Wallet and Verifier products own custody/presentation and reliance;
- storage owns durable records;
- UIX never signs credentials or holds issuer private keys.

## 5. Initial Credential Programs

The platform should launch with horizontally reusable configurations rather than one monolithic identity credential:

- organization membership and role/status;
- employee or contractor status with minimal employment claims;
- training completion and certification;
- professional license/status;
- age-over-threshold or eligibility result with no birth date where possible;
- account/customer relationship or account-control proof;
- education enrollment/award;
- insurance/benefit/healthcare eligibility, not clinical records by default;
- device, workload, software, or environment compliance result;
- delegated authority/mandate with actor, purpose, scope, and expiry;
- vendor/supplier qualification and supply-chain provenance.

Each program needs its own legal, semantic, trust, format, subject-binding, status, and verifier-use analysis. Reuse the platform machinery, not a universal claim schema.

## 6. Credential Configuration Requirements

An immutable published configuration version defines:

- stable `credential_configuration_id`, program/type, issuer, tenant/realm, lifecycle, locale, and branding;
- supported format/profile and exact version;
- credential type identifiers, schema/type metadata/context references, and integrity digests;
- claims with semantic identifier, display name, type, cardinality, required/optional, sensitivity, source, transform, selective-disclosure policy, and retention;
- subject identifier strategy: pairwise, persistent, account, organization, device/workload, or profile-native;
- proof types, algorithms, holder/key binding, key attestation requirements, and nonce behavior;
- authorization details/scopes, flow types, client/wallet requirements, offer lifetime, and transaction-code policy;
- eligibility/policy, dataset freshness, manual approval, issuance limits, validity, reissuance/replacement, and duplicates;
- status mechanism/purpose, update latency, suspension/revocation rules, and privacy;
- signing key/provider/profile, cryptographic suite, rotation, and verification metadata;
- relying-party/trust-framework expectations and conformance evidence.

Published configurations are immutable. Corrections create a successor and a migration/reissuance plan. Stable identifiers must not silently change semantics.

## 7. OpenID4VCI Protocol Surface

The final implementation must use exact OpenID4VCI 1.0 paths and metadata semantics. The route families below express required capability.

### Discovery and metadata

- Credential Issuer metadata at the specification-defined well-known location;
- authorization-server metadata through RFC 8414/OIDC discovery as applicable;
- `credential_configurations_supported` that advertises only active, interoperable formats/proofs/claims;
- credential, batch, deferred, notification, nonce, offer, and status endpoints only when supported;
- issuer identifiers and endpoint origins resolved from canonical tenant/realm authority.

### Credential offers

- offer by value or URI according to the standard;
- one or more allowed credential configuration identifiers;
- authorization-code or pre-authorized-code grant data;
- short expiry, single/limited use, tenant/subject/session/purpose binding, and replay protection;
- QR and deep-link representation generated from the canonical offer, not UI-only fields;
- no sensitive claims or bearer credentials embedded unnecessarily in QR/URI/logs/analytics/referrers.

### Nonce and proof

- fresh `c_nonce` from the nonce endpoint when required;
- proof bound to issuer audience and nonce;
- strictly typed `openid4vci-proof+jwt` where JWT proof is supported;
- validate proof signature/key, type, issuer/client/subject rules, audience, nonce, time, algorithm, and replay;
- appraise key attestation through Attestation Center when policy requires it;
- bind the issued credential to the exact validated key(s).

### Credential endpoint

- validate access token, authorization details/configuration, subject, proof, dataset eligibility/freshness, issuance policy, and limits;
- support single and accurately advertised batch issuance;
- batch items share required dataset/format semantics and use distinct cryptographic data/keys where unlinkability calls for it;
- return immediate credential(s), transaction/deferred response, nonce information, and standard errors as specified;
- commit issuance registry/status allocation/evidence atomically with response availability.

### Deferred and notification

- deferred transaction identifiers are opaque, bound, expiring, least-disclosure, and polling-rate protected;
- re-evaluate policy/source freshness at completion according to program policy;
- notification IDs/events are idempotent and cannot be used to enumerate credentials/subjects;
- manual approval has SLA/escalation and does not leak review detail to unauthorized wallets.

## 8. Authorization and Pre-Authorized Flows

### Authorization-code flow

- use hardened OAuth authorization code with PKCE and exact redirect/client policy;
- express credential authorization using the final specification's authorization details/scopes;
- authenticate the subject at required ACR/AMR and collect program notice/consent where applicable;
- bind authorization to issuer, client/wallet, credential configuration, subject, dataset/purpose, proof/key policy, and short expiry;
- do not authorize generic credentials by free-form type name.

### Pre-authorized-code flow

- generate high-entropy, single-use, short-lived codes through an authenticated out-of-band business process;
- optional transaction code/PIN must be separately conveyed, attempt-limited, never logged, and resistant to guessing;
- bind code to exact subject/program/dataset/issuer/offer and permitted wallet/client policy;
- prevent QR/photo forwarding from silently issuing to the wrong subject/key;
- high-value/sensitive programs require additional subject/key/user-presence controls;
- revoke unused codes when the source transaction is canceled or risk changes.

### Eligibility versus authorization

Eligibility determines whether source facts/policy permit a credential. OAuth authorization determines whether this client/wallet/subject may perform issuance. Both are required; neither implies the other.

## 9. Claim Provenance and Dataset Assembly

1. resolve tenant, program/configuration version, subject, authorized source context, and requested locale;
2. fetch claims from approved source adapters using least privilege;
3. validate source identity, version, freshness, confidence/verification state, tenant/subject binding, and legal/purpose permission;
4. normalize using typed, versioned transformations;
5. calculate derived claims through auditable deterministic rules;
6. apply eligibility, minimization, selective-disclosure, and consistency policy;
7. produce immutable credential dataset digest and provenance links;
8. request approval where required;
9. sign/secure format-specific credential and allocate status;
10. persist issuance metadata/evidence without storing unnecessary subject claims or wallet correlation data.

Every issued claim needs a source or documented derivation. UIX must distinguish source-provided, issuer-verified, derived, self-asserted, and holder-bound fields.

## 10. Credential Formats

### SD-JWT VC

SD-JWT VC is an active IETF Internet-Draft as of July 2026, not yet an RFC. If adopted:

- pin a reviewed draft revision/profile and expose it as preview until stabilized/certified;
- implement SD-JWT issuance/disclosures, digest/salt security, type metadata, status, issuer key validation, and key binding per the pinned draft and RFC 9901 SD-JWT foundation;
- use high-entropy salts and protect undisclosed claim correlation;
- ensure mandatory/non-disclosable claims and claim combinations do not undermine privacy;
- plan migration if the draft changes.

### W3C Verifiable Credentials 2.0

- conform to W3C VC Data Model 2.0 and a selected standards-defined securing mechanism;
- use stable vocabularies/contexts/schema resources with integrity and availability controls;
- explicitly define issuer, subject, validity, credential status, terms/evidence as used, and proof mechanism;
- do not call arbitrary signed JSON a W3C Verifiable Credential.

### ISO mdoc

- treat ISO/IEC 18013-5/18013-7 and related mobile document profiles as format-native implementations;
- require namespace/data-element, issuer-signed, device-binding, validity, MSO, digest, and certificate-chain semantics;
- license/access applicable ISO specifications and build conformance fixtures;
- do not convert a JSON credential into mdoc by changing media type.

### Format strategy

Start with one production format and one clearly labeled preview profile based on target ecosystem. Cross-format issuance from the same dataset is allowed only when each configuration has independent semantic/conformance tests and the UI shows format-specific privacy/trust consequences.

## 11. Holder Binding and Key Attestation

- default to cryptographic key binding for credentials whose risk/profile requires holder control;
- support multiple keys in batch only under final-spec rules and unlinkability policy;
- validate proof freshness, issuer audience, nonce, signature, key type/algorithm, and replay;
- keep holder public key/key reference separate from subject identifier;
- a wallet/device key is not proof of human identity without the issuance authentication/eligibility chain;
- key attestation claims about storage/user-authentication properties must be verified through an approved attestation profile, trust source, policy, and freshness;
- avoid requiring hardware attestation for low-risk credentials where it creates exclusion, tracking, or vendor lock-in without justified benefit;
- support reissuance/key rotation without secretly transferring an old private key.

## 12. Status, Suspension, Revocation, and Replacement

### Status semantics

Define per program:

- no online status (short-lived credential);
- active, suspended, revoked, expired, or superseded semantics;
- status purpose and who may change it;
- update/propagation SLA and wallet/verifier behavior;
- privacy and correlation risk;
- recovery/reissuance rules.

### Bitstring status lists

W3C Bitstring Status List v1.0 can provide efficient privacy-oriented status for applicable W3C credentials:

- sufficiently large lists and allocation strategies to reduce holder correlation;
- signed/secured list credentials, cache headers, versioning, publication availability, and rollback protection;
- separation by tenant/program/status purpose without tiny identifying cohorts;
- no per-subject status URL query logging or authentication requirement that becomes a tracking oracle;
- atomic issuance/status-index allocation and revocation update.

### Replacement

- link predecessor/successor internally without placing stable correlation identifiers in holder-visible credentials unnecessarily;
- reason: expiry renewal, key change, claim correction, format/configuration migration, loss, compromise, or source change;
- old credential status/overlap follows explicit policy;
- reissuance must re-evaluate current eligibility and dataset, not clone stale claims blindly.

## 13. Management API Requirements

Use `/admin/credential-issuer` for management; protocol endpoints remain public/protocol surfaces.

### Programs/configurations

- CRUD/version lifecycle for programs, configurations, claim schemas/mappings, formats, branding, eligibility, proof/key-attestation, validity, status, and issuer key policy;
- validate/lint/simulate/submit/approve/publish/stage/supersede/suspend/retire actions;
- source adapter, authorization server, wallet/client policy, status provider, and trust-framework assignment;
- localized display/notice resources with version and fallback.

### Offers and issuance

- create governed individual/batch campaign offers from authorized business events;
- retrieve safe offer state, usage, expiry, subject/program, and failure—never pre-authorized code after creation;
- query issuance/deferred/notification jobs by opaque reference, configuration, subject reference, source transaction, status, time, and reason;
- approve/reject/cancel/retry/reissue/suspend/revoke/replace actions with policy/impact;
- issued credential metadata/evidence, not holder's stored credential copy or wallet activity.

### Schema/type/status operations

- versioned schema/type metadata/context registry with integrity digest, publication state, compatibility, and consumers;
- status list inventory, capacity, allocation, publication, integrity, cache, and health;
- issuer signing key/profile compatibility, rotation, verifier readiness, and affected credential population;
- trust registry/framework publication evidence where applicable.

## 14. Canonical Data Requirements

### Credential program/configuration version

- program/configuration IDs, tenant/issuer, format/profile/version, types/schema, lifecycle, locale/branding, and owner;
- claim definitions/sources/transforms/disclosure/privacy;
- authorization/eligibility/proof/binding/key-attestation policy;
- validity/status/reissue/replacement and signing key policy;
- approvals, publication, predecessor, compatibility, fixtures, and evidence.

### Credential offer

- offer ID, issuer, allowed configurations, grant modes, subject/source transaction reference, client/wallet constraints, created/expiry/use limits, status, and campaign;
- pre-authorized code stored only as digest, transaction-code policy/attempt state, and no raw URI retention beyond explicit short-lived need;
- retrieval/use correlation and security evidence with privacy minimization.

### Issuance transaction

- transaction ID, offer/authorization, subject reference, client/wallet, configuration, proof/key/attestation digest, dataset/source/policy digest, and approval;
- requested/issued/deferred/notified/canceled/failed states and timestamps;
- credential identifier/reference, format, issuer key/version, validity, status list/index, and replacement lineage;
- stable reason codes, idempotency, retry, audit, and privacy classification.

### Issued credential registry

- issuer-side metadata necessary for status, replacement, audit, and support;
- credential digest/reference and format/configuration, not wallet private keys;
- subject reference protected/pseudonymized according to program;
- issued/valid/expired/revoked/suspended/superseded state, status mechanism, signing key, and evidence;
- retention/deletion/legal-hold and no verifier/presentation history by default.

## 15. Issuer Studio UIX

### Overview

- active/draft/suspended programs, offers, successful/deferred/failed issuance, status lists, signing keys, source freshness, and interoperability posture;
- privacy findings for excessive claims, mandatory identifiers, small status cohorts, long validity, weak holder binding, and correlating metadata;
- action queue for expiring keys/configurations, failed source adapters, deferred SLA, status publication, compromised credential cohorts, and schema drift.

### Credential designer

- program goal, subject, relying-party use, trust framework, and risk framing before fields;
- claim catalog with meaning, source, type, sensitivity, selective disclosure, mandatory status, and sample synthetic value;
- format/profile and key/proof/status configuration;
- holder-visible front/back/details preview with accessibility/localization;
- machine-readable schema/type metadata and semantic diff;
- privacy review answering "Can the same credential or claim correlate a holder across verifiers?"

### Eligibility and issuance policy

- source adapters and claim provenance map;
- typed rule builder/dry run linked to Policy Studio where appropriate;
- authorization/pre-authorized flow, subject authentication, consent/notice, key attestation, approval, duplicate/rate limits, validity, and reissue;
- synthetic scenarios for eligible/ineligible/stale/conflict/manual review;
- version diff, impact, staged publication, rollback, and successor migration.

### Offer and issuance operations

- generate test/production offers with unmistakable environment labeling;
- QR/deep-link preview that warns about shoulder surfing/screenshots and sensitive embedding;
- transaction timeline: offered, authorized, proof validated, dataset assembled, approved, issued/deferred, wallet notified, status changed;
- retry/cancel/reissue only where idempotent and policy-safe;
- support view with redacted reason/evidence and no wallet key/private data.

### Status and incident center

- credential/status-list cohorts, capacity, publication/caching, integrity, and propagation;
- suspend/revoke/replace by credential/program/key/source cohort with impact/approval;
- distinguish issuer status update from verifier cache propagation;
- compromised signing key/source/configuration workflow and redacted evidence export;
- never show who presented a credential unless an explicitly separate, consented verifier relationship supplies that data.

### Interoperability lab

- selected wallet/client profiles and exact specification/format versions;
- scripted discovery, offer, authorization/pre-authorized, nonce/proof, credential/batch, deferred, and notification flows;
- positive/negative fixtures and downloadable safe trace;
- capability badges tied to evidence rather than vendor logos.

## 16. Security, Privacy, and Reliability

- Protect issuer signing keys in approved KMS/HSM/non-exportable providers and separate duties for configuration, eligibility, approval, and signing authority.
- Harden offers/codes/tokens/nonces against interception, replay, injection, guessing, referrer/log/analytics leakage, and cross-tenant use.
- Strictly validate wallet/client redirect, metadata, proof type, algorithm, key, audience, nonce, time, and attestation.
- Bind issuance access tokens to exact authorized credential configurations and subject/client context.
- Prevent claim/source substitution, stale dataset issuance, mass assignment, duplicate identity merge, and unauthorized derived claims.
- Treat QR codes as bearer-adjacent transport artifacts and minimize lifetime/data.
- Rate-limit offer/code attempts, nonce, token, credential, deferred polling, notification, batch, and status endpoints.
- Use atomic issuance/status/evidence persistence and idempotency to prevent duplicate credentials after retry.
- Never log credential values, disclosures, pre-authorized/transaction codes, access tokens, holder keys beyond public metadata, or sensitive claims.
- Minimize issuer-side retention and do not build a presentation-tracking graph.
- Publish schema/type/status/issuer metadata with integrity, availability, versioning, cache, and rollback controls.
- Test key rotation, status outage, source outage, deferred queue recovery, regional failover, compromised cohort response, and privacy deletion.

## 17. Stakeholder Requirements

### Technical marketing

- demonstrate credential design, offer, wallet receipt, selective disclosure capability, status update, and replacement using synthetic subjects;
- explain issuer-holder-verifier roles and that verifiability does not guarantee claim truth or verifier trust;
- prepare stories for workforce/contractor, education, professional licensing, age assurance, account ownership, healthcare eligibility, device/workload compliance, and delegated authority;
- label SD-JWT VC as draft/preview until an RFC/profile certification exists.

### Developer relations

- publish OpenID4VCI discovery, offer, authorization/pre-authorized, nonce/proof, issuance, batch/deferred, notification, status, and error quickstarts;
- provide wallet test harnesses and deterministic positive/adversarial fixtures;
- document exact format/profile versions, schemas/type metadata, key binding, status, issuer keys, rate/retry, and privacy;
- maintain interoperability matrices by version and evidence date.

### Sales and account management

- use a discovery worksheet for credential program, issuer authority, subject population, claims/sources, formats, wallets, verifier ecosystem, eligibility, binding, status, validity, legal/privacy, volume, and region;
- provide a readiness report separating program governance, data, protocol, format, wallet, status, trust, and operations;
- define RACI for issuer, source owner, authorization server, key custodian, wallet provider, status publisher, trust framework, verifier, and support;
- avoid claims of government/legal equivalence or universal wallet acceptance without jurisdiction/ecosystem evidence.

### GTM strategist

- package Credential Program Builder, OpenID4VCI Issuance, Status/Revocation, High-Assurance Key Binding, and Interoperability tiers;
- lead with horizontal organization/training/license/eligibility programs before high-regulation identity documents;
- pair with Wallet SDK, Verification Console, Trust Registry, Attestation, Federation, and Policy Studio;
- meter active credential configurations, issuance volume, managed credentials/status, advanced formats, or governance tier without charging for revocation or privacy controls.

### Copywriter

- distinguish authentication credential from digital credential; issuer, holder, subject, wallet, verifier, proof, status, and trust;
- say "issuer asserts" and "cryptographically verifiable" rather than "fact proven";
- explain every claim's source, disclosure, validity, status, and intended use;
- make offer/code expiry, holder binding, deferred review, suspension, revocation, and replacement clear;
- avoid "anonymous" when a design is only selectively disclosable or pairwise.

## 18. Delivery Instructions

### Frontend engineer

- generate typed management clients; protocol endpoints are wallet-facing, not browser admin APIs;
- prevent credential values, subject claims, codes, offers, tokens, and wallet keys from entering logs, analytics, URLs beyond protocol-required deep links, or local storage;
- render server-returned schema, provenance, policy, proof, status, privacy, and reason data;
- support version/ETag, background issuance/deferred/status jobs, partial batch outcomes, stale source, approval, and rollback;
- generate QR locally only from an already authorized canonical offer representation and apply no third-party QR service;
- instrument program/flow stages with opaque identifiers and safe categories.

### UIX designer

- separate program/configuration lifecycle, offer state, issuance state, credential status, key/status-provider health, and interoperability;
- design for semantic claims and holder privacy before visual card aesthetics;
- cover empty, draft, published, offer created/expired/used, authorization pending, proof failed, source stale, approval/deferred, issuing, issued, notification, suspended, revoked, superseded, and recovery states;
- provide accessible claim tables, semantic diffs, QR alternatives, screen-reader descriptions, and localized previews;
- require impact/approval for claim expansion, mandatory disclosure, binding downgrade, key/status changes, mass revocation, and migration;
- meet WCAG 2.2 AA and do not encode credential status/meaning by color or image alone.

### Copywriter

- create credential-program, claim-source, proof/binding, offer, issuance, deferred, status, error, confirmation, privacy, and recovery catalogs;
- write holder-facing notices separately from issuer-operator and developer copy;
- explain what the issuer knows and does not learn about later presentations;
- calibrate format/specification/legal/trust-framework claims to certified evidence;
- provide compromised key/source, false claim, lost wallet/key, expiration, and replacement guidance.

## 19. Delivery Phases

### Phase 1: Issuer core and one format

- separate digital-credential domain contracts/storage;
- OpenID4VCI final metadata, offer, authorization-code and pre-authorized flows, nonce/proof, single credential endpoint, errors, and test wallet;
- program/configuration/claims/source/eligibility/key/status foundation;
- choose one production credential format with full tests.

### Phase 2: Operations and status

- deferred issuance, notifications, batch where justified, manual approval, source freshness, replacement, W3C Bitstring Status List or selected profile status, key rotation, and Issuer Studio;
- interoperability lab and privacy review/evidence.

### Phase 3: Additional formats and assurance

- SD-JWT VC pinned preview/migration path, W3C VC 2.0 or mdoc profile based on target ecosystem;
- key attestation, high-assurance authorization, richer trust-framework metadata, and wallet-provider profiles;
- cohort incidents and large-scale status operations.

### Phase 4: Vertical programs

- workforce, education, professional licensing, age/eligibility, healthcare, financial onboarding, device/workload, supply chain, and delegated-authority packs;
- jurisdiction-specific legal, accessibility, trust, schema, status, and interoperability evidence.

## 20. Acceptance Criteria

### API/runtime

- A conforming test wallet can discover the issuer, consume an offer, authorize, obtain nonce, prove key control, request, and receive the selected credential profile.
- Pre-authorized codes, transaction codes, access tokens, nonces, and proofs are short-lived/bound/replay-safe and never logged.
- Every issued claim links to an approved source or derivation, policy/configuration version, dataset digest, issuer key, status, and issuance evidence.
- Wrong issuer/audience/nonce/key/proof/client/subject/configuration, stale source, ineligible, replayed, duplicate, and cross-tenant requests fail without issuance.
- Status/suspension/revocation/replacement is privacy-aware, integrity-protected, and operationally observable.
- Digital credentials never use the authentication `CredentialKind` lifecycle as a substitute domain.

### UIX

- An admin can design, simulate, review, publish, and supersede a credential configuration.
- Claim source, sensitivity, disclosure, and holder-visible meaning are clear before publication.
- Test and production offers are unmistakable and accessible without QR.
- Operators can trace issuance without seeing wallet private keys or full credential values unnecessarily.
- Status/key/source incidents show affected cohorts, propagation limits, and recovery.

### Evidence/business

- DevRel can run deterministic positive/adversarial OpenID4VCI fixtures against the selected format.
- Technical marketing can demonstrate end-to-end issuance with synthetic data and evidence-backed claims.
- Sales can produce readiness/RACI without subject credentials or personal data.
- OpenID4VCI/format/wallet/trust/legal interoperability claims link to pinned-version certified evidence.

## 21. Success Measures

- issuer discovery/offer/authorization/proof/issuance/deferred/notification success by safe reason;
- time from offer to issuance and deferred SLA;
- duplicate/replay/code-guessing/proof failure detections;
- source freshness, claim conflict, eligibility, and manual-review rates;
- holder-bound and attested-key coverage by program;
- credential/status/key/configuration replacement success and propagation time;
- status list privacy/capacity/availability posture;
- claim count/sensitivity/mandatory-disclosure reduction;
- wallet interoperability pass rate and support time;
- credential/code/token/claim leakage or cross-tenant issuance incidents.

Guardrails include false issuance, claim provenance loss, offer theft, weak binding, holder correlation, status tracking, stale status, key compromise, privacy overcollection, inaccessible holder experience, and overstated legal/trust acceptance.

## 22. Source Evidence

### Repository

- OAuth/OIDC protocol, token, metadata, authorization, client-authentication, PKCE, JOSE, DPoP, mTLS, and key lifecycle packages;
- principal, federation, provisioning, entitlement, policy, audit, provenance, tenant/realm authority, storage, and runtime packages;
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/credentials/` as an authentication-credential domain that must remain separate;
- Attestation, Token Service, Certificate, Policy, and Provisioning pairing briefs;
- repository opportunity map, which identifies issuer/wallet/verifier as missing distinct pairings.

### Standards and primary sources

- [OpenID for Verifiable Credential Issuance 1.0 Final](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [W3C Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/)
- [W3C Bitstring Status List v1.0](https://www.w3.org/TR/vc-bitstring-status-list/)
- [RFC 9901: Selective Disclosure for JWTs](https://www.rfc-editor.org/rfc/rfc9901)
- [SD-JWT-based Verifiable Digital Credentials, active Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)
- [OpenID for Verifiable Presentations 1.0 Final](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)
- applicable ISO/IEC 18013-5 and 18013-7 documents for mdoc profiles.

## 23. Explicit Non-Claims

This brief does not claim that the current repository:

- implements OpenID4VCI, W3C VC 2.0 issuance, SD-JWT VC, mdoc, or credential status lists;
- has a digital credential issuer, wallet, verifier, or trust registry;
- can reuse authentication `Credential` records as verifiable digital credentials;
- interoperates with any named wallet, government ID, education, healthcare, or financial ecosystem;
- makes issuer claims true merely by signing them;
- provides legal equivalence to physical credentials or regulated identity documents;
- supports privacy-preserving selective disclosure merely because JWT/JOSE exists.

Those claims require protocol and format implementations, governed claim provenance, holder binding, status/privacy controls, wallet/verifier interoperability, legal/trust-framework analysis, adversarial tests, operational proof, and release certification.
