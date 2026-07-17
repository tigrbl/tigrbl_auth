# Service Admin API + UIX Requirements Brief

**Pairing:** `tigrbl-auth-backend-app-service-admin` + `@tigrbl-auth/service-admin-uix`<br>
**Status:** Delivery brief<br>
**Prepared:** July 11, 2026<br>
**Backend app owner:** `pkgs/90-backend-apps/tigrbl-auth-backend-app-service-admin`<br>
**UIX owner:** `pkgs/105-ui/service-admin-uix`

## 1. Product Decision

Deliver this pairing as the workload-identity control plane for service principals, service keys, API keys, token inspection, protected-resource metadata, validation testing, credential rotation posture, and workload audit context.

The experience must organize credentials around an owned service identity and make lifecycle, scope, expiry, last use, and revocation explicit. It is not a human identity console, public login flow, tenant lifecycle surface, developer application catalog, or unrestricted token database browser.

## 2. Users and Jobs

### Primary users

- Platform and service engineers managing non-human identities.
- SRE and operations teams rotating workload credentials.
- Security engineers reviewing least privilege, validation, and audit posture.
- Service owners inspecting credentials attached to their workloads.

### Primary jobs

1. Create and govern a service/workload identity.
2. Issue, rotate, expire, and revoke service keys.
3. Issue, scope, update, and revoke API keys.
4. Inspect sanitized token records and validation metadata.
5. Test introspection and understand allow/deny results.
6. Review rotation events and workload audit history.
7. Determine which workloads are affected before credential or identity changes.

## 3. API Boundary

The UIX consumes exactly one configured service-admin API base URL through `VITE_TIGRBL_AUTH_SERVICE_ADMIN_API_BASE_URL`.

### Owned capabilities and resources

- `ServiceIdentity`
- `CredentialServiceKey`
- `CredentialApiKey`
- `TokenRecord`
- Workload-filtered `AuditEvent`
- Introspection
- OpenID Provider metadata at global, tenant, and realm scopes
- OAuth protected-resource metadata
- Global, tenant, and realm JWKS helpers

### Prohibited access

The UIX must fail closed on:

- tenant lifecycle and human user administration;
- human authentication sessions and consent;
- developer client/application registration;
- cryptographic key administration resources outside service-key ownership;
- public login, authorize, token issuance, registration, logout, revocation, and UserInfo as service-admin operations.

Introspection and validation metadata are permitted; token issuance is not owned by this UIX.

## 4. Required Experience

### Dashboard

- Show service identities, active/suspended services, active/expiring/revoked credentials, validation metadata status, and recent rotation/audit actions.
- Prioritize orphaned credentials, overbroad scope, near expiry, failed rotation, inactive service with active keys, and missing ownership when backed by data.
- Do not convert counts into a generic security score.

### Services and member routes

- Provide stable `#/services/{id}` member routes and explicit selection.
- Remove first-service implicit selection from all detail and credential views.
- Show name, immutable subject, tenant/scope, owner/team, purpose, environment, state, created/updated time, attached credentials, and recent use where contracted.
- Support create, inspect, update, activate/suspend, and delete only through explicit lifecycle operations.
- Explain whether suspension blocks authentication, validation, key use, or new issuance.
- Prevent deletion while active credentials or dependencies remain unless the API performs an explicit cascade with review.

### Service keys

- Bind every key to an explicit service identity.
- Show key ID, algorithm, state, creation, activation, expiry, last use, rotation relationship, and public fingerprint where available.
- Use supported algorithm choices from the contract/profile, not unrestricted text.
- Treat issue, activate, rotate, revoke, expire, and delete as separate lifecycle actions.
- Reveal generated secret/private material once only if the API returns it; never retrieve it again.
- Never render private key, envelope, or raw credential material in tables, logs, analytics, or screenshots.

### API keys

- Bind each API key to one service identity, owner/purpose, scopes/permissions, environment, expiry, and optional network constraints where contracted.
- Replace comma-separated scope entry with a structured permission selector sourced from policy/metadata.
- Generate key material server-side and show it once with copy/download acknowledgment.
- Display only a safe prefix/fingerprint after creation.
- Separate metadata edits from permission escalation; scope increases require additional review/authority.
- Explain revocation propagation and expected integration failure.

### Token records

- Render operationally useful, redacted records rather than raw token payloads.
- Show safe identifier/fingerprint, service subject, issuer, audience, scopes, issued/expiry time, state, and validation/usage outcome where permitted.
- Never show bearer token material, refresh tokens, authorization codes, or unnecessary personal claims.
- Add filtering, retention context, and explicit stale/expired/revoked states.
- If `TokenRecord` is an internal persistence artifact rather than an operator contract, replace the page with a purpose-built workload-token view before productizing it.

### Validation tools

- Start with an empty token input; never prefill a token-like credential outside an explicitly labeled fixture picker.
- Separate decode, signature validation, claims validation, introspection, and authorization decision.
- Show protected-resource metadata and the requirements applied: issuer, audience, scopes, time, token type, and sender constraints when supported.
- Redact token input immediately after submit or on navigation; never persist it.
- Present allow/deny plus safe reason codes and remediation without leaking sensitive claims.
- Include deterministic fixtures for valid, expired, wrong issuer/audience, missing scope, revoked, bad signature, and sender mismatch.

### Rotation events

- Show requested, generated, staged, activated, propagated, retiring, completed, and failed phases where available.
- Link old/new key IDs, service, actor, reason, timestamps, failure, retry, and audit correlation.
- Make clear that creating a key is not a completed zero-downtime rotation.

### Audit

- Enable a filtered workload audit view only when the API exposes it with ownership/isolation proof.
- Show actor, action, target service/credential, permission delta, outcome, timestamp, and correlation ID.
- Redact secrets, tokens, request bodies, and private claims.

## 5. Security and Operational Requirements

- Enforce server-side service ownership, tenant scope, and effective operator permissions on every collection/member/mutation.
- Encode resource identifiers and reject paths outside the service-admin allowlist.
- Never embed development administrator keys or workload secrets in built assets.
- Generate credential material using server-owned cryptography; the UI must not invent secrets unless explicitly designed and reviewed.
- Use one-time secret display with no persistence, telemetry, automatic copy, cached DOM retention, or screenshot fixture containing real material.
- Require consequence review for service suspension/deletion, key rotation/revocation, API-key scope increase, and credential expiry changes.
- Exclude service IDs, subjects, owners, scopes, key IDs, tokens, secrets, audit values, and validation inputs/results from analytics.
- Reconcile mutations from authoritative API state and preserve audit correlation.

## 6. Team Requirements

### Technical marketing

- Provide stable screenshots for service inventory, service detail, API-key issuance, service-key rotation, and validation failure.
- Demonstrate a machine-to-machine journey without exposing or fabricating real secrets.
- Label full lifecycle, last-use, rotation, audit, and sender-constraint capabilities by maturity/profile.
- Avoid “secretless,” “zero trust,” “automatic rotation,” or universal workload identity claims without exact proof.

### Developer relations

- Document isolated startup, workload-admin authentication, API contracts, seeded fixtures, reset, and safe teardown.
- Provide tested examples for service creation, credential issuance, protected call, introspection/validation, rotation, and revocation.
- Explain API keys versus service keys versus OAuth client credentials and when each is appropriate.
- Include expected failure behavior and productionization guidance for storage, rotation, expiry, monitoring, and incident response.

### Sales and account management

- Provide a resettable scenario: create service → issue scoped credential → validate request → rotate/revoke → observe denial/audit.
- Include “what this proves / what it does not prove” for rotation automation, HSM/KMS integration, workload federation, and hosted operations.
- Make environment, tenant, profile, version, fixture status, and known gaps visible.
- Provide a shareable evaluation summary containing no service identifiers or credentials.

### GTM strategy

- Position the pairing around governed non-human identity and observable credential lifecycle.
- Track privacy-safe journey/action category, outcome, fixture used, docs/evidence engagement, and handoff initiation.
- Never emit services, owners, scopes, identifiers, keys, token input, claims, validation output, or audit values.
- Use one taxonomy for workload identity, service key, API key, token validation, rotation, and audit.

### Copywriter

- Use “service identity,” “workload,” “service key,” “API key,” “scope/permission,” “introspection,” “validation,” “rotation,” and “revocation” consistently.
- Explain issue, activate, rotate, expire, revoke, suspend, and delete as distinct actions.
- Write one-time secret warnings and acknowledgments with clear recovery expectations.
- Avoid “safe,” “trusted,” “valid,” or “least privilege” without naming the exact evaluated condition.

## 7. Frontend Engineering Instructions

1. Replace first-service selection with explicit ID-based routes and selected-service state.
2. Generate or validate typed clients/forms against service-admin contracts and retain explicit allowlists.
3. Model service, key, API-key, and rotation lifecycles as explicit states and transitions.
4. Implement one-time secret handling as an isolated component that clears data on acknowledgment, timeout, navigation, and unmount.
5. Replace free-text service IDs, algorithms, scopes, and statuses with contract-backed selectors and validation.
6. Start validation input empty; fixtures must be selected intentionally and labeled as non-production.
7. Sanitize/redact token records and introspection output through tested field policies before rendering.
8. Add ownership/isolation, permission escalation, identifier encoding, secret persistence, redaction, and cross-tenant tests.
9. Add server-backed search/filter/pagination and retention messaging before claiming operational-scale token/audit views.
10. Keep dedicated Resource Validation UIX concerns separate: Service Admin governs workloads; Resource Validation configures protected-API enforcement.

## 8. UIX Designer Instructions

- Use the shared operational console with persistent tenant, environment, profile, operator, and selected-service context.
- Organize credentials beneath an explicit service identity and visualize dependencies before destructive action.
- Design safe one-time secret reveal, copy/download acknowledgment, and cleared state.
- Distinguish active, suspended, expiring, expired, rotating, revoked, failed, and unavailable without color alone.
- Present validation as a staged decision trace rather than an undifferentiated JSON dump.
- Provide empty inventory, first service, many services, orphaned credential, partial metadata, failed rotation, revoked key, and invalid token states.
- Validate keyboard interaction, focus restoration, live-region feedback, reduced motion, high zoom, and WCAG 2.2 AA.

## 9. Copy Deliverables

Produce a route-level copy deck containing:

- service ownership, purpose, lifecycle, suspension, and deletion language;
- service/API-key issuance, scope selection, one-time reveal, expiry, rotation, and revocation copy;
- token-record privacy/retention explanations;
- validation stages, safe denial reasons, fixture labels, and remediation;
- rotation phase, failure, retry, and completion language;
- audit, unauthorized, partial, stale, empty, offline, and support-correlation copy.

## 10. Acceptance Criteria

- The UIX calls only the service-admin API base URL and rejects tenant/user, human session/consent, developer client, key-admin, and public auth paths.
- Every detail and credential view binds to an explicit service ID; no first-record selection remains.
- Service/key/API-key lifecycle actions are stateful, permission-gated, consequence-led, and reconciled.
- Newly issued secrets are shown once and never persisted, logged, analyzed, or included in fixtures/screenshots.
- Validation starts with empty input, separates stages, redacts results, and includes deterministic positive/negative fixtures.
- Token records expose only a purpose-built, redacted operator view with retention context.
- Ownership/isolation, escalation, secret, redaction, contract, accessibility, responsive visual, and end-to-end tests pass.
- Resource Validation and Service Admin remain distinct product boundaries.

## 11. Source Evidence

- `pkgs/90-backend-apps/tigrbl-auth-backend-app-service-admin/README.md`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-service-admin/src/tigrbl_auth_backend_app_service_admin/contract.py`
- `pkgs/105-ui/service-admin-uix/README.md`
- `pkgs/105-ui/service-admin-uix/App.tsx`
- `pkgs/105-ui/service-admin-uix/services/serviceAdminClient.ts`
- `pkgs/105-ui/service-admin-uix/services/workflowCrud.test.ts`
- `pkgs/105-ui/service-admin-uix/pages/serviceCrudPages.test.tsx`
- `pkgs/105-ui/service-admin-uix/pages/ValidationToolsPage.tsx`
- `tests/packages/tigrbl-auth-backend-app-service-admin/`
- `tests/unit/test_product_api_surfaces.py`
- Service-admin SSOT feature/claim/test/evidence/boundary records
