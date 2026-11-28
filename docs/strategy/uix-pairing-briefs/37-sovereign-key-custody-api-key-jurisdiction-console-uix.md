# Sovereign Key Custody API + Key Jurisdiction Console UIX

- **Pairing:** 37
- **Status:** Proposed product brief
- **Primary owners:** Cryptography, platform security, authorization, sovereignty, frontend, UIX, product copy
- **Adjacent pairings:** Sovereignty Policy API; Jurisdiction-Aware Authorization API; Policy Obligation API

## 1. Product decision

Build a Sovereign Key Custody API and Key Jurisdiction Console UIX that constrain and prove where cryptographic keys are generated, held, used, backed up, recovered, administered, and destroyed—and which organizations, operators, services, and authorization quorums can control each operation.

Data location alone is not a sufficient sovereignty control. If an out-of-bound control plane, operator, provider, recovery process, or wrapping key can decrypt or sign, the effective control boundary extends to it.

The product must expose verifiable facts and enforce approved custody policy. It must not claim that an HSM, customer-managed key, or configured region automatically guarantees legal or operational sovereignty.

## 2. Product boundary

This pairing governs cryptographic key custody and use across encryption, signing, authentication, certificate issuance, token issuance, wrapping, derivation, and recovery.

It is distinct from:

- general key inventory and cryptographic implementation;
- certificate lifecycle management;
- regional data placement;
- legal determination of jurisdiction or compliance;
- secret leasing and credential brokering;
- ordinary key rotation scheduling.

It integrates those surfaces by supplying typed custody constraints, authorization decisions, obligations, and evidence.

## 3. Repository starting point

The repository already contains substantial foundations:

- provider-neutral key contracts for kinds, usages, operations, origins, versions, export, derivation, wrapping, and signing;
- durable `crypto_keys` and `crypto_key_versions` with tenant/realm ownership, provider references, allowed operations, origin, extractability, export policy, fingerprints, validity, and lifecycle state;
- durable key envelopes and wrapping-key references;
- durable key-attestation evidence and principal-key bindings;
- versioned key-rotation policies, approval/publish/supersede lifecycle, rotation events, audit evidence, and policy-bound execution;
- signing-provider and trust-domain abstractions, including post-quantum signing support;
- response hooks that scrub key material and tests that preserve provider/runtime boundaries.

Current gaps:

- provider and region are not a typed custody topology;
- no canonical jurisdiction, facility/module, controlling organization, operator, quorum, recovery custodian, or subprocessor model;
- no policy engine validates generation/use/wrapping/backup/recovery/destruction against a sovereign boundary;
- no durable custody decision and per-operation enforcement receipt;
- attestation evidence is not assembled into continuous custody verification;
- opaque `key_metadata` cannot safely substitute for typed, queryable policy fields;
- no dependency closure from a data key through wrapping keys, root keys, modules, control planes, backups, and recovery paths;
- no Key Jurisdiction Console exists.

## 4. Users and jobs to be done

### Cryptography and platform security teams

Define custody profiles, bind keys to approved providers/modules, verify attestation, govern lifecycle operations, investigate drift, and rotate or quarantine affected keys.

### Sovereignty and privacy teams

Confirm that technical custody facts match approved boundaries and retrieve evidence without receiving key material or unrestricted cryptographic authority.

### Application and identity teams

Request policy-compliant signing, decryption, derivation, wrapping, or certificate operations without coupling applications to provider-specific controls.

### Tenant administrators

Choose entitled custody profiles, bring or control keys where supported, approve sensitive operations, and understand service/recovery tradeoffs.

### Incident responders and auditors

Trace every sensitive key operation, detect custody-boundary violations, revoke authority, and reconstruct compromise or recovery events.

## 5. Core domain model

Introduce typed, versioned resources:

- `CustodyBoundary`: permitted jurisdictions, providers, organizations, module classes, control planes, operator constraints, recovery locations, and evidence requirements.
- `CustodyProfile`: reusable control objective for a key class/use, tenant entitlement, lifecycle, and failure mode.
- `CryptographicModule`: provider, service, module/facility identity, region/jurisdiction, validation claims, attestation identity, ownership, and status.
- `CustodyPrincipal`: provider operator, customer operator, service workload, recovery custodian, approver, or auditor with organization and jurisdiction facts.
- `KeyCustodyBinding`: key/version, module, boundary/profile version, tenant/realm, effective interval, and state.
- `KeyDependencyEdge`: data key, wrapping key, KEK, root, derived key, replica, backup, escrow share, or recovery material relationship.
- `KeyOperationRequest`: operation, key/version, purpose, workload, data/resource, requested module, actor, context, and idempotency key.
- `CustodyDecision`: result, exact boundary/profile, dependency closure, reasons, obligations, evidence state, and correlation ID.
- `KeyOperationReceipt`: provider/module response, actual location, key version, authorization, quorum, attestation, outcome, and integrity proof.
- `CustodyEvidence`: attestation, configuration, provider statement, module validation, access log, inventory observation, or destruction proof with freshness.
- `RecoveryPlan`: shares/custodians, locations, quorum, rehearsal, restore target, approvals, and expiry.
- `CustodyException`: narrow scope, risk, compensating controls, authority, expiry, and revocation.

The API stores references and protected metadata, not plaintext private or secret key material.

## 6. Custody policy dimensions

Policies should constrain:

- generation, import, derivation, wrapping, unwrapping, use, backup, restore, replication, export, archival, suspension, revocation, and destruction;
- physical/cloud region, jurisdiction, facility, provider, service tier, and module identity;
- provider-managed, customer-managed, customer-supplied, external/HYOK, split, or threshold control model;
- key kind, algorithm, usage, allowed operations, cryptoperiod, and extractability;
- tenant, realm, workload, data class, purpose, issuer, certificate profile, and relying service;
- operator organization, jurisdiction, assurance, session provenance, and just-in-time authority;
- single-party, dual-control, quorum, split-knowledge, and separation-of-duty requirements;
- wrapping/root-key ancestry, recovery/backup paths, and disaster mode;
- required attestation type, validation claim, observation freshness, and receipt assurance.

Rules must be typed and testable. Marketing labels such as “sovereign HSM” cannot be policy inputs.

## 7. Custody topology and dependency closure

The effective boundary includes every component able to enable a protected operation:

- active and previous key versions;
- replicas and provider-internal copies;
- wrapping and root keys;
- encrypted backups and their recovery keys;
- escrow or threshold shares and custodians;
- control-plane identities and privileged support paths;
- cryptographic modules, firmware, APIs, and provider organizations;
- caches, export artifacts, and migration intermediates.

The API must evaluate the complete known dependency graph and identify its weakest or unknown node. A regional data-encryption key is not verified sovereign if its wrapping root or recovery quorum is outside the boundary.

## 8. Key lifecycle requirements

### Generation and import

Pre-authorize algorithm, origin, module, location, entropy/attestation requirements, ownership, and exportability. Import ceremonies require provenance, wrapping protection, operator quorum, and deletion/retention evidence for staging material.

### Activation and use

Bind each operation to an active key version, exact purpose, workload identity, module, location, authorization, and custody receipt. Provider fallback cannot silently select another region or control model.

### Rotation and migration

Extend existing rotation policy with custody-safe destination validation, wrapping ancestry, re-encryption/re-signing impact, overlap rules, rollback constraints, and proof that retired material is no longer usable outside policy.

### Backup and recovery

Treat recovery as a distinct high-risk path. Validate location, shares, custodians, quorum, target module, rehearsal freshness, emergency authorization, and post-recovery reconciliation.

### Revocation, compromise, and destruction

Propagate impact through dependent keys, tokens, certificates, ciphertext, signatures, and services. Destruction status must distinguish requested, provider-acknowledged, cryptographically erased, independently evidenced, and unverifiable.

## 9. Control models and quorum

Support explicit control modes rather than a single `customer_managed` flag:

- provider-controlled;
- provider-operated/customer-authorized;
- customer-controlled in provider module;
- external/HYOK;
- dual-control across customer and provider;
- threshold or multi-party control;
- offline/root ceremony;
- recovery-only custody.

Quorum policy defines eligible principals, distinct organizations/roles, minimum approvals, expiry, request binding, and anti-replay behavior. Approval is not the cryptographic operation itself; the receipt must prove what actually executed.

## 10. Attestation and evidence

Evidence should cover module identity and state, key generation/import origin, non-extractability, firmware/configuration, location observation, provider service configuration, operator session, quorum, wrapping ancestry, backup/recovery, and destruction.

Each item carries issuer, subject, scope, collection time, validity, trust chain, integrity status, confidence, and expiry. Appraisal policy determines whether it is accepted. A provider assertion and hardware-backed attestation must remain visibly distinct.

Use **declared**, **configured**, **observed**, and **verified** states. Absence of export events is not proof of non-exportability, and a certificate or module validation is not proof of correct deployment.

## 11. Runtime authorization and enforcement

Evaluation receives tenant/realm, actor/workload, operation, key/version, usage/purpose, data/resource, requested and observed module/location, dependency graph, quorum state, and evidence. It returns:

- `allow`, `deny`, `conditional`, or `indeterminate`;
- stable reason codes and safe explanations;
- boundary, profile, policy, and key versions;
- dependency and evidence gaps;
- obligations such as module pinning, quorum, fresh attestation, local operator, or receipt requirement;
- approved provider/module and failover set;
- correlation and provenance IDs.

Enforcement must occur server-side at the provider adapter or broker boundary. The provider's actual module, region, key version, and result are checked against the decision and captured in a receipt.

## 12. API surface

Recommended resources:

- `/key-custody/boundaries`
- `/key-custody/profiles` and `/versions`
- `/key-custody/modules`
- `/key-custody/principals`
- `/key-custody/bindings`
- `/key-custody/dependencies`
- `/key-custody/evaluations` and `/decisions`
- `/key-custody/operations` and `/receipts`
- `/key-custody/evidence` and `/attestations`
- `/key-custody/recovery-plans` and `/ceremonies`
- `/key-custody/drift`
- `/key-custody/exceptions`
- `/key-custody/impact-analyses`

Support idempotency, optimistic concurrency, dry-run simulation, bulk impact, event subscriptions, stable reason codes, effective-time queries, and scoped evidence export. Separate policy administration, key operation, approval, evidence access, audit, and emergency permissions.

Existing `CryptoKey`, `CryptoKeyVersion`, envelope, attestation, and rotation resources remain canonical inputs. Add compatible bindings instead of duplicating or silently replacing them.

## 13. Key Jurisdiction Console UIX

### Custody portfolio

Show keys by tenant, realm, use, provider/module, jurisdiction, custody model, verification state, rotation posture, evidence freshness, recovery readiness, exceptions, and drift. Never expose private material or full sensitive provider references.

### Boundary and profile composer

Guide users through permitted modules/locations, control model, operator constraints, quorum, recovery, export, evidence, and outage behavior. Validate contradictions and simulate affected keys before activation.

### Custody topology

Visualize key versions, modules, wrapping/root ancestry, replicas, backups, shares, custodians, and consumers. Highlight out-of-bound, stale, and unknown dependencies. Provide an accessible table equivalent.

### Operation and receipt explorer

Search generation, import, signing, decryption, wrapping, rotation, recovery, and destruction by correlation ID, key, tenant, principal, module, location, result, or reason. Reconstruct authorization, approvals, provider response, attestation, and enforcement receipt.

### Rotation and migration planner

Compare source/destination custody, cryptographic compatibility, dependent assets, overlap, rollback, outage risk, and re-encryption/re-signing work. Require a verified destination before moving authority.

### Recovery ceremony workspace

Coordinate eligible custodians, share/quorum state, target module/location, approvals, rehearsal, break-glass rules, and post-ceremony evidence without displaying secret shares.

### Drift and evidence center

Compare declared, configured, observed, and verified state. Group issues by root module, root/wrapping key, provider, or operator path; show affected dependents and safe remediation.

## 14. Security, privacy, and reliability

- Never log, render, export, or retain plaintext private/secret key material.
- Redact provider references, attestation internals, operator facts, and topology by role.
- Tenant-isolate keys, bindings, evidence, decisions, approvals, and receipts.
- Require phishing-resistant authentication and just-in-time authorization for high-risk operations.
- Enforce separation of duties and organization-aware quorum server-side.
- Integrity-protect policies, approvals, attestations, receipts, and destruction evidence.
- Prevent replay, confused-deputy use, version substitution, provider fallback, quorum reuse, and exception widening.
- Define evaluator/provider outage behavior; do not silently reroute to a non-approved module.
- Test concurrency, partial provider failure, rollback, stale attestation, compromised wrapping roots, and recovery emergencies.

## 15. Instructions by delivery team

### Frontend engineer

Build reusable custody state, key/module badges, dependency graph/table, evidence freshness, quorum progress, operation timeline, receipt, policy diff, impact, rotation, and recovery components. Use server-issued capabilities for every mutation. Ensure secrets never enter browser analytics, error telemetry, URLs, or clipboard helpers.

### UIX designer

Design around control ownership and verifiable state, not vendor branding. Make primary, wrapping, root, backup, and recovery relationships understandable. Test routine rotation, BYOK/HYOK onboarding, failed quorum, provider drift, compromise, and regional outage journeys. Provide keyboard and screen-reader alternatives to topology views.

### Copywriter

Use “key operation verified in,” “customer-authorized,” “provider-operated,” “evidence stale,” and “recovery path unverified.” Avoid “customer has exclusive control,” “keys never leave,” “sovereign encryption,” or compliance claims unless precise evidence and approved qualification support them.

### Backend and cryptography engineers

Extend canonical contracts with typed custody resources, provider adapters, dependency closure, policy evaluation, quorum binding, operation receipts, and evidence appraisal. Preserve scrubbing and provider-neutral boundaries. Add migrations and adversarial tests without implementing cryptography in UI or policy layers.

## 16. Stakeholder enablement

- **Technical marketing:** demonstrate a key hierarchy with an out-of-bound recovery dependency, blocked operation, remediated binding, and signed receipt using synthetic keys.
- **Developer relations:** provide provider-adapter contracts, local fake HSM/KMS, custody profile examples, operation/receipt schemas, failure scenarios, and BYOK/HYOK integration guides.
- **Sales and account management:** maintain provider/region/control-model matrices, customer ceremony requirements, recovery constraints, evidence levels, shared responsibilities, and lead times.
- **GTM strategy:** package standard managed custody separately from customer-controlled keys, external/HYOK, dual/threshold control, continuous attestation, and sovereign recovery.
- **Copywriting:** maintain approved custody terminology, claim substantiation requirements, vendor-neutral comparisons, and incident/recovery messaging.

## 17. Delivery phases

### Phase 1 — Typed custody foundation

Add boundaries, profiles, modules, bindings, operation decisions, receipts, and console inventory on top of existing key/version/rotation tables.

### Phase 2 — Dependency and assurance

Add wrapping/root/recovery topology, evidence appraisal, drift, quorum, provider enforcement adapters, simulation, and impact analysis.

### Phase 3 — Advanced sovereign operations

Add BYOK/HYOK ceremonies, multi-party control, provider migration, continuous attestation, sovereign failover/recovery, and tenant evidence bundles.

## 18. Acceptance criteria

- Every protected key version has an explicit custody binding or is marked ungoverned.
- Generation, import, use, wrapping, rotation, backup, recovery, export, and destruction are independently constrainable.
- Evaluations cover known wrapping, root, replica, backup, escrow, operator, and recovery dependencies.
- Unknown or stale required evidence cannot appear verified.
- Provider/module/location fallback cannot occur outside an approved set.
- Quorum approvals are distinct, request-bound, time-limited, non-replayable, and confirmed by an operation receipt.
- Every sensitive operation is reconstructable from policy, decision, authorization, actual provider/module, key version, and outcome.
- Rotation and migration validate destination custody and dependent-asset impact before activation.
- Recovery and destruction have explicit states and evidence, not boolean completion flags.
- Existing provider-neutral key and rotation behavior remains compatible and regression-tested.
- UIX meets keyboard, screen-reader, responsive, localization, and color-independent status requirements.
- Tenant isolation, redaction, replay, version substitution, stale evidence, dependency, concurrency, outage, and performance tests pass.

## 19. Success measures

- percentage of key versions with verified custody and complete dependency closure;
- percentage of sensitive operations with matching authorization and receipt;
- out-of-bound operation attempts prevented;
- unknown, stale, and drifted custody dependency rate;
- rotation and migration completion with verified destination evidence;
- recovery rehearsal freshness and successful policy-constrained recovery rate;
- exception count, age, and recurrence;
- time to contain a compromised module, root, operator, or provider;
- time to answer a tenant custody inquiry with a scoped evidence bundle.

These indicate operational assurance, not legal compliance or absolute control.

## 20. Authoritative design references

- [NIST SP 800-57 Part 1 Rev. 5, Recommendation for Key Management](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
- [NIST SP 800-130, Framework for Cryptographic Key Management Systems](https://csrc.nist.gov/pubs/sp/800/130/final)
- [FIPS 140-3, Security Requirements for Cryptographic Modules](https://csrc.nist.gov/pubs/fips/140-3/final)
- [NIST Cryptographic Key Management Systems project](https://csrc.nist.gov/Projects/key-management/cryptographic-key-management-systems)

Standards inform system and evidence design. Validation claims must name exact module, certificate, configuration, version, and scope; a product family label is insufficient.

## 21. Non-claims and dependencies

Do not claim that this product proves exclusive control, prevents every compelled-access scenario, makes cryptography infallible, validates a module, or certifies sovereignty/compliance. Outcomes depend on provider architecture, module and firmware state, operational practice, key hierarchy, operator authority, recovery design, accurate evidence, and legal interpretation.

Dependencies include canonical key/version/envelope/attestation and rotation services, provider adapters, strong authentication, authorization/delegation provenance, policy obligations and receipts, sovereignty boundaries, jurisdiction-aware policy, privileged session provenance, incident response, certificate/token services, and data-key consumer inventory.
