# Cross-Border Transfer Authorization API + Transfer Assessment UIX

- **Pairing:** 35
- **Status:** Proposed product brief
- **Primary owners:** Privacy engineering, authorization, legal operations, security, frontend, UIX, product copy
- **Adjacent pairing:** Sovereignty Policy API + Regional Boundary Control UIX

## 1. Product decision

Build a Cross-Border Transfer Authorization API and Transfer Assessment UIX that turn proposed international data movements and remotely accessible processing into explicit, reviewable, time-bounded authorization decisions.

The product should inventory transfer paths, identify applicable rule sets, assemble technical and organizational facts, record counsel-approved mechanisms and assessments, require supplementary measures, authorize or block execution, monitor material change, and preserve decision evidence.

It must not practice law, select a legal mechanism autonomously, or imply that a technical allow decision guarantees a lawful transfer.

## 2. Product boundary

This pairing answers: **May this specific transfer path proceed now, under which approved basis, controls, scope, and expiry?**

It is distinct from:

- data residency, which describes where data is stored or processed;
- sovereignty policy, which enforces technical and operational boundaries;
- ordinary authorization, which decides whether an actor may perform an action;
- consent and privacy-purpose management;
- retention and deletion policy;
- contractual lifecycle management; and
- legal advice or regulator-facing certification.

A transfer can occur through replication, export, API access, support access, telemetry, backup, remote administration, onward processing, or a downstream subprocessor—not only through a file copy.

## 3. Repository starting point

The current codebase provides only an upstream signal:

- `TenantResidencyRecord` stores `restricted_transfer_regions`.
- `evaluate_residency_access` denies a configured restricted region.
- `ResidencyDecision.transfer_required` is inferred when a requested processing region is not listed among a zone's jurisdictions.
- residency zones and tenant assignments have durable tables and security tests.

The repository has no dedicated transfer case, party/role model, data-flow inventory, destination-country facts, legal mechanism record, transfer assessment, supplementary-measure plan, approval, expiry, onward-transfer chain, monitoring event, authorization receipt, or Transfer Assessment UIX.

The existing boolean must therefore be treated as **“further transfer analysis may be required”**, not as a legal conclusion. Its region-versus-jurisdiction comparison is insufficient to identify all restricted transfers and must remain backward compatible until a richer adapter is introduced.

## 4. Users and jobs to be done

### Privacy and legal teams

Triage proposed transfers, determine applicable frameworks, select or approve mechanisms, document assessments, require safeguards, schedule reviews, and answer audit or regulator inquiries.

### Security and privacy engineers

Supply verified architecture facts, validate technical measures, connect enforcement points, detect route drift, and prove that required controls executed.

### Product and data owners

Describe purpose, data, subjects, frequency, necessity, parties, and operational impact; compare compliant alternatives; and remediate blocked proposals.

### Procurement and vendor management

Maintain recipient, processor, subprocessor, contract, location, and onward-transfer facts without becoming transfer-decision approvers by default.

### Tenant administrators

Understand customer-specific transfer settings, review disclosed recipients and destinations, and participate in approvals or notifications where contracted.

### Support and incident responders

Use narrowly scoped emergency processes and reconstruct any transfer or access performed during an incident.

## 5. Core domain model

Introduce typed, versioned resources:

- `TransferProposal`: initiator, business owner, purpose, trigger, requested dates, systems, and status.
- `TransferPath`: exporter/source, importer/destination, intermediary and onward recipients, jurisdictions, access modes, infrastructure path, and frequency.
- `TransferParty`: organization, legal role, operational role, establishment, processing locations, contacts, and verified identifiers.
- `DataScope`: data categories, sensitivity, data subjects, volume, retention, purpose, and pseudonymization state.
- `ApplicableRegime`: rule-set identifier, territorial rationale, authoritative version, effective dates, and assigned legal owner.
- `TransferMechanism`: mechanism type, governing artifact, parties, module/role configuration, execution state, scope, validity, and limitations.
- `TransferAssessment`: questions, facts, sources, analysis supplied by authorized reviewers, residual risk, decision, rationale, version, and review date.
- `SupplementaryMeasure`: technical, contractual, or organizational measure; owner; verification method; enforcement point; evidence; and status.
- `TransferAuthorization`: exact path and data scope, approved mechanism/assessment versions, conditions, start/end, decision, approvers, and revocation state.
- `OnwardTransfer`: parent authorization, downstream party/path, inherited and additional conditions, and approval status.
- `TransferEvent`: observed export, replication, remote access, disclosure, backup, support session, or onward movement.
- `TransferReceipt`: preflight decision, enforcement outcome, control evidence, actual route, timestamp, and correlation ID.
- `MaterialChange`: changed law/guidance, recipient, route, purpose, data, subprocessor, control, contract, or destination that may require reassessment.

Historical cases must resolve against the exact rule-set, contract, assessment, route, and authorization versions used at decision time.

## 6. Transfer identification

The discovery workflow must test facts rather than assume every cross-region operation is legally identical. It should capture:

- source and destination organizations, establishments, and roles;
- whether a separate recipient receives or can access the data;
- physical movement, remote access, support access, and onward disclosure;
- destination, transit, backup, key-operation, log, and administrative-access locations;
- whether the destination processing is already directly subject to the relevant regime;
- data type, subjects, purpose, volume, frequency, and duration;
- controller/processor and exporter/importer relationships;
- subprocessors and downstream destinations;
- customer-specific contractual constraints.

The UI may recommend questions and flag inconsistencies, but only an authorized policy/legal owner can confirm applicability and mechanism.

## 7. Multi-regime architecture

Do not encode “international transfer” as an EU-only concept. Use configurable, versioned jurisdiction packs that define terminology, question sets, eligible mechanism categories, required approvals, reassessment triggers, and source links.

Initial packs may support EU/EEA GDPR and UK GDPR workflows, followed by customer-selected regimes. A pack is decision support, not embedded legal advice. Content updates require legal review, provenance, effective dates, change notes, and regression tests.

When multiple regimes apply, the case must preserve parallel analyses and require every applicable authorization condition before execution. Never collapse conflicting requirements into an undocumented “most strict” heuristic.

## 8. Mechanism registry

The registry should represent, without automatically prescribing:

- adequacy or equivalent recognized-destination decisions;
- standard contractual clauses and their configured modules;
- UK IDTA/Addendum or other approved contractual instruments;
- binding corporate rules;
- codes, certifications, administrative arrangements, or bespoke approvals where a regime recognizes them;
- narrow statutory exceptions/derogations, with heightened review and non-routine-use warnings;
- no available mechanism.

Each record needs authoritative source, jurisdiction, effective interval, parties/roles, executed artifact, covered data and paths, onward-transfer constraints, required assessments, supplementary measures, notices, and renewal triggers.

The system should never treat a signed contract alone as proof that every covered transfer is authorized.

## 9. Assessment workflow

Use a configurable workflow rather than a universal risk score:

1. confirm the transfer and applicable regimes;
2. map parties, data, purposes, destinations, and onward paths;
3. identify a candidate mechanism approved for the exact roles and scope;
4. gather destination-law, recipient-practice, transparency, and redress facts from governed sources;
5. evaluate whether the mechanism can operate effectively for this transfer;
6. define and verify supplementary measures;
7. record residual risk and authorized reviewer rationale;
8. approve, conditionally approve, deny, or return for remediation;
9. enforce the authorization and monitor material change.

Question sets must support citations, evidence dates, confidence, conflicts, “unknown,” reviewer comments, and privileged/confidential handling. Numeric scoring may prioritize work but must not manufacture a legal conclusion.

## 10. Supplementary measures

Measures must be typed and testable. Examples include encryption with appropriate key control, effective pseudonymization, split processing, data minimization, destination isolation, access restrictions, transparency commitments, challenge/notification procedures, audit rights, and operational governance.

Every required measure needs:

- applicability and expected protection;
- technical or organizational owner;
- enforcement point;
- verification procedure and frequency;
- current evidence and expiry;
- failure behavior;
- residual limitations; and
- linkage to policy obligations and enforcement receipts.

The UI must not imply that encryption is automatically sufficient; effectiveness depends on threat, access path, key control, processing needs, and approved analysis.

## 11. Onward transfers and transfer chains

Authorization must follow the complete known recipient chain. The product should:

- distinguish direct, intermediary, and onward recipients;
- show inherited versus destination-specific conditions;
- prevent a parent authorization from silently covering an unreviewed child path;
- detect new subprocessors, locations, or remote-access routes;
- calculate affected authorizations when a shared recipient changes;
- preserve each party's role and contractual/evidence links;
- block or queue an onward event when coverage is missing or stale.

Unknown recipients and unresolved routes are explicit blockers when policy requires fail-closed behavior.

## 12. Runtime authorization

Preflight evaluation receives actor/workload, action, tenant/realm, data scope, purpose, source, destination, recipient chain, actual route, time, and assurance context. It returns:

- `allow`, `deny`, `conditional`, or `indeterminate`;
- authorization, assessment, mechanism, contract, and rule-pack versions;
- stable reason codes and explanation;
- required obligations and evidence freshness;
- permitted route, recipients, purpose, volume/frequency, and time window;
- remediation and escalation route.

Enforcement points include exports, APIs, replication, backups, analytics, remote support, administrative access, message delivery, and subprocessor routing. An authorization is valid only for its exact scope; it is not a bearer credential for arbitrary transfers.

## 13. Evidence and monitoring

The service must correlate approved intent with observed execution:

- actual source, destination, route, recipient, data class, purpose, and timestamp;
- obligation execution and enforcement receipt;
- contract and mechanism validity;
- supplementary-measure health;
- route, recipient, subprocessor, and destination drift;
- authoritative-content changes and scheduled review;
- unexpected or unauthorized transfer events.

Evidence must carry source, collection time, integrity status, confidence, retention, access classification, and expiry. Absence of observation is not proof that no transfer occurred.

## 14. Material change and reassessment

Configurable triggers include:

- new recipient, subprocessor, country, transit route, or support location;
- changed data category, subject group, purpose, scale, or frequency;
- changed contract, mechanism, role, or corporate relationship;
- degraded encryption, key custody, pseudonymization, access, or audit control;
- relevant authoritative decision, law, guidance, court judgment, or regulator action;
- expired evidence or scheduled review;
- incident, government-access request, or transparency change.

Triggering a review must not erase the prior authorization. Policy determines whether it remains active, becomes conditionally restricted, or is suspended pending reassessment.

## 15. API surface

Recommended resource groups:

- `/transfers/proposals`
- `/transfers/paths` and `/onward-paths`
- `/transfers/parties`
- `/transfers/data-scopes`
- `/transfers/regime-packs`
- `/transfers/mechanisms`
- `/transfers/assessments`
- `/transfers/measures`
- `/transfers/authorizations`
- `/transfers/evaluations`
- `/transfers/events` and `/receipts`
- `/transfers/material-changes`
- `/transfers/evidence-bundles`

Support idempotency, pagination, optimistic concurrency, dry-run evaluation, bulk impact analysis, event subscriptions, stable reason codes, scoped export, and deterministic reconstruction. Separate case drafting, legal approval, technical verification, runtime evaluation, and evidence-reading permissions.

## 16. Transfer Assessment UIX

### Transfer inventory

Show proposed, active, expired, denied, and unassessed paths by tenant, product, data class, purpose, source/destination, recipient, mechanism, owner, and review date. Highlight unknown and observed-but-unregistered paths.

### Guided triage

Use progressive questions to assemble facts and determine which expert review queues apply. Explain why each question matters, allow evidence attachment, expose uncertainty, and avoid presenting generated suggestions as approved legal answers.

### Transfer map

Visualize exporter, intermediary, importer, subprocessors, destinations, remote access, transit, backups, keys, and onward paths. Pair the graph with an accessible table and distinguish proposed, approved, observed, unknown, and blocked edges.

### Assessment workspace

Provide regime-specific sections, authoritative references, fact/evidence panels, reviewer notes, conflicts, measure testing, version diff, and explicit conclusion/rationale controls. Restrict privileged fields and clearly label AI- or system-suggested content as unapproved.

### Mechanism and contract coverage

Show executed status, applicable roles/modules, covered parties/data/paths, expiry, missing annex information, onward constraints, and linked assessments. Never display “contract signed” as equivalent to “transfer approved.”

### Supplementary-measure console

Map each required measure to an enforcement point, owner, evidence, freshness, test result, and failure action. Show residual limitations and controls that cannot technically satisfy the approved requirement.

### Authorization and approval view

Present exact scope, versions, conditions, effective dates, separation-of-duties checks, affected tenants, and operational impact. Require deliberate approval; prohibit dark patterns and bulk approval without scope review.

### Monitoring and reassessment queue

Group drift and change events by root cause and affected authorizations. Prioritize expired mechanisms, failed measures, new recipients, observed unauthorized routes, and regulatory-content updates. Preserve dismissal reason and expiry.

## 17. Workflow and governance

Lifecycle: discover → triage → scope → select candidate mechanism → assess → define measures → verify → approve → activate → monitor → reassess → suspend, revoke, expire, or supersede.

Required governance:

- legal/privacy approval cannot be self-approved by the proposer;
- technical-control verification is separate from legal conclusion;
- approvals are attributable, version-bound, and time-bounded;
- privileged analysis is access-controlled and excluded from broad exports by default;
- exceptions/derogations receive enhanced justification and review;
- emergency transfers have narrow scope, fixed expiry, receipts, and retrospective review;
- deletion does not destroy records subject to approved evidence-retention obligations.

## 18. Security, privacy, and reliability

- Tenant-isolate cases, contracts, assessments, evidence, and receipts.
- Apply field-level authorization to privileged, confidential, and personal information.
- Encrypt records and attachments; integrity-protect approvals and receipts.
- Malware-scan and content-type validate uploaded artifacts.
- Prevent approval replay, version substitution, scope widening, confused-deputy calls, and stale cache authorization.
- Minimize copied personal data; prefer metadata, samples, and governed evidence references.
- Define fail-closed behavior for missing authorization, expired mechanisms, required-control failure, and incomplete recipient chains.
- Provide deterministic replay for captured versions and graceful outage behavior for non-transfer operations.
- Audit reads of sensitive legal and recipient information as well as mutations.

## 19. Instructions by delivery team

### Frontend engineer

Build reusable case status, route map/table, scoped authorization summary, assessment questionnaire, citation/evidence, mechanism coverage, control verification, version diff, approval, and reassessment components. Preserve IDs and version links across views. Enforce UI permissions, but never rely on the browser for authorization or legal logic.

### UIX designer

Design for collaborative expert work with visible uncertainty, provenance, handoffs, and separation of duties. Make transfer scope and onward paths legible before approval. Test complex multi-recipient, multi-regime, remote-access, emergency, and reassessment journeys. Provide accessible non-map alternatives and color-independent status cues.

### Copywriter

Use “transfer analysis required,” “candidate mechanism,” “approved for this scope,” “control evidence expired,” and “reassessment required.” Avoid “GDPR compliant,” “safe country,” “legal transfer,” or “fully protected” unless qualified and approved by counsel. Distinguish official source text, organizational interpretation, reviewer conclusion, and system-generated suggestion.

### Backend and privacy engineers

Define canonical versioned contracts, regime-pack provenance, deterministic policy evaluation, scoped authorization, recipient-chain validation, material-change detection, receipt integrity, evidence retention, and compatibility with the residency `transfer_required` signal. Add migrations, adversarial tests, role/tenant isolation tests, and replay tests.

## 20. Stakeholder enablement

- **Technical marketing:** demonstrate discovery of an onward path, evidence-backed measure verification, a blocked stale authorization, and a controlled reassessment. Avoid universal compliance claims.
- **Developer relations:** deliver API quickstarts, sandbox regime packs, event schemas, transfer-path fixtures, export/remote-access enforcement examples, webhooks, and failure-mode tutorials.
- **Sales and account management:** maintain a regime/mechanism capability matrix, supported integrations, customer responsibilities, legal-review prerequisites, regional availability, and implementation lead times.
- **GTM strategy:** package transfer inventory and workflow separately from runtime enforcement, continuous monitoring, evidence bundles, and advanced multi-regime/subprocessor management.
- **Copywriting:** maintain a legally reviewed glossary, claim library, jurisdiction-pack release notes, empty/error states, and role-specific explanations.

## 21. Delivery phases

### Phase 1 — Governed case system

Add proposals, parties, paths, data scopes, mechanism registry, assessment workflow, approvals, expiry, attachments, version history, and an adapter that converts the current boolean into an analysis queue signal.

### Phase 2 — Technical verification and enforcement

Add supplementary measures, sovereignty/dependency integration, preflight evaluation, scoped authorizations, runtime enforcement, receipts, onward-transfer validation, and deterministic reconstruction.

### Phase 3 — Continuous assurance

Add observed-event inventory, drift/material-change detection, regime-pack updates, bulk impact analysis, reassessment automation, tenant views, evidence bundles, and ecosystem connectors.

## 22. Acceptance criteria

- A transfer case captures direct, remote-access, intermediary, and onward paths.
- Applicable regimes and mechanism categories are versioned, sourced, effective-dated, and counsel-governed.
- Mechanism coverage is validated against exact parties, roles, data, purpose, path, and dates.
- Assessments preserve facts, citations, uncertainty, reviewer rationale, versions, and privileged access controls.
- Supplementary measures link to enforceable obligations, current evidence, owners, and failure behavior.
- Runtime decisions are scope-bound, deterministic, explainable, durable, and linked to enforcement receipts.
- Missing, expired, revoked, materially changed, or incomplete authorization fails according to explicit policy.
- Every onward transfer requires inherited or additional valid coverage; parent approval cannot silently widen scope.
- Material changes identify all affected active authorizations without rewriting history.
- The existing residency signal remains compatible but is never displayed as a legal decision.
- UIX meets keyboard, screen-reader, responsive, localization, and color-independent status requirements.
- Tenant isolation, privilege boundaries, version substitution, replay, upload, stale evidence, outage, and performance tests pass.

## 23. Success measures

- percentage of observed transfer paths registered and assessed;
- time from proposal to decision, separated by waiting owner;
- percentage of active authorizations with complete recipient chains and fresh evidence;
- unexpected transfer and route-drift detection rate;
- expired or failed measures blocked before execution;
- reassessment time after material change;
- exception/derogation volume, recurrence, and age;
- percentage of runtime events with matching authorization and receipt;
- time to produce a scoped, reconstructable evidence bundle;
- false-positive and false-negative rates in transfer discovery.

These are operational assurance measures, not proof that a transfer is legally valid.

## 24. Authoritative design references

- [GDPR, Chapter V—transfers to third countries or international organisations](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [European Commission—Standard Contractual Clauses](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en)
- [EDPB Recommendations 01/2020 on supplementary measures](https://www.edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en)
- [UK ICO—International transfers guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/)
- [UK ICO—Completing a transfer risk assessment/data protection test](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/completing-a-transfer-risk-assessment/)

These sources inform workflow requirements and must be monitored for change. Product implementation requires qualified jurisdiction-specific review.

## 25. Non-claims and dependencies

Do not claim that the product determines governing law, identifies every transfer, selects a lawful mechanism, guarantees equivalent protection, replaces counsel, or certifies compliance. Outcomes depend on accurate architecture and party data, current official sources, executed agreements, effective safeguards, organizational practice, technical enforcement, evidence quality, and authorized legal judgment.

Key dependencies include the Sovereignty Policy API, data inventory/classification, purpose and consent systems, processor/subprocessor registry, contract repository, authorization provenance, policy obligations and receipts, privileged-access/session provenance, key management, telemetry, retention, incident management, and trustworthy authoritative-content update processes.
