# Developer API + UIX Requirements Brief

**Pairing:** `tigrbl-auth-backend-app-developer` + `@tigrbl-auth/developer-uix`<br>
**Status:** Delivery brief<br>
**Prepared:** July 11, 2026<br>
**Backend app owner:** `pkgs/90-backend-apps/tigrbl-auth-backend-app-developer`<br>
**UIX owner:** `pkgs/105-ui/developer-uix`

## 1. Product Decision

Deliver this pairing as the developer self-service portal for registering, configuring, integrating, testing, and maintaining OAuth/OIDC applications within an authorized tenant context.

The experience must organize the current route inventory into one application lifecycle: register → configure → obtain permitted credentials → integrate → test → monitor metadata → rotate or revoke. It is not a tenant lifecycle console, public authorization server, service-identity manager, or raw protocol workbench.

## 2. Users and Jobs

### Primary users

- Application developers integrating login or delegated authorization.
- Developer-platform engineers managing client registrations.
- Security reviewers validating redirect, grant, scope, and client-authentication configuration.

### Primary jobs

1. Register an OAuth/OIDC application.
2. Configure redirect URIs, response/grant types, scopes, and client authentication.
3. Obtain and safely handle client identifiers and newly issued credentials.
4. Generate tested integration snippets.
5. Run a safe authorization-code + PKCE test and understand failures.
6. Inspect issuer discovery/JWKS and application compatibility.
7. Update, rotate, disable, or delete a registration safely.

## 3. API Boundary

The UIX consumes exactly one configured developer API base URL through `VITE_TIGRBL_AUTH_DEVELOPER_API_BASE_URL`.

### Public developer capabilities

- Dynamic client registration and registration management
- OpenID Provider configuration at global, tenant, and realm scopes
- OAuth authorization-server metadata
- Global, tenant, and realm JWKS helpers

### Authenticated developer resources

- `Client`
- `ClientRegistration`
- Developer-filtered `AuditEvent` when exposed

### Prohibited access

The UIX must fail closed on:

- tenant lifecycle and tenant-wide user administration;
- authentication-session and consent administration;
- service identities, service keys, and API keys;
- cryptographic key administration and private key material;
- token/revoked-token storage tables;
- public login, authorize, token, logout, revoke, UserInfo, and introspection as developer-control-plane API operations.

The OAuth tester may navigate the browser to the discovered public authorization endpoint, but the Developer UIX client must not treat that endpoint as part of its own API boundary.

## 4. Required Experience

### Dashboard

- Show tenant/developer context, registered applications, configuration warnings, issuer discovery status, active profile, and version maturity.
- Prioritize incomplete or unsafe configuration: missing redirect, incompatible auth method, unsupported grant, or untested integration.
- Do not convert application counts into readiness/security scores.

### Applications and member routes

- Provide stable application collection and `#/apps/{id}` member routes.
- Never infer selection from the first collection item; all detail, metadata, redirect, credential, scope, and test views must bind to an explicit application ID.
- Reconcile `Client` and `ClientRegistration` representations into a clear developer concept while preserving source/provenance in technical details.
- Support create, inspect, edit, and delete only through contracted operations.

### Registration wizard

- Ask first for application type: browser/SPA, native, server web app, service/confidential client, or other contracted type.
- Derive safe defaults for redirect policy, PKCE, grant/response types, and token endpoint authentication from the type and active profile.
- Validate every field against discovery/OpenAPI metadata before submit.
- Present a review screen with the exact registration payload and security implications.
- Show newly issued secrets once, require acknowledgment, and provide recovery/rotation guidance.

### Redirect URIs

- Replace comma-separated free text with structured URI rows.
- Validate scheme, origin, fragment prohibition, wildcard policy, native loopback behavior, duplicates, and environment labels.
- Warn when a change can break active login integrations.
- Keep localhost exceptions visibly development-only.

### Client metadata and scopes

- Use select/combobox controls populated from supported metadata rather than unrestricted strings for auth methods, grants, responses, and scopes.
- Explain requested scopes in plain language and show their issuer source.
- Distinguish registered metadata, effective metadata, and discovery capabilities.
- Show unknown or no-longer-supported values without silently discarding them.

### Credentials and client JWKS

- The current credentials page marks management as planned; keep rotation/revocation actions disabled or absent until API operations exist.
- Display client ID as copyable non-secret data.
- Reveal newly issued secrets only once; never retrieve or display stored secrets later.
- Support client JWKS/JWKS URI and asymmetric client authentication only when contracted.
- Explain browser clients cannot hold client secrets.

### OAuth flow tester

- Replace the current basic authorization URL generator with a transaction-aware test harness.
- Generate cryptographically strong `state`, `nonce`, and PKCE verifier/challenge for applicable flows.
- Validate redirect URI against the selected registration.
- Show sanitized authorize, callback, and token-exchange stages; never expose reusable secrets or persist tokens.
- Offer expected negative cases: redirect mismatch, invalid state, expired code, wrong issuer, unsupported scope/grant, and PKCE mismatch.
- Clearly label simulated steps versus live calls.

### Discovery and integration snippets

- Render issuer, authorization/token endpoints, JWKS URI, supported scopes/grants/responses/auth methods, and profile/version context.
- Provide tested snippets for `@tigrbl-auth/rp` workspace usage, server-side Python, and curl where appropriate.
- Separate stable public install instructions from repository/prerelease instructions; reviewed npm packages are not currently public.
- Add expected output, productionization notes, copy feedback, and version markers.

### Deletion and revocation

- Distinguish deleting a client record, deleting registration metadata, disabling a client, and rotating/revoking credentials.
- Show affected redirect flows, integrations, grants, and recovery options before action.
- Do not offer a destructive action when the underlying representation or consequence is ambiguous.

## 5. Security and Privacy Requirements

- Enforce developer/tenant ownership server-side for every collection, member, update, and delete.
- Encode identifiers and reject paths outside the developer allowlist.
- Never embed development admin keys or client secrets in built assets.
- Exclude client secrets, private keys, PKCE verifiers, authorization codes, tokens, redirect transaction data, tenant IDs, and client IDs from analytics.
- Reject browser client secrets and unsafe token storage policies.
- Validate redirect and post-logout URIs on both client and server; client validation is guidance, not authorization.
- Use safe one-time secret presentation and prevent accidental inclusion in screenshots/logs.
- Preserve audit correlation for registration and credential-sensitive actions.

## 6. Team Requirements

### Technical marketing

- Provide stable screenshots for app registration, redirect validation, integration snippet, OAuth test, and discovery.
- Demonstrate a five-minute “register an app and complete login” journey using seeded data.
- Label credential rotation, client JWKS, and npm availability according to current maturity.
- Avoid “drop-in,” “zero configuration,” “all frameworks,” or universal OAuth/OIDC support claims.

### Developer relations

- Own the golden path, tested snippets, expected results, troubleshooting, reset, and production checklist.
- Document Docker startup, developer authentication, public versus admin registration routes, discovery, and local callback setup.
- Explain browser/native/server client differences, PKCE, state, nonce, redirect safety, and secret handling.
- Test examples in CI against the selected stable/prerelease matrix.

### Sales and account management

- Provide a resettable scenario: register app → validate redirect → copy configuration → run OAuth test → inspect discovery.
- Include “what this proves / what it does not prove,” especially around credential lifecycle, SDK publication, and production hosting.
- Make tenant, profile, version, environment, and demo data visible.
- Provide a shareable evaluation summary without credentials or identifiers.

### GTM strategy

- Position the pairing around developer self-service and safe integration, not generic IAM administration.
- Track privacy-safe registration/test step completion, error category, snippet language, docs/evidence engagement, and handoff initiation.
- Never capture registration payloads, URIs, identifiers, secrets, codes, tokens, or scopes in analytics.
- Use one taxonomy for application, registration, redirect, credential, scope, discovery, and OAuth test.

### Copywriter

- Prefer “application,” “client ID,” “redirect URI,” “client authentication,” “scope,” and “authorization test” consistently.
- Explain browser versus confidential clients and why browser secrets are unsafe.
- Write field help and errors that state how to fix an invalid redirect, grant, response type, scope, or auth method.
- Avoid “secure by default” unless the exact default/profile behavior is named and evidenced.

## 7. Frontend Engineering Instructions

1. Replace first-item selection with explicit ID-based routes and selected-application state.
2. Generate or validate typed clients/forms against developer OpenAPI, OpenRPC, and discovery metadata.
3. Convert comma-separated metadata fields into structured repeatable controls with per-item validation.
4. Build an application-type-driven registration wizard with profile-aware defaults and a review step.
5. Implement the OAuth tester as an ephemeral state machine with Web Crypto-generated state/nonce/PKCE and sanitized trace output.
6. Keep public authorization navigation separate from developer API requests and allowlisted by discovery.
7. Implement one-time secret rendering without persistence, telemetry, DOM retention after dismissal, or automatic copy.
8. Add contract drift, redirect policy, unsafe browser-secret, ownership, encoded-ID, and cross-tenant leakage tests.
9. Add snippet fixtures tested against published artifacts or explicitly labeled repository workspaces.
10. Keep credential rotation and client JWKS actions maturity-gated until API support and evidence exist.

## 8. UIX Designer Instructions

- Use a polished developer-console variant of the shared UIX system.
- Organize pages around one selected application and its lifecycle, with persistent tenant/environment/profile context.
- Design structured URI/scope/grant/auth-method editors, review screens, one-time secret handling, and protocol-step visualization.
- Distinguish configured, effective, unsupported, untested, warning, failed, and planned without color alone.
- Make code/snippet viewers readable, copyable, keyboard accessible, and mobile safe.
- Provide empty portal, first-app onboarding, many-app search, partial metadata, offline issuer, stale registration, and failed OAuth states.
- Validate focus management, live-region feedback, reduced motion, high zoom, and WCAG 2.2 AA.

## 9. Copy Deliverables

Produce a route-level copy deck containing:

- onboarding and application-type guidance;
- field labels/help/errors for redirects, grants, responses, scopes, and client authentication;
- secret reveal/acknowledgment, rotation maturity, and browser-secret warnings;
- OAuth test stages, negative cases, sanitized protocol details, and reset language;
- discovery and snippet explanations, expected results, productionization notes, and version caveats;
- deletion/disable/revoke impact, empty, partial, unauthorized, stale, offline, and support copy.

## 10. Acceptance Criteria

- The UIX calls only the developer API base URL and rejects tenant lifecycle, user, consent, service, key-admin, token, and raw session paths.
- Every application subview binds to an explicit client/registration ID; no first-record selection remains.
- Registration and metadata forms are structured and validated against active profile/contracts.
- Browser clients cannot select or retain client secrets.
- OAuth testing uses strong state, nonce, and PKCE; validates callback context; and never persists or emits sensitive data.
- Credential rotation/JWKS actions remain clearly planned until supported by the API.
- Stable versus prerelease/workspace snippets and package availability are accurately labeled.
- Ownership/isolation, contract, security, accessibility, responsive visual, and end-to-end integration tests pass.

## 11. Source Evidence

- `pkgs/90-backend-apps/tigrbl-auth-backend-app-developer/README.md`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-developer/src/tigrbl_auth_backend_app_developer/contract.py`
- `pkgs/105-ui/developer-uix/README.md`
- `pkgs/105-ui/developer-uix/App.tsx`
- `pkgs/105-ui/developer-uix/services/developerClient.ts`
- `pkgs/105-ui/developer-uix/services/backendSurface.ts`
- `pkgs/105-ui/developer-uix/services/workflowCrud.test.ts`
- `pkgs/105-ui/developer-uix/pages/developerCrudPages.test.tsx`
- `pkgs/105-ui/developer-uix/pages/OAuthFlowTesterPage.tsx`
- `tests/packages/tigrbl-auth-backend-app-developer/`
- `tests/unit/test_product_api_surfaces.py`
- Developer API/UIX SSOT feature/claim/test/evidence/boundary records
