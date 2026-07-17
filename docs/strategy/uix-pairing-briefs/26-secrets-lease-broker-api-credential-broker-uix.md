# Secrets Lease/Broker API + Credential Broker UIX Requirements Brief

**Pairing:** `tigrbl-auth-router-credential-broker` + `@tigrbl-auth/credential-broker-uix`<br>
**Opportunity-map item:** 16<br>
**Primary buyers:** platform engineering, DevOps, security engineering, data infrastructure, and CI/CD teams<br>
**Best-fit verticals:** cloud platforms, data/AI infrastructure, software delivery, regulated operations, and multi-cloud enterprise<br>
**Status:** proposed product surface; identity, credential, workload, attestation, delegation, token, key, and audit foundations exist

## 1. Product Decision

Build an identity-aware credential broker that exchanges an authenticated and authorized principal’s current trust context for a narrowly scoped, short-lived credential or mediated action.

The product must reduce dependence on long-lived secrets. It brokers database accounts, cloud sessions, SSH certificates, API credentials, third-party OAuth tokens, client certificates, and target-specific capability tokens through policy-bound leases.

The broker’s core promise is:

> Verify the caller, authorize the purpose and target, mint the least credential needed, deliver it through the safest available channel, expire or revoke it, and retain evidence without retaining the secret.

The browser UIX governs broker policy, roles, requests, approvals, leases, connectors, rotation, revocation, and evidence. It is not a general-purpose secret viewer.

## 2. Current Repository Reality

The repository provides substantial adjacent foundations:

- service, workload, machine, client, user, device, and agent principal concepts;
- service keys, API keys, client secrets, credential records, validity windows, digests, and one-time-display guidance;
- OAuth client credentials, JWT assertion, token exchange, resource indicators, DPoP, and mTLS capabilities;
- delegation grants, attenuation, policy decisions, relationship graphs, and audit provenance;
- workload identity, SPIFFE/SPIRE, device, and attestation product briefs and primitives;
- signing-key rotation policies/events and certificate lifecycle direction;
- service-admin and developer surfaces for existing first-party credential lifecycle.

These are not yet a general credential broker. The repository lacks:

- canonical broker target, role, connector, lease, delivery, renewal, and revocation contracts;
- dynamic database/cloud/SSH/third-party credential adapters;
- an identity-to-target-role mapping and policy engine integration;
- secure lease delivery patterns and client/sidecar SDKs;
- revocation confirmation and downstream reconciliation;
- dedicated API and UIX packages;
- production evidence for high-scale lease issuance, renewal, outage, and compromise handling.

The brief therefore extends existing identity and authorization assets; it must not rebrand static service/API key CRUD as dynamic secrets.

## 3. Users and Jobs

### Platform and security administrator

- Connect credential issuers and target systems without spreading root credentials.
- Define who or what may request which target role, for what purpose, and for how long.
- Require attestation, approvals, network/context restrictions, and proof binding.
- Revoke leases and diagnose incomplete revocation.

### Developer, operator, or data engineer

- Request temporary access to a database, host, cloud account, cluster, or vendor API.
- Understand the scope, expiry, approval, and safe usage method.
- Renew when policy permits and stop access cleanly.

### Workload, CI job, or agent

- Authenticate using platform/workload identity instead of a bootstrap secret.
- Receive or use a credential without writing it to source code, configuration, logs, or durable disk.
- Refresh automatically before expiry and fail safely when trust changes.

### Approver and resource owner

- Evaluate a request’s caller, purpose, target, scope, duration, risk, and evidence.
- Approve a bounded lease rather than grant indefinite standing access.

### Incident responder and auditor

- Identify active and recently used leases by principal, target, connector, and incident scope.
- Revoke safely, verify target-side invalidation, and export evidence with no secret material.

## 4. Architectural Ownership

### Credential Broker API owns

- broker targets, roles, templates, and connector configuration references;
- eligibility and issuance policy orchestration;
- lease request, approval, issuance, renewal, expiry, revocation, and reconciliation state;
- delivery-channel selection and one-time response wrapping;
- links among identity evidence, policy decisions, issued credential metadata, and audit events;
- target adapter invocation, health, and capability declarations;
- operator evidence and metrics with secret-safe redaction.

### Existing packages retain ownership

- principals: canonical caller, sponsor, owner, and service/workload facts;
- authenticators and attestation: how caller/device/workload trust is proven;
- authorization policy: allow/deny, constraints, delegation, and decision traces;
- OAuth/token service: standards-based token issuance and exchange;
- certificate service: X.509 lifecycle and CA integration;
- workload trust: SPIFFE identities and SVID delivery;
- credentials: first-party credential taxonomy, verification, and lifecycle primitives;
- storage: durable metadata, transactions, migrations, and outbox;
- audit/security signals: append-only events and risk/status change inputs.

### External issuer responsibility

Database engines, cloud STS services, SSH CAs, PKI systems, OAuth authorization servers, secrets engines, and vendor APIs remain authoritative for their credential formats and invalidation behavior. The broker integrates them through typed adapters rather than cloning them.

## 5. Core Domain Model

### Broker target

- tenant, environment, system, endpoint reference, owner, and classification;
- connector and issuer reference;
- supported credential kinds and delivery modes;
- network zone and residency constraints;
- health, last successful issuance, and last reconciliation;
- emergency-disable status.

### Broker role

A broker role is the named, governed offer exchanged for a credential. It defines:

- target and credential kind;
- target-native role, account template, principals, scopes, or claims;
- subject eligibility and required relationships;
- purpose/resource/action constraints;
- minimum authentication and attestation posture;
- default and maximum TTL;
- renewable flag and maximum total lifetime;
- approval, break-glass, and step-up requirements;
- allowed delivery modes;
- concurrency, rate, and lease-count limits;
- revocation and cleanup behavior;
- owner, reviewers, version, lifecycle, and risk.

### Lease request

- caller, requested subject, actor/delegator, sponsor, and tenant;
- role, target, purpose, ticket/task, resource, and requested duration;
- authenticated session or workload identity references;
- attestation and device/workload posture references;
- policy input snapshot and idempotency key;
- approval and exception state.

### Lease

- opaque lease ID, role/target/connector versions, principal, and purpose;
- issued, not-before, expires, renewable-until, revoked, and reconciled timestamps;
- credential kind, external credential identifier, and non-secret fingerprint;
- delivery mode and delivery acknowledgment;
- renewal count and parent/replacement links;
- policy decision, approval, attestation, and audit references;
- current lifecycle and downstream state;
- no raw credential value.

## 6. Lease Lifecycle

Use an explicit lifecycle:

`requested -> evaluating -> awaiting_approval -> issuing -> active -> renewing -> expiring -> expired`

Exceptional paths include:

`denied`, `issuance_failed`, `delivery_failed`, `revocation_requested`, `revoking`, `revoked`, `revocation_unverified`, `orphaned`, and `compromised`.

Requirements:

- issue only after a fresh policy decision;
- make issuance idempotent and resistant to duplicate target credentials;
- bind the lease to exact subject, role, target, purpose, and policy version;
- renew by re-evaluating trust and policy, not by blindly extending timestamps;
- enforce both per-renewal TTL and maximum total lifetime;
- revoke on explicit request, principal suspension, trust degradation, role change, target disablement, or incident signal;
- reconcile expired/revoked leases against the target;
- quarantine orphaned target credentials and escalate cleanup;
- preserve metadata/evidence after secret material becomes unusable.

## 7. Credential Profiles

### Database credentials

- dynamically create per-lease users where supported;
- use role templates with least database privileges;
- generate high-entropy passwords or certificate authentication;
- set target-side validity/expiration when supported;
- drop/disable the account on revoke and verify absence;
- track active sessions separately because account revoke may not terminate existing connections;
- support connection-proxy mediation when direct credentials are undesirable.

### Cloud credentials

- prefer native federation and security-token services over stored access keys;
- constrain role/session, audience, region, tags, resource, and duration;
- record native session identifiers and policy hashes;
- expose provider-specific revocation limitations honestly;
- distinguish “credential expired” from “existing operation/session terminated.”

### SSH credentials

- prefer short-lived OpenSSH user/host certificates over copying authorized keys;
- bind certificate principals, source restrictions, critical options, extensions, and validity;
- accept a client-generated public key so the private key never reaches the broker;
- protect CA keys behind an HSM/KMS or external signer;
- distribute and reconcile revocation data where early invalidation is required.

### API and third-party credentials

- prefer OAuth federation, token exchange, workload identity federation, or vendor-native ephemeral tokens;
- use request-signing or proxy mediation when the target supports only static upstream secrets;
- never return the upstream root/vendor secret to the requester;
- scope and audience-constrain downstream tokens where supported;
- represent non-revocable tokens as short-lived with explicit limitation metadata.

### Client certificates

- receive a CSR or public key, not a requester private key by default;
- enforce EKU, SAN, subject, issuer, profile, and maximum validity;
- integrate the Certificate Lifecycle API for signing, status, and revocation;
- bind issuance to caller/workload attestation.

## 8. Identity, Attestation, and Authorization

Supported caller identities include human sessions, OAuth clients, service/workload principals, SPIFFE identities, devices, CI jobs, and sponsored agents.

Policy evaluation must consider:

- tenant and principal status;
- actor versus subject and delegation lineage;
- target and broker-role eligibility;
- requested purpose, action, resource, and TTL;
- authentication assurance and recency;
- device, node, workload, build, and artifact attestation;
- network, environment, time, risk, and incident state;
- current lease count, concurrency, budget, and SoD conflicts;
- approval or break-glass evidence.

Trust evidence must have issuer, audience, freshness, nonce/replay, and verification rules. A signed assertion alone is not sufficient if its binding or freshness is unknown.

## 9. Secret-Safe Delivery

Delivery preference, from strongest to weakest:

1. **Mediated request:** a proxy signs or authenticates the target request; the workload never receives the credential.
2. **Local workload agent:** credential is streamed through a mutually authenticated local channel into memory and rotated automatically.
3. **Client-key binding:** broker returns a certificate/token bound to a requester-held key.
4. **Response wrapping:** broker returns a single-use, short-TTL unwrap reference to an authenticated client.
5. **One-time direct response:** allowed only when required by target/client compatibility, with strict no-store behavior.

Requirements:

- never place credentials in URLs, browser storage, telemetry, audit, errors, traces, clipboard by default, or support exports;
- set `Cache-Control: no-store` and equivalent controls;
- allow one successful unwrap, then destroy wrapping state;
- bind unwrap to subject, client instance/channel, audience, and deadline;
- do not make raw secret retrieval available in the administrative UI;
- display only lease ID, fingerprint, scope, expiry, and delivery status;
- acknowledge that process memory can still leak and document client hardening.

## 10. Renewal, Rotation, and Revocation

Renewal and rotation are distinct:

- **renewal** extends or replaces access under the same bounded lease lineage after re-evaluation;
- **rotation** creates new credential material and retires the prior material, optionally with a controlled overlap;
- **revocation** invalidates the lease and target credential as soon as the target permits.

The system must:

- refresh before expiry with jitter and backoff;
- cap overlap and expose both credentials’ states;
- deny renewal after trust, role, ownership, or policy changes;
- cascade incident revocation across lease lineage and related sessions where configured;
- separate broker-side state change, target dispatch, target acknowledgment, and readback verification;
- publish high-confidence status changes to security-signal consumers;
- never label a credential “revoked” when only broker metadata changed.

## 11. Approval and Break-Glass

Human approval is appropriate for interactive, privileged, novel, or high-impact access. Routine workload leases should rely on pre-approved policy and strong attestation rather than impossible per-request approvals.

Approval requirements:

- show caller, target, role, scope, duration, purpose, evidence, and risk;
- prohibit self-approval unless an explicit exception policy allows it;
- support ordered stages, quorum, expiry, escalation, and delegated approvers;
- bind approval to the exact request digest;
- invalidate approval when material request fields change;
- make approvals time-limited and one-use unless explicitly reusable.

Break-glass must require reason, shortest practical TTL, strong authentication, immediate notification, enhanced logging, post-use review, and explicit cleanup verification. It must not silently bypass target-side safety controls.

## 12. Connector Contract

Each connector declares independent capabilities:

- `issue`, `renew`, `rotate`, `revoke`, `lookup`, `list`, `reconcile`, and `terminate_sessions`;
- supported credential kinds and target roles;
- TTL bounds and target-side expiration behavior;
- early-revocation semantics;
- idempotency support;
- maximum throughput and rate limits;
- health and dependency checks;
- evidence returned by each operation;
- secret fields requiring zeroization/redaction.

Connector credentials must be stored by reference in a protected external secrets/KMS/HSM facility, scoped to the narrowest target operations, rotated independently, and never returned via broker APIs.

Untrusted connector code must run with isolation, signed artifacts, constrained network access, least filesystem access, resource limits, and a reviewed plugin lifecycle.

## 13. API Requirements

Provide versioned endpoints for:

- `/targets`, health, capabilities, and emergency disablement;
- `/connectors`, versions, tests, rotation, and reconciliation;
- `/roles`, versions, simulation, approval, and publication;
- `/lease-requests`, evaluations, approvals, denials, and cancellation;
- `/leases`, metadata, renew, rotate, revoke, reconcile, and lineage;
- `/unwrap` as a narrowly scoped one-time exchange;
- `/approvals`, delegation, expiry, and escalation;
- `/incidents/revoke` for authorized bulk containment with preview;
- `/evidence-bundles`, reports, and audit references;
- local agent/SDK streaming interfaces where appropriate.

API rules:

- raw credential values exist only in issuance/delivery responses designed for them;
- normal read/list endpoints can never serialize secret material;
- use idempotency keys, optimistic concurrency, typed errors, stable pagination, and audit correlation;
- require proof-of-possession or channel binding for high-value automated delivery where supported;
- rate-limit by tenant, principal, role, target, and connector;
- process connector operations asynchronously when latency/retry warrants it;
- return policy and lifecycle reasons without leaking target or secret internals.

## 14. Credential Broker UIX

### Overview

Show:

- active and expiring leases;
- privileged and break-glass leases;
- issuance, renewal, and revocation failures;
- unverified or orphaned target credentials;
- connector health and reconciliation freshness;
- static-credential reduction posture;
- approvals awaiting action;
- top roles, targets, and anomalous lease patterns.

### Targets and connectors

Use a guided setup for target identity, issuer, protected connector credential reference, network path, capabilities, role discovery, health test, and restricted publication. Clearly distinguish discovery-only, issue-capable, and revoke-capable integrations.

### Broker role studio

Provide a staged editor for target mapping, credential template, eligibility, attestation, scope, TTL, approval, delivery, limits, renewal, revocation, and evidence. Include dry-run simulation and version diff before publication.

### Request experience

Let authorized people request a role using business context. Show exact target, permissions, duration, prerequisites, approvers, delivery method, and cleanup behavior. Never show connector/root credentials.

### Approval inbox

Prioritize risk and expiry. Show the immutable request digest and material policy facts. Offer approve, deny, request change, delegate, and abstain controls with reason capture.

### Lease inventory and detail

Filter by principal, target, role, kind, state, expiry, approval, incident, and connector. Detail shows lineage, policy, trust evidence, delivery acknowledgment, renewals, target events, revocation progress, and safe fingerprints—not secret values.

### Incident revocation

Support scoped preview by principal, artifact, workload, target, role, connector, or time window. Show likely impact, target limitations, session-termination capability, staged progress, failures, retry, and evidence export.

### Developer integration center

Provide agent/SDK configuration, environment-specific endpoints, workload identity setup, safe sample code, renewal behavior, failure handling, and deterministic sandbox targets. Examples must not normalize secret environment variables when mediated alternatives exist.

## 15. Security, Privacy, and Reliability

- Separate broker administration, connector administration, role ownership, approval, incident revocation, and audit authority.
- Enforce tenant isolation across data, jobs, caches, connector pools, metrics, and logs.
- Store secret metadata and encrypted transient delivery material separately; minimize transient retention.
- Use HSM/KMS/external signers for CA and high-value broker keys.
- Treat connector compromise as a root-risk scenario with scoped credentials and emergency disablement.
- Prevent SSRF through allowlisted target definitions, controlled egress, DNS/IP validation, and no user-provided arbitrary endpoints at request time.
- Prevent command, SQL, template, path, header, and claim injection in adapter inputs.
- Apply replay protection and bind requests/approvals/unwraps to exact contexts.
- Use transactional outbox, idempotent connector operations, reconciliation, and dead-letter operations.
- Define degraded behavior: fail closed for new issuance when authorization/trust is unavailable; preserve safe renewal only under explicit bounded policy.
- Never log raw credentials, authorization headers, DSNs, private keys, unwrap tokens, or connector secrets.
- Test backup/restore so lease metadata recovers without reviving expired credentials or transient secret material.

## 16. Observability and Evidence

Record secret-free events for request, evaluate, approve, deny, issue, delivery, unwrap, renew, rotate, expire, revoke request, target acknowledgment, reconciliation, failure, and emergency containment.

Each event includes actor/subject, tenant, target/role/lease IDs, connector version, policy decision reference, reason code, timestamps, correlation, outcome, and safe fingerprint.

Evidence bundles should contain:

- policy and role versions;
- caller/attestation verification references;
- approval record and request digest;
- lease timeline;
- connector operation digests and target acknowledgments;
- reconciliation result;
- integrity manifest;
- explicit exclusions stating that secret material is not included.

## 17. Stakeholder Requirements

### Technical marketing

Demonstrate “identity in, short-lived access out” across one database, one cloud provider, SSH, and one mediated third-party API. Show automatic expiry, failed renewal after trust change, incident revocation, and proof without exposing credentials. Label adapters and maturity precisely.

### Developer relations

Deliver SDK/agent quickstarts, workload federation setup, CI examples, database connection renewal, SSH certificate use, wrapped-response handling, proxy signing, connector authoring, sandbox fixtures, and failure/retry guidance. Include unsafe-versus-safe integration comparisons.

### Sales and account management

Provide discovery questions for target systems, credential kinds, workload platforms, identity sources, issuers, TTLs, approval needs, network paths, HSM/KMS, scale, regulations, incident needs, and existing vaults. Position the product as integration-friendly, including coexistence with established secret engines.

### GTM strategist

Lead with workload/CI federation and short-lived database/cloud access, then expand to SSH, third-party APIs, agents, and incident containment. Do not claim elimination of all secrets: connector bootstrap, unsupported targets, and legacy systems may still require protected long-lived credentials.

### Copywriter

Standardize `credential`, `lease`, `role`, `target`, `delivery`, `renewal`, `rotation`, `revocation requested`, and `revocation verified`. Avoid “secretless,” “zero standing privilege,” “revoked,” or “never exposed” without qualification and supporting evidence.

## 18. Delivery Instructions

### Frontend engineer

- Generate typed clients from the broker API and enforce no-secret response models in ordinary views.
- Never persist issuance responses in browser state beyond the minimum delivery interaction.
- Disable analytics/session replay on sensitive request, unwrap, connector, and emergency workflows.
- Implement server-side pagination and streaming job progress for large lease inventories and incident revocation.
- Require simulation, diff, and confirmation for role publication and bulk containment.
- Render lifecycle and connector capability states explicitly.
- Provide accessible keyboard workflows and non-color status indicators.

### UIX designer

- Design around leases and outcomes, not a folder tree of stored secrets.
- Make TTL, scope, principal, target, delivery, and revocation proof prominent.
- Distinguish broker state from target-confirmed state.
- Design no-data, stale, degraded, partial-capability, partial-failure, and incident states.
- Keep raw secret reveal out of admin concepts; where one-time delivery is unavoidable, design acknowledgement and immediate dismissal.
- Test dense operational screens with platform engineers and incident responders.

### Copywriter

- Explain exactly what a credential permits and when it stops working.
- State provider limitations for early revocation and active-session termination.
- Write warnings before one-time delivery, privileged approval, role publication, and incident revocation.
- Keep target-native terms available but translate them into consistent broker language.

## 19. Delivery Phases

### Phase 1: Broker core and one reference target

- canonical target, role, request, approval, lease, and connector contracts;
- policy/identity/attestation integration;
- safe delivery SDK and lease inventory UIX;
- one dynamic database or cloud STS adapter;
- expiry, revocation, reconciliation, and evidence.

### Phase 2: Workload and delivery hardening

- local agent, response wrapping, key binding, and mediated requests;
- SPIFFE/Kubernetes/CI federation;
- high-scale renewal, backoff, rate limits, and outage behavior;
- connector SDK and conformance suite.

### Phase 3: Credential portfolio

- database matrix, multi-cloud STS, OpenSSH certificates, client certificates;
- third-party OAuth/token exchange and request-signing adapters;
- approval, break-glass, incident bulk revocation, and session termination where supported.

### Phase 4: Ecosystem and continuous response

- partner connector catalog;
- security-signal-driven revoke/deny-renew;
- agent/tool credential mediation;
- regional controls, HSM profiles, regulated evidence, and enterprise scale certification.

## 20. Acceptance Criteria

### API and runtime

- A verified principal can request only published roles for which current policy allows it.
- Material request changes invalidate prior approval.
- Issuance retries do not create uncontrolled duplicate target credentials.
- Ordinary read/list/audit/export APIs never return secret material.
- One-time unwrap is subject/channel/time bound and succeeds at most once.
- Renewal re-evaluates policy and respects maximum lifetime.
- Expiry and revocation initiate target cleanup and reconciliation.
- UI/API distinguish requested, dispatched, acknowledged, and verified revocation.
- Connector capabilities and limitations are machine-readable.
- Compromise signals can deny renewal and trigger scoped revocation.
- Cross-tenant target, role, lease, connector, or evidence access is denied and tested.

### UIX

- An operator can create and simulate a role without seeing connector credentials.
- A requester understands scope, duration, approval, delivery, and cleanup before submission.
- An approver can make a decision using immutable request context.
- Lease detail reconstructs the lifecycle without exposing the credential.
- Incident responders can preview, execute, monitor, retry, and export scoped revocation.
- No-data, stale, degraded, and target-unverified states are distinct.
- Core workflows meet WCAG 2.2 AA.

### Evidence and business

- Reference demos cover issue, use, renew, expiry, deny-renew, revoke, failed cleanup, reconcile, and compromise containment.
- Each supported adapter has conformance, failure, redaction, idempotency, and cleanup tests.
- Marketing claims map to named tested delivery modes and connector capabilities.
- Recovery tests do not restore expired leases or transient secret material.

## 21. Success Measures

- percentage of access delivered through short-lived versus static credentials;
- median and p95 credential TTL by risk tier;
- issuance and renewal latency/success rate;
- percentage of leases using mediated, agent, or key-bound delivery;
- revocation-request-to-target-verification time;
- orphaned/unverified lease count and age;
- connector reconciliation freshness and error rate;
- approval wait time and expiry-before-use rate;
- denied renewal after trust/policy change;
- incident containment completion and failure rate;
- static credential retirements attributable to broker adoption;
- secret leakage detections in logs, telemetry, or client storage, with a target of zero.

## 22. Source Evidence

### Repository

- `docs/strategy/uix-pairing-briefs/10-additional-api-uix-opportunity-map.md`
- `docs/m2m-workload-identity-focus.md`
- `docs/strategy/identity-market-roadmap.md`
- `docs/architecture/TEMP_IDENTITY_PACKAGE_BOUNDARY_PROPOSAL.md`
- `pkgs/01-storage/tigrbl-identity-storage/`
- `pkgs/20-providers/tigrbl-authn-credentials/`
- `pkgs/20-providers/tigrbl-authz-policy/`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-service-admin/`
- `tests/integration/test_service_key_creation.py`
- prior workload, attestation, certificate, token-service, agent-delegation, and entitlement-governance pairing briefs.

### Standards and primary product references

- [HashiCorp Vault lease model](https://developer.hashicorp.com/vault/docs/concepts/lease): dynamic-secret leases carry duration and renewability and can be renewed or revoked.
- [HashiCorp Vault database secrets engine](https://developer.hashicorp.com/vault/docs/secrets/databases): target-specific dynamic and static database role patterns.
- [AWS IAM temporary security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html): dynamically generated, expiring cloud credentials.
- [SPIFFE concepts](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/) and [SPIFFE Workload API](https://spiffe.io/docs/latest/spiffe-specs/spiffe_workload_api/): attested workload identity and frequently rotated short-lived SVIDs.
- [OpenSSH `ssh-keygen` manual](https://man.openbsd.org/ssh-keygen): signed user/host certificates, principals, options, and validity intervals.
- [RFC 8693, OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693): exchanging subject/actor credentials for audience/resource-bound tokens.
- [RFC 8705, OAuth 2.0 Mutual-TLS](https://www.rfc-editor.org/rfc/rfc8705) and [RFC 9449, DPoP](https://www.rfc-editor.org/rfc/rfc9449): sender-constrained token profiles.

## 23. Explicit Non-Claims

- Existing service keys, API keys, and token exchange do not yet constitute a credential broker.
- The broker does not eliminate every root, connector, or legacy secret.
- Short TTL reduces exposure; it does not make stolen credentials harmless.
- Broker-side revocation does not prove target-side invalidation or session termination.
- Encryption at rest does not justify secret display in an administrative UI.
- SPIFFE identifies workloads; it does not decide target authorization or mint every downstream credential.
- This pairing does not replace every vault, cloud STS, CA, SSH CA, database, PAM session manager, or target-native authorization system.
- “Zero standing privilege” is not valid when standing connector authority or target roles remain broader than each lease.
