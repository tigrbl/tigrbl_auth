# Jurisdiction-Aware Authorization API + Regulatory Policy Map UIX

- **Pairing:** 36
- **Status:** Proposed product brief
- **Primary owners:** Authorization, privacy engineering, policy governance, legal operations, frontend, UIX, product copy
- **Adjacent pairings:** Sovereignty Policy API; Cross-Border Transfer Authorization API; Authorization Provenance API

## 1. Product decision

Build a Jurisdiction-Aware Authorization API and Regulatory Policy Map UIX that determine which governed policy overlays apply to a request, compose them predictably with tenant and product policy, expose conflicts and missing facts, and preserve the exact source and policy lineage behind every result.

The system must not encode law as an undocumented collection of conditionals. It should operate on counsel-governed, versioned policy packs whose applicability rules, interpretations, effective dates, precedence, tests, and source provenance are explicit.

## 2. Product boundary

This pairing answers: **Which jurisdictional and organizational policy overlays apply to this authorization request, and what is their combined technical effect?**

It does not determine governing law, provide legal advice, certify compliance, approve an international transfer, or replace the regional boundary controller. It supplies governed applicability and authorization facts to those workflows.

Jurisdiction may be relevant through establishment, actor or subject location, data-subject nexus, resource location, processing location, service market, contract, sector, customer election, or another reviewed rule. IP geolocation alone is never sufficient proof.

## 3. Repository starting point

The repository has strong components but no jurisdiction-aware application layer:

- durable `Policy`, `PolicyVersion`, `PolicySet`, `PolicySetMember`, and `PolicyTarget` tables;
- policy administration and retrieval contracts;
- a default policy combiner and typed combining algorithms, including deny-overrides;
- authorization decision contracts, policy-version references, replay and stability tests;
- correctness checks for dangling provenance and unknown policy versions;
- authority-graph checks that detect conflicting policy versions;
- tenant, realm, residency zone, jurisdiction, processing-region, and adaptive-access context;
- an authorization decision engine and policy façade.

Current gaps:

- no canonical jurisdiction or applicability-fact model;
- no authoritative-source registry or governed regulatory policy pack;
- no effective-date, supersession, interpretation, or legal-review workflow for such packs;
- no composition precedence across global, jurisdiction, sector, contract, tenant, and resource policy;
- no conflict-resolution case, applicability explanation, jurisdiction evidence, impact simulation, or regulatory map UIX;
- current residency jurisdictions are location labels, not proof that a legal regime applies.

## 4. Users and jobs to be done

### Authorization and platform engineers

Resolve applicable policy consistently, test combinations, diagnose conflicts, prevent stale-pack use, and reconstruct decisions.

### Privacy, legal, and compliance teams

Govern applicability rules and interpretations, cite authoritative sources, review changes, approve effective dates, and assess impact without editing runtime code.

### Product and data owners

Understand why a feature or action is restricted in a context, simulate expansion to new markets, and identify required product changes.

### Tenant administrators

See tenant-elected and contract-specific overlays, their effective dates, operational effects, and escalation paths.

### Support and incident teams

Explain decisions without revealing privileged analysis and identify policy drift or incorrect context safely.

## 5. Core domain model

Introduce typed, versioned resources:

- `Jurisdiction`: canonical identifier, type, parent/peer relationships, aliases, validity, and source.
- `ApplicabilityFact`: typed fact, value, subject, issuer/source, confidence, observation time, expiry, and sensitivity.
- `RegulatorySource`: authority, title, canonical URL/reference, publication/effective dates, jurisdiction, checksum, language, and supersession.
- `PolicyPack`: owner, jurisdiction/sector, scope, lifecycle, legal-review state, and semantic version.
- `ApplicabilityRule`: required facts, excluded facts, rationale, source links, test fixtures, and indeterminate behavior.
- `PolicyOverlay`: machine-enforceable rule, target, priority class, obligations, explanation, and source/interpretation linkage.
- `InterpretationRecord`: approved organizational interpretation, author/reviewer, privilege classification, rationale, assumptions, and review date.
- `CompositionPlan`: selected overlays, precedence graph, combining algorithms, conflicts, unresolved dependencies, and effective interval.
- `JurisdictionDecision`: applicability results, combined authorization result, reasons, obligations, pack versions, facts, and provenance.
- `PolicyConflict`: competing rules, affected scope, severity, owner, disposition, exception, and expiry.
- `RegulatoryChange`: source change, affected packs, detected impact, migration plan, and rollout status.

Runtime decisions reference immutable versions. Updating a source or interpretation creates a new version and impact review; it never rewrites history.

## 6. Applicability context

Evaluation may use verified attributes about:

- actor, subject, customer, controller, processor, employer, and delegated authority;
- tenant, realm, contractual profile, product, market, and service offering;
- resource, data classification, data-subject category, purpose, and sector;
- storage, processing, access, administrator, and recipient locations;
- establishment, offering, monitoring, or other counsel-defined nexus;
- request time, emergency state, device/workload assurance, and transfer path.

Every fact needs provenance and freshness. The UI must distinguish asserted, observed, derived, contractually declared, reviewed, and verified facts. Unknown or conflicting facts cannot be silently converted to false.

## 7. Governed policy packs

A pack contains source references, applicability rules, technical overlays, obligations, explanations, fixtures, owner, reviewers, release notes, effective dates, and retirement rules.

Lifecycle: draft → legal review → technical validation → simulation → approval → scheduled → effective → superseded or withdrawn.

Packs must support localization without translating canonical identifiers. Source text, internal interpretation, implementation rule, and user-facing explanation are separate artifacts. Generated summaries remain drafts until reviewed.

## 8. Policy hierarchy and composition

The system should compose explicitly declared layers, such as:

1. platform safety invariants;
2. jurisdiction and sector overlays;
3. transfer and sovereignty constraints;
4. contractual/customer profile;
5. tenant and realm policy;
6. resource, data, and purpose policy;
7. contextual risk policy;
8. narrow, approved exception.

This list is a configurable governance model, not a universal legal hierarchy. Each layer declares its combining algorithm and whether it may narrow, satisfy, add obligations, or—only with explicit authority—override another result.

Default behavior should be monotonic: a lower layer may add restriction but cannot silently remove a higher-layer prohibition. Algorithms must define handling for allow, deny, conditional, not-applicable, and indeterminate.

## 9. Conflict and indeterminate handling

Conflicts include contradictory effects, mutually impossible obligations, competing precedence, incompatible effective dates, disputed applicability facts, and missing required implementation capability.

The API must return a structured conflict, not pick whichever rule loaded last. Policy defines whether the operation denies, pauses for review, or uses a pre-approved resolution. Every manual disposition needs scope, rationale, authority, expiry, and a linked remediation.

Indeterminate is distinct from deny and not-applicable. It identifies why evaluation cannot complete: unknown jurisdiction, stale evidence, unavailable pack, unresolved conflict, or unsupported obligation.

## 10. Runtime evaluation

The API receives actor/subject, action, resource, tenant/realm, purpose, data and sector context, locations, applicable-party facts, time, and assurance evidence. It returns:

- `allow`, `deny`, `conditional`, or `indeterminate`;
- applicable and non-applicable packs with reasons;
- fact provenance, confidence, and freshness;
- composition plan and combining trace;
- stable reason codes and safe explanations;
- required obligations and enforcement points;
- conflicts, missing facts, and remediation;
- policy, source, interpretation, and composition versions;
- correlation and provenance IDs.

Evaluation must be deterministic for a captured input/version set, tenant-isolated, bounded, cache-safe, and fail closed where policy requires it.

## 11. Regulatory source and change management

Source ingestion should monitor authoritative publishers, but detected content never activates policy automatically. The workflow must:

- record canonical source, checksum, publication/effective dates, language, and retrieval time;
- detect additions, amendments, withdrawals, and source failure;
- route changes to qualified owners;
- map changed sources to interpretations, overlays, tests, tenants, products, and decisions;
- simulate old-versus-new outcomes;
- require reviewed migration and rollout plans;
- retain superseded source and policy lineage.

Web content is evidence input, not trusted executable policy. Protect ingestion from spoofing, prompt injection, parser ambiguity, and unauthorized source substitution.

## 12. API surface

Recommended resources:

- `/jurisdictions`
- `/jurisdiction-facts` and `/fact-sources`
- `/regulatory-sources`
- `/regulatory-policy-packs` and `/versions`
- `/applicability-rules`
- `/policy-overlays`
- `/interpretations`
- `/composition-plans`
- `/jurisdiction-evaluations` and `/decisions`
- `/policy-conflicts`
- `/regulatory-changes` and `/impact-analyses`
- `/jurisdiction-evidence-bundles`

Support idempotency, optimistic concurrency, stable reason codes, batch and dry-run evaluation, policy replay, effective-time queries, event subscriptions, scoped exports, and signed release manifests. Separate source management, interpretation review, pack publication, runtime evaluation, conflict disposition, and evidence access permissions.

## 13. Regulatory Policy Map UIX

### Coverage map

Show jurisdictions and sectors with effective, scheduled, stale, conflicted, unsupported, and unassessed packs. A geographic visualization must have a complete table alternative and must not imply territorial applicability solely through color.

### Policy-pack workspace

Present sources, interpretations, applicability rules, overlays, tests, reviewers, versions, translations, and release notes side by side. Make the distance between official source and technical implementation visible.

### Applicability explorer

Let an authorized user enter or select a request context and inspect which facts triggered each pack, which packs did not apply, what remains unknown, and what additional evidence would resolve the result.

### Composition and conflict view

Visualize the layer stack, precedence edges, combining algorithms, rule effects, obligations, and unresolved conflicts. Provide an exact ordered/table trace suitable for accessibility and audit.

### Decision explorer

Reconstruct facts, pack/source/interpretation versions, applicability results, combined decision, obligations, enforcement receipts, and authorization provenance. Privileged rationale must be redacted from users lacking access while retaining a safe explanation.

### Change-impact center

Compare old and proposed source or pack versions; identify affected tenants, markets, features, resources, tests, and historical replay cases; assign remediation; and manage staged activation or rollback.

## 14. Security, privacy, and reliability

- Treat location, nationality, establishment, sector, and data-subject attributes as sensitive and minimize their use.
- Do not infer protected characteristics where a less intrusive jurisdiction fact suffices.
- Tenant-isolate policy, facts, decisions, conflicts, and evidence.
- Apply field-level access to privileged interpretations and legal analysis.
- Integrity-protect sources, pack releases, approvals, decisions, and receipts.
- Prevent version rollback, source substitution, cache poisoning, approval replay, and exception scope widening.
- Define outage behavior and last-known-good use with maximum age and explicit status.
- Test adversarial attributes, conflicting sources, clock boundaries, retroactive dates, overlapping jurisdictions, and localization.

## 15. Instructions by delivery team

### Frontend engineer

Build reusable jurisdiction status, fact provenance, applicability trace, policy-layer stack, conflict, source/version diff, impact table, approval, and decision-lineage components. Support large datasets with filtering and progressive disclosure. Do not implement policy or legal applicability logic in the browser.

### UIX designer

Design for uncertainty and expert collaboration. Keep map, applicability, composition, and decision concepts distinct. Make missing facts, stale sources, conflicts, effective dates, and privileged content unmistakable. Test multi-jurisdiction, multi-sector, disputed-fact, source-change, and rollback journeys.

### Copywriter

Use “policy pack applies based on,” “applicability unresolved,” “organizational interpretation,” and “technical effect.” Avoid “the law requires” unless the exact reviewed statement and source support it; avoid “compliant jurisdiction” and “legal approval.” Maintain role-specific explanations and a reviewed glossary.

### Backend and policy engineers

Define canonical jurisdiction IDs, typed facts, source provenance, immutable versions, explicit composition semantics, bounded evaluation, deterministic replay, safe caching, and compatibility adapters. Add lifecycle migrations and adversarial tests for precedence, applicability, source integrity, tenant isolation, and time boundaries.

## 16. Stakeholder enablement

- **Technical marketing:** demonstrate a request whose applicable overlays change with verified context, a visible conflict, and replayable policy lineage. Avoid maps that imply legal coverage.
- **Developer relations:** provide pack schemas, fixtures, evaluators, source adapters, decision examples, test harnesses, and a sandbox for composition and replay.
- **Sales and account management:** maintain supported-jurisdiction/sector capability matrices, update cadence, customer fact requirements, shared responsibilities, and explicit limitations.
- **GTM strategy:** distinguish core policy composition from premium jurisdiction packs, continuous source monitoring, impact analysis, and regulated-industry profiles.
- **Copywriting:** own a reviewed claims matrix, jurisdiction terminology, source attribution pattern, change notices, and safe denial/escalation copy.

## 17. Delivery phases

### Phase 1 — Governed applicability

Add canonical jurisdictions, facts and provenance, source registry, versioned packs, applicability evaluation, lifecycle approvals, and an explorer using existing policy/version infrastructure.

### Phase 2 — Composition and impact

Add explicit layer precedence, conflict resources, deterministic combined decisions, obligations, replay, change detection, simulations, and impact analysis.

### Phase 3 — Continuous operations

Add authoritative-source connectors, staged rollout, customer/sector packs, tenant views, evidence bundles, advanced localization, and cross-pairing enforcement receipts.

## 18. Acceptance criteria

- Every applicability result identifies the facts, sources, rules, and versions that produced it.
- Unknown, conflicting, stale, and absent facts remain distinct states.
- Packs cannot become effective without legal review, technical tests, approval, and effective dates.
- Composition order and algorithms are explicit, deterministic, tested, and reconstructable.
- Lower layers cannot silently widen higher-layer authority.
- Conflicts are durable, scoped, attributable, and never resolved by load order.
- Runtime decisions link to immutable source, interpretation, pack, composition, and obligation versions.
- Source changes cannot automatically mutate production policy.
- Historical replay and old-versus-new impact simulation are supported.
- Existing policy contracts and decisions remain compatible through tested adapters.
- UIX is keyboard, screen-reader, responsive, localized, and color-independent.
- Tenant isolation, privilege, source-integrity, replay, time-boundary, caching, outage, and performance tests pass.

## 19. Success measures

- percentage of decisions with complete applicability-fact provenance;
- indeterminate, stale-fact, and unresolved-conflict rates;
- time from authoritative change detection to reviewed impact assessment;
- percentage of pack releases with passing replay and regression suites;
- unexpected decision-change rate after pack activation;
- time to explain a jurisdiction-aware decision;
- number and age of manual conflict dispositions and exceptions;
- source freshness and source-integrity failure rate;
- rollout rollback frequency and affected-request volume.

These measure policy operations and traceability, not legal compliance.

## 20. Authoritative design references

- [NIST SP 800-162, Guide to Attribute Based Access Control](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)
- [GDPR, including Article 3 territorial scope](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [European Commission adequacy decisions](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en)
- [UK ICO guidance on who the UK GDPR applies to](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/personal-information-what-is-it/who-does-the-uk-gdpr-apply-to/)

Sources inform the governance model and require ongoing qualified review; they are not hard-coded product conclusions.

## 21. Non-claims and dependencies

Do not claim that this product determines territorial scope, resolves conflicts of law, guarantees a lawful basis, certifies compliance, or replaces qualified counsel. Results depend on accurate facts, current authoritative sources, approved interpretations, correct policy implementation, reliable enforcement, and organizational governance.

Dependencies include policy administration/retrieval, authorization provenance, policy obligations and receipts, residency and sovereignty, transfer authorization, tenant/realm and contract profiles, data classification, purpose and consent, location/establishment evidence, authoritative-content monitoring, and release certification.
