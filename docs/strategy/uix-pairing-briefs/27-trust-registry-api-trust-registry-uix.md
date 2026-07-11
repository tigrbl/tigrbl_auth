# Trust Registry API + Trust Registry UIX Requirements Brief

**Pairing:** `tigrbl-auth-api-trust-registry` + `@tigrbl-auth/trust-registry-uix`  
**Opportunity-map item:** 17  
**Primary buyers:** ecosystem operators, governments, healthcare exchanges, education consortia, supply-chain networks, and open-finance programs  
**Status:** proposed shared governance surface; federation, credential, certificate, attestation, policy, and residency foundations exist

## 1. Product Decision

Build a versioned, evidence-backed registry that tells ecosystem participants:

- which organizations and technical entities are recognized;
- which roles they are authorized to perform;
- which credential, certificate, schema, status, algorithm, and protocol profiles are permitted;
- under which jurisdiction, purpose, assurance, and time constraints that authorization applies;
- which authority made the determination and from what evidence;
- when trust changed, why it changed, and how consumers learned of the change.

The registry must answer a scoped question, not declare that an entity is universally “trusted.” A correct decision looks like:

> Issuer A was authorized by Framework F to issue Credential Type C for Purpose P in Jurisdiction J at Time T under Profile Version V.

The API serves governance and machine resolution. The UIX supports operators, authorities, participants, auditors, integrators, issuers, verifiers, and relying parties.

## 2. Current Repository Reality

The repository has strong adjacent building blocks:

- OpenID Federation entity statements, trust anchors, trust chains, metadata policy, trust marks, and graph direction;
- issuer, wallet, and verifier requirements that explicitly depend on scoped trust resolution;
- credential types, schemas, formats, status mechanisms, signing keys, and verification-policy concepts;
- certificate authorities, chains, roots/intermediates, profiles, revocation, and trust-store direction;
- attestation trust anchors, endorsers, reference values, appraisal policies, and evidence provenance;
- JOSE algorithm policy, key rotation, JWKS caching, OAuth/OIDC metadata, and token verification;
- residency zones and jurisdiction fields;
- policy decisions, delegation, audit events, and security signals.

What is missing is one canonical product surface that composes these facts into governed, point-in-time trust decisions. There is no dedicated trust-registry API/UIX, normalized framework/member/authority mandate, publication/subscription model, approval workflow, or cross-profile resolution contract.

The registry must reuse specialized owners. It must not duplicate private keys, issue credentials, validate presentations, operate certificate authorities, or reimplement federation protocols.

## 3. Users and Jobs

### Ecosystem or framework operator

- Define the framework, governance authorities, roles, profiles, and change controls.
- Onboard, suspend, reinstate, and remove participants.
- Publish authoritative machine-readable snapshots and urgent deltas.
- demonstrate exactly what was accepted at any historical time.

### Accreditation, supervisory, or scheme authority

- Evaluate participant evidence and grant a bounded mandate.
- issue, renew, suspend, or withdraw certifications and trust marks.
- delegate limited authority while preserving the authority chain.

### Participant administrator

- Register organization and technical endpoints.
- Submit evidence, keys, certificates, credential types, and status services.
- Track reviews, findings, expirations, and required changes.

### Issuer, verifier, wallet, or relying-party engineer

- Resolve whether a counterparty is authorized for a precise transaction.
- Download signed, pinned registry data for online or offline use.
- Handle key rollover, stale data, suspension, and conflicting sources safely.

### Auditor and incident responder

- Reconstruct a resolution with its source snapshot, rules, chain, and evidence.
- Find every consumer and authorization affected by a compromise or withdrawal.

### Public or ecosystem viewer

- Confirm published participation and scope without viewing private evidence or operational details.

## 4. Architectural Ownership

### Trust Registry API owns

- trust frameworks and governance versions;
- organizations, technical entities, roles, mandates, memberships, and authority delegation;
- recognized credential/certificate/schema/status/protocol/algorithm profiles;
- scoped authorization statements and trust-mark references;
- source ingestion, normalization, provenance, approval, publication, and supersession;
- point-in-time trust resolution and explainable decision receipts;
- signed snapshots, deltas, subscriptions, and consumer freshness policy;
- registry evidence, incidents, and impact analysis.

### Specialized products retain ownership

- Federation Trust API: OpenID Federation discovery, entity statements, chains, metadata policy, and automatic registration.
- Credential Issuer API: credential configuration and issuance.
- Verification API: cryptographic, status, holder-binding, presentation, and transaction verification.
- Certificate Lifecycle API: CA, issuance, chain, OCSP/CRL, and certificate operations.
- Attestation API: evidence verification and appraisal.
- Security Signals API: event transport and risk/status coordination.
- Policy engine: local allow/deny composition beyond registry facts.
- JOSE/crypto packages: signature and algorithm enforcement.

### Boundary rules

- Registry inclusion is evidence for policy, not automatic authorization for every transaction.
- Cryptographic validity does not prove ecosystem authorization.
- A trust anchor is configured through an out-of-band governance decision; discovery cannot establish its own root.
- The registry stores public verification material and protected governance evidence, never participant private keys.
- Local consumers may impose stricter policy than the framework; they may not silently weaken mandatory framework constraints.

## 5. Trust Framework Model

A framework requires:

- stable identifier, human name, operator, owner, and public description;
- legal/governance basis and authoritative-source references;
- jurisdiction and sector;
- supported participant roles;
- assurance levels and interpretation;
- accepted protocols, credential/certificate formats, algorithms, schemas, and status mechanisms;
- membership, accreditation, suspension, appeal, and termination rules;
- authority delegation model;
- privacy, retention, incident, and disclosure policy;
- publication, signature, snapshot, delta, and freshness policy;
- semantic version, effective interval, status, and supersession chain.

Framework changes must be versioned and have explicit transition rules. A new version cannot retroactively rewrite prior authorization.

## 6. Participant and Technical Entity Model

Separate the legal organization from its technical entities.

### Organization

- legal and display names, identifiers, jurisdiction, and contacts;
- framework memberships and roles;
- owner and authorized administrators;
- accreditation evidence and decisions;
- lifecycle and incident state.

### Technical entity

- entity ID or canonical endpoint identifier;
- organization and operational owner;
- role: issuer, verifier, wallet provider, relying party, authority, status provider, trust-mark issuer, CA, attester, or other profiled role;
- metadata/discovery endpoints;
- keys, certificates, trust chains, and rollover windows;
- supported protocol/profile versions;
- credential types, schemas, status services, and algorithms;
- environment, jurisdiction, and effective interval;
- provenance and last verification.

One organization may operate many technical entities. A compromised endpoint must be suspendable without falsely withdrawing unrelated organizational roles.

## 7. Mandates, Membership, and Authority

A mandate is a bounded authorization from an authority to an organization or technical entity.

Required scope:

- grantor authority and authority-chain proof;
- grantee organization/entity;
- participant role;
- credential, certificate, schema, service, or trust-mark types;
- purpose, jurisdiction, population, environment, and assurance constraints;
- effective and expiry times;
- evidence, decision, approvers, and policy version;
- delegation permission and maximum depth;
- status: proposed, active, suspended, expired, withdrawn, superseded;
- reason and incident references for state changes.

The registry must reject circular, over-broad, expired, or unauthorized delegation. Suspending a parent authority must produce explicit impact analysis rather than blindly deleting descendants.

## 8. Credential Types and Schemas

For each recognized credential type, record:

- canonical type/configuration identifiers and aliases;
- business purpose, subject population, issuer roles, and verifier use;
- supported formats and proof suites;
- schema, context, vocabulary, claim definitions, cardinality, and sensitivity;
- required/optional/forbidden claims;
- holder/key binding and assurance requirements;
- validity and refresh rules;
- accepted status mechanisms and freshness policy;
- selective-disclosure and correlation considerations;
- rendering/branding references that are clearly non-authoritative;
- jurisdiction/profile constraints;
- version, integrity digest, lifecycle, and supersession.

Schemas must be content-addressed or integrity-bound. Dereferencing a mutable URL without pinning is insufficient for historical validation.

## 9. Certificates, Keys, and Trust Anchors

The registry may publish and govern:

- approved root/intermediate certificates and usage constraints;
- issuer/entity verification keys and JWKS references;
- signing, encryption, federation, status, and attestation key purposes;
- certificate policies/profiles and name constraints;
- algorithm, key-size, curve, and transition policy;
- rollover overlap and emergency replacement;
- OCSP, CRL, status-list, and compromise information;
- source and out-of-band anchor approval evidence.

Trust anchors must be scoped by framework, role, use, profile, jurisdiction, and effective time. “Present in registry” must never mean “valid for every TLS, document, credential, or federation purpose.”

## 10. Status Mechanisms

The registry identifies permitted status methods and providers; it does not replace their real-time responses.

Record:

- mechanism/profile and version;
- provider/authority and endpoint metadata;
- credential or certificate types served;
- status purposes supported;
- update interval and maximum acceptable age;
- cache/offline behavior;
- privacy and correlation properties;
- failure semantics: fail closed, fail open, unknown, or risk-based by use case;
- signing keys/certificates and rollover;
- incident and deprecation state.

W3C VC 2.0 warns that status mechanisms must not enable tracking such as issuer “phone home.” Registry profiles must assess and disclose this privacy property.

## 11. Algorithms and Protocol Profiles

Algorithm policy must identify:

- operation: signing, verification, encryption, key agreement, hashing, or proof;
- protocol/format/profile and participant role;
- allowed, preferred, deprecated, forbidden, and emergency-only states;
- minimum key/parameter requirements;
- effective dates and migration deadlines;
- verification-only grace periods;
- jurisdiction or assurance constraints;
- source standard and policy rationale.

Protocol profiles bundle interoperable requirements for endpoints, metadata, keys, algorithms, credential formats, status, assurance, and tests. Profiles are immutable once published; new versions supersede them.

## 12. Source Ingestion and Provenance

Support authoritative sources including:

- operator-managed records;
- OpenID Federation entity statements and trust marks;
- signed trust lists and government lists;
- certificate trust lists and PKI repositories;
- schema/type repositories;
- accreditation/certification systems;
- approved partner registries.

Every ingested fact includes source URI/identifier, source authority, retrieval time, source effective time, signature/integrity result, parser/profile version, raw-object digest, normalization version, and approval state.

Source priority and conflict rules must be explicit. The UIX must show conflicting facts and prevent silent last-write-wins resolution.

## 13. Publication and Distribution

Publish:

- current signed snapshot;
- immutable historical snapshots;
- ordered signed deltas;
- entity/type/profile-specific resolution endpoints;
- machine-readable status and freshness metadata;
- public transparency view with protected fields removed;
- subscription/security-event channels for urgent changes.

Each snapshot requires framework ID/version, sequence, issued/effective/next-update times, schema version, content digest, signing key ID, previous snapshot digest, and signature.

Consumers must pin acceptable registry authorities and verify signature, sequence, effective time, and freshness. Rollback, freeze, equivocation, split-view, and missed-delta detection are required. Consider append-only transparency logs and independent monitors for high-assurance deployments.

## 14. Trust Resolution API

A resolution request includes:

- framework and local policy profile;
- subject organization/entity/issuer/key/certificate;
- asserted role;
- credential/certificate/schema/status/protocol type;
- purpose, jurisdiction, assurance, audience, and transaction time;
- consumer snapshot/freshness constraints.

The response returns:

- `authorized`, `not_authorized`, `indeterminate`, or `stale`—never an ambiguous boolean;
- exact scope that matched or failed;
- framework/profile/snapshot versions;
- authority and mandate chain;
- technical entity/key/certificate match;
- credential/schema/status/algorithm compatibility;
- effective-time and freshness evaluation;
- warnings, conflicts, deprecations, and incident state;
- decision trace and portable receipt digest;
- source references safe for the caller.

The resolver must distinguish missing evidence from negative evidence. Consumers define how `indeterminate` and `stale` affect their transaction.

## 15. Management API Requirements

Provide versioned endpoints for:

- `/frameworks`, versions, profiles, and publication policy;
- `/organizations`, administrators, evidence, and memberships;
- `/entities`, metadata, endpoints, keys, certificates, and role claims;
- `/authorities`, delegations, and mandates;
- `/credential-types`, schemas, formats, and status policies;
- `/trust-anchors`, keys, certificates, and rollover;
- `/algorithms` and `/protocol-profiles`;
- `/sources`, ingestion jobs, conflicts, and provenance;
- `/proposals`, review, approval, publication, suspension, withdrawal, and appeal;
- `/snapshots`, deltas, subscriptions, and transparency proofs;
- `/resolve`, batch resolution, and historical reconstruction;
- `/incidents`, impact analysis, notifications, and recovery;
- `/evidence-bundles` and public records.

Mutations require scoped authority, separation of duties, optimistic concurrency, idempotency, immutable decision records, and audit correlation. Bulk imports are staged, validated, diffed, approved, and atomically published.

## 16. Trust Registry UIX

### Registry overview

Show framework/version, publication freshness, active organizations/entities by role, expiring mandates/keys/certificates, source health, unresolved conflicts, pending proposals, incidents, deprecated algorithms, and consumer delivery health.

### Ecosystem explorer

Provide searchable organization, entity, authority, role, credential type, schema, profile, and jurisdiction views. Use a graph only as an optional explanation; every relationship must also be accessible in tables and detail pages.

### Participant onboarding

Guide legal identity, administrators, requested roles, technical entities, endpoints, keys/certificates, types, evidence, authority review, interoperability tests, approval, and publication. Clearly separate saved draft, submitted claim, verified evidence, approved mandate, and published record.

### Mandate and authority workbench

Show grantor chain, precise scope, dates, delegation, evidence, approvers, conflicts, descendants, and change impact. Suspension and withdrawal require preview of affected entities, types, consumers, and active incidents.

### Credential/profile catalog

Display business purpose, formats, schemas, claims, privacy, status, algorithms, issuer/verifier roles, versions, conformance assets, and lifecycle. Provide semantic and machine-readable diffs.

### Source and conflict center

Show retrieval/signature/freshness, normalized changes, source authority, conflicts, parser errors, quarantine, and approval. Operators must never resolve conflicts without a recorded rationale.

### Trust resolution workbench

Allow an engineer to enter transaction context and see a step-by-step scoped result: authority, mandate, entity/key, type/schema, status, algorithm, time, jurisdiction, and freshness. Provide sample API request and signed receipt.

### Publication and incident center

Preview snapshot/delta changes, signatures, sequence, rollout, subscriber delivery, and rollback constraints. Incident workflows support suspension, impact analysis, urgent publication, notifications, recovery criteria, and post-incident evidence.

### Public registry

Provide accessible public search for explicitly public framework, organization, role, type, status, and effective-date facts. Do not expose protected evidence, contacts, security architecture, or unpublished incidents.

## 17. Security, Privacy, and Reliability

- Enforce tenant/framework isolation and distinguish public, participant, authority, operator, auditor, and security-response views.
- Separate proposal, evidence verification, approval, publication, signing-key custody, and audit authority.
- Require strong authentication and step-up for anchor, authority, algorithm, suspension, withdrawal, and publication changes.
- Store private evidence separately from public registry records with purpose-bound access and retention.
- Never store participant private keys; protect registry signing keys in HSM/KMS or external signers.
- Verify all external signatures, chains, content types, sizes, redirects, schemas, and endpoints before ingestion.
- Defend ingestion against SSRF, parser bombs, malicious archives, schema recursion, and resource exhaustion.
- Use canonical serialization and domain-separated signatures for snapshots/deltas/receipts.
- Detect stale data, rollback, equivocation, missed sequence, and clock anomalies.
- Support multi-region read availability without allowing split-brain publication.
- Fail safely: unavailable or stale registry data yields an explicit state, never implicit trust.
- Minimize correlation and avoid per-holder status/query telemetry in registry analytics.
- Meet WCAG 2.2 AA for public and administrative interfaces.

## 18. Governance and Change Control

High-impact changes require proposal, validation, independent review, approval, scheduled effective time, publication, notification, and verification.

At minimum, dual control applies to:

- trust anchors and registry signing keys;
- authority creation/delegation;
- participant mandate approval;
- algorithm/profile changes;
- suspension, withdrawal, and emergency reinstatement;
- source-priority/conflict policy;
- historical correction.

Corrections are append-only supersessions. Emergency changes may shorten the workflow only under explicit policy and must receive retrospective review.

## 19. Stakeholder Requirements

### Technical marketing

Demonstrate onboarding, scoped authorization, key rollover, historical resolution, suspension impact, urgent signed delta, and verifier consumption. Explain why signature validity, registry recognition, and transaction authorization are distinct.

### Developer relations

Deliver resolver SDKs, signed snapshot/delta verification, offline cache guidance, OpenID Federation adapters, credential-verifier integration, certificate/trust-list import examples, webhook/Shared Signals examples, conformance fixtures, and stale/conflict/rollback failure cases.

### Sales and account management

Provide discovery for framework governance, authorities, participant roles, jurisdiction, credential/certificate types, protocols, source lists, publication scale, freshness, offline needs, evidence sensitivity, legal basis, and incident response. Clearly map native capabilities, adapters, and customer governance responsibilities.

### GTM strategist

Package by ecosystem outcome: credential issuer authorization, verifier/relying-party registration, federation membership, certificate/trust-service lists, or supply-chain authority. Avoid selling a generic “global trust network”; adoption depends on recognized governance authority and participant agreements.

### Copywriter

Use `recognized`, `authorized for`, `mandate`, `authority`, `effective`, `suspended`, `withdrawn`, `stale`, and `indeterminate` precisely. Avoid an unqualified “trusted,” “certified,” “approved,” “compliant,” or “official.” Every label should expose who decided, for what scope, and when.

## 20. Delivery Instructions

### Frontend engineer

- Generate typed clients and preserve framework/snapshot/time context throughout navigation.
- Implement server-side pagination, filtering, graph traversal bounds, and large-import jobs.
- Build semantic diffs for records and machine payloads.
- Require preview and explicit confirmation for publication and incident changes.
- Display provenance, signature, freshness, and scope on every trust-sensitive record.
- Implement public/private field projection from server authorization, not UI hiding.
- Provide accessible table alternatives for all graphs and timelines.

### UIX designer

- Establish a visual grammar for claim, evidence, verification, mandate, publication, suspension, expiry, and source freshness.
- Make organization versus technical entity and cryptographic validity versus scoped authorization unmistakable.
- Design conflict, stale, missing, degraded, partial-source, superseded, and emergency states.
- Optimize resolution explanation for engineers while keeping public records understandable.
- Design high-impact workflows around change impact, not merely confirmation dialogs.

### Copywriter

- Create a controlled trust/governance glossary shared with issuer, wallet, verifier, federation, certificate, and attestation products.
- Write state-specific explanations and remediation guidance.
- Express scope and evidence limitations near conclusions.
- Avoid legal conclusions unless customer-approved jurisdictional language is supplied.

## 21. Delivery Phases

### Phase 1: Canonical registry and resolver

- framework, organization, entity, role, mandate, profile, and source contracts;
- proposal/approval/publication workflow;
- signed snapshots and point-in-time resolver;
- operator UIX, public registry, audit, and one credential ecosystem profile.

### Phase 2: Credential and federation integration

- credential types, schemas, formats, status, algorithms, and issuer/verifier adapters;
- OpenID Federation entity/trust-mark ingestion;
- resolver SDKs, offline cache, deltas, and subscriptions;
- key/certificate rollover and incident suspension.

### Phase 3: Multi-authority and high assurance

- delegated authority, cross-registry imports, conflict resolution, appeals;
- certificate/trusted-list adapters and transparency monitoring;
- HSM signing, multi-region read scale, evidence profiles, regulated retention.

### Phase 4: Vertical packs

- government/eID, healthcare, education, open finance, supply chain, and communications profiles;
- jurisdiction-specific governance templates and conformance suites;
- partner registry federation only after authority and conflict semantics are proven.

## 22. Acceptance Criteria

### API and trust semantics

- Resolution requires framework, role/type/purpose/jurisdiction/time context and never returns a context-free trust boolean.
- Every positive result traces to an active mandate and valid authority chain.
- Missing, negative, stale, conflicting, suspended, and expired evidence produce distinct outcomes.
- Historical resolution uses immutable versions and reproduces the prior result.
- Trust anchors are explicitly configured and scoped; discovery cannot self-bootstrap trust.
- Snapshots/deltas are signed, sequenced, integrity-linked, and rollback-resistant.
- Key/algorithm/profile rollover supports bounded overlap and deterministic effective times.
- Source provenance and conflict decisions are durable and auditable.
- Public responses exclude protected evidence and operational data.
- Cross-framework and cross-tenant access boundaries are tested.

### UIX

- Operators can onboard and publish a participant without confusing claims with approvals.
- Consumers can reproduce a trust resolution from the UIX and API example.
- Source conflicts and stale information cannot appear as healthy/authorized.
- Suspension preview identifies affected mandates, entities, types, and consumers.
- Every graph has an accessible table/detail representation.
- Core administrative and public workflows meet WCAG 2.2 AA.

### Evidence and business

- Reference fixtures prove onboarding, denial, expiry, rollover, suspension, withdrawal, reinstatement, source conflict, stale cache, missed delta, and historical reconstruction.
- Each vertical claim maps to an adopted profile and authority model.
- Marketing distinguishes repository foundation, implemented adapter, conformance evidence, and external recognition.

## 23. Success Measures

- median participant onboarding and renewal time;
- percentage of published facts with current authoritative provenance;
- resolution latency, availability, and cache hit rate;
- stale/indeterminate/conflict result rate by source;
- time from authority change to signed publication and consumer acknowledgment;
- key/certificate/mandate expiry prevented before outage;
- incident suspension-to-consumer propagation time;
- historical-resolution reproducibility rate;
- percentage of consumers verifying signatures, sequence, and freshness;
- support cases caused by scope/profile ambiguity;
- public registry accessibility and search success;
- conformance pass rate by profile and adapter.

## 24. Source Evidence

### Repository

- `docs/strategy/uix-pairing-briefs/10-additional-api-uix-opportunity-map.md`
- `docs/strategy/uix-pairing-briefs/13-federation-trust-api-trust-center-uix.md`
- `docs/strategy/uix-pairing-briefs/17-certificate-lifecycle-api-certificate-center-uix.md`
- `docs/strategy/uix-pairing-briefs/18-attestation-api-attestation-center-uix.md`
- `docs/strategy/uix-pairing-briefs/20-credential-issuer-api-issuer-studio-uix.md`
- `docs/strategy/uix-pairing-briefs/21-credential-wallet-api-wallet-uix-sdk.md`
- `docs/strategy/uix-pairing-briefs/22-credential-verifier-api-verification-console-uix.md`
- JOSE, federation, credential, certificate, attestation, policy, residency, audit, and security-signal packages/tests.

### Standards and authoritative sources

- [OpenID Federation 1.0 Final Specification](https://openid.net/specs/openid-federation-1_0-final.html): trust anchors, signed entity statements, trust chains, metadata policy, and trust marks.
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/): issuer, credential schema/status vocabulary, validity, and status privacy requirements.
- [Regulation (EU) 2024/1183](https://eur-lex.europa.eu/eli/reg/2024/1183/oj): revised European digital identity framework and machine-readable certified-wallet lists.
- [Commission Implementing Regulation (EU) 2025/848](https://eur-lex.europa.eu/eli/reg_impl/2025/848/oj): registration and verification of wallet-relying parties using authoritative lists and evidence.
- [ETSI TS 119 612](https://www.etsi.org/deliver/etsi_ts/119600_119699/119612/): trusted-list structure and trust-service status concepts; implement only the selected current profile/version after standards review.
- [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280): X.509 path validation and trust-anchor context.
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785): JSON canonicalization considerations for signed registry artifacts.

## 25. Explicit Non-Claims

- Registry presence does not make an entity universally trusted.
- Signature or certificate validity does not prove authorization for a credential type or transaction.
- A trust mark is scoped evidence, not blanket certification.
- The registry does not replace verifier policy, certificate validation, credential status checking, attestation appraisal, or local risk decisions.
- Imported data is not authoritative merely because it is machine-readable or signed; source authority and scope still matter.
- OpenID Federation support does not imply support for every government, certificate, or credential trust-list format.
- Operating the software does not make Tigrbl the legal or supervisory authority for a customer ecosystem.
- A vertical profile is not regulatory compliance or government recognition without independent evidence.
