# Supply-Chain Identity API + Provenance UIX Requirements Brief

**Pairing:** `tigrbl-auth-router-supply-chain-identity` + `@tigrbl-auth/provenance-uix`<br>
**Opportunity-map item:** 19<br>
**Primary buyers:** software vendors, DevSecOps teams, regulated engineering organizations, AI/ML platforms, industrial firmware producers, and artifact consumers<br>
**Status:** proposed product surface; internal identity, attestation, signing, policy, and release-evidence foundations exist, while SLSA/in-toto/Sigstore product support is currently absent

## 1. Product Decision

Build an identity and policy control plane that connects source repositories, contributors, CI/CD workflows, builders, materials, artifacts, signatures, SBOMs, attestations, releases, deployments, and running workloads into a verifiable supply-chain graph.

The product must integrate established ecosystems:

- SLSA for supply-chain assurance tracks, levels, and provenance;
- in-toto attestations and layouts/policies;
- Sigstore/Cosign, Fulcio, Rekor, and trusted-root distribution;
- SPDX and CycloneDX for bills of materials and related lifecycle data;
- OCI registries and digest-addressed artifacts;
- workload identity, attestation, admission control, and deployment systems.

Tigrbl Auth should contribute identity, authorization, delegation, trust, policy, and evidence orchestration. It must not invent a competing signature, SBOM, provenance, or transparency format.

## 2. Product Promise

For any governed artifact or deployment, answer:

1. What exact immutable artifact is this?
2. Which source and materials produced it?
3. Which builder/workflow identity performed each step?
4. Which identities authorized source, build, release, and deployment?
5. Which signed attestations and SBOMs support those claims?
6. Which policy accepted or rejected the artifact, and at what lifecycle gate?
7. Is this the same digest that was deployed and is now running?
8. Which evidence is missing, stale, conflicting, or untrusted?

## 3. Current Repository Reality

The repository has useful foundations:

- human, service, workload, client, machine, device, and agent principals;
- workload identity, SPIFFE, certificate, key, JOSE, and attestation direction;
- policy decisions, decision traces, delegation provenance, authority graphs, and audit events;
- release certification, evidence bundles, claims/evidence linking, and artifact-truthfulness reporting;
- npm provenance configuration in at least one package/release workflow;
- internal documentation for product provenance and release signing;
- device/firmware and agent/tool provenance requirements.

However, the current target-reality matrix reports SLSA, in-toto, and Sigstore as `none`. Historical SBOM/provenance flags and internal evidence terminology are not proof of industry-standard production support.

Missing product foundations include:

- canonical source/build/artifact/release/deployment/workload graph contracts;
- DSSE/in-toto/SLSA/Sigstore/SPDX/CycloneDX ingestion and verification adapters;
- trusted builder and signer registries;
- OCI/referrer and artifact-store integration;
- supply-chain policy/admission APIs;
- transparency-log monitoring;
- dedicated API/UIX packages and conformance suites.

## 4. Users and Jobs

### Platform security and DevSecOps administrator

- register source systems, builders, signers, registries, and deployment environments;
- define which identities may build, sign, promote, and deploy;
- enforce provenance and SBOM policy at lifecycle gates;
- monitor compromised identities, dependencies, and builders.

### Developer and release engineer

- understand why a build or promotion was denied;
- produce compliant provenance and SBOMs automatically;
- sign artifacts with workload identity instead of long-lived keys;
- trace the deployed artifact back to reviewed source.

### Artifact consumer or procurement reviewer

- verify vendor artifacts and evidence against local policy;
- compare versions, components, vulnerabilities, licenses, and build assurance;
- retain a point-in-time verification receipt.

### Auditor and compliance lead

- reconstruct release and deployment authorization;
- show separation of source approval, build, signing, release, and deployment duties;
- export evidence without granting CI/registry administration.

### Incident responder

- find every artifact/release/deployment affected by a compromised source, dependency, builder, signer, workflow, key, or model dataset;
- quarantine and revoke trust while preserving forensic evidence.

### ML/AI and firmware team

- connect models/firmware to source, data/materials, build/training process, tests, signatures, devices, and deployments;
- express profile-specific evidence without pretending software provenance proves model quality or hardware state.

## 5. Architectural Ownership

### Supply-Chain Identity API owns

- normalized identities and relationships among source, builder, signer, artifact, release, deployment, and workload;
- connector configuration references and source provenance;
- ingestion/verification of supported provenance, signature, SBOM, and transparency artifacts;
- supply-chain policy inputs, gate decisions, and decision receipts;
- promotion/deployment authorization orchestration;
- impact analysis, quarantine, exceptions, and evidence exports;
- normalized graph/query APIs and the Provenance UIX.

### Existing packages retain ownership

- principals/workload identity: canonical identities and authentication;
- certificate/JOSE/signing: cryptographic primitives and key lifecycle;
- Attestation API: evidence verification/appraisal infrastructure;
- Trust Registry: approved builders, issuers, roots, profiles, and authorities;
- Policy Studio: decision semantics, versions, traces, and obligations;
- Security Signals: compromise/status events;
- release certification/SSOT: repository-specific release claims and evidence;
- storage/audit: durability and append-only event records.

### External systems remain authoritative

Source control, build platforms, artifact/OCI registries, transparency logs, package repositories, scanners, deployment controllers, and runtime orchestrators own their native state. The API records verified evidence and links, not a fictional replacement state.

## 6. Canonical Supply-Chain Graph

Required nodes:

- organization/project/product;
- source repository, revision, branch/tag, review, and source archive;
- human/service/workload identity and delegated actor;
- build platform, builder identity, workflow, runner, and environment;
- material/dependency/base image/dataset/model/input;
- build invocation and step;
- immutable artifact and digest;
- signature, attestation, SBOM, VEX, scan, and test result;
- release and promotion;
- deployment environment, deployment, workload, device, or fleet;
- policy decision, exception, incident, and evidence bundle.

Required edges include `authored`, `reviewed`, `authorized`, `built_by`, `used_material`, `produced`, `signed_by`, `attested_by`, `describes`, `promoted_as`, `deployed_to`, `running_as`, `derived_from`, `supersedes`, `quarantined_by`, and `verified_under`.

Every node/edge has tenant, source, retrieval time, effective time, integrity, verification, confidence, and version metadata. The graph is derived from evidence; it must not silently upgrade an assertion into a verified fact.

## 7. Identity and Authority Model

Represent separately:

- source author and reviewer;
- workflow trigger actor;
- CI control-plane identity;
- ephemeral runner/workload identity;
- builder identity named in provenance;
- signing identity and certificate issuer;
- release approver/promoter;
- deployment controller and requesting actor;
- running workload identity.

Requirements:

- bind automated identities to repository/workflow/environment/ref as available;
- preserve actor, subject, sponsor, and delegation lineage;
- prohibit identity equivalence based only on matching display names or email strings;
- require authorization at build, sign, promote, and deploy boundaries;
- support separation of duties and bounded exceptions;
- use short-lived, audience-bound identity tokens/certificates for automated signing;
- resolve trust at the relevant time and profile.

## 8. Artifact Identity

An artifact is identified by cryptographic digest plus media/type context, not mutable tag or filename.

Required metadata:

- digest algorithm/value and size;
- artifact/media type and canonical locator(s);
- package coordinates, OCI digest, model/data identifiers, or firmware identifiers;
- producer and project;
- creation/observation time;
- repository/registry and immutable-reference evidence;
- predecessor/successor and release membership;
- signature, provenance, SBOM, scan, and deployment links;
- retention and availability state.

Tags, versions, and release names are aliases. The UI must always reveal the digest behind them.

## 9. Provenance and Attestations

Support DSSE/in-toto statement envelopes and explicitly versioned predicate types. Initial predicates should include selected SLSA provenance and verification summaries, with adapters for SBOM, VEX, vulnerability scan, test, and policy attestations.

Verification stages:

1. parse and schema/profile validation;
2. envelope/signature and certificate/key validation;
3. signer/builder identity and authority resolution;
4. subject digest binding;
5. predicate-specific semantic validation;
6. materials/source/invocation consistency;
7. timestamp/transparency/freshness validation;
8. local policy evaluation.

Store the original artifact by immutable reference/digest where policy permits, plus normalized indexed facts and verification results. Preserve unknown predicate fields; do not claim full semantic verification for an unsupported predicate.

## 10. SLSA Profile

Adopt a named SLSA specification version and track. Current implementation planning should target the approved SLSA v1.2 model, while versioning all claims.

Requirements:

- evaluate source and build tracks independently;
- identify the exact level and requirements assessed;
- verify provenance subject, builder identity, build type, invocation parameters, materials, and completeness properties;
- evaluate builder/platform properties separately from one artifact’s provenance;
- preserve assessment authority, evidence, scope, and expiry;
- issue verification summaries only after required checks;
- show unmet requirements and evidence gaps.

A signed SLSA provenance statement does not by itself prove a SLSA level, vulnerability absence, source correctness, reproducibility, or runtime integrity.

## 11. Sigstore Profile

Support public-good and private Sigstore deployments through explicit trusted-root configuration.

Requirements:

- Cosign signature/attestation discovery for OCI and supported blobs;
- Fulcio certificate chain and OIDC identity checks;
- expected certificate identity and issuer policy;
- Rekor inclusion proof, signed entry/timestamp/bundle verification as applicable;
- CT/SCT verification where required by selected profile;
- TUF-distributed trusted roots and rotation;
- offline bundle verification;
- private-instance endpoint/operator separation;
- monitor transparency entries for unexpected signing identities/artifacts;
- never use insecure-ignore modes in production policy except as an explicitly quarantined diagnostic.

“Keyless” means ephemeral signing keys bound to identity and supporting infrastructure; it does not mean trustless, key-free, or automatically authorized.

## 12. SBOM, VEX, and Composition

Support selected versions of SPDX and CycloneDX without forcing lossless conversion between their models.

Requirements:

- validate syntax/schema and document identity;
- verify signature/attestation and subject artifact binding;
- index components, versions, package URLs, hashes, suppliers, licenses, dependencies, services, and completeness declarations;
- preserve generation tool, time, source, and provenance;
- represent multiple SBOMs for one artifact and expose conflicts;
- track VEX/advisory status with authority, scope, justification, and expiry;
- distinguish component presence, known vulnerability match, exploitability assertion, and policy decision;
- diff SBOMs by artifact digest/version;
- disclose completeness and evidence freshness.

An SBOM is an inventory claim, not proof of completeness, safety, license compliance, or non-exploitation.

## 13. Build and Release Policy

Policy inputs may include:

- approved source organization/repository/ref;
- required review/signature/branch-protection evidence;
- approved builder/workflow identity and immutable workflow reference;
- SLSA track/level requirements;
- hermetic/isolation/material completeness properties;
- expected signer/OIDC issuer/transparency log;
- required SBOM/VEX/scan/test predicates;
- allowed dependencies, registries, licenses, vulnerabilities, and exceptions;
- artifact age and evidence freshness;
- separation of duties;
- target environment and risk tier.

Return allow, deny, quarantine, or indeterminate with trace, missing evidence, obligations, and cache constraints. Policy evaluation must use immutable artifact digest and evidence versions.

## 14. Promotion, Deployment, and Runtime Binding

Promotion/deployment requirements:

- resolve mutable references to an immutable digest before decision;
- verify evidence and policy immediately before promotion/admission;
- bind approval to digest, target environment, configuration identity, and deadline;
- create deployment attestation containing requested and observed digest;
- obtain target/controller acknowledgment;
- observe running workload/device digest and identity where available;
- detect drift, mutable-tag substitution, unsigned sidecars/plugins, or post-admission mutation;
- revoke/quarantine on compromise events according to policy;
- preserve rollback artifact and evidence as a separate decision.

Build provenance does not prove that the same artifact was deployed; deployment evidence does not prove the runtime remained unchanged.

## 15. AI/Model and Dataset Profile

Treat model, dataset, prompt/template, code, tokenizer, adapter, configuration, and evaluation result as distinct digest-addressed materials/artifacts.

Requirements:

- record training/fine-tuning pipeline and builder identity;
- bind model artifact to code, base model, datasets, configuration, and evaluations where disclosure permits;
- support protected references/digests when datasets cannot be exposed;
- record licenses, usage restrictions, privacy/governance attestations, and approval;
- distinguish publisher claims, independent evaluations, and runtime attestations;
- bind deployed model/service version to the verified artifact;
- support model signing and registry/deployment admission.

Provenance does not prove dataset legality, absence of personal data, model safety, fairness, performance, or truthfulness.

## 16. Firmware and Device Profile

- bind source/materials/builder to signed firmware image and manifest digest;
- record hardware/product compatibility, version/sequence, anti-rollback policy, update signer, and release authority;
- integrate Device/Fleet Trust for rollout, observed version, attestation, quarantine, and rollback;
- distinguish manufacturing, update-authority, build, release, and device identities;
- preserve offline verification bundles for constrained devices;
- never infer successful installation from artifact publication alone.

## 17. Transparency and Monitoring

Monitor configured transparency logs and registries for:

- expected and unexpected signing identities;
- duplicate/conflicting provenance for a digest;
- signatures outside approved workflow/time/environment;
- missing inclusion proofs or inconsistent log views;
- new artifacts under protected names;
- compromised/revoked signer or builder identities;
- evidence disappearance or registry mutation.

Transparency logs improve detectability and timestamp evidence; they do not guarantee statement truth, confidentiality, or absence of split views without monitoring and gossip/checkpoint policy.

## 18. API Requirements

Provide versioned endpoints for:

- `/projects`, `/sources`, `/builders`, `/workflows`, and `/signers`;
- `/artifacts`, aliases, digests, relationships, and evidence inventory;
- `/attestations`, `/provenance`, `/signatures`, `/sboms`, `/vex`, and `/scans`;
- `/releases`, promotions, approvals, and evidence bundles;
- `/deployments`, admissions, observations, runtime bindings, and drift;
- `/policies`, profiles, simulations, decisions, and exceptions;
- `/trust-roots`, transparency logs, monitors, and checkpoints;
- `/connectors`, ingestion jobs, health, and coverage;
- `/verify`, batch verification, and portable receipts;
- `/incidents`, impact graph, quarantine, exceptions, and recovery.

API rules:

- digest is mandatory for security decisions;
- treat all imported documents as untrusted with strict size/schema/parser bounds;
- retain raw evidence by immutable content reference and normalization version;
- use idempotent ingestion and deduplicate by digest without merging conflicting provenance;
- provide asynchronous jobs and streaming progress for graph imports and impact analysis;
- enforce tenant/project/environment authority and field-level evidence privacy;
- return separate syntax, signature, identity, trust, semantic, freshness, and policy results.

## 19. Provenance UIX

### Supply-chain overview

Show release/deployment posture, unsigned or unprovenanced artifacts, policy failures, stale/missing SBOMs, unapproved builders/signers, vulnerable components, transparency alerts, drift, exceptions, and connector freshness.

### Artifact explorer

Search by digest, version, package, repository, component, signer, builder, release, and deployment. Detail centers the immutable digest and shows source/materials, build, signatures, attestations, SBOM, policy, releases, and runtime observations.

### Provenance graph

Visualize evidence-backed paths with verified/asserted/missing/conflicting state. Every graph has an accessible table/timeline and bounded expansion. Selecting an edge reveals source evidence and verification.

### Verification workbench

Accept safe artifact/evidence references or controlled uploads, select trust/policy profile, and show layered results plus reproducible CLI/API examples. Uploaded proprietary artifacts are not retained by default.

### Policy and admission studio

Use templates for source, builder, SLSA, signer, transparency, SBOM, vulnerability/license, promotion, deployment, AI, and firmware requirements. Provide fixtures, simulation, semantic diff, approval, staged rollout, and rollback.

### Release and deployment view

Show digest manifest, approvals, evidence completeness, gate decisions, promotion history, target deployments, observed runtime digests, drift, rollback readiness, and exceptions.

### SBOM and impact explorer

Provide component/dependency views, SBOM completeness/source, version diff, VEX/advisory context, affected artifacts/releases/deployments, and remediation tracking. Never render “not affected” without the VEX authority and justification.

### Incident response

Start from compromised dependency, source, workflow, builder, signer, root, artifact, or model dataset. Preview affected graph, quarantine/deny actions, active deployments, exceptions, notifications, and evidence preservation.

## 20. Security, Privacy, and Reliability

- Enforce tenant/project/environment isolation in graph, search, caches, jobs, and exports.
- Separate source, build, signing, release, deployment, policy, trust-root, and audit authority.
- Require strong workload identity and short-lived signing credentials.
- Protect signing and registry credentials with HSM/KMS or external systems; never expose them in UIX.
- Prevent parser, archive, decompression, XML/JSON, graph, and resource-exhaustion attacks.
- Apply SSRF and controlled-egress rules to repositories, registries, logs, and metadata sources.
- Verify digest before using any cached evidence.
- Avoid publishing proprietary source/material names, private repository identity, or personal OIDC claims to public transparency systems without policy/privacy review.
- Detect rollback, freeze, equivocation, stale roots, and missed log checkpoints.
- Use transactional outbox/idempotent consumers for gate and quarantine actions.
- Fail closed or quarantine according to explicit gate policy; never silently allow because a verifier is unavailable.
- Preserve evidence immutably while supporting retention/legal/privacy obligations.
- Meet WCAG 2.2 AA for dense graphs, tables, timelines, and workflows.

## 21. Stakeholder Requirements

### Technical marketing

Demonstrate source-to-running-workload traceability, keyless identity-based signing, SLSA provenance verification, SBOM impact analysis, admission denial, and compromised-builder quarantine. Label standard/profile versions and distinguish generated, signed, verified, and policy-accepted evidence.

### Developer relations

Deliver CI templates, Cosign/Sigstore examples, in-toto/DSSE/SLSA fixtures, SPDX/CycloneDX ingestion, OCI integration, admission samples, policy SDK, local verifier CLI, offline bundles, negative tests, and migration guidance from long-lived signing keys.

### Sales and account management

Use discovery for source/build/registry/deployment platforms, artifact types, SLSA targets, SBOM formats, signing model, private/public Sigstore, trust roots, policy gates, scale, retention, air gaps, AI/firmware needs, and incident workflows. Provide connector/maturity and responsibility matrices.

### GTM strategist

Lead with artifact identity and verification, then add release/deployment gates, SBOM impact, and continuous monitoring. Package AI and firmware as profiles over the same graph. Do not sell “secure supply chain” as a binary outcome or claim SLSA conformance before assessment evidence.

### Copywriter

Standardize `artifact`, `digest`, `signature`, `attestation`, `provenance`, `builder`, `signer`, `materials`, `SBOM`, `verified`, `policy accepted`, `deployed`, and `observed running`. Avoid `trusted build`, `tamper-proof`, `vulnerability-free`, `complete SBOM`, and `SLSA compliant` without scope/evidence.

## 22. Delivery Instructions

### Frontend engineer

- Generate typed clients and carry artifact digest/profile/policy version through every security workflow.
- Implement server pagination/filtering and bounded, lazy graph traversal.
- Provide table/timeline alternatives for graphs.
- Sandbox untrusted evidence rendering and avoid fetching arbitrary embedded URLs.
- Require preview/diff/approval for trust-root, builder, signer, gate, exception, and quarantine changes.
- Separate imported assertions from verified facts in UI data models.
- Instrument flow outcomes without recording proprietary evidence content.

### UIX designer

- Make digest, evidence source, verification stage, freshness, and policy result visually persistent.
- distinguish source claim, signed attestation, identity-authorized attestation, and policy acceptance.
- Design missing, stale, partial, conflicting, unsupported, quarantined, and degraded states.
- Optimize incident impact traversal and release gate explanation.
- Keep expert detail discoverable without making graph visualization the only interface.

### Copywriter

- Write “what this proves / does not prove” for signature, provenance, SBOM, SLSA level, transparency, VEX, deployment, and runtime observations.
- Explain policy failures with remediation and exact missing evidence.
- Preserve external standard vocabulary and version labels.
- Avoid implying misconduct from anomalous or conflicting evidence.

## 23. Delivery Phases

### Phase 1: Artifact identity and verification

- canonical graph, artifact digest, signer/builder/trust contracts;
- OCI/Cosign/Sigstore signature and bundle verification;
- DSSE/in-toto statement ingestion and selected SLSA provenance;
- artifact explorer, verification workbench, receipts, and evidence.

### Phase 2: SBOM and release governance

- SPDX/CycloneDX adapters, component graph, VEX context, and diff;
- release manifests, approvals, SLSA/build policies, exceptions;
- transparency monitoring and trusted-root lifecycle.

### Phase 3: Deployment/runtime closure

- registry promotion and Kubernetes/deployment admission connectors;
- observed digest/workload identity binding and drift;
- security-signal quarantine and incident impact workflows;
- scale, offline, and private Sigstore profiles.

### Phase 4: AI, firmware, and ecosystem

- model/dataset and firmware profiles;
- partner builder/registry/scanner connectors;
- regulated evidence packs and independent conformance/assessment workflows.

## 24. Acceptance Criteria

### API/runtime

- Every decision addresses an immutable artifact digest.
- Signature verification requires an expected identity/trust policy, not signature validity alone.
- Provenance subject digest matches the artifact and supported predicate semantics are validated.
- SLSA results name version, track, level, assessor, evidence, and unmet requirements.
- SBOM/VEX results preserve format/version, source, signature, artifact binding, completeness, and conflicts.
- Promotion/deployment approval binds exact digest and target.
- Running observation is separate from deployment intent.
- Trust-root/log rotation and offline verification are deterministic.
- Imported evidence cannot cross tenant/project boundaries.
- Compromise impact analysis traverses evidence-backed edges and preserves uncertainty.

### UIX

- Users can trace artifact to source/build and to deployment/runtime where evidence exists.
- Mutable tags always resolve to and display a digest.
- Missing evidence is never shown as passing.
- Graphs have accessible non-graph equivalents.
- Incident responders can preview and execute scoped quarantine with partial-failure visibility.
- Core workflows meet WCAG 2.2 AA.

### Evidence/business

- Fixtures cover valid, forged, unsigned, wrong-subject, wrong-identity, untrusted-root, stale-root, missing-log, conflicting provenance, incomplete SBOM, VEX exception, tag substitution, and runtime drift cases.
- Connector and standard claims map to named versions and conformance tests.
- Current product messaging acknowledges that repository SLSA/in-toto/Sigstore support begins at `none` until these phases ship.

## 25. Success Measures

- percentage of released/deployed artifacts identified by immutable digest;
- percentage with verified signature, provenance, and SBOM by risk tier;
- SLSA requirement coverage by track/level and builder;
- verification and admission latency/success;
- unsigned/unapproved artifact denial rate;
- mutable-tag substitution and runtime-drift detections;
- transparency alert response time;
- dependency/signer/builder incident impact-analysis time;
- quarantine-to-confirmed-remediation time;
- SBOM completeness/conflict/freshness distribution;
- long-lived signing key retirement;
- release failures caused by actionable versus false-positive policy;
- evidence reconstruction success for audits.

## 26. Source Evidence

### Repository

- `docs/strategy/uix-pairing-briefs/10-additional-api-uix-opportunity-map.md`
- `docs/compliance/TARGET_REALITY_MATRIX.md`
- `docs/compliance/ADR_GAP_COVERAGE_PROPOSAL.md`
- `docs/compliance/SPEC_GAP_COVERAGE_PROPOSAL.md`
- `docs/architecture/product-provenance-lineage.md`
- `docs/strategy/uix-pairing-briefs/18-attestation-api-attestation-center-uix.md`
- `docs/strategy/uix-pairing-briefs/23-device-iot-identity-api-fleet-trust-uix.md`
- `docs/strategy/uix-pairing-briefs/27-trust-registry-api-trust-registry-uix.md`
- release certification, claims/evidence, authorization provenance, JOSE, workload identity, attestation, policy, audit, and security-signal packages/tests.

### Standards and primary sources

- [SLSA v1.2](https://slsa.dev/spec/v1.2/): approved source/build tracks, levels, provenance, and verification-summary model.
- [in-toto specification](https://github.com/in-toto/docs/blob/master/in-toto-spec.md) and [Attestation Framework](https://github.com/in-toto/attestation): supply-chain step metadata and statement/predicate model.
- [Sigstore documentation](https://docs.sigstore.dev/) and [Cosign identity-based signing](https://docs.sigstore.dev/cosign/signing/overview/): ephemeral keys, Fulcio identity certificates, Rekor transparency, Cosign, and TUF roots.
- [SPDX specifications](https://spdx.dev/use/specifications/): ISO/IEC 5962 SBOM and supply-chain information model; choose supported exact versions.
- [CycloneDX specification](https://cyclonedx.org/specification/overview/): component/service/dependency, SBOM, VEX, formulation, and attestation-oriented model; choose supported exact versions.
- [OCI Image and Distribution specifications](https://opencontainers.org/): digest-addressed images/artifacts and registry distribution.
- [The Update Framework](https://theupdateframework.io/): secure trusted-metadata distribution and rollback/freeze protections.

## 27. Explicit Non-Claims

- A signature proves possession/use of a signing key under a verification policy; it does not prove artifact safety.
- Keyless signing still depends on keys, identity providers, certificate/log services, and trusted roots.
- Transparency-log inclusion does not prove statement truth.
- Provenance does not prove source correctness, reproducibility, vulnerability absence, or runtime integrity.
- An SBOM does not prove completeness, safety, license compliance, or exploitability.
- A VEX statement is an scoped assertion from an authority, not universal proof of non-impact.
- SLSA is versioned and track-specific; one attestation does not establish an entire organization’s conformance.
- Build evidence does not prove the same digest was deployed or remains running.
- Existing internal provenance/evidence features do not establish current Sigstore, in-toto, SLSA, SPDX, or CycloneDX product conformance.
