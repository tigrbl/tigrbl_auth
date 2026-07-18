# Resource Validation API + UIX Requirements Brief

**Pairing:** `tigrbl-auth-backend-app-resource-validation` + proposed `@tigrbl-auth/resource-validation-uix`<br>
**Status:** New UIX required; API exists<br>
**Prepared:** July 11, 2026<br>
**Backend app owner:** `pkgs/90-backend-apps/tigrbl-auth-backend-app-resource-validation`<br>
**Proposed UIX owner:** `pkgs/105-ui/resource-validation-uix`

## 1. Product Decision

Create a dedicated Resource Validation UIX as an authenticated developer/operator workbench for understanding and testing protected-API token validation.

The underlying API is machine-facing and remains authoritative for issuer metadata, protected-resource metadata, JWKS, tenant JWKS, and authorized introspection. The UIX must not turn it into a public token-pasting service, token issuer, policy administration console, or generic JWT decoder.

Production resource servers and gateways consume the API directly. The UIX exists for configuration discovery, controlled testing, troubleshooting, demonstrations, and evidence—not as a request-path dependency.

## 2. Users and Jobs

### Primary users

- Protected-API developers integrating validation middleware.
- API gateway and platform engineers configuring issuers and audiences.
- Security engineers reviewing enforcement and rejection behavior.
- Developer Relations, sales engineers, and evaluators running deterministic demonstrations.

### Primary jobs

1. Discover issuer and protected-resource validation metadata.
2. Inspect global or tenant public signing keys.
3. Define a validation test expectation: issuer, audience, scopes/permissions, time, token type, and sender constraint.
4. Run authorized introspection or deterministic local fixture validation.
5. Understand which validation stage allowed or denied a request.
6. Generate copyable resource-server/gateway configuration.
7. Reproduce representative rejection cases safely.

## 3. API Boundary

The UIX consumes exactly one configured resource-validation backend-app base URL.

### Owned capabilities

- `/.well-known/openid-configuration`
- Tenant OpenID Provider configuration where exposed
- `/.well-known/oauth-protected-resource`
- `/.well-known/jwks.json`
- `/tenants/{tenant_slug}/.well-known/jwks.json`
- Authorized `/introspect`

### Prohibited access

The UIX must fail closed on:

- `/admin*` and diagnostics;
- tenant lifecycle and tenant administration;
- dynamic client registration;
- cryptographic key administration, key envelopes, and attestation resources;
- login, authorization, token issuance, logout, revocation, UserInfo, device authorization, PAR, and token exchange;
- `/rpc` and generic table/resource operations.

The UIX may read public key material from JWKS. It must never request, infer, or display private key material.

## 4. Deployment Model

The UIX has two modes:

### Static metadata mode

- Reads discovery, protected-resource metadata, and JWKS.
- Generates configuration guidance and displays deterministic fixtures.
- May be available in a documentation/demo environment without introspection credentials.

### Authenticated validation mode

- Requires an authorized operator/developer session or server-mediated credential.
- Enables introspection and live validation tests.
- Must never embed introspection credentials in browser bundles.
- Should use a backend-for-frontend or same-origin authenticated session when confidential client authentication is required.

The UIX must never sit in the protected API’s production request path.

## 5. Required Experience

### Overview and health

- Show API endpoint, environment, version/profile, issuer, protected-resource identifier, metadata/JWKS reachability, and last refresh.
- Distinguish reachable metadata from a validated production configuration.
- Show static versus authenticated mode clearly.

### Metadata explorer

- Render issuer, authorization/introspection endpoints, JWKS URI, protected-resource identifier, supported authorization servers, scopes, bearer methods, and sender-constraint metadata when present.
- Provide human explanation and raw JSON with provenance, fetch time, cache state, and copy controls.
- Validate consistency among issuer, metadata URL, protected-resource metadata, and JWKS URI.
- Show missing, malformed, stale, contradictory, and cross-origin failure states.

### JWKS explorer

- Support global and tenant-scoped key sets.
- Show public `kid`, `kty`, `alg`, `use`, curve/modulus summary, and safe fingerprint.
- Flag duplicate `kid`, unsupported algorithm, malformed key, empty key set, and expected-key-not-found conditions.
- Explain key rollover overlap without asserting private-key or signing-system health.
- Never display raw private parameters even if a malformed upstream response includes them; fail closed and raise a high-severity warning.

### Verifier configuration builder

- Capture expected issuer, resource/audience, scopes/permissions, algorithms, clock tolerance, tenant, token type, introspection/JWKS strategy, and sender constraints only where supported.
- Source choices from live metadata/profile and distinguish required, recommended, and unsupported values.
- Generate copyable configuration for `tigrbl-authz-resource-server`, Python middleware examples, and common gateway formats where maintained.
- Mark generated configuration with package/version/profile compatibility and productionization notes.
- This builder does not save or mutate runtime policy unless a future, separately owned configuration API exists.

### Validation workbench

- Start with no token value. Offer deterministic fixture selection separately.
- Accept pasted input only after a privacy warning; never persist it or include it in URLs, telemetry, logs, support payloads, browser history, or screenshots.
- Clear input on submit, navigation, timeout, and unmount while retaining only a safe result summary.
- Separate stages:
  1. input/type recognition;
  2. metadata/issuer resolution;
  3. key or introspection selection;
  4. signature/status validation;
  5. temporal claim validation;
  6. issuer/audience validation;
  7. scope/permission validation;
  8. sender-constraint validation where applicable;
  9. final allow/deny result.
- Show safe reason codes and remediation without exposing reusable claims or credential material.

### Deterministic fixtures

Include isolated, non-production fixtures for:

- valid token;
- expired and not-yet-valid token;
- wrong issuer;
- wrong audience/resource;
- missing required scope/permission;
- invalid signature or unknown `kid`;
- revoked/inactive introspection result;
- malformed token;
- sender-constraint mismatch where supported.

Every fixture must state expected stage/result and be resettable.

### Evidence and export

- Provide a sanitized validation summary with environment, profile, metadata fingerprints, configured requirements, fixture category, stage results, timestamp, and correlation ID.
- Export must never contain the token, full claims, credentials, personal data, private keys, or secrets.
- Link capability statements to applicable claim/test/evidence/release context without presenting a test run as universal certification.

## 6. Security and Privacy Requirements

- Never embed confidential introspection credentials or development secrets in frontend assets.
- Prefer same-origin authenticated requests or a narrowly scoped backend-for-frontend for introspection.
- Do not persist tokens or full validation results in local/session storage, IndexedDB, cache storage, service workers, URLs, telemetry, or error reporting.
- Redact authorization headers and token-like values before rendering/logging any error.
- Treat pasted tokens and claims as sensitive data even in local development.
- Enforce endpoint allowlists; do not permit arbitrary server-side URL fetches that introduce SSRF.
- Tenant slug selection must not enable cross-tenant private data access; JWKS and metadata remain public-contract reads only.
- Use deterministic repository-owned fixtures for screenshots and demonstrations.

## 7. Team Requirements

### Technical marketing

- Provide stable screenshots for metadata, JWKS rollover, successful validation, wrong audience, and missing scope.
- Demonstrate “protect an API” with deterministic fixtures and a sanitized decision trace.
- Label local validation, introspection, sender constraints, and profile coverage precisely.
- Avoid “any token,” “zero trust,” “complete validation,” or universal gateway support claims.

### Developer relations

- Own the quickstart from API startup through metadata inspection, verifier configuration, protected request, allow/deny, and troubleshooting.
- Provide tested Python/resource-server and gateway examples with expected output.
- Explain JWKS versus introspection, cache/rollover, issuer/audience/scope, clock skew, and sender constraints.
- Include deterministic fixtures, reset, local TLS exceptions, and productionization guidance.

### Sales and account management

- Provide a guided scenario: inspect metadata → configure audience/scope → validate success → demonstrate representative denial → export safe summary.
- Include “what this proves / what it does not prove,” particularly for gateway integration, throughput, external interoperability, and certification.
- Make profile, version, environment, fixture status, and static/authenticated mode visible.
- Never ask prospects to paste real production tokens into a demo.

### GTM strategy

- Position the pairing around inspectable API protection and explainable denial.
- Track privacy-safe mode, fixture category, stage reached, allow/deny category, docs/evidence engagement, and handoff initiation.
- Never emit endpoint values, tenant slugs, audiences, scopes, keys, tokens, claims, configurations, or raw validation output.
- Use one taxonomy for issuer, protected resource, JWKS, introspection, audience, scope, sender constraint, and decision.

### Copywriter

- Distinguish decode, verify signature, check status, validate claims, and authorize access.
- Use “allowed by this configured test” rather than calling a token universally valid.
- Explain denial reasons without exposing claims or suggesting unsafe bypasses.
- Avoid “secure,” “trusted,” “certified,” or “compliant” unless tied to exact scoped evidence.

## 8. Frontend Engineering Instructions

1. Scaffold `pkgs/105-ui/resource-validation-uix` using `@tigrbl-auth/uix-core` and a single resource-validation base URL.
2. Implement strict endpoint/method allowlists matching `RESOURCE_VALIDATION_BACKEND_APP_CONTRACT`.
3. Separate static metadata mode from authenticated introspection mode at routing, capability, and deployment layers.
4. Use a server-mediated session for confidential introspection authentication; never ship credentials to the browser.
5. Build token input as an ephemeral secret component with paste warning, immediate clearing, and redaction tests.
6. Normalize metadata/JWKS/introspection into typed, sanitized view models; never render upstream JSON directly without redaction.
7. Prevent arbitrary metadata URL entry or constrain it through an explicit trusted-issuer allowlist to avoid SSRF/open-proxy behavior.
8. Build deterministic fixtures and expected stage assertions into automated tests.
9. Generate versioned snippets from maintained templates and test them against the supported package matrix.
10. Integrate exact routes into Demo Hub while keeping this UIX independently deployable and statically fallible.

## 9. UIX Designer Instructions

- Use a developer-tool variant of the shared UIX system with persistent environment/profile/mode context.
- Visualize validation as a compact stage sequence with evidence and remediation, not a decorative flowchart.
- Design metadata and JWKS summaries with progressive raw-detail disclosure.
- Distinguish pass, deny, unavailable, skipped, unsupported, stale, and warning without color alone.
- Make pasted-token privacy and fixture status impossible to miss.
- Provide responsive layouts for initial/empty, metadata unavailable, malformed JWKS, valid fixture, each denial family, offline, and expired authenticated mode.
- Validate keyboard operation, focus restoration, screen-reader stage announcements, reduced motion, high zoom, and WCAG 2.2 AA.

## 10. Copy Deliverables

Produce a route-level copy deck containing:

- static/authenticated mode explanations;
- issuer/protected-resource/JWKS/introspection field help;
- verifier configuration requirements and compatibility caveats;
- token privacy warning, fixture labels, validation stages, safe reason codes, and remediation;
- export/evidence scope and “what this proves” language;
- unavailable, stale, malformed, forbidden, offline, timeout, and support-correlation copy.

## 11. Acceptance Criteria

- A dedicated Resource Validation UIX package exists or an explicit documented no-UI decision replaces this brief.
- The UIX calls only metadata, JWKS, and authorized introspection routes from the resource-validation API.
- Static and authenticated modes are separated; no confidential credential reaches the browser bundle.
- Token input starts empty, is never persisted or analyzed, and is cleared after use.
- Validation is presented in distinct stages with safe allow/deny reasons and deterministic fixtures.
- Metadata/JWKS/introspection output is typed, redacted, provenance-aware, and tested against malformed/private data.
- Generated configurations/snippets are version/profile labeled and CI-tested.
- Boundary, SSRF, secret, redaction, fixture, accessibility, responsive visual, and end-to-end tests pass.
- Demo Hub links to an exact Resource Validation UIX route instead of only raw API documentation.

## 12. Source Evidence

- `pkgs/90-backend-apps/tigrbl-auth-backend-app-resource-validation/README.md`
- `pkgs/90-backend-apps/tigrbl-auth-backend-app-resource-validation/src/tigrbl_auth_backend_app_resource_validation/contract.py`
- `docker/docker-compose.resource-validation-app.yml`
- `pkgs/105-ui/demo-hub-uix/surfaces.ts`
- `pkgs/105-ui/demo-hub-uix/demoState.ts`
- Resource-validation API unit/integration/conformance tests
- `tigrbl-authz-resource-server` package and verifier contract tests
- Resource-validation SSOT feature/claim/test/evidence/boundary records
