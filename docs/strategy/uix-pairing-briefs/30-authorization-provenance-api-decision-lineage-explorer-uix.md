# Authorization Provenance API + Decision Lineage Explorer UIX Requirements Brief

**Pairing:** `tigrbl-auth-api-authorization-provenance` + `@tigrbl-auth/decision-lineage-explorer-uix`  
**Additional opportunity:** Authorization/delegation/sovereignty extension 1  
**Primary buyers:** security engineering, authorization platform teams, application owners, audit/compliance, incident response, and regulated operations  
**Status:** proposed product surface; deterministic trace, replay, policy, authority graph, token persistence, and audit foundations exist

## 1. Product Decision

Build a dedicated authorization provenance plane that records and explains how an authorization request became a decision and what happened after that decision.

The product must answer:

1. What normalized request was evaluated?
2. Which verified facts and source versions were used?
3. Which policies, roles, relationships, grants, and authority paths participated?
4. Which rules matched, failed, conflicted, or were skipped?
5. Which decision and obligations were produced?
6. Which token, session, resource call, or enforcement event consumed the decision?
7. Can the decision be reproduced under the original state?
8. How would the result differ under another policy or fact version?

The API owns durable, integrity-protected decision lineage, replay, comparison, export, and retention. The UIX provides search, explanation, replay, drift analysis, incident investigation, and evidence reconstruction.

This is not merely an audit-log viewer. Audit records state that events occurred; authorization provenance represents the causal inputs, derivations, authority, policy, and outputs of a decision.

## 2. Current Repository Reality

The repository already contains meaningful foundations:

- `AuthorizationDecisionTrace` with `request_hash`, `policy_hash`, `derivation_hash`, and stable `decision_key`;
- deterministic canonical JSON and hashing;
- `build_authorization_decision_trace` and `build_delegation_provenance` in a dedicated provider package;
- a provenance provider base and capability map;
- token-exchange integration that binds subject, actor, resource, audience, scope, sender constraint, and exchange mode;
- persisted token-record claims containing authorization trace and delegation lineage;
- audit correlation from token exchange to stable request hashes;
- policy decision engine, decision traces, policy versions, obligations, authority derivation graphs, and least-authority diffs;
- policy replay cases, determinism reports, and cross-version decision stability comparisons;
- accepted SSOT specifications for trace reproducibility and policy stability;
- tests proving deterministic results, persistence, actor-sensitive delegation lineage, reference integrity, and runtime regressions.

The current implementation is not yet a general authorization-provenance product:

- the concrete builder is shaped primarily around OAuth token exchange rather than every PDP/PEP and product API decision;
- request and policy views contain a limited set of fields and do not model typed fact-source provenance;
- traces are embedded in token claims rather than represented by a canonical durable decision store;
- there is no dedicated trace table, evaluation-step model, external fact-read record, obligation/enforcement linkage, or immutable evidence bundle;
- no network API or UIX exists for authorized search, explanation, replay, or comparison;
- redaction, retention, legal hold, integrity sealing, regional placement, and export policy are not productized;
- current deterministic replay primitives do not freeze every historical attribute, relationship, policy artifact, resolver, and engine version needed for complete reproduction.

Product messaging must distinguish **deterministic trace construction**, **durable decision lineage**, **historical replay**, and **proof of enforcement**.

## 3. Relationship to Existing Pairings

### Authorization Decision API + Policy Studio

Policy Studio authors, tests, approves, and deploys authorization policy. The decision API evaluates live requests. Authorization Provenance receives decision artifacts and reconstructs why they occurred.

Policy Studio may embed provenance views, but it must call this API rather than own a second trace model.

### Delegation Provenance API

Delegation provenance owns actor/subject chains, grant parentage, attenuation, token exchange, and revocation propagation. Authorization provenance links the delegation lineage used by a decision without duplicating it.

### Policy Obligation and Enforcement Receipt API

Authorization provenance records obligations produced by the PDP and references enforcement receipts. It must not mark an obligation fulfilled merely because it was returned.

### Audit and Security Signals

Audit owns append-only security and operator events. Security Signals owns risk/status event transport. Provenance links their IDs as inputs or outcomes and preserves their source/time semantics.

### Trust Registry and Sovereignty

Trust and sovereignty services supply versioned facts such as recognized authority, jurisdiction, residency, processing region, and transfer constraints. Provenance records which decisions and versions were used.

## 4. Users and Jobs

### Application and resource-server developer

- Find why a request was permitted or denied.
- See the exact action/resource vocabulary and facts supplied to the PDP.
- distinguish application/PEP errors from policy decisions.
- reproduce a problem safely in a non-production workspace.
- verify that the PEP received and enforced the intended decision version.

### Policy engineer

- Inspect rule evaluation and authority derivation.
- compare decisions across policy versions.
- identify unreachable, shadowed, conflicting, overly broad, or unstable policy.
- test a proposed policy against historical-safe cases.

### Security analyst and incident responder

- search decisions by principal, credential, resource, action, policy, grant, session, token, region, device, workload, or incident;
- trace compromise impact and suspect decisions;
- identify use of stale/revoked facts, grants, keys, or policy;
- preserve and export evidence.

### Auditor and compliance analyst

- reconstruct privileged or regulated decisions at the relevant point in time;
- verify separation of policy author, approver, deployer, requester, and enforcer;
- validate retention, integrity, redaction, and enforcement evidence;
- sample decisions without receiving excessive personal or resource data.

### Support engineer and account manager

- explain safe reason categories and correlation state without gaining access to confidential trace facts;
- determine whether an issue belongs to identity, policy, application, data, or enforcement teams.

## 5. Architectural Ownership

### Authorization Provenance API owns

- trace ingestion and normalization;
- canonical decision lineage and integrity identifiers;
- versioned references to policies, facts, authority paths, delegation, and resolver calls;
- durable decision, step, input, output, and linkage records;
- privacy-aware projection and redaction;
- historical replay, counterfactual comparison, and stability analysis;
- token/session/request/enforcement linkage;
- evidence bundles, integrity manifests, retention, and legal hold;
- lineage queries, impact analysis, and Decision Lineage Explorer APIs.

### Authorization Decision API owns

- live request normalization and evaluation;
- permit/deny/indeterminate behavior;
- rules, combining, obligations, safe reasons, latency, and cache directives;
- synchronous response to the PEP.

### Storage owns

- schemas, repositories, transactions, migrations, indexes, partitioning, and retention execution;
- not provenance meaning or replay semantics.

### PEP/resource server owns

- enforcement of the decision and obligations;
- generation of a separate enforcement receipt or failure record;
- never rewriting the PDP decision artifact.

## 6. Provenance Model

The canonical model should align conceptually with W3C PROV’s entities, activities, agents, derivation, attribution, and delegation while using a bounded product schema rather than requiring RDF internally.

### Provenance entities

- normalized authorization request;
- verified identity/credential context;
- subject/resource/action/context fact snapshots;
- policy bundle and individual policy/rule versions;
- role, permission, assignment, relationship, delegation, trust, risk, residency, and classification versions;
- decision and obligations;
- token/session/grant derived from the decision;
- enforcement receipt and resource outcome;
- replay and comparison report.

### Provenance activities

- request normalization;
- fact resolution;
- authority derivation;
- policy/rule evaluation;
- combining and conflict resolution;
- decision issuance;
- token/session projection;
- PEP enforcement;
- replay/comparison;
- invalidation or correction.

### Provenance agents

- requesting actor and represented subject;
- PDP/engine and version;
- policy author/approver/deployer;
- fact-source service;
- PEP/resource server;
- operator or auditor running replay/export.

## 7. Canonical Decision Record

Each decision record requires:

- opaque decision ID and stable decision key;
- tenant, realm/trust domain, environment, and regional partition;
- correlation, request, session, transaction, and incident IDs;
- timestamp, duration, expiry/cache deadline, and clock-source status;
- normalized subject/resource/action/context references;
- actor/subject and delegation-lineage references;
- request schema/version and canonical request hash;
- policy bundle/version/hash and engine/runtime version;
- fact snapshot set/hash and source freshness summary;
- derivation graph root/hash;
- effect: permit, deny, indeterminate, challenge, or profile-defined result;
- safe reason categories and protected reason references;
- obligations/advice and their status references;
- proof/sender-binding context;
- integrity seal, supersession/correction, retention, and legal-hold state.

The stable decision key identifies equivalent normalized inputs and policy state. The unique decision ID identifies a particular evaluation occurrence.

## 8. Input Fact Provenance

Every decision-relevant fact must record:

- fact type and schema version;
- subject/resource/context association;
- normalized or derived value representation;
- source system, resolver, and source record/version;
- observed/effective/expiry times;
- confidence or verification status where meaningful;
- privacy classification and redaction policy;
- canonical digest;
- cache status and retrieval outcome;
- transformation/normalization steps;
- conflicts, missing values, and fallback behavior.

Examples include:

- principal and tenant status;
- authentication assurance and recency;
- device/workload attestation;
- role and entitlement assignments;
- relationship tuples;
- delegation grants and attenuation proofs;
- risk/security signals;
- resource owner/classification;
- purpose, jurisdiction, residency, and transfer policy;
- time, network, transaction value, and environment.

A raw value must not be retained merely because it was evaluated. Prefer typed outcome, digest, protected reference, and source version when full replay does not require the value.

## 9. Evaluation-Step Model

Each trace step records:

- stable step ID and parent/ordering relation;
- evaluator type, implementation/version, and configuration;
- policy/rule/graph edge reference;
- declared inputs and output digest;
- outcome: matched, not matched, failed, skipped, unavailable, or short-circuited;
- safe reason and protected diagnostic reference;
- duration, cache, timeout, retry, and dependency status;
- obligations/advice emitted;
- error classification without secrets or unsafe internals.

Short-circuit and combining behavior must be explicit. A missing step cannot be displayed as a failed rule unless it was actually evaluated.

## 10. Authority Derivation Lineage

The trace must connect effective authority to its sources:

- direct assignment;
- role/permission inheritance;
- group or entitlement membership;
- relationship path;
- delegation grant and attenuation proof;
- trust-framework mandate;
- platform/system authority;
- emergency/break-glass exception;
- policy-derived or contextual authority.

For permit decisions, identify the minimal supporting path or paths and any broader/excess authority discovered. For deny decisions, identify failed requirements without leaking hidden resource or relationship existence.

Cycles, depth limits, fan-out limits, duplicate paths, stale edges, and revocation freshness must be recorded.

## 11. Policy and Combining Lineage

Record:

- policy set/bundle and immutable versions;
- target match and applicability;
- individual rule results;
- priority and combining algorithm;
- explicit deny/permit precedence;
- defaults and missing-data semantics;
- conflicts and resolution;
- obligations/advice derivation;
- rollout cohort/feature flag;
- compatibility/schema and engine version.

The API must support structured rule references even when policy languages differ. It must not require or expose arbitrary policy source to every trace reader.

## 12. Decision-to-Outcome Linkage

Link decisions to:

- OAuth authorization code, token, refresh-token family, or token exchange;
- session or authentication transaction;
- credential/lease/certificate issuance;
- application request and resource operation;
- agent/tool action;
- access-review/remediation action;
- deployment/admission decision;
- PEP enforcement receipt;
- business/resource outcome where explicitly instrumented.

Use hashes or opaque IDs for bearer artifacts; never store raw access/refresh tokens, API keys, cookies, secrets, or DPoP private material.

Decision lineage must distinguish:

- `decision_issued`;
- `decision_delivered`;
- `decision_enforced`;
- `obligations_fulfilled`;
- `operation_succeeded`.

These are not interchangeable claims.

## 13. Historical Replay

Replay reconstructs an evaluation using a declared mode:

### Exact historical replay

Uses frozen request, fact snapshots, policy artifacts, evaluator versions, schemas, and combining behavior. It answers whether the recorded decision is reproducible.

### Current-engine compatibility replay

Uses historical request/facts/policy with the current compatible engine. It detects behavioral drift.

### Current-state replay

Re-evaluates the historical request against current facts and policy. It answers what would happen now, not what should have happened then.

### Counterfactual replay

Changes explicitly selected inputs or a proposed policy version in an isolated workspace. It supports impact analysis but is not production evidence of an actual decision.

Every report names its mode, substitutions, missing artifacts, deterministic status, and limitations. Replays must never invoke live mutations or production side effects.

## 14. Decision Comparison and Drift

Compare by:

- policy version;
- engine/runtime version;
- fact snapshot/current facts;
- delegation or relationship state;
- regional/sovereignty context;
- risk/assurance state;
- PEP/enforcement version.

Return:

- unchanged versus changed effect;
- changed authority paths;
- changed rules/combining result;
- changed facts and freshness;
- obligation additions/removals;
- affected principals/resources/actions;
- confidence and incomplete-comparison warnings.

Bulk historical replay must use representative, privacy-safe sampling and strict resource budgets. It cannot become an unrestricted subject/resource enumeration mechanism.

## 15. Trace Ingestion

Support:

- synchronous trace envelope returned alongside an authorization result;
- asynchronous append through transactional outbox;
- SDK/sidecar collection from embedded PDPs;
- protocol adapters for OAuth/OIDC/token issuance;
- PEP enforcement receipt ingestion;
- controlled import of legacy audit decisions.

Requirements:

- authorization response must not wait on remote provenance persistence when a local durable outbox is available;
- failed provenance delivery is observable, retried, and reconciled;
- trace events are idempotent and ordered per decision;
- collector identity and schema version are authenticated;
- server recomputes/validates canonical hashes where possible;
- imported legacy records are labeled partial and cannot claim replayability.

## 16. API Requirements

Provide versioned endpoints for:

- `/decisions` and `/decisions/{decision_id}`;
- `/decisions/{decision_id}/lineage`;
- `/decisions/{decision_id}/facts` with authorized projections;
- `/decisions/{decision_id}/steps`;
- `/decisions/{decision_id}/authority-paths`;
- `/decisions/{decision_id}/delegation` as a linked projection;
- `/decisions/{decision_id}/tokens-sessions-outcomes`;
- `/decisions/{decision_id}/enforcement`;
- `/search` with bounded, tenant-safe filters;
- `/replays`, jobs, results, and cancellation;
- `/comparisons` and decision-stability reports;
- `/impact` for policy/fact/grant/credential incidents;
- `/exports` and integrity manifests;
- `/retention`, legal hold, and deletion/tombstone operations;
- `/ingest` for authenticated internal producers.

API behavior:

- opaque cursor pagination and bounded time windows;
- field-level authorization and projection;
- stable reason codes and schema versions;
- asynchronous jobs for replay, impact, and export;
- idempotency and optimistic concurrency for holds/corrections;
- no general raw-query language over confidential trace data;
- no mutation of recorded decisions; corrections are linked supersessions.

## 17. Query and Enumeration Safety

Decision traces can expose whether subjects, resources, relationships, policies, or incidents exist. Therefore:

- enforce tenant/resource-owner/support/auditor scopes independently;
- restrict subject/resource search to authorized domains;
- use exact-match or approved indexes for sensitive identifiers;
- prevent timing/count differences from leaking hidden records where practical;
- rate-limit and monitor bulk exploration;
- redact denied-resource details according to the original disclosure policy;
- apply export approvals and purpose limitations;
- prohibit unrestricted joins across tenants, customers, or identity domains.

## 18. Privacy, Redaction, and Retention

Define trace fields as:

- public/safe operational metadata;
- tenant-confidential;
- security-sensitive;
- personal/special-category data;
- secret/prohibited.

Controls:

- store normalized categories, digests, and references instead of raw values where possible;
- tokenize/pseudonymize searchable identifiers with tenant-specific keys;
- redact tokens, credentials, secrets, full request bodies, sensitive resource content, and unnecessary attributes;
- separate protected evidence from the searchable trace index;
- support purpose-bound access, reason capture, legal hold, retention, deletion, and tombstoned integrity references;
- prevent exported evidence from becoming a shadow identity/data warehouse;
- record region/residency and cross-border movement of trace data;
- disclose that exact replay may be impossible after lawful deletion or source expiry.

## 19. Integrity and Evidence

Each trace/evidence bundle should include:

- canonical schema and normalization versions;
- record and segment digests;
- ordered event sequence;
- policy/fact/authority/delegation references and digests;
- decision and outcome references;
- collector/PDP/PEP identities;
- issued/effective/recorded times;
- integrity signature or seal;
- previous-segment/checkpoint link where configured;
- retention/hold/correction metadata;
- export manifest and verification instructions.

Use append-only storage and independently protected checkpoints for high-assurance deployments. “Tamper-evident” requires verified seals/checkpoints; database immutability alone is not enough.

W3C PROV export may map requests/policies/facts/decisions to entities, evaluation/replay/enforcement to activities, and callers/PDPs/PEPs/administrators to agents. The canonical Tigrbl schema remains optimized and bounded for authorization.

## 20. Decision Lineage Explorer UIX

### Overview

Show decision volume and latency, permit/deny/indeterminate distribution, provenance coverage, replayability, stale/missing facts, unmatched enforcement receipts, obligation gaps, policy drift, ingestion failures, retention risk, and regional placement.

Avoid treating a higher permit or deny rate as inherently better.

### Decision search

Filter by authorized tenant/environment/time, decision ID, correlation ID, subject/resource/action type, policy version, effect, reason, authority source, delegation, token/session, PEP, region, incident, replay status, and enforcement state.

Sensitive identifiers use exact authorized lookup and masking.

### Decision detail

Use a layered view:

1. outcome and safe explanation;
2. normalized request;
3. identity/assurance and fact freshness;
4. authority/delegation paths;
5. policy/rule/combining lineage;
6. obligations;
7. token/session/resource linkage;
8. enforcement and operation outcome;
9. integrity, replayability, and retention.

### Lineage graph and timeline

Visualize request, facts, authority, policies, decision, derived artifacts, and enforcement. Every graph must have an accessible table/timeline. Nodes visibly distinguish verified, asserted, derived, missing, stale, redacted, and unavailable.

### Replay workbench

Require mode selection, source decision, allowed substitutions, isolated engine/profile, expected cost, and purpose. Preview protected fields, run asynchronously, then show reproducibility, changes, missing evidence, and limitations.

### Comparison view

Provide semantic before/after differences for facts, policies, authority paths, steps, effect, obligations, and enforcement. Avoid raw JSON as the only comparison.

### Incident impact explorer

Start from compromised credential, principal, grant, relationship, policy, fact source, key, engine version, region, or PEP. Show affected decisions, tokens/sessions, resources, enforcement outcomes, uncertainty, and containment status.

### Evidence room

Provide read-only reconstruction, saved authorized queries, samples, manifests, seal verification, redaction summary, retention/hold state, and export approval. Never expose raw secrets or allow auditors to modify source records.

## 21. Security and Reliability

- Enforce tenant, realm, environment, regional, and field-level isolation.
- Separate provenance administration, policy administration, application support, audit, export, retention, and legal-hold authority.
- Protect audit/provenance tools from the operators whose actions they record.
- Authenticate PDP, collector, fact source, and PEP identities.
- Validate all schemas, hashes, sequences, and references at ingestion.
- Defend parsers, graph queries, replay engines, and exports against resource exhaustion.
- Run replay in isolated, network-denied sandboxes unless an explicit safe resolver profile permits otherwise.
- Prevent replay fixtures from invoking production side effects or secrets.
- Use partitioning, bounded retention, tiered storage, and indexed projections for scale.
- Preserve decision-plane availability with durable local buffering and explicit provenance-loss alerts.
- Detect gaps, duplicates, late events, conflicting collectors, and clock anomalies.
- Do not fail open on authorization because provenance storage is unavailable; instead preserve the decision plus durable delivery obligation according to risk profile.
- Meet WCAG 2.2 AA for dense tables, graphs, and comparisons.

## 22. Stakeholder Requirements

### Technical marketing

Demonstrate one permit, one deny, a delegated decision, policy-version comparison, historical replay, stale fact, and enforcement mismatch. Lead with explainability and evidence, not “AI-powered authorization.” Every demo must state which facts are simulated and whether enforcement is proven.

### Developer relations

Deliver AuthZEN/PDP integration, trace-envelope SDK, outbox/collector example, PEP receipt example, token/session linkage, reason-code guidance, redaction recipes, replay fixtures, W3C PROV export example, and negative cases for missing/stale/conflicting facts.

### Sales and account management

Provide discovery for authorization engines, PEPs, applications, decision volume/latency, retention, privacy, regions, policy languages, fact sources, incident needs, audit frameworks, exports, and current logging. Clearly distinguish trace coverage, replay coverage, and enforcement-receipt coverage.

### GTM strategist

Position this as authorization observability, evidence, and change safety across application, API, workload, agent, and regulated decisions. Package foundational decision search/explanation first, then replay/drift, impact analysis, and evidence exports. Avoid generic SIEM replacement claims.

### Copywriter

Standardize `request`, `fact`, `source`, `authority path`, `policy`, `rule`, `decision`, `obligation`, `enforcement`, `outcome`, `replay`, and `comparison`. Distinguish `recorded`, `verified`, `reproduced`, and `enforced`. Avoid “proof” where the chain is partial.

## 23. Delivery Instructions

### Frontend engineer

- Generate typed clients from trace, replay, and evidence schemas.
- Preserve decision ID, policy version, time, environment, and projection context in navigation.
- Implement server-side filtering/pagination and bounded lazy lineage expansion.
- Provide accessible tables/timelines for every graph.
- Never place sensitive identifiers or query contents in URLs or analytics.
- Render server-authorized projections; client hiding is not redaction.
- Implement asynchronous replay/impact/export progress, cancellation, and partial failure.
- Require purpose/reason and confirmation for protected views and exports.

### UIX designer

- Design for progressive explanation: outcome first, causal detail on demand.
- Establish a visual grammar for verified, asserted, derived, stale, missing, redacted, and unavailable evidence.
- Distinguish decision, delivery, enforcement, obligation fulfillment, and operation success.
- Make replay mode and substitutions impossible to overlook.
- Design no-data versus no-access versus expired/deleted evidence states.
- Test developer debugging, security investigation, audit sampling, and support workflows separately.

### Copywriter

- Write explanations that are accurate without exposing hidden policy/resource facts.
- Provide role-specific reason detail and remediation guidance.
- State replay and evidence limitations beside results.
- Use neutral language for anomalous or inconsistent decisions.

## 24. Delivery Phases

### Phase 1: Durable generalized decision trace

- canonical contracts and durable tables for decision, fact references, steps, authority paths, and links;
- generalize the deterministic builder beyond token exchange;
- authenticated ingestion/outbox and search/detail APIs;
- Decision Lineage Explorer search, detail, timeline, redaction, and audit;
- token/session linkage retained from existing runtime foundations.

### Phase 2: Enforcement and coverage

- PEP SDK and enforcement-receipt linkage;
- obligation status references;
- coverage/gap/reconciliation dashboards;
- AuthZEN Authorization API integration and additional product decision adapters;
- integrity seals/checkpoints and evidence bundles.

### Phase 3: Replay and drift

- frozen fact/policy/engine artifact store;
- exact/current/counterfactual replay modes;
- policy/engine/fact comparison and stability reports;
- privacy-safe bulk replay with budgets and approvals.

### Phase 4: Incident, sovereignty, and ecosystem

- graph impact analysis and containment links;
- regional residency/transfer provenance;
- external auditor/evidence profiles and W3C PROV export;
- cross-engine adapters and enterprise-scale certification.

## 25. Acceptance Criteria

### API and domain

- Every generalized decision has a unique ID and deterministic key derived from canonical request, policy, and derivation/fact state.
- Decision occurrence and decision equivalence are represented separately.
- Trace preserves exact policy/engine/schema versions and authorized fact-source references.
- Steps faithfully represent evaluated, skipped, failed, unavailable, and short-circuited behavior.
- Permit authority is traceable to one or more evidence-backed paths.
- Raw secrets, bearer artifacts, and prohibited fields never enter searchable trace storage.
- Token/session/resource/enforcement links use safe hashes or opaque references.
- Corrections supersede records without mutation.
- Gaps, late events, duplicates, and reference failures are detected and reconciled.
- Cross-tenant/realm/environment/region access is denied and tested.

### Replay

- Exact replay is labeled successful only when required historical request, facts, policy, schemas, and evaluator versions are available and outputs match.
- Current-state and counterfactual runs cannot be mistaken for historical reproduction.
- Replay is side-effect free and sandboxed.
- Decision changes explain the facts, authority, rules, combining, effect, and obligations that changed.
- Missing/deleted/redacted evidence produces an explicit incomplete result.

### UIX

- An authorized developer can explain a standard permit or deny without raw database/log access.
- Auditors see protected projections appropriate to their role, not unrestricted trace contents.
- Decision, enforcement, and operation outcome are visually distinct.
- Search cannot enumerate unauthorized subjects/resources.
- Graphs have equivalent accessible tables/timelines.
- Core workflows meet WCAG 2.2 AA.

### Evidence and business

- Fixtures cover RBAC, ABAC, relationship, delegation, risk, residency, token exchange, missing fact, stale cache, conflict, engine drift, PEP mismatch, and obligation mismatch.
- Marketing claims map to trace coverage, replay coverage, and enforcement coverage independently.
- An evidence bundle verifies its manifest/seal and declares redactions and missing links.

## 26. Success Measures

- percentage of authorization decisions with complete trace ingestion;
- percentage linked to policy, fact, authority, delegation, token/session, and PEP versions;
- percentage linked to enforcement receipts;
- median/p95 time to explain a permit or deny;
- exact historical replay success rate;
- decision drift rate by policy/engine/fact version;
- stale/missing/conflicting fact rate;
- unmatched/late/duplicate trace event rate;
- obligation-to-enforcement linkage and mismatch rate;
- incident impact-analysis time;
- support escalation and mean-time-to-resolution change;
- export/redaction defects and unauthorized-access events;
- trace storage cost per million decisions by retention tier.

Faster investigation is useful only if explanations remain correct, privacy-safe, and causally complete.

## 27. Source Evidence

### Repository

- `docs/compliance/authorization_decision_trace_phase5.md`
- `docs/authorization-models-focus.md`
- `docs/strategy/uix-pairing-briefs/12-authorization-decision-api-policy-studio-uix.md`
- `.ssot/specs/SPEC-1093-authorization-decision-trace-and-reproducibility-requirements.yaml`
- `.ssot/specs/SPEC-1212-policy-determinism-and-decision-stability-contract.yaml`
- `pkgs/20-providers/tigrbl-security-authorization-provenance-builder/`
- `pkgs/05-bases/tigrbl-security-provenance-bases/`
- `pkgs/20-providers/tigrbl-authz-policy/`
- `pkgs/20-providers/tigrbl-authz-policy-decision-engine/`
- `pkgs/30-storage-runtime/tigrbl-authz-policy-authority-derivation-graph/`
- `pkgs/02-contracts/tigrbl-security-trust-contracts/`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/replay/`
- `tests/unit/test_authorization_provenance.py`
- `tests/unit/test_policy_determinism_replay.py`
- `tests/unit/test_decision_stability_policy_versions.py`
- `tests/integration/test_persistence_lifecycle_durability.py`

### Standards and primary guidance

- [OpenID AuthZEN Authorization API 1.0](https://openid.net/specs/authorization-api-1_0.html): Final Specification for PDP/PEP evaluation and search interoperability; provenance extends rather than alters its decision contract.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) and [PROV-AQ](https://www.w3.org/TR/prov-aq/): interoperable provenance concepts and access/query guidance.
- [NIST SP 800-171 Rev. 3](https://csrc.nist.gov/pubs/sp/800/171/r3/final): least privilege, privileged-function logging, audit content, retention, and audit-information protection.
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final): access enforcement, audit generation, protection, review, and accountability control families.
- [RFC 8693](https://www.rfc-editor.org/rfc/rfc8693): OAuth token exchange actor/subject and delegation/impersonation contexts already represented in repository provenance.
- [RFC 9396](https://www.rfc-editor.org/rfc/rfc9396): typed rich authorization details that should remain traceable through authorization decisions.

## 28. Explicit Non-Claims

- A deterministic hash does not prove that input facts were truthful, complete, or authorized.
- A stored trace does not prove that the PEP enforced the decision.
- Returning an obligation does not prove the obligation was fulfilled.
- Historical replay is not exact when policy, facts, schemas, evaluator versions, or protected values are unavailable.
- Counterfactual replay does not prove what actually happened.
- Audit-log correlation alone is not complete causal provenance.
- A signed evidence bundle proves integrity/authenticity under its trust policy, not correctness of every included assertion.
- W3C PROV compatibility does not require exposing sensitive authorization facts as public linked data.
- Existing token-exchange provenance tests do not establish complete authorization-provenance coverage across every API, PDP, PEP, region, or product surface.
