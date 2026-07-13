# Security Signals API + Security Signals Center UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-security-signals` + `@tigrbl-auth/security-signals-center-uix`  
**Status:** New product surface; telemetry, anomaly, audit, session, revocation, policy, JOSE, and provenance foundations exist  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-security-signals`  
**Proposed protocol owner:** `pkgs/50-protocols/tigrbl-security-shared-signals`  
**Proposed UIX owner:** `pkgs/95-ui/security-signals-center-uix`

## 1. Product Decision

Create a security-signal exchange and continuous-access product surface that can receive, validate, normalize, correlate, transmit, investigate, and respond to security events across Tigrbl tenants, applications, identity providers, resource servers, workloads, and trusted partners.

The pairing must separate four concerns:

- **Signal protocol plane:** Security Event Token validation/issuance and OpenID Shared Signals Framework stream behavior.
- **Signal intelligence plane:** normalized facts, subject resolution, deduplication, correlation, severity, confidence, and policy-ready context.
- **Response orchestration plane:** safe, governed actions such as session revocation, token invalidation, step-up, credential suspension, connection quarantine, or manual review.
- **Operations experience:** stream setup, health, investigation, policy simulation, response approval, evidence, and recovery.

Signals are not bearer access tokens, authentication credentials, proof-of-possession proofs, or authorization decisions. Receiving a validly signed event proves who issued the event and preserves its integrity; it does not automatically prove the event is true, correctly mapped, authorized to trigger an action, or relevant to the tenant.

## 2. Current Repository Reality

The repository already includes:

- `AuthTelemetryEvent` and `AnomalySignal` contracts;
- an `AuthAnomalyDetector` that records redacted authentication telemetry and detects first-seen country, untrusted-device, and repeated-failure patterns;
- durable tenant-scoped audit events with actor, client, session, target, outcome, request, details, and occurrence time;
- credential, operator, policy, authorization, delegation, and runtime provenance/audit surfaces;
- session logout/revocation and token revocation runtime operations;
- adaptive access decisions and policy inputs;
- JOSE/JWT signing, verification, key, algorithm, issuer, and audience foundations;
- authorization provenance and decision observability;
- tenant, platform, and service UIX audit placeholders or basic views;
- a roadmap explicitly naming RISC, CAEP, SET, and SSE/SSF as later standards work.

The missing product surface includes canonical event contracts, RFC 8417 validation, SSF transmitter/receiver configuration, stream management, push/poll delivery, replay protection, subject resolution, event taxonomy, response policy, incident workflows, metrics, retention, and operator UIX.

### Required standards correction

The repository contains `tests/unit/test_rfc7952_security_event_token.py`, whose text labels Security Event Tokens as RFC 7952 and imports a removed `tigrbl_auth.rfc.rfc7952` implementation. This is incorrect: Security Event Tokens are defined by **RFC 8417**. RFC 7952 concerns YANG metadata. The stale test must not be treated as conformance evidence or revived under its old namespace. A future implementation needs correctly named RFC 8417 contracts, negative tests, and migration/removal of the misleading test.

OpenID Shared Signals Framework 1.0, CAEP 1.0, and RISC 1.0 reached final-specification status in 2025. The implementation should pin exact versions and profiles at delivery time and keep extension event types namespaced.

## 3. Users and Jobs

### Security operations analyst

1. See high-risk identity, session, credential, device, token, workload, and federation events in one tenant-safe queue.
2. correlate related signals into an investigation without losing source provenance.
3. understand subject, confidence, severity, affected assets, current access, and recommended action.
4. take or approve containment actions and verify their outcome.
5. export a redacted, integrity-linked incident package.

### Identity and access administrator

1. configure trusted transmitters, receivers, event streams, subject formats, and response policies.
2. test a stream end to end before activation.
3. monitor delivery, acknowledgement, retries, gaps, and expiring credentials/keys.
4. simulate how CAEP or RISC events affect sessions, credentials, and access.
5. suspend a stream or rollback policy safely.

### Application/resource-server developer

1. subscribe to relevant, privacy-minimized security events.
2. validate event origin, audience, type, time, and replay identifiers.
3. act on stable normalized event/reason codes.
4. implement retry/idempotency behavior and local continuous-access responses.
5. test with deterministic fixtures and avoid coupling to internal anomaly algorithms.

### Risk, compliance, and privacy teams

1. review event sources, data categories, retention, cross-border transmission, and response authority.
2. prove delivery and response without exposing unnecessary personal data.
3. verify that automation is explainable, reversible where possible, and reviewed for false positives.
4. distinguish raw telemetry, detected anomaly, received assertion, policy decision, and executed response.

## 4. Architectural Ownership

### Shared Signals protocol package owns

- RFC 8417 SET envelope, validation, signing, typing, and event extraction;
- SSF transmitter/receiver metadata and stream-management schemas;
- push and poll delivery protocol behavior selected by the supported profile;
- CAEP/RISC event schemas and subject identifier formats;
- acknowledgement, delivery error, verification, and interoperability fixtures.

### Security Signals API owns

- tenant-scoped stream and partner lifecycle;
- authentication, authorization, rate limits, replay/deduplication, persistence, and routing;
- normalization from protocol events and internal Tigrbl events into canonical signal records;
- subject resolution, correlation, investigation, response-policy evaluation, and orchestration;
- UI-facing management, query, evidence, and operational schemas.

### Existing packages retain ownership

- JOSE packages own cryptography and key operations;
- session, token, credential, federation, authenticator, and provisioning packages own their mutations;
- policy/authorization packages own decisions and response authorization;
- audit/provenance packages own durable evidence semantics;
- storage owns persistent records;
- UIX does not validate tokens or decide containment.

The signal service requests domain actions through typed owning-package commands. It must not update session, token, credential, or connection tables directly.

## 5. Standards and Event Profiles

### Security Event Token baseline

Implement RFC 8417 with:

- explicitly typed signed JWTs and protected algorithm policy;
- issuer, audience, issued-at, JWT ID, and `events` claim validation;
- event payloads keyed by collision-resistant event type URI;
- no inherited assumption that SETs behave like access tokens;
- replay detection based on issuer/audience/JTI and retention policy;
- optional encryption only through a separately tested recipient profile;
- key rotation, metadata discovery, and clock-skew policy.

### Shared Signals Framework

Support a bounded SSF profile for:

- transmitter configuration metadata;
- receiver registration and stream configuration;
- event type selection and subject-format negotiation;
- push delivery and/or poll delivery with explicit capability advertisement;
- stream status, verification, add/remove subject where the pinned version defines it;
- delivery retries, acknowledgements, backoff, dead-letter state, and operational metrics.

### CAEP event families

Initial continuous-access candidates include:

- session revoked;
- token claims changed;
- credential changed;
- assurance level changed;
- device compliance changed;
- account disabled/enabled;
- risk level changed.

The exact event URIs and payload shapes must come from the pinned final CAEP specification, not hand-authored approximations.

### RISC event families

Prioritize compromised account/credential, account disabled/enabled/purged, identifier changed/recycled, recovery activated, and sessions revoked where supported by the pinned RISC profile.

### Tigrbl extension events

Namespaced extensions may include:

- workload attestation or posture changed;
- service key or certificate compromised/rotated;
- federation trust path invalidated;
- delegation grant revoked or attenuated;
- policy version activated/rolled back;
- provisioning source suspended or mass deprovisioning detected;
- agent authorization budget exhausted.

Extensions must be versioned, documented, privacy reviewed, and never masquerade as standard CAEP/RISC events.

## 6. Protocol and Runtime API Requirements

Standards-defined routes should use the exact paths and methods in the pinned SSF profile. The following route families express the required product surface; final names must be reconciled to the specification.

### Public/protocol routes

| Method | Proposed route | Purpose |
|---|---|---|
| `GET` | `/.well-known/ssf-configuration` | Publish transmitter configuration metadata when enabled. |
| `POST` | `/ssf/streams` | Create/configure a receiver stream under authenticated authorization. |
| `GET` | `/ssf/streams/{stream_id}` | Retrieve stream configuration/status. |
| `PATCH/PUT` | `/ssf/streams/{stream_id}` | Update supported stream properties with version control. |
| `DELETE` | `/ssf/streams/{stream_id}` | Disable/remove stream according to retention policy. |
| `POST` | `/ssf/streams/{stream_id}:verify` | Send or process a verification event where specified. |
| `POST` | `/ssf/events` | Receive push-delivered SETs at a configured receiver endpoint. |
| `POST` | `/ssf/poll` | Poll for SETs if the selected delivery profile supports it. |

### Internal signal ingestion

- typed ingestion for Tigrbl audit, authentication, session, token, credential, policy, federation, provisioning, attestation, and workload events;
- immutable event identifier and source sequence/cursor when available;
- schema/version validation before enqueue;
- tenant binding derived from trusted execution context, not event payload alone;
- transactional outbox or equivalent so domain mutation and event publication do not silently diverge.

### Validation pipeline

1. enforce transport, content type, size, and rate limits;
2. resolve an enabled receiver/stream and expected transmitter;
3. parse JWT without trusting claims;
4. validate `typ`, algorithm, key, signature, issuer, audience, times, and required claims;
5. reject access-token semantics and unsupported nested/encrypted forms;
6. deduplicate issuer/audience/JTI before effect;
7. validate each event type and subject identifier against negotiated stream configuration;
8. tenant-bind and resolve the subject without cross-tenant fallback;
9. normalize privacy-minimized facts and persist provenance;
10. evaluate response policy and authorization;
11. execute or queue response through the owning domain;
12. record delivery, decision, action, outcome, and safe acknowledgement.

## 7. Management API Requirements

### Partners and streams

- CRUD/version lifecycle for transmitters, receivers, partner organizations, endpoints, keys, credentials, and stream configurations;
- validate, test, submit, approve, activate, pause, resume, rotate, and retire actions;
- event-type and subject-format allowlists;
- delivery mode, retry, rate, retention, geographic, and data-minimization policy;
- current/previous key view and safe metadata refresh;
- stream health, delivery lag, gaps, dedupe rate, last event, and last successful acknowledgement.

### Signal query and investigation

- tenant-scoped list/detail by time, source, event type, subject type, severity, confidence, state, response, and correlation;
- investigation CRUD with assignee, status, severity, rationale, labels, linked signals, subjects, assets, and actions;
- safe timeline merging source event, validation, normalization, policy decision, domain action, outcome, and recovery;
- related-event search based on explicit correlation rules, not opaque UI-only grouping;
- evidence export with digests, redaction, permissions, and audit.

### Response policy and simulation

- versioned rules mapping normalized signals/context to ignore, observe, notify, step-up, revoke session, revoke token, suspend credential, quarantine connection, deny access, or manual review;
- severity/confidence thresholds, subject scope, tenant/application scope, cooldown, rate cap, and expiration;
- dry-run against synthetic or privacy-safe historical fixtures;
- impact estimate, false-positive sample, before/after action delta, approval, staged rollout, rollback, and kill switch;
- no arbitrary user-authored code in the response path.

## 8. Canonical Data Model

### Signal partner and stream

- partner/stream ID, tenant, role (transmitter/receiver/both), issuer, audience, endpoint, delivery mode, status, and version;
- allowed event types and subject formats;
- signing/encryption key references, credential references, algorithms, metadata source, and rotation state;
- retry, rate, retention, residency, and redaction policies;
- health, verification status, last event, lag, and ownership contacts.

### Security signal

- immutable signal ID, tenant, source, source event ID/JTI, received/occurred times, and protocol/profile version;
- event type, subject identifiers, normalized subject link, affected resource/session/token/credential references;
- severity, confidence, reasons, recommended response, and lifecycle state;
- validation status, issuer/audience/key/algorithm metadata, payload digest, and provenance;
- privacy classification, retention expiry, correlation/investigation links, and duplicate lineage.

### Response decision and action

- policy/version, signal/context digest, decision, reason codes, approval requirement, and decision time;
- target domain/object, requested action, idempotency key, actor/automation identity, status, attempts, and outcome;
- rollback/recovery capability, expiry, superseding action, and correlated audit/provenance records.

### Investigation

- tenant, title, severity, state, owner, created/updated/resolved times;
- linked signals, subjects, assets, streams, sessions, credentials, and actions;
- timeline entries, analyst notes, decisions, evidence references, and closure rationale;
- access classification and retention/legal-hold status.

Raw SET compact tokens should be retained only where evidence policy requires them, encrypted and access-audited. Most UI and analytics use parsed, redacted, normalized records and cryptographic digests.

## 9. Correlation and Response Semantics

### Trust levels

The model must distinguish:

- **received:** bytes arrived from an endpoint;
- **cryptographically valid:** signature, issuer, audience, type, and time passed;
- **trusted source:** transmitter is active and authorized for the event/subject scope;
- **resolved:** subject/resource mapped unambiguously inside the tenant;
- **policy relevant:** event meets response policy criteria;
- **actioned:** an owning domain accepted/executed a response;
- **verified outcome:** the requested security state is observable.

No UI label may collapse these into a single "verified" state.

### Deduplication and ordering

- Deduplicate before domain effects using transmitter, audience, JTI, and event identity.
- Duplicate delivery returns safe success/acknowledgement where protocol requires and links to the original record.
- Do not assume global event ordering across streams.
- Use per-source sequence/cursor only when defined and authenticated.
- Late events remain visible but response policy must consider event time, receipt time, and current subject state.
- Replayed or stale events cannot reverse newer containment/recovery state.

### Automated response guardrails

- Low confidence signals default to observe/notify.
- High-impact actions require confidence, trusted source, unambiguous subject, current-state check, policy authorization, and rate/cooldown limits.
- Mass actions cross a configurable threshold into approval or kill-switch mode.
- Recovery events do not automatically restore access unless an explicit restoration policy exists.
- Response failures are retryable only with stable idempotency keys and domain-safe semantics.

## 10. Security Signals Center UIX

### Overview

- incoming/outgoing signal volume, critical/open signals, active investigations, response actions, stream health, delivery lag, and failures;
- trend by event family, source, tenant/app, response, and safe reason category;
- prioritized action queue for invalid signatures, replay spikes, stream gaps, expiring keys, unresolved subjects, failed containment, and policy anomalies;
- clear separation between security signals and ordinary audit logs.

### Stream setup wizard

1. choose transmit, receive, or bidirectional role;
2. identify partner, issuer, audience, endpoint, delivery method, and tenant scope;
3. exchange/verify keys and credentials safely;
4. negotiate event types and subject formats;
5. set data minimization, retention, retry, rate, and residency;
6. send/receive verification events;
7. preview normalized event and response-policy effect;
8. review findings, ownership, and incident contacts;
9. submit/approve/activate.

### Signal explorer

- accessible table with time, type, subject, source, confidence, severity, validation, response, and state;
- detail view showing trust-level progression and provenance;
- raw claim/header view restricted and redacted, never the default;
- related audit, session, credential, policy, federation, and provisioning context through safe links;
- duplicate/replay lineage and late-event indicators;
- filters are URL-safe only when they contain no personal identifiers.

### Investigation workspace

- chronological timeline of signals, decisions, actions, outcomes, analyst notes, and recovery;
- affected subject/assets and current security state;
- evidence panel with source, signature/key result, payload digest, policy version, and response receipt;
- assign, escalate, contain, add note, request approval, resolve, and reopen actions;
- collaborative notes must not become an ungoverned sensitive-data store.

### Response policy studio

- event/context condition builder with explicit priority and fallthrough;
- outcome options constrained to typed domain actions;
- dry-run and before/after impact against synthetic/redacted fixtures;
- false-positive and blast-radius views;
- staged rollout, observation-only mode, approval, version diff, rollback, and global kill switch;
- deep link to Policy Studio for general authorization logic rather than duplicating it.

### Stream operations

- delivery timeline, lag, acknowledgement, retry, dead letter, dedupe, and gap metrics;
- current/previous keys and rotation readiness;
- pause/resume, reverify, rotate, drain, replay-safe retry, and retire controls;
- partner-facing redacted diagnostic bundle.

## 11. Security, Privacy, and Reliability

- Use strict JWT type and algorithm allowlists, key-use validation, issuer/audience binding, clock policy, and JWT confusion defenses.
- Authenticate stream-management and delivery endpoints independently; do not use SET contents as transport authorization.
- Prevent SSRF in partner metadata/endpoints and require HTTPS plus optional mTLS/DPoP according to profile.
- Apply replay caches and durable dedupe long enough for the threat model and retry window.
- Limit token/event size, event count, nesting, subject count, request rate, and correlation fan-out.
- Reject unknown or unauthorized event types and subject formats; never partially act on an invalid multi-event SET.
- Minimize identifiers and attributes; use opaque/pairwise subject references where interoperable.
- Treat IP, location, device, health, credential, and behavior data as sensitive security telemetry.
- Prevent cross-tenant subject lookup, correlation, analytics, search, export, and notification leakage.
- Encrypt raw tokens and sensitive normalized fields at rest; audit privileged reads.
- Provide retention expiry, deletion, legal hold, residency, and cross-border controls.
- Use queue/outbox, backpressure, circuit breaking, dead letter, replay-safe recovery, and regional failover patterns.
- Measure signal-to-action latency and verify downstream state, not merely request acceptance.
- Keep an emergency kill switch that stops automated response without losing validated signal ingestion/evidence.

## 12. Stakeholder Requirements

### Technical marketing

- demonstrate a session-risk change flowing from signed event through validation, policy, revocation, and verified outcome;
- explain continuous access as reducing stale trust after login, not as omniscient real-time threat detection;
- distinguish standards-based CAEP/RISC events from Tigrbl extensions;
- prepare stories for B2B SaaS, workforce access, account compromise recovery, regulated ecosystems, workload posture, and cross-cloud response.

### Developer relations

- publish correct RFC 8417 SET examples and SSF/CAEP/RISC quickstarts;
- provide deterministic sign/validate, push/poll, duplicate, replay, expiry, wrong audience, unknown type, subject collision, and retry fixtures;
- document event URIs, subject formats, keys, stream metadata, response codes, limits, retry, dedupe, and privacy expectations;
- publish a migration note correcting/removing the legacy RFC 7952 naming.

### Sales and account management

- use a discovery worksheet for role, partner, event types, subjects, delivery mode, keys, network, retention, region, response SLA, automation, and incident contacts;
- receive a readiness report separating protocol implementation, tested interoperability, stream health, and response coverage;
- establish RACI for event truth, delivery, subject mapping, response policy, containment, recovery, and data handling;
- avoid promising automatic remediation without customer-approved policy and supported domain actions.

### GTM strategist

- package Shared Signals Connectivity, Continuous Access Response, Identity Threat Operations, and Advanced Governance as distinct tiers;
- pair with enterprise federation, authenticator lifecycle, resource validation, workload trust, and audit offerings;
- prioritize high-value session/account compromise and credential-change use cases before broad custom-event marketplaces;
- meter by active stream, protected identity/workload, event volume, retention, or automated response tier without discouraging security-event delivery.

### Copywriter

- distinguish telemetry, anomaly, signal, event assertion, incident, decision, requested action, and verified outcome;
- never use "breach confirmed" or "user compromised" solely because one signal arrived;
- show source, confidence, scope, age, response, and recovery state;
- write clear explanations for invalid, duplicate, replayed, stale, unresolved, ignored, contained, and recovered states;
- make automated-action confirmations disclose blast radius and reversibility.

## 13. Delivery Instructions

### Frontend engineer

- generate typed management clients; token parsing and trust validation remain server-side;
- render server-returned trust stages, reason codes, severity, confidence, policy decisions, and response outcomes without recomputing them;
- use event virtualization/pagination and cancellable background queries for high-volume streams;
- prevent raw token/identifier data from entering URLs, analytics, browser logs, clipboard helpers, or local storage;
- implement stale-version handling, idempotent action status, approval waits, partial failures, and kill-switch state;
- instrument time-to-detect, validate, resolve, decide, act, and verify using opaque IDs and safe categories.

### UIX designer

- separate severity from confidence and validation state;
- create a progressive path from portfolio posture to individual cryptographic/protocol evidence;
- design empty, verification, healthy, delayed, duplicate, replay spike, gap, invalid, unresolved, policy-blocked, action-failed, contained, and recovery states;
- provide non-graph timeline/table alternatives and keyboard-complete investigation workflows;
- make automated versus human-approved actions and reversible versus irreversible actions unmistakable;
- meet WCAG 2.2 AA with non-color status, accessible charts/tables, focus management, reduced motion, and announced live updates.

### Copywriter

- build event-type, trust-state, reason-code, remediation, action, confirmation, notification, and incident-status catalogs;
- write separate operator, developer, customer-admin, and partner diagnostic language;
- keep sensitive evidence masked and explain how privileged reveal is audited;
- use calibrated language such as "signal indicates" and "policy requested" until outcome is verified;
- provide safe recovery messaging for false positives, partner outage, key rollover, failed revocation, and stream suspension.

## 14. Delivery Phases

### Phase 1: Correct SET and internal signal core

- RFC 8417 contracts/provider and correct naming;
- canonical signal, source, subject, dedupe, validation, storage, query, and audit;
- internal domain-event ingestion and session/token response adapters;
- migration/removal of stale RFC 7952 test naming.

### Phase 2: SSF receiver and operations

- pinned SSF receiver profile, stream management, push or poll delivery, CAEP/RISC subset, verification, retry, dead letter, and health;
- stream setup, explorer, investigation, and manual response UIX.

### Phase 3: Transmitter and continuous response

- outbound events with privacy policy, partner key/credential lifecycle, delivery evidence, and interoperability fixtures;
- versioned response policy, simulation, staged automation, approval, verified outcomes, and kill switch.

### Phase 4: Ecosystem and vertical profiles

- workload, device, federation, provisioning, certificate, attestation, and agent signals;
- regulated network profiles, SIEM/SOAR integrations, longer evidence retention, and multi-region delivery.

## 15. Acceptance Criteria

### Protocol/API

- Correctly typed RFC 8417 SETs validate issuer, audience, key, signature, time, JTI, events, and profile schema.
- Wrong type/algorithm/key/issuer/audience, expired, replayed, unknown event, unauthorized subject, and cross-tenant inputs fail closed without domain effect.
- Duplicate delivery is idempotent and traceable.
- A supported CAEP/RISC event can move through receive, normalize, resolve, decide, act, and verified outcome with linked provenance.
- Stream configuration accurately advertises event types, subjects, delivery, and capabilities.
- Domain actions execute only through owning packages with policy authorization and idempotency.

### UIX

- An admin can configure and verify a stream without direct server configuration.
- An analyst can distinguish cryptographic validity, source trust, subject resolution, policy relevance, action, and outcome.
- Investigations preserve a tenant-safe timeline and evidence chain.
- Policy simulation reveals predicted actions and blast radius before activation.
- Operators can pause automation independently of ingestion and can recover failed actions safely.

### Evidence/business

- DevRel can run positive and negative fixtures with no RFC 7952 mislabeling.
- Technical marketing can demonstrate a deterministic continuous-access scenario using non-personal sample data.
- Sales can produce a redacted readiness report and RACI.
- Standards and partner interoperability claims link to pinned-version tests and certified release evidence.

## 16. Success Measures

- signal validation success/failure by safe reason category;
- duplicate/replay detection rate and false acceptance incidents;
- p50/p95 receive-to-validate, resolve, decide, action, and verified-outcome latency;
- unresolved-subject, dead-letter, stream-gap, and failed-response age;
- automated response precision, reversal rate, and analyst override rate;
- session/token/credential containment SLA attainment;
- stream verification and key-rotation success;
- investigation time to assignment, containment, recovery, and closure;
- sensitive-data access/export frequency and retention compliance.

Guardrails include false containment, cross-tenant correlation, replay side effects, action storms, unverified restoration, secret/token exposure, privacy overcollection, and overstated standards support.

## 17. Source Evidence

### Repository

- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/adaptive_access.py`
- `pkgs/20-providers/tigrbl-identity-admin-auth-anomaly-detector/`
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/audit_event/`
- credential, operator, policy, session, token, delegation, and authorization audit/provenance packages;
- `pkgs/30-storage-runtime/tigrbl-identity-storage-runtime/src/tigrbl_identity_storage_runtime/revocation.py`
- session/login/logout runtime services and resource-validation/JOSE packages;
- `tests/security/test_authorization_observability.py`
- `tests/unit/test_rfc7952_security_event_token.py` as stale/misnamed planning evidence only;
- `docs/security-certification-concern-plan.md` and opportunity-map research.

### Standards

- [RFC 8417: Security Event Token](https://www.rfc-editor.org/rfc/rfc8417)
- [OpenID Shared Signals Framework 1.0](https://openid.net/specs/openid-sharedsignals-framework-1_0.html)
- [OpenID Continuous Access Evaluation Profile 1.0](https://openid.net/specs/openid-caep-1_0.html)
- [OpenID RISC Profile 1.0](https://openid.net/specs/openid-risc-profile-1_0.html)
- [RFC 8935: Push-Based Security Event Token Delivery](https://www.rfc-editor.org/rfc/rfc8935)
- [RFC 8936: Poll-Based Security Event Token Delivery](https://www.rfc-editor.org/rfc/rfc8936)
- [RFC 8725: JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)

## 18. Explicit Non-Claims

This brief does not claim that the current repository:

- implements RFC 8417 Security Event Tokens;
- implements or conforms to SSF, CAEP, or RISC;
- has a deployable signal transmitter, receiver, or stream-management API;
- supports continuous-access response or verified automated containment;
- provides a production anomaly/risk engine based on the simple in-memory detector;
- interoperates with any named identity, security, SIEM, or SOAR vendor;
- can treat a signed event as independently proven compromise.

Those claims require correctly named and implemented standards profiles, adversarial tests, durable replay/correlation/response behavior, interoperability evidence, privacy review, operational proof, and release certification.
