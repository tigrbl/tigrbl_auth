# Policy Obligation API + Enforcement Receipt UIX Requirements Brief

**Pairing:** `tigrbl-auth-router-policy-obligations` + `@tigrbl-auth/enforcement-receipt-uix`<br>
**Additional opportunity:** Authorization/delegation/sovereignty extension 4<br>
**Primary buyers:** authorization platform teams, API and application security, data governance, regulated operations, workload/agent platforms, and audit/compliance<br>
**Status:** proposed product surface; obligation/advice contracts and handler ports exist, but production enforcement and receipts do not

## 1. Product Decision

Build a dedicated obligation control plane that turns policy-produced conditions into typed, enforceable work and records whether each Policy Enforcement Point actually fulfilled that work.

The product closes this gap:

`PDP permits with obligations -> PEP understands -> PEP enforces -> PEP proves outcome`

It must answer:

1. Which obligations were derived from which policy and decision?
2. Were they mandatory obligations or optional advice?
3. Which PEP/component was responsible for each one?
4. Did the PEP declare compatible semantics and version support?
5. Was the obligation fulfilled before, during, or after the protected operation?
6. What evidence demonstrates fulfillment, failure, partial fulfillment, or inability to verify?
7. Did the protected operation proceed despite an unmet mandatory obligation?
8. What compensation, containment, notification, or review followed a failure?

The API owns obligation type schemas, routing, execution plans, acknowledgments, receipts, reconciliation, and evidence. The UIX owns catalog governance, PEP compatibility, operational monitoring, mismatch investigation, and receipt reconstruction.

## 2. Current Repository Reality

The repository already includes:

- immutable `Obligation` and `Advice` contracts with IDs and attribute maps;
- `ObligationHandlerPort` and `AdviceHandlerPort`;
- abstract obligation/advice handler bases;
- concrete `NoopObligationHandler`, `CollectingObligationHandler`, and advice equivalents;
- Policy Studio requirements for obligations, simulation safety, provenance, and downstream enforcement;
- authorization briefs that reference obligations and decision receipts;
- typed policy request/decision/rule/combiner infrastructure;
- authorization provenance and proposed PEP enforcement-receipt linkage;
- audit, outbox, policy, security signal, residency, credential, token, and resource-server foundations.

These foundations are not production obligation handling:

- `PolicyDecision` currently exposes allowed/reason/matched/trace, not typed obligation instances;
- obligation attributes are untyped mappings;
- no canonical obligation type/version catalog exists;
- no PEP capability registry or compatibility negotiation exists;
- no durable obligation instance, assignment, attempt, receipt, or reconciliation tables exist;
- no distinction exists among pre-, in-, and post-enforcement obligations;
- no mandatory/optional, blocking/asynchronous, or failure semantics are modeled;
- the no-op handler can silently do nothing and must never represent production fulfillment;
- collecting handlers prove invocation only in memory, not enforcement;
- no dedicated API or UIX exists.

## 3. Relationship to Existing Pairings

### Authorization Decision API

The PDP determines whether access is allowed and which obligations/advice apply. This API validates, assigns, tracks, and verifies their enforcement.

### Authorization Provenance

Authorization Provenance records why an obligation was produced and references receipt status. It does not execute or judge fulfillment.

### Authority Attenuation

Attenuation determines whether authority was narrowed and which constraints the PEP must enforce. This API records enforcement of constraints expressed as obligations.

### Delegation Provenance

Delegation grants may require notifications, budgets, approvals, transaction binding, or post-action reporting. Their obligation instances and receipts live here.

### Audit and Security Signals

Audit records events; Security Signals distributes changes/incidents. Obligation receipts link to these systems without replacing them.

## 4. Mandatory Obligations Versus Advice

### Obligation

A mandatory action or condition associated with a decision. The decision may proceed only according to its declared enforcement phase and failure semantics.

Examples:

- require step-up before access;
- redact fields before response;
- restrict output rows or records;
- encrypt or route data through an approved region;
- enforce rate/value/budget limit;
- bind to a transaction digest;
- apply watermarking;
- record an auditable privileged action;
- notify a data/resource owner;
- terminate a session or delete transient data after use.

### Advice

Optional information the PEP may ignore without changing the PDP decision, such as a user-facing explanation or optimization hint. Ignored advice may be observed but is not an enforcement failure.

OASIS XACML explicitly distinguishes obligations from advice: obligations must be fulfilled by the PEP, while advice may be safely ignored. Tigrbl should retain this distinction without adopting XML as its internal format.

No mandatory condition may be labeled advice merely because a PEP lacks support.

## 5. Users and Jobs

### Authorization and security architect

- define obligation types and exact enforcement semantics;
- approve PEP implementations and compatibility;
- ensure policy cannot emit obligations nobody can enforce;
- govern failure, compensation, and evidence requirements.

### Application/API/PEP developer

- discover obligations supported by the PDP and required for a resource/action;
- implement typed handlers;
- acknowledge execution plans;
- emit verifiable, secret-safe receipts;
- test negative, timeout, retry, and partial-failure behavior.

### Policy engineer

- attach obligation templates to policies;
- simulate derivation without side effects;
- validate target PEP coverage before rollout;
- compare obligation changes across policy versions.

### Data, privacy, and sovereignty administrator

- enforce masking, purpose, retention, region, transfer, and recipient restrictions;
- verify that obligations reached the correct data plane;
- investigate unfulfilled controls.

### Auditor and incident responder

- reconstruct decision-to-enforcement chains;
- find permits with missing/failed receipts;
- contain resources, sessions, tokens, or delegates affected by enforcement failure;
- export evidence with clear limitations.

## 6. Architectural Ownership

### Policy Obligation API owns

- obligation/advice type and schema registry;
- obligation templates and versioning;
- decision-produced obligation normalization;
- PEP capability and handler registration;
- obligation assignment and execution planning;
- acknowledgments, attempts, receipts, compensation, and reconciliation;
- compatibility checks and rollout gates;
- evidence and UIX APIs.

### PDP owns

- deriving obligations/advice from the evaluated policy;
- binding them to decision, policy, subject/resource/action, and effective time;
- not asserting they were fulfilled.

### PEP owns

- protecting the resource;
- enforcing assigned obligations at the declared phase;
- failing closed where required;
- emitting truthful receipts and safe evidence.

### Domain services own

- actual masking, encryption, routing, notification, rate limiting, deletion, session control, or business transaction behavior;
- their obligation adapters report to this API.

## 7. Canonical Obligation Type

Each type requires:

- stable URI/name and semantic version;
- owner, domain, and risk classification;
- plain-language purpose;
- parameter JSON Schema or equivalent typed schema;
- parameter sensitivity/redaction rules;
- applicable subject/resource/action types;
- enforcement phase;
- mandatory/advice classification;
- blocking/asynchronous semantics;
- success, partial, failure, and unverifiable definitions;
- idempotency and retry rules;
- timeout and expiry;
- compensation/rollback behavior;
- compatible PEP handler types/versions;
- receipt schema and evidence level;
- privacy, residency, and retention;
- lifecycle: draft, approved, deprecated, retired.

Type versions are immutable after approval. Semantic changes require a new version.

## 8. Obligation Instance

Each decision-produced instance records:

- instance ID and decision/authorization trace IDs;
- tenant, realm, environment, and region;
- obligation type/version and template version;
- policy/rule/version that produced it;
- subject, actor, resource, action, and transaction references;
- typed, normalized parameters and parameter digest;
- mandatory/advice classification;
- phase and ordering/dependency constraints;
- assigned PEP/handler and compatibility profile;
- issued/effective/expiry times;
- idempotency key and attempt policy;
- current lifecycle and outcome;
- receipt/evidence/compensation references;
- retention and legal-hold classification.

Sensitive values use protected references or digests when the handler can resolve them securely.

## 9. Enforcement Phases

### Pre-enforcement

Must complete before the protected operation begins.

Examples:

- step-up authentication;
- user/owner approval;
- device/workload attestation refresh;
- regional route selection;
- key/transaction binding;
- atomic budget reservation;
- data minimization query plan.

### In-enforcement

Must remain active during the operation.

Examples:

- row/field filtering;
- masking/redaction;
- encryption;
- rate/concurrency control;
- session recording;
- egress restriction;
- continuous value/budget limit.

### Post-enforcement

Occurs after the protected operation, with explicit deadline and failure handling.

Examples:

- audit/event publication;
- owner notification;
- temporary-file deletion;
- usage/budget finalization;
- receipt export;
- downstream revocation or follow-up review.

A mandatory pre/in-enforcement obligation cannot be converted to post-enforcement merely for availability.

## 10. Execution Plan

The service converts obligation instances into an ordered dependency graph:

- responsible PEP/handler;
- required phase;
- dependencies and barriers;
- parallelizable tasks;
- timeout/retry/idempotency;
- blocking versus asynchronous;
- failure and compensation policy;
- receipt/evidence level;
- decision/resource-operation binding.

Requirements:

- reject cycles and missing handlers;
- ensure every mandatory obligation is assigned;
- verify handler/type/version compatibility;
- preserve policy-defined order where material;
- avoid duplicate side effects on retries;
- bind the plan to the exact decision and operation digest;
- freeze plan/version for historical evidence.

## 11. Obligation Lifecycle

Use:

`derived -> validated -> assigned -> acknowledged -> executing -> fulfilled`

Alternative states:

`unsupported`, `rejected`, `expired`, `timed_out`, `failed`, `partially_fulfilled`, `compensating`, `compensated`, `unverifiable`, `waived`, and `superseded`.

Rules:

- `unsupported` mandatory obligation denies/blocks operation;
- advice may be `ignored` with optional reason;
- waiver requires explicit policy/authority and creates a new decision context;
- retries preserve idempotency and attempt history;
- timeout does not imply failure or success until reconciled;
- corrections supersede receipts without mutation;
- post-enforcement failure remains open until compensated, accepted, or contained.

## 12. PEP Capability Registry

Each PEP declares:

- stable identity, owner, tenant/environment/region;
- protected resource/action types;
- obligation types and exact versions supported;
- handler implementation/build/deployment identity;
- enforcement phases;
- idempotency/retry/transaction support;
- receipt/evidence levels;
- health, last conformance, and deployment state;
- failure behavior and local buffering;
- attestation/signing capability;
- deprecation and rollout cohort.

Declarations are claims until verified by conformance evidence. Policy rollout must check actual target PEP coverage.

AuthZEN’s request context can describe PEP capabilities, and decision context can carry obligations/advice, but AuthZEN 1.0 leaves their concrete semantics to implementations. This pairing defines a governed Tigrbl profile while retaining AuthZEN compatibility.

## 13. Enforcement Receipt

Each receipt records:

- receipt and obligation-instance IDs;
- decision, plan, policy, and authorization trace IDs;
- PEP and handler identity/version;
- resource/action/transaction digest;
- attempt number and idempotency key;
- started/completed/observed times;
- outcome: fulfilled, partial, failed, compensated, waived, or unverifiable;
- normalized safe result details;
- parameter and output/evidence digests;
- affected record/field/count/value summaries where safe;
- region/route/storage/key references where relevant;
- usage/budget reservation and consumption;
- error/retry/compensation references;
- integrity signature/seal and previous receipt link;
- disclosure, retention, and legal-hold metadata.

Receipts are non-bearer evidence and never confer access.

## 14. Evidence Levels

Define at least:

- **L0 declared:** handler reports success with no independent evidence;
- **L1 correlated:** success linked to a resource operation/audit event;
- **L2 measured:** result includes verifiable output/state digest or readback;
- **L3 independently verified:** separate verifier confirms required state/action;
- **L4 hardware/external attested:** trusted execution, HSM, provider, or authoritative system supplies protected evidence.

The required level is obligation/profile-specific. Higher levels are not universally necessary and can increase privacy/cost.

UIX must display evidence level rather than treating every success receipt equally.

## 15. Core Obligation Families

### Authentication and approval

- step-up authentication method/assurance/recency;
- second-person/quorum approval;
- user/resource-owner interaction;
- delegate acceptance;
- transaction confirmation.

### Data minimization and transformation

- allowed fields/rows/records;
- masking, redaction, tokenization, aggregation;
- selective disclosure;
- output-size or precision limits;
- watermarking or labeling.

### Data handling and sovereignty

- processing/storage/backup region;
- approved route/provider;
- encryption/key jurisdiction;
- transfer authorization reference;
- retention/deletion;
- recipient/onward-disclosure restrictions.

### Usage and transaction limits

- rate, count, concurrency, duration;
- amount/value/currency;
- compute/token/storage/network budget;
- one-use/replay protection;
- transaction digest binding.

### Monitoring and accountability

- audit record;
- session/action recording;
- owner/security notification;
- enhanced telemetry;
- post-use access review;
- evidence bundle.

### Lifecycle and containment

- expire/revoke token, grant, session, or lease;
- quarantine workload/device/artifact;
- delete transient data;
- invalidate caches;
- re-evaluate after security signal.

## 16. Step-Up and Challenge Semantics

Step-up is not “permit now and authenticate later.”

The decision/obligation profile must support:

- challenge/continuation state;
- required authenticator/assurance and recency;
- subject, client, resource/action/transaction binding;
- expiry, nonce, replay, and attempt limits;
- completion callback or polling;
- re-evaluation after successful step-up;
- final decision and new trace.

The pre-step-up permit is not an access permit. The PEP blocks resource access until the final decision.

## 17. Data Filtering, Masking, and Transformation

Requirements:

- use typed field/record schemas and immutable resource/query references;
- preserve relationships between actions, fields, and data classes;
- enforce at the authoritative data plane when possible;
- produce before/after schema or safe count/digest evidence;
- prevent downstream caches/logs/telemetry from retaining unmasked data;
- distinguish omission, masking, tokenization, anonymization, and encryption;
- treat re-identification and derived data separately;
- fail closed if the PEP cannot reliably locate protected fields.

Displaying masked data in the browser after full data was delivered is not adequate enforcement.

## 18. Regional Routing and Sovereignty

Regional obligations bind:

- source/destination/processing/storage/backup regions;
- allowed service/provider/control-plane paths;
- encryption/signing key location;
- administrator/support access region;
- telemetry/audit destination;
- transfer/legal-basis reference;
- emergency/failover policy.

Receipts must distinguish routing selection, actual processing observation, storage confirmation, and downstream replication. A configured region is not proof that every dependency remained within the boundary.

## 19. Budgets and Usage

Budget obligations require:

- typed unit and parent budget;
- atomic reservation before action;
- idempotent consumption/finalization;
- release/refund rules;
- sibling/concurrent allocation safety;
- maximum and remaining values;
- transaction/action binding;
- authoritative ledger receipt;
- handling for partial work and retries.

In-memory counters are insufficient for distributed enforcement.

## 20. Notifications and Audit

- Notifications have recipient, purpose, channel, content template, deadline, retry, privacy, and escalation policy.
- Audit obligations specify event type, required fields, sink, integrity, retention, and correlation.
- Handler must not place secrets or full sensitive payloads into messages/logs.
- Delivery attempt is not recipient acknowledgment unless required and supported.
- Audit event accepted by a local queue is not durable external retention unless the profile says so.
- Notification/audit failure may require operation rollback, containment, or post-action exception depending on policy.

## 21. Compensation and Failure Semantics

For each mandatory obligation define:

- whether failure blocks before operation;
- whether operation can be rolled back;
- compensation action;
- containment if rollback is impossible;
- retry deadline/backoff;
- alert/escalation;
- exception authority;
- final evidence state.

Examples:

- failed mask/filter: block response;
- failed budget reservation: block action;
- failed audit enqueue for privileged action: block under high-assurance profile;
- failed post-use notification: retry/escalate without pretending rollback;
- failed transient-data deletion: quarantine storage and open incident;
- failed regional route: deny rather than use an unauthorized region.

## 22. Idempotency and Transactions

- Every obligation instance and attempt has stable idempotency identity.
- PEP retries cannot duplicate payments, messages, deletions, or budget consumption.
- Use transactional enforcement when resource operation and obligation share a data plane.
- Otherwise use saga/outbox patterns with explicit partial states and compensation.
- Receipt order and duplicate detection are durable.
- At-least-once delivery must not be presented as exactly-once execution.
- Long-running operations use leases/heartbeats and reconciliation.

## 23. Simulation and Testing

Policy simulation must derive and validate obligations without executing side effects.

Provide:

- schema and compatibility validation;
- handler dry-run planning;
- deterministic fixtures;
- fake/sandbox targets;
- failure, timeout, retry, duplicate, crash, and compensation tests;
- PEP conformance suites;
- policy-version obligation diff;
- load and degraded-dependency tests;
- evidence-level verification tests.

No simulation may send real notifications, mutate budgets, delete data, revoke credentials, or write production audit sinks.

## 24. API Requirements

Provide versioned endpoints for:

- `/obligation-types`, schemas, versions, and lifecycle;
- `/advice-types`;
- `/templates` and policy bindings;
- `/peps`, handlers, capabilities, health, and conformance;
- `/instances`, assignment, lifecycle, and status;
- `/plans`, validation, acknowledgment, and execution state;
- `/attempts` and `/receipts`;
- `/reconciliation`, retry, compensation, and exception;
- `/coverage` and rollout gates;
- `/simulations`, fixtures, and compatibility reports;
- `/incidents/impact` and containment;
- `/evidence-bundles`, seals, retention, and legal hold;
- authenticated internal `/ingest` routes for PDPs and PEPs.

API behavior:

- typed schemas and exact versions;
- tenant/resource/PEP/field authorization;
- idempotency and optimistic concurrency;
- immutable decision/receipt records with supersession;
- asynchronous execution for post-enforcement and long-running obligations;
- bounded pagination/search and no secret-bearing parameters;
- no general arbitrary-code handler upload through the API.

## 25. Enforcement Receipt UIX

### Overview

Show obligations derived, acknowledged, fulfilled, failed, partial, timed out, compensated, waived, unsupported, and unverifiable; PEP coverage; permit-without-receipt gaps; evidence levels; and incident/regional posture.

### Obligation catalog

Display purpose, parameters, phase, mandatory/advice, failure semantics, compatible PEPs, evidence level, versions, policy usage, and lifecycle. Changes use semantic diff and impact analysis.

### PEP and handler inventory

Show resource/action scope, supported obligation versions, implementation/deployment identity, conformance, health, receipt level, region, last use, and coverage gaps.

### Decision enforcement timeline

Render decision, obligation derivation, plan, acknowledgment, attempts, protected operation, receipts, compensation, and final reconciliation. Keep decision permit distinct from enforcement success.

### Receipt detail

Show obligation/decision/policy, PEP/handler, phase, parameters under authorized redaction, attempt/idempotency, outcome, evidence level, operation binding, timing, compensation, and integrity verification.

### Coverage and rollout studio

Before policy deployment, identify every target PEP lacking required obligation support. Simulate cohorts, block unsafe rollout, and track upgrades/deprecations.

### Failure and reconciliation queue

Prioritize mandatory pre/in failures, permits without receipts, timed-out work, duplicate/conflicting receipts, failed compensation, regional violations, and unverifiable claims. Support assignment, retry, containment, exception, and evidence.

### Evidence room

Provide read-only decision-to-receipt reconstruction, manifests, integrity verification, redaction summary, retention/hold, and controlled export.

## 26. Search, Privacy, and Data Safety

- Search is tenant/resource/PEP/purpose scoped.
- Mask subjects, resources, transactions, recipients, fields, regions, and evidence according to role.
- Store parameter/output digests or protected references when raw values are unnecessary.
- Prohibit secrets, bearer tokens, raw credentials, unmasked protected data, and private keys in receipts.
- Do not create a shadow data warehouse through transformation/audit receipts.
- Apply regional residency, transfer, retention, deletion, and legal hold to obligation evidence.
- Audit protected receipt views and exports.
- Bound time, count, and graph queries to prevent enumeration.

## 27. Security and Reliability

- Separate obligation type authoring, policy authoring, PEP administration, handler deployment, exception, audit, and evidence authority.
- Authenticate PDP, router, PEP, handler, and receipt signer identities.
- Validate schemas, versions, decision/operation binding, idempotency, sequence, and integrity at ingestion.
- Treat handler plugins as privileged code with signed artifacts, isolation, least network/filesystem access, and reviewed deployment.
- Prevent injection through templates, field selectors, notifications, queries, commands, URLs, and adapter parameters.
- Protect against SSRF in routing/notification/integration obligations.
- Use durable outbox, retries, dead-letter queues, reconciliation, and bounded backpressure.
- Fail closed for unsupported or failed mandatory pre/in obligations.
- Define safe degraded modes for post-enforcement obligations; never silently drop them.
- Detect conflicting receipts, forged PEP identities, replay, clock anomalies, and missing sequences.
- Meet WCAG 2.2 AA for dense operational tables, timelines, and evidence workflows.

## 28. Stakeholder Requirements

### Technical marketing

Demonstrate step-up, server-side masking, budget reservation, regional routing, privileged audit, a failed mandatory obligation, compensation, and a verified receipt. Explicitly show why permit is not synonymous with enforced.

### Developer relations

Deliver AuthZEN decision-context profile, typed handler SDK, PEP capability/receipt SDK, masking/rate/budget/notification examples, outbox/saga patterns, conformance kit, failure injection, simulation safety, and evidence verification.

### Sales and account management

Use discovery for PDPs/PEPs, application/data planes, obligation types, blocking requirements, receipts, audit sinks, regions, masking, budgets, step-up, notification, transactionality, latency, scale, and evidence retention. Separate native handlers from adapters/customer implementations.

### GTM strategist

Position as authorization enforcement assurance: policy conditions become measurable controls. Enter with API masking/step-up/rate/audit, then expand into regional/data governance, agent budgets, and regulated evidence. Do not claim universal policy enforcement when PEP coverage is incomplete.

### Copywriter

Standardize `obligation`, `advice`, `phase`, `PEP`, `handler`, `execution plan`, `attempt`, `receipt`, `fulfilled`, `partial`, `failed`, `compensated`, `waived`, and `unverifiable`. Avoid “compliant” or “enforced” based only on a PDP response.

## 29. Delivery Instructions

### Frontend engineer

- Generate typed clients and forms from server schemas; do not execute obligations in the browser unless the approved profile explicitly makes the browser the PEP.
- Preserve decision, obligation, plan, PEP, attempt, operation, and receipt correlation.
- Render server-authorized/redacted projections.
- Implement async progress, retry, compensation, and partial-failure states.
- Use server-side pagination/filtering for receipt volumes.
- Require semantic diff/impact/coverage confirmation for type and policy rollout.
- Keep protected parameters/evidence out of URLs, analytics, and session replay.
- Provide accessible table alternatives for timelines/graphs.

### UIX designer

- Make mandatory versus advice and pre/in/post phases unmistakable.
- Separate decision permit, PEP acknowledgment, operation, fulfillment, and verification.
- Establish states for unsupported, queued, executing, fulfilled, partial, failed, timed out, compensated, waived, and unverifiable.
- Show evidence level and external dependencies.
- Design no-data, no-access, stale, late, duplicate, conflict, and partial-coverage states.
- Optimize rollout safety, incident operations, and audit reconstruction separately.

### Copywriter

- Explain obligation consequences and failure behavior before rollout.
- State evidence limitations beside receipt outcomes.
- Use neutral language for failure and waiver.
- Distinguish “reported by PEP” from “independently verified.”

## 30. Delivery Phases

### Phase 1: Typed contracts and receipt spine

- extend policy decisions with typed obligation/advice context;
- canonical type/template/instance/plan/PEP/attempt/receipt contracts;
- durable tables, ingestion, search, detail, and timeline;
- replace production no-op behavior with explicit unsupported/fail-closed semantics;
- AuthZEN-compatible decision context profile.

### Phase 2: Core handlers and coverage

- step-up, audit, notification, rate/count, server-side field masking, and session/token lifecycle handlers;
- PEP capability registry and conformance kit;
- rollout coverage gates and failure/reconciliation UIX;
- authorization provenance integration.

### Phase 3: Data, sovereignty, and budgets

- row/record filtering, transformation evidence, region/routing, key location, retention/deletion;
- atomic budget/value/usage ledgers;
- compensation/containment and Security Signals;
- stronger evidence/readback levels.

### Phase 4: Ecosystem and high assurance

- agent, device, workload, credential broker, deployment, and external PEP adapters;
- signed/attested receipts, regional scale, evidence export, and regulated profiles;
- external standards/profile registration only after interoperability evidence.

## 31. Acceptance Criteria

### Domain/API

- Policy decisions carry typed, versioned obligations/advice bound to decision/policy/resource/action.
- Mandatory and optional semantics are server-enforced and cannot be relabeled by the client.
- Every mandatory obligation has a compatible assigned PEP before operation.
- Pre/in obligations block on unsupported, timeout, or failure according to policy.
- Plans are acyclic, ordered, immutable, and operation-bound.
- Attempts are idempotent and preserve retry history.
- Receipts distinguish declared, correlated, measured, independently verified, and attested evidence.
- Missing receipt never becomes fulfilled by timeout/default.
- Compensation/waiver requires explicit state, authority, and evidence.
- Cross-tenant/resource/PEP/region access is denied and tested.

### Handler/PEP

- No-op handler cannot satisfy production mandatory obligations.
- Handler conformance covers success, unsupported, timeout, duplicate, retry, crash, partial, compensation, and forged receipt.
- Browser-only masking cannot satisfy server/data-plane masking.
- Budget/value operations are atomic under concurrency.
- Regional obligations report configured route and observed processing/storage separately.
- Sensitive values never enter receipt/log/export fields.

### UIX

- Operators can trace decision to every obligation and receipt.
- Policy rollout blocks when target PEP coverage is incomplete.
- Permit, operation success, obligation fulfillment, and independent verification are distinct.
- Failures expose owner, deadline, retries, compensation, and residual risk.
- Core workflows meet WCAG 2.2 AA.

### Evidence/business

- Fixtures cover step-up, masking, filter, rate, budget, regional routing, audit, notification, deletion, revocation, partial operation, failed compensation, waiver, and evidence-level differences.
- Marketing claims map independently to obligation derivation, PEP coverage, receipt coverage, and verification level.

## 32. Success Measures

- mandatory obligation instances by lifecycle/outcome;
- percentage assigned to compatible/conformant PEPs;
- decisions permitted with complete versus missing receipt chains;
- pre/in obligation failure-block rate;
- post-obligation completion by deadline;
- partial/failed/unverifiable/waived receipt rate;
- compensation success and residual-risk age;
- evidence-level distribution;
- PEP version/coverage gaps and rollout blocks;
- duplicate side effects prevented by idempotency;
- budget overrun and regional-route violations prevented/detected;
- time to investigate enforcement mismatch;
- sensitive-data leakage incidents in receipts/logs, target zero.

## 33. Source Evidence

### Repository

- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/policy/obligations.py`
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/policy/decisions.py`
- `pkgs/05-bases/tigrbl-authz-policy-bases/`
- `pkgs/10-concrete/tigrbl-authz-policy-obligations-concrete/`
- `docs/strategy/uix-pairing-briefs/12-authorization-decision-api-policy-studio-uix.md`
- `docs/strategy/uix-pairing-briefs/30-authorization-provenance-api-decision-lineage-explorer-uix.md`
- `docs/strategy/uix-pairing-briefs/31-delegation-provenance-api-authority-chain-explorer-uix.md`
- `docs/strategy/uix-pairing-briefs/32-authority-attenuation-api-capability-composer-uix.md`
- policy, resource-server, token, audit, security-signal, residency, credential, and storage packages/tests.

### Standards and primary guidance

- [OpenID AuthZEN Authorization API 1.0](https://openid.net/specs/authorization-api-1_0.html): final PDP/PEP API whose decision context may carry obligations, advice, step-up instructions, and PEP-relevant information while leaving concrete semantics to profiles/implementations.
- [OASIS XACML 3.0](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-cos01-en.html): established distinction between mandatory obligations and safely ignorable advice, with PDP-to-PEP response behavior.
- [NIST Policy Enforcement Point definition](https://csrc.nist.gov/glossary/term/policy_enforcement_point): the PEP requests and enforces authorization decisions.
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final): access enforcement, information flow, audit generation/protection, least privilege, and accountability controls.
- [RFC 9396, OAuth Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396): transaction-specific authorization detail that may produce exact enforcement conditions.
- [RFC 9449, DPoP](https://www.rfc-editor.org/rfc/rfc9449) and [RFC 8705, OAuth mTLS](https://www.rfc-editor.org/rfc/rfc8705): proof-binding requirements that PEPs/resource servers must enforce.

## 34. Explicit Non-Claims

- Returning an obligation does not prove it was assigned, understood, or fulfilled.
- Calling an in-memory/no-op handler does not constitute enforcement.
- A PEP self-reported success receipt is not independent verification.
- Operation success does not prove masking, routing, audit, retention, budget, or notification obligations succeeded.
- Browser-side hiding does not enforce server/data-plane minimization.
- Configuring a region does not prove every processing, storage, backup, key, telemetry, or support path stayed there.
- At-least-once delivery does not establish exactly-once execution.
- Compensation does not always restore the pre-operation state.
- An evidence receipt does not itself establish legal/regulatory compliance.
- Existing obligation/advice contracts and ports are extension foundations, not production obligation enforcement coverage.
