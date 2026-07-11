# Regional Failover Authorization API + Sovereign Continuity UIX

- **Pairing:** 39
- **Status:** Proposed product brief
- **Primary owners:** Identity reliability, authorization, security, sovereignty, incident management, frontend, UIX, product copy
- **Adjacent pairings:** Regional Identity Plane API; Sovereignty Policy API; Sovereign Key Custody API

## 1. Product decision

Build a Regional Failover Authorization API and Sovereign Continuity UIX that decide whether a specific identity capability may move, resume, degrade, or expand authority during disruption—and prove that the resulting operation stayed within approved tenant, jurisdiction, key, policy, state, and recovery boundaries.

Failover must be treated as an authorization transition, not a load-balancer switch. A healthy alternate region is ineligible if it lacks authoritative state, approved key custody, issuer authority, sovereignty coverage, fencing guarantees, or required evidence.

The product must never silently exchange sovereignty, security, or consistency for availability.

## 2. Product boundary

This pairing governs continuity decisions and execution for identity-plane capabilities such as authentication, authorization, token/certificate issuance, validation, introspection, revocation, directory reads/writes, policy evaluation, administration, federation, and audit.

It does not replace:

- infrastructure disaster-recovery orchestration;
- business continuity planning;
- incident command;
- regional identity-plane topology;
- sovereignty or transfer policy;
- key recovery and custody;
- backup/restore engines.

It coordinates those systems through eligibility decisions, obligations, approvals, fencing, receipts, and post-event reconciliation.

## 3. Repository starting point

The repository has useful precursors but no failover product:

- realm/tenant isolation and deterministic issuer/JWKS boundaries;
- authorization-server, policy, key/version, rotation, revocation, session, token, federation, evidence, and audit foundations;
- residency decisions that fail closed outside allowed processing regions;
- runtime capability truth, readiness, degraded/blocked UI states, and qualification evidence;
- key-rotation emergency triggers and administrative audit hooks;
- architectural user journeys calling for backup, restore, and audit-safe break-glass.

Current gaps:

- no regional cell or continuity-plan contract in the existing runtime;
- no typed recovery objective, dependency, candidate, failure-domain, fencing, checkpoint, or failover decision;
- no precomputed eligibility or per-capability degraded-mode policy;
- no durable activation/recovery receipts, split-brain epochs, rejoin workflow, or state reconciliation;
- backup and restore intent is documented but not a governed product surface;
- break-glass is explicitly described as underframed and not productized;
- no Sovereign Continuity UIX.

This pairing depends on the Regional Identity Plane model proposed in pairing 38; it should not invent a parallel topology.

## 4. Users and jobs to be done

### SRE and identity platform teams

Precompute safe candidates, rehearse plans, initiate or automate authorized transitions, monitor execution, fence primaries, and reconcile restored cells.

### Security, sovereignty, and privacy teams

Approve constraints, verify emergency authority, ensure regional/key/data boundaries survive disruption, and review exceptions and evidence.

### Incident commanders

Understand customer and security impact, choose among eligible options, coordinate approvals, and retain an authoritative event timeline.

### Tenant administrators and account teams

Select entitled continuity profiles, approve customer-controlled options where contracted, receive accurate impact notices, and review tenant-scoped outcomes.

### Auditors and post-incident reviewers

Reconstruct detection, decision, approvals, fencing, state used, operations executed, exceptions, and recovery without relying on chat transcripts.

## 5. Core domain model

Introduce typed, versioned resources:

- `ContinuityProfile`: protected capabilities, priorities, RTO/RPO objectives, sovereignty constraints, degraded modes, automation level, and tenant entitlement.
- `ContinuityPlan`: source cell, candidate cells, capability/state/key dependencies, triggers, runbook, approvals, rollback/rejoin, and lifecycle.
- `FailureSignal`: source, affected component/domain, severity, confidence, observations, correlation, and expiry.
- `FailoverCandidate`: target cell, capabilities, authority, state checkpoint, key custody, boundary coverage, capacity, and current eligibility.
- `RecoveryCheckpoint`: state class, source, sequence/epoch, capture time, integrity, replication status, and restore verification.
- `FencingLease`: protected authority, holder, epoch/term, issue/expiry, quorum, enforcement points, and evidence.
- `FailoverEvaluation`: incident/request context, candidates, rejected reasons, impacts, obligations, and policy versions.
- `FailoverAuthorization`: exact capabilities/tenants, target, mode, checkpoint, keys, approvals, start/end, and revocation.
- `ContinuityOperation`: drain, fence, restore, promote, route, degrade, validate, roll back, reconcile, or rejoin.
- `ContinuityReceipt`: operation request, authorization, actual target/state/key/epoch, enforcement result, and integrity proof.
- `ContinuityException`: narrow deviation, compensating controls, customer/legal links, expiry, and retrospective review.
- `ReconciliationCase`: divergent state, authoritative winner, merge/discard plan, affected artifacts, approvals, and proof.

Every plan and execution references immutable topology, policy, key, state-schema, and runbook versions.

## 6. Capability-specific continuity

Do not use one failover switch for the whole identity plane. Define modes per capability:

- authentication with local authenticators versus upstream federation;
- authorization using fresh or last-known-good policy/attributes;
- access/ID token issuance and signing authority;
- refresh-token and authorization-code redemption;
- introspection, revocation, and resource-server validation;
- session creation, continuation, logout, and global revocation;
- credential enrollment, reset, recovery, and deletion;
- directory/profile read and write;
- client, policy, key, tenant, and realm administration;
- certificate/attestation issuance;
- audit/event capture and delivery.

Each mode is `full`, `restricted`, `read-only`, `validation-only`, `queued`, `local-only`, or `unavailable`, with explicit security and user effects.

## 7. Candidate eligibility

A candidate is eligible only when all required conditions hold:

- regional cell and component health are current;
- issuer and authority partition permit the operation;
- source is fenced or the operation is proven safe under concurrent authority;
- state checkpoint satisfies capability-specific freshness and integrity;
- key versions, custody, HSM/module, and JWKS publication are approved;
- policy, consent, entitlement, revocation, replay, and risk state meet staleness limits;
- sovereignty, jurisdiction, transfer, and tenant/realm constraints pass;
- required network, DNS, dependencies, capacity, telemetry, and audit are ready;
- runbook, evidence, rehearsal, approvals, and exception state are valid.

Eligibility expires. It must be reevaluated immediately before activation and continuously during the event.

## 8. RTO, RPO, and security objectives

RTO and RPO are targets, not guarantees. Define them by capability and state class, alongside:

- maximum policy/attribute/revocation/key/trust-bundle staleness;
- maximum authentication or session assurance degradation;
- acceptable lost, duplicated, replayed, or delayed operations;
- maximum emergency authorization duration;
- audit/evidence continuity objective;
- maximum time without authoritative fencing confirmation.

A candidate can meet infrastructure RTO while failing identity security objectives. The UI must show both.

## 9. Fencing and split-brain prevention

Promotion of authoritative writes or minting requires a fencing proof appropriate to the architecture:

- epoch/term lease with monotonic enforcement;
- quorum-issued ownership token;
- provider control-plane isolation;
- cryptographic signing/key-use disablement;
- database/write-leader fencing;
- issuer or routing authority withdrawal.

Network unreachability is not proof that the primary is stopped. Every issuing, state-writing, routing, and key-use enforcement point must reject stale epochs. If fencing cannot be proven, policy should prefer validation-only, read-only, or unavailable modes over dual authority.

## 10. State safety and checkpoint selection

Checkpoint evaluation covers schema version, completeness, integrity, tenant/realm filters, encryption/key access, sequence/epoch, lag, deletion/revocation propagation, replay state, and restore testing.

The system must identify likely effects of staleness:

- replay of authorization codes, refresh tokens, nonces, or credentials;
- acceptance of revoked sessions, grants, certificates, keys, or principals;
- loss of consent, policy, delegation, or risk changes;
- duplicate identifiers or conflicting writes;
- missing audit/evidence events.

Risky state must not be labeled “healthy” merely because restoration succeeded technically.

## 11. Degraded modes

Plans should prefer narrow, explicit degradation over blanket activation. Examples:

- validate already issued tokens but stop minting;
- allow low-risk authentication while disabling enrollment/recovery;
- serve directory reads while queueing writes;
- honor only cached policy within a strict age and scope;
- reject refresh redemption while allowing short remaining access-token validity;
- restrict administrative changes and emergency delegation;
- issue shorter-lived, audience-restricted, proof-bound tokens with enhanced receipts.

Every degraded mode has an owner, maximum duration, user copy, telemetry, exit condition, and post-event reconciliation requirement.

## 12. Automation and approvals

Support three modes:

- **manual:** system recommends; authorized humans approve and execute;
- **guarded automatic:** pre-approved trigger and eligible plan execute automatically within exact bounds;
- **human-confirmed automatic:** the system validates and prepares; an authorized quorum activates.

Automation never widens plan scope. High-impact actions require separation of duties, phishing-resistant authentication, request-bound approvals, and short expiry. Emergency access remains attributable and cannot bypass fencing, tenant isolation, key custody, or immutable receipts.

## 13. Execution lifecycle

Lifecycle: detect → correlate → assess → select plan → evaluate candidates → authorize → fence → restore/synchronize → validate → promote → route → monitor → recover source → reconcile → rejoin or retire → review.

Each transition has preconditions, idempotency, timeout, compensation/rollback where safe, evidence, and a responsible owner. Partial failure must resume from observed state rather than rerunning destructive steps blindly.

## 14. Reconciliation and rejoin

Restored primary cells cannot simply return to service. Rejoin requires:

- confirmation of fencing and authority epochs;
- inventory of divergent writes and issued artifacts;
- revocation/replay/key/policy reconciliation;
- schema and migration compatibility;
- tenant/realm isolation validation;
- sovereignty and custody verification;
- decision on merge, discard, revoke, reissue, or notify;
- staged read then write admission;
- post-event evidence completeness.

Irreconcilable state becomes a durable case with explicit customer/security impact.

## 15. API surface

Recommended resources:

- `/continuity/profiles`
- `/continuity/plans` and `/versions`
- `/continuity/failure-signals` and `/incidents`
- `/continuity/candidates`
- `/continuity/checkpoints`
- `/continuity/fencing-leases`
- `/continuity/evaluations`
- `/continuity/authorizations`
- `/continuity/operations` and `/receipts`
- `/continuity/degraded-modes`
- `/continuity/exceptions`
- `/continuity/reconciliation-cases`
- `/continuity/rehearsals` and `/evidence-bundles`

Support idempotency, optimistic concurrency, dry-run simulation, exact-scope approvals, event subscriptions, stable reason codes, effective-time queries, resumable operations, and scoped exports. Separate plan authoring, incident command, approval, execution, tenant view, audit, and exception permissions.

## 16. Sovereign Continuity UIX

### Readiness portfolio

Show protected tenants/capabilities, eligible candidates, RTO/RPO posture, last rehearsal, checkpoint freshness, fencing readiness, key/sovereignty verification, open exceptions, and uncovered dependencies.

### Plan composer

Guide capability modes, dependencies, targets, triggers, approvals, fencing, state checkpoints, key requirements, degraded behavior, communications, rollback, rejoin, and evidence. Validate contradictions and simulate before approval.

### Incident command view

Provide one authoritative timeline, affected scope, signal confidence, current authority holder, candidate comparison, customer/security impact, approvals, running operations, receipts, and next safe actions.

### Candidate comparison

Compare authority, sovereignty, keys, state freshness, capacity, dependencies, RTO estimate, degraded capabilities, risks, evidence, and blockers. Do not rank an ineligible candidate as “recommended.”

### Fencing and promotion control

Make source authority, epoch, enforcement points, quorum, expiry, and verification explicit. Use deliberate confirmation for irreversible/high-impact transitions and prevent stale-page activation.

### Rehearsal lab

Run synthetic or isolated simulations, inject dependency failures, compare expected/observed outcomes, capture timings and receipts, and turn findings into plan changes without affecting production.

### Reconciliation and review

Show divergent state, issued artifacts, affected tenants, disposition options, owners, evidence gaps, customer notices, exceptions, and corrective actions.

## 17. Security, privacy, and reliability

- Tenant/realm-isolate plans, checkpoints, incidents, decisions, and receipts.
- Use strong, just-in-time, quorum-controlled authority for high-impact operations.
- Integrity-protect plans, signals, approvals, epochs, checkpoints, operations, and receipts.
- Prevent replay, stale approvals, split-brain minting, version substitution, scope widening, and confused-deputy execution.
- Keep incident/topology/operator information restricted and redact tenant-facing views.
- Define behavior when the continuity control service itself is impaired; pre-authorized local controls remain bounded and auditable.
- Test network partitions, clock skew, malicious health signals, delayed fencing, stale backups, lost audit sink, provider control-plane failure, and repeated transition attempts.

## 18. Instructions by delivery team

### Frontend engineer

Build reusable readiness, candidate comparison, capability-mode matrix, timeline, checkpoint, fencing/epoch, quorum, operation progress, receipt, reconciliation, simulation, and evidence components. Use live server state and concurrency tokens for every action; never infer eligibility in the browser.

### UIX designer

Design for high-pressure accuracy: clear authority holder, exact scope, reversible versus irreversible actions, blockers, degraded effects, and next safe step. Avoid optimistic green dashboards that collapse security and availability. Test partitions, uncertain signals, rejected candidates, partial execution, and rejoin.

### Copywriter

Use “candidate eligible at,” “primary fencing unverified,” “validation-only mode,” “checkpoint exceeds policy,” and “authorization expires.” Avoid “disaster-proof,” “zero downtime,” “automatic recovery,” or “no data loss” unless qualified by exact capability, objective, and evidence.

### Backend and reliability engineers

Define canonical continuity contracts, deterministic eligibility, fencing epochs, idempotent resumable operations, receipts, checkpoint verification, and reconciliation. Integrate rather than duplicate regional topology, sovereignty, keys, policy, authorization provenance, and incident systems.

## 19. Stakeholder enablement

- **Technical marketing:** demonstrate an ineligible geographically healthy target, a safe validation-only mode, verified fencing, promotion, and reconciliation using synthetic data.
- **Developer relations:** provide local multi-cell failure labs, plan schemas, signal/event contracts, idempotency examples, degraded-mode SDK behavior, and chaos-test fixtures.
- **Sales and account management:** maintain capability-specific regional coverage, objectives, prerequisites, customer approvals, exclusions, shared responsibilities, and rehearsal options.
- **GTM strategy:** separate basic backup/restore from governed regional continuity, sovereign failover, tenant-dedicated plans, automated evidence, and premium recovery exercises.
- **Copywriting:** maintain continuity claim qualifiers, incident templates, degraded-mode user messages, migration/recovery notices, and post-event summaries.

## 20. Delivery phases

### Phase 1 — Plans and readiness

Add profiles, plans, candidates, dependency/readiness checks, checkpoints, rehearsals, evidence, and read-only UI on top of pairing 38 topology.

### Phase 2 — Authorized execution

Add evaluations, exact-scope approvals, fencing leases, idempotent operations, degraded modes, routing integration, receipts, and incident timeline.

### Phase 3 — Automated assurance

Add guarded automation, continuous eligibility, chaos rehearsal, cross-provider recovery, reconciliation workflows, tenant views, and evidence bundles.

## 21. Acceptance criteria

- Continuity is defined per tenant/realm, capability, state class, and target—not by a global region switch.
- Candidate eligibility covers authority, fencing, keys, state, sovereignty, policy, dependencies, capacity, evidence, and approvals.
- Network loss alone cannot satisfy fencing.
- Stale epochs are rejected by issuing, writing, routing, and key-use enforcement points.
- Degraded modes have exact capabilities, restrictions, maximum durations, user impact, and exit criteria.
- Every activation is scope-bound, time-bound, attributable, idempotent, and linked to actual operation receipts.
- Partial execution resumes safely from observed state.
- Rejoin requires state/artifact reconciliation and staged authority admission.
- Rehearsals prove technical and governance steps without mutating production authority.
- Exceptions automatically expire and trigger retrospective review.
- Existing issuer, tenant/realm, key, policy, residency, and security tests remain passing and expand to continuity cases.
- UIX meets keyboard, screen-reader, responsive, localization, and color-independent status requirements.
- Partition, replay, concurrency, stale checkpoint, malicious signal, outage, rollback, and performance tests pass.

## 22. Success measures

- percentage of protected capabilities with at least one currently eligible candidate;
- rehearsal freshness and plan success rate;
- detection-to-decision, decision-to-fence, fence-to-service, and service-to-reconciliation times;
- RTO/RPO/security-objective attainment by capability;
- blocked unsafe promotion attempts;
- split-brain duration and stale-epoch rejection count;
- operations with matching authorization and receipts;
- exception count, age, recurrence, and expiry compliance;
- reconciliation case age and affected artifacts;
- time to produce a tenant-scoped continuity evidence bundle.

These are operational measurements, not guarantees of availability, data preservation, sovereignty, or compliance.

## 23. Authoritative design references

- [NIST SP 800-34 Rev. 1, Contingency Planning Guide](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final)
- [NIST SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST SP 800-207A, Zero Trust for Cloud-Native Multi-Location Applications](https://csrc.nist.gov/pubs/sp/800/207/a/final)
- [NIST SP 1800-35, Implementing a Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/1800/35/final)

These references inform planning, policy decision/enforcement separation, monitoring, and multi-location security. Product objectives and claims require architecture-specific testing.

## 24. Non-claims and dependencies

Do not claim guaranteed RTO/RPO, zero downtime, zero data loss, automatic legal authorization, perfect split-brain prevention, or compliance certification. Outcomes depend on architecture, providers, networks, state semantics, keys, accurate signals, tested plans, human response, enforcement, and customer configuration.

Dependencies include Regional Identity Plane, Sovereignty Policy, Jurisdiction-Aware Authorization, Cross-Border Transfer Authorization, Sovereign Key Custody, policy obligations and receipts, authorization/delegation provenance, session/token/revocation stores, audit/evidence, runtime qualification, provider orchestration, DNS/routing, incident management, backup/restore, and communications systems.
