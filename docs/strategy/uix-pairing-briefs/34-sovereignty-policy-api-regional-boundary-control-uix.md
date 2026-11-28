# Sovereignty Policy API + Regional Boundary Control UIX

- **Pairing:** 34
- **Status:** Proposed product brief
- **Primary owners:** Authorization, platform security, data infrastructure, frontend, UIX, product copy
- **Adjacent pairing:** Cross-Border Transfer Authorization API + Transfer Assessment UIX

## 1. Product decision

Build a Sovereignty Policy API and Regional Boundary Control UIX that let an organization declare, enforce, observe, and prove where protected workloads and data may be processed and which operators, services, keys, and providers may control them.

The product must not equate a configured cloud region with sovereignty. A boundary is credible only when its complete dependency path—storage, processing, replication, backups, queues, logs, telemetry, keys, administrative access, subprocessors, and recovery—is evaluated and supported by current evidence.

## 2. Product boundary and terminology

- **Residency:** where data is stored or processed.
- **Localization:** a requirement to keep specified data or processing in a location.
- **Sovereignty:** the jurisdictional, organizational, operational, and cryptographic control conditions governing data and workloads.
- **Regional boundary:** the enforceable set of permitted regions, jurisdictions, providers, operators, and control conditions.
- **Cross-border transfer:** movement or legally relevant access across jurisdictions. Its legal basis and assessment belong to the adjacent Transfer Authorization pairing.
- **Availability:** the ability to continue service. Failover is not automatically permitted merely because it improves availability.

This product provides technical policy and evidence, not legal advice or an automatic certification of regulatory compliance.

## 3. Repository starting point

The codebase already provides a narrow, useful foundation:

- `ResidencyZone` defines a zone ID, jurisdictions, and free-form sovereign controls.
- `TenantResidencyRecord` assigns a tenant and optional realm to allowed processing regions and restricted transfer regions.
- `evaluate_residency_access` and `assert_residency_access` fail closed for missing allowlists, tenant or realm mismatch, restricted regions, and out-of-bound processing regions.
- `residency_policy_manifest` exports tenant policy declarations.
- Durable `residency_zones` and `tenant_residency` tables persist zone and assignment state.
- Security tests cover allowed-region decisions and boundary violations.

Current gaps must be represented honestly:

- decisions are not durably recorded in a `residency_decisions` table;
- the decision evaluates one declared `processing_region`, not the full service dependency path;
- sovereign controls are strings rather than typed, testable requirements;
- there is no observed-location evidence, drift detection, enforcement receipt, approval workflow, simulation, exception lifecycle, or operator UI;
- storage, replicas, backups, logs, keys, support access, subprocessors, and failover are not independently modeled;
- `transfer_required` is inferred from region membership and is not a legal transfer determination.

## 4. Users and jobs to be done

### Security and authorization teams

Define reusable boundaries, test requests and deployments, investigate denials, detect drift, and export defensible decision lineage.

### Data and platform teams

Map services and data stores to regions, validate dependency closure, plan migrations, and prevent unauthorized failover or replication.

### Privacy, legal, and compliance teams

Review technical facts, attach interpretations or approvals in the adjacent transfer workflow, and retrieve time-bounded evidence without editing infrastructure policy.

### Tenant and account administrators

Select entitled sovereignty profiles, understand coverage and constraints, request exceptions, and see service-impact warnings.

### Support and incident responders

Diagnose boundary failures and operate approved emergency procedures without silently weakening policy.

## 5. Core domain model

The API should introduce typed, versioned resources:

- `SovereigntyBoundary`: identity, name, lifecycle, jurisdictions, providers, operator constraints, key-control requirements, and default failure mode.
- `BoundaryComponentRule`: component type, permitted locations, prohibited locations, access constraints, evidence requirements, and severity.
- `ResidencyAssignment`: tenant, realm, workload, dataset or data class, purpose, boundary version, effective interval, and precedence.
- `InfrastructureComponent`: service, store, replica, backup, cache, queue, index, log sink, telemetry sink, key service, control plane, or subprocessor.
- `DependencyEdge`: caller, callee, data class, operation, path conditions, and observation source.
- `LocationObservation`: component, observed region/jurisdiction/provider, collection time, source, confidence, and expiry.
- `BoundaryDecision`: subject, action, resource/data class, requested execution context, evaluated boundary version, dependency snapshot, result, reasons, obligations, and correlation ID.
- `BoundaryReceipt`: enforcement point, decision reference, action taken, outcome, timestamp, and signed or integrity-protected evidence.
- `BoundaryException`: exact scope, rationale, approvers, safeguards, expiry, revocation, and linked transfer assessment where applicable.
- `FailoverPlan`: primary and candidate recovery paths, boundary evaluation, approval state, rehearsal evidence, and expiry.

All mutable policies must be versioned. Historical decisions must continue to resolve against the exact version and dependency snapshot used at decision time.

## 6. Boundary dimensions

Each boundary can constrain:

- jurisdiction and physical/cloud region;
- infrastructure provider and service SKU;
- storage, compute, replica, backup, cache, queue, search, and object-store location;
- audit-log, security-log, analytics, and telemetry destinations;
- key generation, custody, HSM operation, signing, decryption, and recovery location;
- support, administrator, and break-glass operator location and organization;
- control-plane and management-plane actions;
- approved subprocessors and downstream services;
- data classification, tenant, realm, workload, purpose, and operation;
- recovery region and emergency operating mode;
- evidence freshness and assurance level.

Rules need explicit semantics: `must`, `must_not`, `one_of`, `all_of`, `requires_evidence`, and `requires_approval`. Free-form tags can supplement but must not replace enforceable rules.

## 7. Declared, configured, observed, and verified state

The UIX must distinguish four states:

1. **Declared:** policy intent.
2. **Configured:** infrastructure reports an intended configuration.
3. **Observed:** telemetry reports actual recent behavior or location.
4. **Verified:** required evidence is fresh and all dependencies satisfy the boundary.

Never label a boundary “compliant” solely from declared or configured state. Use precise labels such as **verified**, **partially evidenced**, **drift detected**, **evidence stale**, **not evaluated**, and **blocked**.

## 8. Policy evaluation and enforcement

Evaluation accepts tenant/realm, actor, action, resource, data class, purpose, candidate processing location, dependency graph, request time, and assurance context. It returns:

- `allow`, `deny`, `conditional`, or `indeterminate`;
- stable reason codes plus human-readable explanations;
- the violated component and dependency path;
- required obligations, such as region pinning, local-key use, log routing, approval, or enhanced evidence;
- boundary and policy versions;
- evidence freshness and gaps;
- whether separate transfer assessment is required, without deciding its legality.

Enforcement points include request routing, job scheduling, database placement, replication, export, key use, administrator access, deployment, and failover. Missing policy, unknown location, stale required evidence, or an incomplete dependency graph must follow the boundary’s explicit fail-closed behavior.

## 9. Dependency closure

A request is inside a boundary only if every material downstream component is permitted. The API must calculate and retain the evaluated dependency closure, including conditional and asynchronous paths.

The UIX should show the weakest dependency, affected data class, and exact path—for example `EU API → global queue → US telemetry sink`—rather than merely stating “outside region.” Unknown nodes and unverified edges are first-class risks, not silently ignored dependencies.

## 10. Storage, replication, deletion, and migration

The product must separately model primary storage, read replicas, backups, snapshots, caches, indexes, derived datasets, and deletion queues. Operators need:

- placement and replication validation before change;
- retention and deletion propagation status;
- migration plans with source, destination, temporary paths, freeze windows, rollback rules, and evidence;
- detection of orphaned copies and stale replicas;
- proof that a migration completed and the former location was handled according to policy.

## 11. Keys and administrative control

Sovereignty can fail even when ciphertext remains in-region. Rules must cover where keys are created, stored, used, rotated, escrowed, and recovered; which organization controls them; and where privileged operators can invoke key or data operations.

Administrative access should integrate with strong authentication, just-in-time authorization, session provenance, policy obligations, and immutable receipts. Emergency access must remain attributable, constrained, time-limited, and reviewable.

## 12. Failover and incident behavior

Every recovery candidate must be evaluated before activation. The system should support:

- precomputed failover eligibility;
- boundary-safe, degraded-service, and prohibited candidates;
- explicit customer or authority approvals where policy requires them;
- rehearsals and evidence-expiry warnings;
- emergency exceptions with fixed scope and expiry;
- post-incident review of decisions, enforcement, and residual copies.

The product must never silently trade sovereignty for availability.

## 13. API surface

Recommended resource groups:

- `/sovereignty/boundaries` and `/versions`
- `/sovereignty/component-rules`
- `/sovereignty/assignments`
- `/sovereignty/components` and `/dependencies`
- `/sovereignty/observations`
- `/sovereignty/evaluations` and `/decisions`
- `/sovereignty/receipts`
- `/sovereignty/drift`
- `/sovereignty/exceptions`
- `/sovereignty/failover-plans` and `/simulations`
- `/sovereignty/evidence-bundles`

Provide idempotency, pagination, optimistic concurrency, stable reason codes, bulk evaluation, dry-run simulation, event subscriptions, and scoped export. Read and mutation permissions must be separated. Sensitive topology and operator-location data require field-level protection and auditable access.

Existing residency contracts should remain compatible while adapters migrate them into the richer versioned model. Deprecation must be documented rather than silently changing current decision semantics.

## 14. Regional Boundary Control UIX

### Portfolio overview

Show boundaries, assigned tenants/workloads, verified coverage, stale evidence, active drift, exceptions, blocked operations, and failover readiness. Filters include tenant, realm, data class, provider, jurisdiction, environment, and assurance state.

### Boundary composer

Use guided, typed controls for each dimension. Present inherited defaults and overrides, validate contradictions, preview affected resources, and require a change rationale. Plain-language summaries must remain paired with the exact machine policy.

### Dependency map

Visualize processing and data paths across services and planes. Highlight unknown nodes, boundary crossings, asynchronous paths, external processors, and the weakest dependency. Offer an accessible tabular equivalent.

### Decision explorer

Search by correlation ID, tenant, resource, actor, region, result, or reason. Reconstruct inputs, boundary version, dependency snapshot, observations, obligations, enforcement receipts, and linked exception or transfer assessment.

### Drift and evidence workspace

Compare declared, configured, observed, and verified state. Group repeated symptoms by root component, show evidence source and freshness, assign remediation, suppress only with reason and expiry, and preserve history.

### Failover simulator

Compare candidate recovery regions, dependencies, service impact, boundary violations, required approvals, and evidence readiness before execution. The UI must make prohibited and unverified candidates unmistakable.

### Tenant-facing view

Expose entitled profiles, current assignment, material service limitations, verification timestamp, planned changes, and exception requests without exposing sensitive infrastructure topology.

## 15. Workflow and governance

Policy lifecycle: draft → validate → simulate → review → approve → schedule → enforce → observe → supersede or retire.

High-impact changes require separation of duties, diff review, affected-tenant preview, rollback plan, and an immutable approval record. Emergency activation is distinct from ordinary publication and triggers retrospective review.

Exceptions must never be permanent by default. They require an owner, narrow scope, justification, compensating controls, approval, start/end time, and automatic expiration. A technical exception that creates a possible cross-border transfer must link to—but not replace—the Transfer Assessment UIX.

## 16. Security, privacy, and reliability requirements

- Encrypt policy, topology, evidence, and receipts in transit and at rest.
- Apply tenant isolation and least-privilege field-level access.
- Integrity-protect decision and enforcement receipts; support signing where assurance warrants it.
- Minimize personal data, especially operator location and access evidence.
- Define evidence retention independently from raw telemetry retention.
- Prevent policy rollback, replay, confused-deputy use, and unauthorized version activation.
- Make policy evaluation deterministic for a captured input/version set.
- Define outage behavior for policy, topology, and observation services.
- Monitor evaluator latency, stale caches, missed events, graph incompleteness, and receipt gaps.

## 17. Instructions by delivery team

### Frontend engineer

Build reusable boundary-state badges, policy diff, dependency graph/table, decision timeline, evidence freshness, simulation comparison, approval, and exception components. Preserve correlation IDs and version links across views. Make large graphs progressively disclosed and keyboard accessible. Do not calculate authority or compliance status in the browser.

### UIX designer

Design around the four-state evidence model and the distinction between residency, sovereignty, transfer, and availability. Prioritize exception expiry, unknown dependencies, stale evidence, and failover impact. Test workflows with security, platform, privacy, support, and tenant-admin personas. Provide non-graph alternatives and color-independent severity cues.

### Copywriter

Use factual language: “processing observed in,” “boundary verified at,” “evidence stale,” and “transfer assessment required.” Avoid “fully sovereign,” “guaranteed compliant,” and legal conclusions. Explain denials with the violating component, policy, evidence state, and safe next action. Create role-sensitive copy for technical operators and tenant administrators.

### Backend and platform engineers

Define canonical typed contracts, versioning, reason codes, dependency snapshots, observation adapters, enforcement integrations, receipts, and outage semantics. Preserve current fail-closed behavior while expanding coverage. Add durable decision history, migrations, tenant isolation tests, adversarial tests, and deterministic replay tests.

## 18. Stakeholder enablement

- **Technical marketing:** publish an architecture demo showing declared versus observed state, dependency drift, a denied failover, and a verifiable remediation. Claims must match shipped enforcement and evidence coverage.
- **Developer relations:** provide quickstarts, policy examples, event schemas, an evaluation sandbox, local fixtures, failure scenarios, and integrations for schedulers, storage, keys, and telemetry.
- **Sales and account management:** use a capability matrix by provider, region, component type, and assurance level; document prerequisites, limitations, shared responsibilities, and rollout dependencies.
- **GTM strategy:** package baseline residency separately from advanced sovereignty evidence, customer-controlled keys, cross-provider boundaries, and regulated-workload operations.
- **Copywriting:** maintain a controlled glossary and approved/non-approved claim library shared by product, docs, demos, and sales materials.

## 19. Delivery phases

### Phase 1 — Honest foundation

Version existing zones and assignments; add durable decisions, stable reason codes, audit events, a boundary overview, decision explorer, and explicit declared/configured status.

### Phase 2 — Dependency and evidence

Add typed component rules, dependency closure, observations, evidence freshness, drift detection, receipts, storage/backup/log/key coverage, and simulations.

### Phase 3 — Operations and ecosystem

Add failover orchestration, migration proof, exception workflows, administrative-access controls, subprocessor adapters, tenant-facing views, and evidence bundles linked to transfer assessments.

## 20. Acceptance criteria

- A boundary can be versioned, reviewed, activated, superseded, and reconstructed historically.
- Assignments can target tenant, realm, workload, dataset/data class, purpose, and effective interval with deterministic precedence.
- Evaluations cover the full known dependency closure and expose unknown or stale elements.
- Storage, replicas, backups, logs, telemetry, keys, administration, subprocessors, and failover can be constrained separately.
- Every enforced allow, deny, or conditional result can link to a durable decision and receipt.
- Operators can simulate policy and failover changes before activation.
- Drift compares declared, configured, observed, and verified states without overstating compliance.
- Exceptions are scoped, approved, time-limited, automatically expired, and fully attributable.
- Transfer requirements link to a separate assessment; this API does not make legal determinations.
- Existing residency behavior remains covered by compatibility and regression tests.
- UIX meets keyboard, screen-reader, responsive, localization, and color-independent status requirements.
- Tenant isolation, field authorization, replay, stale-evidence, graph-incompleteness, outage, and performance tests pass.

## 21. Success measures

- percentage of protected workloads with complete dependency coverage;
- percentage of boundary decisions with fresh required evidence and matching receipts;
- time to detect and remediate regional drift;
- unknown-component and stale-evidence rate;
- prevented unauthorized placements, replication changes, administrative accesses, and failovers;
- exception count, age, expiry compliance, and recurrence;
- policy simulation-to-activation failure rate;
- decision latency and evaluator availability;
- time to answer a tenant or audit inquiry with a reconstructable evidence bundle.

Metrics measure control operation and evidence quality. They are not, by themselves, proof of legal compliance.

## 22. Non-claims and dependencies

Do not claim that the product guarantees sovereignty, establishes a lawful transfer mechanism, eliminates foreign legal access, or certifies compliance. Outcomes depend on deployment architecture, provider capabilities, accurate inventory, fresh observations, organizational controls, customer configuration, and legal interpretation.

Key dependencies include inventory and service graph sources, cloud/provider region metadata, storage and backup controllers, schedulers, key-management systems, privileged-access systems, audit pipelines, policy obligations and receipts, authorization provenance, delegation provenance, and the separate Cross-Border Transfer Authorization pairing.
