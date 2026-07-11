# Entitlement Governance API + Access Review UIX Requirements Brief

**Pairing:** `tigrbl-auth-api-entitlement-governance` + `@tigrbl-auth/access-review-uix`  
**Opportunity-map item:** 15  
**Primary buyers:** security, identity governance, compliance, internal audit, and application owners  
**Best-fit verticals:** regulated enterprise, financial services, healthcare, government, and B2B SaaS  
**Status:** proposed product surface built on existing repository primitives

## 1. Product Decision

Ship an entitlement-governance control plane that answers four questions with durable evidence:

1. What access exists, where did it come from, and who owns it?
2. Should that access still exist?
3. Who reviewed or approved it, using what evidence and policy?
4. Was unwanted access actually removed from every enforcement point?

The API owns entitlement cataloging, access packages, assignments, approval and expiry policy, certification campaigns, separation-of-duties analysis, orphan detection, remediation orchestration, and review evidence. The UIX turns those capabilities into operator, reviewer, resource-owner, auditor, and end-user workflows.

This surface governs access; it does not become a second authorization engine, directory, provisioning protocol, or audit store. It composes the existing policy, principal, delegation, relationship, SCIM, and audit packages.

## 2. Current Repository Reality

This pairing is not greenfield. The repository already contains:

- `EntitlementDefinition` and `EntitlementAssignment` contracts;
- durable `Entitlement` and `EntitlementAssignment` tables;
- durable `AccessReviewCampaign`, `AccessReviewItem`, and `AccessReviewDecision` tables;
- an executable `EntitlementManager` for definition, assignment, expiry, inventory, and revocation;
- an executable `AccessReviewWorkflow` for campaign creation, reviewer allocation, approve/revoke decisions, overdue escalation, and closure;
- revoke-on-review behavior and cross-tenant campaign rejection;
- unit and provisioning-governance ecosystem tests;
- roles, delegation grants, relationship graphs, SCIM users/groups, decision traces, and audit-event foundations.

The current implementation proves a domain slice, but it is not yet a production governance product. Important limitations include:

- in-memory capability workflow and durable tables are not yet one transactional service;
- no dedicated API or UIX package exists;
- entitlement definitions do not yet identify target system, resource, permission, risk, sensitivity, source, or fulfillment mechanism;
- assignments primarily address human subjects and do not fully normalize groups, clients, services, workloads, devices, agents, or nested derivation;
- campaigns store reviewer and item identifiers as JSON lists and lack immutable scoping snapshots;
- decisions are approve/revoke only and lack delegation, abstention, reassignment, exception, consultation, and confidence semantics;
- there is no access-package/request catalog;
- no first-class separation-of-duties policy or violation lifecycle exists;
- revocation records an intent but does not prove downstream deprovisioning;
- no connector health, reconciliation, bulk-scale, notification, export, or evidence-retention product surface exists.

Product language must distinguish **available primitive**, **integrated capability**, and **production-certified workflow**.

## 3. Users and Jobs

### Governance administrator

- Build a normalized entitlement catalog across applications and infrastructure.
- Assign owners, risk, review frequency, approval policy, and fulfillment method.
- Configure access packages, request policy, campaigns, escalations, and remediation.
- Find orphaned, stale, toxic, excessive, and unreviewed access.

### Reviewer or manager

- Understand why a subject has access and what the access enables.
- Review meaningful context without opening multiple systems.
- Approve, revoke, reduce, reassign, delegate, or request more information.
- Complete work efficiently without unsafe bulk approval.

### Application or resource owner

- Attest that catalog entries remain correct.
- Review direct and derived access to owned resources.
- resolve unmapped permissions and failed remediation.

### Auditor and compliance analyst

- Reconstruct campaign scope and every decision at the relevant point in time.
- Verify reviewer independence, deadlines, evidence, exceptions, and remediation.
- Export signed, reproducible evidence without exposing unnecessary personal data.

### Access requester and approver

- Find approved access packages using business language.
- See requirements, approvers, duration, conflicts, and data sensitivity before requesting.
- Track fulfillment, expiry, renewal, and revocation.

### Help desk, sales, and account management

- Diagnose access state without gaining authority to approve or alter it.
- Explain packaged governance capabilities and implementation dependencies accurately.

## 4. Architectural Ownership

### Entitlement Governance API owns

- entitlement metadata, ownership, risk, lifecycle, and source mappings;
- access packages and request/approval policy;
- normalized effective-access projections and derivation paths;
- assignment governance metadata and time bounds;
- campaign templates, immutable campaign snapshots, items, reviewer routing, decisions, exceptions, and attestations;
- SoD rules, simulations, violations, exceptions, and compensating controls;
- orphan/stale-access findings and remediation cases;
- fulfillment/remediation orchestration state and proof references;
- governance reporting and evidence bundles.

### Existing packages retain ownership

- `tigrbl-authz-policy`: runtime authorization semantics and decision traces;
- identity principals: canonical human and non-human principals;
- identity storage: durable tables, migrations, repositories, and transactions;
- delegation: who may act for whom and within what bounds;
- SCIM/directory provisioning: downstream user/group provisioning protocol behavior;
- security signals: continuous risk and status-change events;
- audit: canonical append-only security and operator events;
- tenant/platform admin APIs: tenant and platform administration outside governance.

### Boundary rules

- A governance approval is not itself runtime authorization.
- A campaign decision is not complete revocation until enforcement systems confirm removal.
- A catalog entry may map to roles, groups, scopes, permissions, relationships, credentials, or external accounts without replacing their source model.
- The UIX never talks directly to storage tables or external connectors.
- Tenant isolation is evaluated before ownership, reviewer, or entitlement logic.

## 5. Canonical Entitlement Model

An entitlement is a governed unit of access expressed in business and technical terms. Required fields:

- stable ID, tenant, name, description, status, version, and aliases;
- target system, environment, resource type, resource identifier, and action/permission;
- source system and immutable external identifier;
- owner and backup owner;
- data classification, privilege tier, business criticality, and risk score with rationale;
- assignment modes: direct, group, role, relationship, delegated, policy-derived, birthright, emergency, or external;
- requestability, approval policy, maximum duration, renewal policy, and review frequency;
- fulfillment and revocation adapters;
- last discovered, last reconciled, and last owner-attested timestamps;
- applicable policy, SoD, regulatory, and evidence-retention tags.

Catalog entries must be versioned. Historical campaigns resolve the exact version reviewed, even after current metadata changes.

## 6. Access Packages

An access package groups entitlements into a coherent job, project, partner, customer, or emergency-access offer.

Requirements:

- package name, audience, owner, purpose, entitlements, prerequisites, and lifecycle;
- eligibility policy based on tenant-safe principal attributes and relationships;
- one or more approval stages with escalation and fallback;
- requested and maximum duration;
- terms, training, license, agreement, device, authentication-assurance, or attestation prerequisites;
- automatic assignment and removal triggers;
- package-level and component-level SoD evaluation;
- simulation before publication;
- versioning and staged publication;
- renew, extend, reduce, and revoke workflows;
- no silent entitlement additions to active requests when a package version changes.

Birthright access must be explicit, explainable, periodically revalidated, and removable when qualifying conditions end.

## 7. Assignment and Effective-Access Model

Assignments must support human users, groups, clients, applications, services, workloads, devices, machines, and sponsored agents.

Each assignment records:

- subject, entitlement, tenant, source, status, and effective interval;
- direct or derived assignment type;
- derivation path through group, role, relationship, delegation, package, or policy;
- requester, assigner, approver, sponsor, and owner where applicable;
- business justification and ticket/change reference;
- authoritative source and fulfillment target;
- current reconciliation state;
- revocation intent, execution state, reason, and proof.

Effective access must be computed from a point-in-time graph, not inferred from a single flat row. The product must show duplicate paths so reviewers understand whether removing one path actually removes access.

## 8. Access Request and Approval

The API must support:

- catalog search and eligibility evaluation;
- request creation for self, eligible subordinate, service, workload, or sponsored agent;
- preflight SoD, risk, policy, and prerequisite checks;
- multi-stage approval with quorum or ordered stages;
- approver substitution constrained by delegation policy;
- timeout, escalation, cancellation, denial, expiration, and resubmission;
- fulfillment orchestration and verified completion;
- renewal and extension as new auditable decisions;
- idempotency and optimistic concurrency on all decisions.

Approvers must not approve their own requests unless an explicit, audited exception policy permits it.

## 9. Access Review Campaigns

Campaign types should include:

- manager review;
- application/resource-owner review;
- entitlement-owner metadata attestation;
- privileged and emergency-access review;
- group/role membership review;
- service, workload, device, and agent sponsor review;
- event-driven review after role, risk, employment, ownership, or policy change;
- micro-certification for one high-risk access change;
- continuous review queues backed by periodic evidence snapshots.

Campaign creation must freeze:

- selection query and resolved item set;
- entitlement and assignment versions;
- effective-access derivation paths;
- subject and reviewer facts relevant to the decision;
- applicable risk, SoD, and policy results;
- due dates, escalation rules, fallback behavior, and remediation policy.

Editing a live campaign must create a revision with explicit impact; it must never silently rewrite historical scope.

## 10. Reviewer Decisions

Supported decisions:

- approve/retain;
- revoke;
- reduce or replace access;
- set or shorten expiry;
- reassign item to an eligible reviewer;
- delegate under an active delegation grant;
- request information;
- abstain for conflict of interest;
- approve under a time-bound exception with compensating control.

Every decision includes reviewer identity, authority, authentication context, timestamp, reason code, optional free-text rationale, evidence viewed, policy warnings, conflict declaration, and item version.

Bulk decisions require homogeneous context, explicit item count, risk summary, exception exclusions, preview, and confirmation. High-risk and anomalous items should default to individual review.

## 11. Separation of Duties

The SoD service must model:

- static conflicts between entitlements, roles, packages, or business functions;
- dynamic conflicts based on action sequence, amount, resource, environment, or time;
- preventive checks during request, assignment, package publication, and policy change;
- detective scans over existing effective access;
- cross-system conflicts;
- severity, owner, rationale, scope, effective dates, and remediation guidance;
- time-bound exceptions with independent approval and compensating controls.

SoD evaluation must use effective access, including derived and delegated paths. A rule hit is a finding with an explainable trace, not automatic proof of misconduct.

NIST guidance emphasizes defining separated duties and reviewing privileges to validate continuing need; the product must make those controls testable rather than reducing them to a dashboard label.

## 12. Orphan, Stale, and Excessive Access

Detection must cover:

- entitlement without an accountable owner;
- assignment to a missing, disabled, terminated, or unresolvable subject;
- external account not linked to a canonical principal;
- group, role, application, service, workload, device, or agent without an owner/sponsor;
- access past expiry or no longer justified by source attributes;
- dormant access based on reliable last-use evidence;
- privileged access with no recent review;
- assignment whose source or derivation path no longer exists;
- catalog record no longer present in a source system;
- remediation request that never reached the enforcement target.

Findings require confidence, evidence freshness, source coverage, false-positive handling, assignment to an owner, SLA, and lifecycle. “Unused” must not be claimed when use telemetry is absent or incomplete.

## 13. Remediation and Revocation Proof

Revocation is a state machine:

`requested -> authorized -> dispatched -> acknowledged -> reconciled -> verified`

Alternative terminal states include `failed`, `partially_removed`, `superseded`, `exception`, and `manual_action_required`.

Proof may include:

- connector request/response digest;
- SCIM deletion or membership-update result;
- source-system change ID;
- post-change readback;
- effective-access graph recomputation;
- related token/session/credential invalidation results;
- timestamped audit-event references;
- signed evidence-bundle manifest.

A reviewer-facing “revoked” label may appear only after the product distinguishes decision, dispatch, and verified removal. Failed removal remains visible and escalated.

## 14. API Requirements

Provide versioned endpoints for:

- `/entitlements`, versions, mappings, ownership, and attestations;
- `/access-packages`, versions, simulations, and publication;
- `/assignments`, derivations, expiry, renewals, and revocation;
- `/requests`, approval steps, decisions, cancellation, and fulfillment;
- `/review-templates`, `/campaigns`, `/items`, decisions, delegation, escalation, and closure;
- `/sod/rules`, simulations, violations, exceptions, and compensating controls;
- `/findings` for orphan, stale, excessive, and failed-remediation cases;
- `/remediations`, attempts, acknowledgements, reconciliation, and proof;
- `/connectors`, capabilities, health, freshness, and coverage;
- `/reports` and `/evidence-bundles`.

All list endpoints require stable pagination, typed filtering, safe sorting, tenant-scoped search, and bounded export. All mutations require authorization, idempotency keys where retryable, version preconditions, audit correlation, and machine-readable errors.

High-volume campaign generation and remediation must run as asynchronous jobs with progress, checkpointing, cancellation, retry, and partial-failure visibility.

## 15. Connector and Event Strategy

Initial connectors should reuse:

- SCIM users, groups, and memberships;
- native Tigrbl roles, permissions, relationships, delegation grants, clients, services, workloads, devices, and agents;
- CSV/JSON import only as a controlled bootstrap path with provenance and validation;
- webhooks or Shared Signals events for changes requiring review or revocation.

Connector contracts must declare discovery, assignment, revoke, readback, event, and last-use capabilities independently. The UIX must not imply a connector can remediate simply because it can discover.

SCIM is a provisioning transport for Users, Groups, and extensible resources; it is not the governance model. Shared Signals can accelerate status changes and continuous evaluation; it does not replace authoritative reconciliation.

## 16. Access Review UIX

### Governance home

Show decision-ready posture:

- active high-risk access;
- overdue and escalating review items;
- orphaned resources and owners;
- open SoD violations;
- expiring access;
- failed or unverified remediation;
- connector freshness and coverage;
- campaign completion and reviewer workload.

Never collapse “no findings” and “no data.”

### Entitlement catalog

Provide owner, system, resource, permission, risk, requestability, assignment count, last discovery, review frequency, and mapping status. Detail view shows versions, effective access, packages, conflicts, findings, and evidence.

### Access package studio

Use a staged builder for audience, entitlements, eligibility, approvals, duration, prerequisites, SoD simulation, fulfillment, and publication. A diff view must expose changes between versions.

### Request experience

Use business language first, technical permission detail on demand. Preview approvers, duration, requirements, conflicts, and data sensitivity before submission. Status shows approval and fulfillment separately.

### Campaign builder

Support template selection, scope query, point-in-time preview, reviewer strategy, exclusion review, deadline, escalation, remediation mode, evidence policy, and launch confirmation. Estimate item counts and flag unowned or unreviewable items before launch.

### Reviewer inbox

Prioritize due date and risk. Each item shows:

- subject and relationship to reviewer;
- plain-language access impact;
- source and derivation paths;
- request/assignment justification;
- last review, reliable last use, expiry, and risk;
- SoD and anomaly context;
- duplicate paths and likely effect of revoke;
- decision controls with accessible keyboard operation.

### Campaign operations

Show completion, aging, reassignment, escalation, reviewer conflicts, excluded items, remediation progress, connector failures, and evidence readiness. Operators can intervene without changing recorded decisions.

### SoD and findings workbench

Provide rule authoring, graph-aware simulation, violations, exceptions, remediation, and owner workflows. Explain the exact conflicting access paths and why the rule matched.

### Auditor evidence room

Offer read-only campaign reconstruction, filters, manifests, decision and remediation chains, source freshness, policy versions, and export verification. Mask unrelated personal data.

## 17. Security, Privacy, and Reliability

- Enforce tenant isolation in storage, service, jobs, exports, caches, and connector credentials.
- Separate campaign administration, review, remediation, audit, and connector administration duties.
- Require step-up authentication for privileged bulk decisions, exception approval, and destructive remediation.
- Prevent self-review, circular review, and reviewer assignment through a conflicted chain unless explicitly governed.
- Make decisions append-only; corrections create linked superseding records.
- Encrypt connector credentials and sensitive evidence; never expose secrets in UI or exports.
- Minimize subject attributes and mask sensitive data by role and purpose.
- Preserve source timestamps and freshness so stale data cannot masquerade as current evidence.
- Use transactional outbox/idempotent consumers for remediation and event delivery.
- Reconcile after write; do not treat HTTP success as proof of access removal.
- Apply retention and legal-hold policy to evidence bundles.
- Generate accessible UI conforming to WCAG 2.2 AA, including dense tables and graph alternatives.

## 18. Stakeholder Requirements

### Technical marketing

Deliver a credible narrative around closed-loop governance: discover, understand, decide, remediate, verify. Build demos for quarterly certification, privileged-access review, orphan cleanup, and cross-system SoD. Every claim must identify whether the connector is simulated, native, or production-supported.

### Developer relations

Deliver API quickstarts, typed schemas, webhook/event examples, connector SDK guidance, seeded demo tenants, campaign fixtures, failure-mode examples, and end-to-end samples from discovery through verified revocation.

### Sales and account management

Provide a discovery worksheet covering systems, identities, entitlement volume, review cadence, regulations, ownership, connectors, remediation authority, evidence retention, and deployment. Provide a capability matrix that separates built-in, adapter-required, and roadmap functionality.

### GTM strategist

Package entry offers around access inventory and certification, then expand into request packages, SoD, continuous governance, and non-human identity review. Lead with evidence and time-to-decision; avoid claiming complete IGA parity until connectors, workflows, scale, and certifications support it.

### Copywriter

Create plain-language names for entitlements and consequences. Standardize `retain`, `revoke`, `reduce`, `decision recorded`, `remediation pending`, and `removal verified`. Avoid “safe,” “compliant,” “least privilege,” “unused,” and “revoked” unless the displayed evidence supports the statement.

## 19. Delivery Instructions

### Frontend engineer

- Build generated typed clients from the dedicated API contract.
- Implement route-, tenant-, and action-level authorization; hiding controls is not enforcement.
- Use server-side pagination/filtering and virtualized large lists.
- Preserve filters, selection, and safe resumability across reviewer sessions.
- Make every mutation expose pending, succeeded, partially succeeded, conflicted, and failed states.
- Require preview and explicit confirmation for bulk/high-impact operations.
- Keep decision entry usable without graphs; graphs are explanatory enhancements.
- Instrument completion, abandonment, latency, reassignment, and remediation outcomes without recording sensitive rationale.

### UIX designer

- Design first for the reviewer’s decision, then for campaign administration.
- Establish a visual grammar for source, derivation, risk, freshness, decision, and remediation state.
- Make direct versus inherited access and decision versus verified removal unmistakable.
- Design empty, no-data, stale-data, partial-coverage, degraded-connector, and conflict states.
- Test dense workflows with keyboard and screen-reader users.
- Use progressive disclosure so business reviewers are not forced to parse IAM internals.

### Copywriter

- Write catalog, request, review, exception, escalation, and remediation copy as one vocabulary system.
- Explain consequences before confirmation.
- Provide concise reason-code labels plus optional detail prompts.
- Write neutral conflict and anomaly language; do not imply wrongdoing.
- Include source freshness and coverage caveats wherever conclusions depend on incomplete data.

## 20. Delivery Phases

### Phase 1: Productize existing governance core

- unify contracts, durable tables, and capability workflows transactionally;
- ship entitlement/assignment APIs and catalog UIX;
- ship durable campaign snapshots, reviewer inbox, decisions, escalation, and audit;
- prove revoke decision versus verified removal states.

### Phase 2: Packages and closed-loop remediation

- access packages, requests, staged approvals, expiry, renewal;
- native and SCIM connector contracts;
- fulfillment, readback, reconciliation, retry, and remediation proof;
- evidence bundle export.

### Phase 3: SoD and effective-access intelligence

- normalized derivation graph;
- static and dynamic SoD rules, simulation, violations, and exceptions;
- orphan, stale, excessive, duplicate-path, and failed-remediation findings.

### Phase 4: Continuous and ecosystem governance

- event-driven micro-certifications and Shared Signals integration;
- non-human identity governance depth;
- connector SDK and partner catalog;
- high-scale campaigns, analytics, regional retention, and regulated evidence profiles.

## 21. Acceptance Criteria

### API and domain

- Existing entitlement/review behavior is served from durable transactional state.
- Every object and query is tenant-isolated, authorized, versioned where historical evidence requires it, and audited.
- Campaign scope is immutable and reconstructable at the reviewed point in time.
- Reviewer eligibility, delegation, self-review, conflict, deadline, and concurrency rules are enforced server-side.
- Effective access exposes every supported derivation path.
- SoD checks evaluate direct and derived access and return explainable traces.
- Expiry and revoke decisions trigger idempotent remediation.
- Verified removal requires downstream readback or an explicitly documented weaker proof level.
- Failed/partial remediation remains open and escalates.
- Exports include schema version, source freshness, manifest, and integrity digest.

### UIX

- A reviewer can understand and decide a standard item without leaving the inbox.
- Technical detail and evidence are available without overwhelming the default view.
- Bulk approval cannot include high-risk exceptions without explicit review.
- Campaign operators can distinguish scope, decisions, and remediation completion.
- No-data, stale, partial-coverage, and zero-finding states are visually distinct.
- All core workflows meet WCAG 2.2 AA and work by keyboard.

### Business and evidence

- Demo fixtures prove retain, revoke, expiry, escalation, SoD exception, orphan resolution, failed remediation, and verified removal.
- Marketing and sales claims map to tested capabilities and named connector maturity.
- An auditor can reproduce a completed campaign without database access.
- Success metrics are instrumented with privacy-preserving event definitions.

## 22. Success Measures

- median and 90th-percentile review completion time;
- percentage of campaigns completed by deadline;
- reviewer decision change/reversal rate;
- percentage of review items with complete source, owner, derivation, and freshness context;
- revoke-decision-to-verified-removal latency;
- remediation failure and retry rate;
- orphaned entitlement and assignment aging;
- percentage of high-risk assignments with current review;
- SoD violation time to disposition and exception aging;
- request fulfillment time and expiry enforcement rate;
- reviewer abandonment and support-contact rate;
- connector coverage and data freshness by governed system.

Metrics must segment by risk and connector capability; faster bulk approval alone is not a success signal.

## 23. Source Evidence

### Repository

- `docs/strategy/uix-pairing-briefs/10-additional-api-uix-opportunity-map.md`
- `docs/authorization-models-focus.md`
- `docs/strategy/identity-market-roadmap.md`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/governance/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/entitlement/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/entitlement_assignment/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/access_review_campaign/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/access_review_item/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/access_review_decision/`
- `pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/governance_extension.py`
- `tests/unit/test_governance_extension_plane_phase5.py`
- `tests/unit/test_provisioning_governance_ecosystem_boundary.py`

### Standards and primary guidance

- [NIST SP 800-171 Rev. 3](https://csrc.nist.gov/pubs/sp/800/171/r3/final): separation of duties and periodic privilege review guidance.
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final): account management, separation of duties, least privilege, and audit control families.
- [NIST SP 1800-35, Implementing a Zero Trust Architecture](https://www.nccoe.nist.gov/projects/implementing-zero-trust-architecture): identity governance as centralized access review, role, audit, and SoD support.
- [RFC 7643, SCIM Core Schema](https://datatracker.ietf.org/doc/html/rfc7643) and [RFC 7644, SCIM Protocol](https://datatracker.ietf.org/doc/html/rfc7644): interoperable user/group schemas and provisioning transport.
- [OpenID Shared Signals Framework](https://openid.net/wg/sharedsignals/): secure event streams for identity and security status changes.

## 24. Explicit Non-Claims

- Existing repository primitives do not yet constitute a production-ready IGA product.
- A completed review does not prove access removal without remediation evidence.
- SCIM support does not imply entitlement discovery or governance coverage for every target.
- Access-review records alone do not establish regulatory compliance.
- A policy or SoD match is not proof of malicious behavior.
- Lack of observed use is not proof that access is unused.
- This pairing does not replace a PAM vault, runtime authorization engine, HR system, ITSM system, SIEM, or external source of truth.
