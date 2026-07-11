# Attestation API + Attestation Center UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-attestation` + `@tigrbl-auth/attestation-center-uix`  
**Status:** New product surface; key-attestation contracts/runtime/storage and adjacent evidence foundations exist  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-attestation`  
**Proposed capability owners:** verifier-neutral attestation contracts, appraisal engine, and format/provider adapters  
**Proposed UIX owner:** `pkgs/95-ui/attestation-center-uix`

## 1. Product Decision

Create a verifier-neutral attestation product surface that receives or requests evidence about a key, authenticator, device, machine, workload, confidential-computing environment, build/release artifact, or other supported subject; validates its provenance and freshness; appraises it against versioned policy, endorsements, and reference values; and produces bounded, signed or integrity-protected attestation results for relying parties.

The product must preserve the Remote ATtestation procedureS (RATS) separation of roles and artifacts:

- **Attester:** creates Evidence about a target environment.
- **Verifier:** validates and appraises Evidence using endorsements, reference values, and appraisal policy.
- **Relying Party:** consumes an Attestation Result under its own policy before deciding access or action.
- **Endorser and Reference Value Provider:** supply distinct supporting artifacts.

Evidence is not an attestation result. Cryptographic validity is not policy compliance. Policy compliance is not identity authentication or authorization. An attestation result is scoped, time-bound verifier output and must not be presented as proof that a device or workload is universally "safe."

## 2. Current Repository Reality

The repository already contains:

- provider-neutral `AttestKeyRequest`, `VerifyAttestationRequest`, and `AttestationEvidence` contracts;
- `IAttestationProvider` and `AttestationProviderBase` interfaces for key evidence generation and verification;
- key usages and operations for attestation, verification, key certification, and public export;
- storage-runtime operations that dispatch `attest_key` and `verify_attestation` to a configured key provider;
- durable `KeyAttestationEvidence` with key/version, issuer key/provider, format, evidence, claims, status, verification time, metadata, tenant, and realm;
- durable machine/workload identities with attestation-related fields and planned workload-attestation tests;
- authenticator/WebAuthn-related evidence concepts elsewhere in the identity plane;
- release artifact signing/attestation generation and release attestation events;
- capability/evidence/provenance and certification artifacts;
- policy, resource-validation, certificate, JOSE, trust-domain, audit, and security-event foundations.

The missing product layer includes:

- canonical RATS roles and artifact types;
- challenge/nonce and evidence-session lifecycle;
- typed evidence-format adapters and real verifier providers;
- endorsement/reference-value/trust-anchor registries;
- versioned appraisal policy and attestation-result contracts;
- subject binding, freshness, replay defense, composite/layered evidence, privacy minimization, result issuance, relying-party integration, incident response, and UIX.

### Existing exposure problem

`KeyAttestationEvidence` is currently listed in contract manifests for public, my-account, developer, tenant-admin, platform-admin, service-admin, and resource-validation APIs. Raw attestation evidence is security-sensitive verifier input, not generic CRUD data. The new product must replace broad table exposure with purpose-built, permissioned, redacted views. Public and unrelated APIs should receive only the minimum result/status needed for their job.

### Evidence families must remain distinct

Key/device/workload attestation, WebAuthn authenticator attestation, and software release provenance can share envelopes, policy/evidence infrastructure, and UI patterns, but their claims, roots, freshness, threat models, and relying-party semantics are not interchangeable.

## 3. Users and Jobs

### Verifier/security administrator

1. register verifier providers, trust anchors, endorsers, reference-value sources, formats, and appraisal policies.
2. test evidence with known positive and negative fixtures before activation.
3. understand each validation/appraisal step and the basis for the result.
4. rotate trust/reference values and calculate the impact on subjects and relying parties.
5. suspend a compromised endorser, verifier, policy, or reference set.

### Workload/device/key owner

1. request a fresh challenge and submit supported evidence.
2. see whether evidence was received, validated, appraised, and accepted for a named purpose.
3. understand actionable failure reasons without exposing verifier defenses or unrelated sensitive claims.
4. re-attest after upgrade, rotation, posture change, or expiry.
5. prove current key/device/workload posture to an approved relying party with minimal disclosure.

### Relying-party/application developer

1. request or consume a normalized attestation result rather than implementing vendor evidence parsing.
2. validate result issuer, audience, subject, nonce/context binding, policy/version, claims, and expiry.
3. combine attestation facts with authentication and authorization policy.
4. test stale, replayed, wrong-audience, revoked, and noncompliant results.

### Compliance, privacy, and incident teams

1. trace result claims back to evidence, endorsements, reference values, verifier, policy, and time.
2. control evidence retention, residency, privileged access, export, and disclosure.
3. detect reference-value drift, compromised endorsement roots, weak evidence, replay, and suspicious failure patterns.
4. contain affected identities/credentials through their owning products.

## 4. Architectural Ownership

### Attestation contracts own

- RATS roles and conceptual artifacts;
- challenge, evidence submission, endorsement, reference value, appraisal policy, attestation result, and verification DTOs;
- normalized claims and validation/appraisal reason taxonomy;
- format-neutral provider interfaces and capability discovery.

### Format/provider adapters own

- parsing and cryptographic validation for EAT, TPM, TEE/cloud confidential-computing, key/HSM/KMS, WebAuthn, platform/device, workload, or release evidence;
- provider-specific endorsement/reference-value retrieval and normalization;
- secure challenge/evidence collection where applicable;
- no cross-format fallback or invented claims.

### Attestation API owns

- tenant-scoped verifier/source/policy/artifact lifecycle;
- challenge and attestation-session orchestration;
- subject resolution/binding, provider selection, persistence, privacy, authorization, audit, metrics, and evidence lineage;
- appraisal execution and result issuance/query/revocation;
- UI-facing management and operational schemas.

### Existing owners retain semantics

- key providers own key custody and key-native evidence generation;
- Authenticator Center owns authenticator lifecycle and consumes approved attestation results;
- Workload Trust owns workload registration/SVID issuance and consumes workload results;
- Certificate Center owns certificate lifecycle and consumes key/device results;
- release certification owns software release claim/certification semantics;
- authorization owns access decisions based on result facts;
- Security Signals owns posture-change events and response orchestration;
- UIX never verifies evidence or signs results.

## 5. RATS Artifact Model

### Evidence

Evidence is claims generated by an Attester about one or more target environments. Required metadata includes:

- evidence ID/session, tenant, format/profile/version, source/attester, target subject hint, and receipt time;
- challenge/nonce, freshness method, issued/measurement time where available, and expiry/use limit;
- protected bytes or reference, digest, signature/protection metadata, and evidence chain/composition;
- privacy classification, storage mode, retention expiry, and access controls;
- validation status and parser/provider version.

Evidence claims remain untrusted until format, protection, provenance, freshness, and subject binding validate.

### Endorsement

An Endorsement is a protected statement from a manufacturer/platform/issuer about attesting capabilities, keys, device class, or properties. Store issuer, scope, subject/model identifiers, validity, trust chain, digest, status, and source. Endorsement validity does not assert current runtime state.

### Reference values

Reference values are expected/allowed measurements, versions, configurations, ranges, sets, or constraints used in appraisal. They require:

- subject/product/environment scope;
- producer and provenance;
- version, effective/expiry windows, supersession, and revocation;
- measurement algorithm/type and comparison semantics;
- staged activation and impact analysis.

Do not label every reference value "known good"; acceptable policy may use sets, ranges, exclusions, minimum versions, or relationships.

### Attestation result

A result is verifier output for a relying party and purpose. It includes:

- result ID, issuer/verifier, audience/relying party, tenant, subject, purpose, and correlation;
- policy/version, evidence/endorsement/reference digests or opaque evidence references;
- normalized claims, compliance/status, confidence/strength descriptors, and stable reason codes;
- issued/expiry times, nonce/context binding, result format/version, and signature/integrity metadata;
- supersession/revocation and privacy classification.

Default results should disclose claims necessary for the relying-party decision, not raw evidence.

## 6. Initial Attestation Profiles

### Key custody and provenance

- supported KMS/HSM/secure-element key attestation formats;
- public key/fingerprint binding, provider identity, key origin, generation environment, exportability, usage/operations, algorithm, version, and hardware protection claims;
- current `AttestKeyRequest` as an input seed, expanded with challenge, subject, purpose, profile, and freshness;
- explicit differentiation between provider assertion, verified evidence, and policy-compliant key.

### WebAuthn authenticator

- registration-time attestation object, authenticator data, attestation statement, AAGUID, credential public key, RP binding, challenge, origin, and metadata/roots;
- format-specific verification and metadata/status policy;
- support "none" or self attestation only under explicitly lower-assurance policy;
- no product claim that an attestation format alone proves a specific assurance level.

### Workload/machine/device

- node/platform evidence, workload measurement/selectors, boot/firmware/software state, image digest, configuration, secure boot/TEE/TPM claims where supported;
- current machine/workload principal linkage;
- freshness and instance binding required before workload identity issuance or privileged access;
- composite/layered evidence represented without flattening away which environment asserted each claim.

### Confidential computing

- cloud/vendor TEE evidence profiles and endorsements;
- measurement, signer/product/security version, debug state, TCB status, and bound runtime data;
- provider verifier adapter first; local verifier only with maintained endorsements/reference data and conformance evidence;
- policy should treat platform/vendor outage and revocation status explicitly.

### Release/software provenance

- signed build/release statement, artifact digest, builder identity, source/materials, environment, tests, and policy evidence;
- integrate existing release attestations while preserving supply-chain vocabulary and release-certification ownership;
- do not equate signed build provenance with runtime device/workload attestation.

## 7. Standards Requirements

### RATS architecture

Use RFC 9334 terminology and preserve the Attester, Verifier, Relying Party, Endorser, Reference Value Provider, Evidence, Attestation Result, and two appraisal-policy concepts. Support both passport and background-check integration patterns without forcing one topology.

### Entity Attestation Token

Where EAT is supported, pin RFC 9711 and applicable media types (RFC 9782):

- support only declared JWT or CWT/CBOR profiles and claim sets;
- validate token type/content type, signature/MAC/encryption profile, issuer/key, nonce/time/freshness, UEID/subject, and profile-required claims;
- preserve submodules/layers and profile-specific claims;
- reject unknown critical claims and algorithm/type confusion;
- do not accept generic JWT access tokens as EAT evidence/results.

### Additional formats

TPM quotes, TCG event logs, DICE, Android/Apple/device, WebAuthn, cloud TEE, key-provider, and supply-chain formats require dedicated adapters and primary specifications. A generic JSON upload is not an attestation profile.

## 8. Challenge and Freshness Semantics

1. authenticate/authorize the requester and resolve tenant, subject/purpose, profile, verifier, and relying party;
2. issue a cryptographically unpredictable, single-use challenge bound to session, tenant, intended subject, evidence type, audience/purpose, and short expiry;
3. receive evidence within size/rate/time limits and atomically consume the challenge;
4. verify that protected evidence binds the nonce/challenge or approved freshness mechanism;
5. reject reuse, wrong session/tenant/subject/purpose, expired challenge, missing binding, or weak freshness;
6. record receipt and digest before asynchronous processing;
7. issue result only after all required validation/appraisal steps complete;
8. expire results according to the shortest evidence, endorsement, reference, policy, and relying-party validity constraint.

Timestamp-only freshness is allowed only when the profile establishes trustworthy time. Cached evidence/results require explicit reuse policy, context binding, maximum age, revocation/status checks, and audience controls.

## 9. Verification and Appraisal Pipeline

### Evidence validation

1. resolve exact format/profile and provider;
2. parse safely under depth/count/size constraints;
3. validate protection, chain/key, issuer/endorser, algorithm, and profile;
4. validate challenge/freshness and replay state;
5. bind evidence to the expected attester/target/key/credential/workload/device/artifact;
6. retrieve/version endorsements and reference values through hardened sources;
7. validate endorsement/reference authenticity, scope, status, and time;
8. normalize only claims supported by validated evidence provenance.

### Evidence appraisal

1. select active appraisal policy by tenant, purpose, subject/profile, relying party, and time;
2. evaluate required claims, measurements, versions, configurations, debug state, key posture, TCB/security level, and exclusions;
3. treat missing, indeterminate, stale, unsupported, and noncompliant separately;
4. produce stable reasons and provenance for every derived result claim;
5. apply disclosure policy for the relying party;
6. issue integrity-protected, audience-bound, short-lived result or store a reference result.

### Relying-party appraisal

The relying party independently decides how to use the result: allow, deny, attenuate, require step-up/re-attestation, quarantine, or manual review. The verifier must not hide this authorization decision inside an opaque `valid=True` result.

## 10. API Requirements

### Attestation transaction

| Method | Proposed route | Purpose |
|---|---|---|
| `POST` | `/attestation/v1/challenges` | Create a bounded challenge/session for a profile, subject, purpose, and relying party. |
| `POST` | `/attestation/v1/evidence` | Submit evidence against a challenge. |
| `GET` | `/attestation/v1/sessions/{session_id}` | Return safe processing state and next action. |
| `GET` | `/attestation/v1/results/{result_id}` | Return authorized minimal result/reference. |
| `POST` | `/attestation/v1/results/{result_id}:verify` | Validate an issued result under expected issuer/audience/context. |
| `POST` | `/attestation/v1/results/{result_id}:revoke` | Revoke/supersede result through authorized control path. |

Synchronous evidence appraisal may be offered for bounded fast providers, but the canonical transaction must support asynchronous provider/reference retrieval and polling/callback without duplicate effects.

### Management resources

- `/admin/attestation/verifiers` and provider capability/health lifecycle;
- `/admin/attestation/profiles` for format, claims, freshness, source, privacy, and result settings;
- `/admin/attestation/policies` for versioned appraisal policy;
- `/admin/attestation/endorsers`, `/endorsements`, `/reference-sources`, `/reference-values`, and `/trust-anchors`;
- `/admin/attestation/evidence` as highly restricted metadata/search, not unrestricted raw payload CRUD;
- `/admin/attestation/results`, `/subjects`, `/sessions`, `/incidents`, and `/reports`;
- validate, test, simulate, submit, approve, activate, suspend, supersede, revoke, retire, refresh, and impact actions as appropriate.

### API invariants

- exact tenant filtering before lookup and non-disclosing not-found behavior;
- opaque identifiers and idempotency for submission/result/action;
- immutable evidence/result lineage and policy/reference/version pinning;
- raw evidence only through privileged, audited, purpose-bound access;
- server-side verification; browser/client hints never determine result;
- stable status/reason taxonomy and explicit indeterminate outcomes;
- no generic mutation of received evidence after digest/receipt.

## 11. Canonical Data Requirements

### Attestation profile

- profile ID/version, subject/evidence types, format/media type, verifier provider, and lifecycle;
- allowed algorithms/protection, trust/endorsement/reference sources, challenge/freshness, max evidence/result age, and reuse;
- required/optional claims, normalization, appraisal policy, result format, disclosure, audience, and privacy/retention;
- owner, approvers, compatibility version, fixtures, and evidence.

### Attestation session

- tenant, requester, subject hint/resolved subject, profile, purpose, relying party/audience, verifier, and status;
- challenge digest/reference, issued/expiry/used times, freshness mode, request context digest, and idempotency;
- evidence/result links, failure reason, correlation, and audit.

### Supporting artifact

- kind (endorsement, reference value, trust anchor), producer/source, format/profile, scope, subject/product/model/environment, and claims/measurements;
- protected artifact/reference and digest, signature/trust validation, issued/effective/expiry, status, supersession/revocation, and provenance;
- source refresh/health and impact relationships.

### Appraisal policy

- policy/version, tenant, purpose, subject/profile, relying parties, effective window, lifecycle, and owner;
- typed constraints and handling of missing/unknown/stale/error;
- required evidence strength/freshness and disclosure/result policy;
- test fixtures, simulation outcome, approval, rollout, rollback, and provenance.

## 12. Attestation Center UIX

### Overview

- recent sessions/results by profile, subject class, verifier, purpose, tenant/environment, and outcome;
- validation versus appraisal failures, indeterminate/stale results, replay attempts, expired references, provider/source health, and policy drift;
- posture for keys, authenticators, workloads, machines/devices, confidential environments, and releases;
- prioritized actions for compromised endorsement, stale reference values, verifier outage, mass failure, weak profile, and over-retained evidence.

### Verifier/profile setup wizard

1. choose subject/evidence profile and provider;
2. configure trust anchors, endorsers, reference sources, and retrieval policy;
3. define freshness/challenge and subject binding;
4. define claim normalization and evidence appraisal;
5. define result audience, disclosure, lifetime, and relying-party behavior;
6. run positive, negative, replay, stale, and wrong-subject fixtures;
7. review privacy, retention, residency, failure, and provider outage behavior;
8. submit/approve/activate.

### Evidence and appraisal inspector

- trust-stage view: received, parsed, cryptographically valid, fresh, subject-bound, endorsed/referenced, appraised, result issued, relying-party outcome;
- each claim shows source layer/environment, evidence field/reference, appraisal rule, and disclosure state;
- endorsement/reference/policy versions and timestamps;
- composite/layered evidence tree plus accessible ordered table;
- raw bytes/claims restricted, masked, and audited;
- exact failing/indeterminate step with calibrated remediation.

### Policy and reference-value studio

- typed constraint builder with equality, range, set, minimum version, relationship, and exclusion operations supported by the profile;
- semantic version/digest diff and subject impact;
- synthetic/redacted historical simulation with false-positive/unknown analysis;
- staged activation, observation-only mode, approval, rollback, supersession, and emergency suspend;
- reference sets grouped by product/model/environment and effective window.

### Subject posture and investigations

- subject detail showing identity linkage, recent results, evidence strength/freshness, policy, credentials, workload/device state, and relying-party use;
- timeline of challenge, submission, validation, appraisal, result, access/issuance action, and security signals;
- investigate replay, subject mismatch, compromised root/endorser, reference drift, debug/TCB finding, and anomalous evidence patterns;
- containment links invoke owning product actions rather than direct table updates.

### Privacy and operations

- evidence inventory by classification, retention, region, access, and deletion schedule;
- verifier/source latency, failure, queue, retry, and dependency health;
- privileged evidence-access log and export history;
- redacted evidence/result bundle with digests and policy/reference lineage.

## 13. Security, Privacy, and Reliability

- Generate unpredictable single-use nonces and bind evidence/results to tenant, session, subject, purpose, and audience.
- Protect against replay, relay/cuckoo, confused-deputy, evidence substitution, mix-up, downgrade, parser differential, and composite-layer confusion.
- Enforce strict format/media type, algorithm, key use, claim, critical field, size, nesting, submodule, and collection limits.
- Trust anchors, endorsements, reference values, and appraisal policies are security-critical configuration requiring provenance, versioning, approval, and rollback.
- Harden remote sources against SSRF, DNS rebinding, redirects, oversized content, stale cache, and compromised update channels.
- Separate evidence validation errors from noncompliant appraisal and system/provider failure.
- Treat missing/unknown as explicit; never coerce them to pass.
- Encrypt evidence and sensitive results at rest, minimize retention, and audit reveal/export.
- Avoid stable device identifiers in results when pairwise/opaque identifiers satisfy the relying party.
- Do not reveal detailed firmware/measurement/debug/vulnerability posture more broadly than needed.
- Use queues/outbox, idempotent processing, bounded retries, dead letter, timeouts, circuit breakers, and dependency/version pinning.
- Re-evaluate or revoke results when endorsement/reference/policy status changes and publish security signals to affected relying parties.
- Verify the verifier itself through operational hardening, key custody, release integrity, access control, and potentially mutual attestation in high-assurance profiles.

## 14. Stakeholder Requirements

### Technical marketing

- demonstrate challenge, evidence, appraisal, minimal result, and relying-party attenuation using synthetic evidence;
- explain attestation as scoped evidence-based appraisal, not universal trust or malware detection;
- show cross-vendor normalization while preserving vendor/profile-specific proof;
- prepare stories for HSM/KMS key provenance, passkeys, workload admission, confidential computing, device onboarding, regulated transactions, edge/IoT, and release provenance.

### Developer relations

- publish RATS vocabulary and profile-specific quickstarts for attester, verifier, and relying party;
- provide EAT/key/workload/device fixtures for valid, wrong nonce/audience/subject, replay, expired, unknown endorsement, stale reference, unsupported algorithm, debug/noncompliant, and indeterminate states;
- document result validation, caching/reuse, policy versions, reason codes, disclosure, retry, and privacy;
- provide test adapters without representing synthetic evidence as hardware assurance.

### Sales and account management

- use an assessment for subject/use case, attester technology, evidence format, verifier, endorsers/reference sources, relying parties, freshness, latency, privacy, region, policy, and response;
- deliver a readiness report separating evidence generation, verification, appraisal, result consumption, and operational governance;
- define RACI for device/platform manufacturer, cloud/KMS, customer, Tigrbl verifier, policy owner, relying party, and incident owner;
- avoid claims such as "hardware-backed," "confidential," or named assurance levels without verified profile evidence.

### GTM strategist

- package Key Assurance, Authenticator Assurance, Workload/Device Posture, Confidential Computing Verification, and Attestation Governance separately;
- prioritize key and workload/device profiles already adjacent to repository capabilities;
- pair with Certificate Center, Workload Trust, Authenticator Center, Policy Studio, Security Signals, and release certification;
- meter by managed subject, appraisal, verifier profile, reference source, result volume, retention, or governance tier without discouraging re-attestation.

### Copywriter

- distinguish claim, evidence, endorsement, reference value, validation, appraisal, result, relying-party decision, and authorization;
- use "compliant with policy X at time Y" rather than "trusted" or "secure";
- distinguish failed, noncompliant, indeterminate, stale, unsupported, and system error;
- state evidence/result purpose, audience, age, strength/profile, and disclosure;
- avoid implying that a signature proves claim truth without the attestation root/model.

## 15. Delivery Instructions

### Frontend engineer

- generate typed management/result clients; all parsing, crypto, freshness, and appraisal remain server-side;
- remove generic raw `KeyAttestationEvidence` views from unrelated UI/API paths as replacement views become available;
- never place evidence bytes, stable hardware IDs, measurements, or sensitive claims in URLs, analytics, browser logs, local storage, or notifications;
- render server-returned trust stages, claim provenance, reasons, policy/reference versions, and disclosure decisions;
- support asynchronous sessions, polling/callback status, cancellation, retry-safe actions, stale versions, and provider outages;
- instrument stage latency/outcomes with opaque IDs and safe categories.

### UIX designer

- make Evidence, validation, appraisal, result, and relying-party outcome visually distinct;
- distinguish compliance from confidence/strength and freshness;
- use progressive disclosure from fleet posture to claim/evidence internals;
- design empty, challenge issued/expired, evidence uploading/processing, invalid, replayed, stale, subject mismatch, unsupported, indeterminate, noncompliant, compliant, result expired/revoked, provider unavailable, and recovery states;
- provide accessible table/tree equivalents for composite evidence and lineage;
- meet WCAG 2.2 AA with keyboard operation, non-color state, focus management, accessible diffs/timelines, and reduced motion.

### Copywriter

- create RATS terminology, lifecycle, evidence format, validation, appraisal, reason-code, remediation, confirmation, notification, and privacy catalogs;
- write separate attester/developer, verifier operator, relying-party, and auditor language;
- reveal only remediation appropriate to the actor and avoid exposing defensive reference values;
- explain why re-attestation is needed and what changed;
- write compromised endorsement/reference source, verifier outage, mass result revocation, and false-positive recovery guidance.

## 16. Delivery Phases

### Phase 1: Key attestation correction and core model

- canonical RATS artifacts/roles, challenge/session, result, profile, policy, endorsement/reference, reason, and lineage contracts;
- purpose-built restricted key-evidence API replacing broad generic table exposure;
- one real key-provider evidence/verifier profile with adversarial fixtures;
- Attestation Center inventory/inspector and result consumer SDK.

### Phase 2: Workload/authenticator profiles

- workload/machine evidence adapter linked to Workload Trust;
- WebAuthn attestation appraisal linked to Authenticator Center;
- reference/endorsement refresh, policy simulation, result revocation, and Security Signals integration.

### Phase 3: EAT and confidential computing

- RFC 9711 EAT profile(s), media types, normalized claims, cloud TEE/provider verifiers, composite evidence, and interoperability tests;
- relying-party integrations for workload admission, secret release, token/certificate issuance, and policy attenuation.

### Phase 4: Device, supply chain, and vertical packs

- TPM/device/edge/IoT and enterprise verifier adapters;
- release/software provenance integration and specialized reference-value governance;
- finance, healthcare, government, industrial, telecom, and confidential-data profiles.

## 17. Acceptance Criteria

### API/runtime

- Evidence cannot be appraised without exact profile, valid protection/provenance, freshness, subject binding, and active policy/supporting artifacts.
- Reused, expired, wrong-tenant, wrong-subject, wrong-purpose/audience, malformed, unsupported, and unknown-critical evidence fails without result/action.
- Validation, appraisal, and relying-party decisions remain distinct statuses with linked reasons.
- Results are audience/purpose/subject/policy/version/time bound and disclose only approved claims.
- Endorsement/reference/policy changes identify and revoke/re-evaluate affected results.
- Raw evidence is immutable, encrypted/referenced, access-controlled, retention-bound, and never generically public.

### UIX

- Operators can trace every result claim to evidence, endorsement/reference, policy rule, verifier, and time.
- Users can distinguish invalid, noncompliant, indeterminate, stale, and provider failure.
- Policy/reference changes show affected subjects/results/relying parties before activation.
- Composite evidence is understandable through accessible layered views.
- Incident actions disclose result/access/credential/workload impact and recovery.

### Evidence/business

- DevRel can run positive and adversarial fixtures for each claimed profile.
- Technical marketing can demonstrate appraisal without production hardware IDs or sensitive measurements.
- Sales can produce a readiness/RACI report without raw evidence disclosure.
- RATS/EAT/hardware/vendor/assurance/interoperability claims link to profile-specific certified evidence.

## 18. Success Measures

- challenge completion, evidence validation, appraisal, and result issuance rates;
- p50/p95 time per pipeline stage and provider/source dependency;
- replay, stale, subject-binding, endorsement, reference, and policy failure rates;
- indeterminate and false-positive/override rate;
- subjects with current results by required profile/purpose;
- stale endorsement/reference/policy/result age;
- result revocation/re-evaluation propagation time;
- raw evidence access/export and retention deletion compliance;
- unauthorized acceptance, cross-tenant disclosure, or forged/replayed result incidents.

Guardrails include evidence substitution, weak freshness, false compliance, compromised reference/endorsement acceptance, cross-tenant correlation, privacy leakage, result over-disclosure, stale result use, and overstated assurance.

## 19. Source Evidence

### Repository

- `pkgs/02-contracts/tigrbl-security-trust-contracts/src/tigrbl_security_trust_contracts/keys.py`
- `pkgs/02-contracts/tigrbl-security-trust-contracts/src/tigrbl_security_trust_contracts/protocols.py`
- `pkgs/05-bases/tigrbl-security-trust-domain-bases/`
- `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/crypto_keys.py`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/key_attestation_evidence/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/machine_identity/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/workload_identity/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/release_attestation_event/`
- `pkgs/60-runtime/tigrbl-identity-author/src/tigrbl_identity_author/release_signing/attestations.py`
- API contract manifests currently exposing `KeyAttestationEvidence`;
- planned workload-attestation/verifier-trust-policy tests and evidence/certification docs.

### Standards and primary sources

- [RFC 9334: Remote ATtestation procedureS Architecture](https://www.rfc-editor.org/rfc/rfc9334)
- [RFC 9711: Entity Attestation Token](https://www.rfc-editor.org/rfc/rfc9711)
- [RFC 9782: Entity Attestation Token Media Types](https://www.rfc-editor.org/rfc/rfc9782)
- [RFC 9397: Trusted Execution Environment Provisioning Architecture](https://www.rfc-editor.org/rfc/rfc9397)
- [RFC 9683: Remote Integrity Verification of Network Devices with TPMs](https://www.rfc-editor.org/rfc/rfc9683)
- [Web Authentication Level 3](https://www.w3.org/TR/webauthn-3/)

## 20. Explicit Non-Claims

This brief does not claim that the current repository:

- implements the RATS architecture as a product or RFC 9711 EAT;
- verifies TPM, TEE, confidential-computing, device, workload, or WebAuthn attestation profiles comprehensively;
- operates a production verifier with endorsements and reference values;
- provides hardware-backed assurance merely because key evidence records exist;
- issues audience-bound normalized attestation results;
- safely exposes raw key attestation evidence through every current frontdoor;
- equates release signing evidence with runtime platform attestation.

Those claims require profile-specific evidence generation/verification, freshness and subject binding, trusted endorsements/reference values, appraisal policy, privacy controls, adversarial/interoperability tests, operational proof, and release certification.
