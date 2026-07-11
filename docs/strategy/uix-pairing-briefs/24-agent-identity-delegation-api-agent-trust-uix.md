# Agent Identity and Delegation API + Agent Trust UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-api-agent-delegation` + `@tigrbl-auth/agent-trust-uix`  
**Status:** New product surface; delegation, attenuation, authority graph, token exchange, proof binding, policy, workload, audit, and provenance foundations exist  
**Prepared:** July 11, 2026  
**Proposed API owner:** `pkgs/80-apis/tigrbl-auth-api-agent-delegation`  
**Proposed protocol/profile owners:** OAuth/RAR/token-exchange, optional GNAP, transaction-token, tool-protocol, and agent-runtime adapters  
**Proposed UIX owner:** `pkgs/95-ui/agent-trust-uix`

## 1. Product Decision

Create a governed identity and delegation surface for AI/software agents that binds every agent instance to a sponsor, owner, purpose, runtime/workload identity, model/application profile, tools/resources, authority source, budget, time window, credentials, approvals, task/transaction, actions, outcomes, and revocation state.

Treat an agent as a sponsored non-human principal and workload/client instance, not as:

- the human user who requested work;
- the service account whose credentials it can access;
- the model/provider name;
- a chat session;
- a generic OAuth client with broad scopes;
- a trustworthy actor because its output sounds plausible;
- a new home-grown "AI agent JWT."

The product should compose existing OAuth, GNAP, RAR, token exchange, sender-constrained tokens, delegation grants, authorization decisions, workload attestation, transaction contexts, security signals, and non-bearer receipts. New token formats are unnecessary unless a reviewed standards profile creates a concrete interoperability advantage.

## 2. Current Repository Reality

The repository already has unusually strong foundations for agent authorization:

- durable delegation grants, scopes, proofs, parent/child edges, token links, revocation/expiry/replacement, and audit;
- `DelegationGrantSpec`, lifecycle entries, normalized tenant/action/resource scopes, and attenuation proofs with uncovered scopes;
- authority nodes/edges/scopes, path/reachability proofs, constraints, provenance, and graph integrity;
- RFC 8693 token exchange with subject/actor semantics, delegation versus impersonation, resources/audiences, DPoP/mTLS binding, authorization trace, and delegation lineage;
- RFC 9396 Rich Authorization Requests and resource indicators;
- policy decisions, default-deny direction, relationships, obligations, and decision provenance;
- workload/service/client/machine/device principal types, credentials, attestation, trust domains, and service administration;
- token hashing, revocation, refresh/exchange lineage, resource validation, audit, and security signals;
- planned authorization budgets and delegation-constraint tests.

Missing capabilities include:

- canonical agent definition/instance/sponsor/task/tool/action/budget records;
- lifecycle and separation of model, application, runtime, and agent instance;
- tool/resource schemas and parameter/transaction binding;
- human/service sponsorship, consent/approval, and purpose controls;
- runtime action gateway/enforcement and verified outcomes;
- monetary/rate/data/compute/time/risk budgets;
- memory/context provenance and data-use boundaries;
- prompt/tool injection and confused-deputy controls;
- agent-specific operations UIX, incidents, and ecosystem adapters.

The authorization-budget test is currently skipped as a planning placeholder. Budget support must not be claimed until durable atomic enforcement and concurrency tests exist.

## 3. Users and Jobs

### Human sponsor/requester

1. delegate a clearly described task, resources, actions, constraints, budget, and expiry to an agent.
2. understand which agent/application/model/runtime will act and on whose behalf.
3. approve high-risk or changed actions with exact transaction details.
4. monitor progress and stop/revoke work immediately.
5. receive a concise outcome and tamper-evident delegation/action receipt.

### Service/business sponsor

1. authorize unattended agents under service-owned policies and limited budgets.
2. separate customer, tenant, environment, and data-purpose boundaries.
3. rotate runtime credentials and change models/tools without silently changing authority.
4. prove which business process authorized every action.

### Security/identity administrator

1. register agent apps/runtimes/tools and establish owners, attestations, keys, and policies.
2. review delegation chains and attenuation.
3. detect dormant/orphaned agents, wildcard tools, excessive scopes, deep delegation, unusual spending/data access, and failed approvals.
4. quarantine an instance/app/runtime/tool/model/provider and revoke descendants.

### Tool/API owner

1. publish a typed resource/action/parameter contract and required assurance.
2. receive a short-lived, audience/transaction/proof-bound authorization artifact.
3. validate sponsor/agent/actor/delegation context without trusting client-supplied prose.
4. return structured action receipts and reject replay/parameter drift.

### Developer/agent builder

1. register the agent app and tool dependencies.
2. request only needed access using RAR/GNAP or approved templates.
3. run locally with test identities, policies, budgets, and negative fixtures.
4. obtain credentials without embedding human/service secrets.
5. diagnose denials with stable reasons and safe traces.

## 4. Architectural Ownership

### Agent identity domain owns

- agent definition/application, version, instance/session/task, sponsor, purpose, runtime, model/profile, tool set, data policy, lifecycle, and ownership;
- agent-specific task/action/budget and approval semantics;
- linkage to workload/client/service/human principals without duplicating them;
- agent posture and operations projection.

### Authorization/delegation packages own

- source authority, resource/action scopes, constraints, reachability, attenuation, approval/obligation, decision, and revocation semantics;
- parent/child delegation graph and proof;
- no agent-specific shortcut around policy.

### Protocol/token packages own

- OAuth RAR/resource indicators/PAR, RFC 8693 exchange, DPoP/mTLS, introspection/revocation;
- GNAP grant negotiation if separately implemented;
- transaction tokens only under a pinned draft/future RFC profile;
- no token minting in Agent UIX.

### Agent Delegation API owns

- lifecycle orchestration, task/grant/action/budget/approval runtime, tool gateway contracts, query, evidence, incidents, metrics, and UI schemas;
- integration with Policy Studio, Token Service, Workload Trust, Attestation, Security Signals, and Secrets Broker;
- tenant-safe product filtering and no direct private-secret handling.

## 5. Agent Identity Model

### Agent definition/application

- stable ID, tenant/owner, name, purpose/category, product/app package, publisher, lifecycle, and version;
- supported runtime types, model/provider profiles, tools/resources, data classifications, interaction modes, and human/unattended posture;
- default policy/budget templates and required approvals;
- release signature/provenance, dependencies, security review, and compatibility;
- no authority by existence alone.

### Agent instance

- unique short-lived/runtime-bound instance ID and canonical agent definition/version;
- sponsoring principal/service/tenant and initiating requester;
- workload/client principal, runtime deployment, environment, attestation result, key/credential/proof binding;
- model/provider/version/configuration as observed, not identity root;
- task/session, purpose, authorized tools/resources, delegation grant, budget, start/expiry, and status;
- parent agent/instance where sub-agent delegation exists;
- never use conversational display name as security identifier.

### Sponsor

Sponsor owns the business authority and accountability context. A human sponsor uses current authenticated session/consent/approval. A service sponsor uses service authority/policy and explicit process. Model vendor, tool vendor, developer, operator, and customer may be different parties and require separate provenance.

### Agent lifecycle

- draft/registered;
- approved/active;
- instance starting/attesting;
- running/paused/waiting approval;
- completed/failed/canceled;
- expired/revoked/quarantined;
- definition suspended/retired;
- compromised/under investigation.

Completed or failed instances cannot resume authority without a new task/grant.

## 6. Task and Purpose Model

Every agent action belongs to a task/transaction with:

- human-readable goal and machine-readable task type;
- sponsor, requester, beneficiary, tenant/customer, purpose, and legal/data-use basis;
- permitted resources/actions/tools and parameter constraints;
- inputs/references and sensitivity classification, with digests rather than unnecessary copies;
- expected outputs/destinations and retention;
- time/step/rate/monetary/data/compute/risk budgets;
- required approvals and escalation;
- success, failure, cancel, rollback, and verification criteria;
- parent task and child tasks/agents;
- immutable context/version digest used for authorization and receipts.

Free-form prompt text is not an authorization policy. It may describe intent, but typed task fields and server-side policy govern authority.

## 7. Tool and Resource Contract

### Tool definition/version

- tool ID/version, owner/publisher, endpoint/provider, environment, lifecycle, and release provenance;
- typed operations with resource/action identifiers, JSON/schema/protocol inputs/outputs, side effects, idempotency, reversibility, and risk;
- authentication/proof requirements, resource server/audience, data classifications, egress/retention, rate/cost, and required approvals;
- integrity/signature/digest and compatibility;
- no arbitrary tool metadata from an untrusted prompt at runtime.

### Tool call authorization

1. agent proposes typed operation/resource/parameters and purpose/task;
2. gateway canonicalizes request and calculates transaction digest;
3. resolve active instance, sponsor, delegation path, tool version, current budget/posture, and dependencies;
4. authorize exact action/resource/parameter/transaction under current policy;
5. reserve budget atomically and issue short-lived audience/transaction/proof-bound token or internal capability;
6. tool validates token/proof and exact request digest before effect;
7. tool returns signed/authenticated outcome receipt;
8. gateway commits/reconciles budget and emits audit/security signals;
9. agent receives sanitized result allowed by task/data policy.

An LLM's tool name or function call is a proposal, not authorization.

## 8. Delegation and Attenuation

### Delegation chain

- sponsor/delegator to agent instance;
- optional agent to sub-agent only if source policy allows redelegation;
- each child grant links parent/source authority, scopes, constraints, policy, provenance, proof, time, and revocation;
- normalized tenant/realm/resource/action scopes use existing authority/delegation contracts;
- every child must be a provable subset of effective parent authority and budgets;
- cap chain depth/fan-out and reject cycles;
- revoked/expired/replaced parent invalidates descendants promptly.

### Constraints

- tenant/customer/environment;
- tool/operation/resource/record;
- parameter/value/range/destination;
- purpose/task/transaction digest;
- start/expiry/max age;
- rate/count/money/data/compute/risk;
- location/network/device/workload posture;
- required human/role approvals;
- no redelegation or bounded sub-agent type/count;
- output/egress/retention.

### Attenuation proof

Extend existing proof semantics beyond static scopes to typed constraint and budget partial order. If constraint ordering cannot be proven safely, require a new explicit authorization rather than assuming attenuation.

## 9. Authorization Protocol Strategy

### OAuth profile

Near-term default:

- registered confidential/public client/workload identity as appropriate;
- RAR `authorization_details` for typed tool/resource/action/parameters;
- PAR/JAR for protected large requests where interactive authorization applies;
- resource indicators for target API;
- RFC 8693 subject/actor tokens for sponsor/agent delegation;
- short-lived DPoP/mTLS-bound access tokens;
- `act`, grant/lineage/transaction references, minimal claims, introspection/revocation;
- no long-lived refresh token for ephemeral instances unless narrowly justified.

### GNAP profile

RFC 9635 GNAP is a strong fit for dynamic software-instance grants, multi-stage interaction, continuation, multiple resource tokens, subject information, key-bound requests, and negotiated approval. However, GNAP is parallel to OAuth, not an OAuth extension.

If implemented:

- dedicated contracts/protocol package and resource-server integration;
- client instance key proof and rotation;
- grant request, pending/approved/denied states, interaction, continuation token, access token, subject information, and management;
- map resulting grant to canonical delegation/task/budget/evidence without pretending OAuth wire compatibility;
- start as a preview profile with test clients/resources.

### Transaction tokens

The IETF transaction-token specification and agent-specific work are active Internet-Drafts in 2026. Research/pilot use must pin a revision, label preview, constrain trusted-domain assumptions, bind transaction identity/authorization context across workloads, and plan migration. Do not market draft support as an RFC.

## 10. Agent Credentials and Runtime Trust

- agent app definition has no reusable secret by default;
- each runtime instance uses workload/client identity with short-lived key/credential;
- prefer DPoP/mTLS/SPIFFE or attested non-exportable keys;
- bind token to instance key, task/transaction, audience/resource, sponsor/delegation, and short expiry;
- model/provider API credentials are leased through Secrets Broker and never inserted into prompts/logs;
- human OAuth refresh tokens require explicit delegated connection records and bounded use, not agent storage;
- rotate/revoke on instance end, sponsor/session loss, workload posture change, definition/runtime/model/tool compromise, budget breach, or incident;
- successful attestation authenticates measured runtime posture under policy; it does not make model decisions safe.

## 11. Authorization Budgets

### Budget dimensions

- maximum tool calls/steps;
- per-tool/resource/action count;
- currency/value and per-transaction amount;
- data read/write/export rows/bytes/classification;
- compute/model tokens/runtime duration;
- external messages/recipients;
- sub-agent count/depth;
- risk-weighted actions;
- approval count and retry/failure limits.

### Enforcement

- durable budget and reservation/consumption/release ledger;
- atomic reservation before external effect;
- idempotency key ties retries to one reservation/action;
- pending/committed/released/expired/reconciled/disputed states;
- tool receipt confirms actual use/cost where possible;
- no negative or overflow balance and no concurrency overspend;
- child tasks receive explicitly allocated sub-budgets reducing parent availability;
- threshold actions pause/require approval rather than merely alerting;
- revoke/expire stops new reservations; in-flight policy is explicit;
- compensation/refund does not erase action history.

Budgets are authorization constraints, not billing-only metrics.

## 12. Human Approval and Interaction

Approval requests show:

- agent definition/instance/runtime/model and sponsor;
- task/purpose/customer and why approval is needed;
- exact tool/action/resource and material parameters/transaction data;
- data leaving/recipients, monetary/physical/business effect, and reversibility;
- current authority/budget and requested delta;
- deadline, one-time/reusable scope, downstream/sub-agent effect;
- safe preview/diff and policy recommendation/reasons.

Approval must be cryptographically/session bound to transaction digest, agent instance, policy/version, approver identity/role, expiry, and one-time use. "Approve all future actions" is a separate policy grant with explicit scope/time/budget, not a UI shortcut.

## 13. Prompt, Memory, and Data Boundaries

### Prompt/tool injection defense

- treat model output, retrieved documents, web pages, emails, tool responses, and user-provided content as untrusted data;
- separate system/policy/task/tool schemas from content channels;
- tools receive canonical typed parameters, not raw model-generated HTTP/SQL/shell where avoidable;
- server-side allowlists and policy validate destinations/resources/parameters;
- never let content instruct the runtime to reveal secrets, change sponsor, expand tools, approve itself, or disable audit;
- suspicious instruction/security events can pause task and request review.

### Memory/context

- classify task input, temporary context, durable memory, vector/retrieval indexes, tool outputs, and receipts separately;
- tenant/customer/purpose isolation and source provenance;
- TTL/retention/deletion and no automatic cross-task learning;
- sensitive data minimization/redaction before model/provider;
- model/provider data-use/no-training/region policy;
- memory cannot create authority or serve as trusted identity proof;
- deletion/revocation propagation across caches/indexes/providers is measured.

## 14. Action Receipts and Outcomes

Create non-bearer receipts for high-risk actions and approvals:

- receipt ID/version/type, tenant, task, agent instance, sponsor/requester/actor;
- tool/version, resource/action, parameter/transaction digest, purpose;
- delegation grant/path/proof, policy/decision, token/proof reference;
- budget reservation/actual delta;
- approval(s) and expiry;
- request/attempt/outcome/status/time, tool/provider evidence, correlation;
- signature/integrity digest and supersession/compensation linkage.

Receipts prove what the system recorded and who signed it; they do not necessarily prove physical/business-world success. Outcome verification can use domain-specific evidence and should be shown separately.

## 15. API Requirements

Use `/admin/agent-delegation` for management and `/agent-delegation/v1` for task/runtime operations. OAuth/GNAP endpoints remain protocol-owned.

### Agent definitions/instances

- CRUD/version lifecycle for agent definitions, releases, model/runtime/tool assignments, default policies/budgets, owners, and environments;
- validate, test, submit, approve, activate, suspend, supersede, retire;
- start/attest/activate/pause/resume/cancel/complete/fail/quarantine/revoke instance;
- no browser-supplied runtime attestation or model identity trust.

### Tasks/grants/actions

- create typed task and request delegation/grant;
- simulate authority/budget/tool/data impact;
- approve/deny/modify/cancel/expire;
- propose action, reserve/authorize, submit to gateway, record outcome, compensate/reconcile;
- spawn child task/agent with explicit attenuation/sub-budget;
- query lineage, decisions, receipts, budget, and current revocation.

### Tool registry/gateway

- tool definitions/versions/operations/schemas/risk/data policy;
- provider endpoint/credential reference and health;
- registration integrity, compatibility, test fixtures, activation;
- runtime invoke only through canonical authorized gateway or provider enforcement contract;
- no general arbitrary URL/shell/SQL tool in baseline.

### Operations

- approval queue, active task/agent inventory, incidents, security signals, audit, reports, and evidence exports;
- kill switch by instance/definition/runtime/model/provider/tool/sponsor/tenant;
- impact/descendant query and verified propagation.

## 16. Canonical Data Requirements

### Agent definition/version

- IDs, tenant/owner/publisher, purpose/category, app release/provenance, lifecycle/version;
- model/runtime/tool/data profiles, interaction modes, default task/policy/budget, and assurance;
- approvals, effective/retire, predecessor, compatibility, fixtures, and evidence.

### Agent instance

- definition/version, tenant, sponsor/requester, workload/client/runtime/environment, model/provider observed profile;
- key/credential/attestation, task, parent agent, delegation grant, policy, budget, start/expiry/status;
- current posture/heartbeat, pause/revoke/quarantine/end reason, and provenance.

### Task/action

- task contract from Section 6 and action proposal from Section 7;
- immutable request/context digests and typed material parameters with sensitive values encrypted/referenced;
- decision, budget reservation, approval, token/proof, attempts, result, receipt, and timestamps;
- parent/child links and no unbounded conversation transcript in auth storage.

### Budget ledger

- budget type/unit/limit/window, parent allocation, available/reserved/consumed/released, version;
- reservation/action/idempotency, requested/actual, state, expiry, and reconciliation;
- actor/decision/receipt/audit and tamper-evident sequence.

### Approval

- approver role/identity, exact transaction/task/action/policy/budget delta digest, decision, conditions, issued/expiry/used, and evidence;
- no reusable generic approval token.

## 17. Agent Trust UIX

### Overview

- active/waiting/paused/completed/failed/quarantined agents/tasks;
- authority, delegation depth, tool/data scope, budget, credential/attestation, approval, and incident posture;
- findings for orphan sponsor, wildcard action/resource, broad data egress, proof downgrade, stale runtime, model/tool version drift, budget anomaly, repeated denial, and deep sub-agents;
- current kill-switch/response state.

### Agent catalog and instance detail

- definition/version/owner/purpose/runtime/model/tools/policy/budget/release evidence;
- instance timeline from start/attestation/grant through actions/approvals/outcomes/end;
- sponsor/requester/parent-agent, workload identity, credential/proof, and current posture;
- model shown as implementation dependency, not security identity;
- accessible authority/action/budget/receipt views and optional graph.

### Delegation builder/review

1. choose sponsor, agent definition, task/purpose/customer;
2. select typed tools/resources/actions/parameters/data;
3. set time, redelegation, environment/posture, and budgets;
4. preview source authority and uncovered/excess scopes;
5. simulate representative actions and child delegation;
6. review risk/approvals/egress/irreversibility;
7. issue, activate, and monitor grant;
8. revoke/replace with descendant impact.

### Live task and approval workspace

- goal, typed plan, completed/current/proposed actions, resources/data, budget, approvals, receipts, and outputs;
- separate model explanation from server authorization reason;
- pause/cancel/revoke visible at all times;
- approval card shows exact transaction, not a conversational summary alone;
- outcome verification/compensation and human notes;
- no chain-of-thought capture requirement; use concise action rationale and evidence.

### Tool and policy studio

- tool operation schemas, side effects, risk, data, authentication, rate/cost, idempotency, and provider health;
- policy/budget templates linked to Policy Studio;
- synthetic/adversarial simulation for injection, destination change, amount change, replay, budget race, sub-agent escalation, proof downgrade, and revoked sponsor;
- version diff, impacted agents/tasks, staged activation, rollback.

### Incident/kill switch

- stop new actions while preserving investigation and defined in-flight handling;
- revoke tokens/grants/leases and quarantine runtime/tool/provider;
- descendant and pending approval/action impact;
- credential/data/memory cleanup and verified propagation;
- redacted incident/evidence/action receipt bundle.

## 18. Security, Privacy, Safety, and Reliability

- Default deny; authority derives only from active sponsor/source grant and current policy.
- Strongly authenticate/attest agent workload/client instance and bind every token/action to its key.
- Prevent sponsor/actor substitution, impersonation ambiguity, cross-tenant tasks, delegation cycles, scope/constraint/budget amplification, proof downgrade, and stale grant use.
- Treat prompts/retrieval/tool results/model output as untrusted; keep policy/tool schemas and secret context out of model control.
- Use short-lived audience/transaction-bound PoP tokens and no raw human/service secrets in agent context.
- Enforce budgets atomically under concurrency and reconcile external effects.
- Require explicit high-risk approvals bound to exact parameters; protect approval UI from clickjacking/phishing/fatigue.
- Limit steps, depth/fan-out, tool calls, payloads, destinations, retries, and runtime.
- Use idempotency, outbox, queues, deadlines, circuit breakers, compensation, and verified outcome.
- Isolate tenant/customer/task memory and prevent provider training/retention contrary to policy.
- Redact prompts/tool results/secrets/personal data from logs, receipts, analytics, notifications, and support exports.
- Define physical/financial/legal safety constraints outside model discretion.
- Exercise runaway agent, compromised tool/provider/model/runtime, mass token theft, budget race, approval spoof, data exfiltration, and kill-switch failure.

## 19. Stakeholder Requirements

### Technical marketing

- demonstrate sponsored task, typed delegation, proof-bound tool call, approval, budget, receipt, and revocation using synthetic data;
- explain agent identity versus model name and delegation versus impersonation;
- prepare stories for enterprise automation, finance operations, developer/CI agents, customer support, healthcare administration, procurement, analytics, and security operations;
- never claim autonomous safety or accountability because audit logs exist.

### Developer relations

- provide agent SDK/runtime adapters, RAR/token exchange/GNAP examples, tool gateway contracts, budget/approval/receipt APIs, and test agent/tool fixtures;
- adversarial tests for injection, scope escalation, actor substitution, stale/revoked grant, proof mismatch, replay, parameter drift, budget race, sub-agent cycle, and tool compromise;
- document error/retry/idempotency, kill-switch, data handling, and no-secret prompt patterns;
- label transaction-token/agent drafts as experimental.

### Sales and account management

- use an assessment for sponsors/users, agent use cases, models/providers, runtimes, tools/resources, data, actions/risks, budgets, approvals, unattended operation, audit, region, and incidents;
- provide readiness report separating identity, runtime trust, delegation, tools, policy, credentials, budget, approvals, memory/data, outcomes, and operations;
- define RACI across customer/sponsor, agent developer, model provider, runtime, tool/API owner, Tigrbl, security, and business approver;
- avoid promising model accuracy, safety, non-repudiation, or regulatory compliance from identity controls alone.

### GTM strategist

- package Agent Registry, Delegated Access, Tool Gateway, Budget/Approval Controls, and Agent Operations separately;
- prioritize bounded read/analysis and reversible enterprise workflows before autonomous financial/physical/high-impact actions;
- pair with Authorization, Token, Workload Trust, Attestation, Security Signals, and Secrets Broker;
- meter active agent/task, authorized tool, action volume, budget governance, retention, or enterprise tier—never approval/revocation usage.

### Copywriter

- distinguish agent app, instance, model, runtime, sponsor, requester, actor, tool, task, grant, token, budget, approval, action, outcome, and receipt;
- say "agent requested" versus "policy authorized" versus "tool reported success";
- avoid anthropomorphic claims of intent/understanding/accountability;
- expose sponsor, purpose, exact effect, data egress, budget, expiry, and reversibility;
- label unattended, preview/draft-standard, and model-generated rationales clearly.

## 20. Delivery Instructions

### Frontend engineer

- generate typed clients and render server authority/attenuation/budget/decision/receipt data;
- never use model-produced text as the source of action parameters/approval digest;
- keep secrets, raw tokens, prompts, sensitive tool results, and hidden chain-of-thought out of browser logs/analytics/storage;
- support live task updates, approval expiry, action concurrency, budget reservations, partial/unknown outcomes, pause/kill-switch, and stale versions;
- provide accessible tables/trees for graphs and safe diff of exact material parameters;
- instrument action pipeline stages with opaque IDs and safe categories.

### UIX designer

- separate model suggestion, agent proposal, policy decision, human approval, tool execution, and verified outcome;
- make sponsor/purpose/authority/time/budget/data/tool visible throughout;
- design draft/starting/attesting/running/waiting approval/paused/completed/failed/canceled/expired/revoked/quarantined/unknown outcome states;
- require parameter-level approval for financial/physical/external communication/data export actions;
- keep pause/stop accessible and distinguish stop-new-actions from cancel-in-flight;
- meet WCAG 2.2 AA with keyboard, focus, non-color state, live-region restraint, reduced motion, graph alternatives, and understandable automation timing.

### Copywriter

- create agent identity, delegation, task, tool, budget, approval, action, outcome, incident, reason-code, confirmation, and recovery catalogs;
- write sponsor/operator/developer/tool-owner/auditor language separately;
- avoid trust/safety certainty and expose evidence limitations;
- make approval one-time/scope/expiry/sub-agent/egress/budget consequences explicit;
- provide runaway agent, compromised tool/runtime/model, failed outcome, budget dispute, and kill-switch guidance.

## 21. Delivery Phases

### Phase 1: Canonical sponsored agent and bounded tools

- agent definition/instance/task/tool/action/approval/receipt contracts/storage;
- reuse existing delegation/authority/attenuation/token linkage;
- workload/client identity and DPoP/mTLS-bound short-lived tokens;
- one read-only and one reversible tool profile with Agent Trust UIX.

### Phase 2: Budgets and runtime gateway

- durable atomic budget ledger/reservations, typed tool gateway, exact transaction binding, approval queue, outcomes/compensation, sub-agent constraints, kill switch, and security signals;
- adversarial concurrency/injection tests.

### Phase 3: Dynamic grant protocols and secrets

- hardened RAR/token-exchange profile and optional GNAP preview;
- Secrets Broker leases, attestation-driven runtime trust, transaction-token pilot, external tool ecosystem adapters;
- certified resource-server/tool enforcement.

### Phase 4: High-impact vertical packs

- finance, healthcare administration, developer/CI, customer support, procurement, security, and physical/industrial agent packs;
- specialized approvals, safety, transaction data, evidence, retention, and regulatory analysis.

## 22. Acceptance Criteria

### API/runtime

- Every agent instance maps to active definition/version, sponsor, requester, workload/client/key, task/purpose, grant/path, policy, tools, budget, and expiry.
- Every action uses typed tool/resource/action/parameters and exact transaction digest.
- Child delegation is provably attenuated in scopes, constraints, time, redelegation, and budget, with bounded acyclic depth.
- Budget reservation prevents concurrent overspend and reconciles verified actual use.
- High-risk approval is exact, one-time, authenticated, expiring, and cannot be replayed after parameter change.
- Tool validates proof-bound short-lived authorization and returns traceable outcome.
- Revoking sponsor/grant/instance/tool/runtime propagates to descendants/tokens/leases/pending actions.
- No raw human/service secret or home-grown agent JWT is required.

### UIX

- Users can distinguish agent/model/runtime/sponsor and proposal/authorization/approval/execution/outcome.
- Delegation review exposes source authority, attenuation failures, budgets, sub-agents, and data egress.
- Approval shows exact material transaction effects and reversibility.
- Stop/kill switch is always accessible and its in-flight limitations are clear.
- Critical workflows work without graphs, model prose, hover, or color alone.

### Evidence/business

- DevRel can run deterministic positive/adversarial agent/tool/delegation/budget journeys.
- Technical marketing can demonstrate bounded autonomy with synthetic data and evidence-backed claims.
- Sales can provide agent readiness/RACI and risk-tier scope.
- GNAP/transaction-token/model/runtime/tool/safety/interoperability claims link to versioned certified evidence.

## 23. Success Measures

- registered/approved/active/orphaned/dormant/quarantined agent posture;
- task/action authorize/deny/approval/execute/outcome latency and rate;
- attenuation failures, delegation depth/fan-out, stale/revoked use prevention;
- budget reservation/overspend/reconciliation/dispute rate;
- high-risk approval modification/denial/fatigue and replay prevention;
- sender-constrained/attested runtime coverage;
- injection/data-egress/tool-compromise detections;
- kill-switch request-to-enforcement/verification time;
- unknown/failed/compensated outcome rate;
- secret/prompt/personal data leakage and cross-tenant action incidents.

Guardrails include sponsor ambiguity, impersonation, authority amplification, runaway budget, approval spoof/fatigue, prompt injection, tool confused deputy, secret leakage, false outcome, unsafe physical/financial action, memory cross-contamination, and overstated autonomy/safety.

## 24. Source Evidence

### Repository

- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/delegation/`;
- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/authority/graph.py`;
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/delegation_grant/`;
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/authority_derivation_graph/`;
- `pkgs/40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/delegation.py`;
- authority derivation/attenuation capabilities and tests;
- RFC 9396 RAR, RFC 8693 token exchange, resource indicators, DPoP/mTLS, token/delegation provenance, policy, workload, attestation, audit, and security-signal foundations;
- `tests/security/planning/test_authorization_budgets_planning.py` as planning-only evidence;
- Agent Identity opportunity-map entry.

### Standards and primary sources

- [RFC 9635: Grant Negotiation and Authorization Protocol](https://www.rfc-editor.org/rfc/rfc9635)
- [RFC 9396: OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396)
- [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/rfc/rfc8693)
- [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707)
- [RFC 9449: OAuth 2.0 DPoP](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 8705: OAuth 2.0 mTLS](https://www.rfc-editor.org/rfc/rfc8705)
- [OAuth Transaction Tokens, active Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/)
- [Transaction Tokens for Agents, active Internet-Draft](https://datatracker.ietf.org/doc/draft-oauth-transaction-tokens-for-agents/)

## 25. Explicit Non-Claims

This brief does not claim that the current repository:

- implements canonical agent identities, tasks, tools, actions, approvals, budgets, or receipts;
- provides atomic authorization budget enforcement;
- implements GNAP, transaction tokens, or agent-specific standards drafts;
- safely authorizes LLM/model tool calls directly;
- proves model identity, accuracy, intent, safety, or outcome;
- prevents prompt/tool injection or cross-task memory leakage;
- provides a secrets broker or autonomous high-impact transaction safety;
- can create an "AI agent JWT" and treat it as sufficient agent governance.

Those claims require canonical agent/runtime/tool models, typed enforcement, proof-bound short-lived credentials, durable attenuation/budgets, exact approvals, prompt/data isolation, outcome receipts, adversarial/concurrency tests, runtime/tool interoperability, safety/privacy/legal analysis, and release certification.
